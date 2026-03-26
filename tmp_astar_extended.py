"""Extended A* tool registry: geometry, combinatorics, algebra operators.

Extends the core astar_solver with tools for all 4 AIMO domains.
"""

from __future__ import annotations

import re
import math
from typing import Optional
from fractions import Fraction

from astar_solver import (
    SearchState, ValueType, MathValue, ToolOperator, ToolRegistry,
    heuristic as base_heuristic, astar_solve, SearchResult,
)


def extend_registry(registry: ToolRegistry):
    """Add geometry, combinatorics, and algebra tools to the registry."""

    # Fix priority: if the problem is clearly a sum, suppress modular power extraction
    # by tightening its precondition
    for tool in registry.tools:
        if tool.name == "extract_modular_power":
            original_pre = tool.precondition
            tool.precondition = lambda s, _orig=original_pre: (
                _orig(s)
                and not _has_sum_pattern(s.get_value("problem_text", ""))
                and not _has_digit_pattern_ext(s.get_value("problem_text", ""))
            )
            break

    # =====================================================================
    # COMBINATORICS TOOLS
    # =====================================================================

    registry.tools.append(ToolOperator(
        name="extract_binomial",
        precondition=lambda s: (
            s.has_value("problem_text")
            and not s.has_value("comb_type")
            and _has_binomial_pattern(s.get_value("problem_text"))
        ),
        apply=lambda s: _apply_extract_binomial(s),
        cost=0.5,
        category="extraction",
        description="Extract C(n,k) or binomial coefficient pattern",
    ))

    registry.tools.append(ToolOperator(
        name="extract_counting",
        precondition=lambda s: (
            s.has_value("problem_text")
            and not s.has_value("comb_type")
            and _has_counting_pattern(s.get_value("problem_text"))
        ),
        apply=lambda s: _apply_extract_counting(s),
        cost=0.5,
        category="extraction",
        description="Extract counting/permutation/arrangement problems",
    ))

    registry.tools.append(ToolOperator(
        name="compute_binomial_mod",
        precondition=lambda s: (
            s.has_value("binom_n") and s.has_value("binom_k")
            and not s.has_value("comb_result")
        ),
        apply=lambda s: _apply_binomial_mod(s),
        cost=1.0,
        category="combinatorics",
        description="Compute C(n,k) mod p using Lucas' theorem",
    ))

    registry.tools.append(ToolOperator(
        name="compute_catalan",
        precondition=lambda s: (
            s.has_value("catalan_n") and not s.has_value("comb_result")
        ),
        apply=lambda s: _apply_catalan(s),
        cost=1.0,
        category="combinatorics",
        description="Compute nth Catalan number",
    ))

    registry.tools.append(ToolOperator(
        name="compute_derangements",
        precondition=lambda s: (
            s.has_value("derangement_n") and not s.has_value("comb_result")
        ),
        apply=lambda s: _apply_derangements(s),
        cost=1.0,
        category="combinatorics",
        description="Compute D(n) = n! * sum(-1)^k/k!",
    ))

    registry.tools.append(ToolOperator(
        name="inclusion_exclusion",
        precondition=lambda s: (
            s.has_value("ie_sets") and not s.has_value("comb_result")
        ),
        apply=lambda s: _apply_inclusion_exclusion(s),
        cost=1.5,
        category="combinatorics",
        description="Apply inclusion-exclusion principle",
    ))

    registry.tools.append(ToolOperator(
        name="finalize_comb_result",
        precondition=lambda s: (
            s.has_value("comb_result") and s.candidate_answer is None
        ),
        apply=lambda s: _apply_finalize_comb(s),
        cost=0.1,
        category="finalize",
    ))

    # =====================================================================
    # ALGEBRA TOOLS
    # =====================================================================

    registry.tools.append(ToolOperator(
        name="extract_polynomial",
        precondition=lambda s: (
            s.has_value("problem_text")
            and not s.has_value("poly_coeffs")
            and _has_polynomial_pattern(s.get_value("problem_text"))
        ),
        apply=lambda s: _apply_extract_polynomial(s),
        cost=0.5,
        category="extraction",
        description="Extract polynomial equation from problem text",
    ))

    registry.tools.append(ToolOperator(
        name="extract_sum_formula",
        precondition=lambda s: (
            s.has_value("problem_text")
            and not s.has_value("sum_type")
            and _has_sum_pattern(s.get_value("problem_text"))
        ),
        apply=lambda s: _apply_extract_sum(s),
        cost=0.1,  # Very low cost — sum patterns should beat modular_power
        category="extraction",
        description="Extract summation problem",
    ))

    registry.tools.append(ToolOperator(
        name="solve_polynomial",
        precondition=lambda s: (
            s.has_value("poly_coeffs") and not s.has_value("poly_roots")
        ),
        apply=lambda s: _apply_solve_polynomial(s),
        cost=1.5,
        category="algebra",
        description="Find roots of polynomial using SymPy",
    ))

    registry.tools.append(ToolOperator(
        name="apply_vietas",
        precondition=lambda s: (
            s.has_value("poly_coeffs") and not s.has_value("vieta_result")
            and s.has_value("vieta_query")
        ),
        apply=lambda s: _apply_vietas(s),
        cost=1.0,
        category="algebra",
        description="Apply Vieta's formulas for sum/product of roots",
    ))

    registry.tools.append(ToolOperator(
        name="compute_sum",
        precondition=lambda s: (
            s.has_value("sum_type") and not s.has_value("alg_result")
        ),
        apply=lambda s: _apply_compute_sum(s),
        cost=1.0,
        category="algebra",
        description="Compute closed-form sum (arithmetic, geometric, powers)",
    ))

    registry.tools.append(ToolOperator(
        name="solve_diophantine",
        precondition=lambda s: (
            s.has_value("dioph_equation") and not s.has_value("alg_result")
        ),
        apply=lambda s: _apply_diophantine(s),
        cost=2.0,
        category="algebra",
        description="Solve Diophantine equation using SymPy",
    ))

    registry.tools.append(ToolOperator(
        name="compute_floor_ceiling",
        precondition=lambda s: (
            s.has_value("floor_expr") and not s.has_value("alg_result")
        ),
        apply=lambda s: _apply_floor_ceiling(s),
        cost=1.0,
        category="algebra",
        description="Evaluate floor/ceiling expressions",
    ))

    registry.tools.append(ToolOperator(
        name="finalize_alg_result",
        precondition=lambda s: (
            s.has_value("alg_result") and s.candidate_answer is None
        ),
        apply=lambda s: _apply_finalize_alg(s),
        cost=0.1,
        category="finalize",
    ))

    # =====================================================================
    # GEOMETRY TOOLS
    # =====================================================================

    registry.tools.append(ToolOperator(
        name="extract_triangle",
        precondition=lambda s: (
            s.has_value("problem_text")
            and not s.has_value("geo_type")
            and _has_triangle_pattern(s.get_value("problem_text"))
        ),
        apply=lambda s: _apply_extract_triangle(s),
        cost=0.5,
        category="extraction",
        description="Extract triangle properties from problem text",
    ))

    registry.tools.append(ToolOperator(
        name="extract_circle",
        precondition=lambda s: (
            s.has_value("problem_text")
            and not s.has_value("geo_type")
            and _has_circle_pattern(s.get_value("problem_text"))
        ),
        apply=lambda s: _apply_extract_circle(s),
        cost=0.5,
        category="extraction",
        description="Extract circle properties from problem text",
    ))

    registry.tools.append(ToolOperator(
        name="compute_triangle_area",
        precondition=lambda s: (
            s.has_value("geo_type") and s.get_value("geo_type") == "triangle"
            and s.has_value("tri_sides") and not s.has_value("geo_result")
            and s.get_value("geo_query", "area") == "area"
        ),
        apply=lambda s: _apply_triangle_area(s),
        cost=1.0,
        category="geometry",
        description="Compute triangle area via Heron's formula",
    ))

    registry.tools.append(ToolOperator(
        name="compute_triangle_properties",
        precondition=lambda s: (
            s.has_value("geo_type") and s.get_value("geo_type") == "triangle"
            and s.has_value("tri_sides") and not s.has_value("geo_result")
            and s.get_value("geo_query", "area") in ("perimeter", "inradius", "circumradius")
        ),
        apply=lambda s: _apply_triangle_properties(s),
        cost=1.0,
        category="geometry",
        description="Compute inradius, circumradius, perimeter",
    ))

    registry.tools.append(ToolOperator(
        name="coordinate_geometry",
        precondition=lambda s: (
            s.has_value("geo_points") and not s.has_value("geo_result")
        ),
        apply=lambda s: _apply_coordinate_geometry(s),
        cost=1.5,
        category="geometry",
        description="Solve using coordinate geometry (place, compute, intersect)",
    ))

    registry.tools.append(ToolOperator(
        name="compute_circle_properties",
        precondition=lambda s: (
            s.has_value("geo_type") and s.get_value("geo_type") == "circle"
            and s.has_value("circle_radius") and not s.has_value("geo_result")
        ),
        apply=lambda s: _apply_circle_properties(s),
        cost=1.0,
        category="geometry",
        description="Compute circle area, circumference, arc length, sector area",
    ))

    registry.tools.append(ToolOperator(
        name="finalize_geo_result",
        precondition=lambda s: (
            s.has_value("geo_result") and s.candidate_answer is None
        ),
        apply=lambda s: _apply_finalize_geo(s),
        cost=0.1,
        category="finalize",
    ))

    # =====================================================================
    # GENERAL TOOLS (cross-domain)
    # =====================================================================

    registry.tools.append(ToolOperator(
        name="sympy_solve_generic",
        precondition=lambda s: (
            s.has_value("sympy_equation") and not s.has_value("sympy_result")
        ),
        apply=lambda s: _apply_sympy_solve(s),
        cost=2.0,
        category="algebra",
        description="Generic SymPy equation solver (fallback)",
    ))

    registry.tools.append(ToolOperator(
        name="brute_force_small",
        precondition=lambda s: (
            s.has_value("brute_fn") and s.has_value("brute_range")
            and not s.has_value("brute_result")
        ),
        apply=lambda s: _apply_brute_force(s),
        cost=2.0,
        category="general",
        description="Brute-force search over a small range",
    ))

    registry.tools.append(ToolOperator(
        name="finalize_brute_result",
        precondition=lambda s: (
            s.has_value("brute_result") and s.candidate_answer is None
        ),
        apply=lambda s: _apply_finalize_brute(s),
        cost=0.1,
        category="finalize",
    ))

    registry.tools.append(ToolOperator(
        name="finalize_sympy_result",
        precondition=lambda s: (
            s.has_value("sympy_result") and s.candidate_answer is None
        ),
        apply=lambda s: _apply_finalize_sympy(s),
        cost=0.1,
        category="finalize",
    ))


