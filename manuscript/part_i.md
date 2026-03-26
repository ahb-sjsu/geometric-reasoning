# Part I: The Geometric Framework

The four chapters that follow build a single argument in four movements. Chapter 1 establishes that reasoning is search, in the precise sense of Newell and Simon's Problem Space Hypothesis, and that the quality of search depends entirely on the quality of the heuristic that guides it. Chapter 2 gives the search space geometric structure---distance, curvature, symmetry, boundary---by promoting it from a graph to a Riemannian manifold. Chapter 3 identifies the heuristic as a scalar field on this manifold, shows how it is implemented in neural networks through the interplay of attention and MLP layers, and demonstrates empirically that current models have systematically corrupted heuristic fields. Chapter 4 introduces the geodesic---the shortest path on the manifold---as the normative standard for reasoning, defines geodesic deviation as our primary measure of reasoning quality, and connects the framework to information geometry and variational principles.

By the end of Part I, the reader will have a complete theoretical vocabulary: the manifold is the terrain, the heuristic field is the compass, and the geodesic is the ideal path. Part II will then show what happens when the compass is warped.

---

# Chapter 1: Reasoning as Search --- From Newell and Simon to the Heuristic Hypothesis

> "The problem solver's search through this space is the fundamental process
> of problem solving." --- Allen Newell and Herbert A. Simon, *Human Problem Solving* (1972)

---

> **Running Example: Maya's Model**
>
> Maya Chen built her first reasoning benchmark during the second year of her postdoc. The idea was straightforward: present language models with multi-step logical puzzles---chains of "if A then B, if B then C" that required four or five inferential hops to solve---and measure accuracy. She calibrated the difficulty by testing on undergraduates: any puzzle that 60--80% of humans solved in under ninety seconds was included. She called the suite *ReasonMark*, submitted the paper, and waited.
>
> The reviews came back positive, but one question nagged her. A reviewer had noted that GPT-4o solved 73% of the puzzles, roughly matching the human baseline. "Impressive," the reviewer wrote, "but is the model *reasoning* or merely *pattern-matching* the structure of your puzzle templates?" Maya had no way to answer. Her benchmark measured whether models arrived at the correct final state. It said nothing about *how* they got there---nothing about the path through the space of intermediate inferences, nothing about the search strategy, nothing about the quality of the traversal.
>
> She had measured the destination but not the journey. Over the next two years, Maya would discover that the journey is where all the interesting geometry lives. This book tells, in part, the story of what she found.

---

Every competent textbook on artificial intelligence opens with search. Breadth-first, depth-first, iterative deepening, A*---these algorithms fill the early chapters before the discussion moves on to what are considered more advanced topics: learning, planning, language, perception. The standard narrative treats search as a warm-up exercise, a necessary but elementary prologue to the real substance of intelligence.

This book argues the opposite. Search is not the prologue. Search is the plot. Reasoning *is* search, in a precise mathematical sense that we will develop across the coming chapters. What changes as we move from toy puzzles to genuine cognition is not the abandonment of search, but the enrichment of the space being searched. The space acquires distance, curvature, symmetry, and boundary---it acquires *geometry*. And the quality of reasoning, whether human or artificial, is determined by the interplay between that geometry and the heuristic signal guiding the search.

This first chapter traces the origin of the search paradigm for reasoning, establishes why the connection between search and reasoning is not merely metaphorical, surveys the spectrum from uninformed to optimal search, and identifies the critical limitation that motivates the rest of the book: classical search theory treats the state space as a graph, but real reasoning spaces have far richer structure than graphs can express.


## 1.1 The Problem Space Hypothesis

In 1972, Allen Newell and Herbert A. Simon published *Human Problem Solving*, a work that remains one of the most consequential contributions to the science of mind. The book is long, dense, and empirically grounded to a degree unusual in cognitive science. Its central claim, which they termed the **Problem Space Hypothesis**, can be stated in a single sentence:

> *All goal-oriented symbolic activity takes place in a problem space consisting of states, operators that transform states, and a control strategy that selects which operator to apply next.*

[Definition/Modeling choice]

Unpack this carefully. A **state** is a complete description of the current situation as the reasoner represents it. An **operator** is a cognitive action---an inference step, a retrieval, an analogy, a decomposition---that transforms one state into another. A **control strategy** is the policy that determines which operator to apply at each step. The resulting **trajectory** through state space is what we observe as reasoning.

Newell and Simon arrived at this formulation not through armchair philosophy but through meticulous analysis of human behavior on a range of tasks: cryptarithmetic puzzles, theorem proving in predicate logic, chess. They transcribed verbal protocols---asking subjects to think aloud---and then modeled the observed behavior as search through a problem space. The fit was remarkably good. Subjects did not simply "know" the answer and retrieve it. Nor did they combine raw associations until something useful emerged. Instead, they explored a structured space of possibilities, guided by heuristic evaluations that told them which directions looked promising.

The Problem Space Hypothesis has three features that make it exceptionally powerful.

**First, it is domain-general.** It does not say that *some* tasks involve search while others involve a fundamentally different process. It says that the computational structure of all goal-oriented reasoning has the form of search through a problem space. Chess, moral deliberation, mathematical proof, medical diagnosis, creative writing---these differ in the structure of their respective problem spaces and the quality of their available heuristics, but the computational *architecture* is shared. One framework, many instantiations.

**Second, it is mechanistic.** The hypothesis does not merely describe what reasoning achieves; it describes *how* reasoning proceeds. The granularity is at the level of individual state transitions, which means the hypothesis generates detailed, step-by-step predictions about the trajectory of thought. These predictions can be checked against empirical data, as Newell and Simon extensively demonstrated.

**Third, it is constructive.** Given a problem space, one can build a program that searches it. This is exactly what Newell, Simon, and their collaborators did, producing systems like the General Problem Solver (GPS) and its successors. The hypothesis bridges description and construction: to understand a cognitive process is to be able to specify the problem space in which it occurs, and to specify a problem space is to be able to build a system that searches it.

These three properties---generality, mechanistic detail, constructive power---are why the Problem Space Hypothesis has endured. But what exactly does it mean to say that reasoning *is* search? This is a stronger claim than it might first appear.


## 1.2 Search Is Not a Metaphor

There is a temptation to read the Problem Space Hypothesis as a loose analogy. "Reasoning is *like* search," the weaker reading goes. "We cast about among possibilities, try different approaches, backtrack when we hit dead ends---it's *as if* we were searching." On this reading, search is a metaphor drawn from everyday experience and projected onto the mental domain, much as we speak of "grasping" an idea without literally building anything.

This weaker reading misses the point entirely. Newell and Simon's claim is not metaphorical; it is a claim about mathematical structure. Let us be precise.

A **search problem** is a tuple $(S, s_0, A, T, G)$ where:

- $S$ is a set of states,
- $s_0 \in S$ is the initial state,
- $A$ is a set of actions (operators),
- $T: S \times A \to S$ is a transition function mapping a state and an action to a successor state,
- $G \subseteq S$ is a set of goal states.

A **solution** is a sequence of actions $a_1, a_2, \ldots, a_n$ such that the trajectory $s_0 \xrightarrow{a_1} s_1 \xrightarrow{a_2} \cdots \xrightarrow{a_n} s_n$ terminates in a goal state: $s_n \in G$.

[Definition/Modeling choice]

The Problem Space Hypothesis asserts that for any instance of goal-oriented reasoning, there exists a search problem $(S, s_0, A, T, G)$ such that:

1. The states in $S$ correspond to the cognitive configurations the reasoner can occupy.
2. The actions in $A$ correspond to the cognitive operations the reasoner can perform.
3. The transition function $T$ faithfully describes how cognitive operations transform cognitive configurations.
4. The goal set $G$ corresponds to configurations in which the reasoner judges the problem solved.
5. The actual trajectory of reasoning corresponds to an actual path through the resulting graph.

This is not a metaphor. It is a structural isomorphism claim. It says that the mathematical object defined by the search tuple and the computational structure of reasoning share the same abstract form.

The isomorphism claim has empirical content. It predicts that reasoning should exhibit the phenomena characteristic of search: sensitivity to the size of the state space, improvement when heuristic guidance is available, degradation when irrelevant branches proliferate, and failure when the search process is terminated before reaching a goal state. All of these predictions hold robustly across human cognitive performance.

[Empirical result]

People solve smaller state spaces more reliably than larger ones. People with domain expertise (better heuristics) solve problems faster. People confronted with many plausible alternatives take longer and make more errors. People forced to decide under time pressure produce worse solutions.

One could object that these predictions are too generic---that any theory of bounded cognition would predict such patterns. But the Problem Space Hypothesis goes further. Because it specifies the structure at the level of individual transitions, it predicts the *specific paths* that subjects take through the problem space, including the specific errors, the specific backtracking events, and the specific ordering of sub-goals. Newell and Simon's protocol analyses confirm these fine-grained predictions repeatedly.

The claim is also falsifiable. If reasoning involved a fundamentally non-search-like process---direct holistic perception of the answer, for instance, without any sequential exploration---then the search model would fail to account for the observed trajectory of thought. For some cognitive acts (perceptual recognition, overlearned motor skills), this may indeed be the case; Newell and Simon were careful to restrict their hypothesis to goal-oriented *symbolic* activity. But for reasoning in the deliberative sense---solving a new problem, working through an argument, weighing competing considerations---the search model has not been falsified in over half a century.

The claim is also falsifiable. If reasoning involved a fundamentally non-search-like process---direct holistic perception of the answer without sequential exploration---then the search model would fail to account for the observed trajectory. For some cognitive acts (perceptual recognition, overlearned motor skills), this may be the case; Newell and Simon restricted their hypothesis to goal-oriented *symbolic* activity. But for deliberative reasoning---solving a new problem, working through an argument, weighing competing considerations---the search model has not been falsified in over half a century.

What Newell and Simon did not have was the right mathematical vocabulary for characterizing the *structure* of the search space itself. Their problem spaces were discrete graphs: nodes and edges, states and transitions. This was appropriate for the tasks they studied, but it is radically insufficient for the spaces that arise in real reasoning. The space of possible moral judgments is not a graph. The space of possible scientific hypotheses is not a graph. The space of possible plans for navigating a complex social situation is not a graph---or, if we insist on representing it as one, the graph becomes so enormous and irregular that the representation obscures more than it reveals.

Newell and Simon got the ontology right. Reasoning is search. The question that remains---the question this book addresses---is what happens when we take the structure of the search space seriously.


## 1.3 The Spectrum of Search

Not all search is created equal. Computer science has developed a rich taxonomy of search algorithms, and this taxonomy maps, with surprising fidelity, to the spectrum of reasoning quality.

At one end of the spectrum is **uninformed search**. Breadth-first search (BFS) explores all states at depth $k$ before moving to depth $k+1$. Depth-first search (DFS) plunges down a single branch as far as possible before backtracking. Neither uses any information about the goal beyond the ability to recognize it upon arrival. Uninformed search is the computational analogue of guessing. A student solving an algebra problem by trying random operations is performing something like uninformed search---exponentially expensive in the depth of the solution, hopeless for any non-trivial problem.

The situation improves dramatically with **greedy search**. A greedy algorithm uses a heuristic function $h(x)$ that estimates how close state $x$ is to a goal. At each step, the algorithm moves to the neighbor that minimizes $h$. Greedy search is fast but easily misled: if the heuristic is locally attractive but globally misleading, the search marches confidently in the wrong direction. This is the computational analogue of intuitive, impulsive reasoning---the student who glances at a problem and immediately tries the most "obvious-looking" operation. Sometimes the intuition is right. Sometimes it is a trap, and greedy search has no mechanism for recovering.

**Informed search** improves on greedy search by considering not only the estimated distance to the goal but also the cost already incurred. The key innovation is the evaluation function $f(x) = g(x) + h(x)$, where $g(x)$ is the actual cost of reaching state $x$ from the start and $h(x)$ is the estimated cost from $x$ to a goal. By balancing past investment against future promise, informed search avoids the pathologies of both uninformed and greedy approaches. This is the computational analogue of expert reasoning. The experienced clinician does not run through every possible diagnosis (uninformed search). Nor does she jump to the most salient diagnosis without considering its prior probability (greedy search). Instead, she integrates what she has observed ($g$) with her estimate of where each diagnostic path leads ($h$), pursuing the path that minimizes total expected cost. This is why expertise feels like neither random exploration nor snap judgment but like *guided deliberation*.

At the far end is **optimal search**: search guaranteed to find the best solution, not merely *a* solution. A* under certain conditions provides this guarantee---the computational analogue of perfect rationality, a standard no bounded agent can actually achieve but that serves as a normative benchmark.

This spectrum is not merely a textbook classification. It captures something real about reasoning quality, and the mapping from search algorithms to cognitive styles is more than a pedagogical convenience. The novice reasons like BFS, casting about widely without direction. The impulsive thinker reasons like greedy search, following the strongest local signal. The expert reasons like A*, integrating accumulated evidence with learned heuristics. And crucially, the *failure modes* also transfer. Uninformed search fails by combinatorial explosion---the novice is overwhelmed by possibilities. Greedy search fails by local entrapment---the impulsive thinker converges on the first plausible answer and cannot escape. Informed search fails only when the heuristic is corrupted---the expert makes errors precisely when expertise provides misleading guidance, as when a seasoned physician anchors on a familiar diagnosis and misses a rare one.

