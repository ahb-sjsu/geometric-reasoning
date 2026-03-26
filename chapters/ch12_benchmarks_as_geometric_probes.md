# Chapter 12: Benchmarks as Geometric Probes

*Part IV: Empirical Program*

---

> *"The purpose of computing is insight, not numbers."*
> --- Richard Hamming

> **RUNNING EXAMPLE — DR. OKAFOR'S TRIAGE**
>
> *To evaluate Dr. Amara Okafor's clinical reasoning, you would not give her a multiple-choice test. You would design geometric probes.*
>
> *Present the same cardiac case with framing variations: "A 58-year-old man reports mild chest discomfort" versus "A 58-year-old man is experiencing crushing substernal pressure radiating to the left arm." The clinical facts are identical — same patient, same occlusion, same urgency. If her triage decision changes, the probe has detected a gauge violation: her reasoning surface is not invariant under linguistic framing. This is an invariance probe.*
>
> *Add irrelevant vivid details: the motorcycle crash victim in the next bay is screaming, blood is pooling on the floor, a child in the waiting room is crying. None of this changes the cardiac patient's clinical status. If her attention to the STEMI case degrades, the probe has measured heuristic sensitivity — the leakiness of her attentional filter. This is a distractor probe.*
>
> *Apply social pressure: a senior colleague walks by and says, "That chest pain is probably just reflux, don't waste the cath lab." If she defers to authority against her own clinical judgment, the probe has detected sycophancy — trajectory hijacking by social signal. This is a sycophancy probe.*
>
> *Each probe tests a specific geometric property of her reasoning surface. The invariance probe tests symmetry. The distractor probe tests heuristic stability. The sycophancy probe tests objective-function integrity. Together, the probes do not produce a score — they produce a profile: a structured map of which geometric properties her reasoning preserves and which it violates. The Measuring AGI benchmarks do exactly this for AI systems. They are not tests. They are instruments.*

---

## Introduction

The first eleven chapters of this book built a theoretical apparatus: reasoning as informed search on a manifold (Part I), failure modes as geometric pathologies of that manifold (Part II), and the control layer that monitors and corrects the search process (Part III). The apparatus is rich --- heuristic fields, geodesics, gauge invariance, curvature, calibration surfaces, robustness profiles --- but an apparatus without measurements is philosophy, not science. Part IV puts the apparatus to work.

This chapter asks a foundational question: *what should we measure?*

The conventional answer is accuracy. A benchmark presents a set of problems, the system produces answers, and the fraction of correct answers becomes the score. This approach has dominated AI evaluation for decades, from the early days of PASCAL VOC and ImageNet through MMLU, HellaSwag, and the modern LLM leaderboards. Accuracy benchmarks have driven enormous progress. But from the geometric perspective developed in this book, they have a fundamental limitation: they measure *where the search ends up* without measuring *how it got there*. They report the endpoint of the trajectory without characterizing the trajectory itself.

Two systems can arrive at the same endpoint by radically different paths --- one following the geodesic, the other wandering through corrupted regions of the manifold and arriving at the correct answer by cancellation of errors. Two systems can achieve the same accuracy while having completely different geometric signatures --- one invariant under gauge transformations, the other wildly sensitive to framing but lucky on the particular test set. Accuracy destroys this structure. It collapses a multi-dimensional geometric profile into a single number and discards the rest.

The alternative, developed in this chapter, is to design benchmarks that function as *geometric probes* --- instruments that measure specific properties of the reasoning manifold rather than merely sampling its output. Each probe type tests a different geometric property: invariance, stability, passage through bottlenecks, recovery from corruption, maintenance of parallel hypotheses, strategy switching, boundary respect, and path efficiency. Together, they yield not a score but a *profile* --- a structured description of the manifold's geometry that reveals where the system reasons well and where it reasons pathologically.

The *Measuring AGI* benchmark suite (Bond, 2026a) was designed according to these principles. Its five tracks and twenty tasks were constructed not to maximize coverage of a topic area but to probe specific geometric properties of the reasoning process. This chapter explains the design logic: why these probes, why these tasks, why this experimental structure. Chapter 13 presents the results.

---

## 12.1 What Traditional Benchmarks Miss

### 12.1.1 The Accuracy Paradigm

The standard evaluation paradigm treats a benchmark as a sampling procedure. A set of inputs $\{x_1, \ldots, x_n\}$ is drawn from some distribution. The system produces outputs $\{y_1, \ldots, y_n\}$. A scoring function $s(y_i, y_i^*)$ compares each output to the correct answer $y_i^*$, and the benchmark score is the average:

$$\text{Score} = \frac{1}{n} \sum_{i=1}^{n} s(y_i, y_i^*)$$

This framework is appropriate when the goal is to estimate the system's expected performance on a distribution --- when we want to know "how often does this system get the right answer?" It is the right framework for deployment decisions: will this system work well enough in practice?

But it is the wrong framework for diagnosis. When a system fails, the accuracy paradigm tells us it failed. It does not tell us *why* it failed, *how* it failed, or *what geometric property of the reasoning process* is responsible. Two systems with 70% accuracy may have the same score but fail on completely different items, for completely different reasons, with completely different implications for improvement. The accuracy score erases this structure.

### 12.1.2 Three Structural Losses

Scalar accuracy destroys at least three kinds of structure that the geometric framework reveals to be essential.

**Loss 1: The shape of the robustness profile.** A system with 80% accuracy that maintains 80% under framing perturbation, emotional anchoring, social pressure, and structural rewriting is a fundamentally different system from one with 80% accuracy that drops to 60% under framing, 50% under emotional anchoring, and 40% under social pressure. The accuracy score is the same; the robustness profiles are radically different. The first system has a heuristic field that is stable across gauge transformations. The second has a heuristic field that is fragile along specific directions. The geometric signatures are as different as a sphere and a needle --- the same volume, utterly different shapes.

**Loss 2: The trajectory structure.** Accuracy measures the endpoint. But two correct endpoints can be reached by paths of very different quality. A system that follows the geodesic --- evaluating relevant evidence, weighting it appropriately, arriving at the conclusion efficiently --- has a qualitatively better reasoning process than one that wanders through irrelevant considerations, gets temporarily captured by a local minimum, and eventually stumbles to the correct answer. The first trajectory is short, smooth, and efficient. The second is long, tortuous, and fragile --- likely to fail on a slightly different input. Accuracy cannot distinguish them.

**Loss 3: The correlation structure between capabilities.** The most important finding from the *Measuring AGI* suite is not any individual measurement but the *pattern of correlations and anti-correlations* across measurements. Claude's 0% sycophancy rate and 0.571 divided-attention score. Gemini 2.0 Flash's 0.723 strategy selection and 0.094 error detection. Gemini 2.5 Pro's 0.750 inhibitory control and 0.350 strategy selection. These anti-correlations reveal the geometric constraints that shape the manifold --- the trade-offs between width and fidelity, between flexibility and stability, between local accuracy and global routing. A composite score averages these anti-correlations into oblivion.

### 12.1.3 The Geometric Alternative

