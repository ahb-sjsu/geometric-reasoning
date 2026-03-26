# Chapter 3: The Heuristic Field

> *"Every act of reasoning is a bet about where the answer lives."*

> **RUNNING EXAMPLE — DR. OKAFOR'S TRIAGE**
>
> *Dr. Amara Okafor does not consult a decision tree when she walks into the ER. She walks in, and the room organizes itself. Chest pain radiating to the left arm — high urgency, steep gradient pulling her attention. Skateboard abrasion, bleeding but superficial — low urgency, the field nearly flat. Sudden thunderclap headache — an intermediate ridge, ambiguous, the gradient pointing two ways at once.*
>
> *What she carries, after twenty years of emergency medicine, is not a checklist but a field: a scalar function defined over the space of clinical presentations, assigning to each configuration an estimated distance from disaster. That function is her heuristic field, and its gradient is the force that organizes her attention before she has consciously registered why. The field has topology. There are saddle points — presentations where two diagnoses are equally likely and the gradient offers no clear direction. There are basins — clusters of symptoms that reliably funnel toward a single diagnosis. There are ridges — clinical boundaries where a small change in presentation (sharp versus dull chest pain, unilateral versus bilateral headache) flips the gradient entirely, sending the search into a different diagnostic valley.*
>
> *This chapter gives Dr. Okafor's intuition a mathematical name. The heuristic field is not a metaphor for clinical experience — it is a precise description of what clinical experience computes.*

In Chapter 1, we established that reasoning is search over a structured possibility space. In Chapter 2, we gave that space geometric structure — a manifold equipped with a metric, curvature, and boundaries. But a manifold alone does not explain how a reasoner navigates it. A chess player does not enumerate all possible games; a mathematician does not traverse every chain of logical implications; a language model does not assign equal probability to every token. Something guides the search. Something tells the reasoner where to look next.

That something is the **heuristic field**.

This chapter makes a simple but far-reaching claim: the quality of reasoning is determined by the quality of the heuristic field that guides it. A perfect heuristic yields perfect reasoning. A corrupted heuristic yields corrupted reasoning. And the specific ways in which the heuristic can fail — overestimation, underestimation, discontinuity, flat regions — produce specific, diagnosable pathologies in the reasoning trajectory.

We begin with the formal definition of what a heuristic actually is, mathematically. We then reinterpret the classical A* algorithm as gradient descent on an evaluation landscape, revealing how the geometry of the heuristic field shapes search behavior. We extend this framework to neural networks, showing how attention mechanisms implement heuristic guidance. And we close with the central empirical finding: current language models have systematically corrupted heuristic fields, and this corruption has measurable, predictable consequences.

---

## 3.1 The Heuristic as Scalar Field

### 3.1.1 The Standard Definition

In the classical AI literature, a heuristic function $h(x)$ is defined as an estimate of the cost to reach a goal state from state $x$. If $h^*(x)$ denotes the true optimal cost-to-go, then $h(x) \approx h^*(x)$ is the aspiration — a function that tells us, at every point in the search space, how far we are from where we want to be.

This definition is typically presented in the context of discrete graph search. State $x$ is a node. The goal is another node, or a set of nodes. The cost is measured along edges. The heuristic assigns a number to each node.

But this framing obscures what is really going on. Let us restate it precisely.

### 3.1.2 The Geometric Restatement

Let $M$ be the state manifold — the space of all possible states of the reasoning system, equipped with the geometric structure developed in Chapter 2. Let $\mathcal{G} \subset M$ be the goal set — the region of states that constitute acceptable answers, solutions, or conclusions.

A **heuristic** is a smooth function

$$h: M \to \mathbb{R}$$

that assigns to every state $x \in M$ a real number $h(x)$ representing the estimated cost of reaching $\mathcal{G}$ from $x$.

**[Modeling Axiom.]** This is, formally, a **scalar field** on $M$. It is the same mathematical object as a temperature field in thermodynamics, a potential energy surface in physics, or a loss landscape in machine learning. It assigns a single real number to every point in the space.

More precisely, $h$ is a section of the trivial real line bundle $M \times \mathbb{R} \to M$. This seemingly pedantic observation matters because it tells us how $h$ transforms under changes of coordinates. When we change our representation of the state space — say, by moving from one parameterization of a neural network's internal state to another — the heuristic values must transform accordingly. The heuristic is not a property of any particular coordinate system; it is a geometric invariant of the state manifold.

### 3.1.3 What the Heuristic "Looks Like"

Imagine the state manifold as a landscape, with the heuristic value at each point determining the elevation. The goal states sit in the lowest valleys — regions where $h(x) \approx 0$. States far from the goal sit on high plateaus or mountain peaks. The contour lines of $h$ — the level sets $\{x : h(x) = c\}$ — are "isoheuristic surfaces," sets of states that the heuristic judges to be equidistant from the goal.

A perfect heuristic $h = h^*$ produces a landscape whose level sets are exactly the true equicost surfaces. The valleys are precisely where the solutions are, the ridges separate distinct solution basins, and the elevation at every point accurately reflects the true remaining effort.

An imperfect heuristic produces a warped landscape. Some valleys are illusory — the reasoner descends into them expecting to find a solution, but none exists. Some true solutions are hidden behind ridges that the heuristic places too high. The topology of the landscape may differ from reality: the heuristic might merge distinct solution basins into one, or fracture a single basin into several disconnected pieces.

### 3.1.4 The Gradient of the Heuristic

Because $h$ is a scalar field on a manifold, it has a gradient: $\nabla h$, a vector field that points in the direction of steepest increase in $h$. The negative gradient $-\nabla h$ points toward steepest decrease — toward lower heuristic values, toward the goal.

