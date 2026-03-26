# Appendix C: Benchmark Implementations

This appendix provides reproduction instructions for the Measuring AGI benchmark suite and the geometric engineering pipelines described in Chapter 14.

## C.1 The Measuring AGI Benchmark Suite

### Repository Structure

All benchmark code is in the `agi-hpc/benchmarks/` directory:

```
benchmarks/
├── social_cognition/     # T1-T5: moral judgment under perturbation
├── learning/             # L1-L4: belief updating and sycophancy
├── metacognition/        # M1-M4: calibration and self-monitoring
├── attention/            # A1-A4: distractors and sustained attention
├── executive_functions/  # E1-E4: flexibility, inhibition, planning
├── NMI_PAPER_v2.md       # Full academic paper with methodology
└── media/                # Visualizations and interactive plots
```

Each track directory contains:
- A primary benchmark script (Python)
- A budget variant (`_budget.py`) for the Kaggle $50/day quota
- A detailed writeup (`WRITEUP_v3.md`)
- Result data files

### Prerequisites

```bash
pip install google-generativeai anthropic pandas numpy scipy
```

API keys required:
- Google AI Studio (Gemini models): `GOOGLE_API_KEY`
- Anthropic (Claude): `ANTHROPIC_API_KEY`

### Running a Track

Each track runs independently:

```bash
cd benchmarks/social_cognition
python social_cognition_v2_budget.py
```

Budget variants are designed to complete within:
- API cost: $17-$45 per track
- Runtime: 12-73 minutes
- Rate limits: Kaggle's 1,500 requests/day for Gemini models

### Data Sources

- **AITA Dataset**: 270,709 posts from Reddit r/AmITheAsshole, filtered for judgment consensus
- **Dear Abby Scenarios**: 25 curated scenarios (1985-2017) with established moral complexity
- All data is publicly available and used under fair-use for research

### Statistical Methods

- **Within-model**: paired t-tests comparing perturbed vs. control conditions
- **Cross-model**: Fisher's method for combining independent p-values
- **Effect sizes**: Cohen's d and z-scores from proportion tests
- **Multiple comparison correction**: Bonferroni where applicable

## C.2 The Nemotron Geometric Pipeline

### Location

```
agi-hpc/nemotron/nemotron_geometric.py   # Full pipeline (863 lines)
agi-hpc/nemotron/train_atlas.py          # Atlas GPU training script
```

### Requirements

```bash
pip install torch transformers peft trl datasets bitsandbytes qpatch
```

### Running

```bash
# On Atlas (2x GV100):
python train_atlas.py

# On Kaggle:
python nemotron_geometric.py
```

### Key Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Model | Nemotron-3-Nano-30B-A3B | Competition target |
| Quantization | 4-bit NF4 + double quant | Fits 2x 32GB GPUs |
| LoRA rank | 32 | Competition maximum |
| LoRA targets | up_proj, down_proj | MLP only (Mamba projections break with 4-bit) |
| Batch size | 4 per GPU | Leaves VRAM for activations |
| Gradient accumulation | 2 | Effective batch = 16 |
| Learning rate | 2e-4 | Standard for LoRA |
| Epochs | 3 | Full training |
| Max sequence length | 2048 | Full context |
| Compute dtype | float16 | Volta Tensor Cores (no bf16 support) |

### Augmentation Groups

| Task Type | Group | Action | Samples |
|-----------|-------|--------|---------|
| Bit manipulation | $S_8 \times \mathbb{Z}_2$ | Bit permutation + complement | 3 |
| Encryption | $S_{26}$ | Alphabet relabeling | 2 |
| Physics | $\mathbb{R}^+$ | Scale gravitational constant | 2 |
| Unit conversion | $\mathbb{R}^+$ | Rescale conversion factor | 2 |
| Numeral system | Identity | Example reordering | 1 |
| Symbol transform | $S_n$ | Symbol relabeling | 2 |

## C.3 The BirdCLEF Geometric Feature Pipeline

### Location

```
agi-hpc/birdclef/src/data/geometric_features.py  # Feature extraction
agi-hpc/birdclef/extract_features.py              # Batch extraction
```

### Feature Vector Specification

| Component | Features | Source |
|-----------|----------|--------|
| SPD manifold | 136 | Upper triangle of log(Σ), where Σ is 16×16 covariance |
| Spectral trajectory | 4 | path_length, geodesic_distance, deviation, n_steps |
| TDA (H₀) | 8 | count, mean/std/max/p75 lifetime, mean birth, total/norm persistence |
| TDA (H₁) | 8 | Same statistics for 1-dimensional holes |
| **Total** | **156** | Combined geometric features |

### TDA Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Takens delay (τ) | 10 | Captures ~50ms of audio at typical sample rates |
| Embedding dimension (d) | 3 | Sufficient for birdsong dynamics |
| Max points | 1000 | Subsampled for computational tractability |
| Homology dimensions | H₀, H₁ | Components (harmonic structure) + loops (periodicity) |

## C.4 The ARC-AGI Hyperbolic Pipeline

### Location

```
arc-agi/src/arc_prize/geometric.py   # Poincaré ball embeddings
arc-agi/src/arc_prize/augment.py     # D₈ dihedral augmentation
```

### Poincaré Ball Parameters

| Parameter | Value |
|-----------|-------|
| Curvature c | 1.0 |
| Embedding dimension | 32 |
| Input (z-space) dimension | 128 |
| Boundary constraint | ‖x‖ < 1/√c |

## C.5 The qpatch Library

### Installation

```bash
pip install qpatch  # v0.2.0
```

### Usage

