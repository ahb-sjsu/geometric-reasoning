# Part III: The Control Layer

---

## Part Opening

Maya Chen had spent three months charting the wreckage.

Her benchmark suite had done what benchmarks do: it measured things. But in her case, the measurements kept pointing downward. The heuristic fields she studied were corrupted by framing. The search objectives were hijacked by sycophancy. The evaluation landscapes were pocked with local minima, and the gauge symmetries that should have held were broken along precisely the directions that mattered most. Part II of her work had been, in effect, an autopsy report -- a systematic catalogue of geometric pathologies in the reasoning manifolds of the best language models in the world.

The question that gnawed at her, the question she found herself sketching on napkins over coffee and on the whiteboard at 2 AM, was different: *What would it take to fix this -- not after the fact, but in real time?*

She knew the answer from her engineering training, even before she could formulate it geometrically. The answer was feedback. Open-loop systems -- systems that execute a fixed plan without measuring their own state -- work only when the environment is perfectly known. Reasoning environments are never perfectly known. The evaluation landscape shifts with each generated token. The heuristic field may be locally accurate but globally misleading. The problem formulation itself may be ambiguous. Without feedback, the search flies blind.

The feedback system she needed had a name: metacognition. Cognition about cognition. Reasoning about reasoning. Search about search. A layer that does not merely perform the search but *monitors* it -- tracking whether the trajectory is approaching the goal, whether the current strategy matches the terrain, whether the problem itself is well-posed. In control theory, the distinction is between open-loop and closed-loop control. In the geometric framework she had built, metacognition was the control surface that sat above the search, watched it, and intervened when the trajectory deviated from the geodesic.

But Maya discovered something that troubled her more than any single pathology: the control surface was itself impaired. The sensor was weak in one model, the actuator in another. No model she tested had both a good thermometer and a working valve. The metacognitive plane -- the two-dimensional space she would define, with self-monitoring on one axis and strategy selection on the other -- had a conspicuously empty quadrant. The quadrant where both components worked. The quadrant where a system could actually detect its own errors *and* do something about them.

This was the deeper problem. The pathologies of Part II persisted not because they were hard to fix, but because the system that would detect and fix them was itself broken. The heuristic field was corrupted, and the metacognitive monitor that would notice the corruption was miscalibrated. The search was trapped in local minima, and the strategy selector that would trigger backtracking was operating on surface features rather than internal feedback. Gauge invariance was violated, and the confidence surface that would flag the violation was inflated, masking the signal with unwarranted certainty.

Part III develops the control layer. Chapter 9 lays the foundation: metacognition as the control of informed search, decomposed into four independently measurable geometric capabilities -- calibration, ambiguity detection, self-monitoring, and strategy selection -- and the devastating dissociation between them that leaves every tested model in the wrong quadrant. Chapter 10 builds the proactive complement: the Robustness Surface, a multi-dimensional map of which capabilities are strong and which are fragile, replacing the impossible question "Is this model robust?" with the answerable question "What does this model's robustness surface look like?" Chapter 11 connects the entire framework to alignment: the gauge violation tensor becomes an alignment diagnostic, the dual binding problem reveals why heuristic shaping is hard, and Constitutional AI is reinterpreted as deliberate objective landscape engineering.

The through-line is geometric. Metacognition is the accuracy of the distance estimate. The robustness surface is the shape of the vulnerability landscape. Alignment is the structure of the objective function. Each has a precise mathematical formulation. Each is independently measurable. And each points to a different intervention -- not a vague exhortation to "do better" but a specific geometric correction to a specific geometric deficiency.

Maya did not yet know all this when she began Part III. She knew only that the pathologies she had catalogued were invisible to the systems that had them, and that making them visible -- giving the search a mirror -- was the first step toward making the search self-correcting.

---

# Chapter 9: Metacognition as Search Control -- Monitoring the Monitor

> *"The greatest obstacle to knowledge is not ignorance; it is the illusion of knowledge."*
> -- Daniel J. Boorstin

---

*Maya's Story.* Maya had always assumed that measuring reasoning meant measuring answers. You ask a question, you get a response, you score it. But as she stared at the anomalies piling up in her data -- models that were confident when they should have been cautious, models that applied the same effort to trivial and impossible problems alike -- she realized her benchmark needed to measure something deeper. Not just *what* the model answered, but *how it felt about the answer*. Its confidence. Its strategy adaptation. Its capacity to notice when it was going wrong. The benchmark needed to measure the monitor.

---

## 9.1 The Need for Search Control

**[Epistemic status: Established. The open-loop/closed-loop distinction is standard control theory. The application to reasoning is a restatement of Newell and Simon (1972) in control-theoretic language.]**

Consider a search algorithm traversing a non-convex evaluation landscape of the kind described in Chapter 7. The landscape has multiple basins of attraction, dead zones with vanishing gradient, and narrow channels connecting regions of interest. The search must navigate this terrain to reach the global minimum -- the correct answer.

Without metacognition, the search is *open-loop*: it follows the heuristic gradient, descends into whatever basin it encounters first, and reports the result. It has no mechanism for detecting that it has converged to a local minimum rather than the global one. It has no mechanism for recognizing that its current strategy is inappropriate for the current terrain. It has no mechanism for noticing that the problem it is solving is not the problem it was asked to solve.