# =====================================================================
# PRECONDITION HELPERS
# =====================================================================

def _has_digit_pattern_ext(text: str) -> bool:
    tl = text.lower()
    return any(p in tl for p in ["digit sum", "sum of digits", "digital root", "sum of the digits"])

def _has_binomial_pattern(text: str) -> bool:
    return bool(re.search(r'\\binom|[Cc]\s*\(\s*\d+|choose|\\choose|combination', text))

def _has_counting_pattern(text: str) -> bool:
    tl = text.lower()
    return any(w in tl for w in [
        "how many", "number of ways", "arrangements", "permutation",
        "derangement", "count", "in how many", "total number",
    ])

def _has_polynomial_pattern(text: str) -> bool:
    return bool(re.search(r'x\^[{]?\d+[}]?|polynomial|roots?|vieta', text, re.IGNORECASE))

def _has_sum_pattern(text: str) -> bool:
    tl = text.lower()
    return bool(re.search(r'\\sum|sum of|sum |\\sigma|arithmetic series|geometric series|1\s*\^\s*2.*2\s*\^\s*2|1\s*\^\s*3.*2\s*\^\s*3', tl))

def _has_triangle_pattern(text: str) -> bool:
    tl = text.lower()
    return any(w in tl for w in [
        "triangle", "incircle", "circumscribed", "inscribed",
        "altitude", "median", "inradius", "circumradius",
    ])

def _has_circle_pattern(text: str) -> bool:
    tl = text.lower()
    return any(w in tl for w in [
        "circle", "radius", "diameter", "tangent", "chord",
        "arc", "sector", "circumference",
    ])


# =====================================================================
# COMBINATORICS IMPLEMENTATIONS
# =====================================================================

