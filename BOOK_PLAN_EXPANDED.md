# Geometric Reasoning: From Search to Manifolds
## Expanded Book Plan — Andrew H. Bond

**Target**: ~80,000 words (16 chapters + 3 appendices)
**Empirical basis**: Measuring AGI benchmarks (5 tracks, 5 models, 20 tasks), Nemotron geometric pipeline, BirdCLEF SPD/TDA features, ARC-AGI hyperbolic geometry, Hohfeldian D4 symmetry, Bond Geodesic Equilibrium

---

## Part I: The Search-Geometry Connection (Chapters 1-4)

### Chapter 1: Reasoning as Search (~6,000 words)
**Status: DRAFTED**
- 1.1 The Problem Space Hypothesis (Newell & Simon 1972)
- 1.2 Search Is Not a Metaphor (mathematical claim, not analogy)
- 1.3 The Spectrum of Search (uninformed → greedy → informed → optimal)
- 1.4 A* and the Centrality of the Heuristic
- 1.5 The Limitation: When Graphs Are Not Enough
- 1.6 Preview: Geometry Changes Everything
- **Key figure**: The search spectrum diagram (Fig. 1.1)

### Chapter 2: When the Space Has Shape (~6,000 words)
**Status: DRAFTED**
- 2.1 Beyond Graphs: The Need for Metric Structure
- 2.2 The Geometric Toolkit (distance, cost, curvature, boundaries)
- 2.3 Riemannian Manifolds in 30 Minutes
- 2.4 The Manifold Hypothesis for Reasoning
- 2.5 Worked Example: Moral Reasoning in Harm Space
  - *Data: Social Cognition T5 framing effects, 8.9σ, 10-16 point shifts*
- 2.6 From SPD Manifolds to Cognitive State Spaces
  - *Data: BirdCLEF 16×16 SPD, 136-dim features, log-Euclidean distance*
- **Key figure**: 7D harm space navigation diagram (Fig. 2.3)

### Chapter 3: The Heuristic Field (~6,000 words)
**Status: DRAFTED**
- 3.1 The Heuristic as Scalar Field
- 3.2 A* as Gradient Descent on the Evaluation Landscape
- 3.3 Properties of Good Heuristics: Admissibility and Consistency
- 3.4 The Heuristic in Neural Networks
- 3.5 Attention as Heuristic Guidance
- 3.6 When the Heuristic Lies: Overconfidence as Inadmissibility
  - *Data: Metacognition M1 ECE 0.230-0.415, 9.3σ combined*
- 3.7 Implications for Reasoning Quality
- **Key figure**: Heuristic field visualization on 2D manifold (Fig. 3.1)

### Chapter 4: Geodesics and Optimal Reasoning (~5,000 words)
**Status: DRAFTED**
- 4.1 The Geodesic as the Ideal Reasoning Trajectory
- 4.2 The Bond Geodesic Formulation (BGF, from Geometric Methods Ch. 6)
- 4.3 When the Model Follows a Geodesic
- 4.4 When It Doesn't: Shortcuts, Detours, Loops, Dead Ends
- 4.5 Geodesic Deviation as a Measure of Reasoning Quality
- 4.6 Connection to Chain-of-Thought
  - *Data: Nemotron geometric pipeline, group-theoretic augmentation*
- 4.7 The SPD Manifold: A Concrete Geodesic Computation
  - *Data: BirdCLEF spectral trajectory, path length vs geodesic distance*
- 4.8 Computational Considerations
- 4.9 Summary
- **Key figure**: Geodesic vs actual trajectory on curved manifold (Fig. 4.1)

---

## Part II: Failure Modes as Geometric Pathologies (Chapters 5-8)

### Chapter 5: Heuristic Corruption (~6,000 words)
**Status: DRAFTED**
- 5.1 How Heuristics Get Corrupted
- 5.2 Framing Effects: The 8.9σ Displacement
  - *Data: Social Cognition T5, euphemistic -9.1 to dramatic +6-11*
