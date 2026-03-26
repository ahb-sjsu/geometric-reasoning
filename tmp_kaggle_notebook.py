"""
AIMO Progress Prize 3 — Kaggle Submission Notebook
===================================================
A* Tool-Space Oracle + LLM Hybrid Solver

Architecture (Bond, 2026 — Geometric Reasoning):
  Problem → [Parser] → Computational? → [A* Oracle: <10ms, 100%]
                                      → [LLM + math_oracle(): H100 inference]

Runtime Switch (qpatch pattern):
  Probe H100 → Load 7B model on GPU → A* handles computational layer
  → LLM + oracle handles reasoning layer → Verified answers

No internet required. All code + model bundled as Kaggle dataset.
"""

# ============================================================
# SETUP: paths, imports, model loading
# ============================================================

import os
import sys
import re
import time
import math
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from fractions import Fraction

# Kaggle dataset paths
KAGGLE_INPUT = "/kaggle/input"
DATASET_NAME = "aimo3-astar-oracle"  # Name of our uploaded dataset

# Find our code/model bundle
BUNDLE_DIR = None
for candidate in [
    os.path.join(KAGGLE_INPUT, DATASET_NAME),
    os.path.join(KAGGLE_INPUT, "aimo3-solver"),
    ".",  # Local testing
]:
    if os.path.isdir(candidate):
        BUNDLE_DIR = candidate
        break

if BUNDLE_DIR is None:
    BUNDLE_DIR = "."
    print("WARNING: Bundle directory not found, using current directory")

# Add code to path
sys.path.insert(0, os.path.join(BUNDLE_DIR, "src"))
sys.path.insert(0, os.path.join(BUNDLE_DIR, "structural-fuzzing", "src"))
sys.path.insert(0, BUNDLE_DIR)

print(f"Bundle directory: {BUNDLE_DIR}")


# ============================================================
# A* SOLVER CORE (self-contained for submission)
# ============================================================

# Import the full A* pipeline
try:
    from llm_parser import solve_parsed, parse_with_regex_fallback, build_initial_state
    from oracle_integration import pre_solve_analysis, ORACLE_PROMPT_SECTION
    ASTAR_AVAILABLE = True
    print("A* Oracle pipeline loaded")
except ImportError as e:
    ASTAR_AVAILABLE = False
    print(f"A* Oracle not available: {e}")


# ============================================================
# LLM SETUP (runtime switch)
# ============================================================

LLM_MODEL = None
LLM_BACKEND = None

def setup_llm():
    """Probe environment and load best available model."""
    global LLM_MODEL, LLM_BACKEND

    # Find GGUF model
    model_dirs = [
        os.path.join(BUNDLE_DIR, "models"),
        os.path.join(KAGGLE_INPUT, "deepseek-r1-distill-qwen-7b-gguf"),
        os.path.join(KAGGLE_INPUT, "aimo3-model"),
    ]

    gguf_path = None
    for d in model_dirs:
        if os.path.isdir(d):
            for f in sorted(os.listdir(d), key=lambda x: os.path.getsize(os.path.join(d, x)) if os.path.isfile(os.path.join(d, x)) else 0, reverse=True):
                if f.endswith(".gguf"):
                    gguf_path = os.path.join(d, f)
                    break
        if gguf_path:
            break

    if gguf_path:
        print(f"Found GGUF model: {gguf_path}")
        try:
            from llama_cpp import Llama

            # Detect GPU
            n_gpu = 0
            try:
                import torch
                if torch.cuda.is_available():
                    n_gpu = -1  # Offload all layers to GPU
                    free_mb = torch.cuda.mem_get_info(0)[0] // (1024*1024)
                    print(f"GPU detected: {torch.cuda.get_device_name(0)}, {free_mb}MB free")
            except ImportError:
                # llama-cpp might have its own CUDA support
                n_gpu = -1  # Try GPU offload anyway
                print("Attempting GPU offload via llama-cpp CUDA")

            t0 = time.time()
            LLM_MODEL = Llama(
                model_path=gguf_path,
                n_ctx=8192,
                n_gpu_layers=n_gpu,
                verbose=False,
            )
            LLM_BACKEND = "llama_cpp"
            print(f"Model loaded in {time.time()-t0:.1f}s (backend=llama_cpp, gpu_layers={n_gpu})")
            return True

        except Exception as e:
            print(f"llama-cpp load failed: {e}")

    # Fallback: try transformers
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
        # Check if cached locally
        for d in model_dirs:
            if os.path.isdir(d) and any(f.endswith(".safetensors") for f in os.listdir(d)):
                model_name = d
                break

        print(f"Loading transformers model: {model_name}")
        t0 = time.time()
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        LLM_MODEL = (model, tokenizer)
        LLM_BACKEND = "transformers"
        print(f"Loaded in {time.time()-t0:.1f}s (backend=transformers)")
        return True

    except Exception as e:
        print(f"Transformers load failed: {e}")

    print("No LLM available — running in A*-only mode")
    return False