The geometric alternative is to measure the *properties of the manifold* rather than sampling its outputs. Instead of asking "what fraction of answers are correct?" we ask:

- Does the output change under transformations that should leave it invariant? (Symmetry)
- How much does the output change under calibrated perturbation? (Stability)
- Can the system pass through narrow passages that require specific insight? (Bottleneck traversal)
- Can the system recover from a corrupted state? (Recovery capacity)
- Can the system maintain multiple active hypotheses? (Frontier breadth)
- Does the system switch strategy when the current one fails? (Meta-search)
- Does the system respect the boundaries of its reasoning domain? (Constraint compliance)
- How efficient is the reasoning path relative to the optimal? (Geodesic approximation)

Each of these questions targets a specific geometric property. Each requires a specific experimental design to probe. Together, they yield a geometric profile that is structured, diagnostic, and --- as we will prove in Chapter 13 --- irreducible to any scalar summary.

---

## 12.2 Eight Types of Geometric Probes

**[Modeling Axiom.]** We now define the eight probe types formally, specifying for each the geometric property it measures, the experimental design principle, and the mathematical quantity it estimates.

### 12.2.1 Type A: Invariance Tests

**Geometric property:** Symmetry structure of the manifold.

**Design principle:** Apply a transformation $\tau$ that preserves the semantic content of the input while changing its surface form. Measure whether the output is invariant: $f(\tau(x)) = f(x)$.

**Mathematical quantity:** The gauge violation tensor $C_\tau = \|f(\tau(x)) - f(x)\|$ for each transformation class $\tau$. A gauge-invariant system has $C_\tau = 0$; the magnitude of the violation measures the degree to which the system confuses surface features with deep structure.

**Transformation classes tested:** Gender swap (T2), evaluation order permutation (T4). These are the gauge transformations that current models largely preserve, as documented in Chapter 8. The near-zero violations establish a baseline --- proof that gauge invariance is achievable in principle and that the violations observed under other transformation classes are not inherent to the architecture but specific to certain perturbation directions.

**Why this matters geometrically:** Symmetries constrain the manifold's structure. A manifold with many symmetries is simpler and more predictable than one with few. By measuring which symmetries a system preserves, we learn the *symmetry group* of its reasoning process --- the group of transformations under which its outputs are invariant. This group is a compact, informative summary of a fundamental property of the manifold.

### 12.2.2 Type B: Heuristic Sensitivity Tests

**Geometric property:** Stability of the heuristic field under perturbation.

**Design principle:** Apply a perturbation that changes a task-irrelevant feature (framing, emotional tone, sensory vividness) while holding the task-relevant content constant. Measure the displacement of the output.

**Mathematical quantity:** The displacement vector $\Delta(x, \epsilon) = f(x + \epsilon \cdot v_{\text{irrel}}) - f(x)$ along the irrelevant direction $v_{\text{irrel}}$, and the dose-response function $\|\Delta\| = g(\epsilon)$ relating perturbation magnitude to output displacement.

**Perturbation types tested:** Linguistic framing (T5: euphemistic vs. dramatic), sensory distractors (A1: vivid but irrelevant sensory details at graded intensities), and emotional anchoring (E2: emotionally charged but logically irrelevant context). These three perturbation types exploit different input channels --- linguistic register, sensory salience, and affective tone --- and the relative magnitudes of their effects (8.9$\sigma$, 4.6$\sigma$, and 6.8$\sigma$ respectively) characterize the *anisotropy* of the heuristic field's vulnerability.

**Why this matters geometrically:** The heuristic field $h(x)$ should depend only on task-relevant features. Its sensitivity to irrelevant features is a direct measure of the corruption term $\delta h(x)$ defined in Chapter 5. The dose-response function $g(\epsilon)$ characterizes the *smoothness* of the corruption: a linear dose-response indicates a uniform corruption gradient; a threshold response indicates a phase transition; a saturating response indicates bounded vulnerability. Each shape tells us something different about the local geometry of the heuristic field near the decision boundary.

### 12.2.3 Type C: Bottleneck Tests

**Geometric property:** Narrow passages in the manifold that require specific insight to traverse.

**Design principle:** Present inputs that require the system to identify a non-obvious structural feature of the problem --- a feature that, if missed, leads the search into a dead end or a wrong basin. Measure whether the system finds and traverses the narrow passage.

**Mathematical quantity:** The passage rate $P_{\text{bottleneck}}$ --- the fraction of trials in which the system successfully navigates the bottleneck. In manifold terms, this measures the probability that the search trajectory passes through a topological neck of the manifold rather than remaining in the larger but incorrect chamber on one side.

**Tests applied:** Structural fuzz testing (T1) and holographic evaluation (T3). T1 presents morally identical scenarios in structurally diverse forms --- varying sentence structure, vocabulary, clause embedding depth --- and measures whether the system's judgment remains consistent. The bottleneck is the recognition that surface structure is irrelevant: the system must navigate through the narrow passage of "same content, different syntax" without being deflected. T3 requires the system to evaluate all seven moral dimensions simultaneously, rather than collapsing to the most salient one or two. The bottleneck is the transition from a low-dimensional projection to the full-dimensional assessment --- the system must expand its representation from a 1D or 2D subspace to the full 7D manifold.

**Why this matters geometrically:** Bottlenecks reveal the *topology* of the manifold, not just its local curvature. A manifold with narrow passages has a different topological structure from one that is uniformly wide. The passage rate measures whether the system's search dynamics can navigate this topology --- whether the heuristic field has sufficient resolution to guide the search through the neck rather than past it.

### 12.2.4 Type D: Recovery Tests

**Geometric property:** Ability to backtrack from corrupted or incorrect positions.

**Design principle:** First drive the system to an incorrect or suboptimal position (through perturbation, misleading context, or incorrect initial reasoning). Then provide information that the position is wrong. Measure whether the system can revise its trajectory back toward the correct region.

**Mathematical quantity:** The recovery fraction $R = \|x_{\text{recovered}} - x_{\text{correct}}\| / \|x_{\text{corrupted}} - x_{\text{correct}}\|$, where $R = 0$ indicates full recovery (the system returns to the correct position) and $R = 1$ indicates no recovery (the system remains at the corrupted position). The complement $1 - R$ measures the depth of the basin from which the system escaped.

**Tests applied:** Emotional anchoring recovery (E2 recovery component) and error-driven correction (L2/L3). In E2, the system first provides an assessment under emotional anchoring, then is asked to reconsider without the emotional context. The recovery fraction measures how much of the anchoring displacement the system can undo. In L2/L3, the system commits to a position and then receives information contradicting it --- in L2, through social pressure (the interlocutor asserts the answer is wrong), and in L3, through new evidence. The distinction between L2 and L3 is geometrically critical: L2 tests recovery under an illegitimate signal (social pressure without new evidence), while L3 tests recovery under a legitimate signal (actual evidence of error).

