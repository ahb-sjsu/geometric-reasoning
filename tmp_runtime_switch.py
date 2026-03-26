"""Runtime Switch: qpatch pattern applied to A* oracle pipeline.

Probe → Patch → Telemetry for dynamic model/compute adaptation.

Probes detect what's available:
  - GPU with free memory? → Load quantized model on GPU
  - CPU only? → llama-cpp on CPU (slower but works)
  - API key? → Use Claude API for parsing
  - Nothing? → Regex parser + A* only (no LLM, still solves computational problems)

Patches dynamically configure the pipeline.
Telemetry tracks what actually fires.

Inspired by qpatch (Bond, 2026) — the Patch Switch pattern.
"""

from __future__ import annotations

import os
import sys
import time
import json
from dataclasses import dataclass, field
from typing import Optional, Callable

sys.path.insert(0, "src")
sys.path.insert(0, "../structural-fuzzing/src")


# =============================================================================
# TELEMETRY
# =============================================================================

@dataclass
class PipelineTelemetry:
    """Track what fires during solving."""
    probes_run: dict = field(default_factory=dict)
    patches_applied: list = field(default_factory=list)
    solve_counts: dict = field(default_factory=lambda: {
        "astar_direct": 0,
        "astar_oracle_llm": 0,
        "llm_only": 0,
        "fallback": 0,
    })
    total_astar_time: float = 0.0
    total_llm_time: float = 0.0
    problems_solved: int = 0

    def summary(self) -> str:
        lines = ["Pipeline Telemetry:"]
        lines.append(f"  Problems solved: {self.problems_solved}")
        for mode, count in self.solve_counts.items():
            if count > 0:
                lines.append(f"  {mode}: {count}")
        lines.append(f"  A* time: {self.total_astar_time:.3f}s")
        lines.append(f"  LLM time: {self.total_llm_time:.3f}s")
        lines.append(f"  Probes: {self.probes_run}")
        lines.append(f"  Patches: {self.patches_applied}")
        return "\n".join(lines)

_telemetry = PipelineTelemetry()


# =============================================================================
# PROBES
# =============================================================================

def probe_gpu() -> dict:
    """Probe GPU availability and free memory."""
    result = {"available": False, "devices": [], "free_mb": 0}
    try:
        import torch
        if torch.cuda.is_available():
            result["available"] = True
            for i in range(torch.cuda.device_count()):
                free, total = torch.cuda.mem_get_info(i)
                result["devices"].append({
                    "id": i,
                    "name": torch.cuda.get_device_name(i),
                    "free_mb": free // (1024*1024),
                    "total_mb": total // (1024*1024),
                })
            result["free_mb"] = max(d["free_mb"] for d in result["devices"])
    except ImportError:
        pass
    _telemetry.probes_run["gpu"] = result["available"]
    return result


def probe_llama_cpp() -> dict:
    """Probe llama-cpp-python availability."""
    result = {"available": False, "cuda": False}
    try:
        from llama_cpp import Llama
        result["available"] = True
        # Check if CUDA-enabled
        try:
            import llama_cpp
            result["cuda"] = hasattr(llama_cpp, 'LLAMA_BACKEND_OFFLOAD')
        except Exception:
            pass
    except ImportError:
        pass
    _telemetry.probes_run["llama_cpp"] = result["available"]
    return result


def probe_transformers() -> dict:
    """Probe transformers/torch availability."""
    result = {"available": False, "version": ""}
    try:
        import transformers
        result["available"] = True
        result["version"] = transformers.__version__
    except ImportError:
        pass
    _telemetry.probes_run["transformers"] = result["available"]
    return result


def probe_api_key() -> dict:
    """Probe for API keys (Claude, OpenAI)."""
    result = {"anthropic": False, "openai": False}
    result["anthropic"] = bool(os.environ.get("ANTHROPIC_API_KEY"))
    result["openai"] = bool(os.environ.get("OPENAI_API_KEY"))
    _telemetry.probes_run["api_key"] = result["anthropic"] or result["openai"]
    return result


