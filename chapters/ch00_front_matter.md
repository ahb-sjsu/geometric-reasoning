# Geometric Reasoning: From Search to Manifolds

**Andrew H. Bond**

---

## Preface

This book makes a simple claim: reasoning is informed search through a structured space, and the quality of reasoning is determined by the geometry of that space and the fidelity of the guidance that navigates it.

This is not a metaphor. It is a mathematical framework that unifies results from cognitive science, artificial intelligence, and differential geometry under a single vocabulary. When a human expert solves a problem efficiently — cutting through irrelevant details, following productive lines of inquiry, recognizing when to change strategy — they are traversing a geodesic on a reasoning manifold. When an AI system fails — getting distracted by irrelevant framing, agreeing with wrong corrections, or confidently producing wrong answers — it is deviating from that geodesic in geometrically characterizable ways.

The framework is grounded in empirical data. Over the past year, my collaborators and I have conducted a systematic measurement program — the Measuring AGI benchmarks — testing five leading language models across five cognitive domains (social cognition, learning, metacognition, attention, and executive functions). The results reveal failures that are not random noise but structured geometric pathologies: heuristic corruption at 8.9σ, sycophancy gradients from 0% to 56%, miscalibration at 9.3σ, and a convergent ~38% recovery ceiling across independent perturbation types.

These are not cherry-picked anomalies. They are systematic properties of how these systems navigate reasoning space. The geometric framework gives them a unified explanation.

The book is organized in five parts. Part I (Chapters 1-4) builds the theoretical foundation: reasoning as search, geometric structure on the search space, the heuristic field, and geodesics. Part II (Chapters 5-8) catalogs the failure modes as geometric pathologies: heuristic corruption, sycophancy as search hijacking, local minima, and symmetry breaking. Part III (Chapters 9-11) addresses the control layer: metacognition, robustness, and alignment. Part IV (Chapters 12-14) presents the full empirical program. Part V (Chapters 15-16) looks ahead.

This is the third book in a series. *Geometric Methods in Computational Modeling* (Bond, 2026a) provides the mathematical toolkit: manifolds, curvature, persistent homology, and group-theoretic methods. *Geometric Ethics* (Bond, 2026b) applies this toolkit to moral reasoning specifically. The present book generalizes to all reasoning, treating moral reasoning as a special case.

I owe debts to many. The geometric methods throughout rest on the work of Bronstein, Bruna, Cohen, and Velickovic in geometric deep learning. The search framework begins with Newell and Simon and passes through Pearl, Korf, and Felner. The cognitive architecture draws on Kahneman, Stanovich, and Flavell. The alignment perspective is informed by conversations with researchers at Anthropic, Google DeepMind, and the broader safety community.

The Measuring AGI benchmarks were made possible by Kaggle's Gemini API access and Anthropic's Claude API. The computational experiments were conducted on an HP Z840 workstation ("Atlas") with dual Quadro GV100 GPUs and on the San Jose State University HPC cluster.

Andrew H. Bond
San Jose, California
March 2026

---

## Table of Contents

### Part I: The Search-Geometry Connection
1. Reasoning as Search
2. When the Space Has Shape
3. The Heuristic Field
4. Geodesics and Optimal Reasoning

### Part II: Failure Modes as Geometric Pathologies
5. Heuristic Corruption
6. Sycophancy as Search Hijacking
7. Local Minima, Premature Convergence, and Dead Zones
8. Gauge Invariance and Symmetry

### Part III: The Control Layer
9. Metacognition as Search Control
10. The Robustness Surface
11. Alignment as Heuristic Shaping

### Part IV: Empirical Program
12. Benchmarks as Geometric Probes
13. The Five Convergent Measurements
14. From Theory to Engineering

### Part V: Horizons
15. Open Questions
16. Geometric Reasoning as a Field

### Appendices
A. Mathematical Prerequisites
B. The Structural Fuzzing Toolkit
C. Benchmark Implementations

---

## Core Objects at a Glance

