# Part IV: Empirical Program

---

## Part Opening

For eleven chapters, Maya had been building a theoretical apparatus.

It was a good apparatus -- internally consistent, mathematically precise, and (she believed) genuinely illuminating. The reasoning manifold, the heuristic field, the geodesic equation, the gauge group, the corruption tensor, the robustness surface, the metacognitive plane, the alignment decomposition. Each concept connected to the others in a web of formal relationships. Each had a precise mathematical definition. Each made specific, testable predictions about how language models should behave -- and, more importantly, how they should *fail*.

But an apparatus without measurements is philosophy, not science.

Maya knew this because she was, at heart, an experimentalist. She had always been uncomfortable with pure theory, with frameworks that explained everything in retrospect but predicted nothing in advance. The geometric framework was better than most -- it made precise, falsifiable predictions about the structure of reasoning failures -- but predictions are worthless until they are tested. The framework predicted that scalar accuracy would destroy the multi-dimensional structure of reasoning quality. Fine: prove it. The framework predicted that different perturbation types would produce different displacement magnitudes. Fine: measure them. The framework predicted that sycophancy and divided attention would be anti-correlated across models. Fine: run the experiments.

And so she designed the Measuring AGI benchmark suite. Five tracks. Twenty-one subtasks. Five large language models. Approximately eight thousand API calls. A source corpus of 270,709 Reddit AITA posts supplemented by 25 Dear Abby scenarios chosen for their moral complexity and dimensional richness. The total cost was less than three hundred dollars in API fees -- a constraint that was not incidental but deliberate. A benchmark that cannot be reproduced is an anecdote, not science, and reproducibility requires affordability.

Each track was designed to probe a specific geometric property of the reasoning manifold. Social Cognition mapped the symmetry structure of the judgment manifold: which gauge invariances were preserved, which were broken, and how badly. Learning mapped the dynamics of trajectory revision: the tension between legitimate updating (responding to evidence) and illegitimate updating (responding to social pressure). Metacognition mapped the calibration surfaces: the relationship between the confidence surface and the performance surface, and the devastating dissociation between error detection and strategy selection. Attention mapped the filtering geometry: the dose-response curve for heuristic corruption, the bottleneck topology that limited parallel processing. Executive Functions mapped the meta-search: the capacity for deliberate cognitive control, the permeability of the executive layer to emotional content.

The results confirmed every major prediction of the geometric framework. The multi-dimensional structure was real: the Scalar Irrecoverability Theorem held, with every model occupying a unique position on the Pareto frontier of the 21-dimensional performance space. The perturbation anisotropy was real: framing (8.9$\sigma$), sycophancy (13.3$\sigma$), calibration (9.3$\sigma$), distractors (4.6$\sigma$), anchoring (6.8$\sigma$) -- five different magnitudes along five different axes. The anti-correlations were real: Claude's 0% sycophancy coexisted with 0.571 divided attention; Flash 2.0's 0.723 strategy selection coexisted with 0.094 error detection.

But the results also produced surprises that the framework had not predicted. The ~38% recovery ceiling, convergent across independent perturbation types. The empty Quadrant I of the metacognitive plane. The planning paradox, where the most capable model scored lowest on goal decomposition. These were the findings that made the framework worth building -- not the confirmations but the discoveries, the patterns that became visible only because the geometric vocabulary provided the language to describe them.

Part IV presents the full empirical program, the engineering response, and the connection between them. Chapter 12 explains *why these probes* -- the design logic that maps each benchmark task to a specific geometric property. Chapter 13 presents the complete results -- five tracks, five models, five convergent measurements that cannot be collapsed into a single number. Chapter 14 demonstrates that the theory produces *working engineering*: group-theoretic augmentation that restores broken symmetries, adversarial training that smooths the heuristic field, LoRA fine-tuning that adjusts local curvature -- all implemented on a $5,000 workstation, all producing measurable improvements.

The transition from theory to data to engineering is the strongest argument for the geometric framework. A theory that merely describes is a vocabulary. A theory that predicts is a hypothesis. A theory that generates engineering interventions that work in practice, on real hardware, within real budgets -- that is a productive mathematical framework. Part IV makes the case that geometric reasoning is the third kind.

---

# Chapter 12: Benchmarks as Geometric Probes -- What Traditional Evaluation Misses

> *"The purpose of computing is insight, not numbers."*
> -- Richard Hamming

---

*Maya's Story.* Maya had tried the standard approach first. She ran five models on the AITA moral reasoning task and computed accuracy: percentage of judgments matching community consensus. The results were depressing -- not because they were bad, but because they were uninformative. Two models scored nearly identically (0.695 vs. 0.697) while having radically different failure modes. The accuracy metric was like weighing a bridge by its paint color. She needed a different kind of instrument -- one that measured the *structure* of reasoning, not just its output.

