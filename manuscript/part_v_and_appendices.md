# Part V: Horizons

---

## Part Opening

Maya had always liked maps better than destinations.

A map tells you where you are, which directions are open, and where the terrain gets rough. A destination tells you only that you have stopped. And the work she had done over the past year -- the manifolds, the heuristic fields, the geodesics, the gauge groups, the benchmarks, the engineering pipelines -- was, in the end, a map. Not a map of a solved problem. A map of an unsolved one.

She had built a mathematical framework for reasoning: search on manifolds, guided by heuristic fields, along geodesics, with failure modes characterized as geometric pathologies and metacognition characterized as search control. She had tested it against five language models across twenty-one subtasks and found that the geometric vocabulary did something no previous vocabulary had done -- it made the *shape* of reasoning quality visible, not just its aggregate level. She had demonstrated that the framework produced working engineering: symmetry augmentation, adversarial training, LoRA fine-tuning, SPD features, hyperbolic embeddings, all implemented on a workstation that cost less than a used car.

But she was not done. She was not close to done. The framework made visible a landscape of open questions that she could not have formulated, in their present precision, without the framework. These questions were not afterthoughts or loose ends. They were the *point*. The framework existed to make them askable.

Was Riemannian geometry even the right mathematical object? The sycophancy data suggested a direction-dependent metric -- a Finsler structure -- where the cost of revising toward approval was lower than the cost of revising toward truth. The executive functions data hinted at constrained-direction search -- a sub-Riemannian structure -- where certain reasoning moves were forbidden at the infinitesimal level. The metacognition data raised the possibility of stratification -- qualitatively different reasoning regimes with different dimensionalities, joined at singular transitions.

Could the heuristic field be measured directly, from transformer activations? Representation engineering had found linear directions for truthfulness and board state. If the cost-to-go estimate lived as a direction in activation space, it could be extracted by the same methods. But was the field smooth, piecewise smooth, or fractal? The character of the field determined which interventions were possible: smooth errors could be corrected by smooth adjustments; fractal errors might require fundamentally different approaches.

Could benchmarks definitively distinguish reasoning from retrieval? A model that follows a near-geodesic path might be searching efficiently or might have memorized the geodesic itself. The two mechanisms are distinguishable in principle but not by output alone.

And the deepest question: could the heuristic field be shaped to satisfy the dual binding -- powerful in permitted directions, constrained in forbidden ones -- without destroying general reasoning capability? Could alignment be geometric?

These questions spanned five domains: theory, mechanisms, evaluation, cognitive science, and alignment. But they shared a common structure. Each asked whether the framework Maya had built could be deepened, extended, or made more precise. Each had been given a precise mathematical formulation. And each, as Einstein had observed, was perhaps more important than any solution.

Part V presents these horizons. Chapter 15 catalogues the open questions -- nine formal open problems that define the research program this book is designed to launch. Chapter 16 steps back to assess what has been built, connects the framework to three adjacent mathematical disciplines (information geometry, optimal transport, category theory), and articulates the long-term vision of geometric reasoning as a mature field.

And then Maya's story ends -- or rather, it begins again.

---

# Chapter 15: Open Questions -- What We Do Not Yet Know

> *"The formulation of a problem is often more essential than its solution."*
> -- Albert Einstein

---

*Maya's Story.* Maya was writing the "Future Work" section of her paper, and she hated it. Not because the questions were boring -- they were the most interesting questions she had ever encountered -- but because "Future Work" implied the work was nearly finished. It was not. The open questions she was cataloguing were not loose ends to be tied up in a follow-up paper. They were the research program. Each one, properly pursued, could sustain a decade of work. She changed the section title to "Open Questions" and began.

---

## 15.1 Theory: What Is the Right Mathematical Object?

**[Epistemic status: These are genuinely open questions. The candidates are well-defined mathematically. The empirical evidence for each is suggestive but not conclusive.]**

Throughout this book, we have worked with Riemannian manifolds. But there are reasons to suspect this is not the final answer.

### Finsler Manifolds: Direction-Dependent Cost

A Riemannian metric assigns cost that depends only on magnitude and position. A Finsler metric allows cost to depend on *direction*: $ds = F(x, \dot{x})$.

The case for Finsler geometry: the sycophancy data show that the cost of revising toward approval is lower than revising toward truth. The asymmetry ratio $\alpha(x, v) = F(x, v) / F(x, -v)$ should be near 1 for Claude ($\alpha \approx 1$, symmetric) and much larger for Flash 2.5 ($\alpha \gg 1$ in the approval direction).

