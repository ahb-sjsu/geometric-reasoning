"""A* Tool-Space Solver v2: Deep multi-step reasoning + geodesic metrics.

Extends v1 with:
- Chinese Remainder Theorem (factor → solve per prime → reconstruct)
- Multiplicative order finding
- Multi-step tool chains (6+ steps)
- Geodesic deviation metrics (from Geometric Reasoning framework)
- Hybrid A*/LLM integration point
"""

from __future__ import annotations

import re
import math
import time
from dataclasses import dataclass, field
from typing import Optional
from fractions import Fraction

from astar_solver import (
    SearchState, ValueType, ToolOperator, ToolRegistry,
    astar_solve, SearchResult, heuristic as base_heuristic,
    _reconstruct_path,
)
from astar_extended import extend_registry, extended_heuristic


# =============================================================================
# GEODESIC METRICS (from Geometric Reasoning framework)
# =============================================================================

@dataclass
class GeodesicMetrics:
    """Metrics connecting A* search to Riemannian geometry of tool-space.

    These quantify how "optimal" the discovered solution path is,
    directly mapping to concepts from Geometric Reasoning Ch. 4.
    """
    # Path cost (g): total cost of tool applications on the solution path
    path_cost: float = 0.0

    # Geodesic estimate: minimum possible cost (lower bound)
    # This is the heuristic evaluated at the initial state
    geodesic_estimate: float = 0.0

    # Geodesic deviation: how much longer the actual path is vs the estimate
    # deviation = path_cost - geodesic_estimate >= 0
    # deviation = 0 means the path IS the geodesic
    geodesic_deviation: float = 0.0

    # Search efficiency: fraction of explored states on the solution path
    # 1.0 = perfect (no wasted exploration), lower = more backtracking
    search_efficiency: float = 0.0

    # Branching factor: average number of applicable tools per state
    avg_branching_factor: float = 0.0

    # Heuristic accuracy: how well h(x) predicted actual cost-to-go
    # Computed as average |h(x) - actual_cost_to_go| / actual_cost_to_go
    heuristic_accuracy: float = 0.0

    # Curvature indicator: high branching = negative curvature (fragile)
    # low branching = positive curvature (robust/convergent)
    curvature_sign: str = "flat"  # "positive", "negative", "flat"

    # Path depth: number of tool applications
    path_depth: int = 0

    # Total states explored
    states_explored: int = 0

    def summary(self) -> str:
        lines = [
            "Geodesic Metrics:",
            f"  Path cost (g):         {self.path_cost:.2f}",
            f"  Geodesic estimate:     {self.geodesic_estimate:.2f}",
            f"  Geodesic deviation:    {self.geodesic_deviation:.2f}",
            f"  Search efficiency:     {self.search_efficiency:.1%}",
            f"  Avg branching factor:  {self.avg_branching_factor:.1f}",
            f"  Heuristic accuracy:    {self.heuristic_accuracy:.1%}",
            f"  Curvature:             {self.curvature_sign}",
            f"  Path depth:            {self.path_depth}",
            f"  States explored:       {self.states_explored}",
        ]
        return "\n".join(lines)


def compute_geodesic_metrics(result: SearchResult, initial_h: float) -> GeodesicMetrics:
    """Compute geometric metrics for a completed search."""
    metrics = GeodesicMetrics()

    if result.goal_state is None:
        metrics.states_explored = result.states_explored
        return metrics

    metrics.path_cost = result.goal_state.g_cost
    metrics.geodesic_estimate = initial_h
    metrics.geodesic_deviation = max(0, metrics.path_cost - initial_h)
    metrics.path_depth = len(result.path)
    metrics.states_explored = result.states_explored

    # Search efficiency: path states / total states
    if result.states_explored > 0:
        metrics.search_efficiency = metrics.path_depth / result.states_explored

    # Compute heuristic accuracy along the path
    if result.goal_state and metrics.path_depth > 0:
        # Walk the path and check h(x) at each state
        state = result.goal_state
        path_states = []
        while state is not None:
            path_states.append(state)
            state = state.parent
        path_states.reverse()

        h_errors = []
        for i, s in enumerate(path_states):
            actual_remaining = metrics.path_cost - s.g_cost
            h_val = v2_heuristic(s)
            if actual_remaining > 0:
                h_errors.append(abs(h_val - actual_remaining) / actual_remaining)

        if h_errors:
            metrics.heuristic_accuracy = 1.0 - min(1.0, sum(h_errors) / len(h_errors))

    # Curvature indicator based on branching
    if metrics.avg_branching_factor > 4:
        metrics.curvature_sign = "negative"  # Many choices = divergent paths
    elif metrics.avg_branching_factor < 2:
        metrics.curvature_sign = "positive"  # Few choices = convergent
    else:
        metrics.curvature_sign = "flat"

    return metrics