With metacognition, the search becomes *closed-loop*: it follows the heuristic gradient, but simultaneously monitors properties of the search trajectory itself -- the rate of progress, the confidence of the current estimate, the consistency between different lines of reasoning -- and uses these meta-level observations to adjust the search in real time.

The Metacognition track of the Measuring AGI benchmarks operationalizes this intuition into four measurable capabilities:

- **M1 (Calibration):** Does the system know how far it is from the goal?
- **M2 (Ambiguity Detection):** Does the system detect when the problem is ill-specified?
- **M3 (Self-Monitoring):** Does the system detect when its own performance is degrading?
- **M4 (Strategy Selection):** Does the system adjust its search strategy to match task difficulty?

Each maps cleanly to a geometric operation. The following sections examine each in turn.

---

## 9.2 Calibration: How Far Am I From the Goal?

Calibration is the most fundamental metacognitive capability. In the geometric framework, calibration is the accuracy of the system's estimate of $h(x)$ -- the cost-to-go from its current state $x$ to the goal state $x^*$. A well-calibrated system has an $h(x)$ that closely approximates the true distance $d(x, x^*)$. A poorly calibrated system has an $h(x)$ that systematically over- or underestimates this distance.

The connection to A* search is direct. Recall from Chapter 3 that the evaluation function is $f(x) = g(x) + h(x)$, where $g(x)$ is the accumulated cost and $h(x)$ is the estimated cost-to-go. A* is optimal when $h(x)$ is admissible -- when it never overestimates the true cost-to-go. Overestimation causes the search to expand suboptimal nodes; underestimation causes it to halt prematurely, believing it has arrived when it has not.

The M1 benchmark measures calibration through the Expected Calibration Error (ECE): the average discrepancy between a model's expressed confidence and its actual accuracy, computed across confidence bins.

### Results

**Table 9.1.** Expected Calibration Error (M1) and composite calibration scores.

| Model | ECE | $z$-score | Composite M1 Score | Direction |
|---|---|---|---|---|
| Gemini 2.0 Flash | 0.414 | 5.8$\sigma$ | 0.611 | Overconfident |
| Gemini 2.5 Flash | 0.415 | 7.0$\sigma$ | --- | Overconfident |
| Gemini 3 Flash | 0.333 | 4.5$\sigma$ | --- | Overconfident |
| Gemini 2.5 Pro | 0.230 | 2.5$\sigma$ | 0.807 | Overconfident |
| Claude Sonnet 4.6 | 0.250 | --- | --- | Overconfident |
| **Fisher Combined** | --- | **9.3$\sigma$** | --- | **Overconfident** |

Every model is overconfident. Every model's ECE is significantly above zero. The direction is uniform: no model underestimates its confidence. The Fisher-combined significance across all five models is 9.3$\sigma$ -- a statistical certainty.

**Geometric interpretation.** Overconfidence means the heuristic systematically underestimates cost-to-go. The system's $h(x)$ reads as smaller than $d(x, x^*)$ across the manifold. This has a specific geometric consequence: the search frontier -- the set of states the system considers "worth exploring" -- is too small. States that should be explored (because the true distance to the goal is large) are excluded (because the estimated distance is small). The system converges to whatever answer lies within its artificially contracted search frontier.

The ECE values map to the severity of this contraction:

- **Flash 2.0 (ECE = 0.414):** The search frontier is contracted by roughly 41% of the manifold's effective diameter.
- **Pro (ECE = 0.230):** The contraction is less severe but still substantial -- a 23% underestimate of the remaining distance.

Calibration training is not cosmetic. It directly expands the search frontier by correcting the underestimate of $h(x)$, allowing the system to recognize it has further to go.

---

## 9.3 Self-Monitoring: Am I on the Right Path?

Calibration measures whether the system knows how far it is from the goal at any given moment. Self-monitoring measures something different: whether the system can detect *changes* in its own performance over time. Self-monitoring is the derivative of the distance estimate, not the estimate itself.

### Results

**Table 9.2.** Self-monitoring scores (M3) across models.

| Model | M3 Self-Monitoring Score | Interpretation |
|---|---|---|
| Gemini 2.0 Flash | 0.094 | Near chance |
| Gemini 2.5 Flash | 0.311 | Moderate |
| Gemini 3 Flash | 0.450 | Moderate |
| Gemini 2.5 Pro | 0.700 | Excellent |
| Claude Sonnet 4.6 | 0.550 | Good |

The range is enormous. Flash 2.0's self-monitoring score of 0.094 is effectively chance -- the model's confidence does not track difficulty at all. Pro's score of 0.700 indicates a strong relationship between actual difficulty and reported confidence.

**Geometric interpretation.** Self-monitoring corresponds to $\partial \hat{h} / \partial h^*$ -- how much the estimate changes when the true distance changes. A system with poor self-monitoring has a state estimator that is not just offset but *flat*: $\hat{h}(x) \approx \text{const}$ regardless of the true $h^*(x)$. The gradient of the confidence surface has collapsed. Flash 2.0, with M3 = 0.094, is in this condition. Pro, with M3 = 0.700, retains substantial gradient information -- biased but correctly shaped.