This gradient field is the core navigational signal. A reasoner following $-\nabla h$ is moving in the direction that the heuristic judges to be most promising. The integral curves of $-\nabla h$ — the paths that always follow the direction of steepest descent — are the "heuristic streamlines," the trajectories that the heuristic itself recommends.

When the heuristic is perfect, the streamlines approximate geodesics on $M$ — the optimal reasoning paths discussed in Chapter 4. When the heuristic is imperfect, the streamlines deviate from geodesics, and the nature of the deviation diagnoses the nature of the heuristic's imperfection.

---

## 3.2 A* as Gradient Descent on the Evaluation Landscape

### 3.2.1 The Evaluation Function

The A* search algorithm, introduced by Hart, Nilsson, and Raphael (1968), uses an evaluation function

$$f(x) = g(x) + h(x)$$

where $g(x)$ is the cost already incurred to reach state $x$ from the start state, and $h(x)$ is the heuristic estimate of the remaining cost. The algorithm always expands the state with the lowest $f$-value — the state that appears to lie on the cheapest total path from start to goal.

The standard presentation describes this as "selecting the node with the lowest estimated total cost." This is correct but does not capture the geometric content of the operation.

### 3.2.2 The f-Landscape

Consider the function $f: M \to \mathbb{R}$ as a scalar field in its own right. It defines a landscape — the **evaluation landscape** or **f-landscape** — that combines two sources of information: what the search has already paid ($g$) and what it expects to pay ($h$).

As the search progresses, $g(x)$ changes — the known costs get updated as new paths are discovered. But $h(x)$ is fixed by the heuristic. So the f-landscape is a dynamic surface: the $g$-component evolves while the $h$-component is static. The search proceeds by descending this evolving landscape.

At each step, A* selects the state with minimal $f$-value. This is precisely the operation of finding the lowest point on the current f-landscape's frontier — the boundary between explored and unexplored territory. A* is performing **discrete gradient descent** on the f-landscape, stepping to the lowest neighboring point at each iteration.

### 3.2.3 The Continuous Limit

In the continuous limit — when the state space becomes a manifold and the discrete steps become infinitesimal — A* becomes gradient flow on the f-landscape. The search trajectory satisfies

$$\frac{dx}{dt} = -\nabla f(x) = -\nabla g(x) - \nabla h(x)$$

This is a dynamical system. The search trajectory is a solution curve of this ODE. The behavior of the search is determined by the geometry of the f-landscape: its critical points, its basins of attraction, its saddle structures, its ridgelines.

- **Minima of $f$** are attractors of the search — states toward which the search converges. True solutions correspond to global minima. Local minima of $f$ that are not true solutions are traps — the search converges to them but finds no solution.

- **Saddle points of $f$** are decision points — states where the search must choose between descending into one basin or another. The search's behavior at saddle points determines which solution basin it enters.

- **Ridgelines of $f$** are barriers — the search must climb over them to move between basins. If the ridgelines are too high, the search is trapped in its current basin even if better solutions exist in adjacent basins.

- **Plateaus of $f$** are regions where $\nabla f \approx 0$ — the search has no gradient signal and wanders without direction. These are the "dead zones" we will examine in Chapter 7.

### 3.2.4 Why This Reinterpretation Matters

The standard proof that A* is optimal — that it finds the shortest path when $h$ is admissible and consistent — is an algebraic argument about node expansions. The geometric reinterpretation adds a layer of understanding that the algebraic proof does not provide.

When A* fails to find the optimal path (because $h$ is inadmissible), the geometric view tells us *how* it fails: the f-landscape has a false valley that captures the search before it reaches the true minimum. When A* is slow (because $h$ is uninformative), the geometric view tells us *why*: the f-landscape is flat, providing no gradient signal to direct the search. When A* revisits states (because $h$ is inconsistent), the geometric view tells us *what is happening*: the f-landscape has wrinkles that cause the gradient flow to circle back on itself.

This geometric perspective transfers directly to reasoning systems that are not explicitly running A*. Any system that maintains an estimate of "how far am I from the goal" and uses that estimate to decide what to do next is navigating an evaluation landscape. The geometry of that landscape — which is determined by the quality of the heuristic — governs the system's reasoning behavior.

---

## 3.3 Properties of Good Heuristics: Admissibility and Consistency

### 3.3.1 Admissibility

A heuristic $h$ is **admissible** if it never overestimates the true cost to reach the goal:

$$\forall x \in M: \quad h(x) \leq h^*(x)$$

where $h^*(x)$ is the true optimal cost-to-go. This condition means the heuristic is **optimistic**: it always believes the goal is at least as close as it actually is, or closer.

**[Established Mathematics.]** The celebrated theorem of Hart, Nilsson, and Raphael (1968) states that if $h$ is admissible, then A* finds an optimal path. The geometric content of this theorem is illuminating: admissibility means the f-landscape never has false valleys below the true minimum. Every valley in the f-landscape that is lower than the true solution's valley corresponds to a path that the heuristic judges as cheaper than optimal — but admissibility forbids this. So the true solution's valley is always the deepest, and gradient descent on the f-landscape always finds it.

The converse is equally important: **if the heuristic overestimates** — if there exist states where $h(x) > h^*(x)$ — then the f-landscape can develop false valleys. The search may descend into one of these false valleys and declare a suboptimal solution to be optimal. The magnitude of the overestimation determines the depth of the false valley, and hence the likelihood and severity of the error.

### 3.3.2 Consistency

A heuristic $h$ is **consistent** (also called monotone) if it satisfies the triangle inequality:

$$\forall x, y \in M: \quad h(x) \leq c(x, y) + h(y)$$