# =============================================================================
# DEEP NUMBER THEORY TOOLS
# =============================================================================

def _register_deep_nt_tools(registry: ToolRegistry):
    """Add CRT, multiplicative order, and advanced number theory tools."""

    # Chinese Remainder Theorem: decompose modular problem by prime factors
    registry.tools.append(ToolOperator(
        name="apply_crt_decompose",
        precondition=lambda s: (
            s.has_value("base") and s.has_value("exponent")
            and s.has_value("modulus_factors")
            and not s.has_value("crt_components")
            and len(s.get_value("modulus_factors")) > 1  # Only if composite
        ),
        apply=lambda s: _apply_crt_decompose(s),
        cost=1.0,
        category="number_theory",
        description="Decompose a^b mod m into a^b mod p^k for each prime power",
    ))

    registry.tools.append(ToolOperator(
        name="apply_crt_reconstruct",
        precondition=lambda s: (
            s.has_value("crt_components") and not s.has_value("mod_result")
        ),
        apply=lambda s: _apply_crt_reconstruct(s),
        cost=0.5,
        category="number_theory",
        description="Reconstruct answer from CRT components",
    ))

    # Multiplicative order: ord_m(a) = smallest k such that a^k ≡ 1 mod m
    registry.tools.append(ToolOperator(
        name="find_multiplicative_order",
        precondition=lambda s: (
            s.has_value("base") and s.has_value("modulus")
            and not s.has_value("mult_order")
            and math.gcd(s.get_value("base"), s.get_value("modulus")) == 1
        ),
        apply=lambda s: _apply_mult_order(s),
        cost=1.5,
        category="number_theory",
        description="Find multiplicative order ord_m(a)",
    ))

    registry.tools.append(ToolOperator(
        name="reduce_via_order",
        precondition=lambda s: (
            s.has_value("mult_order") and s.has_value("exponent")
            and s.has_value("base") and s.has_value("modulus")
            and not s.has_value("mod_result")
        ),
        apply=lambda s: _apply_reduce_via_order(s),
        cost=0.5,
        category="number_theory",
        description="Reduce exponent modulo multiplicative order",
    ))

    # GCD / Extended Euclidean
    registry.tools.append(ToolOperator(
        name="compute_gcd",
        precondition=lambda s: (
            s.has_value("gcd_a") and s.has_value("gcd_b")
            and not s.has_value("gcd_result")
        ),
        apply=lambda s: _apply_gcd(s),
        cost=0.5,
        category="number_theory",
        description="Compute gcd(a, b)",
    ))

    # Modular inverse
    registry.tools.append(ToolOperator(
        name="compute_mod_inverse",
        precondition=lambda s: (
            s.has_value("inv_a") and s.has_value("inv_mod")
            and not s.has_value("mod_inverse_result")
        ),
        apply=lambda s: _apply_mod_inverse(s),
        cost=0.5,
        category="number_theory",
        description="Compute a^(-1) mod m",
    ))

    # Sum of divisors
    registry.tools.append(ToolOperator(
        name="sum_of_divisors",
        precondition=lambda s: (
            s.has_value("sod_n") and not s.has_value("sod_result")
        ),
        apply=lambda s: _apply_sum_of_divisors(s),
        cost=1.0,
        category="number_theory",
        description="Compute sigma(n) = sum of divisors of n",
    ))

    # Number of divisors
    registry.tools.append(ToolOperator(
        name="count_divisors",
        precondition=lambda s: (
            s.has_value("modulus_factors") and not s.has_value("num_divisors")
        ),
        apply=lambda s: _apply_count_divisors(s),
        cost=0.5,
        category="number_theory",
        description="Count divisors from factorization: product of (e_i + 1)",
    ))

    # Extract deeper number theory patterns
    registry.tools.append(ToolOperator(
        name="extract_gcd_problem",
        precondition=lambda s: (
            s.has_value("problem_text")
            and not s.has_value("gcd_a")
            and _has_gcd_pattern(s.get_value("problem_text"))
        ),
        apply=lambda s: _apply_extract_gcd(s),
        cost=0.5,
        category="extraction",
        description="Extract gcd(a,b) from problem text",
    ))

    registry.tools.append(ToolOperator(
        name="extract_divisor_problem",
        precondition=lambda s: (
            s.has_value("problem_text")
            and not s.has_value("sod_n") and not s.has_value("modulus_factors")
            and _has_divisor_pattern(s.get_value("problem_text"))
        ),
        apply=lambda s: _apply_extract_divisor(s),
        cost=0.5,
        category="extraction",
        description="Extract divisor counting/sum problem",
    ))

    # Finalize for new result types
    registry.tools.append(ToolOperator(
        name="finalize_gcd_result",
        precondition=lambda s: s.has_value("gcd_result") and s.candidate_answer is None,
        apply=lambda s: _finalize_value(s, "gcd_result"),
        cost=0.1,
        category="finalize",
    ))

    registry.tools.append(ToolOperator(
        name="finalize_sod_result",
        precondition=lambda s: s.has_value("sod_result") and s.candidate_answer is None,
        apply=lambda s: _finalize_value(s, "sod_result"),
        cost=0.1,
        category="finalize",
    ))

    registry.tools.append(ToolOperator(
        name="finalize_num_divisors",
        precondition=lambda s: s.has_value("num_divisors") and s.candidate_answer is None,
        apply=lambda s: _finalize_value(s, "num_divisors"),
        cost=0.1,
        category="finalize",
    ))