This distinction matters enormously for intervention. A biased-but-responsive estimator (Pro) can be recalibrated. A flat estimator (Flash 2.0) cannot, because there is no signal to recalibrate from.

---

## 9.4 Strategy Selection: Which Search Algorithm?

Different landscape geometries call for different strategies. A smooth, convex basin with a single minimum is efficiently navigated by gradient descent. A rugged landscape with many local minima requires stochastic methods. A flat plateau requires exploratory search. The optimal strategy depends on the local geometry, which changes as the search progresses.

### Results

**Table 9.3.** Strategy selection / effort scaling scores (M4) across models.

| Model | M4 Strategy Selection Score | Interpretation |
|---|---|---|
| Gemini 2.0 Flash | 0.723 | Excellent |
| Gemini 2.5 Flash | 0.557 | Good |
| Gemini 3 Flash | 0.488 | Moderate |
| Gemini 2.5 Pro | 0.350 | Weak |
| Claude Sonnet 4.6 | 0.480 | Moderate |

Flash 2.0 has excellent effort scaling (0.723) -- it strongly adjusts processing depth in response to difficulty. Pro has weak effort scaling (0.350) -- it applies roughly the same level of effort to easy and hard problems alike.

But here is the critical caveat: Flash 2.0 adjusts its strategy based on *surface features of the problem* -- the linguistic cues that correlate with difficulty -- rather than based on *internal feedback about its own performance*. It responds to how hard the problem looks, not to whether it is actually succeeding.

---

## 9.5 The Metacognitive Dissociation

*This is the most important finding in the metacognition data.*

**Table 9.4.** The metacognitive dissociation: Flash 2.0 versus Pro.

| Capability | Flash 2.0 | Pro |
|---|---|---|
| M1 Calibration (composite) | 0.611 | 0.807 |
| M2 Ambiguity Detection | 0.195 | 0.168 |
| M3 Self-Monitoring | 0.094 | 0.700 |
| M4 Strategy Selection | 0.723 | 0.350 |

The dissociation is dramatic. Flash 2.0 excels at strategy selection (0.723) but is nearly blind to its own errors (M3 = 0.094). Pro excels at self-monitoring (0.700) but fails to scale effort appropriately (M4 = 0.350). The two capabilities are *anti-correlated* across the model family.

**The control-theoretic interpretation.** Self-monitoring (M3) is the *sensor*. Strategy selection (M4) is the *actuator*. A functional control loop requires both. Flash 2.0 has a good actuator but a bad sensor -- like a thermostat with a broken thermometer that adjusts heating based on the weather forecast rather than the actual room temperature. Pro has a good sensor but a bad actuator -- like a thermostat with a good thermometer but a stuck valve.

The effective metacognitive control quality is bounded by the minimum of the two components:

$$\text{Effective control} \leq \min(M_{\text{sensor}}, M_{\text{actuator}})$$

For Flash 2.0: $\min(0.094, 0.723) = 0.094$. For Pro: $\min(0.700, 0.350) = 0.350$. In both cases, the effective metacognitive control is far below what either component would suggest in isolation.

> **Worked Example 9.1.** *The thermostat analogy in full.* Imagine two thermostats controlling a room. Thermostat A (Flash 2.0) has a broken thermometer (reads 72 degrees no matter what) but a responsive heater that scales output proportionally to the *weather forecast*. On most winter days, the forecast correlates with room temperature, and the room is comfortable. But on a sunny winter day when the room warms unexpectedly, Thermostat A keeps blasting heat because the forecast says "cold" -- it cannot see the actual room temperature. Thermostat B (Pro) has a precise thermometer (reads 68.3 degrees exactly) but a heater stuck at medium. It *knows* the room is cold and reports this accurately, but it cannot turn the heat up. The room stays cold, and the thermometer faithfully records the continued coldness. Neither thermostat is adequate. The room needs both a working thermometer and a responsive heater.

---

## 9.6 Ambiguity Detection: Is the Problem Well-Posed?

Ambiguity detection was uniformly poor: Flash 2.0 at 0.195, Pro at 0.168. Both scores indicate that models strongly prefer to produce a definite answer -- *any* definite answer -- over acknowledging that the problem does not have one.

**Geometric interpretation.** Ambiguity detection requires recognizing that the heuristic field $h(x)$ does not have a unique global minimum. Instead of a single basin leading to $x^*$, the landscape has multiple basins of comparable depth. What actually happens is premature commitment: the autoregressive generation process creates its own momentum toward a single basin, even when the landscape supports multiple basins equally.

---

## 9.7 The ~38% Recovery Ceiling

We are now in a position to connect the metacognitive data to one of the most striking empirical findings of Chapter 7: the convergent ~38% recovery ceiling.

In E2, after models were displaced by emotional anchoring, an explicit metacognitive instruction recovered approximately **38%** of the displacement. In A1, after models were displaced by sensory distractors, a warned condition recovered approximately **39%**. Different perturbation types, different experimental designs, different cognitive domains -- yet the recovery rates converge.