def _apply_extract_binomial(state: SearchState) -> list[SearchState]:
    text = state.get_value("problem_text")
    results = []

    # C(n, k), \binom{n}{k}
    for match in re.finditer(r'(?:C\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)|\\binom\s*[{](\d+)[}]\s*[{](\d+)[}])', text):
        n = int(match.group(1) or match.group(3))
        k = int(match.group(2) or match.group(4))
        s = state.clone()
        s.set_value("binom_n", n, ValueType.INTEGER, "extract_binomial")
        s.set_value("binom_k", k, ValueType.INTEGER, "extract_binomial")
        s.set_value("comb_type", "binomial", ValueType.EXPRESSION, "extract_binomial")
        # Check for modulus
        mod_match = re.search(r'(?:mod|\\pmod|\\bmod)\s*[{]?(\d+)[}]?', text)
        if mod_match:
            s.set_value("comb_modulus", int(mod_match.group(1)), ValueType.INTEGER, "extract_binomial")
        s.producing_tool = "extract_binomial"
        s.applied_tools = state.applied_tools + ("extract_binomial",)
        s.g_cost = state.g_cost + 0.5
        results.append(s)
        break
    return results


def _apply_extract_counting(state: SearchState) -> list[SearchState]:
    text = state.get_value("problem_text").lower()
    results = []

    # Derangement detection
    if "derangement" in text or ("no.*fixed point" in text and "permutation" in text):
        n_match = re.search(r'(\d+)\s*(?:elements?|objects?|letters?|cards?|people)', text)
        if n_match:
            s = state.clone()
            s.set_value("derangement_n", int(n_match.group(1)), ValueType.INTEGER, "extract_counting")
            s.set_value("comb_type", "derangement", ValueType.EXPRESSION, "extract_counting")
            mod_match = re.search(r'(?:mod|\\pmod)\s*[{]?(\d+)[}]?', text)
            if mod_match:
                s.set_value("comb_modulus", int(mod_match.group(1)), ValueType.INTEGER, "extract_counting")
            # "last N digits" -> mod 10^N
            last_match = re.search(r'last\s+(\w+)\s+digits?', text)
            if last_match and not mod_match:
                word_map = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                             "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
                nd = word_map.get(last_match.group(1))
                if nd is None:
                    try:
                        nd = int(last_match.group(1))
                    except ValueError:
                        nd = None
                if nd:
                    s.set_value("comb_modulus", 10 ** nd, ValueType.INTEGER, "extract_counting")
            s.producing_tool = "extract_counting"
            s.applied_tools = state.applied_tools + ("extract_counting",)
            s.g_cost = state.g_cost + 0.5
            results.append(s)

    # Catalan detection
    if "catalan" in text or "parenthesization" in text or "ballot" in text:
        n_match = re.search(r'(\d+)', text)
        if n_match:
            s = state.clone()
            s.set_value("catalan_n", int(n_match.group(1)), ValueType.INTEGER, "extract_counting")
            s.set_value("comb_type", "catalan", ValueType.EXPRESSION, "extract_counting")
            s.producing_tool = "extract_counting"
            s.applied_tools = state.applied_tools + ("extract_counting",)
            s.g_cost = state.g_cost + 0.5
            results.append(s)

    return results


def _lucas_binomial(n: int, k: int, p: int) -> int:
    """Compute C(n, k) mod p using Lucas' theorem (p must be prime)."""
    if k > n:
        return 0
    result = 1
    while n > 0 or k > 0:
        ni = n % p
        ki = k % p
        if ki > ni:
            return 0
        # Compute C(ni, ki) mod p directly
        num = 1
        den = 1
        for i in range(ki):
            num = (num * (ni - i)) % p
            den = (den * (i + 1)) % p
        result = (result * num * pow(den, p - 2, p)) % p
        n //= p
        k //= p
    return result


def _binomial(n: int, k: int) -> int:
    """Compute C(n, k) exactly."""
    if k > n:
        return 0
    if k > n - k:
        k = n - k
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result


def _apply_binomial_mod(state: SearchState) -> list[SearchState]:
    n = state.get_value("binom_n")
    k = state.get_value("binom_k")
    mod = state.get_value("comb_modulus")

    if mod is not None:
        from sympy import isprime
        if isprime(mod):
            result = _lucas_binomial(n, k, mod)
        else:
            result = _binomial(n, k) % mod
    else:
        result = _binomial(n, k)

    s = state.clone()
    s.set_value("comb_result", result, ValueType.INTEGER, "compute_binomial_mod")
    s.answer_confidence = 1.0
    s.producing_tool = "compute_binomial_mod"
    s.applied_tools = state.applied_tools + ("compute_binomial_mod",)
    s.g_cost = state.g_cost + 1.0
    return [s]


def _apply_catalan(state: SearchState) -> list[SearchState]:
    n = state.get_value("catalan_n")
    mod = state.get_value("comb_modulus")

    # C(n) = C(2n, n) / (n + 1)
    c = _binomial(2 * n, n) // (n + 1)
    if mod:
        c = c % mod

    s = state.clone()
    s.set_value("comb_result", c, ValueType.INTEGER, "compute_catalan")
    s.answer_confidence = 1.0
    s.producing_tool = "compute_catalan"
    s.applied_tools = state.applied_tools + ("compute_catalan",)
    s.g_cost = state.g_cost + 1.0
    return [s]


def _apply_derangements(state: SearchState) -> list[SearchState]:
    n = state.get_value("derangement_n")
    mod = state.get_value("comb_modulus")

    # D(n) = (n-1)(D(n-1) + D(n-2)), D(0)=1, D(1)=0
    if n == 0:
        d = 1
    elif n == 1:
        d = 0
    else:
        d_prev2, d_prev1 = 1, 0
        for i in range(2, n + 1):
            d = (i - 1) * (d_prev1 + d_prev2)
            if mod:
                d = d % mod
            d_prev2, d_prev1 = d_prev1, d
        d = d_prev1

    s = state.clone()
    s.set_value("comb_result", d, ValueType.INTEGER, "compute_derangements")
    s.answer_confidence = 1.0
    s.producing_tool = "compute_derangements"
    s.applied_tools = state.applied_tools + ("compute_derangements",)
    s.g_cost = state.g_cost + 1.0
    return [s]


def _apply_inclusion_exclusion(state: SearchState) -> list[SearchState]:
    sets = state.get_value("ie_sets")  # list of set sizes and intersections
    # Expects: {"total": N, "sets": [|A|, |B|, ...], "pairs": [|A∩B|, ...], ...}
    total = sets.get("total", 0)
    singles = sets.get("sets", [])
    pairs = sets.get("pairs", [])
    triples = sets.get("triples", [])

    result = total - sum(singles) + sum(pairs) - sum(triples)

    s = state.clone()
    s.set_value("comb_result", result, ValueType.INTEGER, "inclusion_exclusion")
    s.answer_confidence = 0.9
    s.producing_tool = "inclusion_exclusion"
    s.applied_tools = state.applied_tools + ("inclusion_exclusion",)
    s.g_cost = state.g_cost + 1.5
    return [s]


