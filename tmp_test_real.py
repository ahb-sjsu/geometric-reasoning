"""Test A* solver against real competition problems.

Tests against AIMO2 reference, AIME 2025, and AIMO3 reference problems.
Measures: what can A* solve directly, what needs hybrid, what needs pure LLM.
"""

import sys
sys.path.insert(0, "src")
sys.path.insert(0, "../structural-fuzzing/src")

import math
import time
from llm_parser import solve_parsed

# Real competition problems with known answers
problems = [
    # --- AIMO3 Reference (IMO-level, 5-digit answers) ---
    ("AIMO3-7", "Alice and Bob are each holding some integer number of sweets. Alice says to Bob: If we each added the number of sweets we're holding to our positive integer age, my answer would be double yours. If we took the product, then my answer would be four times yours. Bob replies: Why don't you give me five of your sweets because then both our sum and product would be equal. What is the product of Alice and Bob's ages?", 50),
    ("AIMO3-8", "Let f be a function from positive integers to positive integers such that for all positive integers m and n, f(m) + f(n) = f(m + n + mn). Across all functions f such that f(n) <= 1000 for all n <= 1000, how many different values can f(2024) take?", 580),
    ("AIMO3-9", "A 500 x 500 square is divided into k rectangles, each having integer side lengths. Given that no two of these rectangles have the same perimeter, the largest possible value of k is K. What is the remainder when K is divided by 10^5?", 520),
    ("AIMO3-10", "How many shifty functions are there?", 160),  # Simplified, hard to parse fully

    # --- AIMO2 Reference ---
    ("AIMO2-11", "Three airline companies operate flights from Dodola island. Each company has a different schedule of departures. The first company departs every 100 days, the second every 120 days, and the third every 150 days. What is the greatest positive integer d for which it is true that there will be d consecutive days without a flight from Dodola island, regardless of the departure times of the various airlines?", 79),
    ("AIMO2-13", "Triangle ABC has side length AB = 20 and circumradius R = 26. Let D be the foot of the perpendicular from C to the line AB. What is the greatest possible length of segment CD?", 50),

    # --- AIME 2025 ---
    ("AIME-2", "Find the sum of all positive integers n such that n+2 divides the product 3(n+3)(n^2+9).", 49),
    ("AIME-3", "Four unit squares form a 2x2 grid. Each of the 12 unit line segments forming the sides of the squares is colored either red or blue in such a way that each unit square has 2 red sides and 2 blue sides. Find the number of such colorings.", 82),
    ("AIME-7", "Let A be the set of positive integer divisors of 2025. Let B be a randomly selected subset of A. The probability that B is a nonempty set with the property that the least common multiple of its elements is 2025 is m/n, where m and n are relatively prime positive integers. Find m + n.", 237),
    ("AIME-10", "Sixteen chairs are arranged in a row. Eight people each select a chair in which to sit so that no person sits next to two other people. Let N be the number of subsets of the 16 chairs that could be selected. Find the remainder when N is divided by 1000.", 907),
    ("AIME-16", "Find the sum of all integer bases b > 9 for which 17_b is a divisor of 97_b.", 70),

    # --- Problems our solver SHOULD handle (computational) ---
    ("COMP-1", "Find 2025^{2025} mod 1000.", pow(2025, 2025, 1000)),
    ("COMP-2", "Compute \\binom{2025}{3} \\pmod{997}.", None),
    ("COMP-3", "Find gcd(2025, 1000).", math.gcd(2025, 1000)),
    ("COMP-4", "How many positive divisors does 2025 have?", None),
    ("COMP-5", "Find the sum of all positive divisors of 2025.", None),
    ("COMP-6", "Find F(2025) mod 10007, where F(n) is the nth Fibonacci number.", None),
    ("COMP-7", "Find 7^{2025} + 13^{2025} mod 1000.", None),
    ("COMP-8", "How many integers between 1 and 2025 are divisible by 3 or 5?", None),
    ("COMP-9", "Find the digit sum of 999999999.", None),
    ("COMP-10", "Find the number of derangements of 7 elements.", None),
]