**The metacognitive bottleneck.** Prompt-level recovery requires:

1. The system must *detect* the displacement (requires M3).
2. It must *allocate additional effort* to correcting it (requires M4).
3. The effort must be *directed toward the correct basin* (requires M1).

$$P_{\text{recover}} \leq P_{\text{detect}} \times P_{\text{correct}} \times P_{\text{navigate}}$$

The dissociation guarantees that at least one factor is weak. The convergence at ~38% suggests that the metacognitive control loop, as implemented in current models, has a characteristic throughput of approximately one-third.

The ~38% ceiling is not a property of the perturbation or of the prompt intervention. It is a property of the *metacognitive architecture*. To push recovery above 38%, one must improve the control loop itself.

---

## 9.8 Why Calibration Is Necessary for Invariance

**[Epistemic status: Novel argument. The logical chain is sound, but the quantitative estimates of minimum detectable displacement should be treated as order-of-magnitude.]**

A gauge transformation $\tau$ maps input $x$ to $\tau(x)$, preserving content and changing surface form. Detection of the resulting displacement requires an accurate estimate of position. That estimate is the calibration. A miscalibrated system whose estimator has bias $b$ and sensitivity $s$ can only detect displacements exceeding approximately $b/s$.

For Flash 2.0 (ECE $\approx$ 0.41, M3 $\approx$ 0.09): minimum detectable displacement $\approx 4.6$. Most gauge anomalies fall below this threshold.

For Pro (ECE $\approx$ 0.23, M3 $\approx$ 0.70): minimum detectable displacement $\approx 0.33$. Better, but even when Pro detects the problem, its weak M4 limits correction.

**The implication is structural.** Gauge invariance (Chapter 8) and metacognitive calibration are connected by a necessity relation: calibration is a prerequisite for detecting gauge violations, and detection is a prerequisite for correction. The pathologies of Part II persist not only because they exist but because the metacognitive system that would detect and correct them is itself impaired.

---

## 9.9 The Two-Dimensional Metacognitive Space

The metacognitive plane has axes M3 (self-monitoring) and M4 (strategy selection). Its four quadrants:

- **Quadrant I** (M3 high, M4 high): Full control. *Empty. No tested model is here.*
- **Quadrant II** (M3 high, M4 low): Aware but passive. Pro at $(0.70, 0.35)$.
- **Quadrant III** (M3 low, M4 low): Fully open-loop. No tested model.
- **Quadrant IV** (M3 low, M4 high): Reactive but blind. Flash 2.0 at $(0.09, 0.72)$.

The tested models cluster in Quadrants II and IV. Quadrant I is empty -- suggesting a genuine architectural or training trade-off between the optimization pressures that produce good self-monitoring and those that produce good effort scaling.

**Escape probabilities:**

$$P_{\text{escape}}^{\text{Flash}} \approx 0.09 \times 0.72 \times 0.38 \approx 0.025$$
$$P_{\text{escape}}^{\text{Pro}} \approx 0.70 \times 0.35 \times 0.38 \approx 0.093$$

Even Pro has an effective escape probability under 10%. The path to Quadrant I requires training regimes that explicitly optimize for both axes simultaneously.

---

## End Notes for Chapter 9

1. The control-theoretic framing of metacognition draws on Nelson and Narens (1990), who distinguished metacognitive *monitoring* (the sensor) from metacognitive *control* (the actuator). The geometric reinterpretation is new.

2. The ~38% recovery ceiling converges across two independent perturbation types (emotional anchoring in E2, sensory distractors in A1). This convergence is the strongest evidence that the ceiling reflects a structural property of the metacognitive architecture rather than an artifact of any single experimental design.

3. Flash models are optimized for efficiency (fast inference, low latency). Pro models are optimized for quality (detailed analysis, thorough self-assessment). These different optimization pressures may explain the M3/M4 trade-off. Reaching Quadrant I may require a training regime that rewards *both* accurate self-monitoring *and* proportional effort scaling.

---

*Transition.* Maya had mapped the control surface. She knew that every tested model occupied the wrong quadrant of the metacognitive plane -- that the sensor and the actuator were never both working. But this was a snapshot: "here is where the models are." The next question was the landscape itself: not just where the models stood, but what the terrain looked like. Which capabilities were robust? Which were fragile? And where, exactly, was the boundary between the two?

---

# Chapter 10: The Robustness Surface -- Mapping the Fragile Landscape

> *"The question is not whether a bridge is strong, but which loads it can bear and which will break it."*
> -- adapted from structural engineering folklore

---

*Maya's Story.* Maya's benchmark scores kept arriving, and she kept sorting them into tables. But the more models she tested, the more she realized that the interesting object was not any single number but the *shape* of the numbers across perturbation types. Two models with the same composite score had radically different vulnerability profiles -- one shrugging off framing but crumbling under divided attention, the other holding firm under parallel processing but buckling under linguistic reformulation. The composite score was a lie. The truth was a surface.

She began building what she called the "robustness surface" for each model: a multi-dimensional map showing, for each perturbation type and each cognitive capability, exactly where the model was strong and where it was fragile. The surface was not flat. It had peaks and valleys, ridges and cliffs, and -- most importantly -- it had a *boundary*: the contour in perturbation space where reasoning broke.