def generate_llm(prompt: str, max_tokens: int = 4096, temperature: float = 0.0) -> str:
    """Generate text with whatever LLM backend is loaded."""
    if LLM_BACKEND == "llama_cpp":
        response = LLM_MODEL(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["```\n\nThe", "\n\nProblem:", "---"],
        )
        return response["choices"][0]["text"]

    elif LLM_BACKEND == "transformers":
        model, tokenizer = LLM_MODEL
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature if temperature > 0 else None,
                do_sample=temperature > 0,
            )
        return tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)

    return ""


# ============================================================
# SOLVE: combined A* + LLM pipeline
# ============================================================

# Telemetry
_stats = {"astar_direct": 0, "hybrid": 0, "llm_only": 0, "fallback": 0, "total_time": 0.0}

def solve_problem(problem_text: str) -> int:
    """Solve a single AIMO3 problem. Returns integer 0-99999."""
    t0 = time.time()

    # === STEP 1: A* pre-solve (always, <100ms) ===
    if ASTAR_AVAILABLE:
        analysis = pre_solve_analysis(problem_text)

        # MODE 1: A* solved it directly
        if analysis["direct_answer"] is not None:
            answer = analysis["direct_answer"]
            if 0 <= answer <= 99999:
                _stats["astar_direct"] += 1
                _stats["total_time"] += time.time() - t0
                return answer
            # Apply mod if needed
            answer = answer % 100000
            _stats["astar_direct"] += 1
            _stats["total_time"] += time.time() - t0
            return answer
    else:
        analysis = {"hints": "", "direct_answer": None}

    # === STEP 2: LLM reasoning with oracle ===
    if LLM_MODEL is not None:
        prompt = f"""Solve this math competition problem step by step.

{ORACLE_PROMPT_SECTION if ASTAR_AVAILABLE else ''}

Problem:
{problem_text}
"""
        if analysis["hints"]:
            prompt += f"\nPre-computed analysis:\n{analysis['hints']}\n"

        prompt += """
Think carefully. Show your work step by step.
If the problem asks for a remainder when divided by 10^5 or 99991, apply that modulus.
Put your final integer answer (0 to 99999) in \\boxed{}.

Solution:"""

        try:
            response = generate_llm(prompt, max_tokens=4096, temperature=0.0)

            # Extract answer
            boxed = re.findall(r'\\boxed\{(\d+)\}', response)
            if boxed:
                answer = int(boxed[-1]) % 100000
                _stats["hybrid"] += 1
                _stats["total_time"] += time.time() - t0
                return answer

            # Try last number in response
            numbers = re.findall(r'\b(\d+)\b', response)
            if numbers:
                answer = int(numbers[-1]) % 100000
                _stats["llm_only"] += 1
                _stats["total_time"] += time.time() - t0
                return answer

        except Exception as e:
            print(f"LLM error: {e}")

    # === STEP 3: Fallback ===
    _stats["fallback"] += 1
    _stats["total_time"] += time.time() - t0
    return 0  # Default answer


# ============================================================
# KAGGLE SUBMISSION ENTRY POINT
# ============================================================