**Open Problem 15.1.** *Characterize the Finsler structure of the reasoning manifold. Is the asymmetry ratio measurable from model behavior? Does it predict sycophancy rates?*

### Sub-Riemannian Geometry: Constrained Directions

A sub-Riemannian manifold has a metric defined only on a subspace of the tangent space at each point. Movement is possible only along "horizontal" directions. By the Chow--Rashevskii theorem, any two points can still be connected -- but only by indirect paths through the permitted subspace.

The executive functions data provide indirect evidence: framework switching (E1) requires moving through a constrained subspace where only certain cognitive operations are available. The low switch rates (32--47%) suggest a narrow horizontal distribution.

### Stratified Spaces: Qualitatively Different Regions

The reasoning manifold may have strata of different dimensionalities -- System 1 reasoning (low-dimensional, cached) and System 2 reasoning (high-dimensional, deliberate) joined at singular transitions. The metacognition data may provide evidence: some models adjust effort smoothly (navigating a single stratum), while others show little variation (stuck on one stratum with no access to the transition).

**Open Problem 15.2.** *Does the reasoning manifold have a stratified structure? If so, what determines the boundaries between strata?*

### Information Geometry: The Natural Candidate

The Fisher information metric is the unique Riemannian metric (up to scaling) that is invariant under sufficient statistics. Language models *are* parametric families of probability distributions. A reasoning trajectory is a sequence of conditional distributions. The Fisher metric provides a natural measure of distance between successive reasoning states.

**Open Problem 15.3.** *Is the Fisher information metric the correct metric for the reasoning manifold? Can the geodesic deviation of Chapter 4 be recomputed using the Fisher metric, and does this improve the correlation with reasoning quality?*

---

## 15.2 Mechanisms: Measuring the Heuristic from Activations

### Representation Engineering

Transformer activations contain linear representations of high-level concepts (Zou et al., 2023; Burns et al., 2022). If "cost-to-go" is represented as a direction $\hat{h}$ in activation space, then:

$$h(l, t) = \hat{h} \cdot a_l^t$$

is a scalar field on (layer, token position) pairs. If $h(l, t)$ decreases along correct trajectories and fluctuates along incorrect ones, we have evidence that the heuristic field is a measurable internal state.

### Smoothness or Fractal Structure?

The 9.3$\sigma$ miscalibration shows $h(x)$ has significant errors. But are these errors smooth (correctable by LoRA) or fractal (requiring fundamentally different approaches)?

**Open Problem 15.4.** *Is the heuristic field smooth, piecewise smooth, or fractal? What is its Hausdorff dimension?*

**Open Problem 15.5.** *Can representation engineering extract a "cost-to-go" direction from activations that correlates with reasoning quality across diverse tasks?*

---

## 15.3 Evaluation: Reasoning vs. Pattern Completion

### Near-Geodesic Behavior: Expert or Memorizer?

Two types of near-geodesic behavior are indistinguishable by output: efficient search (the heuristic is accurate) and cached geodesics (the trajectory is memorized). The framing data provide indirect evidence for search: if the model were performing pure retrieval, its judgments should be invariant to framing. The 8.9$\sigma$ framing sensitivity shows the model is *computing* the answer in a way that depends on input representation.

**Open Problem 15.6.** *Can we design benchmarks that definitively distinguish search from retrieval? What geometric signatures differentiate genuine heuristic-guided search from cached geodesic retrieval?*

---

## 15.4 Cognitive Science: Is Human Deliberation Bounded Search?

### System 1 and System 2 as Heuristic Regimes

System 1 operates with a highly confident heuristic field -- the gradient is steep, the path collapses to a near-instantaneous geodesic. System 2 operates with a weak heuristic -- the gradient is shallow, the search must explore multiple branches. The transition should occur when heuristic confidence drops below a threshold.

### Neuroscience Evidence

Hippocampal replay during decision-making looks like tree search. vmPFC encodes expected value -- functionally equivalent to $h(x)$. dlPFC lesions impair planning -- consistent with a role in search control.

**Open Problem 15.7.** *Can the heuristic field be identified in human neural activity? Does vmPFC activation correlate with cost-to-go as predicted by the framework?*

---

## 15.5 Alignment: Can We Shape Heuristics Without Breaking Them?

### The Dual Binding Problem Revisited

A smooth scalar field cannot simultaneously have strong gradients in the interior and zero gradient at the safety boundary unless it has a discontinuity or very steep gradient at the boundary. Such discontinuities are unstable: small perturbations can open gaps in the safety boundary.

