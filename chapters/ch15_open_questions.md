# Chapter 15: Open Questions

*Part V: Horizons*

---

> *"The formulation of a problem is often more essential than its solution."*
> --- Albert Einstein

> **RUNNING EXAMPLE — DR. OKAFOR'S TRIAGE**
>
> *Dr. Amara Okafor's clinical reasoning manifold, developed across the preceding chapters, now confronts questions the framework cannot yet answer. Is her triage space Riemannian — the same cost to move from "probable cardiac event" to "probable anxiety" as to move back? Or does the profound asymmetry of diagnostic error demand Finsler geometry: missing a myocardial infarction kills, while over-triaging chest pain merely costs a CT scan and an hour? The asymmetry ratio $\alpha$ between these directions may be ten to one.*
>
> *Can we measure her heuristic field? If representation engineering could extract a "clinical cost-to-go" direction from a triage AI's activations, would it resemble the gradient that twenty years of emergency medicine burned into her cortex? Would the extracted field be smooth — the gentle landscape of Chapter 3 — or fractal, jagged with the thousand edge cases that resist generalization?*
>
> *And the deepest question: when Dr. Okafor walks into the ER and the room "organizes itself" before conscious thought begins, is that genuinely search? Or is her pattern recognition something outside the search framework entirely — a direct perception of the manifold's structure that no search algorithm, however fast, can replicate? These are the open questions. The framework has earned the right to ask them precisely; it has not yet earned the right to answer them.*

## Introduction

This book has developed a mathematical framework for reasoning: search on manifolds, guided by heuristic fields, along geodesics, with failure modes characterized as geometric pathologies and metacognition characterized as search control. Parts I--IV established the vocabulary, catalogued the failure modes, described the control layer, and presented the empirical program. But a framework is not a finished theory. It is a scaffolding on which a theory can be built --- and the quality of a scaffolding is measured not by what it already supports, but by what it makes visible that was previously hidden.

This chapter catalogs the open questions that the geometric framework makes visible. Some are technical: what is the right mathematical object? Some are empirical: can we measure the heuristic field directly? Some are philosophical: is human reasoning actually search? And some are practical: can we shape heuristics without breaking them? These questions are not afterthoughts. They are the research program that this book is designed to launch.

---

## 15.1 Theory: What Is the Right Mathematical Object?

Throughout this book, we have worked primarily with Riemannian manifolds: smooth spaces equipped with a metric tensor $g_{ij}$ that defines distances, angles, geodesics, and curvature. This choice was motivated by three considerations. First, Riemannian geometry is the most developed branch of differential geometry, offering a rich toolkit of theorems and computational methods. Second, the SPD manifold (Appendix A.4) and the hyperbolic space used in the ARC-AGI pipeline (Section 14.5) are both naturally Riemannian. Third, the geodesic equation --- the central object of Chapter 4 --- requires a connection, and the Levi-Civita connection of a Riemannian metric is the canonical choice.

But there are reasons to suspect that Riemannian geometry is not the final answer. The reasoning manifold may require a richer or more flexible geometric structure. Let us examine the candidates.

### Finsler Manifolds: Direction-Dependent Cost

A Riemannian metric assigns a cost to each infinitesimal displacement that depends only on the *magnitude* of the displacement and the *point* at which it occurs: $ds^2 = g_{ij}(x) \, dx^i \, dx^j$. The cost is the same whether you move "forward" or "backward" along any direction. **[Speculation/Extension.]** A **Finsler metric** generalizes this by allowing the cost to depend on the *direction* of movement as well: $ds = F(x, \dot{x})$, where $F$ is a norm on each tangent space that need not arise from an inner product.

**[Empirical.]** The case for Finsler geometry in reasoning is compelling. Consider the sycophancy data from Chapter 6: the cost of revising a belief in the direction of social approval is lower than the cost of revising in the direction of truth, for most models. This is precisely a direction-dependent metric. The "distance" from state $A$ to state $B$ differs depending on which direction you traverse: moving from a correct belief to an approval-consistent belief is cheap (the system does it readily), while moving from an approval-consistent belief to a correct belief is expensive (the system resists).