# --- Deep NT Implementations ---

def _apply_crt_decompose(state: SearchState) -> list[SearchState]:
    """Compute a^b mod p^k for each prime power in the factorization."""
    base = state.get_value("base")
    exp = state.get_value("exponent")
    factors = state.get_value("modulus_factors")

    components = {}
    for p, k in factors.items():
        pk = p ** k
        components[pk] = pow(base, exp, pk)

    s = state.clone()
    s.set_value("crt_components", components, ValueType.EXPRESSION, "apply_crt_decompose")
    s.producing_tool = "apply_crt_decompose"
    s.applied_tools = state.applied_tools + ("apply_crt_decompose",)
    s.g_cost = state.g_cost + 1.0
    return [s]


def _apply_crt_reconstruct(state: SearchState) -> list[SearchState]:
    """Reconstruct answer using Chinese Remainder Theorem."""
    components = state.get_value("crt_components")  # {modulus: residue}
    moduli = list(components.keys())
    residues = [components[m] for m in moduli]

    # CRT reconstruction
    M = 1
    for m in moduli:
        M *= m

    result = 0
    for m, r in zip(moduli, residues):
        Mi = M // m
        yi = pow(Mi, -1, m)
        result = (result + r * Mi * yi) % M

    s = state.clone()
    s.set_value("mod_result", result, ValueType.INTEGER, "apply_crt_reconstruct")
    s.answer_confidence = 1.0
    s.producing_tool = "apply_crt_reconstruct"
    s.applied_tools = state.applied_tools + ("apply_crt_reconstruct",)
    s.g_cost = state.g_cost + 0.5
    return [s]


def _apply_mult_order(state: SearchState) -> list[SearchState]:
    """Find multiplicative order of base mod modulus."""
    base = state.get_value("base")
    mod = state.get_value("modulus")

    if math.gcd(base, mod) != 1:
        return []

    # Find ord_m(a) by checking a^k mod m for k = 1, 2, ...
    # Optimization: order divides phi(m), so we only need to check divisors of phi(m)
    current = base % mod
    for k in range(1, mod):
        if current == 1:
            s = state.clone()
            s.set_value("mult_order", k, ValueType.INTEGER, "find_multiplicative_order")
            s.producing_tool = "find_multiplicative_order"
            s.applied_tools = state.applied_tools + ("find_multiplicative_order",)
            s.g_cost = state.g_cost + 1.5
            return [s]
        current = (current * base) % mod
        if k > 100000:  # Safety limit
            break

    return []


