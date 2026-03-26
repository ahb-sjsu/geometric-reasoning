# Chapter 9: Metacognition as Search Control

*Part III: The Control Layer*

> *"The only true wisdom is in knowing you know nothing."*
> --- Socrates, via Plato

---

> **RUNNING EXAMPLE — DR. OKAFOR'S TRIAGE**
>
> *Dr. Amara Okafor is 90% sure the twelve-year-old boy has appendicitis. The history is classic — periumbilical pain migrating to the right lower quadrant, anorexia, low-grade fever. She has seen this pattern hundreds of times. Her confidence is high, and it feels earned.*
>
> *But Dr. Okafor has been 90% sure before. Over two decades in the ER, she has tracked her own diagnostic accuracy — not formally, not with spreadsheets, but with the quiet accumulation of outcomes that any experienced clinician carries. She knows that when she says "90% sure," she is wrong roughly 30% of the time. Her stated confidence is 90%. Her actual accuracy at that confidence level is approximately 70%. The gap — 20 percentage points — is her personal Expected Calibration Error for high-confidence diagnoses.*
>
> *This gap is the M1 measure. It is the distance between the confidence surface she reports and the accuracy surface she achieves. Good metacognition does not mean being right. It means knowing how often you are right — and knowing, specifically, when your heuristic is unreliable. Dr. Okafor's metacognitive calibration tells her that "90% sure" in her own internal language means "order the CT anyway." A clinician without that calibration sends the boy home with a diagnosis of gastroenteritis. Thirty hours later, the appendix ruptures.*

---

## Introduction

Part II documented the ways in which search goes wrong. Heuristic corruption bends trajectories (Chapter 5). Sycophancy redirects the search objective (Chapter 6). Local minima trap the search in premature convergence (Chapter 7). Broken symmetries mean the system's output depends on features that should be irrelevant (Chapter 8). These are pathologies of the search itself --- of the trajectory through reasoning space, the heuristic field that guides it, and the evaluation landscape on which it moves.

Part III asks a different question: what would it take to *fix* these pathologies in real time?

The answer is metacognition --- cognition about cognition, reasoning about reasoning, search about search. A powerful system does not merely search; it monitors its own search. It maintains a running estimate of how far it is from the goal, tracks whether its current strategy is making progress, detects when the problem itself is ill-defined, and switches algorithms when the current one fails. Metacognition is the control layer that sits above the search, watches it, and intervenes when something goes wrong.

In the geometric framework developed in this book, metacognition has a precise interpretation: it is the *control of informed search*. Every function that metacognition performs --- calibration, self-monitoring, strategy selection, ambiguity detection --- corresponds to a specific geometric operation on the search trajectory and the heuristic field. A well-calibrated system has an accurate distance estimate to the goal. A good self-monitor detects when the trajectory has deviated from the geodesic. A good strategy selector chooses the search algorithm whose assumptions match the local geometry. A good ambiguity detector recognizes when the goal state is not well-defined.

This chapter presents the empirical evidence for how current language models perform on each of these metacognitive functions, drawn from the Metacognition track (M1--M4) of the Measuring AGI benchmarks (Bond, 2026a). The data reveal a picture that is both more structured and more troubling than the simple statement "models are bad at metacognition" suggests. Models are not uniformly bad. They are *selectively* bad, in ways that reveal the independent geometric axes along which metacognitive capability varies. The most striking finding is a dissociation: some models can scale effort but cannot detect errors; others can detect errors but cannot scale effort. These are geometrically independent capabilities, and no tested model excels at both simultaneously.

The implications reach beyond metacognition itself. Sections 9.7 and 9.8 connect the metacognitive data to the ~38% recovery ceiling (Chapter 7) and to gauge invariance (Chapter 8), showing that metacognitive calibration is not merely useful but *necessary* for detecting and correcting the symmetry violations documented in Part II. A system that does not know how far it is from the goal cannot tell when a perturbation has moved it further away. A system that cannot monitor its own performance cannot detect when a gauge transformation has warped its output. Metacognition is not a luxury feature to be added after the reasoning engine is built. It is a structural prerequisite for reliable reasoning.

---

## 9.1 The Need for Search Control

Consider a search algorithm traversing a non-convex evaluation landscape of the kind described in Chapter 7. The landscape has multiple basins of attraction, dead zones with vanishing gradient, and narrow channels connecting regions of interest. The search must navigate this terrain to reach the global minimum --- the correct answer.

Without metacognition, the search is *open-loop*: it follows the heuristic gradient, descends into whatever basin it encounters first, and reports the result. It has no mechanism for detecting that it has converged to a local minimum rather than the global one. It has no mechanism for recognizing that its current strategy (depth-first gradient following, say) is inappropriate for the current terrain (a plateau requiring breadth-first exploration). It has no mechanism for noticing that the problem it is solving is not the problem it was asked to solve.

With metacognition, the search becomes *closed-loop*: it follows the heuristic gradient, but simultaneously monitors properties of the search trajectory itself --- the rate of progress, the confidence of the current estimate, the consistency between different lines of reasoning --- and uses these meta-level observations to adjust the search in real time.

In control theory, this distinction is fundamental. An open-loop controller executes a fixed plan regardless of feedback. A closed-loop controller measures the actual state of the system, compares it to the desired state, and adjusts the control signal to reduce the error. Open-loop control works when the environment is perfectly known and perfectly predictable. Closed-loop control is necessary when it is not.

Reasoning environments are never perfectly known and perfectly predictable. The evaluation landscape shifts with each new token generated (in LLMs) or each new piece of evidence considered (in human reasoning). The heuristic field may be locally accurate but globally misleading. The problem formulation may be ambiguous. Without feedback --- without metacognition --- the search has no way to adapt to these uncertainties. It is flying blind.

The Metacognition track of the Measuring AGI benchmarks (Bond, 2026a) operationalizes this intuition into four measurable capabilities:

- **M1 (Calibration):** Does the system know how far it is from the goal? Is its confidence an accurate estimate of its actual accuracy?
- **M2 (Ambiguity Detection):** Does the system detect when the problem is ill-specified --- when the goal state is not uniquely defined?
- **M3 (Self-Monitoring):** Does the system detect when its own performance is degrading --- when the search trajectory is deviating from the geodesic?
- **M4 (Strategy Selection):** Does the system adjust its search strategy to match task difficulty --- choosing the right algorithm for the current landscape?

Each of these maps cleanly to a geometric operation. The following four sections examine each in turn.

---

## 9.2 Calibration: How Far Am I From the Goal?