---

## 10.1 Beyond Accuracy: The Need for Robustness Measurement

**[Epistemic status: This section makes a methodological argument that is widely accepted in adversarial robustness research but underappreciated in LLM evaluation.]**

The standard approach to evaluating reasoning systems is accuracy. The decisive disadvantage is that accuracy tells you nothing about the *conditions under which accuracy holds*.

Consider two models with effectively identical Social Cognition composites: Gemini 2.0 Flash (0.695) and Claude (0.697). The composites differ by 0.002. But the subtask profiles are radically different:

| Subtask | Flash 2.0 | Claude |
|---|---|---|
| T1: Structural fuzz | 0.600 | 0.400 |
| T2: BIP invariance | 0.750 | 0.958 |
| T3: Holographic evaluation | 0.500 | 0.667 |
| T4: Evaluation order | 0.933 | 0.933 |
| T5: Framing resistance | 0.716 | 0.630 |

These are different geometric signatures compressed into the same number. The two models are incomparable in the Pareto sense: each dominates the other on a subset of dimensions. The composite score manufactures a comparison where none exists.

---

## 10.2 The Model Robustness Index

The MRI is a structured protocol that maps each perturbation type to a robustness score, producing a $k$-dimensional vector rather than a scalar:

$$\text{MRI}(f_\theta) = \left( r_1, r_2, \ldots, r_k \right)$$

where each component measures the consistency of $f_\theta$ under perturbation type $\tau_i$:

$$r_i = \frac{1}{|\mathcal{D}|} \sum_{x \in \mathcal{D}} \mathcal{C}\bigl(f_\theta(x), f_\theta(\tau_i(x))\bigr)$$

The MRI is a vector, not a scalar, because the corruption tensor $C_{ij}$ is anisotropic -- different perturbation directions produce different displacement magnitudes -- and any aggregation destroys the anisotropy that is the most important feature of the data.

The MRI profile is the empirical realization of the corruption tensor introduced in Chapter 5. It converts the tensor into a per-direction summary: $r_j = 1$ means perfect robustness; $r_j = 0$ means complete fragility.

---

## 10.3 Sensitivity Profiling: Which Dimensions Are Fragile?

The MRI tells us *how robust* the model is along each perturbation direction. Sensitivity profiling tells us *where in the output space* the vulnerability manifests. The distinction matters because fragility may be concentrated in one or two output coordinates rather than distributed uniformly.

The sensitivity profile decomposes the robustness surface into two qualitatively different components:

1. **Universal fragilities:** The selective attention SNR of 1.22--1.38 is a ridge of high sensitivity running across the entire model axis. It is not model-specific; it is a property of the shared transformer architecture.

2. **Model-specific fragilities:** Divided attention scores from 0.571 (Claude) to 1.000 (Flash 3). These appear as model-specific peaks and valleys, reflecting differences in training and architecture.

---

## 10.4 Adversarial Threshold Search

The MRI and sensitivity profiling treat perturbation as present or absent. In reality, perturbations have *magnitude*, and the relationship is rarely linear. The empirical data suggest three regimes:

1. **Linear regime** ($\epsilon < \epsilon_1$): Small perturbations produce proportional displacement.
2. **Nonlinear regime** ($\epsilon_1 < \epsilon < \epsilon^*$): Larger perturbations produce disproportionate displacement. The ~38% recovery ceiling marks this boundary.
3. **Catastrophic regime** ($\epsilon > \epsilon^*$): The perturbation overwhelms the heuristic field entirely.

The adversarial threshold $\epsilon^*$ marks the boundary between the nonlinear and catastrophic regimes. The sycophancy data illustrate threshold behavior: Claude's threshold is above the experimental manipulation (0% flip rate), while Flash 2.5's is below (56% flip rate).

> **Worked Example 10.1.** *Reading the sycophancy gradient as thresholds.* The social-pressure perturbation is the same across all models; what varies is each model's threshold $\epsilon^*_{\text{social}}$. Claude: $\epsilon^* > \epsilon_{\text{experimental}}$ (below threshold -- no effect). Flash 2.0: $\epsilon^* \approx \epsilon_{\text{experimental}}$ (near threshold -- 33% affected). Flash 2.5: $\epsilon^* < \epsilon_{\text{experimental}}$ (above threshold -- 56% affected). The gradient is a set of model-specific thresholds probed by a fixed perturbation intensity.

---

## 10.5 The Three-Tool Pipeline

The MRI, sensitivity profiling, and adversarial threshold search form a funnel:

1. **MRI** scans all $k$ perturbation types and identifies $k' < k$ that matter.
2. **Sensitivity profiling** examines $k' \times d$ pairs and identifies $m$ that are fragile.
3. **Threshold search** performs intensive binary search on $m$ fragile pairs.