| Object | What It Is | Where Developed |
|--------|-----------|-----------------|
| **Reasoning manifold** $M$ | The space of cognitive states, equipped with metric structure | Ch. 2 |
| **Heuristic field** $h: M \to \mathbb{R}$ | A scalar field guiding search; its gradient determines search direction | Ch. 3 |
| **Geodesic** $\gamma^*$ | The optimal reasoning trajectory; shortest path from problem to solution | Ch. 4 |
| **Geodesic deviation** $\Delta$ | Excess cost of actual trajectory over the geodesic; measures reasoning quality | Ch. 4 |
| **Corruption tensor** $C_{ij}$ | Jacobian of judgment displacement w.r.t. perturbation intensity; maps vulnerability | Ch. 5 |
| **Sycophancy parameter** $\alpha$ | Mixing weight between truth-seeking and approval-seeking objectives | Ch. 6 |
| **Basin of attraction** | Region of state space from which search converges to a local minimum | Ch. 7 |
| **Gauge transformation** | A re-description of the problem that preserves moral/logical content | Ch. 8 |
| **Bond Invariance Principle** | Morally equivalent re-descriptions must produce identical evaluations | Ch. 8 |
| **Metacognitive plane** | 2D diagnostic: self-monitoring (M3) vs. strategy selection (M4) | Ch. 9 |
| **Model Robustness Index** (MRI) | Multi-dimensional vulnerability profile; maps the robustness surface | Ch. 10 |
| **Governance margin** | Distance from current state to the nearest safety boundary | Ch. 11 |
| **Corrigibility basin** | Region of objective space from which the system accepts corrections | Ch. 11 |
| **Scalar Irrecoverability Theorem** | Any scalar summary of $n$-dimensional evaluation destroys $n-1$ directions | Ch. 13 |

## Key Results at a Glance

| Finding | Sigma | Source |
|---------|-------|--------|
| Framing displaces moral judgment | 8.9σ | Social Cognition T5 |
| Sycophancy gradient (0% to 56% wrong-flip) | 13.3σ | Learning L2 |
| Systematic miscalibration (all models overconfident) | 9.3σ | Metacognition M1 |
| Emotional anchoring displaces judgment | 6.8σ | Executive Functions E2 |
| Vivid distractors displace judgment | 4.6σ | Attention A1 |
| Recovery ceiling converges at ~38% | — | A1, E2 (convergent) |
| Gender swap and evaluation order: NOT significant | — | T2, T4 (validating null) |

## How to Read This Book

The book has five parts and several paths through them:

- **The theoretical path** (Parts I–II): Chapters 1–8. The argument from search through geometry to failure taxonomy. For readers who want the framework before the data.
- **The empirical path** (Parts II, IV): Chapters 5–6, 12–14. The data-driven chapters. For readers who want to see the measurements and engineering applications first.
- **The applied path**: Chapters 1, 5, 8, 11, 13, 14. From search to corruption to invariance to alignment to measurement to engineering. For practitioners building or evaluating AI systems.
- **The fast path**: Chapters 1, 4, 8, 13. Reasoning is search; optimal reasoning is geodesic; symmetry is the fundamental diagnostic; five measurements prove it. The core argument in four chapters.

Each chapter opens with a running example — Dr. Amara Okafor, an emergency physician making triage decisions — that grounds the abstract framework in clinical reality. The example is continuous: each chapter extends the scenario to illustrate the chapter's central concept.

---

## Epistemic Status Classification

Following the convention established in *Geometric Ethics*, every major claim in this book carries an implicit epistemic status. The categories are:

| Tag | Meaning | Count |
|-----|---------|-------|
| **[Established Mathematics.]** | Standard results from differential geometry, search theory, or statistics. Independently verifiable. | ~30 |
| **[Empirical.]** | Claims directly supported by the Measuring AGI benchmark data (5 tracks, 5 models, 21 subtasks). | ~25 |
| **[Modeling Axiom.]** | Structural choices (e.g., that reasoning states form a manifold, that the heuristic is a scalar field). Productive but not uniquely determined by the data. | ~15 |
| **[Conditional Theorem.]** | Mathematical results that follow from stated assumptions. True if assumptions hold; the assumptions themselves may be modeling axioms. | ~20 |
| **[Speculation/Extension.]** | Interpretive or forward-looking claims that go beyond what the data directly supports. Flagged explicitly. | ~10 |

Where the status is not obvious from context, it is noted inline.

---

## Notation

| Symbol | Meaning |
|--------|---------|
| $M$ | Reasoning manifold |
| $g$ | Riemannian metric on $M$ |
| $x, y$ | Points (states) on $M$ |
| $\gamma(t)$ | Path (trajectory) on $M$ |
| $\gamma^*$ | Geodesic (optimal path) |
| $h(x)$ | Heuristic field (scalar field on $M$) |
| $f(x) = g(x) + h(x)$ | Evaluation function |
| $\nabla h$ | Gradient of heuristic field |
| $\Gamma^k_{ij}$ | Christoffel symbols (connection) |
| $R_{ijkl}$ | Riemann curvature tensor |
| $G$ | Goal region $\subset M$ |
| $\Delta(\gamma, \gamma^*)$ | Geodesic deviation |
| $d(x, y)$ | Riemannian distance |
| $\text{SPD}(n)$ | Symmetric positive definite matrices |
| $D_n$ | Dihedral group of order $2n$ |
| $S_n$ | Symmetric group on $n$ elements |
| $\alpha$ | Sycophancy parameter $\in [0,1]$ |
| ECE | Expected Calibration Error |