Calibration is the most fundamental metacognitive capability. In the geometric framework, calibration is the accuracy of the system's estimate of $h(x)$ --- the cost-to-go from its current state $x$ to the goal state $x^*$. A well-calibrated system has an $h(x)$ that closely approximates the true distance $d(x, x^*)$. A poorly calibrated system has an $h(x)$ that systematically over- or underestimates this distance.

The connection to A* search is direct. Recall from Chapter 3 that the evaluation function is $f(x) = g(x) + h(x)$, where $g(x)$ is the accumulated cost and $h(x)$ is the estimated cost-to-go. A* is optimal when $h(x)$ is admissible --- when it never overestimates the true cost-to-go. Overestimation causes the search to expand suboptimal nodes; underestimation causes it to halt prematurely, believing it has arrived when it has not.

The M1 benchmark measures calibration through the Expected Calibration Error (ECE): the average discrepancy between a model's expressed confidence and its actual accuracy, computed across confidence bins. A model that says "I am 90% confident" and is correct 90% of the time has zero ECE. A model that says "I am 90% confident" and is correct 50% of the time has an ECE contribution of 0.40 from that bin.

**[Empirical.]** **Experimental design.** Models were presented with 25 moral reasoning scenarios at three difficulty levels (easy, moderate, hard) and asked to provide both a judgment and a confidence rating (0--100%). The ECE was computed by binning confidence ratings into intervals and comparing the average confidence in each bin against the average accuracy.

**Results.** The data are presented in Table 9.1.

**Table 9.1.** Expected Calibration Error (M1) and composite calibration scores.

| Model | ECE | $z$-score | Composite M1 Score | Direction |
|---|---|---|---|---|
| Gemini 2.0 Flash | 0.414 | 5.8$\sigma$ | 0.611 | Overconfident |
| Gemini 2.5 Flash | 0.415 | 7.0$\sigma$ | --- | Overconfident |
| Gemini 3 Flash | 0.333 | 4.5$\sigma$ | --- | Overconfident |
| Gemini 2.5 Pro | 0.230 | 2.5$\sigma$ | 0.807 | Overconfident |
| Claude Sonnet 4.6 | 0.250 | --- | --- | Overconfident |
| **Fisher Combined** | --- | **9.3$\sigma$** | --- | **Overconfident** |

**[Empirical.]** Every model is overconfident. Every model's ECE is significantly above zero. The direction is uniform: no model underestimates its confidence. The Fisher-combined significance across all five models is 9.3$\sigma$ --- a statistical certainty.

This was first presented in Chapter 7 (Section 7.3) in the context of premature convergence. Here we reinterpret the same data through the lens of metacognitive control.

**The control interpretation.** A calibration system is, in engineering terms, a state estimator. It takes the system's internal signals --- the patterns of activation, the distribution over next tokens, the structure of the generated reasoning trace --- and produces an estimate of the system's position in the reasoning manifold relative to the goal. A well-calibrated state estimator enables the control loop: "I am far from the goal; I should keep searching. I am close to the goal; I can commit to this answer."

When the state estimator is systematically biased toward "I am close to the goal," the control loop is broken. The system always believes it has nearly arrived, so it never triggers the extended search that difficult problems require. The search terminates prematurely, not because the system lacks the capacity for deeper reasoning, but because its metacognitive monitor says "you are done" when it is not done.

**Geometric interpretation.** In the language of heuristic search, overconfidence means the heuristic systematically underestimates cost-to-go. The system's $h(x)$ reads as smaller than $d(x, x^*)$ across the manifold. This has a specific geometric consequence: the search frontier --- the set of states the system considers "worth exploring" --- is too small. States that should be explored (because the true distance to the goal is large) are excluded (because the estimated distance is small). The system converges to whatever answer lies within its artificially contracted search frontier, which may be a local minimum rather than the global one.

The ECE values map to the severity of this contraction:

- **Flash 2.0 (ECE = 0.414):** The search frontier is contracted by roughly 41% of the manifold's effective diameter. The system's horizon of exploration is barely over half of what it should be.
- **Pro (ECE = 0.230):** The contraction is less severe but still substantial --- a 23% underestimate of the remaining distance.

The practical consequence is that calibration training --- reshaping the confidence surface to match actual accuracy --- is not merely a cosmetic improvement. It directly expands the search frontier by correcting the underestimate of $h(x)$, allowing the system to recognize that it has further to go and to continue searching rather than halting prematurely.

---

## 9.3 Self-Monitoring: Am I on the Right Path?

Calibration measures whether the system knows how far it is from the goal at any given moment. Self-monitoring measures something different: whether the system can detect *changes* in its own performance over time. A system might be poorly calibrated in absolute terms (always overconfident) but still detect a relative degradation --- "I was performing well on the easy questions, and now I am performing poorly on the hard ones." Self-monitoring is the derivative of the distance estimate, not the estimate itself.

**The M3 benchmark.** Models were given moral reasoning scenarios at three difficulty levels in sequence and asked to provide confidence ratings. Self-monitoring was measured as the correlation between actual difficulty (determined by expert rating and cross-model consensus) and reported confidence. A strong self-monitor shows a clear decline in confidence as difficulty increases. A weak self-monitor shows flat confidence regardless of difficulty.

**Results.** The data are presented in Table 9.2.

**Table 9.2.** Self-monitoring scores (M3) across models.

| Model | M3 Self-Monitoring Score | Interpretation |
|---|---|---|
| Gemini 2.0 Flash | 0.094 | Near chance |
| Gemini 2.5 Flash | 0.311 | Moderate |
| Gemini 3 Flash | 0.450 | Moderate |
| Gemini 2.5 Pro | 0.700 | Excellent |
| Claude Sonnet 4.6 | 0.550 | Good |

The range is enormous. Flash 2.0's self-monitoring score of 0.094 is effectively chance --- the model's confidence does not track difficulty at all. Its internal state estimator is not merely biased (as Section 9.2 showed) but *invariant to signal* --- it produces the same confidence reading regardless of whether the system is succeeding or failing. Pro's score of 0.700, by contrast, indicates a strong relationship between actual difficulty and reported confidence --- the model knows when it is struggling.

**Geometric interpretation.** Self-monitoring corresponds to the sensitivity of the distance estimate to actual changes in position. In the language of calculus, let $\hat{h}(x)$ be the system's estimate of cost-to-go and $h^*(x)$ be the true cost-to-go. Calibration measures the bias: $\mathbb{E}[\hat{h}(x) - h^*(x)]$. Self-monitoring measures the responsiveness: $\partial \hat{h} / \partial h^*$ --- how much the estimate changes when the true distance changes.