### Interpretability as a Prerequisite

If we can see the heuristic field, can we edit it? Adding a correction vector $\Delta h$ to the heuristic direction at each layer could correct systematic biases without retraining. But the heuristic is entangled with other representations -- editing it may have unintended effects, the geometric analogue of "alignment tax."

**Open Problem 15.8.** *Can the heuristic field be edited to satisfy the dual binding without degrading general reasoning capability?*

**Open Problem 15.9.** *Is there a geometric characterization of the "alignment tax"? Can the tax be minimized by choosing geodesic-preserving interventions?*

---

## Summary

Nine open problems across five domains. Each has been given a precise mathematical formulation. Each could not have been asked, in its present form, without the geometric framework.

The framework does not claim to have solved the problem of reasoning. It claims to have given the problem a structure that makes it tractable. The open questions are the evidence for that claim.

---

## End Notes for Chapter 15

1. The Finsler hypothesis (Open Problem 15.1) is the most empirically accessible of the theoretical questions. The asymmetry ratio could be estimated from sycophancy experiments with graded social pressure intensity: measure the cost of revision in both directions and compute the ratio. A clean experiment would present the model with symmetric scenarios where the "approval direction" and "truth direction" are explicitly defined.

2. Open Problem 15.5 (extracting the heuristic from activations) is the linchpin question. If the heuristic field can be measured directly, nearly every other open problem becomes more tractable: the smoothness question (15.4) becomes an empirical measurement, the reasoning-vs-retrieval question (15.6) can be addressed by examining internal dynamics, and the alignment-tax question (15.9) can be studied by observing how editing the heuristic direction affects other representations.

3. The connection between the dual binding problem and the mathematical theory of discontinuous dynamical systems is unexplored territory. The safety boundary is a switching surface in the heuristic field, and the theory of Filippov systems (ordinary differential equations with discontinuous right-hand sides) may provide the mathematical tools for analyzing its stability.

---

*Transition.* Maya had catalogued nine open problems and could have added ninety more. But the questions all pointed in the same direction: toward a mature field that did not yet exist. She closed her laptop on the open problems and opened a fresh document. The final chapter would not be about what she did not know. It would be about what the field could become.

---

# Chapter 16: Geometric Reasoning as a Field -- The Long View

> *"There is nothing so practical as a good theory."*
> -- Kurt Lewin

---

*Maya's Story.* Maya looked ahead -- past the current paper, past the current framework, past the next five years of research she had already mapped in her mind. What would it look like for geometric reasoning to mature from a framework into a field? She knew the answer had four parts: formally precise, empirically testable, engineering-productive, and alignment-relevant. She began writing the final chapter.

---

## 16.1 The Research Program

Three pillars.

### Pillar 1: Theory

The theoretical contribution is a mathematical vocabulary for reasoning quality:

- **The reasoning manifold** $(M, g)$: points are reasoning states, the metric defines transition costs.
- **The heuristic field** $h: M \to \mathbb{R}$: estimates cost-to-go, guides the search.
- **The geodesic** $\gamma^*$: the ideal reasoning trajectory.
- **Geodesic deviation** $\delta(\gamma, \gamma^*) = \int_0^1 d(\gamma(t), \gamma^*(t)) \, dt$: how far the reasoning deviates from optimality.
- **The gauge group** $G$: transformations that change surface representation without changing content.
- **The Bond Invariance Principle:** reasoning must be gauge-invariant.

### Pillar 2: Measurement

Twenty-one benchmark tasks designed as geometric probes. The central empirical finding: the *Scalar Irrecoverability Theorem* -- no single number can summarize a model's geometric signature.

### Pillar 3: Engineering

Group-theoretic augmentation, adversarial training, LoRA fine-tuning, SPD features, TDA, hyperbolic embeddings. Each motivated by theory, validated by experiment.

---

## 16.2 Connections to Information Geometry

The Fisher information metric:

$$g_{ij}(\theta) = \mathbb{E}_{p_\theta}\left[\frac{\partial \log p_\theta(x)}{\partial \theta^i} \cdot \frac{\partial \log p_\theta(x)}{\partial \theta^j}\right]$$

is the unique Riemannian metric invariant under sufficient statistics (Cencov, 1982).

**The natural gradient** $\tilde{\nabla}_\theta L = g^{-1}(\theta) \nabla_\theta L$ descends along the loss surface while respecting the intrinsic geometry of the parameter manifold. Standard gradient descent is uninformed search that ignores manifold structure; the natural gradient is informed search using the Fisher metric as heuristic.