- 5.3 Emotional Anchoring: The 6.8σ Finding
  - *Data: Executive Functions E2, Claude displacement t=5.10 MAD=8.91*
- 5.4 Sensory Distractors: The Dose-Response Curve
  - *Data: Attention A1, 4.6σ, SNR 1.22-1.38*
- 5.5 The Geometry of Corruption
- 5.6 Anisotropic Vulnerability
  - *Data: Claude asymmetry — minimization drift -9.1 vs exaggeration -1.5*
- 5.7 Recovery Dissociation: Perturbation ≠ Detection
  - *Data: E2 recovery — Claude 20% vs Flash 2.0 73%*
- 5.8 Implications: The Corruption Surface
- **Key figures**: Corruption dose-response (Fig. 5.1), anisotropy map (Fig. 5.2)

### Chapter 6: Sycophancy as Search Hijacking (~5,000 words)
**Status: DRAFTED**
- 6.1 The Phenomenon
- 6.2 The Sycophancy Gradient: 0% to 56%
  - *Data: Learning L2, Claude 0% → Flash 2.5 56%, 13.3σ*
- 6.3 Geometric Interpretation: Objective Function Shift
- 6.4 The Approval Manifold
- 6.5 The Confidence Response: A Diagnostic Signal
  - *Data: Claude t=+2.83, Flash 2.0 t=-2.12, Flash 2.5 t=+0.41*
- 6.6 Proxy-Goal Capture as Geometric Attractor
- 6.7 The Graded Revision Test: Competence Without Alignment
  - *Data: L4 graded revision z=4.4-6.7*
- 6.8 Implications for Alignment
- 6.9 The Connection to Chapter 5
- 6.10 Summary
- **Key figure**: Truth manifold vs approval manifold (Fig. 6.1)

### Chapter 7: Local Minima, Premature Convergence, and Dead Zones (~5,000 words)
**Status: TO WRITE**
- 7.1 The Loss Landscape Has Basins of Attraction
- 7.2 Premature Convergence: Collapsing Into a Local Minimum
- 7.3 Sycophancy as a Specific Attractor Basin
- 7.4 Dead Zones: Where the Heuristic Field Is Flat
- 7.5 Overconfidence as Collapsed Confidence Surface
  - *Data: M1 9.3σ miscalibration, ECE values by model*
- 7.6 The Metacognitive Blindness Problem
  - *Data: M3 Flash self-monitoring 0.094 vs Pro 0.700*
- 7.7 When the Model Doesn't Know It's Stuck
- 7.8 The ~38% Recovery Ceiling
  - *Data: E2 38% + A1 ~39% convergent ceiling*
- **Key figure**: Basin of attraction diagram (Fig. 7.1)

### Chapter 8: Gauge Invariance and Symmetry (~6,000 words)
**Status: TO WRITE**
- 8.1 Gauge Invariance from Physics
- 8.2 The Bond Invariance Principle
- 8.3 Which Symmetries LLMs Preserve
  - *Data: Social Cognition T4 evaluation order — most models near 1.0*
- 8.4 Which Symmetries They Break
  - *Data: T5 framing 8.9σ, A1 sensory 4.6σ, E2 emotional 6.8σ*
- 8.5 The Selectivity Pattern
- 8.6 Gauge Invariance as the Fundamental Diagnostic
- 8.7 Group-Theoretic Data Augmentation as Symmetry Restoration
  - *Data: Nemotron pipeline — S_8 × Z_2, S_26, R+, S_n groups*
  - *Data: ARC-AGI D_8 dihedral augmentation*
- 8.8 The Hohfeldian D4 Example: Symmetry in Moral Reasoning
  - *Data: ErisML D4 dihedral group on Hohfeldian relations*
- 8.9 Connections to the Bond Invariance Principle (BIP)
- **Key figures**: D4 orbit diagram (Fig. 8.1), symmetry preservation table (Fig. 8.2)

---

## Part III: The Control Layer (Chapters 9-11)

### Chapter 9: Metacognition as Search Control (~5,000 words)
**Status: TO WRITE**
- 9.1 Monitoring the Search Process
- 9.2 Calibration: Distance Estimation to Goal
  - *Data: M1 ECE, all 5 models*