def _apply_reduce_via_order(state: SearchState) -> list[SearchState]:
    order = state.get_value("mult_order")
    exp = state.get_value("exponent")
    base = state.get_value("base")
    mod = state.get_value("modulus")

    reduced = exp % order
    result = pow(base, reduced, mod)

    s = state.clone()
    s.set_value("mod_result", result, ValueType.INTEGER, "reduce_via_order")
    s.answer_confidence = 1.0
    s.producing_tool = "reduce_via_order"
    s.applied_tools = state.applied_tools + ("reduce_via_order",)
    s.g_cost = state.g_cost + 0.5
    return [s]


def _apply_gcd(state: SearchState) -> list[SearchState]:
    a = state.get_value("gcd_a")
    b = state.get_value("gcd_b")
    s = state.clone()
    s.set_value("gcd_result", math.gcd(a, b), ValueType.INTEGER, "compute_gcd")
    s.answer_confidence = 1.0
    s.producing_tool = "compute_gcd"
    s.applied_tools = state.applied_tools + ("compute_gcd",)
    s.g_cost = state.g_cost + 0.5
    return [s]


def _apply_mod_inverse(state: SearchState) -> list[SearchState]:
    a = state.get_value("inv_a")
    m = state.get_value("inv_mod")
    try:
        inv = pow(a, -1, m)
        s = state.clone()
        s.set_value("mod_inverse_result", inv, ValueType.INTEGER, "compute_mod_inverse")
        s.answer_confidence = 1.0
        s.producing_tool = "compute_mod_inverse"
        s.applied_tools = state.applied_tools + ("compute_mod_inverse",)
        s.g_cost = state.g_cost + 0.5
        return [s]
    except ValueError:
        return []


def _apply_sum_of_divisors(state: SearchState) -> list[SearchState]:
    n = state.get_value("sod_n")
    from sympy import factorint
    factors = factorint(n)
    sigma = 1
    for p, e in factors.items():
        sigma *= (p ** (e + 1) - 1) // (p - 1)
    s = state.clone()
    s.set_value("sod_result", sigma, ValueType.INTEGER, "sum_of_divisors")
    s.answer_confidence = 1.0
    s.producing_tool = "sum_of_divisors"
    s.applied_tools = state.applied_tools + ("sum_of_divisors",)
    s.g_cost = state.g_cost + 1.0
    return [s]


def _apply_count_divisors(state: SearchState) -> list[SearchState]:
    factors = state.get_value("modulus_factors")
    count = 1
    for e in factors.values():
        count *= (e + 1)
    s = state.clone()
    s.set_value("num_divisors", count, ValueType.INTEGER, "count_divisors")
    s.answer_confidence = 1.0
    s.producing_tool = "count_divisors"
    s.applied_tools = state.applied_tools + ("count_divisors",)
    s.g_cost = state.g_cost + 0.5
    return [s]


def _apply_extract_gcd(state: SearchState) -> list[SearchState]:
    text = state.get_value("problem_text")
    matches = re.findall(r'gcd\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', text, re.IGNORECASE)
    results = []
    for a, b in matches:
        s = state.clone()
        s.set_value("gcd_a", int(a), ValueType.INTEGER, "extract_gcd_problem")
        s.set_value("gcd_b", int(b), ValueType.INTEGER, "extract_gcd_problem")
        s.producing_tool = "extract_gcd_problem"
        s.applied_tools = state.applied_tools + ("extract_gcd_problem",)
        s.g_cost = state.g_cost + 0.5
        results.append(s)
        break
    return results