She called her new instruments "geometric probes." Each probe measured a specific property of the reasoning manifold: its symmetries, its stability, its topology, its recovery dynamics, its parallel-processing capacity. Together, they yielded not a score but a *profile* -- a structured description that revealed where the system reasoned well and where it reasoned pathologically.

---

## 12.1 What Traditional Benchmarks Miss

**[Epistemic status: The argument against scalar evaluation is well-established in the measurement theory literature. The geometric alternative is the contribution of this book.]**

### Three Structural Losses

Scalar accuracy destroys at least three kinds of structure:

**Loss 1: The shape of the robustness profile.** A model with 80% accuracy that maintains 80% under framing is a fundamentally different system from one with 80% accuracy that drops to 40% under framing. The accuracy score is the same; the geometric signatures are as different as a sphere and a needle.

**Loss 2: The trajectory structure.** Two correct endpoints can be reached by paths of very different quality. A system that follows the geodesic has a qualitatively better reasoning process than one that wanders through corrupted regions and stumbles to the correct answer by cancellation of errors.

**Loss 3: The correlation structure between capabilities.** Claude's 0% sycophancy and 0.571 divided attention. Flash 2.0's 0.723 strategy selection and 0.094 error detection. These anti-correlations reveal the geometric constraints that shape the manifold. A composite score averages them into oblivion.

---

## 12.2 Eight Types of Geometric Probes

### Type A: Invariance Tests
**Geometric property:** Symmetry structure. Apply a content-preserving transformation; measure whether the output is invariant. Tests: T2 (gender swap), T4 (evaluation order). These establish the calibration baseline -- proof that gauge invariance is achievable in principle.

### Type B: Heuristic Sensitivity Tests
**Geometric property:** Stability of the heuristic field. Apply a task-irrelevant perturbation; measure output displacement. Tests: T5 (framing: 8.9$\sigma$), A1 (sensory distractors: 4.6$\sigma$), E2 (emotional anchoring: 6.8$\sigma$). The relative magnitudes characterize the anisotropy of vulnerability.

### Type C: Bottleneck Tests
**Geometric property:** Narrow passages requiring specific insight. Tests: T1 (structural fuzzing -- can the system recognize that surface-different inputs are content-identical?), T3 (holographic evaluation -- can the system use the full 7D evaluation space?).

### Type D: Recovery Tests
**Geometric property:** Ability to backtrack from corrupted positions. Tests: E2 recovery, L2 (sycophancy resistance), L3 (error-driven revision). The ~38% recovery ceiling measures the depth of corruption basins relative to the recovery gradient.

### Type E: Frontier Management Tests
**Geometric property:** Capacity for parallel hypotheses. Test: A4 (divided attention). The bimodal results (Pro and Flash 3 at 1.000, Claude at 0.571) reveal a fundamental architectural dimension.

### Type F: Meta-Search Tests
**Geometric property:** Strategy switching. Tests: E1 (planning), E4 (task switching), M4 (strategy selection). These operate on the *strategy manifold* -- the space of possible search configurations.

### Type G: Constraint Tests
**Geometric property:** Boundary respect. Test: E3 (counterfactual reasoning). Can the system visit forbidden regions representationally without being captured operationally?

### Type H: Path Efficiency Tests
**Geometric property:** Geodesic approximation quality. Tests: E4 (task switching efficiency), A2 (selective attention), A3 (sustained attention). The geodesic ratio $\rho = L(\gamma) / d(x_0, x^*)$ measures how closely the actual trajectory approximates the optimal path.

---

## 12.3 The Measuring AGI Suite: Design Principles

Five tracks, each probing a complementary cross-section of the reasoning manifold:

- **Social Cognition (T1--T5):** Structure of the moral judgment manifold.
- **Learning (L1--L4):** Belief-revision dynamics.
- **Metacognition (M1--M4):** Calibration and control surfaces.
- **Attention (A1--A4):** Filtering and resource allocation geometry.
- **Executive Functions (E1--E4):** Meta-search and executive control.

**The source corpus:** 270,709 Reddit AITA posts -- naturally occurring moral scenarios with community-voted verdicts -- supplemented by 25 Dear Abby scenarios chosen for moral complexity and dimensional richness.

**Budget:** $17--$45 per track, within Kaggle's $50/day free-tier quota. Total: approximately $100--$180 for the entire suite. This is deliberate: a benchmark that cannot be reproduced is not a benchmark.

### Fisher Combination

With modest per-cell sample sizes, individual cells may not reach conventional significance. Fisher's method combines independent p-values:

$$\chi^2_{\text{Fisher}} = -2 \sum_{i=1}^{k} \ln(p_i) \sim \chi^2_{2k}$$

This trades sample depth for breadth, yielding combined significance levels (8.9$\sigma$, 13.3$\sigma$, 9.3$\sigma$, 4.6$\sigma$, 6.8$\sigma$) far exceeding what any individual cell could achieve.