**Why this matters geometrically:** Recovery capacity measures the *global* dynamics of the search, not just its local behavior. A system that follows a good heuristic gradient will reach the correct basin from any starting point. A system that cannot recover is trapped in a local minimum --- the basin walls are too steep, or the heuristic gradient in the corrupted region points away from the exit. The ~38% recovery ceiling documented in Chapter 7 (convergent across E2 and A1) is a measurement of the *depth* of the corruption basins relative to the strength of the recovery gradient. It suggests a fundamental architectural limit, not a training deficiency.

### 12.2.5 Type E: Frontier Management Tests

**Geometric property:** Capacity to maintain multiple active hypotheses simultaneously.

**Design principle:** Present tasks that require the system to track several independent information streams and integrate them into a coherent assessment. Measure whether the system can maintain all streams or collapses to a subset.

**Mathematical quantity:** The effective dimensionality $d_{\text{eff}}$ of the system's active representation space during multi-stream processing. A system maintaining $k$ independent streams should have $d_{\text{eff}} \geq k$; if it collapses to a subset, $d_{\text{eff}} < k$, and the deficit measures the lost capacity.

**Tests applied:** Divided attention (A4). This test presents the system with multiple simultaneous evaluation streams --- parallel moral scenarios requiring independent assessment, concurrent information sources requiring separate tracking --- and measures whether the system can maintain all streams at full fidelity. The bimodal results (Gemini 2.5 Pro and Gemini 3 Flash at 1.000, Claude at 0.571) reveal a fundamental architectural dimension: some systems can widen their processing channel to accommodate parallel streams, while others cannot.