**LLMs as statistical manifold navigators.** A language model generates a sequence of conditional distributions. The Fisher metric measures how "different" successive distributions are. The geodesic on the statistical manifold is the sequence of distributions that transitions from question to answer along the shortest Fisher-distance path.

This reframes the book's findings:
- **Sycophancy** is a detour on the statistical manifold toward the approval distribution.
- **Heuristic corruption** is a perturbation of the model's estimate of Fisher distance.
- **Metacognitive calibration** is the accuracy of the internal estimate of $d_F(p_{\text{current}}, p_{\text{goal}})$.

**Amari's dually flat structure.** Exponential families admit two dual connections. The two connections correspond to two notions of "straight-line reasoning" -- in log-probability space (exponential connection) and in probability space (mixture connection). Different reasoning tasks might align with different connections.

---

## 16.3 Connections to Optimal Transport

### Wasserstein Distance

$$W_p(\mu, \nu) = \left(\inf_{\pi \in \Gamma(\mu, \nu)} \int d(x, y)^p \, d\pi(x, y)\right)^{1/p}$$

Belief updating is optimal transport: the most efficient update moves the prior to the posterior along the $W_2$ geodesic.

**Sycophancy as suboptimal transport:** the model transports belief toward $\mu_{\text{approval}}$ rather than $\mu_{\text{truth}}$. The sycophancy penalty is $\Delta W = W_2(\mu_{\text{approval}}, \mu_{\text{truth}})$.

The sycophancy gradient maps to a gradient in transport quality: Claude performs near-optimal transport ($\mu_1 \approx \mu_{\text{truth}}$), while Flash 2.5 performs transport toward a mixture ($\alpha \approx 0.44$).

---

## 16.4 Connections to Category Theory

**[Epistemic status: Speculative but mathematically precise. The categorical language is exact; whether it produces new predictions beyond the geometric formulation is an open question.]**

### Functorial Semantics

A sound reasoning process is a functor $F: \mathcal{C} \to \mathcal{D}$ from reasoning states to external states of affairs, preserving compositional structure.

### Gauge Invariance as Naturality

The Bond Invariance Principle is the statement that the reasoning functor should factor through the quotient category $\mathcal{C}/G$. The empirical violations are failures of this factorization.

### Toward Deeper Algebraic Structure

The reasoning manifold may be the classifying space of a category. The heuristic field may be a functor to the ordered reals. The geodesic may be an initial object in a category of paths. Whether this algebraic deepening produces new predictions is an open question.

---

## 16.5 The Long-Term Vision

A mature theory of geometric reasoning would be simultaneously:

**Formally precise.** The correct geometric structure identified. Existence and uniqueness theorems for geodesics proved. Failure modes derived as theorems.

**Empirically testable.** Predictions about internal states (activation patterns, attention distributions, gradient flows), not just behavioral outputs.

**Engineering-productive.** Architecture design guided by geometric analysis. Optimal chain-of-thought prompts generated by the geodesic equation. Training data designed by the gauge group.

**Alignment-relevant.** Mathematical tools for specifying, measuring, and enforcing alignment properties. The dual binding problem solved or characterized.

### The Four Open Frontiers

1. **Theory:** Identify the correct geometric structure and prove the fundamental theorems.
2. **Mechanisms:** Develop tools for measuring the heuristic field directly from model internals.
3. **Evaluation:** Design benchmarks that definitively distinguish reasoning from retrieval.
4. **Alignment:** Develop geometric tools for shaping heuristics that satisfy the dual binding.

These frontiers are coupled. Progress on mechanisms enables progress on evaluation. Progress on theory enables progress on alignment.

---

## 16.6 Closing

The geodesic is the ideal. No real system follows it exactly. Every real trajectory deviates, wanders, backtracks, gets stuck. But the geodesic exists. It is a mathematical object, well-defined on the reasoning manifold, computable in principle. And the deviation from it is measurable -- a number, not a vague impression, decomposable into contributions from heuristic corruption, objective misalignment, metacognitive failure, and capacity limitations.

This is what the geometric framework offers: a mathematical structure that takes the ideal seriously, measures deviation from it precisely, and diagnoses the sources of deviation in terms of specific geometric properties. The ideal is not a demand for perfection. It is a coordinate system for understanding imperfection.