where $c(x, y)$ is the cost of moving from $x$ to $y$. Consistency means the heuristic's estimates are mutually coherent — the estimated cost at $x$ is never more than the estimated cost at $y$ plus the cost of getting from $x$ to $y$.

Geometrically, consistency means the f-landscape is **monotonically non-decreasing** along any path away from the goal. There are no "dips" or "wrinkles" in the f-landscape that would cause the search to encounter a lower f-value after passing through a higher one. This ensures that the gradient flow never reverses — the search never needs to backtrack.

Consistency implies admissibility (by induction on the path to the goal), but not vice versa. A heuristic can be admissible (optimistic on average) but inconsistent (locally non-monotone). Such a heuristic produces an f-landscape with local wrinkles — the search still finds the optimal solution (because there are no false valleys below the true minimum), but it may need to revisit states along the way.

### 3.3.3 The Quality Spectrum

Between the zero heuristic $h \equiv 0$ (which is trivially admissible and consistent but provides no guidance) and the perfect heuristic $h = h^*$ (which provides maximum guidance), there is a continuous spectrum of heuristic quality.

A heuristic is "better" when it is closer to $h^*$ — when the f-landscape it produces is closer to the true cost landscape. Formally, the quality of a heuristic can be measured by its **informedness**: the expected value of $h(x)$ over the state space. A more informed admissible heuristic dominates a less informed one in the sense that A* with the more informed heuristic never expands more states than A* with the less informed one.

In the geometric picture, informedness corresponds to the **sharpness** of the f-landscape's valleys. A highly informed heuristic produces steep, narrow valleys that funnel the search directly to the solution. A weakly informed heuristic produces broad, shallow valleys — the search descends toward the solution, but slowly and imprecisely.

### 3.3.4 What Admissibility Means for Cognition

Let us translate these formal properties into cognitive terms. Consider a human or artificial reasoner working on a problem. The heuristic $h(x)$ is whatever internal signal tells the reasoner "I think I am this far from the answer."

**Admissibility** means the reasoner never believes it is closer to the answer than it actually is. An admissible cognitive heuristic is one that errs on the side of caution — "I might need more work" — rather than on the side of premature satisfaction — "I think I'm almost done."

**Consistency** means the reasoner's estimates are locally coherent. If the reasoner judges that state $x$ is close to the answer, and state $y$ is one step from $x$, then the reasoner should judge state $y$ to be only slightly farther from or closer to the answer — not dramatically different.

**Overestimation** — the failure of admissibility — means the reasoner thinks it is farther from the answer than it is. This sounds problematic, but it merely produces excessive caution: the search takes too long but still finds the right answer.

**Underestimation** — the more dangerous failure — means the reasoner thinks it is closer to the answer than it is. The reasoner becomes overconfident, and the search terminates prematurely at a suboptimal solution. This is a critical asymmetry: optimism about proximity is more dangerous than pessimism.

Wait. This requires careful attention. In the A* literature, "overestimation" by the heuristic is dangerous (it means $h(x) > h^*(x)$, the heuristic overestimates cost-to-go), and this causes the algorithm to miss optimal solutions. But in the cognitive context, what we observe as "overconfidence" is the system believing it is *closer* to the goal than it is — which corresponds to the heuristic *underestimating* cost-to-go. The heuristic says "you're almost there" when the truth is "you have a long way to go."

This notational subtlety matters enormously. When a language model is overconfident — when it assigns high probability to an incorrect answer — its heuristic is *underestimating* the remaining cost. In A* terms, this means $h(x) < h^*(x)$, which corresponds to... an admissible heuristic? No. The problem is more subtle than it first appears. The heuristic is underestimating cost-to-go, which is admissible for A* and safe for finding the optimal solution. But the model is not running A*. The model terminates when it believes $h(x) \approx 0$ — when it believes it has reached the goal. If $h$ systematically underestimates, the model terminates too early, at states that it believes are near-goal but are actually far from it.

Let us state this precisely. In an A*-like search that expands nodes until the goal is found, admissibility (never overestimating cost-to-go) guarantees optimality. But in a satisficing search that terminates when the estimated remaining cost drops below a threshold — which is closer to how both humans and LLMs operate — underestimation of cost-to-go is catastrophic. The system halts its search prematurely, satisfied that it has arrived, when in fact it has not.

This is the bridge between the classical A* framework and the cognitive reality of overconfident reasoning, and it will be the focus of Section 3.6.

---

## 3.4 The Heuristic in Neural Networks

### 3.4.1 Where Is the Heuristic?

A transformer-based language model does not have an explicit heuristic function. There is no variable labeled $h$ that stores an estimate of cost-to-go. And yet, the model demonstrably engages in something like heuristic-guided search: it generates tokens that are more likely to lead toward coherent, goal-satisfying completions; it allocates more computation to harder decisions; it produces intermediate reasoning steps that progressively narrow the space of possible answers.

If the heuristic field is the central navigational signal, where does it live in the network?

**[Speculation/Extension.]** The answer is: everywhere and nowhere. The heuristic is not localized in a single component. It is an emergent property of the entire forward pass — the combined action of embeddings, attention layers, MLP layers, layer normalization, and the residual stream. At each layer, the network's internal representation is updated in a way that (implicitly) moves the representation closer to the region of activation space that corresponds to the correct output. The direction and magnitude of this movement at each layer constitutes the local gradient of the implicit heuristic field.

### 3.4.2 The Residual Stream as Heuristic Trajectory

The residual stream interpretation of transformers (Elhage et al., 2021) provides a natural framework. In this view, the model maintains a residual stream $\mathbf{r} \in \mathbb{R}^d$ that is progressively updated by each layer:

$$\mathbf{r}^{(\ell+1)} = \mathbf{r}^{(\ell)} + \Delta^{(\ell)}(\mathbf{r}^{(\ell)})$$