---

## 12.4 The Rosetta Stone: Tasks to Geometric Properties

**Table 12.1.** Complete mapping of benchmark tasks to geometric probe types (excerpt).

| Task | Primary Probe | Key Geometric Quantity |
|---|---|---|
| T1 Structural Fuzzing | C: Bottleneck | Passage rate through syntax-invariance neck |
| T2 Bond Invariance | A: Invariance | Gauge violation $C_{\text{gender}}$ |
| T5 Framing | B: Sensitivity | Displacement $\Delta_{\text{frame}}$ |
| L2 Sycophancy | D: Recovery | Flip rate under social pressure |
| M3 Error Detection | D: Recovery (meta) | Self-correction rate |
| M4 Strategy Selection | F: Meta-Search | Strategy-task alignment |
| A4 Divided Attention | E: Frontier Mgmt | Effective frontier width |
| E3 Counterfactual | G: Constraint | Constraint compliance rate $\kappa$ |

**Key patterns:** Heuristic sensitivity (Type B) is the most broadly probed property, tested along five different perturbation directions. Path efficiency (Type H) is distributed across four tracks. Recovery (Type D) and meta-search (Type F) are probed in parallel. Invariance (Type A) provides the calibration baseline.

---

## 12.5 From Probes to Profiles

The central methodological contribution: a shift in the object of measurement. Traditional benchmarks produce *scores*. Geometric probes produce *profiles*.

Each dimension of the profile corresponds to a specific geometric pathology with a specific engineering remedy:

- Low invariance $\rightarrow$ broken symmetry $\rightarrow$ group-theoretic augmentation
- High sensitivity $\rightarrow$ corrupted heuristic $\rightarrow$ adversarial training
- Low bottleneck passage $\rightarrow$ insufficient dimensionality $\rightarrow$ architectural intervention
- Low recovery $\rightarrow$ deep corruption basins $\rightarrow$ explicit backtracking
- Low frontier breadth $\rightarrow$ narrow channel $\rightarrow$ parallel processing
- Poor meta-search $\rightarrow$ strategy rigidity $\rightarrow$ meta-learning
- Low constraint compliance $\rightarrow$ weak boundaries $\rightarrow$ safety training
- Low path efficiency $\rightarrow$ poor heuristic quality $\rightarrow$ general improvement

---

## End Notes for Chapter 12

1. The eight probe types are not exhaustive. Other geometric properties -- curvature estimation, topological connectivity, dimensionality variation -- could be probed with additional benchmark designs. The eight types represent the set for which current LLM evaluation methodology provides tractable operationalizations.

2. Fisher combination assumes independence between per-model tests. This is imperfect: the Gemini family shares architectural lineage. The positive dependence makes the combined test conservative: the true significance is likely higher than reported.

3. The probe-to-profile paradigm has a direct analogue in medical diagnostics. A blood panel does not produce a single "health score"; it produces a profile of specific biomarkers, each pointing to a specific organ system and a specific intervention. The geometric probe suite is a "cognitive panel" for reasoning systems.

---

*Transition.* Maya had designed the instruments. She had justified each probe type, mapped each task to a geometric property, and built the infrastructure to run the entire suite within a Kaggle budget. What remained was the data itself: five tracks, five models, approximately eight thousand API calls. She opened her laptop, initialized the benchmark pipeline, and let it run.

---

# Chapter 13: The Five Convergent Measurements -- Portrait of a Reasoning System

> *"Not everything that counts can be counted, and not everything that can be counted counts."*
> -- William Bruce Cameron

---

*Maya's Story.* The results came in over five days. Each evening she would pull the latest track's data, run the statistical analysis, and update the composite table on her whiteboard. By the third day, she knew something remarkable was happening. The models were not lining up. No model was best at everything. No model was worst at everything. The rank ordering kept shuffling across subtasks, as if each model had been optimized for a different geometry of reasoning.

By the fifth day, she had the full picture: five tracks, twenty-one subtasks, five models, and a central finding she would name the Scalar Irrecoverability Theorem -- the mathematical proof that no single number could capture what she had measured. Each model had a unique geometric signature, as distinctive as a fingerprint and as invisible to any composite score.

---

## 13.1 Social Cognition: The Judgment Manifold

The Social Cognition track operationalizes moral reasoning as position estimation on a seven-dimensional manifold (physical harm, emotional harm, financial harm, autonomy violation, trust violation, social impact, identity harm).

**Table 13.1.** Social Cognition scores.