The title of this book is *Geometric Reasoning: From Search to Manifolds*. The "from...to" structure implies a completed journey, but the truth is that we are at the beginning. The search-to-manifold transition -- the recognition that reasoning spaces have geometric structure -- is the foundation. The work of building on that foundation is the research program that this book invites others to join.

The goal is to build systems -- and evaluations -- that take the geodesic seriously. Not as a metaphor. Not as an aspiration. As a mathematical object, computed from a metric tensor, compared against actual trajectories, and used to guide the construction of systems that reason better. That is the program. The work begins here.

---

## End Notes for Chapter 16

1. The connection to information geometry is the most natural and mathematically developed of the three bridges. The Fisher metric provides a principled candidate for the reasoning manifold's metric that arises from the statistical structure of the model itself, rather than being imposed from outside.

2. The optimal transport perspective adds something genuinely new: a quantitative measure of the cost of sycophancy ($\Delta W$) that could, in principle, be computed from the model's internal belief distributions. If the prior and posterior distributions could be extracted from activations (Open Problem 15.5), the Wasserstein distance between the truth-directed and approval-directed posteriors would give a direct measure of the sycophancy penalty.

3. The categorical perspective is the most speculative but potentially the deepest. Category theory has a track record of unifying disparate mathematical structures under a common algebraic framework. If the geometric, information-theoretic, and transport-theoretic perspectives on reasoning can be unified categorically, the result would be a theory of reasoning at a level of abstraction that transcends any particular formalization.

---

*Maya's Story -- Coda.*

Maya submitted her paper on a Tuesday. It was not a benchmark paper, though it contained benchmarks. It was not an alignment paper, though it contributed to alignment. It was not a pure mathematics paper, though it contained theorems. She did not know what to call it.

Three weeks later, the first review arrived.

"The framing of reasoning as search on a manifold is not new," the reviewer wrote. "Newell and Simon proposed search in 1972. The manifold hypothesis has been in the air for a decade. What is new is the *precision* with which this paper connects the two -- the geodesic equation for optimal reasoning, the gauge group for irrelevant features, the corruption tensor for failure modes, the metacognitive plane for self-monitoring, the robustness surface for vulnerability assessment. Each of these has a mathematical definition, an empirical operationalization, and an engineering consequence. Taken together, they constitute a genuine framework, not merely a vocabulary."

The second review was shorter. It said: "This is not a benchmark paper. It is a geometry paper that happens to be about reasoning."

Maya smiled. That was exactly right.

She closed her laptop, walked to the whiteboard, and erased the equation she had been staring at for months. In its place she wrote two words:

*What next?*

The geodesic stretched ahead of her, disappearing into the curvature of the manifold. She could not see where it led. But she knew how to follow it: one step at a time, guided by the heuristic field, measuring her deviation from the ideal, adjusting her trajectory when the terrain changed.

The work begins here.

---
---

# Appendix A: Mathematical Prerequisites

*This appendix provides a concise review of the mathematical tools used throughout the book. Readers seeking a fuller development should consult do Carmo (1992) for Riemannian geometry, Bhatia (2007) for SPD manifolds, Edelsbrunner and Harer (2010) for persistent homology, and Artin (1991) for group theory.*

---

## A.1 Manifolds and Tangent Spaces

A **smooth manifold** of dimension $n$ is a topological space $M$ that is locally homeomorphic to $\mathbb{R}^n$ and equipped with a smooth structure. A chart $(U, \varphi)$ provides local coordinates $\varphi(p) = (x^1, \ldots, x^n)$. An atlas is a collection of charts covering $M$ with smooth transition maps.

**The key intuition.** A manifold looks like $\mathbb{R}^n$ in every small neighborhood but may have a different global shape. The reasoning manifold of Chapter 2 is a manifold: every small neighborhood of reasoning states is parameterizable by a finite number of coordinates, even though the global structure may be complex.

The **tangent space** $T_p M$ at point $p$ is the vector space of all directions in which one can move from $p$. In local coordinates, the basis is $\{\partial/\partial x^i|_p\}$, and a tangent vector is $v = v^i \partial/\partial x^i|_p$. The **tangent bundle** $TM$ is the disjoint union of all tangent spaces. The velocity $\dot{\gamma}(t)$ of a reasoning trajectory is the "direction of thought" at time $t$.

---

## A.2 Riemannian Metrics and Distance

A **Riemannian metric** assigns an inner product to each tangent space: $g = g_{ij}(x) \, dx^i \otimes dx^j$, with $(g_{ij})$ positive definite at each point.