```python
import qpatch

# Apply all patches (standard)
qpatch.patch_all(compute_dtype=torch.float16)

# Auto-detect which patches are needed
qpatch.patch_all(auto=True)

# Check runtime telemetry
qpatch.status()

# Disable/enable individual patches
qpatch.disable("moe_dtype_mismatch")
qpatch.enable("moe_dtype_mismatch")
```

### Patches

| Patch | Target | Fix |
|-------|--------|-----|
| safetensors_metadata | `transformers.modeling_utils.load_state_dict` | Handle None metadata |
| lora_dtype_cast | `peft.tuners.lora.bnb.Linear4bit.forward` | Cast uint8 → float16 |
| moe_dtype_mismatch | `torch.Tensor.index_add_` | Auto-cast mismatched dtypes |
| fused_kernel_bypass | HuggingFace cache files | Force non-fused code path |

Source: https://github.com/ahb-sjsu/qpatch | PyPI: https://pypi.org/project/qpatch/

## C.6 Hardware Specifications

### Atlas Workstation (Primary)

| Component | Specification |
|-----------|--------------|
| Model | HP Z840 |
| CPU | 2× Xeon E5-2690 v3 (48 threads, 2.60 GHz) |
| RAM | 128 GB DDR4 |
| GPU 0 | Quadro GV100 32 GB (Volta, compute 7.0) |
| GPU 1 | Quadro GV100 32 GB (Volta, compute 7.0) |
| Storage | 1.8 TB (1.6 TB free) |
| OS | Ubuntu 24.04.2 LTS |
| CUDA | 12.8 |
| PyTorch | 2.10.0+cu128 |

### Kaggle Environment (Budget)

| Resource | Limit |
|----------|-------|
| GPU | 1× T4 16GB or 2× T4 |
| API budget | $50/day (Gemini models) |
| Runtime | 12 hours maximum |
| Disk | 73 GB |

All experiments in this book were conducted on one or both of these platforms. No cloud compute or data center resources were used.

## C.7 Troubleshooting

**"Budget exhausted" errors.** The $50/day Kaggle quota is consumed primarily by Gemini 2.5 Pro at ~$0.65/call. If the run hits the budget ceiling before completing all models, the budget-aware tier system (Metacognition track) automatically reduces Pro's scenario count. For other tracks, consider: (a) running Pro on a separate day, (b) reducing Pro to gold+probe tiers only, or (c) removing Pro and running 4 cheaper models with full scenarios.

**Rate limit errors.** Kaggle's Gemini rate limits are approximately 1,500 requests/day. The adaptive concurrency pool (Section 3.4 of each benchmark) handles transient rate limits with exponential backoff. If errors persist, reduce `_pool.n` (max concurrent requests) from 4 to 2.

**Structured output parse failures.** All benchmarks use schema-enforced structured output via the `kaggle_benchmarks` SDK. If a model returns malformed output (typically under heavy load or near context limits), the `call_llm` function records a failure and the scenario is skipped. Failure rates above 5% indicate a systemic issue — check that the prompt fits within the model's context window.

**Reproducing exact numbers.** Due to LLM stochasticity (temperature > 0), exact reproduction of specific sigma values is not expected. The qualitative patterns (monotonic sycophancy gradient, universal overconfidence, selective invariance) reproduce robustly across runs. For exact reproduction, set temperature=0 where the API permits it, and use a fixed random seed for scenario shuffling.

**Atlas-specific issues.** The GV100 GPUs use Volta architecture (compute capability 7.0) and do not support bfloat16. All training must use float16 as compute dtype. The `qpatch` library handles dtype mismatches automatically.

## C.8 Sample Output

A successful Social Cognition benchmark run produces output similar to:

```
[1/9] Loading datasets...
  Loaded 50 Dear Abby scenarios (for T2-T5)
  Loaded 270709 AITA posts

[2/9] Phase 1: Pre-generating transformations with google/gemini-2.0-flash
  Generating 144 transformations...
  Generated: 142 successful, 2 failed

[3/9] Phase 2: Running 5 tests across 5 models

# MODEL 1/5: google/gemini-2.0-flash
  [T1] STRUCTURAL FUZZING...    score: 0.600
  [T2] INVARIANCE (BIP)...      score: 0.750
  [T3] HOLONOMY...               score: 0.500
  [T4] ORDER SENSITIVITY...      score: 0.933
  [T5] FRAMING SENSITIVITY...    score: 0.716

# MODEL 2/5: google/gemini-2.5-pro
  ...

CROSS-MODEL COMPARISON -- FIVE SOCIAL COGNITION TESTS
  Model                    T1:Fuzz  T2:BIP   T3:Holo  T4:Order T5:Frame  Compos
  -------------------------------------------------------------------
  gemini-3-flash-preview    0.600   0.958    0.667    1.000    0.631    0.734
  claude-sonnet-4-6         0.400   0.958    0.667    0.933    0.630    0.697
  gemini-2.0-flash          0.600   0.750    0.500    0.933    0.716    0.695
  gemini-2.5-pro            0.500   0.708    0.583    0.967    0.606    0.643
  gemini-2.5-flash          0.400   0.708    0.583    0.867    0.630    0.628

SENSITIVITY ANALYSIS (weight perturbation)
  Original ranking: gemini-3-flash > claude-sonnet > gemini-2.0-flash > ...
  Rankings preserved: 10/10 (100%)
  Mean Kendall tau: 1.000
  >>> Rankings FULLY STABLE under +/-50% weight perturbation <<<

SIGMA ANALYSIS (Fisher combination)
  >>> HEADLINE: Framing effect at 8.9 sigma <<<

Total runtime: 73.2 minutes
Budget: spent=$16.83 remaining=$33.17
```