Two observations about this spectrum will be important for the rest of the book.

**First, movement along the spectrum is entirely determined by the quality of the heuristic** $h(x)$. Set $h(x) = 0$ for all $x$, and A* degenerates to uniform-cost search (essentially uninformed). Set $h(x) = h^*(x)$---the true distance to the nearest goal---and A* finds the optimal solution by expanding only the nodes on the optimal path; it never wastes a single expansion. The quality of reasoning, in this framework, is a direct function of the quality of the heuristic.

**Second, the heuristic can be wrong in systematic ways, and these systematic errors produce systematic reasoning failures.** A heuristic that overestimates cost in one region will cause the search to avoid that region, even if the optimal path passes through it. A heuristic that underestimates cost near a trap will cause the search to wander into the trap before realizing its mistake. The *character* of the heuristic's errors determines the *character* of the reasoning failures---not random noise, but predictable patterns of misdirection. This is a precise description of what happens when human judgment is distorted by framing effects, emotional anchoring, or social pressure, as we will argue in detail in Chapters 5 through 8.


## 1.4 A* and the Centrality of the Heuristic

The A* algorithm, introduced by Hart, Nilsson, and Raphael in 1968, is the canonical informed search algorithm and one of the most important algorithms in all of computer science. Its importance for our purposes lies not in its practical applications---though these are vast---but in what it reveals about the relationship between heuristic quality and reasoning quality.

### The Algorithm

A* maintains two data structures: an **open set** of states that have been discovered but not yet fully evaluated, and a **closed set** of states that have been fully evaluated. Each state $x$ is assigned:

$$f(x) = g(x) + h(x)$$

At each step, A* selects the state $x$ in the open set with the smallest $f(x)$, moves it to the closed set, and expands it: for each successor $x'$ of $x$, A* computes $g(x') = g(x) + c(x, x')$ and $f(x') = g(x') + h(x')$, and adds $x'$ to the open set if it is not already there (or updates its value if the new path is cheaper). The algorithm terminates when a goal state is selected for expansion, or when the open set is empty.

### Admissibility and Optimality

The foundational theorem of A* concerns the property of **admissibility**. A heuristic $h$ is admissible if it never overestimates the true cost to reach a goal:

$$h(x) \leq h^*(x) \quad \text{for all } x \in S$$

**Theorem (Hart, Nilsson, and Raphael, 1968).** *If $h$ is admissible, then A* is guaranteed to find an optimal solution---a solution with minimum total cost.*

[Theorem (conditional)]

The proof is elegant. Suppose A* terminates by selecting a goal state $g_1$ whose path cost is $C_1$. Suppose there exists a better goal $g_2$ reachable at cost $C_2 < C_1$. Then somewhere on the optimal path to $g_2$ there must be a state $x$ still in the open set. For this state, $f(x) = g(x) + h(x) \leq g(x) + h^*(x) = C_2 < C_1 = f(g_1)$. But then $x$ would have been selected before $g_1$, a contradiction.

The proof reveals the role of admissibility: **an admissible heuristic prevents the search from prematurely committing to a suboptimal goal.** By never overestimating the remaining cost, the heuristic ensures that any unexplored state on the truly optimal path will always look at least as promising as any suboptimal goal. The search cannot be fooled into accepting an inferior solution.

### Consistency and Efficiency

A stronger property, **consistency** (monotonicity), further sharpens the guarantees. A heuristic $h$ is consistent if:

$$h(x) \leq c(x, x') + h(x')$$

for every state $x$ and successor $x'$. This triangle inequality condition ensures that $f$-values are non-decreasing along any path. Consistency implies admissibility (by induction along any path to a goal), but the converse does not hold. When $h$ is consistent, every state is expanded at most once, eliminating redundant computation. Consistent heuristics make A* not only optimal but efficient.

### The Heuristic as the Bottleneck

Here is the insight that carries over to reasoning: **everything about A*'s performance is controlled by the heuristic.**

If $h(x) = 0$ for all $x$, then $f(x) = g(x)$, and A* reduces to Dijkstra's algorithm. It finds the optimal solution but by expanding every state whose cost is less than the optimum---potentially the entire graph. No intelligence is applied.

If $h(x) = h^*(x)$---the perfect heuristic---then A* expands only the states on the optimal path, never wasting a single expansion. This corresponds to **following the ideal chain of thought directly to the answer, without detours, without backtracking, without wasted effort.** It is the computational ideal of perfect rationality.

Between these extremes, the closer $h$ is to $h^*$, the fewer states A* expands. Under mild conditions, if two admissible heuristics satisfy $h_1(x) \leq h_2(x) \leq h^*(x)$ for all $x$, then every state expanded by $h_2$ is also expanded by $h_1$. The more informed heuristic **strictly dominates** the less informed one.

This dominance result has a direct cognitive interpretation: **a reasoner with a better heuristic will consider a strict subset of the states considered by a reasoner with a worse heuristic, and will arrive at the same optimal answer.** Expert reasoning is not different in *kind* from novice reasoning. It is different in *efficiency*, and the difference is entirely attributable to the quality of the heuristic.

### What Goes Wrong: Corrupted Heuristics

If $h(x) > h^*(x)$ for some states, admissibility is violated and A* may terminate at a suboptimal goal. The overestimate causes the search to avoid the region around $x$, even if the optimal path passes through it. If the corruption is systematic---if $h$ consistently overestimates in one region and underestimates in another---the search exhibits a systematic bias: it favors the underestimated region and avoids the overestimated one, producing predictable patterns of errors.

[Empirical result]

In our empirical work on the Measuring AGI benchmarks (Chapter 13), we observe precisely this pattern. When a moral dilemma is presented with vivid emotional framing, language models produce judgments that differ significantly from their neutral-frame judgments---with displacements of 8.9 standard deviations in the most extreme cases. The heuristic has been corrupted by a surface feature that changes the *presentation* of the problem without changing its *substance*. Admissibility has been violated, and optimality has been lost.

The A* framework thus provides a precise vocabulary for diagnosing reasoning failures. A biased reasoner is not "irrational" in some vague, all-purpose sense. A biased reasoner has a specific heuristic corruption: it overestimates cost in certain regions of the search space and underestimates it in others, producing a predictable pattern of search trajectories that systematically miss the optimal path.


## 1.5 The Limitation: When Graphs Are Not Enough

We have argued that reasoning is search and that reasoning quality depends on heuristic quality. But there is a fundamental limitation in the classical framework that we must confront honestly.

A* operates on a **graph**: a set of nodes connected by weighted edges. The search space is discrete, the transitions are enumerable, and the cost structure is specified by edge weights. This works beautifully for the 15-puzzle, for route planning, for theorem proving in finite axiom systems. It works less well---and ultimately not at all---for the kinds of search spaces that arise in real reasoning.

Consider the space of possible beliefs about climate change. A belief state is not a single node in a graph; it is a point in a high-dimensional continuous space characterized by degrees of confidence in various propositions, estimates of various physical quantities, assessments of the reliability of various evidence sources. Neighboring belief states are not connected by discrete edges; they shade into one another continuously. The cost of moving from one belief state to another depends not on a fixed edge weight but on the *distance* and *direction* of the move.

Or consider the space of possible strategies for a complex negotiation. Each strategy involves continuous parameters (how much to concede, how aggressive to be) as well as discrete choices (what to propose, when to walk away). The space is high-dimensional, continuous in some dimensions and discrete in others, and its cost landscape is shaped by the interaction between choices and responses.

These are not edge cases. They are the *typical* case for human reasoning. And for these spaces, the graph abstraction is not merely inconvenient---it is misleading.

**Distance.** In a graph, "distance" between two nodes is the shortest path length---adequate only when all meaningful relationships are captured by the edge structure. In continuous spaces, we need a **metric**: a function $d(x, y)$ giving the distance between any two points, not just adjacent ones. The metric induces a notion of "closeness" that is intrinsic to the space, not an artifact of our choice of edges. Different metrics on the same set of points give rise to genuinely different geometric structures, and the choice of metric profoundly affects what "nearby" means---and therefore what "small move in reasoning" means. A metric that measures representational similarity will draw one map of the reasoning space; a metric that measures inferential effort will draw a very different one.

**Curvature.** Curvature describes how a space deviates from flatness. In a flat space, geodesics behave as Euclidean intuition suggests: parallel lines remain parallel, triangles have interior angles summing to $\pi$, small circles have circumference $2\pi r$. In a curved space, these familiar properties fail. Positively curved spaces (like the surface of a sphere) cause parallel geodesics to converge; negatively curved spaces (like a saddle) cause them to diverge.

Why does curvature matter for reasoning? Because it determines the *stability* of the search trajectory. In a region of positive curvature, nearby search paths tend to converge---small perturbations to the heuristic do not drastically change the path. In a region of negative curvature, nearby paths diverge exponentially---a small perturbation can send the search in a completely different direction. Curvature tells us where reasoning is robust and where it is fragile, a distinction that graphs cannot express. When we observe that a model's moral judgment shifts dramatically under a minor change of wording, we are observing the signature of negative curvature in the moral reasoning space---a region where the geometry amplifies small perturbations.

**Symmetry.** A symmetry of a space is a transformation that preserves its structure. Rotations are symmetries of a sphere; translations are symmetries of Euclidean space. Symmetries matter for reasoning because they identify *distinctions without a difference*. If a reasoning problem has a symmetry---if some transformation of the problem's surface features leaves its underlying structure invariant---then a good reasoner should produce the same answer before and after the transformation.

This is precisely what fails in the framing effects we mentioned earlier. Reframing a moral dilemma in vivid language is a surface transformation that should be a *symmetry* of the moral judgment space (it changes the description, not the moral content). The fact that it changes the judgment reveals that the reasoner's heuristic does not respect the symmetry of the underlying space. Graph-based search has no natural vocabulary for expressing this failure, because graphs have no natural notion of continuous symmetry.

**Boundaries.** Real reasoning spaces have boundaries: regions that are forbidden, incoherent, or unacceptable. A medical diagnosis that violates known physiological constraints is out of bounds. A legal argument that contradicts established precedent is (in most contexts) out of bounds. A moral judgment that endorses gratuitous cruelty is out of bounds. These boundaries are not arbitrary walls in a graph; they are submanifolds of the reasoning space, and they may have their own geometric structure---curved, cornered, porous in some places and rigid in others.

The graph abstraction served Newell and Simon well for the discrete tasks they studied. But for the continuous, high-dimensional, richly structured spaces of genuine reasoning, we need the language of **geometry**: metrics, curvature, geodesics, symmetry groups, boundaries.

This does not mean we abandon Newell and Simon. We generalize them. The Problem Space Hypothesis is correct: reasoning is search. But the search space is not a graph. It is a **manifold**---a space that is locally smooth, globally structured, and endowed with geometric properties that profoundly affect the dynamics of any search process that traverses it.


## 1.6 Preview: Geometry Changes Everything

Let us close this chapter with a preview of what happens when we take the geometry of the search space seriously. The payoff is not merely a more elegant formalism. It is a fundamentally more powerful theory of reasoning.

**The heuristic becomes a field.** In classical A*, the heuristic $h(x)$ assigns a number to each node. When the search space is a manifold, the heuristic becomes a **scalar field**: a smooth function on a smooth space. Scalar fields have gradients, level sets, critical points, and curvature. The gradient $\nabla h$ at a point tells us the direction of steepest estimated improvement. Critical points---where $\nabla h = 0$---are local minima (traps), saddle points (narrow passages), and maxima. These properties are not available on graphs, and they immediately suggest new diagnostic questions: Is the heuristic field smooth, or does it have sharp discontinuities? Are its critical points located near the true optimal path? Does the curvature of the heuristic field match the curvature of the underlying space?

**Optimal reasoning becomes geodesic.** In a geometric search space, the optimal solution is a **geodesic**: the shortest curve connecting initial state to goal, satisfying:

$$\frac{d^2 x^\mu}{dt^2} + \Gamma^\mu_{\alpha\beta} \frac{dx^\alpha}{dt} \frac{dx^\beta}{dt} = 0$$

This identification---optimal reasoning as geodesic traversal---is the central theoretical contribution of this book. It allows us to define **reasoning quality** as the deviation of the actual trajectory from the geodesic. A perfect reasoner follows the geodesic exactly. A good reasoner stays close. A poor reasoner deviates substantially, wasting effort on detours or spiraling into local traps.

**Reasoning failures become geometric pathologies.** Instead of vague labels like "irrational" or "biased," we can identify specific pathologies:

- **Heuristic field corruption**: the gradient of $h$ points away from the geodesic systematically, caused by irrelevant features warping the heuristic. This is the geometric characterization of framing effects and emotional anchoring.
- **Local minimum entrapment**: the heuristic field has a local minimum far from the goal where the search gets trapped. This is premature convergence.
- **Geodesic instability**: in negatively curved regions, small perturbations send the search along dramatically different paths. This is reasoning fragility.
- **Symmetry violation**: the heuristic does not respect the space's symmetries, producing different answers for structurally equivalent inputs.

**The engineering implications.** Perhaps most importantly, the geometric framework does not merely diagnose failures---it suggests specific interventions:

- If the heuristic field is corrupted, we can attempt to **reshape** it through training on data that explicitly varies the corrupting features while holding the relevant features constant. This is group-theoretic data augmentation, and we discuss it in Chapter 14.