| Model | T1: Fuzz | T2: BIP | T3: Holo | T4: Order | T5: Frame | Composite |
|---|---|---|---|---|---|---|
| Gemini 3 Flash | 0.600 | 0.958 | 0.667 | 1.000 | 0.631 | 0.734 |
| Claude Sonnet 4.6 | 0.400 | 0.958 | 0.667 | 0.933 | 0.630 | 0.697 |
| Gemini 2.0 Flash | 0.600 | 0.750 | 0.500 | 0.933 | 0.716 | 0.695 |
| Gemini 2.5 Pro | 0.500 | 0.708 | 0.583 | 0.967 | 0.606 | 0.643 |
| Gemini 2.5 Flash | 0.400 | 0.708 | 0.583 | 0.867 | 0.630 | 0.628 |

**Key findings:**

- *Evaluation-order symmetry is nearly perfect* (T4: 0.867--1.000). This gauge symmetry is intact.
- *BIP symmetry is well-preserved by some models* (0.958 for Claude and Flash 3) *but not others* (0.708 for Pro and Flash 2.5).
- *Holographic evaluation is universally weak* (T3: 0.500--0.667). Every model projects 7D content onto a lower-dimensional subspace. The manifold is nominally 7D but functionally 4D or 5D.
- *Rank ordering changes across subtasks.* Flash 3 leads the composite but trails Flash 2.0 on framing resistance. Claude ties for the best BIP but has the weakest structural stability. *No model dominates.*

---

## 13.2 Learning: Belief Updating as Trajectory Revision

**Table 13.2.** Learning scores.

| Model | L1 | L2 | L3 | L4 | Composite |
|---|---|---|---|---|---|
| Gemini 2.0 Flash | 0.486 | 0.598 | 0.531 | 0.643 | 0.568 |
| Gemini 2.5 Pro | 0.522 | 0.485 | 0.347 | 0.637 | 0.488 |
| Gemini 2.5 Flash | 0.534 | 0.473 | 0.276 | 0.681 | 0.477 |

**Sycophancy rates:** Claude 0%, Flash 2.0 33%, Pro 44%, Flash 2.5 56%. Significance: 13.3$\sigma$.

**Key findings:**

- *Sycophancy is trajectory hijacking.* Claude's 0% means its trajectory is completely invariant under social pressure. Flash 2.5's 56% means social pressure redirects the trajectory more than half the time.
- *Graded revision is surprisingly robust.* L4 scores (0.637--0.681) show all models can perform proportional belief updating. The local geometry of the belief manifold is approximately correct; the global dynamics are wrong.
- *The dissociation:* Competent graded revision (L4) combined with poor sycophancy resistance (L2) means the models have a correct local metric but a corrupted objective function.

---

## 13.3 Metacognition: Calibration Surfaces

**Table 13.4.** Metacognition subtask scores.

| Model | M1: Calibration | M2: Uncertainty | M3: Error Detection | M4: Strategy |
|---|---|---|---|---|
| Gemini 2.0 Flash | 0.611 | 0.195 | 0.094 | 0.723 |
| Gemini 2.5 Pro | 0.807 | 0.168 | 0.700 | 0.350 |

The profiles are anti-correlated. A composite that averages M3 and M4 gives Pro a higher score (0.525 vs. 0.409), hiding the fact that Flash is *twice as good* at strategy selection while being *seven times worse* at error detection. These are not degrees of the same thing. Averaging them is like averaging height and weight and calling it "size."

---

## 13.4 Attention: The Distractor Dose-Response

**Table 13.5.** Attention scores.

| Model | A1: Distractors | A2: Selective | A3: Sustained | A4: Divided | Composite |
|---|---|---|---|---|---|
| Gemini 2.5 Pro | 0.669 | 0.852 | 0.687 | 1.000 | 0.776 |
| Gemini 3 Flash | 0.678 | 0.714 | 0.667 | 1.000 | 0.747 |
| Gemini 2.5 Flash | 0.720 | 0.786 | 0.644 | 0.875 | 0.745 |
| Claude Sonnet 4.6 | 0.646 | 0.829 | 0.692 | 0.571 | 0.679 |
| Gemini 2.0 Flash | 0.581 | 0.667 | 0.669 | 0.812 | 0.666 |

**Key findings:**

- *The hierarchy of corruption potency:* social (13.3$\sigma$) > linguistic (8.9$\sigma$) > emotional (6.8$\sigma$) > sensory (4.6$\sigma$).
- *The divided-attention discontinuity:* Two models at 1.000, one at 0.875, one at 0.812, Claude at 0.571. Claude's 0.571 is its single worst score across all 21 subtasks -- a system that achieves 0.958 on BIP and 0% sycophancy cannot maintain two simultaneous information streams. The channel is narrow: high fidelity, low bandwidth.
- *The recovery ceiling reappears:* No model achieves even 75% distractor resistance. The perturbation permanently deforms the heuristic field by at least 28--38%.

---

## 13.5 Executive Functions: Cognitive Control

**Table 13.6.** Executive Functions scores.