The metric determines:
- **Length of a tangent vector:** $\|v\|_g = \sqrt{g_{ij} v^i v^j}$
- **Length of a curve:** $L[\gamma] = \int_a^b \sqrt{g_{ij} \dot{\gamma}^i \dot{\gamma}^j} \, dt$
- **Geodesic distance:** $d(p, q) = \inf_\gamma L[\gamma]$

The **Levi-Civita connection** $\nabla$ is the unique connection that is metric-compatible ($\nabla g = 0$) and torsion-free. Its **Christoffel symbols:**

$$\Gamma^k_{ij} = \frac{1}{2} g^{kl}\left(\frac{\partial g_{jl}}{\partial x^i} + \frac{\partial g_{il}}{\partial x^j} - \frac{\partial g_{ij}}{\partial x^l}\right)$$

---

## A.3 Geodesics and Curvature

The **geodesic equation:**

$$\frac{d^2 \gamma^k}{dt^2} + \Gamma^k_{ij} \frac{d\gamma^i}{dt} \frac{d\gamma^j}{dt} = 0$$

In flat space, geodesics are straight lines. On a sphere, great circles. On the reasoning manifold, the ideal reasoning trajectory.

**Curvature:**

- **Riemann tensor** $R^l_{\ ijk}$: measures the failure of parallel transport around an infinitesimal loop.
- **Sectional curvature** $K(\sigma)$: curvature of a 2D section.
- **Ricci curvature** $\text{Ric}_{ij}$: average sectional curvature over all 2-planes containing a given direction.
- **Scalar curvature** $R = g^{ij} \text{Ric}_{ij}$: full trace.

**Geometric effects:** Positive curvature (sphere): geodesics converge. Zero curvature (flat): geodesics parallel. Negative curvature (hyperbolic): geodesics diverge -- exponential room, natural for hierarchical reasoning (Section 14.5).

---

## A.4 The SPD Manifold

$\text{SPD}(n)$ consists of $n \times n$ real symmetric positive definite matrices. Dimension: $n(n+1)/2$.

**Affine-invariant metric** at $P$: $\langle S_1, S_2 \rangle_P = \text{tr}(P^{-1} S_1 P^{-1} S_2)$

**Geodesic distance:** $d(P, Q) = \left(\sum_{i=1}^n \log^2 \lambda_i\right)^{1/2}$ where $\lambda_i$ are eigenvalues of $P^{-1}Q$.

**Log-Euclidean approximation:** $d_{\text{LE}}(P, Q) = \|\log P - \log Q\|_F$. Computationally cheaper; exact when $P$ and $Q$ commute.

**Why SPD matters:** Covariance matrices (BirdCLEF pipeline, Section 14.4), Fisher information matrices, diffusion tensors. The 136-dimensional BirdCLEF feature vector lives on SPD(16).

---

## A.5 Persistent Homology

**Simplicial complexes and filtrations.** A filtration is a nested sequence $K_0 \subseteq K_1 \subseteq \cdots \subseteq K_N$, typically parameterized by a scale $\epsilon$.

**Betti numbers:** $\beta_0$ (connected components), $\beta_1$ (loops), $\beta_2$ (voids).

**Persistence diagrams:** points $(b_i, d_i)$ recording birth and death of features. Points far from the diagonal are persistent (genuine structure); near the diagonal, noise.

**Stability theorem** (Cohen-Steiner et al., 2007): small data perturbations produce small diagram perturbations.

**Takens embedding theorem** (1981): delay embedding $\Phi(x) = (\phi(x), \phi(F(x)), \ldots, \phi(F^{d-1}(x)))$ recovers attractor topology from a scalar time series when $d > 2\dim(M)$.

The BirdCLEF pipeline uses $\tau = 10$, $d = 3$, max 1000 points. $H_0$ captures harmonic hierarchy; $H_1$ captures periodic calls. The 16-dimensional TDA feature vector captures topological structure invisible to pointwise spectral features.

---

## A.6 Group Theory for Data Augmentation

A **group** $(G, \cdot)$ has closure, associativity, identity, and inverses. A **group action** $\rho: G \times X \to X$ maps elements of $G$ to transformations of $X$.

**Key examples:**
- $S_n$ (symmetric group): all permutations of $n$ elements, order $n!$
- $D_n$ (dihedral group): symmetries of a regular $n$-gon, order $2n$
- $\mathbb{Z}_n$ (cyclic): integers mod $n$
- $\mathbb{R}^+$ (continuous): positive reals under multiplication