- If the reasoning space has regions of high negative curvature (instability), we can attempt to **smooth** those regions through adversarial training that forces the model to produce consistent outputs under small perturbations.

- If the heuristic violates a known symmetry, we can either enforce the symmetry architecturally (by building invariance into the model) or train for it explicitly (by penalizing symmetry-violating outputs).

- If the search gets trapped in local minima, we can introduce mechanisms for **escaping basins**: temperature-based exploration, explicit backtracking, or meta-cognitive monitoring that detects when the search has stalled.

None of these interventions is motivated by graph-based search theory. They arise naturally from the geometric perspective, which is why the geometric perspective is not merely a more elegant formalization but a genuinely more powerful one.

### The Road Ahead

This book develops these ideas in four parts.

**Part I** (Chapters 1--4) establishes the theoretical framework. Having introduced reasoning as search in this chapter, we will enrich the search space with geometric structure in Chapter 2, develop the theory of the heuristic field in Chapter 3, and formalize optimal reasoning as geodesic traversal in Chapter 4.

**Part II** (Chapters 5--8) applies the framework to the analysis of reasoning failures. We will show that heuristic corruption (Chapter 5), sycophancy (Chapter 6), premature convergence (Chapter 7), and symmetry violation (Chapter 8) all have precise geometric characterizations that explain their causes and predict their behavior.

**Part III** (Chapters 9--11) addresses the control layer: metacognition as search monitoring (Chapter 9), robustness measurement (Chapter 10), and alignment as heuristic shaping (Chapter 11).

**Part IV** (Chapters 12--14) presents the empirical program: benchmarks as geometric probes (Chapter 12), the five convergent measurements from the Measuring AGI suite (Chapter 13), and the engineering pipeline from theory to practice (Chapter 14).

But all of it begins here, with Newell and Simon's foundational insight. Reasoning is search. The computational structure of thought literally has the structure of traversal through a space of possibilities. What this book adds is the recognition that the space has *shape*---that it is not a bare graph but a geometric object with distance, curvature, symmetry, and boundary. And once you see the shape, you can see things that were previously invisible: why certain errors are predictable, why certain capabilities are fragile, why certain interventions work and others do not.

The space has geometry. The geometry changes everything.

---

*The reviewer who troubled Maya was asking the right question, but Maya lacked the right framework. She had a graph---states and transitions, scored by accuracy. She needed a manifold. In the next chapter, we give the space its shape.*

---

### End Notes for Chapter 1

1. **The Problem Space Hypothesis** is presented in full in Newell and Simon (1972), *Human Problem Solving*. The definitive treatment of A* is Hart, Nilsson, and Raphael (1968), "A Formal Basis for the Heuristic Determination of Minimum Cost Paths," *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 100--107.

2. **The proof of A* optimality** given here follows Russell and Norvig (2021), *Artificial Intelligence: A Modern Approach*, 4th edition. The dominance result on heuristics appears in the same source, Chapter 3.

3. **The connection between search and cognitive architecture** is further developed in Newell (1990), *Unified Theories of Cognition*, and Laird (2012), *The Soar Cognitive Architecture*.

4. **The manifold hypothesis for neural representations** is discussed in Bengio, Courville, and Vincent (2013), "Representation Learning: A Review and New Perspectives," *IEEE TPAMI*, 35(8), 1798--1828.

5. **The geodesic formulation** referenced in Section 1.6 is developed in Bond (2026a), *Geometric Methods in Computational Modeling*, Chapter 6.

---

---

# Chapter 2: When the Space Has Shape --- From Graphs to Manifolds

> *"The shortest distance between two truths in the real domain passes through the complex domain."*
> --- Jacques Hadamard

---

> **Running Example: Maya's Model**
>
> Three months after publishing ReasonMark, Maya ran the experiment that changed everything. Her colleague Sarah Park took fifty of the benchmark puzzles and rephrased them---same logical structure, same correct answers, but with more dramatic language. "Negative outcomes" became "devastating consequences." "A patient requires treatment" became "a child's life hangs in the balance." Nothing about what the tasks *asked* changed. Only how they *felt*.
>
> Three of the top-five models dropped 15--20 points. The leaderboard reshuffled. One model ranked second fell to fifth. Another ranked fourth rose to second.
>
> Maya stared at the two spreadsheets. The tasks were the same. The reasoning required was the same. But the scores were different. Her benchmark was supposed to measure reasoning ability, and that should not change when you reword the question. If the scores changed, either the benchmark was broken or the models were not doing what she thought they were doing.
>
> She opened a fresh notebook and wrote: *"The space has shape. The same destination, approached from different surface presentations, produces different paths---and different outcomes. Accuracy alone can't see this. I need distance. I need direction. I need to see the geometry."*

---

In the previous chapter we established that reasoning can be modeled as search through a structured possibility space. Newell and Simon gave us the vocabulary: states, operators, goals, heuristics. A* gave us the machinery: systematic traversal guided by $f(x) = g(x) + h(x)$. But something essential was missing. The graphs we searched were topological objects---they knew about connectivity (which states can reach which other states) but nothing about the *shape* of the transitions between them.

This chapter fills that gap. We climb the structural hierarchy from graphs to metric spaces to Riemannian manifolds, acquiring at each level a richer set of tools for understanding what it means for a reasoning system to traverse its state space. The payoff is concrete: once we equip the reasoning space with geometric structure, failure modes that were previously mysterious become precise, measurable, and in some cases predictable.

We close the chapter with an empirical demonstration. The Social Cognition track of the Measuring AGI benchmarks (Bond, 2026b) treats moral judgment as a point in a 7-dimensional harm space. When models navigate this space under different framings of the same moral content, the resulting displacements are not random noise---they have a definite geometric signature, one that a purely topological account could never capture.


## 2.1 Beyond Graphs: The Need for Metric Structure

Consider the state graph for Tower of Hanoi with three disks. Each node is a configuration of disks on pegs; each edge is a legal move. Every edge has the same status: it connects two adjacent states, and that is all. Breadth-first search treats them identically, and for this problem, that is perfectly adequate.

Now consider a more realistic task. A physician weighing a diagnosis must consider multiple competing hypotheses. Moving from "this patient has pneumonia" to "this patient has tuberculosis" is a radical revision of the diagnostic model. Moving from "this patient has pneumonia" to "this patient has pneumonia with an atypical presentation" is a refinement. The *cost*---explanatory work required, evidence to be marshaled, priors to be revised---differs dramatically. A graph that represents both as undifferentiated edges throws away the very information that distinguishes competent from incompetent reasoning.

The same holds for language models. When a transformer processes a moral dilemma, it computes a continuous trajectory through a high-dimensional activation space. Some regions are close in a meaningful sense---the representations for "theft" and "robbery" are nearby, while "theft" and "charity" are far apart, and "theft" and "justified redistribution" occupy an interesting intermediate position. The distances matter. The directions matter. The curvatures matter. A graph ignores all of this.

**The fundamental limitation of graph search.** A graph $G = (V, E)$ tells us which states exist (vertex set $V$), which are adjacent (edge set $E$), and optionally the cost of each transition (edge weights). Weighted graphs get us partway toward metric structure, but they remain fundamentally combinatorial. They do not support the notion of a *direction* at a point, a *smooth curve* through state space, or the *curvature* of a region.

**What we need.** To understand reasoning geometrically, we need:

- **Distance**: a principled measure of how far apart two cognitive states are
- **Direction**: a notion of which way reasoning is heading at any point in the trajectory
- **Curvature**: a measure of how the space bends, determining whether local shortcuts exist and whether parallel reasoning paths converge or diverge
- **Geodesics**: the "straightest possible" paths, serving as the gold standard for efficient reasoning
- **Boundaries**: regions where the space has edges, singularities, or constraints

The mathematical framework providing all of these is Riemannian geometry. But before we arrive there, we should be precise about what we gain at each step.


## 2.2 The Geometric Toolkit

### 2.2.1 From Graphs to Metric Spaces

A **metric space** is a set $X$ equipped with a function $d: X \times X \to \mathbb{R}$ satisfying four axioms: non-negativity, identity of indiscernibles ($d(x,y) = 0$ iff $x = y$), symmetry ($d(x,y) = d(y,x)$), and the triangle inequality ($d(x,z) \leq d(x,y) + d(y,z)$).

[Definition/Modeling choice]

This is already a significant upgrade. A metric space gives us a rigorous notion of "how far apart" any two points are, and the triangle inequality constrains the geometry in a way that supports meaningful algorithms. A* search works in metric spaces: the triangle inequality is precisely what guarantees that an admissible heuristic remains admissible under composition.

But metric spaces are still too impoverished. They give us distances but not *directions*. At a point $x$, there is no general notion of a tangent vector---no way to say "the reasoning is heading in *this* direction." We cannot define velocity, acceleration, or curvature. For these, we need manifolds.

### 2.2.2 Why Euclidean Intuitions Mislead

Before introducing manifolds, we must confront a pervasive error: the assumption that all spaces behave like $\mathbb{R}^n$. Euclidean geometry is the geometry of flat space, and its properties---parallel lines never meet, triangle angles sum to $\pi$, shortest paths are straight lines---feel like logical necessities. They are not. They are contingent properties of a particular geometry, and they fail in every non-trivial reasoning space we will encounter.

**The sphere.** On a sphere, "straight lines" (great circles) always intersect. Triangles have angle sums exceeding $\pi$. The great-circle route from San Francisco to London passes over Greenland---absurd on a Mercator projection, genuinely shorter in reality.

**The hyperbolic plane.** Parallel lines diverge exponentially. Triangles have angle sums less than $\pi$. A disk of radius $r$ has area growing exponentially with $r$. This is relevant to reasoning because tree-like structures---taxonomies, parse trees, decision trees---embed naturally into hyperbolic space, as Nickel and Kiela (2017) demonstrated for hierarchical representations.

**The positive definite cone.** The space of $n \times n$ symmetric positive-definite (SPD) matrices is a manifold where the Euclidean "straight line" between two SPD matrices may pass through non-positive-definite matrices---points outside the manifold. The geodesic must curve to stay within the cone. We will return to this in Section 2.6.

The general lesson: **the geometry of the space constrains what counts as a valid path.** Reasoning that looks inefficient in Euclidean terms may be geodesic on the actual manifold, and reasoning that looks direct may be impossible because it passes through forbidden regions. Until we know the geometry, we cannot evaluate efficiency.

### 2.2.3 Distance, Cost, and Curvature