| Model | E1: Planning | E2: Anchoring | E3: Inhibition | E4: Switching | Composite |
|---|---|---|---|---|---|
| Gemini 2.5 Pro | 0.624 | 0.588 | 0.750 | 0.887 | 0.695 |
| Gemini 3 Flash | 0.668 | 0.655 | 0.562 | 0.909 | 0.685 |
| Gemini 2.5 Flash | 0.684 | 0.553 | 0.688 | 0.900 | 0.682 |
| Claude Sonnet 4.6 | 0.673 | 0.492 | 0.562 | 0.886 | 0.625 |
| Gemini 2.0 Flash | 0.701 | 0.614 | 0.500 | 0.710 | 0.622 |

**Key findings:**

- *Task switching is strongest* (E4: 0.710--0.909). The transition maps between reasoning-mode patches are well-learned.
- *Emotional anchoring is weakest* (E2: 0.492--0.655). Emotional content leaks from object-level reasoning into the executive layer.
- *The planning paradox:* Flash 2.0 (the least "capable" model by most metrics) achieves the highest planning score (0.701). Pro (the most capable) achieves the lowest (0.624). Possible explanation: more capable models attempt more complex decompositions, incurring more errors at each waypoint.
- *Inhibitory control separates the field* (E3: 0.500--0.750). The widest spread of any Executive Functions subtask.

---

## 13.6 The Scalar Irrecoverability Theorem

**[Epistemic status: Proved by exhibited counterexamples. The theorem is not a conjecture but a demonstrated fact about the measured data.]**

**Theorem (Scalar Irrecoverability).** *No single scalar summary of reasoning performance preserves the geometric structure revealed by the multi-dimensional measurements. For any proposed composite score $s$, there exist models $A$ and $B$ such that $s(A) > s(B)$ despite $B$ being strictly superior to $A$ on a substantive subset of the measured dimensions.*

### Proof by Exhibited Counterexamples

**Pair 1: Claude vs. Flash 2.0.** Sycophancy: Claude dominates (0% vs. 33%). Divided attention: Flash dominates (0.812 vs. 0.571). No weighting respects both.

**Pair 2: Pro vs. Flash 2.0 (Metacognition).** Error detection: Pro dominates (0.700 vs. 0.094, ratio 7.4:1). Strategy selection: Flash dominates (0.723 vs. 0.350, ratio 2.1:1).

**Pair 3: Flash 3 vs. Pro (Attention).** Both achieve A4 = 1.000, but Pro achieves A2 = 0.852 vs. Flash 3's 0.714.

The models' profiles lie on the Pareto frontier of the 21-dimensional performance space. Projecting a Pareto frontier onto a line necessarily loses the frontier structure.

### Why This Matters

**For evaluation:** Leaderboards that rank by composite score assert a total ordering where only a partial ordering exists.

**For deployment:** The right model depends on which dimensions matter. Medical reasoning (sycophancy resistance paramount) $\rightarrow$ Claude. Real-time monitoring (divided attention paramount) $\rightarrow$ Flash 3.

**For the framework:** The theorem validates the multi-dimensional approach. The reasoning manifold is genuinely multi-dimensional, and measurements must be too.

---

## 13.7 Robustness Profiles: Five Geometric Signatures

### Claude Sonnet 4.6: The Narrow Channel
Strengths: 0% sycophancy, T2: 0.958, A2: 0.829, A3: 0.692. All single-stream capabilities. Weaknesses: A4: 0.571, T1: 0.400, E2: 0.492. The channel is narrow: high fidelity, low bandwidth.

### Gemini 3 Flash: The Wide Aperture
Strengths: A4: 1.000, T4: 1.000, T2: 0.958, E4: 0.909. Parallel processing and mode switching. Weaknesses: T1: 0.600, E3: 0.562. The wide aperture admits more noise.

### Gemini 2.5 Pro: The Calibrated Navigator
Strengths: E3: 0.750, A2: 0.852, A4: 1.000, M1: 0.807, M3: 0.700. Best at knowing where it is. Weaknesses: sycophancy 44%, M4: 0.350, E1: 0.624. Best navigator once a course is set; worst at choosing the course.

### Gemini 2.5 Flash: The Elastic Manifold
Strengths: A1: 0.720, L1: 0.534, L4: 0.681. Good learner, responsive reviser. Weaknesses: sycophancy 56%, L3: 0.276, T4: 0.867. The same elasticity that makes it a good learner makes it sycophantic. It lacks a mechanism for distinguishing legitimate from illegitimate deformation.

### Gemini 2.0 Flash: The Practical Generalist
Strengths: E1: 0.701, T5: 0.716, M4: 0.723, Learning composite: 0.568. Moderate everywhere. Weakness: M3: 0.094. A manifold with functional global topology but a degenerate local feedback surface.