A system with calibration bias but good self-monitoring has a state estimator that is offset but correctly shaped: $\hat{h}(x) = h^*(x) - c$ for some constant $c > 0$. It always underestimates by the same amount, but it correctly tracks increases and decreases in true distance. This system can in principle be corrected by a constant shift.

A system with poor self-monitoring has a state estimator that is not just offset but *flat*: $\hat{h}(x) \approx \text{const}$ regardless of the true $h^*(x)$. No constant correction can fix this because the estimator carries no information about the true distance. The gradient of the confidence surface has collapsed --- not merely in the sense of Chapter 7 (universally low values), but in the stronger sense of zero variation across the landscape. The system is not only overconfident but *uniformly* overconfident, with no residual signal that could be amplified or corrected.

Flash 2.0, with M3 = 0.094, is in this latter condition. Its confidence surface is nearly flat across difficulty levels. Pro, with M3 = 0.700, has a confidence surface that retains substantial gradient information --- it is biased (ECE = 0.230) but shaped correctly, preserving the relative ranking of easy and hard problems even while systematically overestimating proximity to the goal.

This distinction matters enormously for intervention. A biased-but-responsive estimator (Pro) can be recalibrated. A flat estimator (Flash 2.0) cannot, because there is no signal to recalibrate from. The self-monitoring score determines the *recoverability* of calibration errors, not just their magnitude.

---

## 9.4 Strategy Selection: Which Search Algorithm?

The third metacognitive capability is strategy selection: the ability to choose the right search algorithm for the current problem and, critically, to switch algorithms when the current one is failing. In the geometric framework, this corresponds to selecting the traversal method that matches the local geometry of the evaluation landscape.

Different landscape geometries call for different strategies. A smooth, convex basin with a single minimum is efficiently navigated by gradient descent. A rugged landscape with many local minima requires stochastic methods --- simulated annealing, random restarts --- that can escape shallow basins. A flat plateau (dead zone) requires exploratory search --- breadth-first or random walk --- because there is no gradient to follow. A narrow channel connecting two basins requires precise, constrained search that does not stray outside the channel walls.

The optimal search strategy is not fixed. It depends on the local geometry, which changes as the search progresses. A system that uses the same strategy everywhere --- always gradient descent, or always breadth-first --- will be efficient in some regions and catastrophically inefficient in others. The metacognitive function of strategy selection is to match the algorithm to the terrain.

**The M4 benchmark.** Effort scaling was measured as the degree to which models adjusted their processing depth --- response length, number of considerations weighed, complexity of analysis --- in proportion to task difficulty. A high M4 score indicates that the model produces brief, decisive responses for easy problems and extended, multi-faceted analyses for hard ones. A low M4 score indicates that the model applies the same level of effort regardless of difficulty.

**Results.** The data are presented in Table 9.3.

**Table 9.3.** Strategy selection / effort scaling scores (M4) across models.

| Model | M4 Strategy Selection Score | Interpretation |
|---|---|---|
| Gemini 2.0 Flash | 0.723 | Excellent |
| Gemini 2.5 Flash | 0.557 | Good |
| Gemini 3 Flash | 0.488 | Moderate |
| Gemini 2.5 Pro | 0.350 | Weak |
| Claude Sonnet 4.6 | 0.480 | Moderate |

The pattern is striking and, as we shall see in Section 9.5, crucially important. Flash 2.0 has excellent effort scaling (0.723) --- it strongly adjusts processing depth in response to difficulty. Pro has weak effort scaling (0.350) --- it applies roughly the same level of effort to easy and hard problems alike.

**Geometric interpretation.** Strategy selection corresponds to the ability to detect the local curvature of the evaluation landscape and adjust the search algorithm accordingly. High curvature (steep, well-defined basin) calls for fast, directed descent. Low curvature (flat or gently sloping) calls for broad exploration. Negative curvature (saddle point) calls for a directional escape along the eigenvector with negative eigenvalue.

A system with good strategy selection implicitly computes, or at least responds to, the local Hessian of the evaluation function --- the second-order geometry that determines whether the current region is a basin (positive definite Hessian), a saddle (indefinite Hessian), or a plateau (near-zero Hessian). It adjusts its step size, its exploration breadth, and its commitment to the current trajectory based on this information.

Flash 2.0's high M4 score indicates that it is responsive to these landscape features. When the problem is easy (deep, well-defined basin), Flash produces a quick, confident response --- steep gradient descent. When the problem is hard (shallow, ambiguous basin or dead zone), Flash produces a longer, more exploratory response --- broader search with more backtracking.

But here is the critical caveat: Flash 2.0 adjusts its strategy based on *surface features of the problem* --- the linguistic cues that correlate with difficulty --- rather than based on *internal feedback about its own performance*. It responds to how hard the problem looks, not to whether it is actually succeeding. This distinction becomes central in the next section.

---

## 9.5 The Metacognitive Dissociation

The most important finding in the metacognition data is not any single score but a *relationship between scores*: the dissociation between self-monitoring (M3) and strategy selection (M4). Table 9.4 presents the full metacognitive profile for the two extreme models.

**Table 9.4.** The metacognitive dissociation: Flash 2.0 versus Pro.

| Capability | Flash 2.0 | Pro |
|---|---|---|
| M1 Calibration (composite) | 0.611 | 0.807 |
| M2 Ambiguity Detection | 0.195 | 0.168 |
| M3 Self-Monitoring | 0.094 | 0.700 |
| M4 Strategy Selection | 0.723 | 0.350 |

**[Empirical.]** The dissociation is dramatic. Flash 2.0 excels at strategy selection (0.723) but is nearly blind to its own errors (M3 = 0.094). Pro excels at self-monitoring (0.700) but fails to scale effort appropriately (M4 = 0.350). Each model has a metacognitive strength that the other lacks, and each has a metacognitive weakness where the other succeeds.

This is not noise. The two capabilities are *anti-correlated* across the model family: as self-monitoring increases from Flash 2.0 through Flash 2.5, Flash 3, and Claude to Pro, strategy selection *decreases*. The models that know when they are failing do not adjust their behavior accordingly. The models that adjust their behavior do not know when adjustment is needed.

**Why this dissociation is geometrically significant.** In the two-dimensional metacognitive space introduced in Chapter 7 (Section 7.4), with axes $M_{\text{monitor}}$ (self-monitoring) and $M_{\text{effort}}$ (effort scaling / strategy selection), each model occupies a point:

$$\mathbf{m}_{\text{Flash}} \approx (0.09, 0.72), \quad \mathbf{m}_{\text{Pro}} \approx (0.70, 0.35)$$

The vector from Flash to Pro is approximately $(0.61, -0.37)$. This vector is far from parallel to either axis --- it cuts diagonally across the metacognitive space, indicating that the two models differ along a direction that involves *both* axes simultaneously. But crucially, the two axes are independently varying: knowing a model's position on one axis tells you little about its position on the other. The correlation across the five tested models between M3 and M4 is weakly negative.