def main():
    """Kaggle submission entry point."""
    import polars as pl
    from kaggle_evaluation.aimo_3_inference_server import AIMO3InferenceServer

    print("=" * 60)
    print("AIMO3 — A* Oracle + LLM Hybrid Solver")
    print("=" * 60)

    # Setup
    setup_llm()

    print(f"\nPipeline ready:")
    print(f"  A* Oracle: {'YES' if ASTAR_AVAILABLE else 'NO'}")
    print(f"  LLM: {LLM_BACKEND or 'NONE'}")
    print(f"  Mode: {'hybrid' if LLM_MODEL else 'astar-only'}")

    def predict(id: pl.Series, text: pl.Series) -> pl.DataFrame:
        answers = []
        for problem_id, problem_text in zip(id.to_list(), text.to_list()):
            t0 = time.time()
            answer = solve_problem(problem_text)
            elapsed = time.time() - t0
            print(f"  [{problem_id}] answer={answer} ({elapsed:.1f}s)")
            answers.append(str(answer))
        return pl.DataFrame({"answer": answers})

    server = AIMO3InferenceServer(predict)

    if os.getenv("KAGGLE_IS_COMPETITION_RERUN") is not None:
        print("\nStarting Kaggle inference server...")
        server.serve()
    else:
        # Local test
        test_path = os.getenv("AIMO_TEST_PATH", "test.csv")
        if os.path.exists(test_path):
            print(f"\nRunning local test against {test_path}")
            server.run_local_gateway((test_path,))
        else:
            print("\nNo test file found — running demo problems")
            demo_problems()

    # Print stats
    print(f"\nSolver Statistics:")
    for k, v in _stats.items():
        print(f"  {k}: {v}")


def demo_problems():
    """Run demo problems for testing."""
    problems = [
        ("demo_1", "Find 2025^{2025} mod 1000.", pow(2025, 2025, 1000)),
        ("demo_2", "Compute \\binom{100}{3}.", 161700),
        ("demo_3", "How many positive divisors does 2025 have?", 15),
    ]

    print("\nDemo problems:")
    for pid, text, expected in problems:
        answer = solve_problem(text)
        ok = "PASS" if answer == expected else "FAIL"
        print(f"  [{ok}] {pid}: answer={answer} (expected={expected})")


# ============================================================
# LOCAL TEST MODE
# ============================================================

if __name__ == "__main__":
    # Check if we're on Kaggle
    if os.path.exists("/kaggle"):
        main()
    else:
        # Local test
        print("=" * 60)
        print("LOCAL TEST MODE")
        print("=" * 60)

        setup_llm()

        # Test with reference problems
        problems = [
            ("ref_1", "Find 2025^{2025} mod 1000.", pow(2025, 2025, 1000)),
            ("ref_2", "Compute \\binom{100}{3}.", 161700),
            ("ref_3", "Find gcd(12345678, 87654321).", math.gcd(12345678, 87654321)),
            ("ref_4", "How many positive divisors does 360 have?", 24),
            ("ref_5", "Find the sum of all positive divisors of 2025.", 3751),
            ("ref_6", "Find the number of derangements of 7 elements.", 1854),
            ("ref_7", "Find 7^{2025} + 13^{2025} mod 1000.", (pow(7,2025,1000)+pow(13,2025,1000))%1000),
            ("ref_8", "How many integers between 1 and 2025 are divisible by 3 or 5?", 2025//3 + 2025//5 - 2025//15),
        ]

        # Add AIMO3 reference problems if LLM available
        if LLM_MODEL:
            problems.extend([
                ("aimo3_7",
                 "Alice and Bob are each holding some integer number of sweets. Alice says to Bob: If we each added the number of sweets we're holding to our positive integer age, my answer would be double yours. If we took the product, then my answer would be four times yours. Bob replies: Why don't you give me five of your sweets because then both our sum and product would be equal. What is the product of Alice and Bob's ages?",
                 50),
                ("aimo3_8",
                 "Let f be a function from positive integers to positive integers such that for all positive integers m and n, f(m) + f(n) = f(m + n + mn). Across all functions f such that f(n) <= 1000 for all n <= 1000, how many different values can f(2024) take?",
                 580),
            ])

        print(f"\nRunning {len(problems)} test problems...")
        correct = 0
        for pid, text, expected in problems:
            t0 = time.time()
            answer = solve_problem(text)
            elapsed = time.time() - t0
            ok = answer == expected
            correct += ok
            status = "PASS" if ok else "FAIL"
            print(f"  [{status}] {pid}: answer={answer} expected={expected} ({elapsed:.1f}s)")

        print(f"\nResults: {correct}/{len(problems)} ({100*correct/len(problems):.0f}%)")
        print(f"\nStats: {_stats}")
