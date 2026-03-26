"""A* search through mathematical tool-space for olympiad problem solving.

Core idea (from Geometric Reasoning framework):
  - Reasoning is search on a manifold
  - States = partial mathematical knowledge about the problem
  - Operators = mathematical tools (SymPy, number theory, structural fuzzing)
  - Heuristic field h(x) = estimated distance to a concrete integer answer
  - A* finds the geodesic (optimal tool-application path) from problem → answer

This replaces LLM chain-of-thought with principled search through tool invocations.
"""

from __future__ import annotations

import heapq
import math
import re
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Optional, Any
from fractions import Fraction

import numpy as np


# =============================================================================
# TASK 1: STATE REPRESENTATION
# =============================================================================

class ValueType(Enum):
    """Types of mathematical values we can track."""
    INTEGER = auto()
    RATIONAL = auto()
    EXPRESSION = auto()  # symbolic
    SET = auto()         # set of values
    SEQUENCE = auto()    # ordered list
    MODULAR = auto()     # (value, modulus) pair
    UNKNOWN = auto()


@dataclass(frozen=False)
class MathValue:
    """A named mathematical value with type information."""
    name: str
    value: Any
    vtype: ValueType = ValueType.UNKNOWN
    provenance: str = ""  # which tool produced this

    def __repr__(self):
        return f"{self.name}={self.value} ({self.vtype.name})"


@dataclass
class SearchState:
    """State in the A* search through tool-space.

    Represents what we currently know about the problem:
    - Extracted quantities from the problem text
    - Intermediate computation results
    - Constraints and relationships
    - The current best candidate answer
    """
    # Known values (name -> MathValue)
    values: dict[str, MathValue] = field(default_factory=dict)

    # Constraints discovered (e.g., "answer mod 1000", "0 <= answer <= 99999")
    constraints: list[str] = field(default_factory=list)

    # The candidate answer (None if not yet found)
    candidate_answer: Optional[int] = None

    # Confidence in the candidate (0-1)
    answer_confidence: float = 0.0

    # Path cost g(x): number of tool applications so far
    g_cost: float = 0.0

    # Tools already applied (to avoid cycles)
    applied_tools: tuple[str, ...] = ()

    # Parent state (for path reconstruction)
    parent: Optional[SearchState] = None

    # Which tool produced this state
    producing_tool: str = ""

    def __lt__(self, other):
        """For heapq ordering."""
        return self.g_cost < other.g_cost

    def clone(self) -> SearchState:
        """Create a mutable copy of this state."""
        return SearchState(
            values=dict(self.values),
            constraints=list(self.constraints),
            candidate_answer=self.candidate_answer,
            answer_confidence=self.answer_confidence,
            g_cost=self.g_cost,
            applied_tools=self.applied_tools,
            parent=self,
            producing_tool="",
        )

    def state_key(self) -> str:
        """Hash key for cycle detection."""
        vals = tuple(sorted((k, repr(v.value)) for k, v in self.values.items()))
        return f"{vals}|{self.candidate_answer}|{self.applied_tools}"

    def has_value(self, name: str) -> bool:
        return name in self.values

    def get_value(self, name: str, default=None):
        if name in self.values:
            return self.values[name].value
        return default

    def set_value(self, name: str, value: Any, vtype: ValueType = ValueType.UNKNOWN,
                  provenance: str = ""):
        self.values[name] = MathValue(name=name, value=value, vtype=vtype,
                                       provenance=provenance)


# =============================================================================
# TASK 2: OPERATOR / TOOL REGISTRY
# =============================================================================

@dataclass
class ToolOperator:
    """A mathematical tool that can be applied to a state.

    Each tool has:
    - name: unique identifier
    - precondition: function(state) -> bool, can this tool be applied?
    - apply: function(state) -> list[SearchState], what new states does it produce?
    - cost: how expensive is this tool (for g_cost)
    - category: for organizing tools
    """
    name: str
    precondition: Callable[[SearchState], bool]
    apply: Callable[[SearchState], list[SearchState]]
    cost: float = 1.0
    category: str = "general"
    description: str = ""