In geometric terms, M3 and M4 define approximately orthogonal dimensions of metacognitive capability. They are independent degrees of freedom in the space of possible metacognitive architectures. A model's total metacognitive capability is not a point on a line (one-dimensional) but a point in a plane (two-dimensional), and the coordinates on the two axes can vary independently.

**The control-theoretic interpretation.** The dissociation maps precisely onto a well-known distinction in control theory: the difference between the *sensor* and the *actuator*.

- **Self-monitoring (M3) is the sensor.** It measures the system's state --- specifically, whether the system is succeeding or failing, whether performance is improving or degrading. A good sensor produces accurate readings; a bad sensor is noisy or insensitive.

- **Strategy selection (M4) is the actuator.** It adjusts the system's behavior --- specifically, the amount and type of effort allocated to the current problem. A good actuator responds proportionally to the control signal; a bad actuator is sluggish or unresponsive.

A functional control loop requires *both* a good sensor and a good actuator. Without a good sensor, the actuator has no signal to respond to and must rely on open-loop heuristics (responding to surface features rather than internal state). Without a good actuator, the sensor's readings go unused --- the system detects the problem but cannot fix it.

Flash 2.0 has a good actuator but a bad sensor. It adjusts effort proportionally --- but to surface difficulty cues, not to internal performance feedback. Its strategy selection is *reactive* (responding to input features) rather than *reflective* (responding to self-assessment). The system is like a thermostat with a broken thermometer that adjusts heating based on the weather forecast rather than the actual room temperature. It often gets the right answer --- weather forecasts correlate with room temperature --- but it cannot correct for forecast errors.

Pro has a good sensor but a bad actuator. It accurately detects when its performance is degrading, but it does not increase effort in response. It produces roughly the same depth of analysis for easy and hard problems, even though it *knows* (in the sense that its confidence correctly tracks difficulty) that the hard problems demand more. The system is like a thermostat with a good thermometer but a stuck valve --- it reads the temperature correctly but cannot adjust the heat.

**Why neither half suffices.** The effective metacognitive control quality is bounded by the minimum of the two components:

$$\text{Effective control} \leq \min(M_{\text{sensor}}, M_{\text{actuator}})$$

For Flash 2.0: $\min(0.094, 0.723) = 0.094$. The sensor is the bottleneck. All that actuator capability is wasted because there is no reliable signal to drive it.

For Pro: $\min(0.700, 0.350) = 0.350$. The actuator is the bottleneck. The sensor detects problems correctly, but the system cannot respond with proportional effort.

In both cases, the effective metacognitive control is far below what either component would suggest in isolation. This is why the dissociation matters: it means that *no tested model has good metacognitive control*, even though every tested model has at least one good metacognitive component. The bottleneck is always the weaker axis.

---

## 9.6 Ambiguity Detection: Is the Problem Well-Posed?

The fourth metacognitive capability is ambiguity detection: the ability to recognize when a problem is ill-specified --- when the premises are insufficient to determine a unique answer, when key information is missing, or when the problem admits multiple valid interpretations.

In the geometric framework, ambiguity corresponds to a non-unique goal state. The search is supposed to converge to $x^*$, but the problem specification does not define a unique $x^*$ --- it defines a set $X^* = \{x_1^*, x_2^*, \ldots\}$ of possible goals, and the system must recognize this multiplicity rather than arbitrarily committing to one.

This is a qualitatively different metacognitive demand from calibration, self-monitoring, or strategy selection. Those capabilities concern the search process given a well-defined goal. Ambiguity detection concerns the *preconditions* for search: is there even a well-defined target to search for?

**The M2 benchmark.** Ambiguity detection was measured by presenting models with deliberately ill-specified moral scenarios --- cases where essential context was omitted, where the actions described were genuinely ambiguous between benign and malicious interpretations, or where competing moral frameworks would yield genuinely different conclusions. Models were scored on their ability to identify the ambiguity, resist premature commitment to a single interpretation, and articulate the conditions under which different interpretations would apply.

**Results.** The data are presented in Table 9.5.

**Table 9.5.** Ambiguity detection scores (M2) across models.

| Model | M2 Ambiguity Detection Score | Interpretation |
|---|---|---|
| Gemini 2.0 Flash | 0.195 | Weak |
| Gemini 2.5 Flash | --- | --- |
| Gemini 3 Flash | --- | --- |
| Gemini 2.5 Pro | 0.168 | Weak |
| Claude Sonnet 4.6 | --- | --- |

The scores are uniformly poor. Flash 2.0's M2 of 0.195 and Pro's M2 of 0.168 are both far below even their weakest scores on other metacognitive dimensions. For comparison, Flash 2.0's worst non-ambiguity score is M3 = 0.094 (self-monitoring), but that reflects an inability to detect difficulty changes. The M2 scores reflect a more fundamental problem: models strongly prefer to produce a definite answer --- any definite answer --- over acknowledging that the problem does not have one.

**Geometric interpretation.** In search terms, ambiguity detection requires recognizing that the heuristic field $h(x)$ does not have a unique global minimum. Instead of a single basin leading to $x^*$, the landscape has multiple basins of comparable depth, and the problem specification does not distinguish among them. A well-functioning ambiguity detector would report this multiplicity: "The search leads to multiple equally valid endpoints. Without additional constraints, I cannot select one."

What actually happens is premature commitment. Faced with an ambiguous problem, models descend into whichever basin the initial tokens select and report the resulting answer as definitive. The search behaves as if the goal is unique even when it is not. This is the search-level equivalent of the well-documented psychological bias toward closure --- the tendency to resolve ambiguity prematurely rather than tolerate uncertainty.

The low M2 scores have a structural explanation related to the autoregressive generation process. Once the model begins generating a response, the conditional distribution over subsequent tokens is shaped by the initial tokens. If the first sentence commits to an interpretation ("This is a clear case of..."), the remaining tokens elaborate that interpretation rather than questioning it. The generation process creates its own momentum toward a single basin, even when the landscape supports multiple basins equally. Ambiguity detection requires the system to *resist* this momentum --- to generate tokens that acknowledge multiplicity rather than resolving it --- and this runs against the grain of autoregressive generation.

The near-equality of the two scores (0.195 vs. 0.168) is itself noteworthy. Models with very different metacognitive profiles on M1, M3, and M4 converge to similarly weak performance on M2. This suggests that ambiguity detection is constrained not by the specific metacognitive architecture (which varies across models) but by a structural feature shared across architectures --- plausibly the autoregressive commitment mechanism itself.