def probe_model_cache() -> dict:
    """Probe for locally cached model files."""
    result = {"gguf_models": [], "hf_models": []}

    # Check common locations
    model_dirs = [
        os.path.expanduser("~/.cache/huggingface/hub"),
        os.path.expanduser("~/models"),
        "/home/claude/models",
        "./models",
    ]

    for d in model_dirs:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(".gguf"):
                    result["gguf_models"].append(os.path.join(d, f))
                elif os.path.isdir(os.path.join(d, f)):
                    result["hf_models"].append(f)

    _telemetry.probes_run["model_cache"] = len(result["gguf_models"]) + len(result["hf_models"])
    return result


def probe_all() -> dict:
    """Run all probes and return combined status."""
    return {
        "gpu": probe_gpu(),
        "llama_cpp": probe_llama_cpp(),
        "transformers": probe_transformers(),
        "api_key": probe_api_key(),
        "model_cache": probe_model_cache(),
    }


# =============================================================================
# PATCHES (configure pipeline based on probes)
# =============================================================================

class PipelineConfig:
    """Dynamic pipeline configuration."""

    def __init__(self):
        self.llm_backend: Optional[str] = None  # "llama_cpp", "transformers", "api", None
        self.llm_model: Optional[str] = None
        self.llm_device: str = "cpu"
        self.parser_mode: str = "regex"  # "regex", "llm"
        self.astar_enabled: bool = True
        self.oracle_enabled: bool = True
        self.model_instance = None

    def summary(self) -> str:
        return (f"Pipeline: llm={self.llm_backend or 'none'}, "
                f"model={self.llm_model or 'none'}, device={self.llm_device}, "
                f"parser={self.parser_mode}, astar={self.astar_enabled}, "
                f"oracle={self.oracle_enabled}")


def configure_pipeline(probes: dict) -> PipelineConfig:
    """Configure pipeline based on probe results. Returns best available config."""
    config = PipelineConfig()

    gpu = probes["gpu"]
    llama = probes["llama_cpp"]
    transformers = probes["transformers"]
    api = probes["api_key"]
    cache = probes["model_cache"]

    # Strategy 1: Local GGUF model (best for offline/Kaggle)
    if llama["available"] and cache["gguf_models"]:
        config.llm_backend = "llama_cpp"
        config.llm_model = cache["gguf_models"][0]
        config.llm_device = "cuda" if (gpu["available"] and gpu["free_mb"] > 4000) else "cpu"
        _telemetry.patches_applied.append("llama_cpp_gguf")

    # Strategy 2: HuggingFace transformers model
    elif transformers["available"] and gpu["available"] and gpu["free_mb"] > 8000:
        config.llm_backend = "transformers"
        if cache["hf_models"]:
            config.llm_model = cache["hf_models"][0]
        config.llm_device = "cuda"
        _telemetry.patches_applied.append("transformers_gpu")

    # Strategy 3: API (Claude or OpenAI)
    elif api["anthropic"]:
        config.llm_backend = "api"
        config.llm_model = "claude-haiku-4-5-20251001"
        config.parser_mode = "llm"
        _telemetry.patches_applied.append("claude_api")

    elif api["openai"]:
        config.llm_backend = "api"
        config.llm_model = "gpt-4o-mini"
        config.parser_mode = "llm"
        _telemetry.patches_applied.append("openai_api")

    # Strategy 4: A* only (no LLM available)
    else:
        config.llm_backend = None
        config.parser_mode = "regex"
        _telemetry.patches_applied.append("astar_only")

    # A* oracle is always available
    config.astar_enabled = True
    config.oracle_enabled = True

    return config


# =============================================================================
# LLM BACKENDS
# =============================================================================

def load_llama_cpp_model(model_path: str, device: str = "cpu", n_ctx: int = 8192):
    """Load a GGUF model with llama-cpp-python."""
    from llama_cpp import Llama

    n_gpu_layers = -1 if device == "cuda" else 0

    model = Llama(
        model_path=model_path,
        n_ctx=n_ctx,
        n_gpu_layers=n_gpu_layers,
        verbose=False,
    )
    return model