class ToolRegistry:
    """Registry of all available mathematical tools."""

    def __init__(self):
        self.tools: list[ToolOperator] = []
        self._register_all_tools()

    def _register_all_tools(self):
        """Register all available mathematical tools."""

        # --- EXTRACTION TOOLS (parse problem text) ---

        self.tools.append(ToolOperator(
            name="extract_modular_power",
            precondition=lambda s: (
                s.has_value("problem_text")
                and not s.has_value("base")
                and _has_power_mod_pattern(s.get_value("problem_text"))
            ),
            apply=self._apply_extract_modular_power,
            cost=0.5,
            category="extraction",
            description="Extract base^exp mod m from problem text",
        ))

        self.tools.append(ToolOperator(
            name="extract_last_digits",
            precondition=lambda s: (
                s.has_value("problem_text")
                and not s.has_value("base")
                and _has_last_digits_pattern(s.get_value("problem_text"))
            ),
            apply=self._apply_extract_last_digits,
            cost=0.5,
            category="extraction",
            description="Extract 'last N digits of base^exp' pattern",
        ))

        self.tools.append(ToolOperator(
            name="extract_fibonacci",
            precondition=lambda s: (
                s.has_value("problem_text")
                and not s.has_value("fib_n")
                and _has_fibonacci_pattern(s.get_value("problem_text"))
            ),
            apply=self._apply_extract_fibonacci,
            cost=0.5,
            category="extraction",
            description="Extract Fibonacci F(n) mod m pattern",
        ))

        self.tools.append(ToolOperator(
            name="extract_sequence_pattern",
            precondition=lambda s: (
                s.has_value("problem_text")
                and not s.has_value("sequence_type")
                and _has_sequence_pattern(s.get_value("problem_text"))
            ),
            apply=self._apply_extract_sequence,
            cost=0.5,
            category="extraction",
            description="Extract sequence/recurrence from problem text",
        ))

        self.tools.append(ToolOperator(
            name="extract_remainder",
            precondition=lambda s: (
                s.has_value("problem_text")
                and not s.has_value("base")
                and _has_remainder_pattern(s.get_value("problem_text"))
            ),
            apply=self._apply_extract_remainder,
            cost=0.5,
            category="extraction",
            description="Extract 'remainder when X divided by Y' pattern",
        ))

        # --- NUMBER THEORY TOOLS ---

        self.tools.append(ToolOperator(
            name="compute_modular_power",
            precondition=lambda s: (
                s.has_value("base") and s.has_value("exponent") and s.has_value("modulus")
                and not s.has_value("mod_result")
            ),
            apply=self._apply_modular_power,
            cost=1.0,
            category="number_theory",
            description="Compute base^exp mod m using Python's pow()",
        ))

        self.tools.append(ToolOperator(
            name="detect_power_periodicity",
            precondition=lambda s: (
                s.has_value("base") and s.has_value("modulus")
                and not s.has_value("period")
            ),
            apply=self._apply_detect_periodicity,
            cost=1.0,
            category="number_theory",
            description="Find period of base^n mod m sequence",
        ))

        self.tools.append(ToolOperator(
            name="apply_periodicity",
            precondition=lambda s: (
                s.has_value("period") and s.has_value("exponent")
                and s.has_value("repeating_block")
                and not s.has_value("mod_result")
            ),
            apply=self._apply_use_periodicity,
            cost=0.5,
            category="number_theory",
            description="Use discovered period to compute answer",
        ))

        self.tools.append(ToolOperator(
            name="factorize",
            precondition=lambda s: (
                s.has_value("modulus") and not s.has_value("modulus_factors")
                and isinstance(s.get_value("modulus"), int)
                and s.get_value("modulus") < 10**8
            ),
            apply=self._apply_factorize,
            cost=1.0,
            category="number_theory",
            description="Factorize the modulus",
        ))

        self.tools.append(ToolOperator(
            name="euler_totient",
            precondition=lambda s: (
                s.has_value("modulus_factors") and not s.has_value("totient")
            ),
            apply=self._apply_euler_totient,
            cost=0.5,
            category="number_theory",
            description="Compute Euler's totient from factorization",
        ))

        self.tools.append(ToolOperator(
            name="apply_fermats_little",
            precondition=lambda s: (
                s.has_value("base") and s.has_value("exponent")
                and s.has_value("modulus") and s.has_value("totient")
                and not s.has_value("reduced_exponent")
            ),
            apply=self._apply_fermats,
            cost=0.5,
            category="number_theory",
            description="Reduce exponent using Euler's theorem: a^phi(m) = 1 mod m",
        ))

        # --- FIBONACCI / PISANO ---

        self.tools.append(ToolOperator(
            name="find_pisano_period",
            precondition=lambda s: (
                s.has_value("fib_n") and s.has_value("fib_modulus")
                and not s.has_value("pisano_period")
            ),
            apply=self._apply_pisano,
            cost=2.0,
            category="fibonacci",
            description="Find Pisano period pi(m) for Fibonacci mod m",
        ))

        self.tools.append(ToolOperator(
            name="compute_fib_via_pisano",
            precondition=lambda s: (
                s.has_value("fib_n") and s.has_value("fib_modulus")
                and s.has_value("pisano_period")
                and not s.has_value("fib_result")
            ),
            apply=self._apply_fib_via_pisano,
            cost=1.0,
            category="fibonacci",
            description="Compute F(n) mod m using Pisano period reduction",
        ))

        self.tools.append(ToolOperator(
            name="compute_fib_matrix",
            precondition=lambda s: (
                s.has_value("fib_n") and s.has_value("fib_modulus")
                and not s.has_value("fib_result")
            ),
            apply=self._apply_fib_matrix,
            cost=1.5,
            category="fibonacci",
            description="Compute F(n) mod m via matrix exponentiation",
        ))

        # --- SEQUENCE ANALYSIS ---

        self.tools.append(ToolOperator(
            name="compute_small_cases",
            precondition=lambda s: (
                s.has_value("sequence_fn") and not s.has_value("sequence_values")
            ),
            apply=self._apply_compute_small_cases,
            cost=1.0,
            category="sequence",
            description="Compute first N terms of a sequence",
        ))

        self.tools.append(ToolOperator(
            name="detect_recurrence",
            precondition=lambda s: (
                s.has_value("sequence_values") and not s.has_value("recurrence")
            ),
            apply=self._apply_detect_recurrence,
            cost=1.0,
            category="sequence",
            description="Detect linear recurrence from sequence values",
        ))

        self.tools.append(ToolOperator(
            name="extend_recurrence",
            precondition=lambda s: (
                s.has_value("recurrence") and s.has_value("sequence_values")
                and s.has_value("target_n")
                and not s.has_value("sequence_answer")
            ),
            apply=self._apply_extend_recurrence,
            cost=1.0,
            category="sequence",
            description="Extend sequence to target_n using discovered recurrence",
        ))

        self.tools.append(ToolOperator(
            name="detect_sequence_periodicity",
            precondition=lambda s: (
                s.has_value("sequence_values")
                and not s.has_value("seq_period")
                and not s.has_value("recurrence")
            ),
            apply=self._apply_detect_seq_periodicity,
            cost=1.0,
            category="sequence",
            description="Detect periodicity in sequence values",
        ))

        # --- ANSWER FINALIZATION ---

        self.tools.append(ToolOperator(
            name="finalize_mod_result",
            precondition=lambda s: (
                s.has_value("mod_result") and s.candidate_answer is None
            ),
            apply=self._apply_finalize_mod,
            cost=0.1,
            category="finalize",
            description="Set mod_result as the final answer",
        ))

        self.tools.append(ToolOperator(
            name="finalize_fib_result",
            precondition=lambda s: (
                s.has_value("fib_result") and s.candidate_answer is None
            ),
            apply=self._apply_finalize_fib,
            cost=0.1,
            category="finalize",
            description="Set fib_result as the final answer",
        ))

        self.tools.append(ToolOperator(
            name="finalize_sequence_answer",
            precondition=lambda s: (
                s.has_value("sequence_answer") and s.candidate_answer is None
            ),
            apply=self._apply_finalize_sequence,
            cost=0.1,
            category="finalize",
            description="Set sequence_answer as the final answer",
        ))

    # --- TOOL IMPLEMENTATIONS ---

    def _apply_extract_modular_power(self, state: SearchState) -> list[SearchState]:
        text = state.get_value("problem_text")
        results = []
        patterns = [
            # a^{b} mod c, a^b mod c
            (r'(\d+)\s*[\^]\s*[{]?(\d+)[}]?\s*(?:\\pmod|\\bmod|\\mod|mod)\s*[{]?(\d+)[}]?', False),
            # a^{b} (mod c)
            (r'(\d+)\s*[\^]\s*[{]?(\d+)[}]?\s*\(\s*(?:mod|\\bmod)\s+(\d+)\s*\)', False),
        ]
        for pattern, _ in patterns:
            for match in re.finditer(pattern, text):
                s = state.clone()
                s.set_value("base", int(match.group(1)), ValueType.INTEGER, "extract_modular_power")
                s.set_value("exponent", int(match.group(2)), ValueType.INTEGER, "extract_modular_power")
                s.set_value("modulus", int(match.group(3)), ValueType.INTEGER, "extract_modular_power")
                s.producing_tool = "extract_modular_power"
                s.applied_tools = state.applied_tools + ("extract_modular_power",)
                s.g_cost = state.g_cost + 0.5
                results.append(s)
        return results

    def _apply_extract_last_digits(self, state: SearchState) -> list[SearchState]:
        text = state.get_value("problem_text").lower()
        results = []
        word_map = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                     "six": 6, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
        for match in re.finditer(r'last\s+(\w+)\s+digits?\s+of\s+(\d+)\s*[\^]\s*[{]?(\d+)', text):
            n_str, base, exp = match.group(1), match.group(2), match.group(3)
            n_digits = word_map.get(n_str)
            if n_digits is None:
                try:
                    n_digits = int(n_str)
                except ValueError:
                    continue
            s = state.clone()
            s.set_value("base", int(base), ValueType.INTEGER, "extract_last_digits")
            s.set_value("exponent", int(exp), ValueType.INTEGER, "extract_last_digits")
            s.set_value("modulus", 10 ** n_digits, ValueType.INTEGER, "extract_last_digits")
            s.producing_tool = "extract_last_digits"
            s.applied_tools = state.applied_tools + ("extract_last_digits",)
            s.g_cost = state.g_cost + 0.5
            results.append(s)
        return results

    def _apply_extract_fibonacci(self, state: SearchState) -> list[SearchState]:
        text = state.get_value("problem_text")
        results = []
        # F(N) mod M, F_{N} mod M
        for match in re.finditer(r'[fF]\s*[_({\[]?\s*(\d+)\s*[_)}\]]?', text):
            n = int(match.group(1))
            mod_match = re.search(r'(?:mod|\\pmod|\\bmod)\s*[{]?(\d+)[}]?', text)
            if mod_match:
                m = int(mod_match.group(1))
                s = state.clone()
                s.set_value("fib_n", n, ValueType.INTEGER, "extract_fibonacci")
                s.set_value("fib_modulus", m, ValueType.INTEGER, "extract_fibonacci")
                s.producing_tool = "extract_fibonacci"
                s.applied_tools = state.applied_tools + ("extract_fibonacci",)
                s.g_cost = state.g_cost + 0.5
                results.append(s)
                break
        return results

    def _apply_extract_sequence(self, state: SearchState) -> list[SearchState]:
        text = state.get_value("problem_text").lower()
        results = []

        # Look for recurrence definitions like a(n) = ... a(n-1) ...
        rec_match = re.search(
            r'a\s*\(\s*n\s*\)\s*=\s*(.+?)(?:for|where|with|,\s*a\s*\()', text
        )
        if rec_match:
            s = state.clone()
            s.set_value("sequence_type", "recurrence", ValueType.EXPRESSION, "extract_sequence")
            s.set_value("sequence_def", rec_match.group(1).strip(), ValueType.EXPRESSION, "extract_sequence")
            s.producing_tool = "extract_sequence"
            s.applied_tools = state.applied_tools + ("extract_sequence",)
            s.g_cost = state.g_cost + 0.5
            results.append(s)

        # Domino tiling / combinatorial counting
        if "tiling" in text or "domino" in text:
            # Extract target N
            n_match = re.search(r'(\d+)\s*(?:by|x|×)', text)
            if n_match:
                target_n = int(n_match.group(1))
                s = state.clone()
                s.set_value("sequence_type", "tiling", ValueType.EXPRESSION, "extract_sequence")
                s.set_value("target_n", target_n, ValueType.INTEGER, "extract_sequence")

                # Domino tiling of 2xN is Fibonacci-like
                def tiling(n):
                    if n <= 0: return 0
                    if n == 1: return 1
                    if n == 2: return 2
                    a, b = 1, 2
                    for _ in range(3, n + 1):
                        a, b = b, a + b
                    return b
                s.set_value("sequence_fn", tiling, ValueType.EXPRESSION, "extract_sequence")
                s.producing_tool = "extract_sequence"
                s.applied_tools = state.applied_tools + ("extract_sequence",)
                s.g_cost = state.g_cost + 0.5
                results.append(s)

        return results

    def _apply_extract_remainder(self, state: SearchState) -> list[SearchState]:
        text = state.get_value("problem_text").lower()
        results = []
        for match in re.finditer(
            r'remainder\s+when\s+(\d+)\s*[\^]\s*[{]?(\d+)[}]?\s+is\s+divided\s+by\s+(\d+)', text
        ):
            s = state.clone()
            s.set_value("base", int(match.group(1)), ValueType.INTEGER, "extract_remainder")
            s.set_value("exponent", int(match.group(2)), ValueType.INTEGER, "extract_remainder")
            s.set_value("modulus", int(match.group(3)), ValueType.INTEGER, "extract_remainder")
            s.producing_tool = "extract_remainder"
            s.applied_tools = state.applied_tools + ("extract_remainder",)
            s.g_cost = state.g_cost + 0.5
            results.append(s)
        return results

    def _apply_modular_power(self, state: SearchState) -> list[SearchState]:
        base = state.get_value("base")
        exp = state.get_value("exponent")
        mod = state.get_value("modulus")
        result = pow(base, exp, mod)
        s = state.clone()
        s.set_value("mod_result", result, ValueType.INTEGER, "compute_modular_power")
        s.answer_confidence = 1.0
        s.producing_tool = "compute_modular_power"
        s.applied_tools = state.applied_tools + ("compute_modular_power",)
        s.g_cost = state.g_cost + 1.0
        return [s]

    def _apply_detect_periodicity(self, state: SearchState) -> list[SearchState]:
        base = state.get_value("base")
        mod = state.get_value("modulus")
        values = [pow(base, n, mod) for n in range(1, min(mod + 1, 500))]

        from structural_explorer import detect_periodicity
        period_info = detect_periodicity(values)

        if period_info and period_info["confidence"] > 0.5:
            s = state.clone()
            s.set_value("period", period_info["period"], ValueType.INTEGER, "detect_power_periodicity")
            s.set_value("repeating_block", period_info["repeating_block"], ValueType.SEQUENCE, "detect_power_periodicity")
            s.set_value("period_offset", period_info["offset"], ValueType.INTEGER, "detect_power_periodicity")
            s.producing_tool = "detect_power_periodicity"
            s.applied_tools = state.applied_tools + ("detect_power_periodicity",)
            s.g_cost = state.g_cost + 1.0
            return [s]
        return []

    def _apply_use_periodicity(self, state: SearchState) -> list[SearchState]:
        period = state.get_value("period")
        exp = state.get_value("exponent")
        block = state.get_value("repeating_block")
        offset = state.get_value("period_offset", 0)
        idx = (exp - 1 - offset) % period
        result = block[idx]
        s = state.clone()
        s.set_value("mod_result", result, ValueType.INTEGER, "apply_periodicity")
        s.answer_confidence = 1.0
        s.producing_tool = "apply_periodicity"
        s.applied_tools = state.applied_tools + ("apply_periodicity",)
        s.g_cost = state.g_cost + 0.5
        return [s]

    def _apply_factorize(self, state: SearchState) -> list[SearchState]:
        mod = state.get_value("modulus")
        from sympy import factorint
        factors = factorint(mod)
        s = state.clone()
        s.set_value("modulus_factors", factors, ValueType.EXPRESSION, "factorize")
        s.producing_tool = "factorize"
        s.applied_tools = state.applied_tools + ("factorize",)
        s.g_cost = state.g_cost + 1.0
        return [s]

    def _apply_euler_totient(self, state: SearchState) -> list[SearchState]:
        factors = state.get_value("modulus_factors")
        totient = 1
        for p, e in factors.items():
            totient *= (p - 1) * (p ** (e - 1))
        s = state.clone()
        s.set_value("totient", totient, ValueType.INTEGER, "euler_totient")
        s.producing_tool = "euler_totient"
        s.applied_tools = state.applied_tools + ("euler_totient",)
        s.g_cost = state.g_cost + 0.5
        return [s]

    def _apply_fermats(self, state: SearchState) -> list[SearchState]:
        base = state.get_value("base")
        exp = state.get_value("exponent")
        mod = state.get_value("modulus")
        totient = state.get_value("totient")

        # Check gcd(base, mod) == 1
        if math.gcd(base, mod) != 1:
            return []

        reduced = exp % totient
        result = pow(base, reduced, mod)
        s = state.clone()
        s.set_value("reduced_exponent", reduced, ValueType.INTEGER, "apply_fermats_little")
        s.set_value("mod_result", result, ValueType.INTEGER, "apply_fermats_little")
        s.answer_confidence = 1.0
        s.producing_tool = "apply_fermats_little"
        s.applied_tools = state.applied_tools + ("apply_fermats_little",)
        s.g_cost = state.g_cost + 0.5
        return [s]

    def _apply_pisano(self, state: SearchState) -> list[SearchState]:
        m = state.get_value("fib_modulus")
        from structural_explorer import find_pisano_period
        pisano = find_pisano_period(m)
        if pisano is not None:
            s = state.clone()
            s.set_value("pisano_period", pisano, ValueType.INTEGER, "find_pisano_period")
            s.producing_tool = "find_pisano_period"
            s.applied_tools = state.applied_tools + ("find_pisano_period",)
            s.g_cost = state.g_cost + 2.0
            return [s]
        return []

    def _apply_fib_via_pisano(self, state: SearchState) -> list[SearchState]:
        n = state.get_value("fib_n")
        m = state.get_value("fib_modulus")
        pisano = state.get_value("pisano_period")
        reduced = n % pisano

        # Compute F(reduced) mod m
        if reduced <= 1:
            result = reduced
        else:
            a, b = 0, 1
            for _ in range(2, reduced + 1):
                a, b = b, (a + b) % m
            result = b

        s = state.clone()
        s.set_value("fib_result", result, ValueType.INTEGER, "compute_fib_via_pisano")
        s.answer_confidence = 1.0
        s.producing_tool = "compute_fib_via_pisano"
        s.applied_tools = state.applied_tools + ("compute_fib_via_pisano",)
        s.g_cost = state.g_cost + 1.0
        return [s]

    def _apply_fib_matrix(self, state: SearchState) -> list[SearchState]:
        n = state.get_value("fib_n")
        m = state.get_value("fib_modulus")

        def mat_mult(A, B, mod):
            return [
                [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % mod,
                 (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % mod],
                [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % mod,
                 (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % mod],
            ]

        def mat_pow(M, p, mod):
            result = [[1, 0], [0, 1]]
            base = M
            while p:
                if p % 2:
                    result = mat_mult(result, base, mod)
                base = mat_mult(base, base, mod)
                p //= 2
            return result

        M = mat_pow([[1, 1], [1, 0]], n, m)
        result = M[0][1]

        s = state.clone()
        s.set_value("fib_result", result, ValueType.INTEGER, "compute_fib_matrix")
        s.answer_confidence = 1.0
        s.producing_tool = "compute_fib_matrix"
        s.applied_tools = state.applied_tools + ("compute_fib_matrix",)
        s.g_cost = state.g_cost + 1.5
        return [s]

    def _apply_compute_small_cases(self, state: SearchState) -> list[SearchState]:
        fn = state.get_value("sequence_fn")
        target = state.get_value("target_n", 50)
        n_terms = min(50, target)

        values = []
        start = state.get_value("sequence_start", 1)
        for i in range(start, start + n_terms):
            try:
                values.append(fn(i))
            except Exception:
                break

        if len(values) < 6:
            return []

        s = state.clone()
        s.set_value("sequence_values", values, ValueType.SEQUENCE, "compute_small_cases")
        s.set_value("sequence_start", start, ValueType.INTEGER, "compute_small_cases")
        s.producing_tool = "compute_small_cases"
        s.applied_tools = state.applied_tools + ("compute_small_cases",)
        s.g_cost = state.g_cost + 1.0
        return [s]

    def _apply_detect_recurrence(self, state: SearchState) -> list[SearchState]:
        values = state.get_value("sequence_values")
        from structural_explorer import detect_recurrence
        rec_info = detect_recurrence(values)
        if rec_info and rec_info["confidence"] > 0.5:
            s = state.clone()
            s.set_value("recurrence", rec_info, ValueType.EXPRESSION, "detect_recurrence")
            s.producing_tool = "detect_recurrence"
            s.applied_tools = state.applied_tools + ("detect_recurrence",)
            s.g_cost = state.g_cost + 1.0
            return [s]
        return []

    def _apply_extend_recurrence(self, state: SearchState) -> list[SearchState]:
        rec = state.get_value("recurrence")
        values = list(state.get_value("sequence_values"))
        target = state.get_value("target_n")
        start = state.get_value("sequence_start", 0)

        order = rec["order"]
        coeffs = rec["coefficients"]
        constant = rec["constant"]

        for i in range(len(values), target - start + 1):
            val = sum(coeffs[j] * values[i - j - 1] for j in range(order)) + constant
            values.append(val)

        answer = values[target - start] if target - start < len(values) else None

        if answer is not None:
            s = state.clone()
            s.set_value("sequence_answer", int(answer), ValueType.INTEGER, "extend_recurrence")
            s.answer_confidence = rec["confidence"]
            s.producing_tool = "extend_recurrence"
            s.applied_tools = state.applied_tools + ("extend_recurrence",)
            s.g_cost = state.g_cost + 1.0
            return [s]
        return []

    def _apply_detect_seq_periodicity(self, state: SearchState) -> list[SearchState]:
        values = state.get_value("sequence_values")
        from structural_explorer import detect_periodicity
        period_info = detect_periodicity(values)
        if period_info and period_info["confidence"] > 0.5:
            target = state.get_value("target_n")
            start = state.get_value("sequence_start", 0)
            period = period_info["period"]
            offset = period_info["offset"]
            block = period_info["repeating_block"]
            idx = (target - start - offset) % period
            answer = block[idx]

            s = state.clone()
            s.set_value("seq_period", period, ValueType.INTEGER, "detect_sequence_periodicity")
            s.set_value("sequence_answer", answer, ValueType.INTEGER, "detect_sequence_periodicity")
            s.answer_confidence = period_info["confidence"]
            s.producing_tool = "detect_sequence_periodicity"
            s.applied_tools = state.applied_tools + ("detect_sequence_periodicity",)
            s.g_cost = state.g_cost + 1.0
            return [s]
        return []

    def _apply_finalize_mod(self, state: SearchState) -> list[SearchState]:
        s = state.clone()
        s.candidate_answer = state.get_value("mod_result")
        s.answer_confidence = 1.0
        s.producing_tool = "finalize_mod_result"
        s.applied_tools = state.applied_tools + ("finalize_mod_result",)
        s.g_cost = state.g_cost + 0.1
        return [s]

    def _apply_finalize_fib(self, state: SearchState) -> list[SearchState]:
        s = state.clone()
        s.candidate_answer = state.get_value("fib_result")
        s.answer_confidence = 1.0
        s.producing_tool = "finalize_fib_result"
        s.applied_tools = state.applied_tools + ("finalize_fib_result",)
        s.g_cost = state.g_cost + 0.1
        return [s]

    def _apply_finalize_sequence(self, state: SearchState) -> list[SearchState]:
        s = state.clone()
        s.candidate_answer = state.get_value("sequence_answer")
        s.answer_confidence = state.answer_confidence
        s.producing_tool = "finalize_sequence_answer"
        s.applied_tools = state.applied_tools + ("finalize_sequence_answer",)
        s.g_cost = state.g_cost + 0.1
        return [s]

    def applicable_tools(self, state: SearchState) -> list[ToolOperator]:
        """Return all tools whose preconditions are satisfied."""
        return [t for t in self.tools if t.precondition(state)]


# =============================================================================
# HELPER FUNCTIONS FOR PRECONDITIONS
# =============================================================================

def _has_power_mod_pattern(text: str) -> bool:
    return bool(re.search(
        r'\d+\s*[\^]\s*[{]?\d+[}]?\s*(?:\\pmod|\\bmod|\\mod|mod|\(\s*mod)', text
    ))

def _has_last_digits_pattern(text: str) -> bool:
    return bool(re.search(r'last\s+\w+\s+digits?\s+of\s+\d+\s*[\^]', text.lower()))

def _has_fibonacci_pattern(text: str) -> bool:
    return bool(re.search(r'fibonacci|F\s*[_({\[]\s*\d+', text, re.IGNORECASE))

def _has_sequence_pattern(text: str) -> bool:
    tl = text.lower()
    return ("a(n)" in tl or "a_n" in tl or "tiling" in tl or "domino" in tl
            or "recurrence" in tl or "sequence" in tl)

def _has_remainder_pattern(text: str) -> bool:
    return bool(re.search(r'remainder\s+when\s+\d+\s*[\^]', text.lower()))


# =============================================================================
# TASK 3: HEURISTIC FIELD
# =============================================================================

def heuristic(state: SearchState) -> float:
    """Estimate distance from current state to having a concrete answer.

    h(x) = 0 means we have a confident answer.
    Higher values mean we're further from the answer.

    Key signals:
    - Do we have a candidate answer? (big reduction)
    - Do we have intermediate results? (moderate reduction)
    - Have we extracted problem parameters? (some reduction)
    - How many unknowns remain?
    """
    if state.candidate_answer is not None and state.answer_confidence >= 0.95:
        return 0.0  # Goal state

    h = 5.0  # Base distance: raw problem text, nothing extracted

    # Extracted parameters reduce distance
    if state.has_value("base") or state.has_value("fib_n") or state.has_value("sequence_fn"):
        h -= 1.5  # We know what we're computing

    if state.has_value("modulus") or state.has_value("fib_modulus"):
        h -= 0.5  # We know the modular structure

    # Intermediate results reduce distance further
    if state.has_value("period") or state.has_value("pisano_period"):
        h -= 1.0  # We've found structural insight

    if state.has_value("totient"):
        h -= 0.5

    if state.has_value("recurrence"):
        h -= 1.0

    if state.has_value("sequence_values"):
        h -= 0.5

    # Having a result but not finalized
    if state.has_value("mod_result") or state.has_value("fib_result") or state.has_value("sequence_answer"):
        h -= 1.5

    # Having a candidate answer
    if state.candidate_answer is not None:
        h = 0.5 * (1.0 - state.answer_confidence)

    return max(0.0, h)


# =============================================================================
# TASK 4: A* SEARCH ENGINE
# =============================================================================

@dataclass
class SearchResult:
    """Result of A* search through tool-space."""
    answer: Optional[int]
    confidence: float
    path: list[str]  # tool names in order
    states_explored: int
    elapsed: float
    goal_state: Optional[SearchState]

    def format_path(self) -> str:
        if not self.path:
            return "No solution path found"
        return " → ".join(self.path)


def astar_solve(
    problem_text: str,
    max_states: int = 500,
    max_time: float = 30.0,
    verbose: bool = False,
) -> SearchResult:
    """A* search through mathematical tool-space to solve a problem.

    Args:
        problem_text: The problem statement (LaTeX or plain text)
        max_states: Maximum states to explore before giving up
        max_time: Maximum wall-clock time in seconds
        verbose: Print search progress

    Returns:
        SearchResult with answer, confidence, solution path, and stats
    """
    t0 = time.time()
    registry = ToolRegistry()

    # Initial state: just the problem text
    initial = SearchState()
    initial.set_value("problem_text", problem_text, ValueType.EXPRESSION, "input")

    # Priority queue: (f_cost, tie_breaker, state)
    counter = 0
    open_set: list[tuple[float, int, SearchState]] = []
    h0 = heuristic(initial)
    heapq.heappush(open_set, (initial.g_cost + h0, counter, initial))

    # Visited states (cycle detection)
    visited: set[str] = set()

    states_explored = 0
    best_state: Optional[SearchState] = None

    while open_set and states_explored < max_states:
        elapsed = time.time() - t0
        if elapsed > max_time:
            if verbose:
                print(f"  Time limit reached ({elapsed:.1f}s)")
            break

        f_cost, _, current = heapq.heappop(open_set)
        state_key = current.state_key()

        if state_key in visited:
            continue
        visited.add(state_key)
        states_explored += 1

        if verbose and states_explored % 10 == 0:
            print(f"  States explored: {states_explored}, f={f_cost:.2f}, "
                  f"tools={len(current.applied_tools)}")

        # Goal test
        if current.candidate_answer is not None and current.answer_confidence >= 0.95:
            elapsed = time.time() - t0
            path = _reconstruct_path(current)
            if verbose:
                print(f"  GOAL FOUND: answer={current.candidate_answer} "
                      f"after {states_explored} states, {elapsed:.3f}s")
                print(f"  Path: {' -> '.join(path)}")
            return SearchResult(
                answer=current.candidate_answer,
                confidence=current.answer_confidence,
                path=path,
                states_explored=states_explored,
                elapsed=elapsed,
                goal_state=current,
            )

        # Track best state seen so far
        if best_state is None or (
            current.candidate_answer is not None
            and (best_state.candidate_answer is None
                 or current.answer_confidence > best_state.answer_confidence)
        ):
            best_state = current

        # Expand: apply all applicable tools
        applicable = registry.applicable_tools(current)
        if verbose and applicable:
            tool_names = [t.name for t in applicable]
            if states_explored <= 5:
                print(f"  State {states_explored}: applicable tools = {tool_names}")

        for tool in applicable:
            # Avoid re-applying the same tool
            if tool.name in current.applied_tools:
                continue

            try:
                new_states = tool.apply(current)
            except Exception as e:
                if verbose:
                    print(f"  Tool {tool.name} failed: {e}")
                continue

            for new_state in new_states:
                new_key = new_state.state_key()
                if new_key not in visited:
                    h = heuristic(new_state)
                    f = new_state.g_cost + h
                    counter += 1
                    heapq.heappush(open_set, (f, counter, new_state))

    elapsed = time.time() - t0

    # Return best result found
    if best_state and best_state.candidate_answer is not None:
        path = _reconstruct_path(best_state)
        return SearchResult(
            answer=best_state.candidate_answer,
            confidence=best_state.answer_confidence,
            path=path,
            states_explored=states_explored,
            elapsed=elapsed,
            goal_state=best_state,
        )

    return SearchResult(
        answer=None,
        confidence=0.0,
        path=[],
        states_explored=states_explored,
        elapsed=elapsed,
        goal_state=None,
    )


def _reconstruct_path(state: SearchState) -> list[str]:
    """Walk parent pointers to reconstruct the tool application path."""
    path = []
    current = state
    while current is not None:
        if current.producing_tool:
            path.append(current.producing_tool)
        current = current.parent
    path.reverse()
    return path


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    import sys

    problems = [
        ("2^2024 mod 7", "Find 2^{2024} mod 7.", pow(2, 2024, 7)),
        ("3^999 mod 13", "Find 3^{999} mod 13.", pow(3, 999, 13)),
        ("7^999 mod 1000", "Find the last three digits of 7^{999}.", pow(7, 999, 1000)),
        ("17^2023 mod 100", "What is the remainder when 17^{2023} is divided by 100?", pow(17, 2023, 100)),
        ("2^10000 mod 9", "Find 2^{10000} mod 9.", pow(2, 10000, 9)),
        ("F(10^6) mod 10007", "Find F(1000000) mod 10007, where F(n) is the nth Fibonacci number.", None),
        ("n^2 mod 97 at n=50000", "Find 50000^{2} mod 97.", (50000**2) % 97),
    ]

    # Compute F(10^6) mod 10007 ground truth
    def fib_mod_fast(n, m):
        if n <= 1:
            return n % m
        def mat_mult(A, B, mod):
            return [
                [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % mod, (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % mod],
                [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % mod, (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % mod],
            ]
        def mat_pow(M, p, mod):
            result = [[1, 0], [0, 1]]
            base = M
            while p:
                if p % 2:
                    result = mat_mult(result, base, mod)
                base = mat_mult(base, base, mod)
                p //= 2
            return result
        M = mat_pow([[1, 1], [1, 0]], n, m)
        return M[0][1]

    problems[5] = ("F(10^6) mod 10007", problems[5][1], fib_mod_fast(1000000, 10007))

    print("=" * 70)
    print("A* TOOL-SPACE SEARCH: MATH OLYMPIAD SOLVER")
    print("=" * 70)

    total = 0
    correct = 0
    total_time = 0.0
    total_states = 0

    for name, problem, expected in problems:
        total += 1
        print(f"\n[{name}]")
        print(f"  Problem: {problem}")

        result = astar_solve(problem, verbose=True)

        ok = result.answer == expected
        correct += ok
        total_time += result.elapsed
        total_states += result.states_explored

        status = "PASS" if ok else "FAIL"
        print(f"  Expected: {expected}, Got: {result.answer}  [{status}]")
        print(f"  Path: {result.format_path()}")
        print(f"  States explored: {result.states_explored}, Time: {result.elapsed:.3f}s")

    print("\n" + "=" * 70)
    print(f"RESULTS: {correct}/{total} correct ({100*correct/total:.0f}%)")
    print(f"Total states explored: {total_states}")
    print(f"Total time: {total_time:.3f}s")
    print(f"Average time per problem: {total_time/total:.3f}s")
    print("=" * 70)