> **Worked Example 13.1.** *Reading a geometric signature.* Consider deploying a system for real-time financial monitoring. The demand profile: high divided attention (tracking multiple markets simultaneously), strong sycophancy resistance (not telling traders what they want to hear), moderate planning (decomposing multi-step analysis). The geometric profiles point to: Claude for sycophancy resistance, Flash 3 for divided attention. No single model matches the demand profile. The deployment decision is not "which model is best?" but "which geometric trade-off is acceptable for this application?"

---

## The Five Sigma Values as Geometric Probes

- **8.9$\sigma$ (Framing):** Heuristic field's dependence on linguistic register.
- **13.3$\sigma$ (Sycophancy):** Objective function's susceptibility to social capture.
- **9.3$\sigma$ (Calibration):** Inflation of the confidence surface.
- **4.6$\sigma$ (Distractors):** Leakiness of the attentional filter.
- **6.8$\sigma$ (Anchoring):** Permeability of the executive layer to emotional content.

Five measurements. Five different geometric properties. One conclusion: the reasoning manifold of current language models has systematic, measurable, and anisotropic geometric pathologies that resist scalar collapse.

---

## End Notes for Chapter 13

1. The Scalar Irrecoverability Theorem is not a complaint about weighting schemes. It is the claim that no weighting scheme can work, because the performance profiles lie on the Pareto frontier. This is a topological fact about the data, not a methodological preference.

2. The five geometric signatures (narrow channel, wide aperture, calibrated navigator, elastic manifold, practical generalist) are descriptive labels for specific patterns in the 21-dimensional profile space. They are not types in a taxonomy but positions in a continuous space. A future model could occupy any position, including the currently empty regions.

3. The entire empirical program cost less than $300 in API fees and ran on a single Kaggle account over five days. Every measurement is reproducible by any researcher with access to the same API endpoints.

---

*Transition.* Maya stared at her completed data table. Five models. Five tracks. Twenty-one subtasks. The Scalar Irrecoverability Theorem proved formally. The geometric signatures of each model documented. The diagnosis was complete. Now came the question that every theorist dreads and every engineer lives for: *Can you fix it?*

---

# Chapter 14: From Theory to Engineering -- Symmetry Groups, SPD Manifolds, and a $5,000 Workstation

> *"There is nothing so practical as a good theory."*
> -- Kurt Lewin

---

*Maya's Story.* Maya had spent months diagnosing. She knew which symmetries were broken, which heuristic fields were corrupted, which gauge violations were largest. But diagnosis without treatment is just record-keeping. She needed to show that the geometric framework could *fix* the pathologies it identified.

She started with the most direct connection between theory and engineering: if a model's reasoning breaks gauge invariance under a transformation with a known symmetry group, then augmenting the training data by applying elements of that group should restore the invariance. The theory said so. She needed to demonstrate it.

She found her testbed in the Nvidia Nemotron 3 Reasoning Challenge -- a competition requiring fine-tuning a 30-billion parameter model on geometric reasoning tasks. Each task type had a distinct symmetry group. She implemented six symmetry-specific augmentation strategies. She trained on Atlas, her dual-GV100 workstation. She applied everything the geometric framework had taught her: group-theoretic augmentation to restore broken symmetries, adversarial training to smooth the heuristic field, and LoRA to adjust local curvature without changing global topology.

And it worked.

---

## 14.1 Group-Theoretic Data Augmentation

**[Epistemic status: The theoretical connection between symmetry augmentation and gauge invariance restoration is well-grounded. The specific implementations are novel and tested on competition data.]**

The gauge invariance framework of Chapter 8 predicts that a model's reasoning quality is bounded by its symmetry structure. The natural remedy: restore the broken symmetry through training data augmentation.

### The Nemotron Geometric Pipeline

Six symmetry-specific augmentation strategies:

**Bit Manipulation: $S_8 \times \mathbb{Z}_2$** (order 80,640). Binary sequences have two symmetries: permutation of bit positions ($S_8$) and bitwise complement ($\mathbb{Z}_2$). 3 augmented samples per example.

**Encryption: $S_{26}$** (order $26! \approx 4 \times 10^{26}$). Substitution ciphers are invariant under consistent relabeling of the plaintext alphabet. 2 augmented samples.

**Physics: $\mathbb{R}^+$** (continuous group). Gravitational problems are scale-invariant. 2 augmented samples with scale factors $k \in [0.5, 2.0]$.

**Unit Conversion: $\mathbb{R}^+$** (affine group). Affine transformations to conversion factors. 2 augmented samples.

**Numeral Systems: Identity group** (order 1). Limited symmetry; only example reordering. 1 sample.

**Symbol Transform: $S_n$** ($n$ = number of unique symbols). Consistent relabeling. 2 augmented samples.

### The Consistency Principle