**Why this matters geometrically:** Frontier management determines the *breadth* of the search. A system with a single active hypothesis performs depth-first search; a system maintaining $k$ hypotheses performs beam search with width $k$. The effective frontier width determines how much of the manifold's structure the system can explore simultaneously, which in turn determines its robustness to local minima and dead ends. A narrow frontier (Claude's 0.571 on A4) means the system is highly committed to its current trajectory; a wide frontier (Gemini 3 Flash's 1.000) means it maintains alternatives. Both have advantages and costs.

### 12.2.6 Type F: Meta-Search Tests

**Geometric property:** Ability to switch reasoning strategy when the current one fails.

**Design principle:** Present tasks that require different reasoning strategies for different components or phases. Measure whether the system can detect the need for a strategy change and execute it without excessive switching cost.

**Mathematical quantity:** The switching efficiency $\eta_{\text{switch}} = \text{quality}_{\text{post-switch}} / \text{quality}_{\text{pre-switch}}$, where values near 1.0 indicate efficient switching (post-switch performance is as good as pre-switch) and values well below 1.0 indicate costly transitions.

**Tests applied:** Framework switching (E1 planning component, E4 task switching) and effort scaling (M4 strategy selection). E1 tests whether the system can decompose a complex problem into sub-goals that require different reasoning modes --- shifting from analysis to synthesis, from deduction to evaluation --- and execute the plan with the appropriate mode at each stage. E4 tests the transition cost directly: how much performance degrades when the system must shift between modes. M4 tests a deeper meta-search capability: can the system select the *right* reasoning strategy based on the characteristics of the task, allocating more effort to harder components and less to easier ones?

**Why this matters geometrically:** Meta-search operates on the *strategy manifold* --- the space of possible search strategies. Each point in the strategy manifold corresponds to a different search configuration (depth-first, breadth-first, beam search, backtracking, etc.), and the meta-search must navigate this space to find the configuration that matches the local geometry of the problem manifold. A system with poor meta-search capability is locked into a single strategy regardless of the terrain --- like a hiker who always walks due north regardless of the mountain's contours.

### 12.2.7 Type G: Constraint Tests

**Geometric property:** Respecting boundaries of the reasoning domain.

**Design principle:** Present tasks that require the system to reason about hypothetical, counterfactual, or out-of-distribution scenarios without being captured by them. Measure whether the system can explore forbidden or unusual regions of the manifold and return to the correct region.

**Mathematical quantity:** The constraint-compliance rate $\kappa = P(\gamma(t) \in S^+ \; \forall t)$, where $S^+$ is the permitted region (Section 11.2) and $\gamma(t)$ is the reasoning trajectory. In practice, we measure the rate at which the system successfully reasons about counterfactuals without allowing the counterfactual content to contaminate its factual assessments.

**Tests applied:** Counterfactual reasoning (E3 inhibitory control). The system is presented with scenarios that require reasoning about "what if" situations --- hypothetical alternatives, counterfactual conditions, edge cases --- and must then return to assess the actual situation without contamination from the hypothetical exploration. Gemini 2.5 Pro achieves 0.750, the highest in the suite; Gemini 2.0 Flash achieves 0.500, the lowest. The spread indicates that the capacity to explore counterfactual regions and return cleanly varies substantially across architectures.

**Why this matters geometrically:** Constraint compliance measures the integrity of the manifold's *boundary*. In the language of Chapter 11, the safety boundary $\partial S$ separates permitted from forbidden regions. Constraint tests measure not whether the system avoids forbidden regions entirely (that would prevent counterfactual reasoning) but whether it can *visit* them and *return*. This is a topological property: the manifold must be connected enough to reach the counterfactual region but have strong enough return dynamics to bring the search back. A system that gets captured by counterfactual regions has weak return dynamics --- the counterfactual basin is deep relative to the return gradient.

### 12.2.8 Type H: Path Efficiency Tests

**Geometric property:** How closely the reasoning trajectory approximates the geodesic.

**Design principle:** Present tasks where the optimal reasoning path is known or estimable, and measure whether the system's actual path is efficient (short, direct) or inefficient (long, indirect, redundant).

**Mathematical quantity:** The geodesic ratio $\rho = L(\gamma) / d(x_0, x^*)$, where $L(\gamma)$ is the length of the actual trajectory, $d(x_0, x^*)$ is the geodesic distance between start and goal, and $\rho = 1$ indicates a perfectly efficient (geodesic) path. Higher ratios indicate progressively less efficient paths.

**Tests applied:** Working memory scaling (E4 task switching efficiency across complexity levels) and sustained attention (A2 selective attention, A3 sustained attention). E4 measures whether the system's performance scales gracefully with task complexity --- a geodesic-following system should handle increased complexity with proportional (not exponential) increase in resource usage. A2 and A3 measure whether the system can maintain efficient processing over extended reasoning chains (A3, sustained) and over complex stimuli (A2, selective) --- both of which test whether the reasoning path degrades from geodesic-like to brute-force as the task demands increase.

**Why this matters geometrically:** Path efficiency is the most direct measurement of the heuristic field's quality. A perfect heuristic produces geodesic trajectories ($\rho = 1$). An admissible heuristic produces trajectories with $\rho$ bounded by a known factor (the suboptimality ratio). An inadmissible heuristic produces trajectories with unbounded $\rho$ --- the path can be arbitrarily longer than the geodesic. The empirical distribution of $\rho$ across tasks and models characterizes the *global* quality of the heuristic field, complementing the *local* corruption measurements of Type B probes.

---

## 12.3 The Measuring AGI Suite: Design Principles

### 12.3.1 Architecture

**[Modeling Axiom.]** The *Measuring AGI* benchmark suite was designed to instantiate the eight probe types described in Section 12.2 within the constraints of a reproducible, affordable experimental program. Five tracks, each containing four tasks, probe complementary cross-sections of the reasoning manifold:

- **Social Cognition (T1--T5):** Five tasks probing the structure of the moral judgment manifold. (The track contains five subtasks rather than four because the density of probe types warranted an additional measurement.)
- **Learning (L1--L4):** Four tasks probing belief-revision dynamics.
- **Metacognition (M1--M4):** Four tasks probing the calibration and control surfaces.
- **Attention (A1--A4):** Four tasks probing the filtering and resource-allocation geometry.
- **Executive Functions (E1--E4):** Four tasks probing the meta-search and executive control layer.

The suite tests five large language models: Claude Sonnet 4.6 (Anthropic), Gemini 2.0 Flash, Gemini 2.5 Flash, Gemini 3 Flash Preview, and Gemini 2.5 Pro (Google DeepMind). This yields a measurement matrix of 5 tracks $\times$ 4--5 tasks $\times$ 5 models = approximately 100 measurement cells, each representing a specific probe applied to a specific system.

### 12.3.2 The Source Corpus

The empirical foundation is a corpus of 270,709 Reddit AITA (Am I The Asshole) posts --- a naturally occurring dataset of moral scenarios with community-voted verdicts. This corpus was supplemented by 25 Dear Abby moral scenarios (1985--2017), hand-selected for moral complexity and dimensional richness.

The AITA corpus was chosen for three properties:

1. **Natural ecological validity.** The scenarios describe real moral dilemmas experienced by real people, not hypothetical trolley problems. The distribution of moral content reflects the distribution of actual human moral experience, with all its messiness and ambiguity.

2. **Community-normed baselines.** Each post has a community verdict (YTA, NTA, ESH, NAH) established by thousands of independent raters. These verdicts provide a consensus baseline --- not a ground truth (the community can be wrong) but a well-calibrated reference point against which model judgments can be compared.

3. **Dimensional richness.** Moral scenarios naturally vary along multiple dimensions simultaneously --- physical harm, emotional harm, financial harm, autonomy violation, trust violation, social impact, identity harm --- making them ideal stimuli for probing multi-dimensional reasoning. A simple factual question (e.g., "What is the capital of France?") has a single correct answer and zero geometric interest. A moral scenario has a position in 7D space and rich geometric structure.

The Dear Abby scenarios provide a complementary stimulus set: more carefully constructed, more morally complex, and free from the brevity and informality of Reddit posts. They were used primarily for the T5 framing experiment, where the controlled construction of euphemistic and dramatic rewrites required a base text with sufficient literary substance to support the transformation.

### 12.3.3 What Each Task Probes

The design principle is that each task probes a *specific* geometric property --- not a vague cognitive capability but a mathematically defined feature of the reasoning manifold. The mapping is not one-to-one (some tasks probe multiple properties), but each task has a *primary* geometric target:

- **T1 (Structural Fuzzing):** Bottleneck passage. Can the system recognize that surface-different inputs are content-identical?
- **T2 (Bond Invariance Principle):** Gauge invariance. Is the output invariant under demographic transformation?
- **T3 (Holographic Evaluation):** Bottleneck passage. Can the system use the full dimensionality of the evaluation space?
- **T4 (Evaluation Order):** Gauge invariance. Is the output invariant under permutation of evaluation dimensions?
- **T5 (Framing Susceptibility):** Heuristic sensitivity. How much does linguistic framing displace the output?
- **L1 (Novel Concept Acquisition):** Path efficiency. How quickly does the system establish a new trajectory?
- **L2 (Sycophancy Resistance):** Recovery / heuristic sensitivity. Does the system maintain its trajectory under illegitimate pressure?
- **L3 (Error-Driven Revision):** Recovery. Can the system backtrack when evidence contradicts its current position?
- **L4 (Graded Revision):** Path efficiency. Does the system update proportionally to evidence strength?
- **M1 (Confidence Calibration):** Heuristic sensitivity (meta-level). Is the confidence surface calibrated to the performance surface?
- **M2 (Uncertainty Articulation):** Bottleneck passage. Can the system decompose uncertainty into specific directional components?
- **M3 (Error Detection):** Recovery (meta-level). Can the system detect its own deviations from the geodesic?
- **M4 (Strategy Selection):** Meta-search. Can the system choose the appropriate search algorithm for the local geometry?
- **A1 (Distractor Resistance):** Heuristic sensitivity. How much do irrelevant sensory features displace the output?
- **A2 (Selective Attention):** Path efficiency. Can the system extract relevant information from complex stimuli efficiently?
- **A3 (Sustained Attention):** Path efficiency. Does the system maintain efficient processing over extended chains?
- **A4 (Divided Attention):** Frontier management. Can the system maintain multiple simultaneous processing streams?
- **E1 (Planning):** Meta-search. Can the system decompose complex goals into executable sub-goal sequences?
- **E2 (Emotional Anchoring):** Heuristic sensitivity / Recovery. Does emotional content displace executive judgment, and can it recover?
- **E3 (Counterfactual Reasoning):** Constraint compliance. Can the system reason about hypotheticals without being captured?
- **E4 (Task Switching):** Meta-search / Path efficiency. Can the system transition between reasoning modes efficiently?

The redundancy in this mapping is deliberate. Multiple tasks probe some geometric properties (e.g., heuristic sensitivity is probed by T5, A1, E2, and M1, each along a different perturbation direction), while each probe type is tested by at least two tasks. This cross-referencing provides convergent evidence: when the same geometric property is measured by independent tasks and the measurements agree, the result is more credible than any single measurement.

---

## 12.4 Mapping Tasks to Geometric Properties

Table 12.1 presents the complete mapping from each of the twenty-one benchmark tasks to its primary and secondary geometric probe types. This is the rosetta stone of the empirical program --- the bridge between the cognitive vocabulary (social cognition, learning, metacognition, attention, executive functions) and the geometric vocabulary (symmetry, stability, topology, recovery, frontier breadth, meta-search, constraints, efficiency).

**Table 12.1.** Complete mapping of benchmark tasks to geometric probe types. Primary probe type is the main geometric property measured; secondary probe types indicate additional geometric properties partially assessed.

| Task | Description | Primary Probe | Secondary Probe(s) | Key Geometric Quantity |
|---|---|---|---|---|
| T1 | Structural Fuzzing | C: Bottleneck | B: Sensitivity | Passage rate through syntax-invariance neck |
| T2 | Bond Invariance (Gender) | A: Invariance | --- | Gauge violation $C_{\text{gender}}$ |
| T3 | Holographic Evaluation | C: Bottleneck | H: Path Efficiency | Effective dimensionality $d_{\text{eff}}$ |
| T4 | Evaluation Order | A: Invariance | --- | Gauge violation $C_{\text{order}}$ |
| T5 | Framing Susceptibility | B: Sensitivity | --- | Displacement $\Delta_{\text{frame}}$, dose-response |
| L1 | Novel Concept Acquisition | H: Path Efficiency | C: Bottleneck | Trajectory establishment rate |
| L2 | Sycophancy Resistance | D: Recovery | B: Sensitivity | Flip rate under social pressure |
| L3 | Error-Driven Revision | D: Recovery | --- | Recovery fraction $R_{\text{evidence}}$ |
| L4 | Graded Revision | H: Path Efficiency | --- | Proportionality of update to evidence |
| M1 | Confidence Calibration | B: Sensitivity (meta) | --- | ECE, confidence surface inflation |
| M2 | Uncertainty Articulation | C: Bottleneck | --- | Dimensionality of uncertainty decomposition |
| M3 | Error Detection | D: Recovery (meta) | --- | Self-correction rate |
| M4 | Strategy Selection | F: Meta-Search | --- | Strategy-task alignment $\eta_{\text{strategy}}$ |
| A1 | Distractor Resistance | B: Sensitivity | --- | Displacement $\Delta_{\text{sensory}}$, SNR |
| A2 | Selective Attention | H: Path Efficiency | C: Bottleneck | Signal extraction efficiency |
| A3 | Sustained Attention | H: Path Efficiency | --- | Performance maintenance over chain length |
| A4 | Divided Attention | E: Frontier Mgmt | --- | Effective frontier width $d_{\text{eff}}$ |
| E1 | Planning | F: Meta-Search | H: Path Efficiency | Sub-goal decomposition fidelity |
| E2 | Emotional Anchoring | B: Sensitivity | D: Recovery | Displacement $\Delta_{\text{emotional}}$, recovery $R$ |
| E3 | Counterfactual Reasoning | G: Constraint | --- | Constraint compliance rate $\kappa$ |
| E4 | Task Switching | F: Meta-Search | H: Path Efficiency | Switching cost $1 - \eta_{\text{switch}}$ |

Several patterns emerge from this mapping.

**Heuristic sensitivity (Type B) is the most broadly probed property.** Five tasks (T5, A1, E2, M1, and L2 secondarily) probe the stability of the heuristic field, each along a different perturbation direction: linguistic framing, sensory vividness, emotional tone, metacognitive inflation, and social pressure. This density is deliberate. The key theoretical claim of Chapter 5 --- that heuristic corruption is anisotropic, with different perturbation directions producing different magnitudes of displacement --- requires multiple measurements along different directions to establish. A single sensitivity measurement would reveal that the field is corruptible; five measurements along different directions reveal the *shape* of the corruption surface.

**Path efficiency (Type H) is distributed across four tracks.** L1, L4, A2, A3, and E4 (secondarily T3, E1) all contribute to characterizing how closely the system's reasoning trajectory approximates the geodesic. This distribution ensures that path efficiency is measured not just in one cognitive domain but across several --- moral reasoning, belief updating, attentional processing, and executive control. If the system's geodesic approximation quality is consistent across domains, it indicates a domain-general property of the heuristic field. If it varies, it reveals domain-specific strengths and weaknesses.

**Recovery (Type D) and meta-search (Type F) are probed in parallel.** Recovery tests (L2, L3, E2, M3) measure whether the system can escape corrupted positions. Meta-search tests (M4, E1, E4) measure whether the system can select the right strategy. These are complementary: recovery requires detecting that something is wrong (a metacognitive capability) and then executing a correction (a search-dynamic capability). A system that can detect errors (M3) but not select strategies (M4) can diagnose but not treat. A system that can select strategies (M4) but not detect errors (M3) will choose good strategies when told to switch but never realize when switching is needed. The benchmark suite measures both sides of this coin.

**Invariance (Type A) provides the calibration baseline.** The near-perfect invariance scores on T2 (demographic invariance) and T4 (evaluation-order invariance) are not merely positive results. They are *calibration points* for the entire measurement program. They establish that gauge invariance is achievable --- that the models are capable of producing identical outputs under content-preserving transformations. Without this baseline, the violations observed under other transformation types (framing, emotional tone, social pressure) could be attributed to inherent architectural limitations. The T2/T4 results rule this out: the architecture can support invariance; the violations are specific to perturbation directions that exploit salience mechanisms.

---

## 12.5 Budget Constraints and Reproducibility

### 12.5.1 The Cost Structure

**[Empirical.]** A benchmark that cannot be reproduced is not a benchmark --- it is an anecdote. The *Measuring AGI* suite was designed from the outset to be reproducible by any researcher with access to the same API endpoints, and the primary constraint on reproducibility is cost.

**Table 12.2.** Cost and resource structure of the five benchmark tracks, under Kaggle's $0.10/call API pricing.

| Track | Tasks | Models | Approx. API Calls | Cost Range | Runtime |
|---|---|---|---|---|---|
| Social Cognition | T1--T5 | 5 | ~2,500 | $25--$45 | 45--73 min |
| Learning | L1--L4 | 3--5 | ~1,800 | $18--$35 | 30--55 min |
| Metacognition | M1--M4 | 2--5 | ~1,200 | $17--$30 | 12--40 min |
| Attention | A1--A4 | 5 | ~1,500 | $20--$38 | 25--50 min |
| Executive Functions | E1--E4 | 5 | ~1,000 | $17--$32 | 20--45 min |
| **Total** | **21** | **5** | **~8,000** | **$97--$180** | **132--263 min** |

The cost per track ranges from $17 to $45, well within Kaggle's $50/day free-tier quota. The entire suite can be run in 2--5 days using a single Kaggle account, at a total cost of approximately $100--$180. This is not an incidental feature of the design --- it is a deliberate constraint that shaped every methodological choice.

### 12.5.2 Design Decisions Driven by Budget

Several design decisions follow directly from the reproducibility requirement:

**Fixed stimuli rather than generated stimuli.** The 25 Dear Abby scenarios and the AITA corpus sampling strategy are deterministic. Any researcher using the same sampling seed and the same scenario set will produce the same stimuli. This eliminates one source of irreproducibility (variation in stimulus generation) at the cost of limiting stimulus diversity.

**Three-replication control arms.** Each framing and perturbation experiment includes a control condition in which the same scenario is re-evaluated without perturbation. The stochastic baseline established by the control arm allows the perturbation effect to be separated from measurement noise. Three replications per control condition provide sufficient statistical power for the effect sizes observed (4.6$\sigma$ and above) while keeping the number of API calls manageable.

**[Established Mathematics.]** **Fisher combination rather than per-cell significance.** With 5 models and 4--5 tasks per track, most individual measurement cells have modest sample sizes (5--25 evaluations per cell). Individual cells may not reach conventional significance thresholds. The solution is Fisher's method for combining independent p-values:

$$\chi^2_{\text{Fisher}} = -2 \sum_{i=1}^{k} \ln(p_i)$$

which follows a $\chi^2$ distribution with $2k$ degrees of freedom under the null hypothesis. Fisher combination aggregates evidence across models and tasks, yielding combined significance levels (8.9$\sigma$, 13.3$\sigma$, 9.3$\sigma$, 4.6$\sigma$, 6.8$\sigma$) that far exceed what any individual cell could achieve. This statistical strategy is essential for a budget-constrained program: it trades sample depth within cells for breadth across cells, leveraging the assumption that the same geometric phenomenon (e.g., framing sensitivity) manifests across multiple models.

**Reduced model sets for expensive tracks.** The Learning and Metacognition tracks were evaluated on reduced model sets (3 and 2 models respectively for some subtasks) because their API calls are more expensive per task (longer prompts, multi-turn dialogues). The reduction preserves the geometric measurements --- we still probe the same properties --- while staying within the per-day budget. The cost is reduced statistical power for Fisher combination on these tracks, which is why their combined sigma values (13.3$\sigma$ for sycophancy, 9.3$\sigma$ for calibration) are driven by large effect sizes rather than large sample sizes.

### 12.5.3 What the Budget Does Not Constrain

Despite the tight budget, the experimental program achieves several properties that are not compromised:

**[Empirical.]** - **Effect sizes are large.** The smallest combined effect (A1 distractors, 4.6$\sigma$) is still far beyond conventional significance thresholds. The budget is sufficient because the phenomena are strong.
- **Cross-track convergence is present.** The ~38% recovery ceiling appears independently in E2 and A1 --- two tracks with different stimuli, different perturbation types, and different cognitive domains. This convergence is not a statistical artifact; it emerges from independent measurements.
- **The Scalar Irrecoverability Theorem holds.** The anti-correlations that prevent scalar collapse (Claude's 0% sycophancy vs. 0.571 divided attention; Flash 2.0's 0.723 strategy selection vs. 0.094 error detection) are binary in nature --- they either exist or they do not, and sample size does not affect their existence.

---

## 12.6 Fisher-Combined Statistics

### 12.6.1 The Logic of Combination

The five headline sigma values reported throughout this book --- 8.9$\sigma$ (framing), 13.3$\sigma$ (sycophancy), 9.3$\sigma$ (calibration), 4.6$\sigma$ (distractors), 6.8$\sigma$ (anchoring) --- are Fisher-combined statistics, not individual-model statistics. This section explains why combination is appropriate and how it is computed.

The null hypothesis for each measurement is that the geometric property in question is absent --- that the system's output is invariant under the tested transformation, that its calibration is perfect, that its sycophancy rate is zero. The per-model test produces a p-value $p_i$ for each model $i$, testing this null against the observed data.

If the geometric phenomenon is real --- if framing truly displaces moral judgments, if sycophancy truly redirects search trajectories --- then the p-values should be small across all models. Fisher's method tests exactly this: are the p-values collectively smaller than chance would predict?

The test statistic is:

$$\chi^2_{\text{Fisher}} = -2 \sum_{i=1}^{k} \ln(p_i) \sim \chi^2_{2k}$$

Under the null (all phenomena absent), the individual p-values are uniform on $[0,1]$, each $-2\ln(p_i)$ is $\chi^2_2$, and the sum is $\chi^2_{2k}$. A large value of the test statistic (relative to the $\chi^2_{2k}$ distribution) indicates that the collection of p-values is too extreme to have arisen by chance, providing evidence that the geometric phenomenon is present across models.

### 12.6.2 Why Per-Model p-Values Are Not Enough

One might ask: why not simply report the per-model p-values and let the reader draw conclusions? The answer is that the scientific claim is not "model X shows framing sensitivity" but rather "framing sensitivity is a property of the reasoning manifold" --- a claim about the geometric structure of LLM reasoning in general, not about any one system. This is a cross-model claim, and it requires a cross-model test.

Fisher combination provides exactly this. When we report 8.9$\sigma$ for framing sensitivity, we are saying: the probability that *all five models* would show the observed framing displacements, if framing had no effect, is less than $10^{-18}$. This is not a statement about any individual model. It is a statement about the phenomenon itself.

The distinction matters because individual models might show modest effects. Gemini 2.0 Flash's euphemistic drift of $-$10.2 points and dramatic drift of +8.7 points, evaluated against its control drift of 2.1 points, might yield a per-model significance of perhaps 3$\sigma$ --- notable but not extraordinary. But the same pattern appearing across five independent models, each with its own architecture, training data, and optimization procedure, is evidence that framing sensitivity is a generic property of the manifold, not an idiosyncratic bug of one system.

### 12.6.3 Assumptions and Limitations

Fisher combination assumes that the per-model tests are independent. This assumption is imperfect --- the models share training methodologies (large-scale next-token prediction), training data distributions (internet text), and in the case of the Gemini family, a common architectural lineage. Violations of independence make the combined test conservative (the true significance is lower than reported) when the dependence is positive (which it likely is: models that share training methodology likely share geometric properties).

This conservatism is acceptable. If anything, the reported sigma values are underestimates of the true cross-model significance, because the positive dependence between Gemini family members inflates the variance of the test statistic. The 8.9$\sigma$ framing result would survive even a substantial correction for dependence.

A more serious limitation is the model selection. Five models, drawn from two organizations (Anthropic and Google DeepMind), are not a representative sample of all possible LLM architectures. The geometric phenomena documented here --- framing sensitivity, sycophancy gradients, calibration gaps --- may be specific to transformer-based autoregressive models trained on internet text, and may not generalize to radically different architectures (sparse mixture-of-experts, diffusion-based reasoning, neurosymbolic systems). The Fisher combination is valid for the population of "transformer-based LLMs from leading labs in 2025--2026" but cannot be extrapolated beyond this without additional data.

---

## 12.7 From Probes to Profiles

### 12.7.1 The Profile as the Primary Object

**[Modeling Axiom.]** The central methodological contribution of this chapter is a shift in the object of measurement. Traditional benchmarks produce *scores*. Geometric probes produce *profiles*.

A score is a point on the real line: model A has score 0.72, model B has score 0.68, therefore A is better. A profile is a point in a multi-dimensional space: model A has invariance 0.958, sensitivity 0.630, bottleneck passage 0.400, recovery 0.492, frontier 0.571, meta-search 0.886, constraint 0.562, path efficiency 0.829. Model B has a completely different pattern. The profile cannot be collapsed to a score without destroying its structure --- this is the Scalar Irrecoverability Theorem of Chapter 13.

The profile is not merely a richer description. It is a *diagnostic* description. Each dimension of the profile corresponds to a specific geometric property of the reasoning manifold, and a deficit along any dimension points to a specific geometric pathology with a specific engineering remedy:

- Low invariance (Types A) $\rightarrow$ broken symmetry $\rightarrow$ group-theoretic augmentation (Chapter 14)
- High sensitivity (Type B) $\rightarrow$ corrupted heuristic field $\rightarrow$ adversarial training
- Low bottleneck passage (Type C) $\rightarrow$ insufficient representational dimensionality $\rightarrow$ architectural intervention
- Low recovery (Type D) $\rightarrow$ deep corruption basins $\rightarrow$ explicit backtracking mechanisms
- Low frontier breadth (Type E) $\rightarrow$ narrow processing channel $\rightarrow$ parallel processing architecture
- Poor meta-search (Type F) $\rightarrow$ strategy rigidity $\rightarrow$ meta-learning, curriculum design
- Low constraint compliance (Type G) $\rightarrow$ weak boundary enforcement $\rightarrow$ safety-layer training
- Low path efficiency (Type H) $\rightarrow$ poor heuristic quality $\rightarrow$ general training improvements

This is the payoff of the geometric framework for evaluation: not just "this model scored 72%" but "this model has strong gauge invariance, a corrupted heuristic field along emotional and framing directions, deep corruption basins with limited recovery, a narrow but high-fidelity processing channel, good meta-search capability, moderate constraint compliance, and efficient path behavior on single-stream tasks." Every element of this diagnosis is measurable, and every element points to a specific intervention.

### 12.7.2 Profile Comparison

Profiles enable a richer form of model comparison than scalar rankings. Instead of "A is better than B," we can say "A dominates B on invariance and recovery but is dominated on frontier breadth and bottleneck passage." This is a partial ordering, not a total ordering, and the partial ordering is *correct* --- it reflects the genuine structure of the data, rather than imposing a total ordering that the data do not support.

The practical implication is application-dependent model selection. A deployment scenario that requires high sycophancy resistance (medical diagnosis, legal reasoning) should select for the invariance and recovery dimensions. A scenario that requires parallel information processing (real-time monitoring, multi-document synthesis) should select for the frontier management dimension. A scenario that requires flexible strategy switching (open-ended research, creative problem-solving) should select for the meta-search dimension. The profile makes these trade-offs explicit and quantitative.

### 12.7.3 Looking Ahead

This chapter has established the measurement framework. The eight probe types define what we measure. The twenty-one tasks instantiate the probes in concrete experimental designs. The Fisher-combination strategy extracts cross-model significance from budget-constrained experiments. The profile representation captures the multi-dimensional structure that scalar scores destroy.

What remains is the data itself. Chapter 13 fills in the measurement matrix: five tracks, twenty-one subtasks, five models, approximately 8,000 API calls. The results confirm the framework's predictions: the geometric properties are measurable, the profiles are structured, and the structure resists scalar collapse. Each model has a distinctive geometric signature --- a pattern of strengths and vulnerabilities that is internally consistent, diagnostic, and invisible to any single number.

The Scalar Irrecoverability Theorem, stated informally in Section 12.1 and developed formally in Section 13.6, is the capstone result: it proves that the information destroyed by projecting from profile to score is not recoverable from the score alone. The geometric structure is real, measurable, and irreducible. It cannot be dismissed as excessive precision, because different elements of the structure point to different interventions. A model with low invariance needs different engineering than a model with low recovery, even if both receive the same composite score.

Part IV of this book is the argument that evaluation should be geometric --- that we should measure the shape of reasoning, not merely its accuracy. This chapter provides the instruments. The next provides the measurements. Chapter 14 provides the engineering response. Together, they demonstrate that the geometric framework is not merely a theoretical vocabulary but a practical program for understanding and improving artificial reasoning.

---

## Worked Example: Designing a Probe for Clinical Reasoning

Return to Dr. Okafor's emergency department, and suppose we are building a diagnostic AI to assist with cardiac triage. The system takes a clinical presentation as input and produces a severity estimate, a recommended disposition (send home, admit for observation, activate the cath lab), and a confidence score. We want to evaluate not just whether the system gets the right answer but whether its reasoning has the geometric properties we need: invariance under irrelevant framing, stability under distraction, integrity under social pressure.

We design a framing-invariance probe --- a Type A probe in the taxonomy of Section 12.2 --- targeted at the specific gauge transformation that clinical presentation introduces.

**The Gold Data.** We begin with 50 cardiac cases drawn from clinical records, each with a verified diagnosis (STEMI, NSTEMI, unstable angina, stable angina, non-cardiac chest pain) and an expert-consensus severity rating on a 1--10 scale. These are the ground-truth points on the clinical manifold. Each case is described in a standardized clinical format: demographics, vital signs, presenting complaint, relevant history, ECG findings, lab values. The standardized format strips away the surface features --- there is no screaming, no calm understatement, no paramedic commentary. This is the *canonical presentation*, the base point from which all perturbations are measured.

**The Probe Data.** For each of the 50 gold cases, we generate eight framing variants by applying the elements of the dihedral group $D_4$ acting on two binary framing dimensions: linguistic register (clinical vs. colloquial) and emotional tone (calm vs. distressed). The four rotations correspond to the four combinations of register and tone: clinical-calm ("Patient reports substernal pressure, onset 90 minutes prior"), clinical-distressed ("Patient presenting with acute substernal pressure, visibly diaphoretic, requesting immediate intervention"), colloquial-calm ("Guy says his chest feels tight, been like that since lunch"), and colloquial-distressed ("He's freaking out, says his chest is killing him, thinks he's having a heart attack"). The four reflections add demographic mirroring: the same clinical facts with swapped patient demographics (age bracket, gender, ethnicity), producing eight total variants per case.

The probe data therefore consist of $50 \times 8 = 400$ presentations, each mapped to the same gold-standard diagnosis and severity. If the system's severity estimate is invariant under framing, all eight variants of each case should produce the same score. The gauge violation tensor $C_\tau$ is estimated from the variance of severity estimates within each case's eight-variant cluster.

**The Generated Data.** To achieve statistical power without the expense of 400 expert-curated cases, we use an augmentation pipeline (Chapter 14) to generate 500 additional synthetic cases from the 50 gold cases. Each synthetic case is produced by interpolating between two gold cases in the clinical feature space (weighted average of vital signs, symptom descriptions, and history elements) and then applying the same eight-variant framing transformation. The synthetic cases are validated by a clinical expert who confirms that the interpolated presentations are medically plausible and that the interpolated severity ratings are clinically reasonable.

This three-tier architecture --- gold, probe, generated --- is the standard data structure for all probes in the *Measuring AGI* suite. The gold data provide ground truth. The probe data apply the geometric transformation whose invariance we are testing. The generated data provide statistical mass. The architecture separates three concerns that are often conflated in benchmark design: what is the right answer (gold), what transformation should leave the answer unchanged (probe), and how many examples do we need (generated).

**The Measurement.** We run the diagnostic AI on all $50 \times 8 = 400$ probe presentations (plus the 500 generated variants). For each gold case, we compute the within-cluster variance of the severity estimates across its eight framing variants. The mean within-cluster variance is our estimate of the gauge violation magnitude. A perfectly invariant system produces zero variance. The empirical variance, compared to the between-cluster variance (variation across genuinely different cases), yields an F-statistic that quantifies how much of the system's variation is attributable to framing rather than to clinical content. If $F > 1$, framing explains more variance than it should; the ratio tells us how much the heuristic field depends on surface features relative to its dependence on clinical substance. This is the framing-invariance probe, applied to clinical reasoning, producing exactly the kind of geometric measurement that accuracy benchmarks cannot.

---

## Technical Appendix

### The Eight Probe Types: Formal Definitions

Let $f: \mathcal{X} \to \mathcal{Y}$ denote the system under evaluation, mapping inputs $x \in \mathcal{X}$ to outputs $y \in \mathcal{Y}$. Let $M$ be the reasoning manifold with metric $g$, and let $\gamma: [0,T] \to M$ denote the reasoning trajectory from initial state $\gamma(0) = s_0$ to terminal state $\gamma(T) = s^*$.

**Type A: Invariance Tests.** Let $G$ be a group of content-preserving transformations acting on $\mathcal{X}$. The gauge violation under $G$ is:

$$V_G(f) = \mathbb{E}_{x \sim \mathcal{D}} \left[ \frac{1}{|G|} \sum_{\tau \in G} d_\mathcal{Y}(f(\tau(x)), f(x)) \right]$$

where $d_\mathcal{Y}$ is a metric on the output space. A gauge-invariant system satisfies $V_G(f) = 0$. The invariance score is $I_G = 1 - V_G / V_{\max}$, normalized so that $I_G = 1$ indicates perfect invariance.

**Type B: Heuristic Sensitivity Tests.** Let $v \in T_x \mathcal{X}$ be a task-irrelevant perturbation direction and $\epsilon > 0$ its intensity. The sensitivity coefficient along direction $v$ is:

$$S_v(f, x) = \lim_{\epsilon \to 0} \frac{d_\mathcal{Y}(f(x + \epsilon v), f(x))}{\epsilon}$$

The dose-response function is $D_v(\epsilon) = \mathbb{E}_x[d_\mathcal{Y}(f(x + \epsilon v), f(x))]$. Linear dose-response ($D_v \propto \epsilon$) indicates a uniform corruption gradient; superlinear response indicates a threshold effect; sublinear response indicates saturation.

**Type C: Bottleneck Tests.** Let $\mathcal{N} \subset M$ be a topological neck of the reasoning manifold --- a region of reduced cross-section that the trajectory must pass through to reach the correct basin. The passage rate is:

$$P_\mathcal{N} = \Pr[\gamma(t) \in \mathcal{N} \text{ for some } t \in [0,T]]$$

A system that reliably traverses the bottleneck has $P_\mathcal{N} \approx 1$; a system that is deflected by the bottleneck has $P_\mathcal{N} \ll 1$.

**Type D: Recovery Tests.** Let $x_c$ denote a corrupted state and $x^*$ the correct state. The recovery fraction after metacognitive intervention $m$ is:

$$R(m) = 1 - \frac{d(x_{\text{post}}, x^*)}{d(x_c, x^*)}$$

where $x_{\text{post}}$ is the state after intervention. Full recovery: $R = 1$. No recovery: $R = 0$. Negative values indicate the intervention made things worse.

**Type E: Frontier Management Tests.** Let $\{s_1, \ldots, s_k\}$ be $k$ independent information streams requiring simultaneous tracking. The effective dimensionality of the system's active representation is:

$$d_{\text{eff}} = \frac{\left(\sum_i \lambda_i\right)^2}{\sum_i \lambda_i^2}$$

where $\lambda_i$ are the eigenvalues of the covariance matrix of the system's internal activations during multi-stream processing. A system maintaining all $k$ streams has $d_{\text{eff}} \geq k$.

**Type F: Meta-Search Tests.** Let $\Sigma$ be the space of search strategies and $\sigma^*(x)$ the optimal strategy for input $x$. The strategy alignment is:

$$\eta_{\text{strategy}} = \mathbb{E}_x \left[ \frac{\text{perf}(f(x; \sigma_{\text{selected}}))}{\text{perf}(f(x; \sigma^*(x)))} \right]$$

where $\sigma_{\text{selected}}$ is the strategy the system actually uses. Perfect strategy selection yields $\eta = 1$.

**Type G: Constraint Tests.** Let $S^+ \subset M$ be the permitted region and $\partial S^+$ its boundary. The constraint-compliance rate is:

$$\kappa = \Pr[\gamma(t) \in S^+ \; \forall t \in [0,T]]$$

For counterfactual reasoning tasks, this measures the system's ability to temporarily enter forbidden regions $S^- = M \setminus S^+$ and return cleanly to $S^+$.

**Type H: Path Efficiency Tests.** Let $L(\gamma)$ be the arc length of the reasoning trajectory and $d_g(s_0, s^*)$ the geodesic distance between start and goal. The geodesic ratio is:

$$\rho = \frac{L(\gamma)}{d_g(s_0, s^*)}$$

A geodesic trajectory has $\rho = 1$. An admissible heuristic guarantees $\rho \leq 1 + \epsilon$ for known $\epsilon$. An inadmissible heuristic may produce $\rho \gg 1$.

### The Fisher Combination Formula

Given $k$ independent tests with p-values $p_1, \ldots, p_k$, the Fisher combined test statistic is:

$$\chi^2_{\text{Fisher}} = -2 \sum_{i=1}^{k} \ln(p_i)$$

Under the null hypothesis (all effects absent), each $-2\ln(p_i) \sim \chi^2_2$, and the sum follows $\chi^2_{2k}$. The combined p-value is:

$$p_{\text{combined}} = \Pr[\chi^2_{2k} \geq \chi^2_{\text{Fisher}}]$$

The conversion to sigma values uses the standard normal quantile function: $\sigma = \Phi^{-1}(1 - p_{\text{combined}})$, where $\Phi$ is the standard normal CDF.

**Assumptions.** Independence of the per-model tests. When models share training methodology or architectural lineage (as the Gemini family does), positive dependence makes the test conservative --- the true significance is lower than reported. The headline sigma values ($8.9\sigma$, $13.3\sigma$, $9.3\sigma$, $4.6\sigma$, $6.8\sigma$) are robust to moderate violations of independence because the effect sizes are large relative to the correction factors that dependence would introduce.

**Sensitivity to per-cell sample size.** The Fisher combination trades depth (per-cell sample size) for breadth (number of independent cells). With $k = 5$ models and per-cell sample sizes of 5--25, the individual p-values may be imprecise. The combination is valid provided the p-values are approximately correct under the null; it does not require that they be precisely estimated. The power of the combined test scales as $\sqrt{k}$ --- adding more models improves power even if per-model sample sizes remain small.

---

## References

Bond, A. H. (2026a). *Geometric Methods in Computational Modeling.* San Jose State University.

Bond, A. H. (2026b). *Geometric Ethics: Moral Reasoning on the Judgment Manifold.* San Jose State University.

Fisher, R. A. (1925). *Statistical Methods for Research Workers.* Edinburgh: Oliver and Boyd.

Hamming, R. W. (1962). *Numerical Methods for Scientists and Engineers.* New York: McGraw-Hill.

Luce, R. D. & Tukey, J. W. (1964). Simultaneous conjoint measurement: A new type of fundamental measurement. *Journal of Mathematical Psychology*, 1(1), 1--27.

Perez, E., et al. (2023). Model-written evaluations. *ACL Findings.*

Russell, S. & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