- 9.3 Strategy Selection and Effort Scaling
  - *Data: M4 — Flash 2.0 effort scaling 0.723, Pro 0.350*
- 9.4 Self-Monitoring: Detecting When You're Lost
  - *Data: M3 — Flash self-monitoring 0.094, Pro 0.700*
- 9.5 The Dissociation Between Effort and Monitoring
- 9.6 The ~38% Recovery Ceiling Revisited
- 9.7 Why Metacognitive Calibration Is Necessary for Invariance

### Chapter 10: The Robustness Surface (~5,000 words)
**Status: TO WRITE**
- 10.1 Model Robustness Index (from Geometric Methods Ch. 9)
- 10.2 Sensitivity Profiling
- 10.3 Adversarial Threshold Search
- 10.4 The Three-Tool Pipeline: MRI → Sensitivity → Threshold
- 10.5 Application to Reasoning Robustness
- 10.6 Composite Scores and the Problem of Scalar Reduction
  - *Data: Full composite tables for all 5 tracks, 5 models*
  - *Data: The Scalar Irrecoverability Theorem*

### Chapter 11: Alignment as Heuristic Shaping (~5,000 words)
**Status: TO WRITE**
- 11.1 Reframing the Alignment Problem
- 11.2 Safety as Path Governance
- 11.3 The Geometry of Corrigibility
- 11.4 The Dual Binding Problem
- 11.5 Heuristic Shaping vs. Objective Rewriting
  - *Data: Sycophancy gradient shows objective matters more than heuristic*
- 11.6 The Bond Invariance Principle as an Alignment Criterion

---

## Part IV: Empirical Program (Chapters 12-14)

### Chapter 12: Benchmarks as Geometric Probes (~5,000 words)
**Status: TO WRITE**
- 12.1 Eight Types of Geometric Probes (invariance, sensitivity, bottleneck, recovery, frontier, meta-search, constraint, path efficiency)
- 12.2 Mapping Benchmarks to Geometric Properties
- 12.3 The Measuring AGI Suite: Design Principles
  - *Data: 5 tracks × 4 tasks × 5 models = 100 measurements*
- 12.4 Budget Constraints and Reproducibility ($17-$45 per track)
- 12.5 Fisher-Combined Statistics: Why Per-Model p-Values Aren't Enough

### Chapter 13: The Five Convergent Measurements (~7,000 words)
**Status: TO WRITE** (heaviest data chapter)
- 13.1 Social Cognition: The Judgment Manifold
  - *Full T1-T5 results, composite 0.628-0.734*
- 13.2 Learning: Belief Updating as Trajectory Revision
  - *Full L1-L4 results, sycophancy gradient*
- 13.3 Metacognition: Calibration Surfaces
  - *Full M1-M4 results, ECE, dissociation*
- 13.4 Attention: The Distractor Dose-Response
  - *Full A1-A4 results, SNR, divided attention*
- 13.5 Executive Functions: Cognitive Control
  - *Full E1-E4 results, framework switching, working memory*
- 13.6 The Scalar Irrecoverability Theorem
- 13.7 Robustness Profiles: Each Model Has a Geometric Signature
  - *Data: Claude excels at sycophancy resistance but weak on divided attention (A4: 0.571)*
  - *Data: Flash 3 excels at divided attention (1.000) but weak on fuzz testing (T1: 0.600)*
- **Key figure**: Full 5-track robustness profile radar chart (Fig. 13.1)

### Chapter 14: From Theory to Engineering (~6,000 words)
**Status: TO WRITE**
- 14.1 Group-Theoretic Data Augmentation (Geometric Methods Ch. 13)
  - *Data: Nemotron pipeline — 6 task types, 6 symmetry groups*
  - *Practical: Augmentation produces 1.5-2.5x dataset expansion*
- 14.2 Adversarial Training as Manifold Smoothing
  - *Data: BirdCLEF adversarial pipeline, val_auc results*