def _apply_finalize_comb(state: SearchState) -> list[SearchState]:
    s = state.clone()
    s.candidate_answer = int(state.get_value("comb_result"))
    s.answer_confidence = state.answer_confidence if state.answer_confidence > 0 else 1.0
    s.producing_tool = "finalize_comb_result"
    s.applied_tools = state.applied_tools + ("finalize_comb_result",)
    s.g_cost = state.g_cost + 0.1
    return [s]


# =====================================================================
# ALGEBRA IMPLEMENTATIONS
# =====================================================================

def _apply_extract_polynomial(state: SearchState) -> list[SearchState]:
    text = state.get_value("problem_text")
    results = []

    # Vieta's: "sum of roots", "product of roots"
    if re.search(r'vieta|sum of.*roots|product of.*roots', text, re.IGNORECASE):
        # Extract polynomial coefficients
        # e.g., x^3 - 6x^2 + 11x - 6 = 0
        poly_match = re.search(
            r'x\^[{]?(\d+)[}]?\s*([+-]\s*\d*x[^=]*?)=\s*0', text
        )
        if poly_match:
            s = state.clone()
            s.set_value("poly_text", text, ValueType.EXPRESSION, "extract_polynomial")
            s.set_value("vieta_query", "sum_and_product", ValueType.EXPRESSION, "extract_polynomial")
            s.producing_tool = "extract_polynomial"
            s.applied_tools = state.applied_tools + ("extract_polynomial",)
            s.g_cost = state.g_cost + 0.5
            results.append(s)

    # General polynomial equation
    # Try to use SymPy to parse
    if "solve" in text.lower() or "roots" in text.lower() or "find" in text.lower():
        s = state.clone()
        s.set_value("poly_text", text, ValueType.EXPRESSION, "extract_polynomial")
        s.producing_tool = "extract_polynomial"
        s.applied_tools = state.applied_tools + ("extract_polynomial",)
        s.g_cost = state.g_cost + 0.5
        results.append(s)

    return results[:1]  # Take best match


def _apply_extract_sum(state: SearchState) -> list[SearchState]:
    text = state.get_value("problem_text").lower()
    results = []

    # Sum of squares: "1^2 + 2^2 + ... + N^2" — extract N (the last number before ^2)
    sq_match = re.search(r'1\s*\^\s*2\s*\+\s*2\s*\^\s*2\s*\+\s*.*?\+\s*(\d+)\s*\^\s*2', text)
    if not sq_match:
        # "sum of squares ... N" — grab the largest number
        sq_match = re.search(r'sum.*?squares.*?(\d+)\^2', text)
    if not sq_match:
        # "sum of squares 1^2 + ... + n^2" with n given elsewhere
        sq_match = re.search(r'sum.*?squares.*?(\d+)', text)
    if sq_match:
        n = int(sq_match.group(1))
        if n > 1:  # Sanity check
            s = state.clone()
            s.set_value("sum_type", "squares", ValueType.EXPRESSION, "extract_sum")
            s.set_value("sum_n", n, ValueType.INTEGER, "extract_sum")
            mod_match = re.search(r'(?:mod|\\pmod)\s*[{]?(\d+)[}]?', text)
            if mod_match:
                s.set_value("sum_modulus", int(mod_match.group(1)), ValueType.INTEGER, "extract_sum")
            s.producing_tool = "extract_sum"
            s.applied_tools = state.applied_tools + ("extract_sum",)
            s.g_cost = state.g_cost + 0.5
            results.append(s)

    # Sum of cubes: "1^3 + 2^3 + ... + N^3"
    cube_match = re.search(r'1\s*\^\s*3\s*\+\s*2\s*\^\s*3\s*\+\s*.*?\+\s*(\d+)\s*\^\s*3', text)
    if not cube_match:
        cube_match = re.search(r'sum.*?cubes.*?(\d+)\^3', text)
    if not cube_match:
        cube_match = re.search(r'sum.*?cubes.*?(\d+)', text)
    if cube_match and not results:
        n = int(cube_match.group(1))
        if n > 1:
            s = state.clone()
            s.set_value("sum_type", "cubes", ValueType.EXPRESSION, "extract_sum")
            s.set_value("sum_n", n, ValueType.INTEGER, "extract_sum")
            mod_match = re.search(r'(?:mod|\\pmod)\s*[{]?(\d+)[}]?', text)
            if mod_match:
                s.set_value("sum_modulus", int(mod_match.group(1)), ValueType.INTEGER, "extract_sum")
            s.producing_tool = "extract_sum"
            s.applied_tools = state.applied_tools + ("extract_sum",)
            s.g_cost = state.g_cost + 0.5
            results.append(s)

    # Arithmetic series: "3 + 7 + 11 + ... + 399"
    arith_match = re.search(r'(\d+)\s*\+\s*(\d+)\s*\+\s*(\d+)\s*\+\s*(?:\.\s*){2,}\s*\+\s*(\d+)', text)
    if not arith_match:
        arith_match = re.search(r'sum\s+(\d+)\s*\+\s*(\d+)\s*\+\s*.*?\+\s*(\d+)', text)
        if arith_match:
            # Repack into 4-group format
            a1 = int(arith_match.group(1))
            a2 = int(arith_match.group(2))
            an = int(arith_match.group(3))
            d = a2 - a1
            if d != 0:
                n = (an - a1) // d + 1
                s = state.clone()
                s.set_value("sum_type", "arithmetic", ValueType.EXPRESSION, "extract_sum")
                s.set_value("sum_a1", a1, ValueType.INTEGER, "extract_sum")
                s.set_value("sum_d", d, ValueType.INTEGER, "extract_sum")
                s.set_value("sum_n", n, ValueType.INTEGER, "extract_sum")
                s.producing_tool = "extract_sum"
                s.applied_tools = state.applied_tools + ("extract_sum",)
                s.g_cost = state.g_cost + 0.5
                results.append(s)
            arith_match = None  # Already handled
    if arith_match and not results:
        a1 = int(arith_match.group(1))
        a2 = int(arith_match.group(2))
        an = int(arith_match.group(4))
        d = a2 - a1
        if d != 0:
            n = (an - a1) // d + 1
            s = state.clone()
            s.set_value("sum_type", "arithmetic", ValueType.EXPRESSION, "extract_sum")
            s.set_value("sum_a1", a1, ValueType.INTEGER, "extract_sum")
            s.set_value("sum_d", d, ValueType.INTEGER, "extract_sum")
            s.set_value("sum_n", n, ValueType.INTEGER, "extract_sum")
            s.producing_tool = "extract_sum"
            s.applied_tools = state.applied_tools + ("extract_sum",)
            s.g_cost = state.g_cost + 0.5
            results.append(s)

    # Geometric series
    geo_match = re.search(r'geometric.*ratio\s*[=]?\s*(\d+(?:/\d+)?)', text)
    if geo_match and not results:
        r_str = geo_match.group(1)
        r = Fraction(r_str)
        n_match = re.search(r'(\d+)\s*terms?', text)
        a_match = re.search(r'first\s+term\s*[=:]\s*(\d+)', text)
        if n_match:
            s = state.clone()
            s.set_value("sum_type", "geometric", ValueType.EXPRESSION, "extract_sum")
            s.set_value("sum_n", int(n_match.group(1)), ValueType.INTEGER, "extract_sum")
            s.set_value("sum_r", r, ValueType.RATIONAL, "extract_sum")
            if a_match:
                s.set_value("sum_a1", int(a_match.group(1)), ValueType.INTEGER, "extract_sum")
            s.producing_tool = "extract_sum"
            s.applied_tools = state.applied_tools + ("extract_sum",)
            s.g_cost = state.g_cost + 0.5
            results.append(s)

    return results[:1]