def _apply_extract_divisor(state: SearchState) -> list[SearchState]:
    text = state.get_value("problem_text").lower()
    results = []

    # "number of divisors of N" or "how many divisors does N have"
    div_match = re.search(r'(?:number of|how many|count)\s*(?:positive\s+)?divisors\s*(?:of|does)\s*(\d+)', text)
    if div_match:
        n = int(div_match.group(1))
        from sympy import factorint
        s = state.clone()
        s.set_value("modulus_factors", factorint(n), ValueType.EXPRESSION, "extract_divisor_problem")
        s.producing_tool = "extract_divisor_problem"
        s.applied_tools = state.applied_tools + ("extract_divisor_problem",)
        s.g_cost = state.g_cost + 0.5
        results.append(s)

    # "sum of divisors of N"
    sod_match = re.search(r'sum\s*(?:of\s+)?(?:all\s+)?(?:positive\s+)?divisors\s*(?:of)\s*(\d+)', text)
    if sod_match and not results:
        n = int(sod_match.group(1))
        s = state.clone()
        s.set_value("sod_n", n, ValueType.INTEGER, "extract_divisor_problem")
        s.producing_tool = "extract_divisor_problem"
        s.applied_tools = state.applied_tools + ("extract_divisor_problem",)
        s.g_cost = state.g_cost + 0.5
        results.append(s)

    return results


def _has_gcd_pattern(text: str) -> bool:
    return bool(re.search(r'gcd\s*\(', text, re.IGNORECASE))

def _has_divisor_pattern(text: str) -> bool:
    tl = text.lower()
    return any(p in tl for p in ["divisors of", "divisors does", "sum of divisors"])


def _finalize_value(state: SearchState, key: str) -> list[SearchState]:
    s = state.clone()
    s.candidate_answer = int(state.get_value(key))
    s.answer_confidence = 1.0
    s.producing_tool = f"finalize_{key}"
    s.applied_tools = state.applied_tools + (f"finalize_{key}",)
    s.g_cost = state.g_cost + 0.1
    return [s]


# =============================================================================
# V2 HEURISTIC (deeper awareness)
# =============================================================================

def v2_heuristic(state: SearchState) -> float:
    """Enhanced heuristic with deep NT awareness."""
    h = extended_heuristic(state)

    # CRT signals
    if state.has_value("crt_components"):
        h = min(h, 1.0)
    if state.has_value("mult_order"):
        h -= 0.5
    if state.has_value("gcd_a"):
        h -= 0.5
    if state.has_value("sod_n"):
        h -= 0.5
    if state.has_value("num_divisors") or state.has_value("sod_result") or state.has_value("gcd_result"):
        h = min(h, 0.5)

    return max(0.0, h)


# =============================================================================
# V2 SOLVER
# =============================================================================

def astar_solve_v2(
    problem_text: str,
    max_states: int = 2000,
    max_time: float = 60.0,
    verbose: bool = False,
) -> tuple[SearchResult, GeodesicMetrics]:
    """A* solve v2 with deep tools and geodesic metrics."""
    import astar_solver

    # Patch heuristic
    original_heuristic = astar_solver.heuristic
    astar_solver.heuristic = v2_heuristic

    # Extend registry with both extended and deep tools
    original_init = ToolRegistry._register_all_tools

    def patched_init(self):
        original_init(self)
        extend_registry(self)
        _register_deep_nt_tools(self)

    ToolRegistry._register_all_tools = patched_init

    # Compute initial heuristic for geodesic metrics
    initial_state = SearchState()
    initial_state.set_value("problem_text", problem_text, ValueType.EXPRESSION, "input")
    initial_h = v2_heuristic(initial_state)

    try:
        result = astar_solve(problem_text, max_states=max_states,
                             max_time=max_time, verbose=verbose)
    finally:
        astar_solver.heuristic = original_heuristic
        ToolRegistry._register_all_tools = original_init

    metrics = compute_geodesic_metrics(result, initial_h)
    return result, metrics


# =============================================================================
# COMPREHENSIVE V2 TEST SUITE
# =============================================================================