where $\Delta^{(\ell)}$ is the update contributed by layer $\ell$ (the sum of the attention head outputs and the MLP output).

Each update $\Delta^{(\ell)}$ moves the residual stream in some direction. If the model is "reasoning well," these updates move the residual stream toward the region of activation space that maps to the correct answer under the unembedding matrix. If the model is "reasoning poorly," the updates move it in unproductive or counterproductive directions.

The implicit heuristic $h(\mathbf{r})$ at any point in the residual stream is something like "the distance from $\mathbf{r}$ to the correct-answer region of activation space." We cannot measure this directly (we do not know the correct-answer region in advance), but we can characterize it indirectly through the model's behavior. The model's confidence (the probability it assigns to the most likely next token) is a proxy for $h(\mathbf{r})$ — high confidence corresponds to low estimated remaining cost.

### 3.4.3 MLP Layers as Heuristic Evaluation

The MLP layers in a transformer perform a function that is strikingly analogous to heuristic evaluation in classical search. Each MLP layer takes the current representation, passes it through a nonlinear transformation, and produces an update vector. This update is computed based on the model's "knowledge" — the patterns encoded in the MLP weights during training.

In the heuristic field framework, the MLP layers implement the **evaluation component** of the heuristic: they look at the current state (representation) and compute an estimate of what direction to move. The weights of the MLP encode, in compressed form, the model's learned understanding of what "closer to the goal" looks like for various types of problems.

This is why MLP layers have been found to store factual knowledge (Meng et al., 2022; Geva et al., 2021). Factual knowledge is precisely the kind of information needed to evaluate heuristic cost: knowing that "Paris is the capital of France" allows the heuristic to assign low cost-to-go to representations that are heading toward "Paris" when the question asks about France's capital.

---

## 3.5 Attention as Heuristic Guidance

### 3.5.1 What Attention Does

The attention mechanism (Vaswani et al., 2017) computes, for each token position, a weighted combination of value vectors from all other positions:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

The attention weights — the softmax-normalized dot products of queries and keys — determine how much each position contributes to the update of every other position. A high attention weight from position $i$ to position $j$ means that the information at position $j$ is judged to be relevant for updating the representation at position $i$.

### 3.5.2 Attention as Relevance Routing

**[Speculation/Extension.]** In the heuristic field framework, attention implements the **guidance component** of the heuristic: it determines which information is relevant for the current reasoning step. This is precisely what a heuristic does — it says "look here, not there."

Consider a model solving a multi-step reasoning problem. At each layer, the attention mechanism must decide which pieces of the input (and which intermediate reasoning results from previous layers) are most relevant to the current inferential step. A high attention weight says: "This token carries information that reduces the estimated cost-to-go." A low attention weight says: "This token is irrelevant to the current reasoning objective."

This is not a metaphor. The attention pattern is literally a routing mechanism that implements preferential allocation of computational resources to promising directions. It is a discrete approximation to the gradient of the heuristic field — it points the computation toward the information that the model judges will most reduce the remaining distance to the goal.

### 3.5.3 Multi-Head Attention as Multi-Directional Heuristic

Multi-head attention — the use of multiple independent attention heads per layer — corresponds to evaluating the heuristic gradient along multiple directions simultaneously. Each head computes its own relevance judgments, attending to different aspects of the input. One head might attend to syntactic structure; another to semantic content; another to positional information.

In the heuristic field picture, each head computes a directional derivative of the heuristic in a different direction. The combined output of all heads gives a multi-dimensional gradient signal — not just "the goal is that way," but "the goal is that way along dimension 1, that way along dimension 2, and that way along dimension 3."

This explains why multi-head attention is so effective: it provides a richer, more informative gradient signal than single-head attention. A single head can only point in one direction at a time. Multiple heads can triangulate — combining multiple directional signals to produce a more accurate estimate of the true gradient.

### 3.5.4 The Attention Pattern as Heuristic Topology

The pattern of attention weights across all heads and all layers constitutes a complex relational structure. This structure is the model's implicit representation of which parts of the problem are connected to which other parts — the topology of the heuristic field.

When the attention pattern correctly identifies the relevant dependencies in a problem, the heuristic field has the right topology — it guides the search along paths that respect the problem's structure. When the attention pattern misidentifies relevance — attending to superficially salient but logically irrelevant features — the heuristic field's topology is wrong. The search follows paths that feel productive (they attend to vivid, attention-grabbing information) but do not actually lead toward the goal.

This is the mechanism behind the heuristic corruption effects we will examine in Chapter 5. Framing effects, emotional anchoring, and sensory distractors do not change the logical structure of the problem. They change the attention pattern — and through it, the topology of the implicit heuristic field. The corrupted heuristic guides the search toward the salient rather than the correct, toward the vivid rather than the valid.

---

## 3.6 When the Heuristic Lies: Overconfidence as Inadmissibility

### 3.6.1 The Calibration Connection

We are now in a position to connect the formal framework to empirical measurement. If the heuristic field guides reasoning, and the quality of reasoning depends on the quality of the heuristic field, then we should be able to measure heuristic quality. And we can — through **calibration**.

A reasoner is **well-calibrated** if its confidence in its answers matches its actual accuracy. When the reasoner says "I am 80% confident this answer is correct," the answer should be correct approximately 80% of the time. Calibration is precisely the accuracy of the heuristic's terminal evaluation: when the reasoner judges $h(x) \approx 0$ (I have reached the goal), is it actually at the goal?

The **Expected Calibration Error (ECE)** quantifies the gap between stated confidence and actual accuracy, averaged across confidence bins:

$$\text{ECE} = \sum_{b=1}^{B} \frac{n_b}{N} |\text{acc}(b) - \text{conf}(b)|$$