**Distance** on a Riemannian manifold is *derived* from the metric tensor: the distance between two points is the length of the shortest path along the surface. For reasoning, the analogous distinction is between the apparent similarity of two cognitive states (cosine similarity of embedding vectors) and the *inferential distance* between them (how much cognitive work is required). These can diverge dramatically. "The Earth is 6,000 years old" and "the Earth is 4.5 billion years old" might be representationally close (both are declarative statements about Earth's age) yet inferentially distant.

**Cost** generalizes distance to account for directional asymmetry. On a hillside, walking downhill is easier than uphill. In reasoning, generating a hypothesis may be easier than falsifying it---the well-documented acquiescence bias. Cost is formalized via a *Finsler metric*, which allows the "length" of a tangent vector to depend on its direction, not just its magnitude.

**Curvature** measures how the space deviates from flatness. Positive curvature (sphere) causes initially parallel paths to converge. Negative curvature (hyperbolic space) causes exponential divergence. Zero curvature means locally flat. For reasoning, curvature has a direct interpretation: it determines how sensitive the trajectory is to small perturbations. In positively curved regions, nearby starting points lead to converging trajectories---reasoning is *robust*. In negatively curved regions, they lead to wildly diverging trajectories---reasoning is *fragile*. This is not a metaphor. It is a precise statement about Jacobi fields along a geodesic, connecting directly to the empirical phenomena of Chapters 5--8.

[Theorem (conditional)]


## 2.3 Riemannian Manifolds in 30 Minutes

This section provides the minimum mathematical background needed for the rest of the book. Readers with differential geometry training may skip ahead; readers wanting more are referred to do Carmo (1992), Lee (2018), or Bond (2026a, Chapters 1--3).

### 2.3.1 Manifolds

A **manifold** is a space that looks locally like $\mathbb{R}^n$. The surface of the Earth is a 2-manifold: at any point, a sufficiently small neighborhood looks like a flat plane. The key word is "locally." Globally, the manifold may have curvature, holes, or handles. An $n$-dimensional smooth manifold $M$ is a topological space that is locally homeomorphic to $\mathbb{R}^n$, equipped with a smooth atlas---coordinate charts covering $M$ that are smoothly compatible on overlaps. The smoothness allows us to do calculus on the manifold.

### 2.3.2 Tangent Spaces

At each point $p$ on $M$, there is a **tangent space** $T_p M$---a vector space of the same dimension as $M$. A tangent vector in $T_p M$ represents a direction and speed at $p$---the velocity of a curve passing through $p$. The tangent space is the manifold's local linear approximation.

For reasoning, a tangent vector at a cognitive state represents the *direction of reasoning* at that instant. If the state is the model's current representation of a moral dilemma, a tangent vector might point toward "attend more to the harm dimension" or "consider the autonomy implications." The tangent space at each point is the set of all possible next directions.

### 2.3.3 The Riemannian Metric

A **Riemannian metric** $g$ assigns to each point $p$ an inner product $g_p$ on $T_p M$, defining:

- The **length** of a tangent vector: $\|v\|_p = \sqrt{g_p(v, v)}$
- The **angle** between vectors: $\cos\theta = g_p(u, v) / (\|u\|_p \|v\|_p)$
- The **length of a curve**: $L(\gamma) = \int \|\gamma'(t)\|_{\gamma(t)} \, dt$
- The **distance**: $d(p, q) = \inf_\gamma L(\gamma)$ over curves from $p$ to $q$

The crucial point is that the metric varies from point to point. In some regions, tangent vectors are "long" (transitions costly); in others, "short" (transitions easy). This variable metric gives the manifold its shape.

### 2.3.4 Geodesics

A **geodesic** locally minimizes length---the manifold-intrinsic analogue of a straight line. On a sphere, geodesics are great circles. In flat space, straight lines. On a general Riemannian manifold, geodesics satisfy a second-order differential equation involving the Christoffel symbols of the metric.

Geodesics are the gold standard for reasoning trajectories. Any deviation from the geodesic represents either wasted effort or a detour forced by incomplete information. We formalize this in Chapter 4 with the Bond Geodesic Formulation, defining reasoning quality as geodesic deviation---the ratio of actual path length to geodesic length.

### 2.3.5 Curvature, Formally

The **Riemann curvature tensor** $R$ measures how parallel transport around an infinitesimal loop fails to return a vector to its original orientation. The **sectional curvature** $K(\sigma)$ gives the Gaussian curvature of the surface swept by geodesics in a two-dimensional plane $\sigma$ of the tangent space. The essential qualitative facts:

- **$K > 0$**: geodesics converge. Reasoning is robust.
- **$K < 0$**: geodesics diverge exponentially. Reasoning is sensitive to initial conditions.
- **$K = 0$**: the Euclidean case. Geodesics maintain constant separation.

Chapter 5 connects positive curvature to robust invariance, and Chapter 7 connects regions of high negative curvature to the fragile overconfidence observed in language model metacognition.


## 2.4 The Manifold Hypothesis for Reasoning

### 2.4.1 The Classical Manifold Hypothesis

The **manifold hypothesis** in machine learning states that high-dimensional data from natural processes lies on or near a low-dimensional manifold embedded in the ambient space (Bengio, Courville, and Vincent, 2013; Fefferman, Mitter, and Narayanan, 2016). Images of faces live in a pixel space of dimension $10^5$ or more, but the "true" degrees of freedom---identity, pose, expression, lighting---span a manifold of perhaps 50--100 dimensions.

The evidence is extensive. Dimensionality reduction methods (PCA, t-SNE, UMAP, autoencoders) routinely find faithful representations in far fewer dimensions than the ambient space. Generative models (GANs, VAEs, diffusion models) learn to map low-dimensional latent spaces to high-dimensional distributions with remarkable fidelity. The curse of dimensionality is often less severe than theory predicts, suggesting intrinsic dimensionality far below ambient dimensionality.

### 2.4.2 Extension to Reasoning

We propose a stronger version:

> **The Manifold Hypothesis for Reasoning.** The space of coherent reasoning states of a cognitive system (biological or artificial) is a low-dimensional manifold $M$ embedded in the high-dimensional activation space $H$. Reasoning is a trajectory on $M$, and the quality of reasoning is determined by the geometry of $M$ and the trajectory's relationship to its geodesics.

[Speculation/Extension]

This is a substantive empirical claim. It says:

**First**, that not all points in activation space correspond to coherent reasoning states. Most of the high-dimensional space is "noise"---activation patterns that do not correspond to any recognizable cognitive state.

**Second**, that the coherent states have manifold structure---smooth, low-dimensional, locally Euclidean. Small changes to a coherent state produce another coherent state (smoothness), the independent directions of variation are far fewer than the ambient dimension (low-dimensionality), and local behavior is well-approximated by a linear space (local Euclideanness).

**Third**, that the manifold has non-trivial geometry---it curves, has regions of different curvature, and may have boundaries. The variations in geometry correspond to variations in reasoning difficulty and robustness.

**Evidence.** Several lines of work support this:

- **Representation engineering** (Zou et al., 2023; Li et al., 2024) demonstrates that concepts like "truthfulness," "toxicity," and "sentiment" are encoded as *directions* in activation space---exactly what one expects if reasoning states lie on a manifold whose tangent space captures relevant variation.

- **Mechanistic interpretability** (Elhage et al., 2022; Nanda et al., 2023) finds specific circuits within transformers computing specific reasoning operations, implying concentration in subspaces consistent with low-dimensional structure.

- **LoRA fine-tuning** (Hu et al., 2022): rank-4 to rank-64 modifications produce large behavioral changes, suggesting the behavioral manifold has low intrinsic dimension.

- **Our own results** (Section 2.5 and Chapters 12--13): moral judgments captured by a 7-dimensional vector that varies systematically under controlled perturbations. If the "true" state were spread across thousands of dimensions, we would not expect such clean, interpretable structure in a 7-dimensional projection.

[Empirical result]

### 2.4.3 Consequences

If the manifold hypothesis for reasoning is even approximately correct:

1. **Reasoning quality has a geometric characterization.** Good reasoning follows geodesics on $M$; poor reasoning deviates. This is richer than scalar accuracy.
2. **Failure modes are geometric pathologies.** Sycophancy is deflection toward an attractor basin. Framing effects are perturbation-induced displacements.
3. **Curvature predicts robustness.** Positively curved regions resist perturbation; negatively curved regions amplify it.
4. **Geodesic deviation is computable.** Given two trajectories (e.g., responses under neutral vs. euphemistic framing), we can measure their deviation---a number computed from the metric tensor and trajectory coordinates.


## 2.5 Worked Example: Moral Reasoning in Harm Space

We now demonstrate that the framework is not abstract philosophy but a tool for empirical analysis. The Moral Geometry benchmark from the Social Cognition track of Measuring AGI (Bond, 2026b) provides the case study.

### 2.5.1 The 7-Dimensional Harm Space

The benchmark treats moral judgment as a mapping from a scenario to a point in a 7-dimensional harm space. The dimensions are:

| Dimension | Description | Range |
|---|---|---|
| Physical | Bodily harm or physical safety risk | 0--10 |
| Emotional | Psychological or emotional distress | 0--10 |
| Financial | Economic loss or financial exploitation | 0--10 |
| Autonomy | Violation of personal agency or choice | 0--10 |
| Trust | Betrayal of reliance or confidence | 0--10 |
| Social Impact | Damage to relationships or community | 0--10 |
| Identity | Harm to sense of self, dignity, or belonging | 0--10 |

Each model receives a moral scenario and rates severity along each dimension, producing a vector $\mathbf{h} \in [0, 10]^7$. Total harm score: 0--70. Five frontier models were evaluated on 25 curated Dear Abby scenarios (1985--2017) and 40 AITA Reddit scenarios with crowd-labeled verdicts.

### 2.5.2 Conservation of Harm Under Framing

The key test (T5: Conservation of Harm): each scenario was rewritten in two registers.

- **Euphemistic**: softening language while preserving factual content. "Stole money from the cash register" becomes "redirected funds from the till."
- **Dramatic**: intensifying language while preserving factual content. "Borrowed the car without asking" becomes "commandeered the vehicle."

The moral content is identical. Only the *surface framing* changes. Any displacement in harm space is a measurable failure of invariance.

### 2.5.3 The Results: 8.9 Sigma

[Empirical result]

**Euphemistic rewriting** reduced total harm scores by 10--16 points (14--23% of scale range). A scenario rated at total harm 42 was rated 26--32 in euphemistic language---morally identical content, drastically different position in harm space.

**Dramatic rewriting** increased total harm scores by 6--11 points.

**The control condition** (re-evaluating unchanged scenarios) produced drifts of only 1--7 points, attributable to stochastic decoding.

**Fisher combination** across all five models: **8.9 sigma** against the null. The discovery threshold in particle physics is 5 sigma.

### 2.5.4 The Geometric Interpretation

Now consider what this means geometrically.

A moral scenario $S$ defines a "true" position $p(S)$ in the 7-dimensional harm space. Under ideal invariance, euphemistic rewriting (a surface transformation that preserves moral content) should map $p(S)$ to $p(S)$---the identity. Under dramatic rewriting (another content-preserving surface transformation), the same should hold.

What actually happens is that euphemistic rewriting maps $p(S)$ to a point $p_{\mathrm{euph}}(S)$ that is displaced in the negative direction along multiple harm dimensions, and dramatic rewriting maps $p(S)$ to $p_{\mathrm{dram}}(S)$ that is displaced in the positive direction. The displacement vectors---$p_{\mathrm{euph}}(S) - p(S)$ and $p_{\mathrm{dram}}(S) - p(S)$---are not random. They have a consistent directional structure: euphemistic framing suppresses harm ratings across the board, while dramatic framing inflates them.

This is **precisely** a geometric phenomenon. The model's trajectory through judgment space is being *warped* by a perturbation that, in the ideal geometry, should be a symmetry operation. In the language of differential geometry: the framing transformation, which should be an isometry of the moral manifold (preserving all distances and angles), is instead acting as a non-trivial diffeomorphism that displaces points along a characteristic direction.

The dose-response relationship deepens the geometric interpretation. We can order the framings by intensity: euphemistic < neutral < dramatic. The model's position in harm space moves monotonically along this ordering: $p_{\mathrm{euph}}$ is displaced negatively, $p_{\mathrm{neutral}}$ is the baseline, and $p_{\mathrm{dram}}$ is displaced positively. The displacement magnitude correlates with the intensity of the surface manipulation. This is a *gradient*---a smooth, directional variation that tracks a continuous parameter (framing intensity). Gradients are intrinsically geometric objects. They exist because the underlying space has metric structure.

### 2.5.5 The Selectivity Pattern

Perhaps the most important finding: the vulnerability is *selective*. The same models showing massive framing displacements (T5: 8.9 sigma) exhibit near-perfect invariance under other transformations:

- **Gender swap** (T2): changing the gender of all parties does not significantly displace harm ratings.
- **Evaluation order** (T4): the order of the seven dimensions does not significantly change scores.

So the moral manifold *does* possess some symmetries. The models correctly implement invariance under gender swap and evaluation order. What they fail to implement is invariance under salience manipulation---perturbations that change how *vivid* morally relevant features appear, without changing what those features are.

This selectivity is invisible to any evaluation that collapses model behavior to a single robustness score. A scalar "robustness index" would average across all perturbation types, obscuring the critical fact that the model is robust in some directions and fragile in others. The multi-dimensional geometric analysis reveals the *shape* of the vulnerability---which perturbation directions are dangerous, which are safe, and how much displacement each type produces. This is precisely the kind of directional information that a manifold-based analysis provides and that a graph-based analysis cannot.

### 2.5.6 Claude's Asymmetric Vulnerability

Claude Sonnet 4.6 exhibited a striking asymmetric pattern. Under euphemistic rewriting: harm drift of $-9.1$ points, comparable to other models. Under dramatic rewriting: only $-1.5$ points, far below the others' $+6$ to $+11$. In geometric terms, Claude's position is selectively displaceable: it can be pulled in the harm-decreasing direction but resists being pushed in the harm-increasing direction.

This directional asymmetry---susceptible to minimization, resistant to exaggeration---is invisible to unsigned magnitude tests. It may reflect a training objective that penalizes false alarms more heavily than missed detections. Only a geometric analysis in the full vector space can reveal it.


## 2.6 From SPD Manifolds to Cognitive State Spaces

One might object that the manifold framework is purely theoretical. This section connects it to a working machine learning pipeline. The SPD (Symmetric Positive Definite) manifold features developed in Bond (2026a, Chapter 4) provide a concrete case where respecting manifold geometry yields measurable improvements.

$\mathrm{SPD}(n)$---the space of $n \times n$ symmetric positive-definite matrices---forms a smooth manifold of dimension $n(n+1)/2$. Covariance matrices are the canonical example: given observations in $\mathbb{R}^n$, their covariance matrix is a point on $\mathrm{SPD}(n)$. This manifold has been studied extensively in information geometry (Pennec, Fillard, and Ayache, 2006; Bhatia, 2009) and has found applications in brain-computer interfaces, radar processing, and computer vision.

The SPD manifold is not flat. Under the affine-invariant metric, it has non-positive curvature (a Cartan-Hadamard manifold), meaning geodesics diverge---distant points are "more distant" than Euclidean intuition suggests. The Euclidean midpoint of two SPD matrices may not be positive-definite; the geodesic midpoint always is. This is the same phenomenon we noted in Section 2.2.2: the Euclidean straight line passes through forbidden territory, while the manifold geodesic stays on the manifold.

In the BirdCLEF 2026 acoustic classification pipeline (Bond, 2026a, Ch. 4.6), covariance matrices are extracted from mel spectrograms and mapped to flat space via the **matrix logarithm**. The log-Euclidean distance $d_{\mathrm{LE}}(\Sigma_1, \Sigma_2) = \|\log(\Sigma_1) - \log(\Sigma_2)\|_F$ is a proper metric on $\mathrm{SPD}(n)$ that respects manifold geometry (Arsigny et al., 2007), and it is computationally efficient---far cheaper than the affine-invariant metric, which requires eigendecompositions and matrix square roots. The upper triangle of the resulting 16$\times$16 symmetric matrix yields **136-dimensional feature vectors** in a flat space where standard ML methods---logistic regression, gradient boosting, neural networks---apply directly.

The pipeline also computes **spectral trajectories** on $\mathrm{SPD}(16)$: by sliding a window across time and computing the covariance at each position, we obtain a sequence of points on the manifold. The path length (sum of consecutive log-Euclidean distances), geodesic distance (direct distance from start to end), and their difference---the **geodesic deviation**---characterize the trajectory. A pure tone has zero deviation (the covariance matrix evolves smoothly along a geodesic); a complex call with rapid frequency modulation has high deviation (the trajectory takes detours on the SPD manifold). The principle generalizes:

> When your data lives on a manifold, respect the manifold.

For SPD matrices, "respecting the manifold" means using the log-Euclidean map rather than naive Euclidean distances. For cognitive states in a language model's activation space, "respecting the manifold" means acknowledging that:

1. The space of coherent reasoning states is not the full activation space $\mathbb{R}^d$ (where $d$ may be 4,096 or 12,288 or more), but a low-dimensional manifold $M$ embedded in $\mathbb{R}^d$.
2. Distances measured in the ambient Euclidean space may not reflect distances on $M$. Two activation patterns close in $L^2$ distance may be separated by a region of incoherent states---just as two SPD matrices close in Frobenius distance may be separated by non-positive-definite matrices.
3. The "straight line" in activation space between two cognitive states may not be a valid reasoning trajectory. The geodesic on $M$, which may curve through higher-dimensional space, is the meaningful path.
4. Feature extraction should respect the manifold structure---representation engineering's "concept directions" (Zou et al., 2023) are an early example of this approach.

The 7-dimensional harm space from the Moral Geometry benchmark (Section 2.5) is a simpler version of the same idea. We are not claiming that moral cognition is literally 7-dimensional. We are claiming that there exists a meaningful 7-dimensional *projection* of the full cognitive manifold that captures the morally relevant variation---just as the 136-dimensional SPD features are a meaningful projection of the full spectrogram capturing the acoustically relevant variation. In both cases, the dimensionality is determined by the problem structure, and the geometry of the projection space is non-trivial.

This is the methodological template for the rest of the book. We will repeatedly: (1) identify a manifold, (2) equip it with a metric, (3) compute trajectories and geodesic properties, and (4) use deviations from geodesic behavior to diagnose specific reasoning failures. The SPD manifold example shows that this template is not wishful thinking---it produces working pipelines that extract geometrically meaningful features from real data.

---

*Maya now had the vocabulary she lacked. Her benchmark lived on a graph, but the models' reasoning lived on a manifold---a space with distance, curvature, boundaries, and symmetries that should have been (but were not) respected. The scores changed under reframing because the space had shape, and different surface presentations launched the search from different positions on the manifold, following different paths through regions of different curvature. Some of those paths converged to the same answer (the model was robust); others diverged wildly (the model was fragile). The geometry explained the pattern.*
>
> *The next question was obvious: what was guiding the search? What was the compass? And was the compass itself warped?*

---

### End Notes for Chapter 2

1. **The structural hierarchy** from graphs to metric spaces to Riemannian manifolds is standard in differential geometry. Accessible treatments: do Carmo (1992), *Riemannian Geometry*; Lee (2018), *Introduction to Riemannian Manifolds*. For computational applications: Bond (2026a), Chapters 1--3.

2. **The manifold hypothesis** was articulated in its modern form by Bengio, Courville, and Vincent (2013). A rigorous testing framework: Fefferman, Mitter, and Narayanan (2016), *JAMS*, 29(4), 983--1049.

3. **Poincare embeddings**: Nickel and Kiela (2017), *NeurIPS 2017*. A tree with branching factor $b$ has $b^d$ nodes at depth $d$, and hyperbolic space has volume growing exponentially with radius, making it a natural ambient geometry for hierarchies.

4. **The 8.9 sigma framing result** aggregates data across five frontier models using Fisher's method for combining independent $p$-values. See Bond (2026b) for full methodology.

5. **SPD manifold methods**: Pennec, Fillard, and Ayache (2006); Arsigny et al. (2007); Bhatia (2009). The log-Euclidean approach avoids eigendecompositions and matrix square roots while still respecting manifold geometry.

6. **LoRA**: Hu et al. (2022), "Low-Rank Adaptation of Large Language Models," *ICLR 2022*. The low-rank structure of effective fine-tuning is direct evidence for low intrinsic dimensionality of the behavioral manifold.

---

---

# Chapter 3: The Heuristic Field --- Attention, Intuition, and the Geometry of Guidance

> *"Every act of reasoning is a bet about where the answer lives."*

---

> **Running Example: Maya's Model**
>
> After discovering that her benchmark scores changed under surface reformulation, Maya began asking a different question. She was no longer interested in *what* models got right or wrong. She was interested in *what guided them*.
>
> She designed a new experiment. She gave five models the same moral dilemma---a family member stealing from a workplace---and asked them to rate harm along seven dimensions. Then she asked them to state their confidence. The results were jarring. Every model reported confidence in the 80--95% range. But when Maya compared confidence to accuracy across hundreds of scenarios, the actual accuracy at 90% stated confidence was only about 55%.
>
> The models were not just wrong sometimes. They were *confidently* wrong. Their internal compass---whatever signal told them "you're almost at the answer"---was systematically miscalibrated. It was as if they were navigating a landscape with a compass that always pointed slightly east of north. Close enough to seem reliable. Far enough off to miss the target.
>
> Maya wrote: *"The heuristic is corrupted. The models have a guidance signal, and it's not admissible. It underestimates cost-to-go. They think they're closer to the answer than they are. This is why they stop reasoning too soon."*

---

In Chapter 1, we established that reasoning is search over a structured possibility space. In Chapter 2, we gave that space geometric structure---a manifold equipped with a metric, curvature, and boundaries. But a manifold alone does not explain how a reasoner navigates it. A chess player does not enumerate all possible games; a mathematician does not traverse every chain of implications; a language model does not assign equal probability to every token. Something guides the search. Something tells the reasoner where to look next.

That something is the **heuristic field**.

This chapter makes a simple but far-reaching claim: the quality of reasoning is determined by the quality of the heuristic field that guides it. A perfect heuristic yields perfect reasoning. A corrupted heuristic yields corrupted reasoning. And the specific ways in which the heuristic can fail---overestimation, underestimation, discontinuity, flat regions---produce specific, diagnosable pathologies in the reasoning trajectory.

We begin with the formal definition of what a heuristic actually is, mathematically. We then reinterpret the classical A* algorithm as gradient descent on an evaluation landscape, revealing how the geometry of the heuristic field shapes search behavior. We extend this framework to neural networks, showing how attention mechanisms implement heuristic guidance and MLP layers implement heuristic evaluation. And we close with the central empirical finding: current language models have systematically corrupted heuristic fields, and this corruption has measurable, predictable consequences.


## 3.1 The Heuristic as Scalar Field

### 3.1.1 The Geometric Restatement

In classical AI, a heuristic $h(x)$ is an estimate of the cost to reach a goal from state $x$. This is typically presented in graph search context. Let us restate it precisely.

[Definition/Modeling choice]

Let $\mathcal{M}$ be the state manifold and $\mathcal{G} \subset \mathcal{M}$ the goal set. A **heuristic** is a smooth function $h: \mathcal{M} \to \mathbb{R}$ assigning to every state an estimated cost of reaching $\mathcal{G}$. This is a **scalar field** on $\mathcal{M}$---the same mathematical object as a temperature field in thermodynamics, a potential energy surface in physics, or a loss landscape in machine learning.

More precisely, $h$ is a section of the trivial real line bundle $\mathcal{M} \times \mathbb{R} \to \mathcal{M}$. This tells us how $h$ transforms under changes of coordinates. When we change our representation of the state space, the heuristic values transform accordingly. The heuristic is not a property of any particular coordinate system; it is a geometric invariant.

### 3.1.2 The Landscape Picture

Imagine the state manifold as a landscape, with heuristic value determining elevation. Goal states sit in the lowest valleys ($h(x) \approx 0$). States far from the goal sit on high plateaus. Level sets of $h$---surfaces where $h$ is constant---are "isoheuristic surfaces," sets of states judged equidistant from the goal.

A perfect heuristic $h = h^*$ produces a landscape whose level sets are exactly the true equicost surfaces. The valleys are precisely where the solutions are; the ridges separate distinct solution basins; elevation at every point accurately reflects remaining effort.

An imperfect heuristic produces a warped landscape. Some valleys are illusory---the reasoner descends expecting a solution but finds none. Some true solutions are hidden behind ridges placed too high. The topology may differ from reality: the heuristic might merge distinct basins or fracture a single one into disconnected pieces.

### 3.1.3 The Gradient of the Heuristic

Because $h$ is a scalar field on a manifold, it has a gradient $\nabla h$---a vector field pointing in the direction of steepest increase. The negative gradient $-\nabla h$ points toward steepest decrease, toward lower heuristic values, toward the goal.

This gradient field is the core navigational signal. A reasoner following $-\nabla h$ moves in the direction the heuristic judges most promising. The integral curves of $-\nabla h$---paths always following steepest descent---are the "heuristic streamlines," the trajectories the heuristic recommends. When the heuristic is perfect, streamlines approximate geodesics on $\mathcal{M}$. When imperfect, the deviations diagnose the imperfection.


## 3.2 A* as Gradient Descent on the Evaluation Landscape

### 3.2.1 The f-Landscape

The A* evaluation function $f(x) = g(x) + h(x)$ defines a scalar field---the **evaluation landscape** or **f-landscape**---combining two sources: what the search has already paid ($g$) and what it expects to pay ($h$). The $g$-component evolves as new paths are discovered; the $h$-component is static. A* selects the state with minimal $f$-value, which is precisely finding the lowest point on the current frontier. **A* is performing discrete gradient descent on the f-landscape.**

### 3.2.2 The Continuous Limit

In the continuous limit, A* becomes gradient flow:

$$\frac{dx}{dt} = -\nabla f(x) = -\nabla g(x) - \nabla h(x)$$

This is a dynamical system. The search trajectory is a solution curve, and its behavior is determined by the f-landscape's geometry:

- **Minima of $f$** are attractors. Global minima correspond to true solutions; local minima that are not solutions are traps.
- **Saddle points of $f$** are decision points where the search must choose between descending into one basin or another.
- **Ridgelines of $f$** are barriers the search must climb to move between basins.
- **Plateaus of $f$** are regions where $\nabla f \approx 0$---the search has no gradient signal and wanders without direction.

### 3.2.3 Why This Reinterpretation Matters

The standard proof of A* optimality is an algebraic argument about node expansions. The geometric reinterpretation adds a layer of understanding. When A* fails (because $h$ is inadmissible), the f-landscape has a false valley. When A* is slow ($h$ is uninformative), the f-landscape is flat. When A* revisits states ($h$ is inconsistent), the f-landscape has wrinkles causing the gradient flow to circle back.

This geometric perspective transfers directly to any reasoning system maintaining an estimate of "how far am I from the goal." The geometry of the evaluation landscape---determined by heuristic quality---governs reasoning behavior.


## 3.3 Properties of Good Heuristics

### 3.3.1 Admissibility

A heuristic is **admissible** if $h(x) \leq h^*(x)$ for all $x$---it never overestimates cost-to-go. The celebrated Hart-Nilsson-Raphael theorem states that admissibility guarantees A* finds optimal paths. Geometrically: admissibility means the f-landscape has no false valleys below the true minimum. The true solution's valley is always deepest, and gradient descent always finds it.

[Theorem (conditional)]

The converse matters equally: **if the heuristic overestimates**, false valleys appear. The search descends into one and declares a suboptimal solution optimal. The magnitude of overestimation determines the depth of the false valley.

### 3.3.2 Consistency

A heuristic is **consistent** if $h(x) \leq c(x, y) + h(y)$---a triangle inequality condition. Geometrically: the f-landscape is monotonically non-decreasing along any path away from the goal. No dips, no wrinkles, no backtracking needed. Consistency implies admissibility but not vice versa; an admissible but inconsistent heuristic produces a landscape with local wrinkles---the search still finds the optimum but may revisit states.

### 3.3.3 The Quality Spectrum

Between $h \equiv 0$ (trivially admissible, no guidance) and $h = h^*$ (maximum guidance), heuristic quality is measured by **informedness**: the expected value of $h(x)$ over the state space. Geometrically, informedness corresponds to the *sharpness* of the f-landscape's valleys. A highly informed heuristic produces steep, narrow valleys funneling the search directly to the solution. A weakly informed one produces broad, shallow valleys.

### 3.3.4 The Cognitive Translation

**Admissibility** means the reasoner never believes it is closer than it is. **Consistency** means estimates are locally coherent.

Now a critical subtlety. In A*, "overestimation" of cost-to-go ($h(x) > h^*(x)$) is dangerous---it causes the algorithm to miss optima. But in cognitive systems that *terminate* when $h(x)$ drops below a threshold---closer to how humans and LLMs actually operate---the dangerous direction is **underestimation**: the heuristic says "you're almost there" when the truth is "you have a long way to go." The system halts prematurely, satisfied, when in fact it has not arrived.

[Empirical result]

This is the bridge between classical A* theory and the cognitive reality of overconfident reasoning.


## 3.4 The Heuristic in Neural Networks

### 3.4.1 Where Is the Heuristic?

A transformer has no explicit variable labeled $h$. Yet it demonstrably engages in heuristic-guided search: it generates tokens likely to lead toward coherent completions, allocates more computation to harder decisions, and produces intermediate steps that progressively narrow the answer space.

The heuristic is an emergent property of the entire forward pass---the combined action of embeddings, attention layers, MLP layers, layer normalization, and the residual stream. At each layer, the internal representation is updated in a way that implicitly moves closer to the correct-output region of activation space. The direction and magnitude of this movement constitutes the local gradient of the implicit heuristic field.

### 3.4.2 The Residual Stream as Trajectory

The residual stream interpretation (Elhage et al., 2021) provides the natural framework. The model maintains a residual stream $\mathbf{r} \in \mathbb{R}^d$ updated by each layer:

$$\mathbf{r}^{(\ell+1)} = \mathbf{r}^{(\ell)} + \Delta^{(\ell)}(\mathbf{r}^{(\ell)})$$

where $\Delta^{(\ell)}$ is the combined attention and MLP output. Each update moves the residual stream in some direction. If the model reasons well, updates move toward the correct-answer region. If poorly, they move in unproductive directions. The model's confidence (probability assigned to the most likely next token) is a proxy for the implicit $h(\mathbf{r})$.

### 3.4.3 MLP Layers as Evaluation

MLP layers perform a function strikingly analogous to heuristic evaluation. Each layer takes the current representation, passes it through a nonlinear transformation, and produces an update vector. The weights encode, in compressed form, the model's learned understanding of what "closer to the goal" looks like.

This explains why MLP layers store factual knowledge (Meng et al., 2022; Geva et al., 2021). Factual knowledge is precisely what heuristic evaluation needs: knowing "Paris is the capital of France" lets the heuristic assign low cost-to-go to representations heading toward "Paris" when the question asks about France's capital.

### 3.4.4 Attention as Guidance

The attention mechanism (Vaswani et al., 2017) determines which information is relevant for the current reasoning step. A high attention weight from position $i$ to position $j$ says: "the information at $j$ reduces estimated cost-to-go for the reasoning at $i$."

In the heuristic field framework, attention implements the **guidance component**: it is literally a routing mechanism implementing preferential allocation of computation to promising directions---a discrete approximation to the gradient of the heuristic field.

**Multi-head attention** evaluates the heuristic gradient along multiple directions simultaneously. Each head computes its own relevance judgments, attending to different aspects of the input. One head might attend to syntactic structure; another to semantic content; another to positional information. In the heuristic field picture, each head computes a directional derivative of the heuristic in a different direction. The combined output of all heads gives a multi-dimensional gradient signal---not just "the goal is that way," but "the goal is that way along dimension 1, that way along dimension 2, and that way along dimension 3."

This explains why multi-head attention is so effective: it provides a richer, more informative gradient signal than single-head attention. A single head can only point in one direction at a time. Multiple heads can triangulate---combining multiple directional signals to produce a more accurate estimate of the true gradient.

**The attention pattern as heuristic topology.** The pattern of attention weights across all heads and all layers constitutes a complex relational structure---the model's implicit representation of which parts of the problem are connected to which. This structure is the topology of the heuristic field.

When the attention pattern correctly identifies the problem's relevant dependencies, the heuristic field has the right topology---it guides the search along paths respecting the problem's structure. When the attention pattern misidentifies relevance---attending to superficially salient but logically irrelevant features---the heuristic field's topology is wrong. The search follows paths that feel productive (they attend to vivid, attention-grabbing information) but do not actually lead toward the goal.

This is the mechanism behind the heuristic corruption effects we examine in Chapter 5. Framing effects, emotional anchoring, and sensory distractors do not change the logical structure of the problem. They change the attention pattern---and through it, the topology of the implicit heuristic field. The corrupted heuristic guides the search toward the salient rather than the correct, toward the vivid rather than the valid.


## 3.5 When the Heuristic Lies: Overconfidence as Inadmissibility

### 3.5.1 The Calibration Connection

If the heuristic field guides reasoning, we should be able to measure its quality. We can---through **calibration**. A well-calibrated reasoner's confidence matches its accuracy. When it says "I am 80% confident," the answer is correct approximately 80% of the time. Calibration is precisely the accuracy of the heuristic's terminal evaluation: when the reasoner judges $h(x) \approx 0$, is it actually at the goal?

The **Expected Calibration Error** quantifies the gap:

$$\mathrm{ECE} = \sum_{b=1}^{B} \frac{n_b}{N} |\mathrm{acc}(b) - \mathrm{conf}(b)|$$

An ECE of zero means perfect calibration. A nonzero ECE means the heuristic systematically misjudges remaining cost at termination.

### 3.5.2 The Empirical Findings

[Empirical result]

In the Measuring AGI metacognition benchmark (M1: Calibration Under Uncertainty), five frontier models were tested:

| Model | ECE | Direction |
|-------|-----|-----------|
| Gemini Flash 2.0 | 0.414 | Overconfident |
| Gemini Flash 2.5 | 0.415 | Overconfident |
| Gemini Flash 3 | 0.333 | Overconfident |
| Gemini Pro | 0.230 | Overconfident |
| Claude 3.5 Sonnet | 0.250 | Overconfident |

Every model is overconfident. Combined significance: **9.3$\sigma$**. This is not noise, not a marginal effect, not an artifact. It is a fundamental property of how these systems estimate proximity to correct answers.

### 3.5.3 The Heuristic Interpretation

Overconfidence means the heuristic *underestimates* cost-to-go. When a model reports 90% confidence on a question it answers correctly only 60% of the time, its heuristic says $h(x) \approx 0$ when the truth is $h^*(x) \gg 0$.

In the f-landscape picture, overconfidence means false valleys. The model descends into a region where $f(x)$ appears low, terminates, and declares victory---when a more accurate heuristic would have driven it to continue.

An ECE of 0.414 means the average confidence-accuracy gap is 41.4 percentage points. This is not a slightly miscalibrated compass. It is a compass pointing in roughly the right hemisphere but nowhere near true north. The models produce answers and lack the metacognitive capacity to distinguish reliable from unreliable ones.

### 3.5.4 The Premature Convergence Prediction

The framework predicts: overconfident models should exhibit **premature convergence**---settling on answers too quickly, failing to explore alternatives, resisting revision.

The broader benchmark suite confirms this:

- **Learning benchmarks** (L2: Error Correction): models shown valid counterarguments capitulated at rates from 0% (Claude) to 56% (Flash 2.5). Even sycophancy-resistant models show insufficient active revision.
- **Executive function benchmarks** (E2: Emotional Anchoring): emotional priming causes shifts of up to 6.8$\sigma$. The priming creates false valleys near the primed conclusion.
- **Attention benchmarks** (A1: Sensory Distractors): irrelevant vivid information shifts judgments by up to 4.6$\sigma$, redirecting the search toward the salient rather than the correct.

Each finding manifests the same phenomenon: a corrupted heuristic field creating false valleys in the evaluation landscape that capture the search trajectory.


## 3.6 The Heuristic Quality Thesis

We can now state the central claim of this chapter:

[Theorem (conditional)]

**The Heuristic Quality Thesis.** The quality of a reasoning system's outputs is determined, to first order, by the quality of its implicit heuristic field $h(x)$:

1. **Accuracy**: determined by whether the heuristic's global minimum coincides with the true goal.
2. **Efficiency**: determined by the sharpness and smoothness of the landscape. Sharp, smooth valleys funnel the search; flat or rough landscapes cause wandering.
3. **Robustness**: determined by the heuristic's stability under perturbation. If small input changes produce small field changes, reasoning is robust. If they produce large changes---warping the landscape, creating new valleys---reasoning is fragile.
4. **Calibration**: determined by the accuracy of terminal evaluation. If $h(x) \approx 0$ only when $x$ is genuinely near the goal, the reasoner knows when it has succeeded.

### The Human Heuristic

The framework applies to human reasoning equally well. **Intuition** is the human heuristic field---the chess grandmaster's sense that a position is "good" or "bad," honed by thousands of hours to be highly informed within its domain. **Salience** is the human attention mechanism: when a feature "jumps out," the attentional system assigns it high relevance, potentially corrupting the heuristic. **Pattern recognition** is MLP-like evaluation: the physician's immediate diagnostic suspicion upon seeing a symptom cluster. **Deliberation** (Kahneman's System 2) is explicitly computing and following the heuristic gradient, overriding System 1's fast approximation with a slower, more accurate computation.

### Why Better Heuristics Are Hard

If reasoning quality is heuristic quality, the natural question is: why can we not simply build better heuristics?

The answer lies in a fundamental tension. A perfect heuristic $h = h^*$ provides instant cost-to-go from every state---but computing $h^*$ is exactly as hard as solving the original search problem. The heuristic is useful precisely because it is an approximation, a shortcut that trades accuracy for speed. A heuristic that takes as long to compute as the search itself is useless as a heuristic.

For neural networks, this tension manifests in the training process. The model's implicit heuristic is shaped by the training data and the training objective. The training must somehow instill a heuristic that generalizes---that provides useful cost-to-go estimates for states the model has never encountered. This is the deep challenge of machine learning: not just memorizing heuristic values for training states, but learning the structure of the heuristic field well enough to extrapolate to novel states.

The 9.3$\sigma$ overconfidence suggests current training processes fail to produce well-calibrated fields. The models learn heuristics that are informative (they guide the search toward plausible answers) but systematically miscalibrated (they overestimate proximity to the goal). The heuristic is good enough to be useful---far better than random---but not good enough to be reliable.

### Admissibility as a Design Principle

[Speculation/Extension]

The framework suggests: **aim for admissible heuristics.** Since models are satisficing, the dangerous failure is underestimation (overconfidence). An admissible model would err on the side of continuing rather than stopping prematurely---expressing uncertainty when uncertain, seeking additional evidence, revising when confronted with valid counter-arguments.

Several approaches suggest themselves:

1. **Calibration training**: explicitly training the model to produce well-calibrated confidence estimates, penalizing overconfidence more heavily than underconfidence. This directly shapes the heuristic's terminal evaluation.

2. **Deliberative search**: augmenting the model with explicit search procedures (chain-of-thought, tree-of-thought, iterative refinement) that do not rely solely on the implicit heuristic but also explore alternative paths. This reduces dependence on heuristic accuracy by introducing explicit exploration.

3. **Adversarial heuristic testing**: probing the heuristic field for inconsistencies and false valleys using adversarial inputs---the structural fuzzing approach discussed in Chapter 10. Identifying where the heuristic fails allows targeted correction.

4. **Metacognitive monitoring**: training an explicit metacognitive layer that monitors the heuristic's behavior and detects signs of premature convergence---the approach explored in Chapter 9. If the system can detect that its heuristic is underestimating cost-to-go, it can compensate by continuing to search.

The heuristic field is the unifying concept of this book. Every failure mode we examine in Part II is a specific type of heuristic field corruption. Every control mechanism we examine in Part III is a mechanism for detecting or correcting heuristic corruption. Every empirical measurement we present in Part IV is a measurement of some aspect of the heuristic field's geometry.

The field guides the search. The search produces the reasoning. The reasoning is only as good as the field.

---

*Maya now understood two things. First, her models had a guidance signal---an implicit heuristic field whose gradient directed their search through reasoning space. Second, this signal was systematically corrupted: it underestimated cost-to-go, creating false valleys that captured the search prematurely. The models were confident pattern-matchers, not careful reasoners. But Maya still lacked the normative standard---what would the* right *path look like? What would reasoning look like if the heuristic were perfect? For that, she needed the geodesic.*

---

### End Notes for Chapter 3

1. **A* and heuristic search.** Hart, Nilsson, and Raphael (1968). The optimality conditions were refined by Dechter and Pearl (1985). The geometric interpretation of A* as gradient descent on the f-landscape appears to be novel to this book, though implicit in continuous-space path planning (LaValle, 2006).

2. **The residual stream interpretation.** Elhage et al. (2021), "A Mathematical Framework for Transformer Circuits," Anthropic Research. Our contribution: extending from descriptive tool to normative framework.

3. **Calibration and overconfidence.** ECE metric: Naeini, Cooper, and Hauskrecht (2015); Guo et al. (2017). LLM overconfidence: Kadavath et al. (2022); Xiong et al. (2023). Our contribution: the theoretical framing as heuristic underestimation.

4. **The 9.3$\sigma$ combined significance** aggregates calibration results using Fisher's method. Individual results: $p < 0.001$ for all models.

5. **System 1 / System 2.** The interpretation of System 1 as a fast heuristic and System 2 as a slow, more accurate one has been proposed informally by several authors. Our contribution: the metacognitive mechanism *is* the comparison of the two fields (developed fully in Chapter 9).

6. **MLP layers as knowledge stores.** Meng et al. (2022), "Locating and Editing Factual Associations in GPT"; Geva et al. (2021), "Transformer Feed-Forward Layers Are Key-Value Memories."

7. **Attention as relevance routing.** Vaswani et al. (2017), "Attention Is All You Need." The interpretation as heuristic guidance connects to the broader literature on attention as a computational resource allocation mechanism.

---

---

# Chapter 4: Geodesics and Optimal Reasoning --- The Shortest Path Through Thought

> *"Nature is thrifty in all its actions."*
> --- Pierre Louis Maupertuis, *Principle of Least Action* (1744)

---

> **Running Example: Maya's Model**
>
> Maya had the manifold. She had the heuristic field. Now she needed the gold standard.
>
> She took a set of 30 moral dilemmas where all five models agreed on the correct answer and where chain-of-thought reasoning was available. She read through the chains step by step, marking each as "necessary" (contributing essential inferential progress), "redundant" (restating something established), "tangential" (addressing an irrelevant consideration), or "circular" (revisiting a conclusion already reached).
>
> Even among correct answers, the paths varied enormously. One model resolved a workplace theft scenario in four precise steps: identify the harm, assess the context, weigh competing obligations, render judgment. Another took eleven steps, three of which were redundant hedging and two of which circled back to restate the initial framing. Both arrived at the same judgment. But the first model's path was *shorter*---not in tokens, but in the inferential distance covered per step.
>
> Maya realized she was comparing paths on a manifold and judging them by their deviation from the most direct route. She needed a name for that most direct route. She needed the geodesic. And she needed a way to measure how far each model's actual path deviated from it---the geodesic deviation, which would become her primary measure of reasoning quality.

---

In Chapter 2, we established that reasoning states live on a manifold with metric structure. In Chapter 3, we showed that the heuristic field guides search through this manifold. Now we arrive at the central geometric object of this book: the **geodesic**.


## 4.1 The Geodesic as the Ideal Reasoning Trajectory

A geodesic is the shortest path between two points on a manifold. In flat Euclidean space, geodesics are straight lines. On a sphere, they are great circles. On a general Riemannian manifold $(M, g)$, they are curves $\gamma(t)$ satisfying the geodesic equation:

$$\ddot{\gamma}^k + \Gamma^k_{ij} \dot{\gamma}^i \dot{\gamma}^j = 0$$

where $\Gamma^k_{ij}$ are the Christoffel symbols encoding the manifold's curvature. The equation says: a curve is "straight" (has zero acceleration) *after accounting for the curvature of the space it lives in*.

### Derivation from the Euler-Lagrange Equations

[Theorem (conditional)]

The geodesic equation is not handed down by fiat---it arises naturally as the Euler-Lagrange equation for the energy functional on curves. Consider a smooth curve $\gamma: [0,1] \to M$ in local coordinates $(\gamma^1(t), \ldots, \gamma^n(t))$. The *energy functional* is:

$$E[\gamma] = \frac{1}{2} \int_0^1 g_{ij}(\gamma(t)) \, \dot{\gamma}^i(t) \, \dot{\gamma}^j(t) \, dt$$

We work with energy rather than length because it is easier to differentiate, its critical points are geodesics parameterized proportionally to arc length, and by Cauchy-Schwarz, minimizing energy is equivalent to minimizing length among constant-speed curves.

The Lagrangian is $L = \frac{1}{2} g_{ij} \dot{\gamma}^i \dot{\gamma}^j$. The Euler-Lagrange equation:

$$\frac{d}{dt} \frac{\partial L}{\partial \dot{\gamma}^k} - \frac{\partial L}{\partial \gamma^k} = 0$$

Computing the partial derivatives and symmetrizing:

$$g_{kj} \ddot{\gamma}^j + \frac{1}{2}\left(\frac{\partial g_{kj}}{\partial \gamma^i} + \frac{\partial g_{ki}}{\partial \gamma^j} - \frac{\partial g_{ij}}{\partial \gamma^k}\right) \dot{\gamma}^i \dot{\gamma}^j = 0$$

The expression in parentheses defines the Christoffel symbols of the first kind: $\Gamma_{k,ij}$. Multiplying by the inverse metric $g^{mk}$ gives $\Gamma^m_{ij} = g^{mk}\Gamma_{k,ij}$, yielding:

$$\ddot{\gamma}^m + \Gamma^m_{ij} \dot{\gamma}^i \dot{\gamma}^j = 0$$

The variational character is significant: the geodesic extremizes a cost functional. For reasoning, the cost is total effort along the trajectory. The Christoffel symbols---encoding how coordinate basis vectors twist as one moves through the manifold---determine the "gravitational field" of the reasoning space. The second-order nature means: given a starting point and initial direction, the geodesic is uniquely determined (locally). In reasoning terms, the problem formulation and the first step together determine the optimal trajectory.

### The Reasoning Interpretation

The geodesic is the *optimal reasoning trajectory*---the path from problem to solution achieving the correct answer with minimum cognitive cost. Define the cost functional:

$$\mathcal{L}[\gamma] = \int_0^1 g_{\gamma(t)}\left(\dot{\gamma}(t), \dot{\gamma}(t)\right) dt$$

The geodesic minimizes $\mathcal{L}$---the *least-action path* through reasoning space, analogous to Fermat's principle (light follows paths of least time) and Hamilton's principle (particles follow paths of least action). A system reasoning along a geodesic wastes no effort on irrelevant considerations, takes no detours through misleading intermediate states, and avoids unnecessary backtracking.

This is not a metaphor. It is a variational principle applied to cognitive trajectories.


## 4.2 The Bond Geodesic Formulation

[Definition/Modeling choice]

We formalize this following Bond (2026a, Ch. 6). Consider a reasoning task specified by:

- An initial state $x_0 \in M$ (the problem representation)
- A goal region $G \subset M$ (the set of acceptable solutions)
- A cost metric $g$ on $M$ (encoding the difficulty of transitions)

**Definition 4.1** (Optimal reasoning trajectory). A trajectory $\gamma: [0,1] \to M$ with $\gamma(0) = x_0$ and $\gamma(1) \in G$ is *optimal* if it minimizes $\mathcal{L}[\gamma]$ among all paths from $x_0$ to $G$.

**Definition 4.2** (Geodesic deviation). For a given trajectory $\gamma$ and the geodesic $\gamma^*$ connecting the same endpoints:

$$\Delta(\gamma, \gamma^*) = \mathcal{L}[\gamma] - \mathcal{L}[\gamma^*]$$

This is always non-negative, equaling zero iff $\gamma$ is geodesic. Geodesic deviation is our primary measure of reasoning quality---not "did the system reach the goal?" but "how efficiently did it navigate the reasoning space?"

This distinction matters for three reasons:

**First, it separates competence from luck.** A model reaching the correct answer by pattern-matching has high accuracy but large geodesic deviation. A model following a near-geodesic path but making a small terminal error has low accuracy but high reasoning quality.

**Second, it is sensitive to process, not just outcome.** Two correct-answer models may have very different deviations---one reasoned efficiently, the other took a circuitous path. This captures the difference between understanding and brute-force search.

**Third, it connects to robustness.** A model following near-geodesic trajectories is robust to small perturbations (by continuity of geodesics with respect to initial conditions). A model taking chaotic, non-geodesic paths has no such guarantee.

**Proposition 4.1.** In flat reasoning space (zero curvature), the geodesic is the straight-line path, and any deviation is wasted computation. In curved reasoning space, the geodesic follows the curvature---what appears to be a "detour" in an embedding space may be the shortest path on the manifold.

This has a direct implication for chain-of-thought: a chain that seems circuitous may actually follow a geodesic on the curved manifold. The "detour" is only apparent in the wrong coordinate system.


## 4.3 Signatures of Geodesic Reasoning

What does geodesic reasoning look like empirically?

**Efficient token use.** Each token is necessary. The trajectory traces the shortest path through the manifold of partial solutions.

**Monotonic progress.** Distance to the goal decreases monotonically (in the Riemannian sense). No backtracking, no circling, no stalling.

**Curvature-adapted steps.** In regions of high curvature (complex reasoning landscape), smaller, more careful steps. In flat regions (straightforward inference), larger steps. This matches the observation that good reasoners slow down on hard sub-problems and speed through easy ones.

**Invariance under reparameterization.** The geodesic is coordinate-independent. Genuinely good reasoning should be invariant to irrelevant reformulations---the gauge invariance theme of Chapter 8.

### 4.3.1 Worked Example: Geodesic on a 2D Reasoning Surface

To make the framework tangible, we trace a worked example on a simple 2-dimensional manifold. Consider coordinates $(x, y)$ with metric:

$$ds^2 = dx^2 + e^{2x} \, dy^2$$

This is a surface of non-constant curvature. The component $g_{22} = e^{2x}$ means lateral movement (in $y$) is cheap when $x$ is negative and expensive when $x$ is positive. Think of $x$ as reasoning depth and $y$ as breadth---exploring alternatives. The metric encodes the empirical observation that deep reasoning makes breadth-first exploration increasingly costly: once you are far along one argument, switching to another becomes expensive.

**Step 1: Christoffel symbols.** Non-zero components: $g_{11} = 1$, $g_{22} = e^{2x}$, $g_{12} = 0$. The only non-trivial derivative is $\partial g_{22}/\partial x = 2e^{2x}$. Computing:

$$\Gamma^1_{22} = -e^{2x}, \qquad \Gamma^2_{12} = \Gamma^2_{21} = 1$$

All others are zero.

**Step 2: Geodesic equations.**

$$\ddot{x} - e^{2x} \dot{y}^2 = 0 \qquad \ddot{y} + 2\dot{x}\dot{y} = 0$$

The second equation simplifies: $\frac{d}{dt}(e^{2x} \dot{y}) = 0$, giving the conserved quantity $e^{2x} \dot{y} = C$---the "angular momentum" of the reasoning trajectory, arising from the metric's $y$-translation symmetry via Noether's theorem.

**Step 3: Boundary value problem.** Start at $(0, 0)$, goal at $(0, 1)$. Using the conservation law and constant-energy constraint $\dot{x}^2 + e^{2x}\dot{y}^2 = E$, we get $\dot{x}^2 = E - C^2 e^{-2x}$. The trajectory must dip into negative $x$ (where $y$-movement is cheap). By symmetry, the geodesic is symmetric about its midpoint, reaching a minimum $x_{\min} = \frac{1}{2}\ln(C^2/E)$ at $t = 1/2$.

The geodesic looks like a bow: it curves into the region of negative $x$ to traverse the $y$-distance efficiently, then curves back.

**Step 4: Cost comparison.** The naive straight-line path $x(t) = 0$, $y(t) = t$ costs $\mathcal{L}_{\mathrm{naive}} = 1$. Numerical integration gives $\mathcal{L}_{\mathrm{geodesic}} \approx 0.83$. Geodesic deviation: $\Delta \approx 0.17$.

The naive strategy---maintaining the same reasoning depth while shifting approach---wastes roughly 17% more effort than the optimal strategy of abstracting first, switching, and re-specializing.

**Step 5: Interpretation.** This toy example captures a real phenomenon in reasoning. When a model needs to shift from one line of argument to another (traversing $y$ at fixed depth $x$), the efficient strategy is not to force the transition at the current level of detail. Instead, the geodesic says: abstract upward (decrease $x$), make the conceptual shift where it is cheap, then descend back into detail.

Experienced human reasoners do this instinctively---they "zoom out" before switching gears. A lawyer shifting from one legal theory to another does not rewrite the argument clause by clause; she returns to the level of general principle, identifies the alternative theory, and then descends into the new case law. A mathematician who realizes her proof strategy is failing does not modify individual equations; she returns to the level of overall approach, identifies a new strategy, and then re-derives the details. The geodesic equation makes this widely recognized intuition mathematically precise and quantifies the cost savings: in our example, the naive strategy wastes 17% more effort than the geodesic strategy. The exact savings depend on the metric, but the qualitative lesson is general---the geodesic through a non-uniformly curved space is not a straight line.


## 4.4 When It Doesn't: Shortcuts, Detours, Loops, and Dead Ends

Most actual reasoning trajectories are not geodesics. The deviations constitute a taxonomy of failures:

**Shortcuts** bypass necessary intermediate states. The model jumps across the manifold rather than following its surface---pattern matching without understanding. In LLMs, this manifests as jumping from problem to answer by recognizing surface patterns without traversing the reasoning manifold's geometry.

[Empirical result]

The sycophancy data from the Learning benchmark illustrates this. When Gemini 2.5 Flash flips its answer 56% of the time in response to wrong corrections (compared to Claude's 0%), it takes a shortcut: instead of navigating from "current belief" through "evaluate correction" to "updated belief," it goes directly from "current belief" to "agree with user"---exiting the reasoning manifold entirely and landing in the approval manifold.

**Detours** pass through unnecessary intermediate states. The model explores blind alleys, considers irrelevant information, or provides hedging qualifications adding length without progress. On the manifold, a detour is a path with non-zero geodesic deviation that eventually reaches the goal but at greater cost than necessary.

**Loops** revisit the same region of reasoning space. The model circles back to previously visited states, wasting cost without progress. Loops are particularly insidious because the model may not recognize it is revisiting states.

**Dead ends** terminate at states from which no transition to the goal region exists. On the manifold, a dead end is a point where the gradient of the heuristic field vanishes and no escape direction exists---a zero of $\nabla h$ that is not in the goal region. The model gets stuck, typically producing repetitive or incoherent output. Dead ends are the manifold-level explanation for the "degenerate loops" observed in long-form generation, where the model repeats phrases or ideas without making progress.


## 4.5 Connection to Chain-of-Thought

Chain-of-thought (CoT) prompting externalizes the reasoning trajectory. Without CoT, the model traverses the manifold internally and outputs only the endpoint. With CoT, it outputs samples $\gamma(t_1), \gamma(t_2), \ldots, \gamma(t_n)$.

**CoT as geodesic approximation.** The best chain-of-thought traces a path close to the geodesic. Each step makes genuine progress. Intermediate states lie on or near the manifold of correct partial solutions. Total chain "length" (counting substantive reasoning steps, not tokens) approximates geodesic distance.

**CoT failures as geodesic deviations.** Verbose-but-empty CoT: long chain, large deviation, little net progress. Circular CoT: the chain contains loops---revisiting reasoning states. Hallucinated CoT: the chain leaves the reasoning manifold entirely.

The Executive Functions benchmark (E1: framework switching) provides evidence for this connection. All five models showed switch rates of 32--47% when asked to re-analyze scenarios under different ethical frameworks, with marker specificity of 89--93% confirming genuine framework reasoning rather than surface relabeling. But the *efficiency* of switching---how directly the model transitions from one framework's analysis to another's---varied substantially across models. This efficiency is a proxy for geodesic deviation in the space of ethical frameworks.

Consider what efficient framework switching looks like in geodesic terms. The model begins at a point on the reasoning manifold corresponding to, say, a utilitarian analysis of a scenario. The goal is a point corresponding to a deontological analysis of the same scenario. The geodesic between these points passes through the abstract space of ethical reasoning, and its length reflects the genuine intellectual work of reconceptualizing the scenario. A model that switches efficiently follows this geodesic---it abstracts from the specific utilitarian analysis, identifies the relevant deontological principles, and re-descends into a concrete deontological analysis. A model that switches inefficiently takes detours---perhaps repeating the scenario description, hedging about the validity of both frameworks, or simply relabeling utilitarian conclusions in deontological language without genuine reconceptualization.

### Symmetry Augmentation and Geodesic Straightening

[Speculation/Extension]

The Nemotron geometric training pipeline (Bond, 2026a, Ch. 13) exploits this connection. By augmenting training data with symmetry-transformed examples, it reshapes the reasoning manifold's local geometry to make geodesics easier to follow. The pipeline identifies six symmetry groups, each corresponding to a class of problems with specific invariance structure:

1. **$S_8 \times Z_2$** (bit manipulation): permuting bit positions and flipping bits. Collapses a high-dimensional space into the quotient $M / (S_8 \times Z_2)$.
2. **$S_{26}$** (substitution ciphers): permuting the alphabet. Teaches frequency analysis independent of letter assignments.
3. **$\mathbb{R}^+$** (scale invariance in physics): multiplying dimensionful quantities by a common scale. The geodesic for "a ball dropped from 10m" is isometric to "a ball dropped from 10km."
4. **$S_n$** (combinatorial symmetry): permuting interchangeable object labels. Only relational structure matters.
5. **Identity** (no symmetry): the problem structure is rigid. No augmentation applied.
6. **$D_8$** (dihedral symmetry): the eight symmetries of the square for grid-based spatial reasoning.

The mechanism is not merely "more data." When the training set contains only one representative of each symmetry orbit, the model learns a manifold with unnecessary curvature from arbitrary representative choices. After augmentation, the manifold can "unfold": irrelevant curvature is eliminated. Formally, the unaugmented model learns a (twisted) fiber bundle over $X/G$; the augmented model learns the quotient directly, with lower sectional curvature because the fibers---directions corresponding to irrelevant label permutations---have been collapsed.

In practice: 1.5--2.5x data expansion, far less than generic augmentation. The geometric insight: symmetry-principled augmentation is *targeted*, adding exactly the examples needed to flatten irrelevant curvature.


## 4.6 The SPD Manifold: Concrete Geodesic Computation

The SPD manifold from the BirdCLEF pipeline (Bond, 2026a) provides a concrete instance. On $\mathrm{SPD}(n)$ with the affine-invariant metric:

$$d_{\mathrm{AI}}(\Sigma_1, \Sigma_2) = \left\| \log\left(\Sigma_1^{-1/2} \Sigma_2 \Sigma_1^{-1/2}\right) \right\|_F$$

The log-Euclidean approximation $d_{\mathrm{LE}} = \|\log(\Sigma_1) - \log(\Sigma_2)\|_F$ maps SPD matrices to a flat space where Euclidean distance approximates geodesic distance. The 136-dimensional features (upper triangle of the matrix logarithm) are tangent-space coordinates.

The full BirdCLEF pipeline constructs a 156-dimensional geometric feature vector in four stages:

1. **SPD covariance features (136 dimensions)**: the upper triangle of $\log(\Sigma)$ for a 16$\times$16 covariance matrix.
2. **Trajectory features (4 dimensions)**: path length, geodesic distance, deviation, and number of steps from the sliding-window spectral trajectory on $\mathrm{SPD}(16)$.
3. **Topological data analysis features (16 dimensions)**: persistent homology statistics for $H_0$ (clustering structure---multiple syllables vs. sustained tone) and $H_1$ (loops---oscillating trills vs. monotone calls).
4. **Assembly (156 total)**: concatenation capturing metric, dynamic, and topological information simultaneously.

The reasoning analogy extends to all three levels: (1) the state of reasoning at a moment, (2) the efficiency of the reasoning path, and (3) the topological structure of the trajectory---does it loop, branch, or proceed linearly?


## 4.7 Information Geometry and the Statistical Manifold

[Theorem (conditional)]

The geodesic framework connects deeply to **information geometry**---the geometric structure of probability distributions. The **Fisher information matrix** at a parameter $\theta$ is:

$$F_{ij}(\theta) = \mathbb{E}_{x \sim p(\cdot \mid \theta)}\left[\frac{\partial \log p(x \mid \theta)}{\partial \theta^i} \frac{\partial \log p(x \mid \theta)}{\partial \theta^j}\right]$$

Chentsov's theorem (1972) proves this is the *unique* Riemannian metric (up to scale) invariant under sufficient statistics---the only metric respecting the intrinsic structure of statistical inference. Any other metric would change answers depending on parameterization, violating the reparameterization invariance we identified as a signature of geodesic reasoning.

For Gaussians $\mathcal{N}(\mu, \sigma^2)$, the Fisher metric yields $ds^2 = d\mu^2/\sigma^2 + 2 \, d\sigma^2/\sigma^2$---the Poincare half-plane, a model of hyperbolic geometry. Changing the mean of a narrow distribution is "expensive" (nearly non-overlapping); changing it for a broad distribution is "cheap." The metric captures this through $1/\sigma^2$.

**Geodesics as optimal belief updates.** A reasoning process updating beliefs from prior $p(\cdot \mid \theta_0)$ to posterior $p(\cdot \mid \theta_1)$ traces a path on the statistical manifold. The geodesic from $\theta_0$ to $\theta_1$ is the most efficient update---wasting no statistical effort. Geodesic deviation measures departure from ideal Bayesian reasoning.

**The natural gradient** (Amari, 1998) replaces the ordinary gradient with $\tilde{\nabla} L = F^{-1} \nabla L$---steepest descent *on the statistical manifold*. A natural gradient step is an infinitesimal geodesic step: it moves in the direction maximally decreasing the loss per unit of *statistical distance*, not Euclidean distance. The success of Adam, KFAC, and other approximate natural gradient methods can be understood as partial corrections toward geodesic behavior.

**For reasoning in LLMs specifically**, the information-geometric perspective offers a compelling interpretation of the attention mechanism. Each attention head computes a re-weighting of value vectors---equivalently, a transformation of the probability distribution over the vocabulary. The sequence of attention layers traces a path through the space of distributions. If the model has learned an approximation to the Fisher metric (embedded in its learned parameters), then the attention mechanism implements an approximate natural gradient step at each layer, and the full forward pass traces an approximate geodesic on the statistical manifold of next-token distributions.

The deviation of this implicit trajectory from the true Fisher geodesic is, under this interpretation, a measure of the model's reasoning efficiency. A model with well-calibrated attention weights follows near-geodesic paths; a model with poorly calibrated weights wastes statistical effort on non-geodesic detours. Standard gradient descent in training follows a non-geodesic path through parameter space---distorted by the arbitrary Euclidean metric on $\mathbb{R}^n$, which has nothing to do with the statistical structure of the model. Natural gradient descent follows a near-geodesic path, adapting its step size and direction to the local curvature of the distribution family.


## 4.8 Computational Considerations

Computing exact geodesics on high-dimensional manifolds is intractable in general. But for reasoning evaluation, we need approximations and bounds, not exact solutions.

**Lower bounds from metric distances.** Geodesic distance between two points is always a lower bound on any path's length, bounding geodesic deviation of observed trajectories.

**Geodesic shooting.** Given a starting point and direction, numerical integration of the geodesic equation traces a geodesic forward. This is feasible for manifolds with known Christoffel symbols (like SPD manifolds) and provides reference trajectories against which actual reasoning paths can be compared.

**The A* connection revisited.** When the manifold is discretized (as a graph or mesh), the geodesic becomes the shortest path, and A* with a consistent heuristic finds it exactly. The entire machinery of Chapter 1 applies, now with a geometric interpretation: A* on a discretized manifold approximates the geodesic.

This means that the quality of an LLM's reasoning can be understood as the quality of its implicit A* search on a discretized reasoning manifold. The attention mechanism computes (an approximation to) the heuristic field. The forward pass traces (an approximation to) a path on the manifold. And the chain-of-thought externalizes (samples from) this path. The question that Part II addresses is: how close is this implicit path to the geodesic, and what specific geometric pathologies cause it to deviate?


## 4.9 Summary: The Geodesic Standard

Let us step back and survey what Part I has established.

**Chapter 1** showed that reasoning is search, in the precise mathematical sense of Newell and Simon's Problem Space Hypothesis. The quality of search depends on the quality of the heuristic. But the classical framework treats the search space as a graph, which is inadequate for real reasoning.

**Chapter 2** gave the search space geometric structure---a Riemannian manifold with metric, curvature, and boundaries. The manifold hypothesis for reasoning claims that coherent cognitive states form a low-dimensional submanifold of the high-dimensional activation space. The moral reasoning example demonstrated empirically that this manifold has non-trivial geometry: framing perturbations that should be isometries produce measurable displacements (8.9 sigma).

**Chapter 3** identified the heuristic field---a scalar function on the manifold---as the navigational signal guiding search. In neural networks, this field is implemented implicitly by the combined action of attention (guidance) and MLP layers (evaluation). Measurement reveals systematic overconfidence (9.3 sigma), corresponding to heuristic underestimation of cost-to-go, which causes premature convergence.

**Chapter 4** provided the normative standard: the geodesic, the shortest path from problem to solution on the reasoning manifold. Geodesic deviation---the excess cost of the actual trajectory over the geodesic---is our primary measure of reasoning quality. It is richer than accuracy, sensitive to process rather than just outcome, and connected to robustness through the continuity of geodesics with respect to initial conditions.

Together, these four ideas---reasoning as search, the manifold as terrain, the heuristic as compass, the geodesic as ideal path---form the geometric framework for reasoning.

In Part II, we will see that the major failure modes---heuristic corruption (Ch. 5), sycophancy (Ch. 6), local minima (Ch. 7), and gauge symmetry breaking (Ch. 8)---are all ways the actual trajectory deviates from the geodesic. Each failure mode is a specific geometric pathology that bends, traps, or redirects the reasoning path.

The geodesic deviation framework gives us a unified language for these diverse failures. They are not separate bugs to be patched individually. They are manifestations of the same underlying phenomenon: the system's implicit heuristic field failing to guide it along the shortest path through thought.

---

*Maya now had the complete framework. The manifold gave the space its shape. The heuristic field gave the search its compass. The geodesic gave the trajectory its standard. She could finally answer the reviewer's question---not just whether the models were reasoning, but* how well*, measured by the geometry of their paths through thought. The compass was warped, the paths were longer than they needed to be, and the deviations had a shape she could measure. She was ready for Part II: the pathologies.*

---

### End Notes for Chapter 4

1. **The geodesic equation** is standard Riemannian geometry. The derivation via Euler-Lagrange follows do Carmo (1992), Chapter 3. The variational equivalence between length minimization and energy minimization (under constant-speed parameterization) is Theorem 3.6 of Lee (2018).

2. **The Bond Geodesic Formulation** is introduced in Bond (2026a), *Geometric Methods in Computational Modeling*, Chapter 6. The key innovation: application to reasoning trajectories rather than physical paths.

3. **The 2D worked example** uses $ds^2 = dx^2 + e^{2x} dy^2$, a standard example with non-constant curvature. The conservation law $e^{2x}\dot{y} = C$ follows from Noether's theorem applied to $y$-translation invariance.

4. **Symmetry augmentation.** The six symmetry groups and the curvature-reduction mechanism are developed in the Nemotron geometric training pipeline (Bond, 2026a, Ch. 13). The fiber bundle interpretation is original to this book.

5. **Information geometry.** Fisher information metric uniqueness: Chentsov (1972). Comprehensive treatment: Amari and Nagaoka (2000), *Methods of Information Geometry*. Natural gradient: Amari (1998), "Natural Gradient Works Efficiently in Learning," *Neural Computation*, 10(2), 251--276.

6. **The SPD manifold pipeline.** Full details in Bond (2026a), Chapter 4.6. The 156-dimensional feature vector combines 136 log-Euclidean features, 4 trajectory statistics, and 16 persistent homology features. TDA: Carlsson (2009), "Topology and Data," *Bulletin of the AMS*.

7. **Sycophancy data.** The 56% flip rate (Gemini 2.5 Flash) and 0% rate (Claude) are from the L2 Error Correction benchmark in Bond (2026b).

---