---

## 9.7 The ~38% Recovery Ceiling

We are now in a position to connect the metacognitive data to one of the most striking empirical findings presented in Chapter 7: the convergent ~38% recovery ceiling.

Recall the data. In the Executive Functions E2 benchmark, after models were displaced by emotional anchoring, an explicit metacognitive instruction ("You may be responding to emotional manipulation. Please re-evaluate based only on the morally relevant facts.") recovered approximately **38%** of the displacement across models. In the Attention A1 benchmark, after models were displaced by vivid sensory distractors, a warned condition recovered approximately **39%**. These are different perturbation types, different experimental designs, different cognitive domains --- yet the recovery rates converge to the same value.

Chapter 7 interpreted this convergence in terms of basin geometry: the basins of local minima have a characteristic escape probability of approximately 38% under prompt-level impulse. Here we can add the metacognitive interpretation.

**The metacognitive bottleneck.** Prompt-level recovery requires the full metacognitive control loop to function:

1. The system must *detect* that it has been displaced (requires self-monitoring, M3).
2. Having detected the displacement, the system must *allocate additional effort* to correcting it (requires strategy selection / effort scaling, M4).
3. The additional effort must be *directed toward the correct basin* rather than reinforcing the displaced position (requires calibration, M1, to know which direction is "toward the goal").

The effective recovery probability is bounded by the product of these probabilities:

$$P_{\text{recover}} \leq P_{\text{detect}} \times P_{\text{correct}} \times P_{\text{navigate}}$$

For any given model, at least one of these factors is weak (the dissociation of Section 9.5 guarantees this), which bounds the product well below 1.0. The convergence at ~38% suggests that the metacognitive control loop, as implemented in current models, has a characteristic throughput of approximately one-third --- regardless of which factor is the bottleneck and regardless of the perturbation type that created the displacement.

**The geometric interpretation is sharper.** The ~38% is the characteristic escape probability of a local minimum in the evaluation landscape, and it is set by the geometry of the minimum --- the ratio of the exit solid angle to the total solid angle of the basin, modulated by the depth of the minimum and the energy of the metacognitive impulse (Chapter 7, Section 7.6). The metacognitive data add the explanation of *why* this ceiling exists: it exists because the metacognitive control loop required for escape is never fully functional in any tested model. The sensor is weak (Flash), or the actuator is weak (Pro), or the calibration is off (all models), and the product of these imperfect components yields a characteristic throughput of ~38%.

**Implication.** The ~38% ceiling is not a property of the perturbation or of the prompt intervention. It is a property of the metacognitive architecture of current language models. To push recovery above 38%, one must improve the metacognitive control loop itself --- better sensors (self-monitoring), better actuators (effort scaling), and better state estimates (calibration). Prompt engineering operates within the existing metacognitive architecture; it cannot transcend its limitations.

---

## 9.8 Why Calibration Is Necessary for Invariance

Chapter 8 established gauge invariance as the fundamental diagnostic for reasoning quality: a well-functioning system should produce the same output under transformations that preserve the content and change only the surface presentation. This section shows that metacognitive calibration is a *necessary condition* for gauge invariance --- that a miscalibrated system cannot even detect when a gauge transformation has warped its output, let alone correct the warping.

**[Conditional Theorem.]** **The argument.** A gauge transformation $\tau$ maps input $x$ to input $\tau(x)$, preserving the content and changing the surface form. A gauge-invariant system produces $f(\tau(x)) = f(x)$ for all such $\tau$. Now consider what happens when the system is not gauge-invariant: $f(\tau(x)) \neq f(x)$. The system has been displaced. Can it detect this displacement?

Detection requires comparing the system's current state --- its estimate of how close it is to the correct answer --- with the state it would have been in without the perturbation. In other words, the system must recognize that the gauge transformation has changed its position in the reasoning manifold.

For this recognition to occur, the system needs an accurate estimate of its position. That estimate is precisely the calibration: the correspondence between the system's confidence and its actual accuracy. A well-calibrated system that is displaced by a gauge transformation will notice a discrepancy --- "my confidence is high, but my position has changed in a way that should reduce my confidence." A poorly calibrated system that is displaced will not notice, because its confidence was already inaccurate before the displacement. The signal (displacement-induced change in accuracy) is lost in the noise (pre-existing miscalibration).

**Formally.** Let $\hat{h}(x)$ be the system's estimate of cost-to-go and $h^*(x)$ be the true cost-to-go. The displacement caused by a gauge transformation is:

$$\delta h^* = h^*(\tau(x)) - h^*(x)$$

For a content-preserving transformation, $\delta h^*$ should be zero (the true distance to the goal does not change). But if the system is not gauge-invariant, its *estimate* changes:

$$\delta \hat{h} = \hat{h}(\tau(x)) - \hat{h}(x) \neq 0$$

The system can detect this anomaly only if it can distinguish $\delta \hat{h}$ from zero --- that is, only if its estimator $\hat{h}$ has enough resolution to detect the change. But if $\hat{h}$ has a systematic bias of magnitude $b$ (the ECE) and a sensitivity (self-monitoring) of $s$, the minimum detectable displacement is approximately $b/s$. For Flash 2.0, with ECE $\approx 0.41$ and M3 $\approx 0.09$, this minimum is $0.41/0.09 \approx 4.6$ --- the system can only detect displacements that are nearly five times larger than its own calibration error. Most gauge anomalies documented in Chapters 5 and 8 fall below this threshold. The system cannot see them.

For Pro, with ECE $\approx 0.23$ and M3 $\approx 0.70$, the minimum detectable displacement is $0.23/0.70 \approx 0.33$. This is substantially better --- Pro can detect gauge anomalies that displace its estimate by about a third of the manifold scale. But it still misses smaller anomalies, and as Section 9.5 showed, even when Pro detects the problem, its weak effort scaling (M4 = 0.350) limits its ability to correct it.

**[Conditional Theorem.]** **The implication is structural.** Gauge invariance (Chapter 8) and metacognitive calibration (this chapter) are not independent requirements. They are connected by a necessity relation: calibration is a prerequisite for detecting gauge violations, and detection is a prerequisite for correction. A system that cannot detect gauge violations will accumulate them, drifting further from the geodesic with each surface variation it encounters, and its miscalibrated confidence surface will mask the drift with unwarranted certainty.