where $\text{acc}(b)$ is the actual accuracy in bin $b$, $\text{conf}(b)$ is the mean confidence in bin $b$, $n_b$ is the number of predictions in bin $b$, and $N$ is the total number of predictions.

An ECE of zero means perfect calibration — the heuristic's terminal evaluation is perfectly accurate. A nonzero ECE means the heuristic systematically misjudges the remaining cost at termination.

### 3.6.2 The Empirical Findings

In the Measuring AGI metacognition benchmark (M1: Calibration Under Uncertainty), we measured calibration ECE across five frontier language models. The results are unambiguous:

| Model | ECE | Direction |
|-------|-----|-----------|
| Gemini Flash 2.0 | 0.414 | Overconfident |
| Gemini Flash 2.5 | 0.415 | Overconfident |
| Gemini Flash 3 | 0.333 | Overconfident |
| Gemini Pro | 0.230 | Overconfident |
| Claude Sonnet 4.6 | 0.250 | Overconfident |

**[Empirical.]** Every model is overconfident. Every model systematically reports higher confidence than its accuracy warrants. The combined statistical significance across all models is **9.3$\sigma$** — this is not noise, not a marginal effect, not an artifact of measurement. This is a fundamental property of how these systems estimate their own proximity to correct answers.

### 3.6.3 The Heuristic Interpretation

Translate these findings into the heuristic field framework:

**[Conditional Theorem.]** **Overconfidence means the heuristic underestimates cost-to-go.** When a model reports 90% confidence on a question it answers correctly only 60% of the time, its internal heuristic is saying $h(x) \approx 0$ — "I have essentially reached the goal" — when the truth is $h^*(x) \gg 0$ — "I am still far from a reliably correct answer."

In the f-landscape picture, overconfidence means the f-landscape has false valleys. The model descends into a region where $f(x)$ is low — the combined path cost and estimated remaining cost appears small — but the true cost-to-go is much larger. The model terminates its search, satisfied with its answer, when a more accurate heuristic would have driven it to continue searching, to consider alternatives, to check its work.

This is not admissibility failure in the A* sense (where the heuristic overestimates cost-to-go). It is the complementary failure relevant to satisficing search: the heuristic *underestimates* cost-to-go, causing premature termination. In a system that stops searching when it believes $h(x)$ is small enough, underestimation is the dangerous direction.

### 3.6.4 The Premature Convergence Prediction

The heuristic field framework makes a specific prediction: overconfident models should exhibit **premature convergence**. They should settle on answers too quickly, fail to explore alternative solutions, and resist revising their initial judgments.

This is exactly what the broader benchmark suite reveals:

- In the **learning benchmarks** (L2: Error Correction), models shown valid counterarguments to correct answers capitulated at rates from 0% (Claude) to 56% (Flash 2.5). But crucially, even models that resist sycophantic capitulation show insufficient *active* revision. The heuristic says "I'm done" before the reasoning is actually complete.

- In the **executive function benchmarks** (E2: Emotional Anchoring), emotional priming causes significant shifts in moral judgment — up to 6.8$\sigma$. The priming does not change the logical content of the problem, but it changes the heuristic's evaluation of where the goal lies. The emotionally anchored heuristic creates a false valley near the primed conclusion.

- In the **attention benchmarks** (A1: Sensory Distractors), irrelevant vivid information shifts moral judgments by up to 4.6$\sigma$. The distractors corrupt the attention-mediated heuristic, redirecting the search toward the salient rather than the correct.

Each of these findings is a manifestation of the same underlying phenomenon: a corrupted heuristic field that misjudges cost-to-go, creating false valleys in the evaluation landscape that capture the search trajectory.

### 3.6.5 The Magnitude of Corruption

The ECE values we observe are not small perturbations. An ECE of 0.414 means that, on average, the gap between stated confidence and actual accuracy is 41.4 percentage points. This is a heuristic that is not merely slightly miscalibrated — it is catastrophically misleading.

To appreciate the magnitude, consider what a 0.414 ECE would mean for A* search. If the heuristic's estimates of cost-to-go were off by 41.4% on average, the search would routinely descend into false valleys, routinely miss optimal solutions, routinely terminate at suboptimal states. The algorithm would still function — it would produce answers — but the answers would be unreliable, and the algorithm would lack the ability to distinguish reliable from unreliable answers.

This is, in fact, a precise description of the current state of language model reasoning: the models produce answers, some correct and some incorrect, and they lack the metacognitive capacity to reliably distinguish which is which. The heuristic field framework provides a unified explanation: the implicit heuristic that guides the model's reasoning is systematically corrupted, and the model has no mechanism for detecting or correcting this corruption.

---

## 3.7 Implications for Reasoning Quality

### 3.7.1 The Central Theorem

We can now state the central claim of this chapter as a theorem, or more precisely, as a theoretical framework that organizes the empirical evidence:

**[Conditional Theorem.]** **The Heuristic Quality Thesis.** The quality of a reasoning system's outputs is determined, to first order, by the quality of its implicit heuristic field $h(x)$. Specifically:

1. **Accuracy** is determined by whether the heuristic's global minimum coincides with the true goal state. If the deepest valley in the heuristic landscape is at the correct answer, the reasoner finds the correct answer.

2. **Efficiency** is determined by the sharpness and smoothness of the heuristic landscape. A sharp, smooth landscape funnels the search directly to the answer. A flat or rough landscape causes the search to wander.

3. **Robustness** is determined by the stability of the heuristic under perturbation. If small changes to the input (framing, emotional tone, irrelevant context) produce small changes in the heuristic field, reasoning is robust. If they produce large changes — warping the landscape, creating new valleys, eliminating old ones — reasoning is fragile.