def _apply_compute_sum(state: SearchState) -> list[SearchState]:
    sum_type = state.get_value("sum_type")
    n = state.get_value("sum_n")
    mod = state.get_value("sum_modulus")

    if sum_type == "squares":
        result = n * (n + 1) * (2 * n + 1) // 6
    elif sum_type == "cubes":
        s_n = n * (n + 1) // 2
        result = s_n * s_n
    elif sum_type == "arithmetic":
        a1 = state.get_value("sum_a1", 1)
        d = state.get_value("sum_d", 1)
        result = n * (2 * a1 + (n - 1) * d) // 2
    elif sum_type == "geometric":
        a1 = state.get_value("sum_a1", 1)
        r = state.get_value("sum_r", Fraction(2))
        if r == 1:
            result = a1 * n
        else:
            result = int(a1 * (r ** n - 1) / (r - 1))
    else:
        return []

    if mod:
        result = result % mod

    s = state.clone()
    s.set_value("alg_result", int(result), ValueType.INTEGER, f"compute_sum_{sum_type}")
    s.answer_confidence = 1.0
    s.producing_tool = "compute_sum"
    s.applied_tools = state.applied_tools + ("compute_sum",)
    s.g_cost = state.g_cost + 1.0
    return [s]


def _apply_solve_polynomial(state: SearchState) -> list[SearchState]:
    # Use SymPy to solve
    try:
        from sympy import symbols, solve, Poly, sympify
        x = symbols('x')
        text = state.get_value("poly_text", "")

        # Try to extract equation from text
        eq_match = re.search(r'([\dx\^\s\+\-\*{}/]+)\s*=\s*0', text)
        if eq_match:
            expr_str = eq_match.group(1)
            expr_str = re.sub(r'(\d+)x', r'\1*x', expr_str)
            expr_str = re.sub(r'x\^[{]?(\d+)[}]?', r'x**\1', expr_str)
            try:
                expr = sympify(expr_str)
                roots = solve(expr, x)
                s = state.clone()
                s.set_value("poly_roots", [complex(r) for r in roots], ValueType.SET, "solve_polynomial")
                s.set_value("poly_coeffs", Poly(expr, x).all_coeffs(), ValueType.SEQUENCE, "solve_polynomial")
                s.producing_tool = "solve_polynomial"
                s.applied_tools = state.applied_tools + ("solve_polynomial",)
                s.g_cost = state.g_cost + 1.5
                return [s]
            except Exception:
                pass
    except ImportError:
        pass
    return []


def _apply_vietas(state: SearchState) -> list[SearchState]:
    coeffs = state.get_value("poly_coeffs")
    if not coeffs or len(coeffs) < 2:
        return []

    # Vieta's: for a_n*x^n + ... + a_0 = 0
    # sum of roots = -a_{n-1}/a_n
    # product of roots = (-1)^n * a_0/a_n
    a_n = coeffs[0]
    if a_n == 0:
        return []

    n = len(coeffs) - 1
    sum_roots = -coeffs[1] / a_n if len(coeffs) > 1 else 0
    prod_roots = ((-1) ** n) * coeffs[-1] / a_n

    s = state.clone()
    s.set_value("vieta_sum", Fraction(sum_roots).limit_denominator(10**6), ValueType.RATIONAL, "apply_vietas")
    s.set_value("vieta_product", Fraction(prod_roots).limit_denominator(10**6), ValueType.RATIONAL, "apply_vietas")
    s.set_value("vieta_result", int(sum_roots + prod_roots), ValueType.INTEGER, "apply_vietas")
    s.producing_tool = "apply_vietas"
    s.applied_tools = state.applied_tools + ("apply_vietas",)
    s.g_cost = state.g_cost + 1.0
    return [s]


def _apply_diophantine(state: SearchState) -> list[SearchState]:
    try:
        from sympy import symbols, diophantine, sympify
        eq_str = state.get_value("dioph_equation")
        x, y = symbols('x y')
        expr = sympify(eq_str)
        solutions = diophantine(expr)
        if solutions:
            s = state.clone()
            s.set_value("alg_result", len(solutions), ValueType.INTEGER, "solve_diophantine")
            s.answer_confidence = 1.0
            s.producing_tool = "solve_diophantine"
            s.applied_tools = state.applied_tools + ("solve_diophantine",)
            s.g_cost = state.g_cost + 2.0
            return [s]
    except Exception:
        pass
    return []


def _apply_floor_ceiling(state: SearchState) -> list[SearchState]:
    expr = state.get_value("floor_expr")
    try:
        result = int(math.floor(eval(expr)))
        s = state.clone()
        s.set_value("alg_result", result, ValueType.INTEGER, "compute_floor_ceiling")
        s.answer_confidence = 1.0
        s.producing_tool = "compute_floor_ceiling"
        s.applied_tools = state.applied_tools + ("compute_floor_ceiling",)
        s.g_cost = state.g_cost + 1.0
        return [s]
    except Exception:
        return []