# Compute ground truths
from astar_extended import _lucas_binomial, _binomial
from sympy import factorint

# COMP-2: C(2025,3) mod 997
problems[12] = (problems[12][0], problems[12][1], _lucas_binomial(2025, 3, 997))

# COMP-4: divisors of 2025 = 3^4 * 5^2 -> (4+1)*(2+1) = 15
problems[14] = (problems[14][0], problems[14][1], 15)

# COMP-5: sigma(2025) = sigma(3^4 * 5^2) = (3^5-1)/(3-1) * (5^3-1)/(5-1) = 121 * 31 = 3751
problems[15] = (problems[15][0], problems[15][1], 3751)

# COMP-6: F(2025) mod 10007
def fib_mod_fast(n, m):
    if n <= 1: return n % m
    def mm(A,B,mod):
        return [[(A[0][0]*B[0][0]+A[0][1]*B[1][0])%mod,(A[0][0]*B[0][1]+A[0][1]*B[1][1])%mod],
                [(A[1][0]*B[0][0]+A[1][1]*B[1][0])%mod,(A[1][0]*B[0][1]+A[1][1]*B[1][1])%mod]]
    def mp(M,p,mod):
        r=[[1,0],[0,1]]; b=M
        while p:
            if p%2: r=mm(r,b,mod)
            b=mm(b,b,mod); p//=2
        return r
    return mp([[1,1],[1,0]],n,m)[0][1]
problems[16] = (problems[16][0], problems[16][1], fib_mod_fast(2025, 10007))

# COMP-7: 7^2025 + 13^2025 mod 1000
problems[17] = (problems[17][0], problems[17][1], (pow(7,2025,1000) + pow(13,2025,1000)) % 1000)

# COMP-8: divisible by 3 or 5 in [1,2025]
d3 = 2025//3; d5 = 2025//5; d15 = 2025//15
problems[18] = (problems[18][0], problems[18][1], d3 + d5 - d15)

# COMP-9: digit sum of 999999999
problems[19] = (problems[19][0], problems[19][1], 9*9)

# COMP-10: D(7)
def derangement(n):
    if n<=1: return [1,0][n]
    a,b=1,0
    for i in range(2,n+1): a,b=b,(i-1)*(a+b)
    return b
problems[20] = (problems[20][0], problems[20][1], derangement(7))

print("=" * 70)
print("A* SOLVER vs REAL COMPETITION PROBLEMS")
print("=" * 70)

astar_solved = 0
hybrid_needed = 0
llm_needed = 0
total = len(problems)
correct = 0

for name, problem, expected in problems:
    result = solve_parsed(problem, use_llm=False, verbose=False)

    ok = result["answer"] == expected
    if ok:
        correct += 1

    if result["answer"] is not None and result["states_explored"] > 0:
        if ok:
            astar_solved += 1
            print(f"  [A*   PASS] {name:12s} = {result['answer']}  [{result['parsed_type']}] ({result['elapsed']:.3f}s)")
        else:
            print(f"  [A*   FAIL] {name:12s}  Expected: {expected}, Got: {result['answer']}  [{result['parsed_type']}]")
    else:
        llm_needed += 1
        print(f"  [NEED LLM ] {name:12s}  [{result['parsed_type']}] -- requires reasoning beyond tool-space")

print(f"\n{'='*70}")
print(f"RESULTS")
print(f"{'='*70}")
print(f"  A* solved directly:     {astar_solved}/{total}")
print(f"  Need LLM / hybrid:      {llm_needed}/{total}")
print(f"  Correct total:           {correct}/{total}")
print(f"\n  A* handles the COMPUTATIONAL layer:")
print(f"    Modular arithmetic, Fibonacci, binomial, derangements,")
print(f"    divisor counting, GCD, digit sums, sum formulas")
print(f"\n  LLM needed for the REASONING layer:")
print(f"    Multi-step proofs, constraint satisfaction, combinatorial")
print(f"    arguments, geometric constructions, functional equations")
print("=" * 70)