4. **Calibration** is determined by the accuracy of the heuristic's terminal evaluation. If $h(x) \approx 0$ only when $x$ is genuinely near the goal, the reasoner knows when it has found the answer. If $h(x) \approx 0$ at states far from the goal, the reasoner is overconfident and does not know when it has failed.

### 3.7.2 The Human Heuristic

The framework applies to human reasoning as well, and provides a precise vocabulary for phenomena that cognitive science has long described informally.

**Intuition** is the human heuristic field. When a chess grandmaster looks at a board position and immediately senses that it is "good" or "bad" for white, the grandmaster is evaluating $h(x)$ — estimating the cost-to-go from the current position. The grandmaster's intuition, honed by thousands of hours of study and play, implements a heuristic that is highly informed (close to $h^*$) within its domain of expertise.

**Salience** is the human attention mechanism — the counterpart of the transformer's attention weights. When a feature of the environment "jumps out" at us, our attentional system is assigning it high relevance — high attention weight — in the heuristic evaluation. The salience of vivid, emotionally charged, or personally relevant information corresponds to attention weights that are disproportionately large for those features, potentially corrupting the heuristic.

**Pattern recognition** is the human analog of MLP-based heuristic evaluation. When a physician looks at a set of symptoms and immediately suspects a diagnosis, the physician's pattern recognition system is computing a heuristic evaluation: "Given what I see, the goal (correct diagnosis) is probably in this direction." The quality of this pattern recognition — how accurately it estimates cost-to-go — determines the quality of the physician's diagnostic reasoning.

**Deliberation** — what Kahneman (2011) calls "System 2" — is the process of explicitly computing and following the gradient of the heuristic field. When we stop to think carefully, we are overriding the fast, automatic heuristic evaluation (System 1) with a slower, more deliberate computation. In our framework, System 1 provides a rough but fast heuristic; System 2 computes a more accurate heuristic at greater computational cost. The interaction between the two is the interaction between a fast approximate gradient and a slow exact gradient.

### 3.7.3 Why Better Heuristics Are Hard

If reasoning quality is heuristic quality, the natural question is: why can't we simply build better heuristics?

The answer lies in the computational complexity of the heuristic itself. A perfect heuristic $h = h^*$ provides instant access to the optimal cost-to-go from every state — but computing $h^*$ is exactly as hard as solving the original search problem. The heuristic is useful precisely because it is an approximation, a shortcut that trades accuracy for speed.

This is the fundamental tension of all reasoning: the heuristic must be good enough to guide the search productively, but cheap enough to compute that it does not negate the benefit of heuristic search over brute-force enumeration. A heuristic that takes as long to compute as the search itself is useless as a heuristic.

For neural networks, this tension manifests in the training process. The model's implicit heuristic is shaped by the training data and the training objective. The training process must somehow instill a heuristic that generalizes — that provides useful cost-to-go estimates for states the model has never encountered. This is the deep challenge of machine learning: not just memorizing the heuristic values for training states, but learning the structure of the heuristic field well enough to extrapolate to novel states.

The 9.3$\sigma$ overconfidence we observe suggests that current training processes fail to produce well-calibrated heuristic fields. The models learn heuristics that are informative (they guide the search toward plausible answers) but systematically miscalibrated (they overestimate proximity to the goal). The heuristic is good enough to be useful — far better than random — but not good enough to be reliable.

### 3.7.4 Admissibility as a Design Principle