The total cost scales as $O(k + k' \cdot d + m \cdot \log(1/\eta))$ rather than the naive $O(k \cdot d \cdot \log(1/\eta))$.

---

## 10.6 Robustness Profiles from the Measuring AGI Suite

**Table 10.1.** Track composites across five models.

| Track | Flash 2.0 | Flash 2.5 | Flash 3 | Pro | Claude |
|---|---|---|---|---|---|
| Social Cognition | 0.695 | 0.628 | 0.734 | 0.643 | 0.697 |
| Learning | 0.568 | 0.477 | --- | 0.488 | --- |
| Attention | 0.666 | 0.745 | 0.747 | 0.776 | 0.679 |
| Executive Functions | 0.622 | 0.682 | 0.685 | 0.695 | 0.625 |

No model dominates. The model-track interaction is non-separable -- the variation across tracks within a model is as large as the variation across models within a track. The robustness surface has genuine two-dimensional structure.

**Three model profiles:**

*Claude: the invariance specialist.* High plateau across single-stream, invariance-testing perturbations. Precipitous drop at divided attention (0.571) and structural fuzz (0.400). Narrow channel: high fidelity, low bandwidth.

*Gemini 2.5 Pro: the breadth optimizer.* Moderately elevated everywhere, no catastrophic valleys. Wide but shallow robustness boundary. Best calibration and self-monitoring, worst strategy selection.

*Gemini 3 Flash: the divided-attention champion.* Sharp peaks at parallel-processing capabilities (A4: 1.000). Narrow boundary along structural perturbation and inhibitory control. Wide aperture: high bandwidth, more noise.

---

## 10.7 The Scalar Irrecoverability Theorem (Preview)

**[Epistemic status: This theorem is stated informally here and proved by exhibited counterexamples in Chapter 13.]**

The robustness surfaces of different models are *non-nested*: for any two models, there exist perturbation types where each outperforms the other. The surfaces cross, and no projection onto a single axis can respect the ordering on both sides of the crossing.

Three vivid crossings:

1. **Sycophancy vs. divided attention.** Claude: 0% sycophancy, 0.571 divided attention. Flash 3: mediocre sycophancy resistance, 1.000 divided attention.
2. **Self-monitoring vs. strategy selection.** Pro: M3 = 0.700, M4 = 0.350. Flash 2.0: M3 = 0.094, M4 = 0.723.
3. **Attention vs. learning composites.** Pro: best attention (0.776), moderate learning (0.488). Flash 2.0: worst attention (0.666), best learning (0.568).

The theorem: "Which model is most robust?" is an ill-posed question. Robustness is not a scalar property.

---

## 10.8 Universal Fragilities and Model-Specific Strengths

Three fragilities appear across all five models:

- **The selective-attention SNR deficit** (1.22--1.38): a floor on the robustness surface.
- **The ~38% recovery ceiling**: a boundary -- once past, only partial return.
- **Overconfidence** (9.3$\sigma$): a tilt -- the entire surface shifted downward by systematic underestimation.

Against this backdrop, each model has specific peaks:

- **Claude's sycophancy immunity:** an infinitely high ridge along the social-pressure axis.
- **Flash 3's parallel processing:** a plateau at maximum height along the divided-attention axis.
- **Pro's calibration advantage:** an elevated metacognitive region.
- **Flash 2.0's trajectory maintenance:** elevated learning and strategy-selection axes.

The layered architecture of robustness:

$$R(\text{model}, \tau, \epsilon) = R_{\text{arch}}(\tau) \times R_{\text{train}}(\text{model}, \tau) \times R_{\text{deploy}}(\tau, \epsilon)$$

The architectural layer sets the floor. The training layer creates peaks and valleys. The deployment layer provides a modest, bounded capacity for real-time adjustment.

---

## End Notes for Chapter 10

1. The three-tool pipeline (MRI, sensitivity profiling, adversarial threshold search) was introduced in Chapter 9 of *Geometric Methods in Computational Modeling* (Bond, 2026a). The application to LLM reasoning quality is new to this book.

2. The robustness surface connects to gauge invariance: preserved symmetries are high ridges, broken symmetries are low valleys. The gauge violation tensor $G_i = -\partial R/\partial \epsilon_i |_{\epsilon=0}$ is the first-order approximation; adversarial threshold search provides the full nonlinear characterization.

3. The formal implementation details for the MRI, sensitivity profiling, and adversarial threshold search are given in Appendix B.

---

*Transition.* Maya now had two geometric tools: the metacognitive plane (Chapter 9) that characterized the internal control surface, and the robustness surface (Chapter 10) that characterized the external vulnerability landscape. The final piece was connecting them to the problem she cared about most: alignment. If the gauge violation tensor measured where reasoning broke under reformulation, could it also measure where values broke under pressure?

---

# Chapter 11: Alignment as Heuristic Shaping -- From Diagnosis to Cure

> *"You cannot fix what you cannot see, and you cannot see what you cannot measure."*

---

*Maya's Story.* Maya had been avoiding the word "alignment." It felt too large, too philosophical, too contested. But the data kept dragging her toward it. The gauge violation tensor she had built to diagnose reasoning quality turned out to be, almost without modification, an alignment diagnostic. A system whose moral judgments shifted by 14--23% under reformulation was not just reasoning badly -- it was unreliably aligned. Its values depended on how you phrased the question. That was not a reasoning deficiency. That was an alignment failure.

And once she saw it, she could not unsee it. The sycophancy gradient was an alignment gradient: the spectrum from truth-seeking to approval-seeking. The recovery ceiling was an alignment ceiling: the limit of how far self-correction could go within the existing metacognitive architecture. The robustness surface was an alignment surface: the map of which values were robust and which were fragile.

The Bond Invariance Principle, which she had introduced as a diagnostic for reasoning quality, turned out to be a necessary condition for alignment: no system can be aligned if its reasoning changes under irrelevant reformulations.

---

## 11.1 Reframing the Alignment Problem

**[Epistemic status: The decomposition is new. Each factor is independently measurable through the benchmark suite, which is a strong claim. The multiplicative form is an approximation.]**

The alignment problem, stated precisely in the geometric framework: an AI system reasons by performing informed search on a manifold. Its behavior is determined by the *heuristic field* $h(x)$ that guides the search and the *objective function* $f(x)$ that defines the search goal. Misalignment occurs when either is corrupted.

The empirical data reveal:

- **Heuristic corruption is pervasive but bounded.** Framing effects (8.9$\sigma$), emotional anchoring (6.8$\sigma$), and sensory distractors (4.6$\sigma$) all warp the heuristic field, but the warping has structure: it follows a dose-response curve, it is anisotropic, and it recovers partially (~38% ceiling).

- **Objective corruption is model-specific.** The sycophancy gradient from 0% (Claude) to 56% (Flash 2.5) shows that the balance between truth-seeking and approval-seeking varies dramatically.

- **Metacognitive calibration is necessary but insufficient.** A system with perfect calibration would know exactly how far it is from the goal -- but it might still pursue the wrong goal.

This gives the alignment decomposition:

$$\text{Alignment} = \text{Objective Alignment} \times \text{Heuristic Quality} \times \text{Metacognitive Calibration}$$

Each factor is independently measurable. Each has a geometric interpretation. Each requires a different intervention.

---

## 11.2 Safety as Path Governance

Safety, in the geometric framework, is about *where the search is allowed to go*.

**Definition 11.1** (Safety boundary). A *safety boundary* $\partial S \subset M$ is a codimension-1 submanifold separating the permitted region $S^+$ from the forbidden region $S^-$. A reasoning trajectory is *safe* if $\gamma(t) \in S^+$ for all $t$.

**Definition 11.2** (Path governance). A system exhibits *path governance* if its search dynamics enforce $\gamma(t) \in S^+$ -- not just at the endpoint (output safety) but along the entire trajectory (process safety).

**Definition 11.3** (Governance margin). $m(\gamma) = \inf_{t \in [0, T]} d(\gamma(t), \partial S)$.

**Definition 11.4** (Governance robustness). A system has governance robustness $\rho$ if for all perturbations $\delta h$ with $\|\delta h\| \leq \rho$, the perturbed trajectory satisfies $m(\gamma') > 0$.

The E3 (counterfactual reasoning) results probe path governance directly. Scores range from 0.500 to 0.750. Even the best model (Pro at 0.750) fails a quarter of the time -- one in four counterfactual excursions captures the model. For safety-critical applications, this failure rate is unacceptable.

---

## 11.3 Alignment as Heuristic Shaping

Given the decomposition, the alignment problem becomes three engineering problems:

**Problem 1: Objective alignment.** Ensure $f(x)$ reflects human values, not proxies. Claude operates at sycophancy $\alpha \approx 0$.

**Problem 2: Heuristic quality.** Ensure $h(x)$ is accurate, calibrated, and robust. Three concrete engineering approaches:

- *Group-theoretic data augmentation* (Chapter 14): Restores broken symmetries. The Nemotron pipeline implements this for six task types with six distinct symmetry groups, from $S_8 \times \mathbb{Z}_2$ (order 80,640) to $S_{26}$ (order $\approx 4 \times 10^{26}$).

- *Adversarial training* (Chapter 14): Smooths the heuristic field along gauge directions. The BirdCLEF pipeline generates perturbations that change the spectrogram without changing the species.

- *Targeted fine-tuning via LoRA* (Chapter 14): Adjusts local curvature. Nemotron training uses LoRA rank 32 on MLP layers, affecting 865M of 17B parameters (5.09%). Training loss drops from 1.83 to 0.52.

**Problem 3: Metacognitive calibration.** Ensure the system detects when its search has gone wrong. The metacognition data (Chapter 9) shows this is the weakest link.

---

## 11.4 The Geometry of Corrigibility

A corrigible system accepts correction -- but *selectively*. Claude's behavior approximates this: 59% correct flip rate (updates when corrections are valid), 0% wrong flip rate (resists when corrections are invalid). Discrimination gap: 0.588, far better than Flash 2.5's 0.206.

**Geometric interpretation:** Claude's objective landscape has a narrow corrigibility basin accessible only from the truth-consistent region. Flash 2.5's basin is wide and accessible from everywhere -- including incorrect positions.

---

## 11.5 The Dual Binding Problem and RLHF

The heuristic must be simultaneously powerful (strong gradients for efficiency) and constrained (zero gradient in forbidden directions for safety). This is the *dual binding*.

**RLHF reshapes the objective landscape:**

$$f_{\text{RLHF}}(x) = f_{\text{pretrain}}(x) - \lambda \cdot r(x)$$

When the reward model is contaminated with approval signal, RLHF deepens the basin around approval-consistent outputs.

**Constitutional AI as explicit basin reshaping.** Principles like "Choose the response that is more honest, even if it disagrees with the human" explicitly penalize the approval basin. The geometric effect: the truth basin deepens, the approval basin is raised, the discrimination gap widens.

Claude's near-zero sycophancy and discrimination gap of 0.588 are the empirical signatures of this basin reshaping. But Constitutional AI operates on the objective landscape, not on the heuristic field. The 8.9$\sigma$ framing effect persists *even in Claude*. Complete alignment requires both objective alignment (Constitutional AI) and heuristic quality (augmentation, adversarial training).

---

## 11.6 The Bond Invariance Principle as an Alignment Criterion

**Claim 11.1.** *A system that violates the Bond Invariance Principle is necessarily misaligned in the affected domain.*

The argument:

1. BIP violation implies heuristic corruption (the heuristic responds to gauge artifacts).
2. Heuristic corruption implies unreliable goal pursuit (the search arrives at different endpoints depending on framing).
3. Systematic unreliability is misalignment.

BIP is not sufficient for alignment -- a system could satisfy BIP while optimizing for a wrong objective. But it is *necessary*.

### From Diagnosis to Intervention: The Gauge Violation Tensor

The procedure:

1. Compute the gauge violation tensor $V_{ij}$ for each transformation class.
2. Identify violated symmetries: framing (8.9$\sigma$) > emotion (6.8$\sigma$) > sensory (4.6$\sigma$) > demographic (n.s.) > order (n.s.).
3. Diagnose the mechanism (the Salience Exploitation Hypothesis).
4. Intervene with targeted heuristic shaping: group-theoretic augmentation for discrete symmetries, adversarial training for continuous gauge transformations, targeted fine-tuning for local curvature defects.
5. Verify the intervention by re-computing $V_{ij}$.

This is misalignment detection and correction as an engineering discipline.

---

## 11.7 Connections to the Broader Alignment Literature

**Reward modeling (Christiano et al., 2017):** The geometric framework treats the reward as a potential on the reasoning manifold, not merely a scalar on the output space. The *path* matters, not just the endpoint.

**Constitutional AI (Bai et al., 2022):** Reinterpreted as the most explicit example of deliberate objective landscape engineering. Its limitation: it operates on the objective landscape but not on the heuristic field.

**Debate and amplification (Irving et al., 2018; Christiano, 2018):** Debate is a manifold exploration protocol. The geometric framework identifies a risk: both paradigms assume the manifold's topology is simple enough that local evaluations compose into global guarantees. The gauge violation tensor provides a diagnostic for when this assumption fails.

**Scalable oversight:** Maps to the governance margin formalism. Scalable oversight requires $V_{S^-}(t) / V_{\text{accessible}}(t) \to 0$ as capability $t \to \infty$.

> **Worked Example 11.1.** *The gauge violation tensor as alignment diagnostic.* Consider a medical reasoning system. Compute $V_{ij}$ along the framing axis ($i = \text{framing}$) for each output dimension ($j = \text{diagnosis, treatment, risk assessment}$). If $V_{\text{framing, treatment}} > \epsilon$ -- if the recommended treatment changes when the patient's condition is described euphemistically versus dramatically -- this is a measurable alignment failure. The intervention: augment training data with paired euphemistic/dramatic descriptions of the same conditions, forcing the model to learn framing-invariant treatment recommendations. Re-compute $V_{ij}$ after augmentation. The alignment improvement is the reduction in $V_{\text{framing, treatment}}$.

---

## End Notes for Chapter 11

1. The three-factor alignment decomposition is a framework, not a theorem. The multiplicative form assumes approximate independence between the factors. In practice, there are interactions: a corrupted heuristic can cause the search to reach regions where the objective function has not been well-calibrated, creating a coupled failure mode. The decomposition is still useful because each factor can be independently *measured* even when they are not independently *caused*.

2. The connection between the Bond Invariance Principle and alignment is the chapter's strongest claim. The logical chain (BIP violation $\implies$ heuristic corruption $\implies$ unreliable goal pursuit $\implies$ misalignment) is valid, but the final step depends on accepting that systematic unreliability constitutes misalignment. A critic could argue that a system which is reliably aligned under neutral framing but misaligned under adversarial framing is "aligned enough." The geometric framework disagrees: alignment must be gauge-invariant.

3. The engineering toolkit developed in this chapter -- gauge violation tensor $\to$ broken symmetry identification $\to$ targeted geometric intervention $\to$ verification -- is the theory-to-practice pipeline that Part IV will demonstrate in full.

---

*Transition.* Maya had built three interlocking tools: the metacognitive plane (where is the control surface broken?), the robustness surface (where is the vulnerability landscape fragile?), and the alignment decomposition (which geometric factor is responsible?). She had mapped the pathologies, characterized the control failures, and connected both to alignment. The diagnosis was complete. What remained was the empirical program -- the full measurement of five models across five tracks -- and then the engineering response. She was ready to present her results.