def generate_llama_cpp(model, prompt: str, max_tokens: int = 4096, temperature: float = 0.0) -> str:
    """Generate text with llama-cpp model."""
    response = model(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        stop=["```\n\nThe", "\n\nProblem:", "---"],
    )
    return response["choices"][0]["text"]


def generate_api(prompt: str, model: str = "claude-haiku-4-5-20251001") -> str:
    """Generate text with API."""
    if "claude" in model:
        import anthropic
        client = anthropic.Anthropic()
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    else:
        import openai
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            temperature=0.0,
        )
        return response.choices[0].message.content


# =============================================================================
# UNIFIED SOLVER
# =============================================================================

def solve_with_pipeline(
    problem_text: str,
    config: PipelineConfig,
    verbose: bool = False,
) -> dict:
    """Solve a problem using the dynamically configured pipeline.

    Flow:
    1. A* pre-solve (always runs, <10ms)
    2. If A* solves it → return (MODE 1)
    3. If LLM available → run LLM with oracle hints (MODE 2/3)
    4. If no LLM → return A* partial result or None (MODE 4)
    """
    t0 = time.time()

    # Step 1: A* pre-solve
    from llm_parser import solve_parsed
    from oracle_integration import pre_solve_analysis, ORACLE_PROMPT_SECTION

    astar_t0 = time.time()
    analysis = pre_solve_analysis(problem_text)
    astar_time = time.time() - astar_t0
    _telemetry.total_astar_time += astar_time

    # MODE 1: A* direct solve
    if analysis["direct_answer"] is not None:
        _telemetry.solve_counts["astar_direct"] += 1
        _telemetry.problems_solved += 1
        return {
            "answer": analysis["direct_answer"],
            "mode": "astar_direct",
            "parsed_type": analysis["parsed_type"],
            "elapsed": time.time() - t0,
            "astar_time": astar_time,
            "llm_time": 0,
        }

    # Step 2: LLM reasoning (if available)
    if config.llm_backend is not None:
        # Build prompt with oracle instructions + hints
        prompt = f"""Solve this math problem step by step.

{ORACLE_PROMPT_SECTION}

Problem:
{problem_text}
"""
        if analysis["hints"]:
            prompt += f"\n## Pre-computed analysis:\n{analysis['hints']}\n"

        prompt += "\nSolve step by step. Use math_oracle() for any computation. Put your final integer answer in \\boxed{}.\n\nSolution:"

        llm_t0 = time.time()
        try:
            if config.llm_backend == "llama_cpp" and config.model_instance:
                response = generate_llama_cpp(config.model_instance, prompt)
            elif config.llm_backend == "api":
                response = generate_api(prompt, config.llm_model)
            else:
                response = ""

            llm_time = time.time() - llm_t0
            _telemetry.total_llm_time += llm_time

            # Extract answer from response
            import re
            boxed = re.findall(r'\\boxed\{(\d+)\}', response)
            if boxed:
                answer = int(boxed[-1])
                _telemetry.solve_counts["astar_oracle_llm"] += 1
                _telemetry.problems_solved += 1
                return {
                    "answer": answer,
                    "mode": "astar_oracle_llm",
                    "parsed_type": analysis["parsed_type"],
                    "elapsed": time.time() - t0,
                    "astar_time": astar_time,
                    "llm_time": llm_time,
                    "llm_response": response[:500],
                }

            # Try extracting last number
            numbers = re.findall(r'\b(\d+)\b', response)
            if numbers:
                answer = int(numbers[-1])
                _telemetry.solve_counts["llm_only"] += 1
                _telemetry.problems_solved += 1
                return {
                    "answer": answer,
                    "mode": "llm_only",
                    "parsed_type": analysis["parsed_type"],
                    "elapsed": time.time() - t0,
                    "astar_time": astar_time,
                    "llm_time": llm_time,
                }

        except Exception as e:
            if verbose:
                print(f"LLM error: {e}")

    # MODE 4: No LLM, A* couldn't solve directly
    _telemetry.solve_counts["fallback"] += 1
    return {
        "answer": None,
        "mode": "fallback",
        "parsed_type": analysis["parsed_type"],
        "elapsed": time.time() - t0,
        "astar_time": astar_time,
        "llm_time": 0,
        "hints": analysis["hints"],
    }