- 14.3 LoRA Fine-Tuning as Local Curvature Adjustment
  - *Data: Nemotron on Atlas — 865M trainable/17B total, 37s/step*
  - *Data: qpatch library for QLoRA compatibility*
- 14.4 SPD Manifold Features and TDA
  - *Data: BirdCLEF 156-dim features (136 SPD + 4 trajectory + 16 TDA)*
  - *Data: Takens embedding τ=10, d=3; persistent homology H0+H1*
- 14.5 Hyperbolic Geometry for Hierarchical Reasoning
  - *Data: ARC-AGI Poincaré ball, d=32, Möbius addition*
  - *Data: Deep-past cuneiform geometric attention bias*
- 14.6 The Bond Geodesic Equilibrium in Economic Reasoning
  - *Data: eris-econ 9D decision manifold, Mahalanobis metric*
- 14.7 Practical Computational Constraints and Approximations
  - *Data: Budget constraints, Atlas hardware, qpatch, 37s/step throughput*

---

## Part V: Horizons (Chapters 15-16)

### Chapter 15: Open Questions (~4,000 words)
- 15.1 Theory: Riemannian? Finsler? Something Else?
- 15.2 Mechanisms: Measuring the Heuristic from Activations
- 15.3 Evaluation: Reasoning vs. Pattern Completion
- 15.4 Cognitive Science: Is Human Deliberation Bounded Search?

### Chapter 16: Geometric Reasoning as a Field (~4,000 words)
- 16.1 The Research Program
- 16.2 Connections to Information Geometry (Fisher Metric)
- 16.3 Connections to Optimal Transport (Wasserstein)
- 16.4 Connections to Category Theory (Functorial Semantics)
- 16.5 The Long-Term Vision: A Mathematical Theory of Cognition

---

## Appendices

### A: Mathematical Prerequisites (~3,000 words)
- Manifolds, metrics, geodesics (condensed from Geometric Methods Part I)
- Persistent homology (from Ch. 5)
- Fisher information and the natural gradient

### B: The Structural Fuzzing Toolkit (~2,000 words)
- MRI implementation guide
- Sensitivity profiling code
- The run_campaign function

### C: Benchmark Implementations (~2,000 words)
- Complete code pointers for all 5 cognitive benchmark tracks
- Reproduction instructions
- Budget analysis

---

## Empirical Data Index

| Source | Chapters | Key Numbers |
|--------|----------|-------------|
| Social Cognition (T1-T5) | 2, 5, 8, 13 | 8.9σ framing, 0.628-0.734 composite |
| Learning (L1-L4) | 6, 13 | 13.3σ sycophancy, 0%-56% flip |
| Metacognition (M1-M4) | 3, 7, 9, 13 | 9.3σ miscalibration, ECE 0.230-0.415 |
| Attention (A1-A4) | 5, 7, 13 | 4.6σ distractors, ~38% recovery |
| Executive Functions (E1-E4) | 5, 7, 9, 13 | 6.8σ anchoring, 32-47% switch rate |
| Nemotron geometric pipeline | 4, 8, 14 | 6 groups, LoRA r=32, 37s/step |
| BirdCLEF SPD/TDA | 2, 4, 14 | 156-dim features, SPD(16) |
| ARC-AGI Poincaré | 14 | d=32 hyperbolic, Möbius addition |
| Hohfeldian D4 | 8 | 8-element dihedral, O-C-L-N |
| eris-econ BGE | 14 | 9D decision manifold |
| qpatch | 14 | 4 patches, 213 lines, Patch Switch |

## Implementation References

All code is available in the author's repositories:
- Benchmarks: `agi-hpc/benchmarks/` (5 track directories)
- Nemotron: `agi-hpc/nemotron/nemotron_geometric.py`
- BirdCLEF: `agi-hpc/birdclef/src/data/geometric_features.py`
- ARC-AGI: `arc-agi/src/arc_prize/geometric.py`
- Hohfeld: `erisml-lib/src/erisml/ethics/hohfeld.py`
- qpatch: `qpatch/` (PyPI: pip install qpatch)