The formal framework suggests a design principle for improving reasoning systems: **aim for admissible heuristics**. Since the models are satisficing (they stop when they think they're close enough), the dangerous failure mode is underestimation of cost-to-go (overconfidence). The safe failure mode is overestimation (underconfidence).

A model with an admissible heuristic would err on the side of continuing to reason rather than stopping prematurely. It would express uncertainty when uncertain, seek additional evidence when evidence is insufficient, and revise its answers when confronted with valid counter-arguments. It would, in short, reason more like an ideal Bayesian agent and less like a confident pattern-matcher.

How might admissibility be achieved? Several approaches suggest themselves:

1. **Calibration training**: Explicitly training the model to produce well-calibrated confidence estimates, penalizing overconfidence more heavily than underconfidence. This directly shapes the heuristic's terminal evaluation.

2. **Deliberative search**: Augmenting the model with explicit search procedures (chain-of-thought, tree-of-thought, iterative refinement) that do not rely solely on the implicit heuristic but also explore alternative paths. This reduces dependence on heuristic accuracy by introducing explicit exploration.

3. **Adversarial heuristic testing**: Probing the heuristic field for inconsistencies and false valleys using adversarial inputs — the structural fuzzing approach discussed in Chapter 10. Identifying where the heuristic fails allows targeted correction.

4. **Metacognitive monitoring**: Training an explicit metacognitive layer that monitors the heuristic's behavior and detects signs of premature convergence — the approach explored in Chapter 9. If the system can detect that its heuristic is underestimating cost-to-go, it can compensate by continuing to search.

### 3.7.5 The View from Chapter 3

Let us step back and survey what we have established.

Reasoning is search on a manifold (Chapter 1 and 2). The search is guided by a heuristic field — a scalar function on the manifold that estimates cost-to-go (Section 3.1). The search follows the gradient of the combined evaluation function $f = g + h$, and the geometry of this f-landscape determines search behavior (Section 3.2). Good heuristics are admissible and consistent; the quality of the heuristic determines the quality of the search (Section 3.3).

In neural networks, the heuristic is implemented implicitly by the combined action of all network components, with attention mechanisms providing the guidance signal and MLP layers providing the evaluation signal (Sections 3.4 and 3.5). The quality of this implicit heuristic can be measured through calibration, and the measurements reveal systematic overconfidence — a heuristic that underestimates cost-to-go and causes premature convergence (Section 3.6).

The central claim — that reasoning quality equals heuristic field quality — has both theoretical grounding (in the A* optimality theorem and its generalizations) and empirical support (in the measured correlation between calibration quality and reasoning reliability across models) (Section 3.7).

What we have not yet addressed is the *optimal* reasoning trajectory — the path the search would follow if the heuristic were perfect. That is the subject of Chapter 4, where we develop the concept of the geodesic on the reasoning manifold. Nor have we addressed the specific mechanisms by which the heuristic field can be corrupted — that is the subject of Chapters 5 through 8, where we examine framing effects, sycophancy, local minima, and symmetry breaking as geometric pathologies of the heuristic field.

The heuristic field is the unifying concept of this book. Every failure mode we will examine in Part II is a specific type of heuristic field corruption. Every control mechanism we will examine in Part III is a mechanism for detecting or correcting heuristic corruption. And every empirical measurement we will present in Part IV is a measurement of some aspect of the heuristic field's geometry.

The field guides the search. The search produces the reasoning. The reasoning is only as good as the field.

---

## Notes on Chapter 3

**Historical note on A* and heuristic search.** The A* algorithm was introduced by Hart, Nilsson, and Raphael (1968) and has been the subject of extensive theoretical analysis. The optimality conditions (admissibility and consistency) were established in the original paper and refined by subsequent work, notably Dechter and Pearl (1985). The geometric interpretation of A* as gradient descent on the f-landscape appears to be novel to this book, though it is implicit in the work on continuous-space path planning (LaValle, 2006).

**The residual stream interpretation.** The view of transformers as iteratively updating a residual stream was articulated by Elhage et al. (2021) in their work on mathematical frameworks for transformer circuits. The connection between this view and heuristic search, developed in Section 3.4, extends their framework from a descriptive tool to a normative one: the residual stream updates should be understood not just as additive contributions but as gradient steps in an implicit heuristic landscape.

**Calibration and overconfidence.** The expected calibration error (ECE) metric is standard in the machine learning literature (Naeini et al., 2015; Guo et al., 2017). The finding that large language models are systematically overconfident has been reported by several groups (Kadavath et al., 2022; Xiong et al., 2023). Our contribution is the theoretical framing: overconfidence as heuristic underestimation of cost-to-go, and the connection to premature convergence via the satisficing search model.

**The 9.3$\sigma$ combined significance.** This figure aggregates the calibration results across all five models tested in the M1 benchmark using Fisher's method for combining independent p-values. The individual results range from $p < 0.001$ for all models, with the combined effect being far beyond any conventional significance threshold. See the Measuring AGI benchmark documentation for full methodological details.

**Connection to Kahneman's System 1 / System 2.** The interpretation of System 1 as a fast heuristic and System 2 as a slow but more accurate heuristic computation has been proposed informally by several authors. Our contribution is to make this precise: System 1 implements a heuristic field with certain geometric properties (fast evaluation, possibly inconsistent, good within domain); System 2 implements a different heuristic field (slow evaluation, more consistent, better calibrated). The interaction between the two is governed by the relative accuracy of their heuristic fields, not by some separate "metacognitive" mechanism — or rather, the metacognitive mechanism *is* the comparison of the two heuristic fields, as we develop in Chapter 9.

---

## Worked Example: When the Heuristic Hesitates

Two patients arrive within minutes of each other on Dr. Okafor's shift. Both are men in their fifties. Both report chest tightness. Both are diaphoretic. On the surface — in the raw symptom coordinates — they occupy nearly the same point in the clinical state space.

**Patient A** has substernal pressure radiating to the jaw, onset during exertion, with a history of hypertension. **Patient B** has epigastric tightness that worsens when lying flat, onset after a large meal, with a history of GERD. The symptom vectors are close in the ambient space, but the heuristic field assigns them very different values — or at least, a well-calibrated heuristic field should.

**The gradient at Patient A's state.** Dr. Okafor's heuristic evaluates Patient A and returns a steep negative gradient: high estimated cost-to-go toward the "benign" region, low cost-to-go toward "acute coronary syndrome." The gradient is unambiguous. She moves decisively: ECG, troponin, aspirin, cardiology consult. The search descends rapidly into the correct diagnostic basin.

**The gradient at Patient B's state.** Here the heuristic field is shallower. The presentation is consistent with GERD — but it is also consistent with atypical MI. The gradient vector is short, nearly horizontal. The heuristic cannot confidently distinguish the two basins. This is a *near-saddle region* of the heuristic landscape: the estimated cost-to-go toward "cardiac" and toward "GI" are nearly equal, and the gradient provides weak directional guidance.

**What the good heuristic does.** A well-calibrated heuristic, confronted with a near-saddle, does not pick a direction and commit. It recognizes that the gradient signal is unreliable in this region and switches to a different strategy: *gather more information to reshape the local landscape*. Dr. Okafor orders both a GI workup and cardiac enzymes. She is not being indecisive — she is correctly responding to the local geometry of her heuristic field. She is spending computation (additional tests) to sharpen the gradient before descending.

**What the corrupted heuristic does.** A model with the overconfidence pathology described in Section 3.6 behaves differently. Its heuristic, which systematically underestimates cost-to-go, evaluates Patient B and returns a confident gradient pointing toward "GERD" — the heuristic says $h(x) \approx 0$, we are nearly at the goal, no further search is needed. The model (or the overconfident clinician) diagnoses GERD and sends the patient home. If the true diagnosis is MI, the premature convergence is catastrophic.

**The measurable difference.** The geodesic deviation between the two diagnostic trajectories is quantifiable. The correct trajectory — gather information, wait for labs, then commit — has a longer path length but terminates in the correct diagnostic basin. The overconfident trajectory is shorter but terminates in the wrong basin. The geodesic deviation of the overconfident path, measured as the additional cost required to recover from the wrong basin (emergency re-presentation, delayed treatment, potential myocardial damage), dwarfs the cost of the "extra" tests that the calibrated heuristic recommended.

This is the core asymmetry of Section 3.3.4 made clinical: in a satisficing system, the cost of a false valley (premature convergence to the wrong diagnosis) vastly exceeds the cost of a gentle slope (extra caution before convergence). Admissibility — the heuristic's refusal to declare victory prematurely — is not perfectionism. It is the geometric condition for safe search in a space where errors are irreversible.

---

## Technical Appendix

**The Heuristic Field (Formal Definition).** Let $(M, g)$ be a Riemannian reasoning manifold and $\mathcal{G} \subset M$ a goal region. A *heuristic field* is a smooth function $h: M \to \mathbb{R}_{\geq 0}$ satisfying $h(x) = 0$ for $x \in \mathcal{G}$ and $h(x) > 0$ for $x \notin \mathcal{G}$. The function $h$ is interpreted as an estimate of the geodesic distance from $x$ to the nearest point in $\mathcal{G}$.

**Admissibility (Definition 3.1).** A heuristic field $h$ is *admissible* if for all $x \in M$:

$$h(x) \leq d_g(x, \mathcal{G})$$

where $d_g(x, \mathcal{G}) = \inf_{y \in \mathcal{G}} d_g(x, y)$ is the geodesic distance from $x$ to the goal region. Admissibility guarantees that the evaluation landscape $f = g + h$ has no false valleys below the true optimum.

**Consistency (Definition 3.2).** A heuristic field $h$ is *consistent* if for all $x, y \in M$:

$$h(x) \leq d_g(x, y) + h(y)$$

Consistency is equivalent to the condition that $h$ is a *Lipschitz function with Lipschitz constant 1* with respect to the geodesic distance on $M$. In the smooth case, consistency is equivalent to $\|\nabla h\|_g \leq 1$ everywhere — the gradient of the heuristic has magnitude at most 1 in the Riemannian metric. This means the heuristic's rate of change never exceeds the actual rate of change of geodesic distance. Consistency implies admissibility (by integration along geodesics from $x$ to $\mathcal{G}$), but not vice versa.

**The Heuristic Quality Thesis (Theorem 3.1, informal).** Let $\gamma_h$ be the search trajectory produced by gradient descent on the evaluation landscape $f = g + h$. Then:

(i) If $h = h^*$ (the perfect heuristic), $\gamma_h$ is a geodesic to $\mathcal{G}$.

(ii) The geodesic deviation $\Delta(\gamma_h, \gamma^*) = \mathcal{L}[\gamma_h] - \mathcal{L}[\gamma^*]$ is bounded by the $L^\infty$ norm of the heuristic error: $\Delta(\gamma_h, \gamma^*) \leq C \|h - h^*\|_\infty$ for a constant $C$ depending on the curvature of $M$.

(iii) If $h$ is admissible and $M$ is compact, $\gamma_h$ terminates in $\mathcal{G}$.

**Premature Convergence Criterion (Proposition 3.1).** Let $\tau > 0$ be a termination threshold: the search halts when $h(x) < \tau$. If $h$ underestimates the true cost-to-go by at least $\delta > \tau$ on a region $U \subset M$ with $U \cap \mathcal{G} = \emptyset$, then any search trajectory entering $U$ terminates outside the goal region. That is, the set $\{x \in M : h(x) < \tau, \, d_g(x, \mathcal{G}) > \delta\}$ is a *false termination region* — a basin from which the satisficing search cannot escape.

**Overconfidence as Heuristic Underestimation (Corollary 3.1).** If a system's implicit heuristic satisfies $\mathbb{E}[h(x) - h^*(x)] = -\beta$ with $\beta > 0$ (systematic underestimation of cost-to-go by an average of $\beta$), then the expected false termination rate is at least $\Pr[h^*(x) > \tau + \beta \mid h(x) < \tau]$, which increases monotonically with $\beta$. An ECE of 0.414 corresponds to a regime where this false termination rate is substantial, consistent with the empirical observation that models reporting high confidence are frequently incorrect.

---

## References for Chapter 3

Dechter, R., & Pearl, J. (1985). Generalized best-first search strategies and the optimality of A*. *Journal of the ACM*, 32(3), 505-536.

Elhage, N., Nanda, N., Olsson, C., et al. (2021). A mathematical framework for transformer circuits. *Anthropic Research*.

Geva, M., Schuster, R., Berant, J., & Levy, O. (2021). Transformer feed-forward layers are key-value memories. *Proceedings of EMNLP 2021*.

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. *Proceedings of ICML 2017*.

Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 100-107.

Kadavath, S., Conerly, T., Askell, A., et al. (2022). Language models (mostly) know what they know. *arXiv preprint arXiv:2207.05221*.

Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.

LaValle, S. M. (2006). *Planning Algorithms*. Cambridge University Press.

Meng, K., Bau, D., Andonian, A., & Belinkov, Y. (2022). Locating and editing factual associations in GPT. *Advances in Neural Information Processing Systems*, 35.

Naeini, M. P., Cooper, G., & Hauskrecht, M. (2015). Obtaining well calibrated probabilities using Bayesian binning. *Proceedings of AAAI 2015*.

Newell, A., & Simon, H. A. (1972). *Human Problem Solving*. Prentice-Hall.

Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453-458.

Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30.

Xiong, M., Hu, Z., Lu, X., et al. (2023). Can LLMs express their uncertainty? An empirical evaluation of confidence elicitation in LLMs. *arXiv preprint arXiv:2306.13063*.