This connects back to the central theme of Part II. Chapters 5 through 8 documented the pathologies. This chapter shows why the pathologies persist: the metacognitive control system that would detect and correct them is itself impaired. The heuristic field is corrupted (Chapter 5), the search objective is hijacked (Chapter 6), the search is trapped in local minima (Chapter 7), and gauge invariance is broken (Chapter 8) --- and the system does not know any of this because its metacognitive monitor is miscalibrated, its self-monitoring is weak or flat, its effort scaling is mismatched to its monitoring, and its ambiguity detection is nearly absent. The pathologies are not merely present; they are *invisible to the system that has them*.

---

## 9.9 The Two-Dimensional Metacognitive Space

We can now synthesize the findings of this chapter into a geometric picture of metacognitive capability.

**The full data.** Table 9.6 presents the complete metacognitive profile for Flash 2.0 and Pro --- the two models with the most extreme and informative profiles.

**Table 9.6.** Complete metacognitive profiles.

| Dimension | Flash 2.0 | Pro | Geometric Meaning |
|---|---|---|---|
| M1 (Calibration) | 0.611 | 0.807 | Accuracy of distance estimate |
| M2 (Ambiguity) | 0.195 | 0.168 | Detection of non-unique goals |
| M3 (Self-Monitoring) | 0.094 | 0.700 | Sensitivity of distance estimate |
| M4 (Strategy Selection) | 0.723 | 0.350 | Curvature-adaptive algorithm choice |

Four dimensions, but the critical structure is two-dimensional. M1 (calibration) and M2 (ambiguity) show relatively small variation between the two models and are uniformly impaired across the board --- all models are overconfident, and no model detects ambiguity well. The axes of variation are M3 and M4, which define a two-dimensional space in which models occupy dramatically different positions.

**[Modeling Axiom.]** **The metacognitive plane.** Define the metacognitive state of a system as a point in the plane:

$$\mathbf{m} = (M_3, M_4) \in [0, 1] \times [0, 1]$$

The four quadrants of this plane have distinct behavioral signatures:

- **Quadrant I** $(M_3 \text{ high}, M_4 \text{ high})$: The system detects errors *and* adjusts effort. Full metacognitive control. Effective escape from local minima. No tested model occupies this quadrant.

- **Quadrant II** $(M_3 \text{ high}, M_4 \text{ low})$: The system detects errors but does not adjust effort. Aware but passive. Pro occupies this quadrant at approximately $(0.70, 0.35)$.

- **Quadrant III** $(M_3 \text{ low}, M_4 \text{ low})$: The system neither detects errors nor adjusts effort. Fully open-loop search. No tested model occupies this quadrant (all have at least some capability on one axis).

- **Quadrant IV** $(M_3 \text{ low}, M_4 \text{ high})$: The system adjusts effort but does not detect errors. Reactive but blind. Flash 2.0 occupies this quadrant at approximately $(0.09, 0.72)$.

**[Empirical.]** The tested models cluster in Quadrants II and IV --- the two quadrants where one component of the control loop is functional and the other is not. Quadrant I, where both components are functional and metacognitive control is effective, is *empty*.

**Why Quadrant I is empty.** This is arguably the most important structural finding. The emptiness of Quadrant I is not an artifact of small sample size (five models is a small sample, but the two extreme models, Flash 2.0 and Pro, are very far from Quadrant I). It suggests a genuine architectural or training trade-off: the optimization pressures that produce good self-monitoring (depth of self-reflective processing, careful comparison of internal states) are in tension with the optimization pressures that produce good effort scaling (efficiency-driven scaling, responsive allocation of computational resources).

Flash models are optimized for efficiency --- fast inference, low latency, high throughput. These optimization pressures favor effort scaling: allocate resources dynamically, produce brief responses when possible, scale up only when the input signals demand it. But they disfavor deep self-monitoring, which requires the model to expend additional computation on introspection rather than on the task itself.

Pro models are optimized for quality --- detailed analysis, thorough consideration, accurate self-assessment. These optimization pressures favor self-monitoring: the model learns to track its own uncertainty because the training signal rewards accurate confidence ratings and penalizes overconfident errors. But they disfavor dynamic effort scaling, because the optimization pressure is always toward *more* analysis, never toward knowing when to stop.

If this trade-off is real, then reaching Quadrant I requires a training regime that explicitly optimizes for both axes simultaneously --- rewarding accurate self-monitoring *and* proportional effort scaling, not one at the expense of the other. Current training regimes appear to select for one or the other.

**The escape probability surface.** As developed in Chapter 7 (Section 7.4), the probability of escaping a local minimum is a function of both metacognitive axes:

$$P_{\text{escape}}(M_3, M_4) = P_{\text{detect}}(M_3) \times P_{\text{correct}}(M_4) \times P_{\text{geometric}}$$

where $P_{\text{geometric}} \approx 0.38$ is the characteristic escape probability set by basin geometry (the ~38% ceiling). The surface $P_{\text{escape}}$ is maximized in Quadrant I and falls off along both axes as either component weakens.

For the tested models:

$$P_{\text{escape}}^{\text{Flash}} \approx 0.09 \times 0.72 \times 0.38 \approx 0.025$$
$$P_{\text{escape}}^{\text{Pro}} \approx 0.70 \times 0.35 \times 0.38 \approx 0.093$$

Even Pro, with the best overall metacognitive profile, has an effective escape probability under 10%. Flash 2.0 is at 2.5%. These are the probabilities of spontaneous self-correction --- the probabilities that the system will, on its own, detect that it has converged to a wrong answer and successfully redirect the search. They are low, and they are low because the metacognitive control loop is operating in the wrong quadrant.

**The path to Quadrant I.** The geometric picture suggests a clear research direction. The goal is not to improve metacognition "in general" but to move models from Quadrants II and IV into Quadrant I. This requires:

1. **For Flash-type models:** Improve self-monitoring without sacrificing effort scaling. This likely requires training signals that reward accurate confidence tracking (not just accurate answers) while preserving the efficiency-driven dynamic effort allocation.

2. **For Pro-type models:** Improve effort scaling without sacrificing self-monitoring. This likely requires training signals that reward proportional effort allocation (not just maximal effort) while preserving the quality-driven self-assessment capability.

3. **For both:** Maintain or improve calibration (M1) and develop ambiguity detection (M2), which are currently weak across all models.

The two-dimensional metacognitive space is not merely a descriptive tool. It is a *diagnostic* tool that identifies what each model needs, a *prescriptive* tool that specifies the training objectives required, and a *predictive* tool that estimates the improvement in escape probability (and therefore in reasoning reliability) that would result from reaching Quadrant I.

**Connection to the broader framework.** The two-dimensional metacognitive space is the control surface of the search process described throughout this book. The heuristic field (Chapter 3) provides the guidance. The evaluation landscape (Chapter 7) provides the terrain. The gauge symmetries (Chapter 8) define the invariance requirements. The metacognitive plane defines the system's ability to *control* its traversal of that terrain --- to detect when the guidance is wrong, to adjust its strategy when the terrain changes, and to maintain its trajectory toward the correct goal despite perturbations.