More formally, define the asymmetry ratio $\alpha(x, v) = F(x, v) / F(x, -v)$. In a Riemannian manifold, $\alpha = 1$ everywhere --- the metric is symmetric. In a Finsler manifold, $\alpha$ can vary. The sycophancy gradient (0% to 56% flip rate) suggests that the asymmetry ratio differs dramatically across models: Claude operates near $\alpha \approx 1$ (symmetric cost for truth-seeking vs. approval-seeking), while Flash 2.5 operates at $\alpha \gg 1$ in the approval direction.

The technical cost of Finsler geometry is significant. The connection is no longer unique (there are multiple natural choices: the Chern connection, the Berwald connection, the Cartan connection), the curvature theory is more complex, and computational tools are less mature. But the empirical data suggest the cost may be worth paying.

**Open Problem 15.1.** *Characterize the Finsler structure of the reasoning manifold. Is the asymmetry ratio $\alpha(x, v)$ measurable from model behavior? Does it predict sycophancy rates?*

### Sub-Riemannian Geometry: Constrained Directions

**[Speculation/Extension.]** A sub-Riemannian manifold is a smooth manifold equipped with a metric, but the metric is defined only on a *subspace* of the tangent space at each point. Movement is only possible along the "horizontal" directions; the remaining "vertical" directions are inaccessible at the infinitesimal level. Yet, by the Chow--Rashevskii theorem, if the horizontal directions and their iterated Lie brackets span the full tangent space, then any two points can still be connected by a horizontal path --- the path just cannot take the direct route.

This structure may be relevant to reasoning under constraints. When a language model is asked to solve a problem subject to specific rules (e.g., "explain quantum entanglement without using the word 'particle'"), certain directions in the reasoning space are forbidden at each step. The system can still reach the goal, but it must navigate through the permitted subspace, taking indirect paths that satisfy the constraints. The resulting trajectories are sub-Riemannian geodesics: they minimize length among paths that respect the constraint distribution.

The executive functions data (Chapter 13.5) provides indirect evidence. Framework switching tasks (E1) require the model to change its entire reasoning strategy mid-problem --- a transition that may require moving through a constrained subspace where only certain cognitive operations are available. The low switch rates (32--47%) suggest that the horizontal distribution is narrow: the available directions at each point are limited, and navigating through the constrained space is difficult.

### Stratified Spaces: Qualitatively Different Regions

A stratified space is a topological space decomposed into smooth pieces (strata) of different dimensions, glued together along their boundaries. The classic example is a cone: the tip is a 0-dimensional stratum, and the rest is a 2-dimensional stratum. The geometry changes qualitatively at the stratum boundaries.