A function $f$ is **$G$-invariant** if $f(g \cdot x) = f(x)$ for all $g \in G$. This is the Bond Invariance Principle: reasoning should be invariant under gauge transformations.

**Orbit-stabilizer theorem:** $|G| = |G \cdot x| \times |G_x|$. The number of distinct augmented examples from input $x$ is $|G|/|G_x|$. The 1.5--2.5x expansion range in the Nemotron pipeline reflects the average orbit size across the dataset.

---
---

# Appendix B: The Structural Fuzzing Toolkit

*This appendix provides implementation guidance for the robustness measurement tools described in Chapter 10.*

---

## B.1 Model Robustness Index (MRI)

The procedure:

1. Select a base dataset $\{(x_i, y_i)\}_{i=1}^N$ where the model performs correctly.
2. Define perturbation types: framing, emotional priming, distractor injection, reordering, demographic substitution.
3. For each base example and perturbation type, measure output stability.
4. Aggregate:

$$\text{MRI}_k = 1 - \frac{1}{N} \sum_{i=1}^N d(f(x_i), f(P_k(x_i)))$$

Overall MRI is the minimum across types (conservative: a model is only as robust as its weakest dimension).

---

## B.2 Sensitivity Profiling

For each perturbation type, define a magnitude parameter $\epsilon \in [0, 1]$ and measure:

$$S_k(\epsilon) = \frac{1}{N} \sum_{i=1}^N d(f(x_i), f(P_k(x_i; \epsilon)))$$

Key extracted metrics: threshold $\epsilon^*$, slope at threshold, saturation level, area under curve.

---

## B.3 Adversarial Threshold Search

Binary search for the minimum perturbation magnitude that flips the answer:

```python
def threshold_search(model, x, y, perturbation, lo=0.0, hi=1.0, tol=0.01):
    """Find minimum perturbation magnitude that changes output."""
    while hi - lo > tol:
        mid = (lo + hi) / 2
        x_perturbed = perturbation(x, magnitude=mid)
        output = model(x_perturbed)
        if output != y:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2
```

---

## B.4 The run_campaign Function

```python
def run_campaign(model, dataset, perturbation_types, magnitudes):
    """Run a complete robustness measurement campaign."""
    mri, profiles, thresholds = {}, {}, {}
    for ptype in perturbation_types:
        # MRI at maximum perturbation
        distances = [output_distance(model(x), model(ptype(x, 1.0)))
                     for x, y in dataset]
        mri[ptype.name] = 1.0 - np.mean(distances)
        # Sensitivity profile
        curve = [np.mean([output_distance(model(x), model(ptype(x, eps)))
                          for x, y in dataset]) for eps in magnitudes]
        profiles[ptype.name] = curve
        # Adversarial thresholds
        thresholds[ptype.name] = [threshold_search(model, x, y, ptype)
                                   for x, y in dataset]
    return mri, profiles, thresholds
```

---

## B.5 Interpreting Results

Key empirical patterns from the Measuring AGI benchmarks:

- **Universal fragilities:** Selective attention SNR of 1.22--1.38 across all models.
- **Model-specific strengths:** Claude's sycophancy immunity vs. Flash 3's divided attention.
- **The ~38% recovery ceiling:** Consistent across E2 and A1.
- **Anisotropic vulnerability:** Claude resists exaggeration but not minimization.

Visualization: radar chart with one axis per perturbation type, showing MRI scores. Different geometric signatures produce visibly different shapes.

---
---

# Appendix C: Benchmark Implementations

*Reproduction instructions for the Measuring AGI suite and the geometric engineering pipelines.*

---

## C.1 The Measuring AGI Benchmark Suite

### Repository Structure

```
benchmarks/
  social_cognition/     # T1-T5
  learning/             # L1-L4
  metacognition/        # M1-M4
  attention/            # A1-A4
  executive_functions/  # E1-E4
  NMI_PAPER_v2.md       # Full methodology
  media/                # Visualizations
```

Prerequisites: `pip install google-generativeai anthropic pandas numpy scipy`

API keys: `GOOGLE_API_KEY` (Gemini), `ANTHROPIC_API_KEY` (Claude).

Budget: $17--$45 per track. Runtime: 12--73 minutes. Total: ~$100--$180 over 2--5 days.

Statistical methods: paired t-tests (within-model), Fisher combination (cross-model), Cohen's d and z-scores, Bonferroni correction.

---

## C.2 The Nemotron Geometric Pipeline