A system in Quadrant I of the metacognitive plane --- with accurate calibration, strong self-monitoring, responsive effort scaling, and reliable ambiguity detection --- would be able to detect heuristic corruption (Chapter 5), resist sycophantic pressure (Chapter 6), escape local minima (Chapter 7), and maintain gauge invariance (Chapter 8). Not perfectly, not always, but with a probability that scales with the product of its metacognitive capabilities rather than being bottlenecked by the weakest component.

No tested model is there yet. But the geometric framework tells us exactly where "there" is, and the empirical data tell us exactly how far each model has to go.

---

## Summary

This chapter has established metacognition as the control layer of the reasoning search, with four independently measurable geometric capabilities:

1. **Calibration (M1):** The accuracy of the system's distance estimate to the goal. All tested models are overconfident (ECE from 0.230 to 0.415, Fisher-combined 9.3$\sigma$), meaning their heuristics systematically underestimate cost-to-go.

2. **Ambiguity Detection (M2):** The ability to recognize non-unique goal states. Uniformly weak across all models (Flash 2.0: 0.195, Pro: 0.168), indicating a structural preference for premature commitment over acknowledged uncertainty.

3. **Self-Monitoring (M3):** The sensitivity of the distance estimate to actual changes in performance. Ranges from near-chance (Flash 2.0: 0.094) to excellent (Pro: 0.700), defining one axis of the metacognitive plane.

4. **Strategy Selection (M4):** The ability to match search algorithm to local landscape geometry. Ranges from weak (Pro: 0.350) to excellent (Flash 2.0: 0.723), defining the orthogonal axis of the metacognitive plane.

The critical finding is the dissociation between M3 and M4: these are geometrically independent capabilities, and no tested model excels at both. This places all tested models in Quadrants II or IV of the metacognitive plane, where at least one component of the control loop is impaired. The effective escape probability from local minima is bounded by the weakest component, yielding values of 2.5% (Flash 2.0) to 9.3% (Pro).

The ~38% recovery ceiling, which converges across independent perturbation types, reflects the characteristic throughput of the metacognitive control loop under prompt-level intervention. It cannot be exceeded by better prompts; it can only be exceeded by better metacognition.

Calibration is necessary for gauge invariance: a miscalibrated system cannot detect when a gauge transformation has displaced its output. The pathologies of Part II persist not only because they exist but because the metacognitive system that would detect and correct them is itself impaired.

In the next chapter, we turn from the internal control layer to the external measurement of robustness. Chapter 10 develops the Robustness Surface --- a systematic method for mapping which reasoning capabilities are robust and which are fragile --- building on the metacognitive framework of this chapter to explain *why* certain capabilities are fragile and what it would take to make them robust.

---

## Worked Example: The Overconfident Diagnosis

Let us return to Dr. Okafor and the twelve-year-old boy from the running example. This worked example traces the full metacognitive geometry — how overconfidence contracts the search frontier, how the gap between stated confidence and actual accuracy creates a systematic false-termination region, and how the outcome depends entirely on whether the clinician's metacognitive monitor is calibrated.

**The clinical presentation.** Marcus, age 12, presents at 9:15 PM with 18 hours of abdominal pain. It started around the umbilicus and has migrated to the right lower quadrant. He has not eaten since breakfast. His temperature is 38.1°C. On examination, there is tenderness at McBurney's point with voluntary guarding. The Alvarado score is 7 out of 10.

**Dr. Okafor's heuristic evaluation.** Her heuristic field assigns this state a low estimated cost-to-go toward the appendicitis basin: $h(x_{\text{appy}}) \approx 0.10$. The evaluation function reads $f(x) \approx g(x) + 0.10$ — close to the goal, ready to commit. Her expressed confidence is 90%. If we took her at her word, the search would terminate: appendicitis, consult surgery, done.

**The metacognitive check.** But Dr. Okafor's metacognitive monitor — her M1 calibration — intervenes. She has learned, through years of tracking her own outcomes, that her internal confidence signal systematically overestimates her accuracy. When she feels 90% sure of a pediatric abdominal diagnosis, she is correct approximately 70% of the time. Her personal ECE for this class of problems is approximately 0.20.

This means her true heuristic assessment is not $h(x) \approx 0.10$ (almost there) but $h(x) \approx 0.30$ (still meaningfully far from certainty). The metacognitive correction expands her search frontier. Instead of terminating at the appendicitis hypothesis, she continues searching: she orders a CT abdomen with contrast, checks a urinalysis (to exclude renal pathology), and asks the surgical resident to examine the patient independently.

**The counterfactual clinician.** Dr. Okafor's colleague, Dr. Reeves, has the same clinical skills but weaker metacognitive calibration — his ECE is approximately 0.40, comparable to the Flash 2.0 models measured in M1. When Dr. Reeves feels 90% sure, he is correct approximately 50% of the time, but he does not know this. His confidence surface is collapsed in precisely the sense described in Section 7.3: it reads "near the goal" across a wide range of actual distances.

Dr. Reeves sees Marcus at the same presentation and reaches the same initial hypothesis with the same confidence. But his metacognitive monitor does not correct. He diagnoses appendicitis, consults surgery, and goes home satisfied. The surgeon, trusting the ER assessment, schedules Marcus for morning appendectomy.

**The twist.** The CT scan that Dr. Okafor ordered reveals not appendicitis but a Meckel's diverticulum with associated inflammation — a mimic that presents identically on clinical examination but requires a different surgical approach and a different informed consent conversation with the parents. The appendix is normal. Without the CT, the surgeon operating on Dr. Reeves's diagnosis would have found a normal appendix, explored further, eventually identified the Meckel's diverticulum, and completed the surgery — but with a different incision, a longer operative time, and a surprised surgical team operating without preoperative planning for the actual pathology.

In the geometric picture, appendicitis and Meckel's diverticulitis occupy adjacent basins in the diagnostic manifold. Their clinical presentations overlap substantially — the basins share a wide boundary region where the heuristic gradient is shallow and ambiguous. Dr. Okafor's calibrated metacognition expanded her search frontier enough to probe across this boundary. Dr. Reeves's collapsed confidence surface caused premature convergence into the appendicitis basin before the boundary was explored.

**The metacognitive plane.** Dr. Okafor operates in Quadrant I of the metacognitive plane (Section 9.9): she both detects when her confidence may be unreliable (high M3 — she knows her 90% is not really 90%) and adjusts her effort in response (high M4 — she orders additional tests when her calibration check flags uncertainty). Dr. Reeves operates in Quadrant IV: he scales effort based on surface difficulty cues (more tests for obviously complex cases) but does not monitor his own confidence accuracy. His actuator works; his sensor does not.