if __name__ == "__main__":
    # Helper for Fibonacci
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

    problems = [
        # --- ORIGINAL 22 (should still all pass) ---
        ("NT1: 2^2024 mod 7", "Find 2^{2024} mod 7.", pow(2, 2024, 7)),
        ("NT2: 3^999 mod 13", "Find 3^{999} mod 13.", pow(3, 999, 13)),
        ("NT3: last 3 digits 7^999", "Find the last three digits of 7^{999}.", pow(7, 999, 1000)),
        ("NT4: 17^2023 mod 100", "What is the remainder when 17^{2023} is divided by 100?", pow(17, 2023, 100)),
        ("NT5: 2^10000 mod 9", "Find 2^{10000} mod 9.", pow(2, 10000, 9)),
        ("NT6: 13^2025 mod 1000", "Find the last three digits of 13^{2025}.", pow(13, 2025, 1000)),
        ("NT7: 7^343 mod 10", "Find 7^{343} mod 10.", pow(7, 343, 10)),
        ("SEQ1: F(10^6) mod 10007", "Find F(1000000) mod 10007, where F(n) is the nth Fibonacci number.", fib_mod_fast(1000000, 10007)),
        ("SEQ2: F(100) mod 997", "Find F(100) mod 997, where F(n) is the nth Fibonacci number.", fib_mod_fast(100, 997)),
        ("SEQ3: 50000^2 mod 97", "Find 50000^{2} mod 97.", (50000**2) % 97),
        ("COMB1: C(100,3)", "Compute \\binom{100}{3}.", 161700),
        ("COMB2: C(1000,2) mod 997", "Compute \\binom{1000}{2} \\pmod{997}.", (1000*999//2) % 997),
        ("COMB3: C(20,10)", "Compute C(20, 10).", 184756),
        ("COMB4: D(5)", "Find the number of derangements of 5 elements (permutations with no fixed points).", 44),
        ("COMB5: D(10)", "Find the number of derangements of 10 elements.", 1334961),
        ("ALG1: sum squares 100", "Find the sum of squares 1^2 + 2^2 + ... + 100^2.", 338350),
        ("ALG2: sum cubes 50", "Find the sum of cubes 1^3 + 2^3 + ... + 50^3.", 1625625),
        ("ALG3: arithmetic", "Find the sum 3 + 7 + 11 + ... + 399.", 20100),
        ("ALG4: sum sq mod", "Find the sum of squares 1^2 + 2^2 + ... + 1000^2 mod 10007.", 333833500 % 10007),
        ("GEO1: area 3,4,5", "A triangle has sides 3, 4, and 5. Find its area.", 6),
        ("GEO2: area 13,14,15", "A triangle has sides 13, 14, and 15. Find its area.", 84),
        ("GEO3: perimeter", "A triangle has sides 7, 24, and 25. Find its perimeter.", 56),

        # --- NEW: DEEP NUMBER THEORY (multi-step) ---
        ("DNT1: gcd(12345678, 87654321)", "Find gcd(12345678, 87654321).", math.gcd(12345678, 87654321)),
        ("DNT2: gcd(2^20-1, 2^15-1)", "Find gcd(1048575, 32767).", math.gcd(1048575, 32767)),
        ("DNT3: divisors of 360", "How many positive divisors does 360 have?", 24),
        ("DNT4: divisors of 10^6", "How many positive divisors does 1000000 have?", 49),
        ("DNT5: sum of divisors 360", "Find the sum of all positive divisors of 360.", 1170),
        ("DNT6: sum of divisors 2520", "Find the sum of all positive divisors of 2520.", 9360),

        # --- NEW: HARDER COMBINATORICS ---
        ("HCOMB1: C(100,50) mod 997", "Compute \\binom{100}{50} \\pmod{997}.", None),  # Lucas
        ("HCOMB2: D(8) mod 1000", "Find the number of derangements of 8 elements. Give the last three digits.", None),

        # --- NEW: HARDER ALGEBRA ---
        ("HALG1: sum sq 10000 mod 97", "Find the sum of squares 1^2 + 2^2 + ... + 10000^2 mod 97.", None),
    ]

    # Compute missing ground truths
    from astar_extended import _lucas_binomial, _binomial

    # HCOMB1: C(100,50) mod 997
    problems[28] = (problems[28][0], problems[28][1], _lucas_binomial(100, 50, 997))

    # HCOMB2: D(8) last 3 digits
    def derangement(n):
        if n == 0: return 1
        if n == 1: return 0
        d0, d1 = 1, 0
        for i in range(2, n+1):
            d0, d1 = d1, (i-1) * (d0 + d1)
        return d1
    problems[29] = (problems[29][0], problems[29][1], derangement(8) % 1000)

    # HALG1
    n = 10000
    problems[30] = (problems[30][0], problems[30][1], (n*(n+1)*(2*n+1)//6) % 97)

    print("=" * 70)
    print("A* TOOL-SPACE SOLVER v2: DEEP MULTI-STEP + GEODESIC METRICS")
    print("=" * 70)
    print(f"Total problems: {len(problems)}")

    total = 0
    correct = 0
    total_time = 0.0
    total_states = 0
    all_metrics = []
    results_by_domain = {}
    failures = []

    for name, problem, expected in problems:
        domain = name.split(":")[0].rstrip("0123456789")
        total += 1

        t0 = time.time()
        result, metrics = astar_solve_v2(problem, verbose=False)
        elapsed = time.time() - t0

        ok = result.answer == expected
        correct += ok
        total_time += elapsed
        total_states += result.states_explored
        all_metrics.append(metrics)

        status = "PASS" if ok else "FAIL"
        path_str = result.format_path()

        print(f"  [{status}] {name}")
        if not ok:
            print(f"    Expected: {expected}, Got: {result.answer}")
            print(f"    Path: {path_str}")
            failures.append(name)
        else:
            print(f"    = {result.answer}  [{path_str}]  "
                  f"({result.states_explored} states, {elapsed:.3f}s, "
                  f"dev={metrics.geodesic_deviation:.2f})")

        if domain not in results_by_domain:
            results_by_domain[domain] = {"correct": 0, "total": 0}
        results_by_domain[domain]["total"] += 1
        if ok:
            results_by_domain[domain]["correct"] += 1

    # Aggregate geodesic metrics
    passing_metrics = [m for m, (_, _, e) in zip(all_metrics, problems) if m.path_depth > 0]

    print("\n" + "=" * 70)
    print("RESULTS BY DOMAIN")
    print("=" * 70)
    for domain, stats in sorted(results_by_domain.items()):
        c, t = stats["correct"], stats["total"]
        print(f"  {domain:8s}: {c}/{t} ({100*c/t:.0f}%)")
    print(f"  {'TOTAL':8s}: {correct}/{total} ({100*correct/total:.0f}%)")

    if failures:
        print(f"\n  Failures: {', '.join(failures)}")

    print(f"\n" + "=" * 70)
    print("GEODESIC METRICS (Geometric Reasoning Framework)")
    print("=" * 70)

    if passing_metrics:
        avg_deviation = sum(m.geodesic_deviation for m in passing_metrics) / len(passing_metrics)
        avg_efficiency = sum(m.search_efficiency for m in passing_metrics) / len(passing_metrics)
        avg_depth = sum(m.path_depth for m in passing_metrics) / len(passing_metrics)
        avg_accuracy = sum(m.heuristic_accuracy for m in passing_metrics) / len(passing_metrics)
        max_deviation = max(m.geodesic_deviation for m in passing_metrics)

        print(f"  Average geodesic deviation:  {avg_deviation:.3f}")
        print(f"  Maximum geodesic deviation:  {max_deviation:.3f}")
        print(f"  Average search efficiency:   {avg_efficiency:.1%}")
        print(f"  Average heuristic accuracy:  {avg_accuracy:.1%}")
        print(f"  Average path depth:          {avg_depth:.1f} tools")
        print(f"  Total states explored:       {total_states}")
        print(f"  Total time:                  {total_time:.3f}s")
        print(f"  Average time per problem:    {total_time/total:.3f}s")

        # Curvature distribution
        curvatures = [m.curvature_sign for m in passing_metrics]
        print(f"\n  Curvature distribution:")
        for c in ["positive", "flat", "negative"]:
            n = curvatures.count(c)
            print(f"    {c:10s}: {n}/{len(curvatures)} ({100*n/len(curvatures):.0f}%)")

    print("=" * 70)