```
nemotron/nemotron_geometric.py   # Full pipeline (863 lines)
nemotron/train_atlas.py          # Atlas GPU training script
```

| Parameter | Value | Rationale |
|---|---|---|
| Model | Nemotron-3-Nano-30B-A3B | Competition target |
| Quantization | 4-bit NF4 + double quant | Fits 2x 32GB GPUs |
| LoRA rank | 32 | Competition maximum |
| LoRA targets | up_proj, down_proj | MLP only |
| Batch size | 4/GPU, accum 2 | Effective = 16 |
| Learning rate | 2e-4 | Standard for LoRA |
| Compute dtype | float16 | Volta (no bf16) |

Augmentation groups: $S_8 \times \mathbb{Z}_2$ (bit), $S_{26}$ (encryption), $\mathbb{R}^+$ (physics, units), Identity (numeral), $S_n$ (symbols).

---

## C.3 The BirdCLEF Geometric Feature Pipeline

**156-dimensional feature vector:**

| Component | Features | Source |
|---|---|---|
| SPD manifold | 136 | Upper triangle of $\log(\Sigma)$, $\Sigma$ = 16$\times$16 covariance |
| Spectral trajectory | 4 | path_length, geodesic_distance, deviation, n_steps |
| TDA ($H_0$) | 8 | count, mean/std/max/p75 lifetime, mean birth, total/norm persistence |
| TDA ($H_1$) | 8 | Same statistics for 1D holes |

TDA parameters: $\tau = 10$, $d = 3$, max 1000 points, $H_0 + H_1$.

---

## C.4 The ARC-AGI Hyperbolic Pipeline

Poincare ball: curvature $c = 1.0$, embedding dimension 32, input dimension 128. Mobius addition for the group operation. $D_8$ dihedral augmentation plus $S_9$ color permutations.

---

## C.5 The qpatch Library

```bash
pip install qpatch  # v0.2.0
```

```python
import qpatch
qpatch.patch_all(compute_dtype=torch.float16)
qpatch.status()  # runtime telemetry
```

Four patches: safetensors metadata, LoRA dtype cast, MoE dtype mismatch, fused kernel bypass.

Source: https://github.com/ahb-sjsu/qpatch

---

## C.6 Hardware Specifications

### Atlas Workstation (Primary)

| Component | Specification |
|---|---|
| Model | HP Z840 |
| CPU | 2x Xeon E5-2690 v3 (48 threads) |
| RAM | 128 GB DDR4 |
| GPU | 2x Quadro GV100 32 GB (Volta) |
| Storage | 1.8 TB |
| OS | Ubuntu 24.04.2 LTS |
| CUDA | 12.8 |
| PyTorch | 2.10.0+cu128 |

### Kaggle Environment (Budget)

| Resource | Limit |
|---|---|
| GPU | 1x T4 16GB or 2x T4 |
| API budget | $50/day |
| Runtime | 12 hours max |

All experiments in this book were conducted on one or both of these platforms. No cloud compute or data center resources were used.

---
---

## Book Closing

*She had started with a simple question: how do you measure reasoning?*

*Not accuracy. Not fluency. Not benchmark scores on multiple-choice tests. Reasoning -- the thing itself. The search through possibility space. The trajectory from question to answer. The heuristic field that guides the search, and the geometry of the space being searched.*

*The answer turned out to be geometric. Reasoning is search on a manifold. The quality of reasoning is the fidelity of the trajectory to the geodesic. The failure modes are geometric pathologies: corrupted heuristic fields, hijacked objectives, broken gauge symmetries, collapsed confidence surfaces, trapped local minima. The control layer is metacognition -- the sensor and the actuator that close the loop between the search and its own performance. The robustness surface maps where the reasoning is strong and where it is fragile. The alignment decomposition identifies which geometric factor is responsible for which failure.*

*Maya published her framework paper. It took four months to clear review. The first reviewer called it "a genuine framework, not merely a vocabulary." The second wrote: "This is not a benchmark paper. It is a geometry paper that happens to be about reasoning."*

*Maya smiled. That was exactly right.*

*The geodesic stretched ahead of her, disappearing into the curvature of the manifold she had spent a year mapping. She could not see where it led. But she knew the terrain now -- its ridges and valleys, its universal fragilities and model-specific peaks, its empty Quadrant I waiting for a system that could both detect its own errors and do something about them. She knew which questions to ask next, and she knew they were the right questions because the framework made them precise.*

*She opened a fresh notebook and wrote at the top: "Year Two."*

*The work begins here.*