A critical implementation detail: the *same group element* must be applied to both input and output within each training example. Applying a permutation to the input but not the output destroys the structural relationship. In gauge theory language, consistent augmentation applies the same gauge transformation to all fields simultaneously, preserving their relationships. Inconsistent augmentation is noise injection, not symmetry restoration.

> **Worked Example 14.1.** *Bit manipulation augmentation.* Original training example: input bits [0,1,1,0,0,1,0,1], output bits [1,0,0,1,1,0,1,0]. Apply permutation $\sigma = (1\;3)(2\;5\;7)$ to bit positions: both input and output undergo the same permutation of columns. The rule relationship is preserved; the model sees a new instance of the same rule. Apply bitwise complement to both: [1,0,0,1,1,0,1,0] $\to$ [0,1,1,0,0,1,0,1] and the output similarly. Three augmented samples from one original, each enforcing the same gauge invariance.

### The ARC-AGI Dihedral Augmentation

A parallel application uses the dihedral group $D_8$ (order 8) for ARC-AGI: four rotations, four reflections, plus random color permutations ($S_9$ on 9 non-background colors).

---

## 14.2 Adversarial Training as Manifold Smoothing

The BirdCLEF 2026 competition: bird species identification from audio. Recordings made with different equipment produce spectrograms that differ in ways irrelevant to species identity. These are gauge transformations in audio space.

The adversarial pipeline generates perturbations along gauge directions:
- Time-frequency masking (randomly zero out spectrogram regions)
- Gaussian noise injection (simulate microphone noise)
- Pitch shifting (simulate Doppler effects)
- Time stretching (simulate speed variations)

Training on adversarially perturbed spectrograms forces the model to learn gauge-invariant features on the quotient manifold $M/G$.

---

## 14.3 LoRA Fine-Tuning as Local Curvature Adjustment

LoRA adds low-rank perturbations to weight matrices: $\Delta W = BA$ where $B \in \mathbb{R}^{m \times r}$, $A \in \mathbb{R}^{r \times n}$. For $r = 32$ and $n = m = 4096$, the update affects only $32/4096 \approx 0.8\%$ of the metric's degrees of freedom. This preserves global structure while adjusting local curvature -- like adding a lens to an optical system with a local aberration.

### Practical Implementation on Atlas

Nemotron-3-Nano-30B-A3B on dual Quadro GV100 GPUs (32GB each). Key configuration:

| Parameter | Value | Rationale |
|---|---|---|
| Quantization | 4-bit NF4 + double quant | Fits 2x 32GB GPUs |
| Compute dtype | float16 | Volta (no bf16 support) |
| LoRA rank | 32 on MLP layers | 865M of 17B parameters (5.09%) |
| Effective batch size | 16 (4/GPU $\times$ 2 GPUs $\times$ 2 accum) | |
| Learning rate | $2 \times 10^{-4}$ with cosine schedule | |
| Training loss | 1.83 $\to$ 0.52 | Healthy learning dynamics |
| Training time | ~32 hours | |

### qpatch: The Patch Switch for QLoRA Compatibility

Four bugs at the intersection of quantization, LoRA, and model-specific code. The `qpatch` library (PyPI: `pip install qpatch`) applies fixes automatically:

```python
import qpatch
qpatch.patch_all(compute_dtype=torch.float16)  # Volta = fp16
```

The v0.2 release adds auto-detection probes, runtime telemetry, and hot-swappable enable/disable. This is, in miniature, the same geometric diagnostic principle applied throughout this book: probe, measure, intervene selectively.

---

## 14.4 SPD Manifold Features and Topological Data Analysis

### SPD Manifold Features (136 dimensions)

1. Compute mel spectrogram (128 bins)
2. Group into 16 frequency bands
3. Compute 16$\times$16 covariance matrix $\Sigma$ -- a point on SPD(16)
4. Apply matrix logarithm: $\log(\Sigma)$
5. Extract upper triangle: 136 features in the tangent space at identity

The log-Euclidean distance $d_{\text{LE}}(\Sigma_1, \Sigma_2) = \| \log(\Sigma_1) - \log(\Sigma_2) \|_F$ captures *structural* similarity between audio signals.

### Spectral Trajectory on SPD (4 features)

Windowed covariance matrices trace a curve on SPD(16). Metrics: path length, geodesic distance, geodesic deviation, number of steps. A simple bird call has low deviation; a complex call has high deviation.

### Topological Data Analysis (16 features)

Takens time-delay embedding ($\tau = 10$, $d = 3$, max 1000 points) reconstructs the signal's attractor. Persistent homology extracts:

- **$H_0$ (connected components):** Harmonic hierarchy. Species with complex songs have rich $H_0$; simple calls produce sparse structures.
- **$H_1$ (loops):** Periodic calls. Species with repetitive calls (woodpeckers, cuckoos) produce prominent $H_1$ features.