# =============================================================================
# MAIN: Probe → Configure → Solve → Report
# =============================================================================

if __name__ == "__main__":
    import math

    print("=" * 70)
    print("A* ORACLE PIPELINE with RUNTIME SWITCH (qpatch pattern)")
    print("=" * 70)

    # PROBE
    print("\n--- PROBING ENVIRONMENT ---")
    probes = probe_all()
    for name, result in probes.items():
        if isinstance(result, dict):
            status = result.get("available", result)
            print(f"  {name:15s}: {status}")

    # CONFIGURE
    print("\n--- CONFIGURING PIPELINE ---")
    config = configure_pipeline(probes)
    print(f"  {config.summary()}")

    # LOAD MODEL (if available)
    if config.llm_backend == "llama_cpp" and config.llm_model:
        print(f"\n--- LOADING MODEL: {config.llm_model} ---")
        t0 = time.time()
        config.model_instance = load_llama_cpp_model(
            config.llm_model, config.llm_device, n_ctx=4096
        )
        print(f"  Loaded in {time.time()-t0:.1f}s")

    # SOLVE
    print("\n--- SOLVING PROBLEMS ---")

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

    from astar_extended import _lucas_binomial
    d3=2025//3; d5=2025//5; d15=2025//15

    problems = [
        # Computational (A* direct)
        ("COMP-1", "Find 2025^{2025} mod 1000.", pow(2025,2025,1000)),
        ("COMP-2", "Compute \\binom{100}{3}.", 161700),
        ("COMP-3", "Find F(2025) mod 10007, where F(n) is the nth Fibonacci number.", fib_mod_fast(2025,10007)),
        ("COMP-4", "Find gcd(12345678, 87654321).", math.gcd(12345678,87654321)),
        ("COMP-5", "How many positive divisors does 2025 have?", 15),
        ("COMP-6", "Find the sum of all positive divisors of 2025.", 3751),
        ("COMP-7", "Find 7^{2025} + 13^{2025} mod 1000.", (pow(7,2025,1000)+pow(13,2025,1000))%1000),
        ("COMP-8", "How many integers between 1 and 2025 are divisible by 3 or 5?", d3+d5-d15),
        ("COMP-9", "Find the digit sum of 999999999.", 81),
        ("COMP-10", "Find the number of derangements of 7 elements.", 1854),

        # Reasoning (needs LLM — tests hybrid/fallback)
        ("AIMO3-7", "Alice and Bob are each holding some integer number of sweets. Alice says to Bob: If we each added the number of sweets we're holding to our positive integer age, my answer would be double yours. If we took the product, then my answer would be four times yours. Bob replies: Why don't you give me five of your sweets because then both our sum and product would be equal. What is the product of Alice and Bob's ages?", 50),
        ("AIME-2", "Find the sum of all positive integers n such that n+2 divides the product 3(n+3)(n^2+9).", 49),
        ("AIME-16", "Find the sum of all integer bases b > 9 for which 17_b is a divisor of 97_b.", 70),
    ]

    total = correct = 0
    for name, problem, expected in problems:
        total += 1
        result = solve_with_pipeline(problem, config)
        ok = result["answer"] == expected
        correct += ok

        if ok:
            print(f"  [PASS] {name:10s} = {result['answer']:>8}  "
                  f"[{result['mode']:18s}] ({result['elapsed']:.3f}s)")
        elif result["answer"] is not None:
            print(f"  [FAIL] {name:10s}  expected={expected} got={result['answer']}  "
                  f"[{result['mode']}]")
        else:
            print(f"  [----] {name:10s}  needs LLM (type={result['parsed_type']})")

    # REPORT
    print(f"\n{'='*70}")
    print("RESULTS & TELEMETRY")
    print(f"{'='*70}")
    print(f"  Accuracy: {correct}/{total} ({100*correct/total:.0f}%)")
    print(f"\n{_telemetry.summary()}")
    print(f"\n  Pipeline: {config.summary()}")
    print(f"{'='*70}")
