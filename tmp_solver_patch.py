"""Integration patch: structural exploration for AIMO3 solver.

This module hooks into the AIMO3 solver pipeline to add a pre-reasoning
structural exploration pass. For number theory and combinatorics problems,
it attempts to discover mathematical structure (periodicity, recurrences,
invariants) before the LLM sees the problem.

Usage:
    from solver_patch import patch_solver
    patch_solver()  # Monkey-patches solve_math_problem

Or standalone:
    python solver_patch.py "Find 2^{2024} mod 7"
"""

from __future__ import annotations

import re
import time
from typing import Optional

from src.structural_explorer import (
    DiscoveredStructure,
    explore_modular_powers,
    explore_sequence,
    explore_problem_text,
    explore_with_fuzzing,
    detect_periodicity,
    find_pisano_period,
)
from src.logger import get_logger

logger = get_logger(__name__)


def structural_pre_solve(problem_latex: str, problem_type: str = "general") -> dict:
    """Run structural exploration before LLM reasoning.

    Returns a dict with:
        - "hints": str to inject into the prompt
        - "predicted_answer": int or None
        - "confidence": float (0-1)
        - "structures": list of DiscoveredStructure
        - "elapsed": float (seconds)
    """
    t0 = time.time()
    structures: list[DiscoveredStructure] = []

    # 1. Try text-based pattern extraction
    text_structures = explore_problem_text(problem_latex)
    structures.extend(text_structures)

    # 2. For number theory problems, try additional explorations
    if problem_type in ("number_theory", "general"):
        _explore_number_theory(problem_latex, structures)

    # 3. For sequence/combinatorics, try to detect patterns in small cases
    if problem_type in ("combinatorics", "sequence", "general"):
        _explore_combinatorial(problem_latex, structures)

    elapsed = time.time() - t0

    # Pick the best prediction
    best = None
    for s in structures:
        if s.predicted_answer is not None and s.confidence > 0:
            if best is None or s.confidence > best.confidence:
                best = s

    # Format hints for prompt injection
    hint_parts = []
    for s in structures:
        if s.confidence >= 0.5:
            hint_parts.append(s.as_hint())

    result = {
        "hints": "\n".join(hint_parts),
        "predicted_answer": best.predicted_answer if best else None,
        "confidence": best.confidence if best else 0.0,
        "structures": structures,
        "elapsed": elapsed,
    }

    if best and best.predicted_answer is not None:
        logger.info(
            f"Structural exploration: predicted answer={best.predicted_answer} "
            f"(confidence={best.confidence:.0%}, type={best.problem_type}, "
            f"elapsed={elapsed:.3f}s)"
        )
    else:
        logger.info(f"Structural exploration: no prediction (elapsed={elapsed:.3f}s)")

    return result


def _explore_number_theory(problem_latex: str, structures: list[DiscoveredStructure]):
    """Additional number theory explorations."""
    text = problem_latex.lower()

    # Look for "mod" or "remainder" or "divisible" patterns
    # Extract any explicit modular arithmetic
    mod_patterns = re.findall(
        r'(\d+)\s*[\^]\s*[{]?(\d+)[}]?\s*(?:\\pmod|\\bmod|\\mod|mod)\s*[{]?(\d+)',
        problem_latex,
    )
    for base, exp, mod in mod_patterns:
        b, e, m = int(base), int(exp), int(mod)
        if b < 10**6 and m < 10**6:
            result = explore_modular_powers(b, m, e)
            structures.append(result)

    # "remainder when X divided by Y"
    remainder_patterns = re.findall(
        r'remainder.*?(\d+)\s*[\^]\s*[{]?(\d+)[}]?.*?(?:divided|div).*?(\d+)',
        text,
    )
    for base, exp, mod in remainder_patterns:
        b, e, m = int(base), int(exp), int(mod)
        if b < 10**6 and m < 10**6:
            result = explore_modular_powers(b, m, e)
            structures.append(result)

    # "last N digits" -> mod 10^N
    last_digits = re.findall(
        r'last\s+(\d+)\s+digits?\s+of\s+(\d+)\s*[\^]\s*[{]?(\d+)',
        text,
    )
    for n_digits, base, exp in last_digits:
        m = 10 ** int(n_digits)
        result = explore_modular_powers(int(base), m, int(exp))
        structures.append(result)

    # Euler's totient / Fermat's little theorem patterns
    # If we see "a^(p-1) mod p" structure, note the period
    if "fermat" in text or "euler" in text or "totient" in text:
        # Extract modulus
        mods = re.findall(r'(?:mod|modulo)\s*(\d+)', text)
        bases = re.findall(r'(\d+)\s*[\^]', problem_latex)
        if mods and bases:
            m = int(mods[0])
            b = int(bases[0])
            # Compute order of b mod m
            values = [pow(b, n, m) for n in range(1, min(m + 1, 1000))]
            period = detect_periodicity(values)
            if period:
                structures.append(DiscoveredStructure(
                    problem_type="periodicity",
                    description=f"Order of {b} mod {m} is {period['period']}",
                    confidence=period["confidence"],
                    details=period,
                ))