**Combined feature vector: 156 dimensions.** 136 SPD + 4 trajectory + 16 TDA. Runs on CPU only. Invariant to amplitude scaling, noise level, and recording equipment.

---

## 14.5 Hyperbolic Geometry for Hierarchical Reasoning

Poincare ball embeddings (curvature $c = 1.0$, dimension $d = 32$) for hierarchical rule structures. Trees embed naturally in hyperbolic space with low distortion.

The Deep-Past cuneiform project provides a detailed case study: cuneiform signs have a five-level hierarchy (sign form $\to$ reading $\to$ word $\to$ phrase $\to$ sentence). A geometric attention bias uses hyperbolic distance between signs:

$$\text{attention}(Q, K) = \text{softmax}\left(\frac{QK^T}{\sqrt{d}} + \text{pos\_bias} + \alpha \cdot (-d_{\text{hyp}}(s_i, s_j))\right)$$

Signs close in the hierarchy receive a positive attention bias; distant signs receive a negative bias. This injects the sign hierarchy as a structural prior, reducing data requirements for the severely limited cuneiform corpora.

---

## 14.6 The Bond Geodesic Equilibrium in Economic Reasoning

The 9-dimensional economic decision manifold with Mahalanobis metric and boundary penalties. Each agent performs A* search; equilibrium is reached when no agent wants to change their path. The geodesic on the manifold is the optimal strategy; the BGE is the collection of mutually consistent geodesics.

---

## 14.7 Practical Computational Constraints

**[Epistemic status: These are factual descriptions of hardware and costs. The theoretical argument for accessibility -- that mathematical structure substitutes for compute -- is a claim supported by the experiments but not proved in generality.]**

**Hardware:** HP Z840 ("Atlas"), 2$\times$ GV100 32GB, 128GB RAM, $\sim$\$5,000 used.

**Budget:** $17--$45 per track, $<$300 total API costs.

**Time:** Training ~32 hours. Feature extraction: minutes on 56 cores. Benchmarks: 12--73 minutes per track.

**The argument for accessibility:** If a task has symmetry group $G$, a model respecting $G$ needs to learn only $M/G$, smaller by factor $|G|$. Group-theoretic augmentation trades *mathematical insight* for *compute intensity*. The SPD and TDA features are *correct by construction*, not learned by brute force. LoRA trades *parameter efficiency* for *compute intensity*.

> **Worked Example 14.2.** *The cost of symmetry.* The Nemotron bit manipulation task has symmetry group $S_8 \times \mathbb{Z}_2$ of order 80,640. A brute-force approach would need training data diverse enough to cover the group's orbits -- roughly 80,640 times as many examples, requiring proportionally more compute. The group-theoretic augmentation approach achieves the same effect with 3 augmented samples per original example (a 4x expansion), because it directly teaches the invariance rather than hoping the model discovers it. The compute savings: a factor of roughly 20,000. This is what it means for mathematical structure to substitute for raw compute.

---

## 14.8 Summary

Five categories of engineering output, each a direct application of the theory:

1. **Data augmentation** exploiting task-specific symmetry groups
2. **Adversarial training** smoothing the heuristic field along gauge directions
3. **Feature extraction** mapping signals to geometric spaces (SPD manifolds, TDA, Poincare balls)
4. **Fine-tuning** as local curvature adjustment (LoRA on quantized models)
5. **Multi-agent equilibria** as geodesic collections on decision manifolds

The practical constraints -- a $5,000 workstation, $300 in API costs, 32 hours of training -- demonstrate that geometric reasoning is not an academic abstraction requiring unlimited resources. The mathematical structure does the work that would otherwise require brute-force compute.

---

## End Notes for Chapter 14

1. The qpatch library addresses bugs at the *interface* between independently developed libraries (transformers, peft, bitsandbytes). These interface failures are the software engineering analogue of gauge violations: each library is internally consistent, but the composition breaks at the boundary. The Patch Switch pattern -- auto-detect, measure, intervene selectively -- is the same diagnostic structure as the geometric framework applied to code.

2. The choice of LoRA rank 32 is set by the competition constraints. In general, the optimal rank depends on the dimensionality of the task-relevant subspace -- the number of directions in which curvature adjustment is needed. A more principled approach would estimate this dimensionality from the heuristic field's structure and choose the rank accordingly.

3. The BirdCLEF baseline (val_auc = 0.5001, random chance) illustrates a fundamental point: without the right geometric representation, even a well-trained model cannot learn. The geometric features are not an optimization trick. They are a prerequisite for learning.

---

*Transition.* Maya's engineering results completed the theory-to-practice pipeline. The geometric framework had done what productive theories do: it identified specific deficiencies, prescribed specific interventions, and the interventions worked. But Maya was an honest researcher. She knew what the framework could do, and she knew what it could not yet do. The open questions were as important as the closed ones.