def _apply_finalize_alg(state: SearchState) -> list[SearchState]:
    s = state.clone()
    s.candidate_answer = int(state.get_value("alg_result"))
    s.answer_confidence = state.answer_confidence if state.answer_confidence > 0 else 1.0
    s.producing_tool = "finalize_alg_result"
    s.applied_tools = state.applied_tools + ("finalize_alg_result",)
    s.g_cost = state.g_cost + 0.1
    return [s]


# =====================================================================
# GEOMETRY IMPLEMENTATIONS
# =====================================================================

def _apply_extract_triangle(state: SearchState) -> list[SearchState]:
    text = state.get_value("problem_text")
    results = []

    # Extract sides: "sides 3, 4, and 5" or "sides 3, 4, 5" or "a=X, b=Y, c=Z"
    side_match = re.findall(
        r'(?:sides?|lengths?)\s*(?:of\s+)?(?:are\s+)?(\d+)\s*,\s*(\d+)\s*(?:,\s*and\s*|\s*,\s*and\s+|,\s*)(\d+)',
        text.lower()
    )
    if not side_match:
        side_match = re.findall(r'a\s*=\s*(\d+)\s*,\s*b\s*=\s*(\d+)\s*,\s*c\s*=\s*(\d+)', text.lower())
    if not side_match:
        # "has sides X, Y and Z"
        side_match = re.findall(r'(\d+)\s*,\s*(\d+)\s*(?:,\s*)?and\s*(\d+)', text.lower())

    if side_match:
        a, b, c = int(side_match[0][0]), int(side_match[0][1]), int(side_match[0][2])
        s = state.clone()
        s.set_value("geo_type", "triangle", ValueType.EXPRESSION, "extract_triangle")
        s.set_value("tri_sides", (a, b, c), ValueType.SEQUENCE, "extract_triangle")

        # What are we asked to find?
        tl = text.lower()
        if "area" in tl:
            s.set_value("geo_query", "area", ValueType.EXPRESSION, "extract_triangle")
        elif "inradius" in tl or "incircle" in tl:
            s.set_value("geo_query", "inradius", ValueType.EXPRESSION, "extract_triangle")
        elif "circumradius" in tl or "circumscribed" in tl:
            s.set_value("geo_query", "circumradius", ValueType.EXPRESSION, "extract_triangle")
        elif "perimeter" in tl:
            s.set_value("geo_query", "perimeter", ValueType.EXPRESSION, "extract_triangle")

        s.producing_tool = "extract_triangle"
        s.applied_tools = state.applied_tools + ("extract_triangle",)
        s.g_cost = state.g_cost + 0.5
        results.append(s)

    return results


def _apply_extract_circle(state: SearchState) -> list[SearchState]:
    text = state.get_value("problem_text").lower()
    results = []

    r_match = re.search(r'radius\s*(?:of|=|is)\s*(\d+)', text)
    if r_match:
        s = state.clone()
        s.set_value("geo_type", "circle", ValueType.EXPRESSION, "extract_circle")
        s.set_value("circle_radius", int(r_match.group(1)), ValueType.INTEGER, "extract_circle")
        if "area" in text:
            s.set_value("geo_query", "area", ValueType.EXPRESSION, "extract_circle")
        elif "circumference" in text:
            s.set_value("geo_query", "circumference", ValueType.EXPRESSION, "extract_circle")
        s.producing_tool = "extract_circle"
        s.applied_tools = state.applied_tools + ("extract_circle",)
        s.g_cost = state.g_cost + 0.5
        results.append(s)
    return results


def _apply_triangle_area(state: SearchState) -> list[SearchState]:
    sides = state.get_value("tri_sides")
    a, b, c = sides

    # Heron's formula
    s_val = (a + b + c) / 2
    area_sq = s_val * (s_val - a) * (s_val - b) * (s_val - c)
    if area_sq < 0:
        return []

    area = math.sqrt(area_sq)

    # Check if area is integer or has clean form
    s = state.clone()
    if abs(area - round(area)) < 1e-9:
        s.set_value("geo_result", int(round(area)), ValueType.INTEGER, "compute_triangle_area")
    else:
        # Return area * some multiplier if problem asks for integer
        # Check if 4*area^2 is a perfect integer (common in competition)
        area_sq_4 = 4 * area_sq
        if abs(area_sq_4 - round(area_sq_4)) < 1e-9:
            s.set_value("geo_result", int(round(area_sq_4)), ValueType.INTEGER, "compute_triangle_area")
            s.set_value("geo_note", "This is 4*area^2, not area", ValueType.EXPRESSION, "compute_triangle_area")
        else:
            # Store as Fraction if possible
            from fractions import Fraction
            area_frac = Fraction(a + b + c, 2)
            s.set_value("triangle_area_exact", area, ValueType.RATIONAL, "compute_triangle_area")
            s.set_value("geo_result", int(round(area)), ValueType.INTEGER, "compute_triangle_area")

    s.answer_confidence = 1.0
    s.producing_tool = "compute_triangle_area"
    s.applied_tools = state.applied_tools + ("compute_triangle_area",)
    s.g_cost = state.g_cost + 1.0
    return [s]


def _apply_triangle_properties(state: SearchState) -> list[SearchState]:
    sides = state.get_value("tri_sides")
    a, b, c = sides

    s_val = (a + b + c) / 2
    area_sq = s_val * (s_val - a) * (s_val - b) * (s_val - c)
    if area_sq < 0:
        return []
    area = math.sqrt(area_sq)

    results = []
    query = state.get_value("geo_query", "")

    s = state.clone()
    s.set_value("triangle_area", area, ValueType.RATIONAL, "compute_triangle_properties")
    s.set_value("triangle_perimeter", a + b + c, ValueType.INTEGER, "compute_triangle_properties")

    if area > 0:
        inradius = area / s_val
        s.set_value("inradius", inradius, ValueType.RATIONAL, "compute_triangle_properties")

    circumradius = (a * b * c) / (4 * area) if area > 0 else None
    if circumradius is not None:
        s.set_value("circumradius", circumradius, ValueType.RATIONAL, "compute_triangle_properties")

    # Set geo_result based on query
    if query == "inradius" and area > 0:
        ir = area / s_val
        if abs(ir - round(ir)) < 1e-9:
            s.set_value("geo_result", int(round(ir)), ValueType.INTEGER, "compute_triangle_properties")
        else:
            s.set_value("geo_result", int(round(ir * 100)) , ValueType.INTEGER, "compute_triangle_properties")
            s.set_value("geo_note", "inradius * 100", ValueType.EXPRESSION, "compute_triangle_properties")
    elif query == "circumradius" and circumradius:
        if abs(circumradius - round(circumradius)) < 1e-9:
            s.set_value("geo_result", int(round(circumradius)), ValueType.INTEGER, "compute_triangle_properties")
    elif query == "area":
        if abs(area - round(area)) < 1e-9:
            s.set_value("geo_result", int(round(area)), ValueType.INTEGER, "compute_triangle_properties")
    elif query == "perimeter":
        s.set_value("geo_result", a + b + c, ValueType.INTEGER, "compute_triangle_properties")

    s.answer_confidence = 1.0
    s.producing_tool = "compute_triangle_properties"
    s.applied_tools = state.applied_tools + ("compute_triangle_properties",)
    s.g_cost = state.g_cost + 1.0
    results.append(s)

    return results