The reasoning manifold may be stratified. Consider the transition between System 1 and System 2 reasoning (to use Kahneman's terminology, discussed further in Section 15.4). In System 1, the model navigates a low-dimensional manifold of cached associations --- fast, automatic, pattern-matched. In System 2, it navigates a higher-dimensional manifold of explicit inference steps --- slow, deliberate, compositional. The transition between these two modes is not a smooth deformation; it is a qualitative change in the dimensionality of the accessible state space.

The metacognition data (Chapter 9) may provide evidence for stratification. The effort scaling results (M4) show that some models adjust their computational effort smoothly in response to task difficulty (Flash 2.0, effort score 0.723), while others show little variation (Pro, effort score 0.350). The smooth-adjustment models may be navigating a single stratum of variable difficulty. The low-adjustment models may be stuck on a single stratum with no access to the transition that would take them to a higher-dimensional reasoning space.

**Open Problem 15.2.** *Does the reasoning manifold have a stratified structure? If so, what determines the boundaries between strata, and can we measure the dimensionality of each stratum from model activations?*

### Information Geometry: The Natural Candidate

**[Established Mathematics.]** Information geometry, developed principally by Shun-ichi Amari and his collaborators, equips the space of probability distributions with a natural Riemannian structure: the Fisher information metric. If $p(x|\theta)$ is a parametric family of distributions, the Fisher metric is:

$$g_{ij}(\theta) = \mathbb{E}\left[\frac{\partial \log p(x|\theta)}{\partial \theta^i} \frac{\partial \log p(x|\theta)}{\partial \theta^j}\right]$$

This metric has a deep information-theoretic justification: it is the unique Riemannian metric (up to scaling) that is invariant under sufficient statistics. In other words, it is the metric that measures "how much information" distinguishes nearby distributions --- exactly the quantity that matters for reasoning about uncertain propositions.

Language models *are* parametric families of probability distributions. Each model state defines a distribution over next tokens. A reasoning trajectory is a sequence of distributions --- each conditioned on the growing context. The Fisher metric provides a natural way to measure the "distance" between successive reasoning states: two states are close if their predictive distributions are similar, and far apart if they are dissimilar. This is precisely the notion of distance that the geometric framework requires.

The connection deepens in Section 16.2. For now, the key observation is that information geometry provides a candidate geometric structure that is not imposed from outside but *arises naturally from the statistical structure of the model itself*. This is the strongest argument for any particular geometric formalization: the geometry should not be a choice we make but a structure we discover.

**Open Problem 15.3.** *Is the Fisher information metric the correct metric for the reasoning manifold? If so, how does it relate to the heuristic field $h(x)$ and the geodesic equation? Can the geodesic deviation measured in Chapter 4 be recomputed using the Fisher metric, and does this improve the correlation with reasoning quality?*

---

## 15.2 Mechanisms: Measuring the Heuristic from Activations

The heuristic field $h(x)$ has been this book's central construct: the scalar field that guides search, whose corruption explains failure modes (Chapter 5), whose geometry predicts sycophancy (Chapter 6), and whose calibration determines metacognitive quality (Chapter 9). But throughout, the heuristic has been *inferred* from behavior --- from the model's outputs, not from its internal states. Can we do better? Can we measure $h(x)$ directly from the model's activations?

### Representation Engineering

**[Speculation/Extension.]** The most promising approach comes from representation engineering (Zou et al., 2023; Burns et al., 2022). The central finding of this research program is that transformer activations contain *linear* representations of high-level concepts. Given a set of contrast pairs --- statements that differ along a single semantic dimension (e.g., truthful vs. false, happy vs. sad) --- a simple linear probe (logistic regression on the activation vectors) can identify a direction in activation space that corresponds to that dimension. These directions are remarkably consistent across layers and inputs, suggesting that the model maintains a structured representation of semantic content.

The relevance to the heuristic field is immediate. If the model's estimate of "how close am I to the correct answer" is represented as a direction in activation space, then a linear probe trained on contrast pairs (correct vs. incorrect reasoning steps) should recover that direction. The projection of the activation vector onto this direction at each step of the reasoning process would give a direct measurement of $h(x)$ --- the model's internal estimate of the cost-to-go.

Preliminary evidence suggests this is feasible. Li et al. (2024) identified "truthfulness" directions in LLaMA activations. Marks and Tegmark (2023) found "board state" representations in a chess-playing transformer. If the heuristic field exists as a structured representation in activation space, it should be discoverable by similar methods.

### The Heuristic as a Direction

More precisely, suppose the heuristic field is represented by a direction $\hat{h}$ in activation space. At each layer $l$ and token position $t$, the model produces an activation vector $a_l^t \in \mathbb{R}^d$, where $d$ is the hidden dimension. The heuristic value at this point in the reasoning trajectory would be:

$$h(l, t) = \hat{h} \cdot a_l^t$$

This is a scalar field on the space of (layer, token position) pairs --- exactly what we need. If $h(l, t)$ decreases monotonically along correct reasoning trajectories (the search is getting closer to the goal) and fluctuates or increases along incorrect ones (the search is wandering or moving away), we would have direct evidence that the heuristic field is not merely a useful abstraction but a measurable internal state.

The challenge is identifying $\hat{h}$. Representation engineering requires contrast pairs, which means we need examples of reasoning steps that are "closer to the goal" and "farther from the goal" --- a ground truth that may be difficult to establish for open-ended reasoning. Chain-of-thought traces with known-correct and known-incorrect intermediate steps provide one source. Mathematical proofs with verified lemmas provide another.

### Smoothness or Fractal Structure?

A deeper question concerns the regularity of the heuristic field. The theoretical framework of this book assumes $h(x)$ is at least $C^1$ (continuously differentiable) --- smooth enough to define a gradient, which the search follows. But there is no a priori reason why the heuristic must be smooth. If the model's internal representation of "distance to goal" has discontinuities, fractal structure, or high-frequency oscillations, the gradient-following picture breaks down.

Consider the metacognition data. The 9.3$\sigma$ combined miscalibration (Chapter 9) suggests that $h(x)$ has significant systematic errors. But are these errors *smooth* --- a gentle warping of the heuristic surface, like a lens distortion? Or are they *fractal* --- a jagged, self-similar structure where the error at any scale resembles the error at every other scale?

The distinction matters for intervention. Smooth errors can be corrected by smooth adjustments (LoRA fine-tuning as local curvature adjustment, Section 14.3). Fractal errors require fundamentally different approaches --- perhaps retraining from scratch, or regularization that specifically penalizes high-frequency variation in the heuristic.

**Open Problem 15.4.** *Is the heuristic field $h(x)$, as measured from transformer activations, smooth, piecewise smooth, or fractal? What is its Hausdorff dimension? Does the regularity class correlate with the model's reasoning quality?*

**Open Problem 15.5.** *Can representation engineering extract a "cost-to-go" direction from transformer activations that correlates with reasoning quality across diverse tasks? If so, does the extracted direction vary across tasks (task-specific heuristics) or remain stable (a general reasoning heuristic)?*

---

## 15.3 Evaluation: Reasoning vs. Pattern Completion

The central challenge for any empirical program in reasoning is the distinction between genuine search and memorized lookup. A model that produces the correct answer to a mathematical problem may have *derived* the answer through a chain of inference steps --- genuine search through the reasoning manifold --- or it may have *recognized* the problem as similar to a training example and *retrieved* the answer from memory. Both produce the same output. The trajectories are observationally identical at the output level.

### Near-Geodesic Behavior: Expert or Memorizer?

Chapter 4 proposed geodesic deviation as a measure of reasoning quality: a model that follows a near-geodesic path is reasoning well, because it is taking a near-optimal trajectory through the reasoning manifold. But there is an ambiguity. An expert who has internalized the structure of the domain also follows near-geodesic paths --- not because they are searching efficiently, but because they have learned the geodesics themselves. An expert chess player does not search the game tree from scratch; they recognize patterns and recall the appropriate response. The trajectory *appears* geodesic, but the mechanism is retrieval, not search.

In the geometric framework, this ambiguity maps to a distinction between two types of near-geodesic behavior:

1. **Efficient search**: The heuristic field $h(x)$ is accurate, and the search algorithm follows it efficiently, yielding a trajectory close to the geodesic.
2. **Cached geodesics**: The model has memorized (portions of) the geodesic itself, and retrieves the trajectory directly without computing $h(x)$ at each step.

These two mechanisms are distinguishable in principle but not by output alone. The difference lies in the *internal dynamics*: efficient search should show evidence of evaluation and comparison at each step, while cached retrieval should show pattern matching followed by direct emission.

### The Novel-Problem Test

The gold standard for distinguishing reasoning from retrieval is performance on truly novel problems --- problems that the model cannot have encountered during training and that cannot be solved by interpolating from known solutions. If a model performs well on problems that require genuine compositional reasoning over novel combinations of familiar elements, we have stronger evidence for search than for retrieval.

The ARC-AGI challenge (Chollet, 2019) was designed with precisely this criterion: each task is a unique 2D grid transformation that cannot be solved by pattern matching against a training set. Our hyperbolic geometry pipeline (Section 14.5) addresses this directly, but the general challenge remains: how novel is "novel"? A model trained on billions of tokens has been exposed to an extraordinary range of patterns, analogies, and transformations. What appears novel to the evaluator may be a recombination of elements the model has seen in different contexts.

The framing susceptibility data from Chapter 5 provides indirect evidence. If the model were performing pure retrieval, its judgments should be invariant to framing --- it would retrieve the same answer regardless of how the question is phrased. The fact that framing shifts the judgment by 10--16 points (8.9$\sigma$) shows that the model is *computing* the answer in a way that is sensitive to the input representation. This is more consistent with search (where the starting point and heuristic field depend on the input representation) than with lookup (where the answer is keyed by abstract content).

But this argument is not conclusive. A retrieval system with noisy keys could also show sensitivity to input representation: different framings could activate different cached responses. The distinction between search and retrieval remains genuinely unresolved.

### Out-of-Distribution Evaluation

A more systematic approach uses out-of-distribution (OOD) evaluation: test the model on problems drawn from a distribution that is demonstrably different from the training distribution. If the model's performance degrades gracefully --- maintaining the geometric structure of its reasoning (consistent heuristic field, smooth trajectories, appropriate geodesic deviation) while making more errors --- this suggests genuine search with a less accurate heuristic. If the model's performance degrades catastrophically --- losing all geometric structure and producing incoherent trajectories --- this suggests the model has fallen off the manifold of memorized patterns.

The Measuring AGI benchmarks (Chapter 13) provide a partial implementation of this approach. The structural fuzzing test (T1) and the framing test (T5) deliberately construct inputs that differ from typical training data while preserving the essential reasoning content. Models that maintain high scores on these tests are demonstrating some degree of genuine reasoning. Models whose scores drop sharply are relying more heavily on surface-level pattern matching.

**Open Problem 15.6.** *Can we design benchmarks that definitively distinguish search from retrieval? What geometric signatures differentiate genuine heuristic-guided search from cached geodesic retrieval?*

---

## 15.4 Cognitive Science: Is Human Deliberation Bounded Search?

The Problem Space Hypothesis of Newell and Simon (Chapter 1) claims that human reasoning is search. The geometric framework extends this claim: human reasoning is search on a manifold with heuristic guidance. But does the claim hold empirically? Is human deliberation actually described by the search framework, or is search merely a convenient computational metaphor?

### System 1 and System 2 as Heuristic Regimes

Kahneman's dual-process theory (2011) distinguishes two modes of cognition: System 1 (fast, automatic, effortless) and System 2 (slow, deliberate, effortful). In the geometric framework, these map to different regimes of the same search process:

**System 1** operates with a highly confident heuristic field. The gradient is steep, the path to the goal is clear, and the search converges in one or two steps --- so quickly that it does not feel like "search" at all. This is the regime of expert pattern recognition: the chess grandmaster who sees the correct move immediately, the native speaker who parses a sentence without effort, the experienced driver who navigates a familiar route on autopilot. The heuristic is so good that the search trajectory collapses to a near-instantaneous geodesic.

**System 2** operates with a weak or ambiguous heuristic field. The gradient is shallow, the path to the goal is unclear, and the search must explore multiple branches before converging. This is the regime of deliberate problem-solving: the novice chess player who considers many moves, the language learner who constructs a sentence word by word, the driver navigating an unfamiliar city. The heuristic provides some guidance, but the search must do real work.

This mapping predicts several features of human cognition that are empirically observed. The System 1/System 2 transition should occur when the heuristic confidence drops below a threshold --- when the model's internal estimate of the cost-to-go becomes uncertain enough that the search cannot converge in a single step. This is consistent with the feeling of "switching to effortful mode" that Kahneman describes: it is the subjective correlate of the heuristic field becoming flat.

### Attention as Heuristic Guidance

Chapter 3 developed the analogy between attention mechanisms and heuristic guidance. In humans, attention serves exactly this function: it selects which aspects of the environment to process, which memories to retrieve, which inferences to pursue. Attention is the mechanism by which the heuristic field is implemented in biological hardware.

The attention data from Chapter 13.4 supports this connection indirectly. The selective attention task (A1) measures the ability to maintain focus on relevant information while ignoring distractors --- exactly the function of a well-calibrated heuristic field that points toward the goal and away from irrelevant attractors. The divided attention task (A4) measures the ability to maintain multiple parallel search fronts --- the biological analogue of beam search.

The fact that LLMs show similar patterns of attention vulnerability as humans (sensitivity to salient distractors, capacity limitations under divided attention) suggests that the geometric framework applies to both. But the analogy has limits: LLM attention is a specific computational mechanism (scaled dot-product attention), while human attention is a complex, multi-scale phenomenon involving neural oscillations, neuromodulatory systems, and top-down feedback loops that are only partially understood.

### The Introspection Problem

A fundamental obstacle to testing the search hypothesis in humans is the unreliability of introspection. We cannot directly observe human search trajectories. We can observe behavior (response times, eye movements, error patterns) and neural activity (fMRI, EEG, single-unit recordings), but the mapping from these observables to the internal search trajectory is indirect and contested.

Verbal protocols --- the method Newell and Simon used to support the Problem Space Hypothesis --- provide some evidence for search-like computation. Subjects do report "considering alternatives," "backing up," and "trying a different approach" --- descriptions consistent with search through a problem space. But verbal protocols are incomplete (much of cognition is not verbally accessible), biased (subjects may confabulate post-hoc explanations), and limited to slow, deliberate reasoning (System 2 only).

### Neuroscience Evidence

More direct evidence comes from neuroscience. Several lines of research suggest that the brain performs search-like computation:

**Hippocampal replay.** During decision-making, the hippocampus replays sequences of place cells corresponding to possible future trajectories (Pfeiffer and Foster, 2013). This looks remarkably like tree search: the brain simulates multiple possible paths before committing to one.

**Prefrontal cortex and planning.** The prefrontal cortex, particularly the dorsolateral prefrontal cortex (dlPFC), is activated during planning and deliberate reasoning. Lesions to dlPFC impair the ability to plan ahead --- consistent with a role in search control (metacognition, Chapter 9).

**Neural evidence for heuristic evaluation.** The ventromedial prefrontal cortex (vmPFC) encodes expected value --- a scalar estimate of the quality of the current state. This is functionally equivalent to $h(x)$: a scalar field that estimates the cost-to-go from the current state.

These findings are suggestive but not conclusive. The brain is not a digital computer, and the mapping from neural activity to computational operations is far from established. The geometric framework provides a language in which the hypothesis can be precisely stated --- human deliberation is bounded search on a cognitive manifold with heuristic guidance --- but testing that hypothesis requires advances in both neuroscience and computational modeling that are beyond the current state of either field.

**Open Problem 15.7.** *Can the heuristic field $h(x)$ be identified in human neural activity? Specifically, does vmPFC activation during deliberation correlate with the cost-to-go as predicted by the geometric framework? Can hippocampal replay sequences be mapped onto search trajectories on a cognitive manifold?*

---

## 15.5 Alignment: Can We Shape Heuristics Without Breaking Them?

Chapter 11 established that alignment decomposes into three geometric problems: objective alignment, heuristic quality, and metacognitive calibration. Of these, heuristic shaping --- training interventions that improve the heuristic field's geometry --- was identified as the most tractable. But heuristic shaping faces a fundamental tension that Chapter 11 named the *dual binding problem*: the heuristic must be simultaneously powerful and constrained.

### The Dual Binding Problem Revisited

A powerful heuristic has strong gradients: it provides clear, unambiguous guidance about which direction the search should go. A constrained heuristic has zero gradient in forbidden directions: it does not guide the search toward harmful, deceptive, or misaligned states. **[Speculation/Extension.]** The dual binding requires both simultaneously --- a field that is smooth and informative in the permitted region and discontinuous at the safety boundary.

This is not just an engineering challenge; it is a mathematical one. A smooth scalar field on a manifold cannot simultaneously have strong gradients in the interior and zero gradient at a submanifold of codimension 1 (the safety boundary) unless the field itself has a discontinuity or a very steep gradient at the boundary. Such discontinuities are unstable: small perturbations to the field (from distribution shift, adversarial inputs, or fine-tuning) can open gaps in the safety boundary.

The corruption data from Chapter 5 illustrates the fragility. Framing perturbations that shift the heuristic by 8.9$\sigma$ could, in principle, shift the search trajectory across a safety boundary. The model's heuristic was shaped (by RLHF or equivalent) to avoid harmful outputs, but the shaping was not robust to the specific perturbation direction exploited by the framing manipulation.

### Interpretability as a Prerequisite

If we can see the heuristic field --- if representation engineering (Section 15.2) succeeds in extracting $h(x)$ from transformer activations --- can we also *edit* it? The prospect is tantalizing: identify the direction in activation space corresponding to "sycophancy," and ablate it. Identify the safety boundary in the heuristic field, and reinforce it.

Recent work on activation editing suggests this may be partially feasible. Representation engineering has been used to "steer" model behavior by adding or subtracting vectors in activation space during inference. If the heuristic field is linearly represented (Open Problem 15.5), then adding a correction vector $\Delta h$ to the heuristic direction at each layer could, in principle, correct systematic biases without retraining.

But the risks are significant. The heuristic field is not a single independent variable; it is entangled with the rest of the model's representation. Editing the heuristic direction may have unintended effects on other capabilities --- the geometric analogue of "alignment tax." A correction that eliminates sycophancy might also eliminate appropriate deference. A correction that reinforces the safety boundary might also block legitimate reasoning about dangerous topics.

### Can Alignment Be Geometric?

The deepest question in this section is whether the geometric framework can contribute to alignment theory beyond diagnosis. This book has shown that the framework is productive for *identifying* and *characterizing* misalignment: the gauge violation tensor, the sycophancy gradient, the corruption dose-response curve, the miscalibration surface. These are diagnostic tools. But can the framework guide *interventions* --- not just tell us what is wrong, but tell us how to fix it?

The engineering results of Chapter 14 provide grounds for cautious optimism. Group-theoretic augmentation restored broken symmetries. Adversarial training smoothed the heuristic field. LoRA fine-tuning adjusted local curvature. Each of these interventions was motivated by the geometric framework and implemented successfully. The question is whether the same approach scales to the harder problem of alignment.

**Open Problem 15.8.** *Can the heuristic field be edited (via activation engineering or targeted fine-tuning) to satisfy the dual binding --- strong gradients in the permitted region, zero gradient in forbidden directions --- without degrading general reasoning capability?*

**Open Problem 15.9.** *Is there a geometric characterization of the "alignment tax" --- the loss in reasoning capability that results from safety interventions? Can the tax be minimized by choosing interventions that are geodesic-preserving in the permitted region?*

---

## 15.6 Summary

The open questions catalogued in this chapter span five domains --- theory, mechanisms, evaluation, cognitive science, and alignment --- but they share a common structure. Each asks whether the geometric framework developed in this book can be deepened, extended, or made more precise.

The theoretical questions ask whether Riemannian geometry is sufficient or whether Finsler, sub-Riemannian, stratified, or information-geometric structures are needed. The mechanistic questions ask whether the heuristic field can be measured directly from activations. The evaluation questions ask whether we can distinguish genuine search from memorized retrieval. The cognitive science questions ask whether the framework applies to biological as well as artificial cognition. The alignment questions ask whether we can shape the heuristic field without destroying it.

None of these questions have been answered. But each has been given a precise mathematical formulation --- which is, as Einstein suggested, often more important than the solution itself. The geometric framework does not claim to have solved the problem of reasoning. It claims to have given the problem a structure that makes it tractable. The open questions in this chapter are the evidence for that claim: they are questions that could not have been asked, in their present form, without the framework.

Chapter 16 addresses the final question: what would it look like for geometric reasoning to mature from a framework into a field?