def _explore_combinatorial(problem_latex: str, structures: list[DiscoveredStructure]):
    """Try to detect combinatorial patterns via small-case computation."""
    text = problem_latex.lower()

    # Look for tiling / partition / counting patterns
    # These are hard to auto-detect from text, but if we see specific clues...

    # Fibonacci / Pisano detection
    if "fibonacci" in text or "f_n" in text.replace(" ", "") or "f_{n" in problem_latex:
        # Try to extract the target and modulus
        mods = re.findall(r'(?:mod|modulo|\\pmod)\s*[{]?(\d+)[}]?', problem_latex)
        indices = re.findall(r'[fF]\s*[_(]\s*[{]?(\d+)[}]?', problem_latex)

        if mods and indices:
            m = int(mods[0])
            n = int(indices[0])

            # Use Pisano period for efficient computation
            pisano = find_pisano_period(m)
            if pisano is not None:
                # F(n) mod m = F(n mod pisano) mod m
                reduced_n = n % pisano

                def fib_mod(k, mod=m):
                    if k <= 1:
                        return k
                    a, b = 0, 1
                    for _ in range(2, k + 1):
                        a, b = b, (a + b) % mod
                    return b

                answer = fib_mod(reduced_n, m)
                structures.append(DiscoveredStructure(
                    problem_type="pisano_period",
                    description=f"Pisano period pi({m}) = {pisano}; F({n}) mod {m} = F({reduced_n}) mod {m} = {answer}",
                    confidence=1.0,
                    predicted_answer=answer,
                    details={"pisano_period": pisano, "reduced_n": reduced_n},
                ))


def patch_solver():
    """Monkey-patch the AIMO3 solver to include structural exploration.

    Modifies solve_math_problem to:
    1. Run structural exploration before LLM attempts
    2. Inject discovered structure as hints into the prompt
    3. Boost voting weight for answers that match structural predictions
    """
    import src.solver as solver_module
    import src.voting as voting_module

    original_solve = solver_module.solve_math_problem
    original_weighted_vote = voting_module.weighted_majority_vote

    def patched_solve_math_problem(problem_latex: str) -> int:
        # Run structural exploration first
        from src.classification import get_classification_info
        classification_info = get_classification_info(problem_latex)
        problem_type = classification_info["type"]

        exploration = structural_pre_solve(problem_latex, problem_type)

        # If we have a high-confidence prediction from pure computation,
        # we can use it directly (no LLM needed)
        if exploration["confidence"] >= 0.95 and exploration["predicted_answer"] is not None:
            answer = exploration["predicted_answer"]
            # Validate bounds (AIMO: 0-99999)
            if 0 <= answer <= 99999:
                logger.info(
                    f"Structural exploration provided direct answer: {answer} "
                    f"(confidence={exploration['confidence']:.0%})"
                )
                return answer

        # Inject structural hints into the problem for the LLM
        if exploration["hints"]:
            # Prepend structural insights to the problem
            augmented_problem = (
                problem_latex + "\n\n"
                "## Pre-computed structural analysis (verified computationally):\n"
                + exploration["hints"]
            )
        else:
            augmented_problem = problem_latex

        # Store exploration results for voting boost (via thread-local or global)
        solver_module._structural_exploration = exploration

        # Call original solver with augmented problem
        result = original_solve(augmented_problem)

        return result

    def patched_weighted_vote(answers, metadata_list, default=0):
        """Boost weight for answers matching structural prediction."""
        exploration = getattr(solver_module, '_structural_exploration', None)

        if exploration and exploration["predicted_answer"] is not None:
            predicted = exploration["predicted_answer"]
            confidence = exploration["confidence"]

            for i, (answer, metadata) in enumerate(zip(answers, metadata_list)):
                if answer == predicted:
                    # Add structural match bonus
                    bonus = 1.0 * confidence  # Up to +1.0 weight
                    metadata["structural_match"] = True
                    metadata["structural_bonus"] = bonus
                    logger.info(
                        f"Attempt {i+1}: answer {answer} matches structural prediction "
                        f"(+{bonus:.2f} weight)"
                    )

        return original_weighted_vote(answers, metadata_list, default)

    solver_module.solve_math_problem = patched_solve_math_problem
    voting_module.weighted_majority_vote = patched_weighted_vote

    logger.info("Structural exploration patch applied to solver")


# --- Standalone testing ---

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        problem = " ".join(sys.argv[1:])
    else:
        problem = "Find the remainder when 2^{2024} is divided by 7."

    print(f"Problem: {problem}")
    print()

    result = structural_pre_solve(problem)

    if result["structures"]:
        for s in result["structures"]:
            print(s.as_hint())
            print()
    else:
        print("No structure discovered.")

    if result["predicted_answer"] is not None:
        print(f"Predicted answer: {result['predicted_answer']}")
        print(f"Confidence: {result['confidence']:.0%}")

    print(f"Elapsed: {result['elapsed']:.3f}s")