def _apply_coordinate_geometry(state: SearchState) -> list[SearchState]:
    # Generic coordinate geometry - uses SymPy geometry module
    try:
        from sympy.geometry import Point, Line, Circle, Triangle as SymTriangle
        points = state.get_value("geo_points")
        # points is a dict of name -> (x, y)
        sym_points = {name: Point(x, y) for name, (x, y) in points.items()}

        query = state.get_value("geo_query", "distance")

        if query == "distance" and len(sym_points) >= 2:
            names = list(sym_points.keys())
            d = sym_points[names[0]].distance(sym_points[names[1]])
            s = state.clone()
            s.set_value("geo_result", int(d) if d == int(d) else float(d), ValueType.RATIONAL, "coordinate_geometry")
            s.answer_confidence = 1.0
            s.producing_tool = "coordinate_geometry"
            s.applied_tools = state.applied_tools + ("coordinate_geometry",)
            s.g_cost = state.g_cost + 1.5
            return [s]

    except Exception:
        pass
    return []


def _apply_circle_properties(state: SearchState) -> list[SearchState]:
    r = state.get_value("circle_radius")
    query = state.get_value("geo_query", "area")

    s = state.clone()
    if query == "area":
        # For competition: often asks for area/pi or area in terms of pi
        area = math.pi * r * r
        s.set_value("geo_result", int(round(area)), ValueType.INTEGER, "compute_circle_properties")
        s.set_value("geo_result_exact", f"{r*r}*pi", ValueType.EXPRESSION, "compute_circle_properties")
    elif query == "circumference":
        circ = 2 * math.pi * r
        s.set_value("geo_result", int(round(circ)), ValueType.INTEGER, "compute_circle_properties")

    s.answer_confidence = 0.8  # Lower confidence since pi rounding
    s.producing_tool = "compute_circle_properties"
    s.applied_tools = state.applied_tools + ("compute_circle_properties",)
    s.g_cost = state.g_cost + 1.0
    return [s]


def _apply_finalize_geo(state: SearchState) -> list[SearchState]:
    s = state.clone()
    result = state.get_value("geo_result")
    s.candidate_answer = int(result) if result is not None else None
    s.answer_confidence = state.answer_confidence if state.answer_confidence > 0 else 1.0
    s.producing_tool = "finalize_geo_result"
    s.applied_tools = state.applied_tools + ("finalize_geo_result",)
    s.g_cost = state.g_cost + 0.1
    return [s]


# =====================================================================
# GENERAL TOOL IMPLEMENTATIONS
# =====================================================================

def _apply_sympy_solve(state: SearchState) -> list[SearchState]:
    try:
        from sympy import symbols, solve, sympify
        eq_str = state.get_value("sympy_equation")
        x = symbols('x')
        expr = sympify(eq_str)
        sols = solve(expr, x)
        if sols:
            s = state.clone()
            s.set_value("sympy_result", int(sols[0]) if len(sols) == 1 else len(sols),
                        ValueType.INTEGER, "sympy_solve_generic")
            s.answer_confidence = 1.0
            s.producing_tool = "sympy_solve_generic"
            s.applied_tools = state.applied_tools + ("sympy_solve_generic",)
            s.g_cost = state.g_cost + 2.0
            return [s]
    except Exception:
        pass
    return []


def _apply_brute_force(state: SearchState) -> list[SearchState]:
    fn = state.get_value("brute_fn")
    lo, hi = state.get_value("brute_range")
    for val in range(lo, hi + 1):
        if fn(val):
            s = state.clone()
            s.set_value("brute_result", val, ValueType.INTEGER, "brute_force_small")
            s.answer_confidence = 1.0
            s.producing_tool = "brute_force_small"
            s.applied_tools = state.applied_tools + ("brute_force_small",)
            s.g_cost = state.g_cost + 2.0
            return [s]
    return []


def _apply_finalize_brute(state: SearchState) -> list[SearchState]:
    s = state.clone()
    s.candidate_answer = state.get_value("brute_result")
    s.answer_confidence = 1.0
    s.producing_tool = "finalize_brute_result"
    s.applied_tools = state.applied_tools + ("finalize_brute_result",)
    s.g_cost = state.g_cost + 0.1
    return [s]


def _apply_finalize_sympy(state: SearchState) -> list[SearchState]:
    s = state.clone()
    s.candidate_answer = state.get_value("sympy_result")
    s.answer_confidence = 1.0
    s.producing_tool = "finalize_sympy_result"
    s.applied_tools = state.applied_tools + ("finalize_sympy_result",)
    s.g_cost = state.g_cost + 0.1
    return [s]


# =====================================================================
# EXTENDED HEURISTIC (domain-aware)
# =====================================================================

def extended_heuristic(state: SearchState) -> float:
    """Enhanced heuristic that understands all 4 AIMO domains."""
    h = base_heuristic(state)

    # Combinatorics signals
    if state.has_value("comb_type"):
        h -= 0.5
    if state.has_value("binom_n") or state.has_value("catalan_n") or state.has_value("derangement_n"):
        h -= 0.5
    if state.has_value("comb_result"):
        h = min(h, 0.5)

    # Algebra signals
    if state.has_value("sum_type") or state.has_value("poly_text"):
        h -= 0.5
    if state.has_value("alg_result") or state.has_value("vieta_result"):
        h = min(h, 0.5)

    # Geometry signals
    if state.has_value("geo_type"):
        h -= 0.5
    if state.has_value("tri_sides") or state.has_value("circle_radius"):
        h -= 0.5
    if state.has_value("geo_result"):
        h = min(h, 0.5)

    return max(0.0, h)


