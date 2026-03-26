"""Structural exploration for math olympiad problems.

Uses structural fuzzing to empirically discover mathematical structure
(periodicity, recurrences, invariants) in parameterized problems.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np


@dataclass
class DiscoveredStructure:
    """Structure discovered by empirical exploration."""
    problem_type: str
    description: str
    confidence: float
    predicted_answer: Optional[int] = None
    details: dict = field(default_factory=dict)

    def as_hint(self) -> str:
        """Format as a hint for LLM prompt injection."""
        lines = [f"Structural insight ({self.confidence:.0%} confidence):"]
        lines.append(f"  Type: {self.problem_type}")
        lines.append(f"  {self.description}")
        if self.predicted_answer is not None:
            lines.append(f"  Predicted answer: {self.predicted_answer}")
        for k, v in self.details.items():
            if k not in ("summary",):
                lines.append(f"  {k}: {v}")
        return "\n".join(lines)


def detect_periodicity(values: list[int], min_period: int = 1, max_period: int = 100) -> Optional[dict]:
    """Detect periodicity in a sequence of integer values."""
    n = len(values)
    if n < 6:
        return None

    for period in range(min_period, min(max_period + 1, n // 3)):
        for offset in range(min(period, n // 3)):
            matches = 0
            checks = 0
            for i in range(offset, n - period):
                checks += 1
                if values[i] == values[i + period]:
                    matches += 1

            if checks > 0 and matches == checks:
                confirmed = checks
                confidence = min(1.0, confirmed / 10)
                return {
                    "period": period,
                    "offset": offset,
                    "confirmed_cycles": confirmed,
                    "confidence": confidence,
                    "repeating_block": values[offset:offset + period],
                }
    return None


def detect_recurrence(values: list[int], max_order: int = 5) -> Optional[dict]:
    """Detect linear recurrence relations in integer sequences."""
    n = len(values)

    for order in range(1, min(max_order + 1, n // 3)):
        n_eqs = n - order
        if n_eqs < order + 2:
            continue

        A = np.zeros((n_eqs, order + 1))
        b = np.zeros(n_eqs)

        for i in range(n_eqs):
            idx = i + order
            for j in range(order):
                A[i, j] = values[idx - j - 1]
            A[i, order] = 1
            b[i] = values[idx]

        try:
            coeffs, residuals, rank, sv = np.linalg.lstsq(A, b, rcond=None)
            predicted = A @ coeffs
            max_error = np.max(np.abs(predicted - b))

            if max_error < 0.5:
                int_coeffs = [int(round(c)) for c in coeffs[:order]]
                int_const = int(round(coeffs[order]))

                all_match = True
                for i in range(order, n):
                    pred = sum(int_coeffs[j] * values[i - j - 1] for j in range(order)) + int_const
                    if pred != values[i]:
                        all_match = False
                        break

                if all_match:
                    return {
                        "order": order,
                        "coefficients": int_coeffs,
                        "constant": int_const,
                        "confidence": min(1.0, (n - order) / 10),
                        "formula": _format_recurrence(int_coeffs, int_const),
                    }
        except np.linalg.LinAlgError:
            continue

    return None


def find_pisano_period(m: int, max_iter: int = 2_000_000) -> Optional[int]:
    """Find the Pisano period pi(m) — period of Fibonacci sequence mod m.

    The Pisano period always starts with F(0)=0, F(1)=1, so we look for
    the pair (0, 1) to reappear.
    """
    if m == 1:
        return 1
    a, b = 0, 1
    for i in range(1, max_iter + 1):
        a, b = b, (a + b) % m
        if a == 0 and b == 1:
            return i
    return None


def detect_modular_recurrence(values: list[int], modulus: int, max_order: int = 5) -> Optional[dict]:
    """Detect linear recurrence in modular arithmetic.

    Like detect_recurrence but works mod m, avoiding floating-point issues
    with large modular sequences.
    """
    n = len(values)

    for order in range(1, min(max_order + 1, n // 3)):
        # Try to find coefficients c such that
        # a[n] = sum(c[j] * a[n-j-1]) mod modulus
        # Use Gaussian elimination over Z/mZ for prime modulus,
        # or brute force for small order

        if order <= 2:
            # Brute force: try all coefficient combos mod modulus
            # For order 1: a[n] = c * a[n-1] + d mod m
            found = _brute_force_modular_recurrence(values, modulus, order)
            if found:
                return found
        else:
            # For higher order, try least-squares then verify mod m
            n_eqs = n - order
            if n_eqs < order + 2:
                continue

            # Try all possible constant terms (0 only for simplicity)
            for const in [0]:
                # Build system and solve mod m if prime
                A_rows = []
                b_vals = []
                for i in range(order, min(order + order + 2, n)):
                    row = [values[i - j - 1] for j in range(order)]
                    A_rows.append(row)
                    b_vals.append((values[i] - const) % modulus)

                # Try to solve via brute force for small search space
                if order <= 3 and modulus < 1000:
                    found = _brute_force_modular_recurrence(values, modulus, order)
                    if found:
                        return found
                break

    return None


def _brute_force_modular_recurrence(values: list[int], modulus: int, order: int) -> Optional[dict]:
    """Brute-force search for modular linear recurrence of given order.

    Only practical for order <= 2 and moderate modulus.
    """
    n = len(values)
    if n < order + 5:
        return None

    if order == 1:
        # a[n] = c * a[n-1] + d mod m
        # From first two equations: solve for c, d
        for idx in range(order, n - 1):
            if values[idx - 1] == 0:
                continue
            # Try to find c from: values[idx] = c * values[idx-1] + d
            # and: values[idx+1] = c * values[idx] + d
            # Subtract: values[idx+1] - values[idx] = c * (values[idx] - values[idx-1])
            diff_b = (values[idx + 1] - values[idx]) % modulus
            diff_a = (values[idx] - values[idx - 1]) % modulus
            if diff_a == 0:
                continue
            # c = diff_b / diff_a mod m
            try:
                c = (diff_b * pow(diff_a, -1, modulus)) % modulus
            except ValueError:
                continue
            d = (values[idx] - c * values[idx - 1]) % modulus

            # Verify
            all_match = True
            for i in range(order, n):
                pred = (c * values[i - 1] + d) % modulus
                if pred != values[i]:
                    all_match = False
                    break

            if all_match:
                return {
                    "order": 1,
                    "coefficients": [int(c)],
                    "constant": int(d),
                    "modulus": modulus,
                    "confidence": min(1.0, (n - order) / 10),
                    "formula": f"a[n] = {c}*a[n-1] + {d} (mod {modulus})",
                }
        return None

    elif order == 2:
        # a[n] = c1*a[n-1] + c2*a[n-2] + d mod m
        # Try d=0 first (most common in olympiad problems)
        for d in [0]:
            # From two equations, solve for c1, c2
            for idx in range(order, n - 1):
                # values[idx] = c1*values[idx-1] + c2*values[idx-2] + d
                # values[idx+1] = c1*values[idx] + c2*values[idx-1] + d
                a11 = values[idx - 1]
                a12 = values[idx - 2]
                b1 = (values[idx] - d) % modulus
                a21 = values[idx]
                a22 = values[idx - 1]
                b2 = (values[idx + 1] - d) % modulus

                det = (a11 * a22 - a12 * a21) % modulus
                if det == 0:
                    continue
                try:
                    det_inv = pow(det, -1, modulus)
                except ValueError:
                    continue

                c1 = (det_inv * (a22 * b1 - a12 * b2)) % modulus
                c2 = (det_inv * (a11 * b2 - a21 * b1)) % modulus

                # Verify
                all_match = True
                for i in range(order, n):
                    pred = (c1 * values[i - 1] + c2 * values[i - 2] + d) % modulus
                    if pred != values[i]:
                        all_match = False
                        break

                if all_match:
                    return {
                        "order": 2,
                        "coefficients": [int(c1), int(c2)],
                        "constant": int(d),
                        "modulus": modulus,
                        "confidence": min(1.0, (n - order) / 10),
                        "formula": f"a[n] = {c1}*a[n-1] + {c2}*a[n-2] + {d} (mod {modulus})",
                    }

        return None

    return None


def detect_ratio_recurrence(values: list[int], max_degree: int = 2) -> Optional[dict]:
    """Detect recurrences of the form a[n] = R(n) * a[n-1] where R is rational.

    This catches sequences like Catalan numbers: C(n) = (4n-2)/(n+1) * C(n-1).
    """
    n = len(values)
    if n < 8:
        return None

    # Compute ratios (as fractions to avoid float issues)
    from fractions import Fraction
    ratios = []
    for i in range(1, n):
        if values[i - 1] == 0:
            return None
        ratios.append(Fraction(values[i], values[i - 1]))

    # Try to fit R(n) = (an + b) / (cn + d) to the ratios
    # ratios[i] corresponds to a[i+1]/a[i], so n = i + 1 (if start=0)
    # or more generally, the index of a[n]

    # For degree-1 rational: R(n) = (a*n + b) / (c*n + d)
    # We need at least 4 equations to solve for 4 unknowns (up to scaling)
    # R(n) * (c*n + d) = a*n + b
    # ratio[i] * (c*(i+1) + d) = a*(i+1) + b  [if values start at index 0]

    # Try: assume c=1 (normalize), then:
    # ratio[i] * ((i+1) + d) = a*(i+1) + b
    # This is linear in a, b, d

    if len(ratios) < 5:
        return None

    # Build overdetermined system for a, b, d:
    # ratio[i] * (i+1) + ratio[i] * d = a*(i+1) + b
    # => a*(i+1) + b - ratio[i]*d = ratio[i]*(i+1)
    n_eqs = min(len(ratios), 20)
    A_mat = []
    b_vec = []
    for i in range(n_eqs):
        ni = Fraction(i + 1)  # the n value for this ratio
        A_mat.append([ni, Fraction(1), -ratios[i]])
        b_vec.append(ratios[i] * ni)

    # Solve with first 3 equations, verify with rest
    if len(A_mat) >= 3:
        # Use Fraction-based elimination
        try:
            # Solve 3x3 system
            A3 = [row[:] for row in A_mat[:3]]
            b3 = b_vec[:3]

            # Gaussian elimination
            for col in range(3):
                # Find pivot
                pivot = None
                for row in range(col, 3):
                    if A3[row][col] != 0:
                        pivot = row
                        break
                if pivot is None:
                    raise ValueError("Singular")
                A3[col], A3[pivot] = A3[pivot], A3[col]
                b3[col], b3[pivot] = b3[pivot], b3[col]

                for row in range(3):
                    if row == col:
                        continue
                    factor = A3[row][col] / A3[col][col]
                    for j in range(3):
                        A3[row][j] -= factor * A3[col][j]
                    b3[row] -= factor * b3[col]

            a_coeff = b3[0] / A3[0][0]
            b_coeff = b3[1] / A3[1][1]
            d_coeff = b3[2] / A3[2][2]

            # Verify against remaining equations
            all_match = True
            for i in range(n_eqs):
                ni = Fraction(i + 1)
                expected_ratio = (a_coeff * ni + b_coeff) / (ni + d_coeff)
                if expected_ratio != ratios[i]:
                    all_match = False
                    break

            if all_match:
                return {
                    "type": "ratio_recurrence",
                    "numerator": (a_coeff, b_coeff),  # a*n + b
                    "denominator": (Fraction(1), d_coeff),  # n + d
                    "confidence": min(1.0, n_eqs / 10),
                    "formula": f"a[n] = ({a_coeff}*n + {b_coeff}) / (n + {d_coeff}) * a[n-1]",
                }
        except (ValueError, ZeroDivisionError):
            pass

    return None


def _format_recurrence(coeffs: list[int], constant: int) -> str:
    terms = []
    for i, c in enumerate(coeffs):
        if c == 0:
            continue
        if c == 1:
            terms.append(f"a[n-{i+1}]")
        elif c == -1:
            terms.append(f"-a[n-{i+1}]")
        else:
            terms.append(f"{c}*a[n-{i+1}]")

    if constant != 0:
        terms.append(str(constant))

    return "a[n] = " + " + ".join(terms) if terms else "a[n] = 0"


def explore_modular_powers(base: int, modulus: int, target_exp: int) -> DiscoveredStructure:
    """Explore b^n mod m to find periodicity and compute b^target_exp mod m."""
    values = []
    for n in range(1, min(target_exp + 1, 500)):
        values.append(pow(base, n, modulus))

    period_info = detect_periodicity(values)

    if period_info and period_info["confidence"] > 0.5:
        period = period_info["period"]
        offset = period_info["offset"]
        block = period_info["repeating_block"]

        idx = (target_exp - 1 - offset) % period
        predicted = block[idx]

        return DiscoveredStructure(
            problem_type="periodicity",
            description=f"{base}^n mod {modulus} has period {period} (starting at n={offset+1})",
            confidence=period_info["confidence"],
            predicted_answer=predicted,
            details={
                "period": period,
                "repeating_block": block,
                "verification": f"{base}^{target_exp} mod {modulus} = block[({target_exp}-1-{offset}) % {period}] = block[{idx}] = {predicted}",
            },
        )

    answer = pow(base, target_exp, modulus)
    return DiscoveredStructure(
        problem_type="direct_computation",
        description=f"Computed {base}^{target_exp} mod {modulus} directly",
        confidence=1.0,
        predicted_answer=answer,
    )


def explore_sequence(
    compute_fn: Callable[[int], int],
    target_n: int,
    start: int = 0,
    explore_up_to: int = 50,
    modulus: Optional[int] = None,
) -> DiscoveredStructure:
    """Explore a sequence defined by compute_fn(n) to discover structure.

    If modulus is provided, uses modular-aware detection (larger exploration
    window, modular recurrence detection, Pisano period for Fibonacci-like).
    """
    # Adaptive exploration window for modular sequences
    if modulus is not None:
        explore_up_to = max(explore_up_to, min(modulus * 3, 50000))

    values = []
    for n in range(start, start + explore_up_to):
        try:
            v = compute_fn(n)
            values.append(v)
        except Exception:
            break

    if len(values) < 6:
        return DiscoveredStructure(
            problem_type="insufficient_data",
            description="Could not compute enough terms",
            confidence=0.0,
        )

    # Detect if this is a modular sequence (bounded values)
    is_modular = modulus is not None
    if not is_modular:
        max_val = max(abs(v) for v in values)
        min_val = min(values)
        if min_val >= 0 and max_val < 10**6 and len(set(values)) < len(values) * 0.8:
            # Likely modular — infer modulus
            is_modular = True
            modulus = max_val + 1

    # Try periodicity first (works great for modular sequences)
    max_period = min(len(values) // 3, 10000) if is_modular else 100
    period_info = detect_periodicity(values, max_period=max_period)
    if period_info and period_info["confidence"] > 0.5:
        period = period_info["period"]
        offset = period_info["offset"]
        block = period_info["repeating_block"]
        idx = (target_n - start - offset) % period
        predicted = block[idx]

        return DiscoveredStructure(
            problem_type="periodicity",
            description=f"Sequence has period {period}",
            confidence=period_info["confidence"],
            predicted_answer=predicted,
            details={"period": period, "block_length": len(block)},
        )

    # Try modular recurrence if applicable
    if is_modular and modulus is not None:
        mod_rec = detect_modular_recurrence(values, modulus)
        if mod_rec and mod_rec["confidence"] > 0.5:
            # Extend using modular recurrence
            extended = list(values)
            order = mod_rec["order"]
            coeffs = mod_rec["coefficients"]
            constant = mod_rec["constant"]

            for i in range(len(extended), target_n - start + 1):
                val = sum(coeffs[j] * extended[i - j - 1] for j in range(order))
                val = (val + constant) % modulus
                extended.append(val)

            predicted = extended[target_n - start] if target_n - start < len(extended) else None

            return DiscoveredStructure(
                problem_type="modular_recurrence",
                description=mod_rec["formula"],
                confidence=mod_rec["confidence"],
                predicted_answer=predicted,
                details=mod_rec,
            )

    # Try standard (non-modular) recurrence
    rec_info = detect_recurrence(values)
    if rec_info and rec_info["confidence"] > 0.5:
        extended = list(values)
        order = rec_info["order"]
        coeffs = rec_info["coefficients"]
        constant = rec_info["constant"]

        for i in range(len(extended), target_n - start + 1):
            val = sum(coeffs[j] * extended[i - j - 1] for j in range(order)) + constant
            extended.append(val)

        predicted = extended[target_n - start] if target_n - start < len(extended) else None

        return DiscoveredStructure(
            problem_type="recurrence",
            description=rec_info["formula"],
            confidence=rec_info["confidence"],
            predicted_answer=predicted,
            details=rec_info,
        )

    # Try ratio recurrence (e.g., Catalan: C(n) = (4n-2)/(n+1) * C(n-1))
    ratio_info = detect_ratio_recurrence(values)
    if ratio_info and ratio_info["confidence"] > 0.5:
        from fractions import Fraction
        # Extend using ratio recurrence
        extended = [Fraction(v) for v in values]
        a_c, b_c = ratio_info["numerator"]
        c_c, d_c = ratio_info["denominator"]

        for i in range(len(extended), target_n - start + 1):
            ni = Fraction(start + i)
            ratio = (a_c * ni + b_c) / (c_c * ni + d_c)
            extended.append(extended[-1] * ratio)

        predicted_val = extended[target_n - start] if target_n - start < len(extended) else None
        if predicted_val is not None:
            if modulus is not None:
                predicted = int(predicted_val) % modulus
            else:
                predicted = int(predicted_val)
        else:
            predicted = None

        return DiscoveredStructure(
            problem_type="ratio_recurrence",
            description=ratio_info["formula"],
            confidence=ratio_info["confidence"],
            predicted_answer=predicted,
            details=ratio_info,
        )

    # Try polynomial fit (degrees 1-4)
    x = np.arange(start, start + len(values), dtype=float)
    y = np.array(values, dtype=float)

    for degree in range(1, 5):
        if len(values) < degree + 3:
            continue
        coeffs_poly = np.polyfit(x, y, degree)
        fitted = np.polyval(coeffs_poly, x)
        max_err = np.max(np.abs(fitted - y))

        if max_err < 0.5:
            predicted = int(round(np.polyval(coeffs_poly, target_n)))
            int_coeffs = [int(round(c)) for c in coeffs_poly]

            return DiscoveredStructure(
                problem_type="polynomial",
                description=f"Degree-{degree} polynomial: {int_coeffs}",
                confidence=min(1.0, len(values) / (degree * 5)),
                predicted_answer=predicted,
                details={"degree": degree, "coefficients": int_coeffs},
            )

    return DiscoveredStructure(
        problem_type="unknown",
        description="No structure detected",
        confidence=0.0,
        details={"first_values": values[:20]},
    )


def explore_problem_text(problem_text: str) -> list[DiscoveredStructure]:
    """Attempt to extract and explore mathematical structure from problem text.

    Looks for patterns like:
    - "Find X mod M" -> modular arithmetic exploration
    - Sequence/recurrence clues -> sequence exploration
    - Power/exponent patterns -> modular power exploration

    Returns a list of discovered structures (may be empty).
    """
    results = []
    text = problem_text.lower()

    # Pattern: "a^b mod m" or "remainder when a^b is divided by m"
    power_mod = re.findall(
        r'(\d+)\s*[\^]\s*[{]?(\d+)[}]?\s*(?:mod|modulo)\s*(\d+)', text
    )
    if not power_mod:
        power_mod = re.findall(
            r'remainder\s+when\s+(\d+)\s*[\^]\s*[{]?(\d+)[}]?\s*.*?divided\s+by\s+(\d+)', text
        )
    for base, exp, mod in power_mod:
        result = explore_modular_powers(int(base), int(mod), int(exp))
        results.append(result)

    # Pattern: "last N digits of a^b" -> a^b mod 10^N
    last_digits = re.findall(
        r'last\s+(\w+)\s+digits?\s+of\s+(\d+)\s*[\^]\s*[{]?(\d+)', text
    )
    word_to_num = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    for n_word, base, exp in last_digits:
        n_digits = word_to_num.get(n_word, None) or int(n_word)
        mod = 10 ** n_digits
        result = explore_modular_powers(int(base), mod, int(exp))
        results.append(result)

    # Pattern: "F(n) mod m" or "Fibonacci" with mod
    if "fibonacci" in text or "f(" in text:
        fib_mod = re.findall(r'(?:mod|modulo)\s*(\d+)', text)
        fib_n = re.findall(r'[fF]\s*\(\s*(\d+)\s*\)', text)
        if fib_mod and fib_n:
            m = int(fib_mod[0])
            n = int(fib_n[0])

            def fib_mod_fn(k, mod=m):
                if k <= 1:
                    return k
                a, b = 0, 1
                for _ in range(2, k + 1):
                    a, b = b, (a + b) % mod
                return b

            result = explore_sequence(
                compute_fn=fib_mod_fn,
                target_n=n,
                start=0,
                modulus=m,
            )
            results.append(result)

    return results


def explore_with_fuzzing(
    dim_names: list[str],
    evaluate_fn: Callable,
    target_params: dict,
) -> DiscoveredStructure:
    """Run a lightweight structural fuzzing campaign on a parameterized problem."""
    from structural_fuzzing.pipeline import run_campaign

    report = run_campaign(
        dim_names=dim_names,
        evaluate_fn=evaluate_fn,
        max_subset_dims=min(4, len(dim_names)),
        n_mri_perturbations=100,
        run_baselines=False,
        verbose=False,
    )

    summary_parts = []

    if report.sensitivity_results:
        top_dims = [s for s in report.sensitivity_results if s.delta_mae > 0.01]
        if top_dims:
            summary_parts.append(
                f"Key dimensions: {', '.join(s.dim_name for s in top_dims[:3])}")

    if report.mri_result:
        if report.mri_result.mri < 0.1:
            summary_parts.append("Solution is highly robust (broad minimum)")
        elif report.mri_result.mri > 1.0:
            summary_parts.append("Solution is fragile (sharp minimum)")

    if report.pareto_results:
        best = report.pareto_results[0]
        summary_parts.append(f"Best config: {best.dim_names} with MAE={best.mae:.4f}")

    return DiscoveredStructure(
        problem_type="fuzzing_campaign",
        description="; ".join(summary_parts),
        confidence=0.7 if report.pareto_results and report.pareto_results[0].mae < 0.1 else 0.3,
        details={
            "best_mae": report.pareto_results[0].mae if report.pareto_results else None,
            "pareto_count": len(report.pareto_results),
            "mri": report.mri_result.mri if report.mri_result else None,
            "summary": report.summary(),
        },
    )