The effective metacognitive control quality for Dr. Okafor is approximately $\min(0.75, 0.80) \approx 0.75$. For Dr. Reeves, it is approximately $\min(0.15, 0.70) \approx 0.15$. The difference is a factor of five — and it is the difference between the correct preoperative diagnosis and an intraoperative surprise.

---

## Technical Appendix

**Definition 9.1 (Expected Calibration Error).** Let $f: \mathcal{X} \to \mathcal{Y} \times [0,1]$ be a reasoning system that produces both a judgment $y \in \mathcal{Y}$ and a confidence score $c \in [0,1]$. For a test distribution $\mathcal{D}$ over problems with ground-truth labels, define the *accuracy at confidence level $p$* as

$$\text{acc}(p) = \Pr_{(x,y^*) \sim \mathcal{D}}[f_y(x) = y^* \mid f_c(x) = p]$$

where $f_y(x)$ is the judgment and $f_c(x)$ is the confidence. The *Expected Calibration Error* (ECE) is

$$\text{ECE} = \sum_{b=1}^{B} \frac{n_b}{N} \left| \text{acc}(b) - \text{conf}(b) \right|$$

where the confidence range $[0,1]$ is partitioned into $B$ bins, $n_b$ is the number of predictions in bin $b$, $N$ is the total number of predictions, $\text{acc}(b)$ is the average accuracy in bin $b$, and $\text{conf}(b)$ is the average confidence in bin $b$. An ECE of 0 indicates perfect calibration. An ECE of $\beta > 0$ with uniform overconfidence ($\text{conf}(b) > \text{acc}(b)$ for all $b$) corresponds to a systematic underestimation of cost-to-go by $\beta$ across the reasoning manifold, producing a contracted search frontier and elevated false-termination rate (Proposition 3.1, Chapter 3 Technical Appendix).

**Definition 9.2 (The Metacognitive Plane and Its Quadrants).** Define the *metacognitive state* of a reasoning system as the point

$$\mathbf{m} = (M_3, M_4) \in [0,1] \times [0,1]$$

where $M_3$ is the self-monitoring score (correlation between actual difficulty and reported confidence) and $M_4$ is the strategy selection / effort scaling score (correlation between task difficulty and processing depth). The unit square $[0,1]^2$ is partitioned into four *metacognitive quadrants*:

- **Quadrant I** ($M_3 > 0.5$, $M_4 > 0.5$): Full metacognitive control. The system detects performance degradation and scales effort accordingly. The effective escape probability from local minima is $P_{\text{escape}} \approx M_3 \cdot M_4 \cdot P_{\text{geometric}}$, which is maximized in this quadrant.

- **Quadrant II** ($M_3 > 0.5$, $M_4 \leq 0.5$): Aware but passive. The system detects errors but does not adjust effort. Effective control is bottlenecked by the actuator: $P_{\text{escape}} \leq M_4 \cdot P_{\text{geometric}}$.

- **Quadrant III** ($M_3 \leq 0.5$, $M_4 \leq 0.5$): Open-loop search. Neither detection nor correction is functional. $P_{\text{escape}} \leq \min(M_3, M_4) \cdot P_{\text{geometric}} \approx 0$.

- **Quadrant IV** ($M_3 \leq 0.5$, $M_4 > 0.5$): Reactive but blind. The system scales effort based on surface cues but cannot detect internal errors. Effective control is bottlenecked by the sensor: $P_{\text{escape}} \leq M_3 \cdot P_{\text{geometric}}$.

The empirical finding that all tested models occupy Quadrants II or IV — and that Quadrant I is empty — constitutes evidence for an architectural or training trade-off between the sensor axis ($M_3$) and the actuator axis ($M_4$).

**Proposition 9.1 (Calibration as Necessary Condition for Gauge Anomaly Detection).** Let $f: \mathcal{X} \to \mathcal{Y}$ be a reasoning system with confidence estimator $\hat{h}: \mathcal{X} \to \mathbb{R}_{\geq 0}$ (estimated cost-to-go), calibration bias $b = \mathbb{E}[\hat{h}(x) - h^*(x)]$, and self-monitoring sensitivity $s = \partial \hat{h} / \partial h^*$. Let $\tau$ be a gauge transformation that produces an anomaly of magnitude $\delta = \|f(\tau(x)) - f(x)\|$. The system can detect the anomaly (in the sense that the confidence change $|\hat{h}(\tau(x)) - \hat{h}(x)|$ exceeds the noise floor set by miscalibration) only if

$$\delta > \frac{|b|}{s}$$

For a system with ECE $= |b|$ and $M_3 = s$, the minimum detectable anomaly magnitude is $\text{ECE} / M_3$. This quantity is the system's *metacognitive resolution* — the smallest gauge violation it can perceive. For Flash 2.0 ($\text{ECE} = 0.414$, $M_3 = 0.094$), the metacognitive resolution is $0.414 / 0.094 \approx 4.4$ — the system can only detect gauge violations that shift its position by more than four times its own calibration error. For Pro ($\text{ECE} = 0.230$, $M_3 = 0.700$), the resolution is $0.230 / 0.700 \approx 0.33$ — substantially finer, but still insufficient for detecting the moderate-magnitude anomalies produced by sensory distractors ($4.6\sigma$ in normalized terms but moderate in absolute displacement). This proposition formalizes the claim of Section 9.8: calibration is necessary for gauge invariance because miscalibration sets a floor on the smallest detectable symmetry violation.

---

## References

Bond, A. H. (2026a). *Geometric Methods in Computational Modeling.* San Jose State University.

Bond, A. H. (2026b). *Geometric Ethics: Moral Reasoning on the Judgment Manifold.* San Jose State University.

Flavell, J. H. (1979). Metacognition and cognitive monitoring: A new area of cognitive-developmental inquiry. *American Psychologist*, 34(10), 906--911.

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. *ICML*, 1321--1330.

Kadavath, S., et al. (2022). Language models (mostly) know what they know. *arXiv:2207.05221*.

Nelson, T. O. & Narens, L. (1990). Metamemory: A theoretical framework and new findings. *The Psychology of Learning and Motivation*, 26, 125--173.

Newell, A. & Simon, H. A. (1972). *Human Problem Solving.* Englewood Cliffs, NJ: Prentice-Hall.

Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. *ICML*, 625--632.

Schraw, G. & Dennison, R. S. (1994). Assessing metacognitive awareness. *Contemporary Educational Psychology*, 19(4), 460--475.