# =====================================================================
# EXTENDED SOLVER
# =====================================================================

def astar_solve_extended(
    problem_text: str,
    max_states: int = 1000,
    max_time: float = 60.0,
    verbose: bool = False,
) -> SearchResult:
    """A* solve with extended tool registry (all 4 AIMO domains)."""
    import astar_solver

    # Monkey-patch the heuristic
    original_heuristic = astar_solver.heuristic
    astar_solver.heuristic = extended_heuristic

    # Extend the registry
    original_init = ToolRegistry._register_all_tools

    def patched_init(self):
        original_init(self)
        extend_registry(self)

    ToolRegistry._register_all_tools = patched_init

    try:
        result = astar_solve(problem_text, max_states=max_states,
                             max_time=max_time, verbose=verbose)
    finally:
        astar_solver.heuristic = original_heuristic
        ToolRegistry._register_all_tools = original_init

    return result


# =====================================================================
# COMPREHENSIVE TEST SUITE
# =====================================================================

if __name__ == "__main__":
    import time as time_mod

    problems = [
        # --- NUMBER THEORY (7 problems) ---
        ("NT1: 2^2024 mod 7",
         "Find 2^{2024} mod 7.",
         pow(2, 2024, 7)),

        ("NT2: 3^999 mod 13",
         "Find 3^{999} mod 13.",
         pow(3, 999, 13)),

        ("NT3: last 3 digits of 7^999",
         "Find the last three digits of 7^{999}.",
         pow(7, 999, 1000)),

        ("NT4: 17^2023 mod 100",
         "What is the remainder when 17^{2023} is divided by 100?",
         pow(17, 2023, 100)),

        ("NT5: 2^10000 mod 9",
         "Find 2^{10000} mod 9.",
         pow(2, 10000, 9)),

        ("NT6: 13^2025 mod 1000",
         "Find the last three digits of 13^{2025}.",
         pow(13, 2025, 1000)),

        ("NT7: 7^7^7 mod 10",
         "Find 7^{343} mod 10.",
         pow(7, 343, 10)),

        # --- FIBONACCI / SEQUENCES (3 problems) ---
        ("SEQ1: F(10^6) mod 10007",
         "Find F(1000000) mod 10007, where F(n) is the nth Fibonacci number.",
         None),  # computed below

        ("SEQ2: F(100) mod 997",
         "Find F(100) mod 997, where F(n) is the nth Fibonacci number.",
         None),  # computed below

        ("SEQ3: 50000^2 mod 97",
         "Find 50000^{2} mod 97.",
         (50000**2) % 97),

        # --- COMBINATORICS (5 problems) ---
        ("COMB1: C(100,3)",
         "Compute \\binom{100}{3}.",
         161700),

        ("COMB2: C(1000,2) mod 997",
         "Compute \\binom{1000}{2} \\pmod{997}.",
         (1000 * 999 // 2) % 997),

        ("COMB3: C(20,10)",
         "Compute C(20, 10).",
         184756),

        ("COMB4: D(5) derangements",
         "Find the number of derangements of 5 elements (permutations with no fixed points).",
         44),

        ("COMB5: D(10) derangements",
         "Find the number of derangements of 10 elements.",
         1334961),

        # --- ALGEBRA (4 problems) ---
        ("ALG1: sum of squares to 100",
         "Find the sum of squares 1^2 + 2^2 + ... + 100^2.",
         338350),

        ("ALG2: sum of cubes to 50",
         "Find the sum of cubes 1^3 + 2^3 + ... + 50^3.",
         1625625),

        ("ALG3: arithmetic series",
         "Find the sum 3 + 7 + 11 + ... + 399.",
         20100),

        ("ALG4: sum of squares mod 10007",
         "Find the sum of squares 1^2 + 2^2 + ... + 1000^2 mod 10007.",
         333833500 % 10007),

        # --- GEOMETRY (3 problems) ---
        ("GEO1: triangle area (3,4,5)",
         "A triangle has sides 3, 4, and 5. Find its area.",
         6),

        ("GEO2: triangle area (13,14,15)",
         "A triangle has sides 13, 14, and 15. Find its area.",
         84),

        ("GEO3: triangle perimeter",
         "A triangle has sides 7, 24, and 25. Find its perimeter.",
         56),
    ]

    # Compute Fibonacci ground truths
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

    problems[7] = (problems[7][0], problems[7][1], fib_mod_fast(1000000, 10007))
    problems[8] = (problems[8][0], problems[8][1], fib_mod_fast(100, 997))

    print("=" * 70)
    print("A* TOOL-SPACE SEARCH: COMPREHENSIVE 4-DOMAIN TEST")
    print("=" * 70)
    print(f"Total problems: {len(problems)}")
    print(f"Domains: Number Theory, Sequences, Combinatorics, Algebra, Geometry")

    results_by_domain = {}
    total = 0
    correct = 0
    total_time = 0.0
    total_states = 0

    for name, problem, expected in problems:
        domain = name.split(":")[0]
        total += 1

        t0 = time_mod.time()
        result = astar_solve_extended(problem, verbose=False)
        elapsed = time_mod.time() - t0

        ok = result.answer == expected
        correct += ok
        total_time += elapsed
        total_states += result.states_explored

        status = "PASS" if ok else "FAIL"
        print(f"\n  [{status}] {name}")
        print(f"    Expected: {expected}, Got: {result.answer}")
        print(f"    Path: {result.format_path()}")
        print(f"    States: {result.states_explored}, Time: {elapsed:.3f}s")

        if domain not in results_by_domain:
            results_by_domain[domain] = {"correct": 0, "total": 0}
        results_by_domain[domain]["total"] += 1
        if ok:
            results_by_domain[domain]["correct"] += 1

    print("\n" + "=" * 70)
    print("RESULTS BY DOMAIN")
    print("=" * 70)
    for domain, stats in sorted(results_by_domain.items()):
        c, t = stats["correct"], stats["total"]
        print(f"  {domain:8s}: {c}/{t} ({100*c/t:.0f}%)")
    print(f"  {'TOTAL':8s}: {correct}/{total} ({100*correct/total:.0f}%)")
    print(f"\nTotal states explored: {total_states}")
    print(f"Total time: {total_time:.3f}s")
    print(f"Average time per problem: {total_time/total:.3f}s")
    print("=" * 70)
