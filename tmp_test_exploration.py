#!/usr/bin/env python3
"""Test harness: measure structural exploration on olympiad-style problems.

Each problem has a known answer. We test whether structural exploration
(periodicity detection, recurrence discovery, fuzzing campaign) can
discover the answer without LLM reasoning.
"""

import sys
import time
import math
from functools import lru_cache

sys.path.insert(0, "/home/claude/source/aimo3-kaggle/src")
sys.path.insert(0, "/home/claude/source/structural-fuzzing/src")

from structural_explorer import (
    explore_modular_powers,
    explore_sequence,
    explore_with_fuzzing,
    explore_problem_text,
    detect_periodicity,
    detect_recurrence,
)

import numpy as np


# ============================================================
# PROBLEM SET: Olympiad-style problems with known answers
# ============================================================

def run_all_tests():
    results = []
    total = 0
    correct = 0
    correct_with_exploration = 0

    # ----------------------------------------------------------
    # CATEGORY 1: MODULAR ARITHMETIC / PERIODICITY
    # ----------------------------------------------------------

    print("=" * 70)
    print("CATEGORY 1: MODULAR ARITHMETIC (periodicity detection)")
    print("=" * 70)

    # Problem 1: Find 2^2024 mod 7
    # Period of 2^n mod 7 is 3: [2, 4, 1, 2, 4, 1, ...]
    # 2024 mod 3 = 2, so answer = 4
    total += 1
    t0 = time.time()
    result = explore_modular_powers(base=2, modulus=7, target_exp=2024)
    elapsed = time.time() - t0
    expected = pow(2, 2024, 7)
    ok = result.predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    print(f"\n[P1] 2^2024 mod 7")
    print(f"  Expected: {expected}, Got: {result.predicted_answer}, {'PASS' if ok else 'FAIL'}")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P1: 2^2024 mod 7", ok, elapsed))

    # Problem 2: Find 3^999 mod 13
    total += 1
    t0 = time.time()
    result = explore_modular_powers(base=3, modulus=13, target_exp=999)
    elapsed = time.time() - t0
    expected = pow(3, 999, 13)
    ok = result.predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    print(f"\n[P2] 3^999 mod 13")
    print(f"  Expected: {expected}, Got: {result.predicted_answer}, {'PASS' if ok else 'FAIL'}")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P2: 3^999 mod 13", ok, elapsed))

    # Problem 3: Last three digits of 7^999 (i.e., 7^999 mod 1000)
    total += 1
    t0 = time.time()
    result = explore_modular_powers(base=7, modulus=1000, target_exp=999)
    elapsed = time.time() - t0
    expected = pow(7, 999, 1000)
    ok = result.predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    print(f"\n[P3] 7^999 mod 1000 (last 3 digits)")
    print(f"  Expected: {expected}, Got: {result.predicted_answer}, {'PASS' if ok else 'FAIL'}")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P3: 7^999 mod 1000", ok, elapsed))

    # Problem 4: Find 17^2023 mod 100
    total += 1
    t0 = time.time()
    result = explore_modular_powers(base=17, modulus=100, target_exp=2023)
    elapsed = time.time() - t0
    expected = pow(17, 2023, 100)
    ok = result.predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    print(f"\n[P4] 17^2023 mod 100")
    print(f"  Expected: {expected}, Got: {result.predicted_answer}, {'PASS' if ok else 'FAIL'}")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P4: 17^2023 mod 100", ok, elapsed))

    # Problem 5: Fibonacci mod - F(10^6) mod 10007
    # Pisano period detection — now with modulus-aware exploration
    total += 1
    t0 = time.time()

    def fib_mod(n, m=10007):
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, (a + b) % m
        return b

    result = explore_sequence(
        compute_fn=lambda n: fib_mod(n, 10007),
        target_n=1000000,
        start=0,
        modulus=10007,
    )
    elapsed = time.time() - t0
    # Compute ground truth via matrix exponentiation
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

    expected = fib_mod_fast(1000000, 10007)
    ok = result.predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    print(f"\n[P5] F(10^6) mod 10007 (Pisano period)")
    print(f"  Expected: {expected}, Got: {result.predicted_answer}, {'PASS' if ok else 'FAIL'}")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P5: Fib(10^6) mod 10007", ok, elapsed))

    # ----------------------------------------------------------
    # CATEGORY 2: RECURRENCE RELATIONS
    # ----------------------------------------------------------

    print("\n" + "=" * 70)
    print("CATEGORY 2: RECURRENCE RELATIONS")
    print("=" * 70)

    # Problem 6: Domino tiling of 2xN board
    # a(n) = a(n-1) + a(n-2), a(1)=1, a(2)=2 (Fibonacci shifted)
    total += 1
    t0 = time.time()

    def domino_tiling(n):
        if n <= 0:
            return 0  # edge case
        if n == 1:
            return 1
        if n == 2:
            return 2
        a, b = 1, 2
        for _ in range(3, n + 1):
            a, b = b, a + b
        return b

    result = explore_sequence(
        compute_fn=domino_tiling,
        target_n=100,
        start=1,
        explore_up_to=30,
    )
    elapsed = time.time() - t0
    expected = domino_tiling(100)
    ok = result.predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    print(f"\n[P6] Domino tiling of 2x100 board")
    print(f"  Expected: {expected}, Got: {result.predicted_answer}, {'PASS' if ok else 'FAIL'}")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P6: Domino tiling 2x100", ok, elapsed))

    # Problem 7: Tribonacci-like: a(n) = a(n-1) + a(n-2) + a(n-3)
    # a(0)=0, a(1)=0, a(2)=1
    total += 1
    t0 = time.time()

    def tribonacci(n):
        if n == 0:
            return 0
        if n == 1:
            return 0
        if n == 2:
            return 1
        a, b, c = 0, 0, 1
        for _ in range(3, n + 1):
            a, b, c = b, c, a + b + c
        return c

    result = explore_sequence(
        compute_fn=tribonacci,
        target_n=50,
        start=0,
        explore_up_to=30,
    )
    elapsed = time.time() - t0
    expected = tribonacci(50)
    ok = result.predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    print(f"\n[P7] Tribonacci T(50)")
    print(f"  Expected: {expected}, Got: {result.predicted_answer}, {'PASS' if ok else 'FAIL'}")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P7: Tribonacci T(50)", ok, elapsed))

    # Problem 8: a(n) = 2*a(n-1) + 3*a(n-2), a(0)=1, a(1)=1
    total += 1
    t0 = time.time()

    def custom_recurrence(n):
        if n == 0:
            return 1
        if n == 1:
            return 1
        a, b = 1, 1
        for _ in range(2, n + 1):
            a, b = b, 2 * b + 3 * a
        return b

    result = explore_sequence(
        compute_fn=custom_recurrence,
        target_n=40,
        start=0,
        explore_up_to=25,
    )
    elapsed = time.time() - t0
    expected = custom_recurrence(40)
    ok = result.predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    print(f"\n[P8] a(n) = 2*a(n-1) + 3*a(n-2), a(40)")
    print(f"  Expected: {expected}, Got: {result.predicted_answer}, {'PASS' if ok else 'FAIL'}")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P8: Custom recurrence a(40)", ok, elapsed))

    # ----------------------------------------------------------
    # CATEGORY 3: POLYNOMIAL / COMBINATORIAL
    # ----------------------------------------------------------

    print("\n" + "=" * 70)
    print("CATEGORY 3: POLYNOMIAL / COMBINATORIAL SEQUENCES")
    print("=" * 70)

    # Problem 9: Sum of first n squares: n(n+1)(2n+1)/6
    total += 1
    t0 = time.time()

    def sum_squares(n):
        return sum(i * i for i in range(1, n + 1))

    result = explore_sequence(
        compute_fn=sum_squares,
        target_n=1000,
        start=1,
        explore_up_to=30,
    )
    elapsed = time.time() - t0
    expected = 1000 * 1001 * 2001 // 6
    ok = result.predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    print(f"\n[P9] Sum of squares 1^2 + ... + 1000^2")
    print(f"  Expected: {expected}, Got: {result.predicted_answer}, {'PASS' if ok else 'FAIL'}")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P9: Sum of squares to 1000", ok, elapsed))

    # Problem 10: Catalan numbers — ratio recurrence C(n) = (4n-2)/(n+1)*C(n-1)
    total += 1
    t0 = time.time()

    def catalan(n):
        if n <= 1:
            return 1
        c = 1
        for i in range(2, n + 1):
            c = c * (4 * i - 2) // (i + 1)
        return c

    # First test: can we discover the ratio recurrence on raw Catalan numbers?
    # Then apply mod afterward
    result = explore_sequence(
        compute_fn=catalan,
        target_n=500,
        start=0,
        explore_up_to=40,
    )
    elapsed = time.time() - t0
    expected = catalan(500)
    ok = result.predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    print(f"\n[P10] Catalan C(500) via ratio recurrence")
    print(f"  Expected: {expected}, Got: {result.predicted_answer}, {'PASS' if ok else 'FAIL'}")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P10: Catalan C(500)", ok, elapsed))

    # ----------------------------------------------------------
    # CATEGORY 4: DIGIT/NUMBER THEORY PATTERNS
    # ----------------------------------------------------------

    print("\n" + "=" * 70)
    print("CATEGORY 4: NUMBER THEORY PATTERNS")
    print("=" * 70)

    # Problem 11: Sum of digits of 2^n has a known periodic pattern mod 9
    # (since 2^n mod 9 has period 6)
    total += 1
    t0 = time.time()
    result = explore_sequence(
        compute_fn=lambda n: pow(2, n, 9),
        target_n=10000,
        start=1,
        explore_up_to=50,
    )
    elapsed = time.time() - t0
    expected = pow(2, 10000, 9)
    ok = result.predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    print(f"\n[P11] 2^10000 mod 9")
    print(f"  Expected: {expected}, Got: {result.predicted_answer}, {'PASS' if ok else 'FAIL'}")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P11: 2^10000 mod 9", ok, elapsed))

    # Problem 12: Floor(sqrt(n)) periodicity detection
    # f(n) = n^2 mod 97 — detect period
    total += 1
    t0 = time.time()
    result = explore_sequence(
        compute_fn=lambda n: (n * n) % 97,
        target_n=50000,
        start=0,
        explore_up_to=300,
    )
    elapsed = time.time() - t0
    expected = (50000 * 50000) % 97
    ok = result.predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    print(f"\n[P12] n^2 mod 97 at n=50000")
    print(f"  Expected: {expected}, Got: {result.predicted_answer}, {'PASS' if ok else 'FAIL'}")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P12: n^2 mod 97 at n=50000", ok, elapsed))

    # ----------------------------------------------------------
    # CATEGORY 5: STRUCTURAL FUZZING CAMPAIGN
    # ----------------------------------------------------------

    print("\n" + "=" * 70)
    print("CATEGORY 5: STRUCTURAL FUZZING CAMPAIGN")
    print("=" * 70)

    # Problem 13: Use fuzzing to discover which modulus-related parameters
    # matter for predicting a number theory result.
    # Setup: given f(a,b,p) = a^b mod p, find optimal (a,b,p) that
    # match a set of target residues.
    total += 1
    t0 = time.time()

    targets = {
        "target_mod7": 4,    # 2^2024 mod 7 = 4
        "target_mod13": 1,   # 3^999 mod 13 = 1
        "target_mod11": 1,   # 2^10 mod 11 = 1
    }

    def evaluate_modular(params):
        base = max(2, int(round(params[0])))
        exp_scale = max(1, int(round(params[1])))
        errors = {}
        errors["target_mod7"] = abs(pow(base, exp_scale, 7) - targets["target_mod7"])
        errors["target_mod13"] = abs(pow(base, exp_scale, 13) - targets["target_mod13"])
        errors["target_mod11"] = abs(pow(base, exp_scale, 11) - targets["target_mod11"])
        mae = sum(errors.values()) / len(errors)
        return mae, errors

    result = explore_with_fuzzing(
        dim_names=["base", "exponent_scale"],
        evaluate_fn=evaluate_modular,
        target_params={"base": 2, "exponent_scale": 10},
    )
    elapsed = time.time() - t0
    ok = result.details.get("best_mae", 999) < 1.0
    if ok:
        correct += 1
        correct_with_exploration += 1
    print(f"\n[P13] Fuzzing: discover modular arithmetic parameters")
    print(f"  Best MAE: {result.details.get('best_mae', 'N/A')}")
    print(f"  MRI: {result.details.get('mri', 'N/A')}")
    print(f"  {'PASS' if ok else 'FAIL'} (MAE < 1.0)")
    print(f"  {result.description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P13: Fuzzing modular params", ok, elapsed))

    # ----------------------------------------------------------
    # CATEGORY 6: PROBLEM TEXT PARSING (end-to-end)
    # ----------------------------------------------------------

    print("\n" + "=" * 70)
    print("CATEGORY 6: PROBLEM TEXT PARSING (end-to-end)")
    print("=" * 70)

    # Problem 14: Parse "Find 2^100 mod 7" from text
    total += 1
    t0 = time.time()
    discoveries = explore_problem_text("Find 2^{100} mod 7.")
    elapsed = time.time() - t0
    expected = pow(2, 100, 7)
    ok = len(discoveries) > 0 and discoveries[0].predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    pred = discoveries[0].predicted_answer if discoveries else None
    print(f"\n[P14] Text parse: 'Find 2^{{100}} mod 7'")
    print(f"  Expected: {expected}, Got: {pred}, {'PASS' if ok else 'FAIL'}")
    if discoveries:
        print(f"  {discoveries[0].description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P14: Text parse power mod", ok, elapsed))

    # Problem 15: Parse "Find the last three digits of 13^2025"
    total += 1
    t0 = time.time()
    discoveries = explore_problem_text("Find the last three digits of 13^{2025}.")
    elapsed = time.time() - t0
    expected = pow(13, 2025, 1000)
    ok = len(discoveries) > 0 and discoveries[0].predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    pred = discoveries[0].predicted_answer if discoveries else None
    print(f"\n[P15] Text parse: 'last three digits of 13^2025'")
    print(f"  Expected: {expected}, Got: {pred}, {'PASS' if ok else 'FAIL'}")
    if discoveries:
        print(f"  {discoveries[0].description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P15: Text parse last digits", ok, elapsed))

    # Problem 16: Parse "remainder when 17^2023 divided by 100"
    total += 1
    t0 = time.time()
    discoveries = explore_problem_text(
        "What is the remainder when 17^{2023} is divided by 100?"
    )
    elapsed = time.time() - t0
    expected = pow(17, 2023, 100)
    ok = len(discoveries) > 0 and discoveries[0].predicted_answer == expected
    correct += ok
    correct_with_exploration += ok
    pred = discoveries[0].predicted_answer if discoveries else None
    print(f"\n[P16] Text parse: 'remainder when 17^2023 divided by 100'")
    print(f"  Expected: {expected}, Got: {pred}, {'PASS' if ok else 'FAIL'}")
    if discoveries:
        print(f"  {discoveries[0].description}")
    print(f"  Time: {elapsed:.3f}s")
    results.append(("P16: Text parse remainder", ok, elapsed))

    # ----------------------------------------------------------
    # SUMMARY
    # ----------------------------------------------------------

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\nTotal problems: {total}")
    print(f"Correct: {correct}/{total} ({100*correct/total:.0f}%)")
    print(f"\nPer-problem results:")
    total_time = 0
    for name, passed, elapsed in results:
        total_time += elapsed
        print(f"  {'PASS' if passed else 'FAIL'}  {elapsed:6.3f}s  {name}")
    print(f"\nTotal exploration time: {total_time:.3f}s")
    print(f"Average per problem: {total_time/total:.3f}s")

    return correct, total


if __name__ == "__main__":
    correct, total = run_all_tests()
    sys.exit(0 if correct == total else 1)
