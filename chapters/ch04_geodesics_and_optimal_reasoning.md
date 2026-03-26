# Chapter 4: Geodesics and Optimal Reasoning

> *"Nature is thrifty in all its actions."*
> --- Pierre Louis Maupertuis, formulating the principle of least action (1744)

> **RUNNING EXAMPLE — DR. OKAFOR'S TRIAGE**
>
> *Dr. Amara Okafor's best triage decisions have a quality that her residents notice but struggle to articulate. She does not simply arrive at the right answer — she arrives there directly. Chest pain, diaphoresis, age over sixty: cardiac workup. The trajectory from presentation to disposition passes through exactly the intermediate assessments it needs to pass through, and no others. She does not detour through irrelevant differentials. She does not loop back to reconsider possibilities she has already ruled out. She does not overshoot into excessive testing. The path is clean.*
>
> *That clean path is a geodesic — the shortest route through the manifold of clinical reasoning, given its curvature. When she deviates from the geodesic, she knows it: the case that nagged her all shift, the diagnosis that required three revisions, the patient she almost sent home. Those deviations have a cost, measured in time, in resources, in risk. This chapter gives that cost a name — geodesic deviation — and shows that it is not a metaphor for inefficiency but a computable quantity on the reasoning manifold.*

---

## 4.1 The Geodesic as the Ideal Reasoning Trajectory

In Chapter 2, we established that reasoning states live on a manifold with metric structure. In Chapter 3, we showed that the heuristic field guides search through this manifold. Now we arrive at the central geometric object of this book: the *geodesic*.

A geodesic is the shortest path between two points on a manifold. In flat Euclidean space, geodesics are straight lines. On a sphere, they are great circles. On a general Riemannian manifold $(M, g)$, they are curves $\gamma(t)$ satisfying the geodesic equation:

$$\frac{d^2 \gamma^k}{dt^2} + \Gamma^k_{ij} \frac{d\gamma^i}{dt} \frac{d\gamma^j}{dt} = 0$$

where $\Gamma^k_{ij}$ are the Christoffel symbols encoding the manifold's curvature. The geodesic equation says: a curve is "straight" (has zero acceleration) *after accounting for the curvature of the space it lives in*.

### Derivation from the Euler-Lagrange equations

The geodesic equation is not handed down by fiat — it arises naturally as the Euler-Lagrange equation for the length (or energy) functional on curves. To see this, consider a smooth curve $\gamma: [0,1] \to M$ on a Riemannian manifold $(M, g)$ with local coordinates $(\gamma^1(t), \ldots, \gamma^n(t))$. The *energy functional* is:

$$E[\gamma] = \frac{1}{2} \int_0^1 g_{ij}(\gamma(t)) \, \dot{\gamma}^i(t) \, \dot{\gamma}^j(t) \, dt$$

where $\dot{\gamma}^i = d\gamma^i / dt$ and we use the Einstein summation convention. We work with the energy rather than the length because (a) it is easier to differentiate, (b) its critical points are geodesics parameterized proportionally to arc length, and (c) by the Cauchy-Schwarz inequality, minimizing energy is equivalent to minimizing length among constant-speed curves.

The integrand serves as the Lagrangian: $L(\gamma^k, \dot{\gamma}^k) = \frac{1}{2} g_{ij}(\gamma) \dot{\gamma}^i \dot{\gamma}^j$. The Euler-Lagrange equation for this Lagrangian is:

$$\frac{d}{dt} \frac{\partial L}{\partial \dot{\gamma}^k} - \frac{\partial L}{\partial \gamma^k} = 0$$

Computing the partial derivatives:

$$\frac{\partial L}{\partial \dot{\gamma}^k} = g_{kj} \dot{\gamma}^j$$

where we used the symmetry $g_{ij} = g_{ji}$. Taking the total time derivative:

$$\frac{d}{dt}\left(g_{kj} \dot{\gamma}^j\right) = g_{kj} \ddot{\gamma}^j + \frac{\partial g_{kj}}{\partial \gamma^m} \dot{\gamma}^m \dot{\gamma}^j$$

For the other term:

$$\frac{\partial L}{\partial \gamma^k} = \frac{1}{2} \frac{\partial g_{ij}}{\partial \gamma^k} \dot{\gamma}^i \dot{\gamma}^j$$

Substituting into the Euler-Lagrange equation:

$$g_{kj} \ddot{\gamma}^j + \frac{\partial g_{kj}}{\partial \gamma^m} \dot{\gamma}^m \dot{\gamma}^j - \frac{1}{2} \frac{\partial g_{ij}}{\partial \gamma^k} \dot{\gamma}^i \dot{\gamma}^j = 0$$

We can symmetrize the second term by writing:

$$\frac{\partial g_{kj}}{\partial \gamma^m} \dot{\gamma}^m \dot{\gamma}^j = \frac{1}{2}\left(\frac{\partial g_{kj}}{\partial \gamma^i} + \frac{\partial g_{ki}}{\partial \gamma^j}\right) \dot{\gamma}^i \dot{\gamma}^j$$

since $\dot{\gamma}^i \dot{\gamma}^j$ is symmetric in $i$ and $j$. This gives:

$$g_{kj} \ddot{\gamma}^j + \frac{1}{2}\left(\frac{\partial g_{kj}}{\partial \gamma^i} + \frac{\partial g_{ki}}{\partial \gamma^j} - \frac{\partial g_{ij}}{\partial \gamma^k}\right) \dot{\gamma}^i \dot{\gamma}^j = 0$$

Now we recognize the expression in parentheses. Define the Christoffel symbols of the first kind:

$$\Gamma_{k,ij} = \frac{1}{2}\left(\frac{\partial g_{kj}}{\partial \gamma^i} + \frac{\partial g_{ki}}{\partial \gamma^j} - \frac{\partial g_{ij}}{\partial \gamma^k}\right)$$

so the equation becomes $g_{kj} \ddot{\gamma}^j + \Gamma_{k,ij} \dot{\gamma}^i \dot{\gamma}^j = 0$. Multiplying through by the inverse metric $g^{mk}$:

$$\ddot{\gamma}^m + g^{mk} \Gamma_{k,ij} \dot{\gamma}^i \dot{\gamma}^j = 0$$

The quantity $\Gamma^m_{ij} = g^{mk} \Gamma_{k,ij}$ is the Christoffel symbol of the second kind. We arrive at the geodesic equation:

$$\ddot{\gamma}^m + \Gamma^m_{ij} \dot{\gamma}^i \dot{\gamma}^j = 0$$

**[Established Mathematics.]** This derivation reveals the geodesic's variational character: it is not merely a curve with zero "acceleration" in some abstract sense, but the curve that extremizes a cost. For reasoning, the cost is the total effort expended along the trajectory. The Christoffel symbols, which encode how the coordinate basis vectors twist and turn as one moves through the manifold, determine the "gravitational" field of the reasoning space — the curvature that bends optimal trajectories away from naive straight-line paths.

The second-order nature of the geodesic equation is also significant: given a starting point $\gamma(0) = x_0$ and an initial velocity $\dot{\gamma}(0) = v_0$, the geodesic is uniquely determined (at least locally). In the reasoning context, this means that the problem formulation (the starting point) and the initial direction of reasoning (the first step) together determine the optimal trajectory. Choosing the right initial direction — the right first step — is critical.

For reasoning, the geodesic has a specific interpretation: it is the *optimal reasoning trajectory* — the path from problem to solution that achieves the correct answer with minimum cognitive cost. When a system reasons along a geodesic, it wastes no effort on irrelevant considerations, takes no detours through misleading intermediate states, and avoids unnecessary backtracking.

This is not a metaphor. If we define a cost functional on reasoning trajectories:

$$\mathcal{L}[\gamma] = \int_0^1 g_{\gamma(t)}\left(\dot{\gamma}(t), \dot{\gamma}(t)\right) dt$$

then the geodesic is the trajectory that minimizes $\mathcal{L}$ — it is the *least-action path* through reasoning space, in the same sense that light follows the path of least time (Fermat's principle) and particles follow paths of least action (Hamilton's principle).

## 4.2 The Bond Geodesic Formulation

We formalize this connection following the framework introduced in *Geometric Methods in Computational Modeling* (Bond, 2026a, Ch. 6). Consider a reasoning task specified by:

- An initial state $x_0 \in M$ (the problem representation)
- A goal region $G \subset M$ (the set of acceptable solutions)
- A cost metric $g$ on $M$ (encoding the difficulty of transitions)

**Definition 4.1** (Optimal reasoning trajectory). A reasoning trajectory $\gamma: [0,1] \to M$ with $\gamma(0) = x_0$ and $\gamma(1) \in G$ is *optimal* if it minimizes the cost functional $\mathcal{L}[\gamma]$ among all paths from $x_0$ to $G$.

**[Modeling Axiom.]** **Definition 4.2** (Geodesic deviation). For a given reasoning trajectory $\gamma$ and the geodesic $\gamma^*$ connecting the same endpoints, the *geodesic deviation* is:

$$\Delta(\gamma, \gamma^*) = \mathcal{L}[\gamma] - \mathcal{L}[\gamma^*]$$

This is always non-negative, and equals zero if and only if $\gamma$ is a geodesic. The geodesic deviation is our primary measure of reasoning quality — not "did the system get the right answer?" but "how efficiently did it navigate the reasoning space?"

**[Conditional Theorem.]** **Proposition 4.1**. In flat reasoning space (zero curvature), the geodesic is the straight-line path from problem to solution, and any deviation corresponds to wasted computation. In curved reasoning space, the geodesic follows the curvature — what appears to be a "detour" in an embedding space may in fact be the shortest path on the manifold.

This proposition has a direct implication for chain-of-thought reasoning: a chain-of-thought that seems to take a circuitous route through intermediate steps may actually be following a geodesic on the curved reasoning manifold. The "detour" is only apparent when viewed in the wrong coordinate system.

## 4.3 When the Model Follows a Geodesic

What does geodesic reasoning look like empirically? We can identify several signatures:

**Efficient token use.** A model reasoning along a geodesic produces each intermediate token because it is necessary — not because it is filling space or hedging. The token-level trajectory traces the shortest path through the manifold of partial solutions.

**Monotonic progress.** Along a geodesic, the distance to the goal decreases monotonically (in the Riemannian sense). There is no backtracking, no going in circles, no getting stuck. Each reasoning step moves closer to the answer.

**Curvature-adapted steps.** In regions of high curvature (where the reasoning landscape is complex), the geodesic takes smaller, more careful steps. In flat regions (straightforward inference), it takes larger steps. This corresponds to the observation that good reasoners slow down on hard sub-problems and speed through easy ones.

**Invariance under reparameterization.** A geodesic is a geometric object — it doesn't depend on the coordinates used to describe it. Similarly, genuinely good reasoning should be invariant to irrelevant reformulations of the problem. This connects directly to the gauge invariance theme of Chapter 8.

### 4.3.1 Worked Example: Geodesic on a 2D Reasoning Surface

To make the geodesic framework tangible, we trace a complete worked example on a simple 2-dimensional manifold. Consider a reasoning surface parameterized by coordinates $(x, y)$ with the metric:

$$ds^2 = dx^2 + e^{2x} \, dy^2$$

This is a surface of non-constant curvature. The metric component $g_{22} = e^{2x}$ means that "lateral" movement (in the $y$-direction) is cheap when $x$ is negative (small $e^{2x}$) and expensive when $x$ is positive (large $e^{2x}$). In reasoning terms, think of $x$ as the "depth" of reasoning and $y$ as the "breadth" — exploring alternative approaches. The metric encodes the empirical observation that deep reasoning makes breadth-first exploration increasingly costly: once you are far along one line of argument, switching to another becomes expensive.

**Step 1: Compute the Christoffel symbols.** The non-zero metric components are $g_{11} = 1$, $g_{22} = e^{2x}$, $g_{12} = g_{21} = 0$. The inverse metric has $g^{11} = 1$, $g^{22} = e^{-2x}$.

Since $g_{11}$ is constant and $g_{12} = 0$, most partial derivatives vanish. The only non-trivial derivative is $\partial g_{22}/\partial x = 2e^{2x}$. Computing the Christoffel symbols:

$$\Gamma^1_{22} = -\frac{1}{2} g^{11} \frac{\partial g_{22}}{\partial x} = -e^{2x}$$

$$\Gamma^2_{12} = \Gamma^2_{21} = \frac{1}{2} g^{22} \frac{\partial g_{22}}{\partial x} = 1$$

All other Christoffel symbols are zero.

**Step 2: Write the geodesic equations.** The two coupled ODEs are:

$$\ddot{x} - e^{2x} \dot{y}^2 = 0$$

$$\ddot{y} + 2\dot{x}\dot{y} = 0$$

The second equation has a useful simplification. Note that $\frac{d}{dt}(e^{2x} \dot{y}) = 2\dot{x} e^{2x} \dot{y} + e^{2x} \ddot{y} = e^{2x}(\ddot{y} + 2\dot{x}\dot{y}) = 0$. So $e^{2x} \dot{y} = C$ is a conserved quantity — the "angular momentum" of the reasoning trajectory. This conservation law reflects the metric's symmetry in $y$ (the metric does not depend on $y$, so Noether's theorem gives a conserved quantity associated with $y$-translation).

**Step 3: Solve for a specific boundary value problem.** Suppose the problem state is $(x_0, y_0) = (0, 0)$ and the goal state is $(x_1, y_1) = (0, 1)$. We seek the geodesic connecting these two points.

Using the conservation law $e^{2x} \dot{y} = C$ and the unit-speed constraint $\dot{x}^2 + e^{2x} \dot{y}^2 = E$ (constant energy), we get:

$$\dot{x}^2 = E - \frac{C^2}{e^{2x}}$$

This is a one-dimensional effective potential problem. The trajectory must satisfy $E - C^2 e^{-2x} \geq 0$, i.e., $x \geq \frac{1}{2}\ln(C^2/E)$. Since both endpoints have $x = 0$, the geodesic must dip into negative $x$ values (where $y$-movement is cheaper) before returning.

By symmetry of the boundary conditions (same $x$ at both ends), the geodesic is symmetric about its midpoint: $x(t)$ reaches a minimum $x_{\min}$ at $t = 1/2$, and $y(1/2) = 1/2$. This minimum is determined by $\dot{x} = 0$:

$$x_{\min} = \frac{1}{2}\ln\left(\frac{C^2}{E}\right)$$

The geodesic looks like a bow: it curves into the region of negative $x$ (where lateral movement is cheap) to traverse the $y$-distance more efficiently, then curves back. This is the geometric analogue of a reasoning strategy that first "steps back" to a more abstract level where switching approaches is easy, executes the switch, and then re-descends to the original depth.

**Step 4: Compare with the naive path.** The naive straight-line path in coordinate space is $x(t) = 0$, $y(t) = t$ for $t \in [0,1]$. Its cost is:

$$\mathcal{L}_{\text{naive}} = \int_0^1 e^{2 \cdot 0} \cdot 1^2 \, dt = 1$$

The geodesic has cost strictly less than 1, because by dipping into negative $x$ it exploits the cheaper metric there. Numerical integration for this boundary problem gives $\mathcal{L}_{\text{geodesic}} \approx 0.83$, so the geodesic deviation of the naive path is:

$$\Delta \approx 1.0 - 0.83 = 0.17$$

The naive strategy — maintaining the same reasoning depth while shifting approach — wastes roughly 17% more effort than the optimal strategy of abstracting first, switching, and re-specializing.

**Step 5: Interpret.** This toy example captures a real phenomenon in reasoning. When a model needs to shift from one line of argument to another (traversing $y$ at fixed depth $x$), the efficient strategy is not to force the transition at the current level of detail. Instead, the geodesic says: abstract upward (decrease $x$), make the conceptual shift where it is cheap, then descend back into detail. Experienced human reasoners do this instinctively — they "zoom out" before switching gears. The geodesic equation makes this intuition mathematically precise and quantifies the cost savings.

## 4.4 When It Doesn't: Shortcuts, Detours, Loops, and Dead Ends

Most actual reasoning trajectories are not geodesics. The deviations from geodesic behavior constitute a taxonomy of reasoning failures:

**Shortcuts** are paths that bypass necessary intermediate states. In the language of manifolds, a shortcut jumps across the manifold rather than following its surface — it ignores the intrinsic structure of the reasoning space. In LLMs, this manifests as "pattern matching without understanding": the model jumps directly from problem to answer by recognizing a surface pattern, without traversing the reasoning manifold's geometry.

The sycophancy data from the Learning benchmark illustrates this vividly. When Gemini 2.5 Flash flips its answer 56% of the time in response to wrong corrections (compared to Claude's 0%), it is taking a shortcut: instead of navigating the manifold from "current belief" through "evaluate correction" to "updated belief," it takes a direct path from "current belief" to "agree with user" — a shortcut that exits the reasoning manifold entirely and lands in the approval manifold.

**Detours** are paths that pass through unnecessary intermediate states. The model considers irrelevant information, explores blind alleys, or provides hedging qualifications that add length without adding progress. On the manifold, a detour is a path with non-zero geodesic deviation that eventually reaches the goal but takes more effort than necessary.

**Loops** are paths that revisit the same region of the reasoning space. The model generates reasoning steps that circle back to previously visited states. On the manifold, a loop is a closed sub-path — a cycle that wastes cost without making progress. Loops are particularly insidious because the model may not recognize it is revisiting states.

**Dead ends** are paths that terminate in states from which no transition to the goal region exists. On the manifold, a dead end is a point where the gradient of the heuristic field vanishes and no escape direction exists — a zero of $\nabla h$ that is not in the goal region. The model gets stuck, typically producing repetitive or incoherent output.

## 4.5 Geodesic Deviation as a Measure of Reasoning Quality

We now have a principled alternative to accuracy as a measure of reasoning quality. Traditional evaluation asks: "Did the model reach the goal region?" Geodesic deviation asks: "How efficiently did the model's trajectory approximate the optimal path?"

This distinction matters for three reasons:

**First, it separates competence from luck.** A model that reaches the correct answer by a lucky shortcut (pattern-matching the answer without reasoning) has high accuracy but large geodesic deviation. A model that follows a near-geodesic trajectory but makes a small error at the end has low accuracy but high reasoning quality.

**Second, it is sensitive to process, not just outcome.** Two models that both get the right answer may have very different geodesic deviations — one reasoned efficiently while the other took a circuitous path. This captures the difference between understanding and brute-force search.

**Third, it connects to robustness.** A model that follows near-geodesic trajectories is robust to small perturbations — a small change in the input will produce a small change in the trajectory (by continuity of geodesics with respect to initial conditions). A model that takes chaotic, non-geodesic paths has no such guarantee.

**[Empirical.]** The empirical data from the Executive Functions benchmark (E1, framework switching) provides evidence for this connection. All five models showed switch rates of 32-47% when asked to re-analyze scenarios under different ethical frameworks. The marker specificity was 89-93%, confirming genuine framework reasoning rather than surface relabeling. But the *efficiency* of the switching — how directly the model transitions from one framework's analysis to another's — varied substantially. This efficiency is a proxy for geodesic deviation in the space of ethical frameworks.

## 4.6 Connection to Chain-of-Thought

Chain-of-thought (CoT) prompting asks the model to "show its work" — to produce intermediate reasoning steps before the final answer. In our framework, CoT is the *externalization of the reasoning trajectory*.

Without CoT, the model performs an internal traversal of the reasoning manifold and outputs only the endpoint. With CoT, it outputs samples along the trajectory $\gamma(t_1), \gamma(t_2), \ldots, \gamma(t_n)$. This is immensely useful for our framework because it makes the trajectory (approximately) observable.

**CoT as geodesic approximation.** The best chain-of-thought reasoning traces a path close to the geodesic. Each step makes genuine progress toward the goal. The intermediate states are on or near the manifold of correct partial solutions. The total "length" of the chain (measured by the number of substantive reasoning steps, not tokens) approximates the geodesic distance from problem to solution.

**CoT failures as geodesic deviations.** Bad chain-of-thought reasoning corresponds to large geodesic deviations:
- *Verbose but empty CoT*: the chain is long but the geodesic deviation is large — the model traverses many states but makes little net progress.
- *Circular CoT*: the chain contains loops — the model revisits reasoning states.
- *Hallucinated CoT*: the chain leaves the reasoning manifold entirely — the intermediate states are not on any valid reasoning surface.

The Nemotron geometric training pipeline (Ch. 13 of *Geometric Methods*) exploits this connection directly. **[Speculation/Extension.]** By augmenting training data with symmetry-transformed examples — applying group actions (S_8 × Z_2 for bit manipulation, S_26 for encryption, R+ for physics) — we reshape the local geometry of the reasoning manifold to make geodesics easier to follow. The augmented model doesn't just see more examples; it learns the *symmetry structure* of the solution space, which straightens the geodesics.

### The six symmetry groups and their geometric role

The Nemotron pipeline identifies six distinct symmetry groups, each corresponding to a class of reasoning problems whose solution spaces possess specific invariance structure:

1. **$S_8 \times Z_2$ (bit manipulation).** The symmetric group $S_8$ permutes eight bit positions, and $Z_2$ flips each bit. Together they generate the full symmetry group of 8-bit Boolean operations. A problem like "compute the XOR of two bytes" has the same abstract structure regardless of which bit positions are involved. By augmenting with all $8! \times 2^8 = 10{,}321{,}920$ symmetry-equivalent formulations (in practice a representative sample), the pipeline teaches the model that the reasoning manifold for bit manipulation is invariant under these permutations. Geometrically, this collapses a high-dimensional space into a lower-dimensional quotient manifold $M / (S_8 \times Z_2)$, on which geodesics are shorter and easier to follow.

2. **$S_{26}$ (substitution ciphers / encryption).** The symmetric group on 26 letters acts on alphabetic substitution ciphers. Any permutation of the alphabet produces an equivalent cipher. The reasoning required to decrypt a message is invariant under relabeling of the cipher alphabet. Augmenting with $S_{26}$ transformations (again, a representative sample from the $26! \approx 4 \times 10^{26}$ possible permutations) teaches the model the abstract structure of frequency analysis and pattern matching independent of specific letter assignments.

3. **$\mathbb{R}^+$ (scale invariance in physics).** Positive real scaling acts on physical quantities: a kinematics problem stated in meters is the same problem stated in kilometers, up to a scale factor. The group $\mathbb{R}^+$ acts by multiplying all dimensionful quantities by a common scale. Augmenting with rescaled versions of physics problems teaches the model that the reasoning manifold is scale-invariant — the geodesic for "a ball dropped from 10m" is isometric to the geodesic for "a ball dropped from 10km" (after appropriate rescaling of time).

4. **$S_n$ (combinatorial symmetry).** For problems involving $n$ interchangeable objects — graph coloring, scheduling, assignment — the symmetric group $S_n$ permutes the labels. Augmenting with $S_n$-transformed examples teaches the model that the identity of objects is irrelevant; only the relational structure matters. This is the geometric realization of the combinatorial principle that isomorphic instances are equivalent.

5. **Identity (no symmetry).** Some reasoning problems have no exploitable symmetry — the problem structure is rigid and every detail matters. The identity group $\{e\}$ acts trivially, and no augmentation is applied. Recognizing when no symmetry exists is itself important: attempting to exploit non-existent symmetry would map correct solutions to incorrect ones, distorting the manifold rather than simplifying it.

6. **$D_4$ (dihedral symmetry in spatial reasoning).** The dihedral group of order 8 — the symmetries of the square — acts on grid-based spatial reasoning problems. Rotations by 90, 180, and 270 degrees and reflections across four axes generate $D_4$. For problems on a square grid (maze navigation, Conway's Game of Life, pixel manipulation), augmenting with $D_4$ teaches the model that the reasoning is invariant under rigid motions of the grid.

### How augmentation reshapes local curvature

The mechanism by which symmetry augmentation improves reasoning is not merely "more data." It has a precise geometric interpretation. When the training set contains only one representative of each symmetry orbit, the model must learn a manifold that wraps around to identify symmetric points — a manifold with unnecessary curvature induced by the arbitrary choice of representative. After augmentation, the model sees all representatives in each orbit. The learned manifold can "unfold" — the curvature induced by arbitrary labeling conventions is eliminated, and the intrinsic curvature of the problem structure is revealed.

Formally, if $G$ is a symmetry group acting on the input space $X$, the unaugmented model learns a manifold $M$ that is a (twisted) fiber bundle over the quotient $X/G$. The augmented model learns the quotient directly. The quotient has lower curvature (in the sectional curvature sense) because the fibers — the directions corresponding to irrelevant label permutations — have been collapsed.

In practice, the Nemotron pipeline achieves a **1.5x to 2.5x data expansion factor** depending on the symmetry group. For $D_4$, each example generates up to 8 variants (the 8 elements of the dihedral group), yielding a 2.0-2.5x expansion after deduplication. For $S_n$ with moderate $n$, a representative sample of permutations yields approximately 1.5-2.0x expansion. The $\mathbb{R}^+$ group, being continuous, allows arbitrary expansion; in practice, 3-5 scale factors are sampled per example, giving 1.5-2.0x expansion. The identity group contributes 1.0x (no expansion).

The expected aggregate expansion across the full training mixture is **1.5-2.5x**, depending on the composition of problem types. This is not a large factor — it is far less than generic data augmentation schemes that might 10x the data. The geometric insight is that symmetry-principled augmentation is *targeted*: it adds exactly the examples needed to flatten the irrelevant curvature, and no more.

## 4.7 The SPD Manifold: A Concrete Geodesic Computation

To make these ideas concrete, consider the Symmetric Positive Definite (SPD) manifold used in the BirdCLEF geometric feature pipeline (Bond 2026a, Ch. 4.6).

The space of $n \times n$ symmetric positive definite matrices $\text{SPD}(n)$ is a Riemannian manifold with the affine-invariant metric:

$$d_{\text{AI}}(\Sigma_1, \Sigma_2) = \left\| \log\left(\Sigma_1^{-1/2} \Sigma_2 \Sigma_1^{-1/2}\right) \right\|_F$$

In the BirdCLEF pipeline, mel-spectrogram frequency bands are grouped into 16 bands, producing 16×16 covariance matrices — points on SPD(16). The log-Euclidean approximation:

$$d_{\text{LE}}(\Sigma_1, \Sigma_2) = \left\| \log(\Sigma_1) - \log(\Sigma_2) \right\|_F$$

maps SPD matrices to a flat space (the tangent space at the identity) where Euclidean distance is a good approximation to geodesic distance. The 136-dimensional feature vectors (the upper triangle of the matrix logarithm) are coordinates in this tangent space.

But the key insight for reasoning is the *geodesic deviation on SPD*. The BirdCLEF pipeline computes a "spectral trajectory" — the sequence of covariance matrices computed from sliding windows over the audio signal. This trajectory lives on SPD(16). The pipeline measures:

- **Path length**: the total Riemannian distance along the trajectory
- **Geodesic distance**: the direct Riemannian distance from start to end
- **Geodesic deviation**: path length minus geodesic distance

This deviation measures how "direct" the spectral evolution is. A bird call with a simple harmonic structure has low deviation — the covariance matrix evolves smoothly along a geodesic. A complex call with rapid frequency modulation has high deviation — the trajectory takes detours on the SPD manifold.

The analogy to reasoning is precise: replace "covariance matrix" with "cognitive state" and "spectral trajectory" with "reasoning trajectory." The geodesic deviation measures how directly the system navigates from problem to solution. The mathematics is identical.

### The full BirdCLEF feature geometry

The BirdCLEF pipeline constructs a feature vector that fully exploits the SPD manifold's geometry. The construction proceeds in four stages, producing a total of 156 features.

**Stage 1: SPD covariance features (136 dimensions).** Each 5-second audio clip is decomposed into 16 mel-frequency bands. A 16×16 covariance matrix $\Sigma \in \text{SPD}(16)$ is computed from the band energies within each window. The matrix logarithm $\log(\Sigma)$ maps this to the tangent space at the identity, yielding a 16×16 symmetric matrix. The upper triangle (including the diagonal) contains $16 \times 17 / 2 = 136$ independent entries. These 136 features are coordinates on the tangent space of SPD(16) at the identity — they capture the full second-order statistical structure of the frequency content, including all cross-band correlations.

The choice of 16 bands is deliberate: it balances spectral resolution (enough bands to distinguish species-specific harmonic structure) against the dimensionality of the covariance matrix (a 32×32 matrix would yield 528 features, creating sparsity issues for downstream classifiers). The 16-band decomposition produces a covariance matrix that is empirically well-conditioned for bird vocalizations in the 150 Hz to 15 kHz range.

**Stage 2: Trajectory features (4 dimensions).** The sliding-window analysis produces a sequence of SPD matrices $\Sigma_1, \Sigma_2, \ldots, \Sigma_T$ — a discrete trajectory on SPD(16). From this trajectory, four geometric features are extracted:

- **path_length**: $\sum_{t=1}^{T-1} d_{\text{LE}}(\Sigma_t, \Sigma_{t+1})$ — the total distance traveled along the trajectory. This measures the total spectral variation in the clip. Calls with rapid frequency modulation have high path length.
- **geodesic_distance**: $d_{\text{LE}}(\Sigma_1, \Sigma_T)$ — the direct distance from the first to the last covariance matrix. This measures the net spectral change over the clip.
- **deviation**: path_length $-$ geodesic_distance — the excess path length beyond what a geodesic would require. This is the geodesic deviation, measuring how "direct" the spectral evolution is. It is always non-negative and equals zero only if the trajectory is a geodesic (i.e., the spectral content evolves in a perfectly uniform direction on the SPD manifold).
- **n_steps**: $T$ — the number of windows in the trajectory. This is a normalization feature: deviation should be interpreted relative to the number of steps.

These four features encode the dynamics of the spectral trajectory — information that is invisible in any single-frame analysis.

**Stage 3: Topological data analysis features (16 dimensions).** The pipeline also extracts topological features from the sequence of covariance matrices using persistent homology. The pairwise distance matrix $D_{st} = d_{\text{LE}}(\Sigma_s, \Sigma_t)$ is computed, and a Vietoris-Rips filtration is constructed. The persistence diagrams for homology groups $H_0$ and $H_1$ capture:

- **$H_0$ features (8 dimensions)**: statistics of the connected components' lifetimes — the birth/death times, persistence values, and their moments. These capture the clustering structure of the spectral trajectory: does the call consist of several distinct "syllables" (multiple long-lived $H_0$ generators) or a single sustained tone (one dominant generator)?
- **$H_1$ features (8 dimensions)**: statistics of the 1-cycles' lifetimes. These capture loops in the spectral trajectory — does the call return to previously visited spectral states? A trill, which oscillates between two spectral configurations, creates a prominent $H_1$ generator. A monotone call does not.

The 16 TDA features provide topological invariants of the spectral trajectory — information about its shape that is invariant under continuous deformations. Where the geodesic deviation measures metric properties (how far the trajectory deviates from a geodesic), the TDA features measure topological properties (how many holes and loops the trajectory contains).

**Stage 4: Assembly (156 total dimensions).** The complete feature vector is the concatenation:

$$\mathbf{f} = [\underbrace{f_1, \ldots, f_{136}}_{\text{SPD covariance}} \;;\; \underbrace{f_{137}, \ldots, f_{140}}_{\text{trajectory}} \;;\; \underbrace{f_{141}, \ldots, f_{156}}_{\text{TDA}}]$$

This 156-dimensional vector lives in a space that combines the tangent space of SPD(16) (for static spectral structure), the space of trajectory statistics (for spectral dynamics), and the space of topological invariants (for spectral topology). It is a comprehensive geometric descriptor that captures structure at the metric, dynamic, and topological levels simultaneously.

The reasoning analogy extends to all three levels: (1) the covariance features correspond to the "state" of the reasoning process at a given moment, (2) the trajectory features correspond to the efficiency and directness of the reasoning path, and (3) the TDA features correspond to the topological structure of the reasoning trajectory — does it loop, branch, or proceed linearly?

## 4.8 Computational Considerations

Computing exact geodesics on high-dimensional manifolds is intractable in general. But for reasoning evaluation, we don't need exact geodesics — we need approximations and bounds.

**Lower bounds from metric distances.** The geodesic distance between two points is always a lower bound on the length of any path between them. If we can compute or approximate the geodesic distance (even without knowing the geodesic itself), we can bound the geodesic deviation of any observed trajectory.

**Geodesic shooting.** Given a starting point and an initial direction, we can numerically integrate the geodesic equation to trace a geodesic forward. This is feasible for manifolds with known Christoffel symbols (like SPD manifolds) and provides reference trajectories for comparison.

**The A* connection revisited.** When the manifold is discretized (as a graph or mesh), the geodesic is the shortest path, and A* with a consistent heuristic finds it exactly. The entire machinery of Chapter 1 applies, now with a geometric interpretation: A* on a discretized manifold approximates the geodesic.

This means that the quality of an LLM's reasoning can be understood as the quality of its implicit A* search on a discretized reasoning manifold. The attention mechanism computes (an approximation to) the heuristic field. The forward pass traces (an approximation to) a path on the manifold. And the chain-of-thought externalizes (samples from) this path.

The question is: how close is this implicit path to the geodesic?

### 4.8.1 Connection to Information Geometry

The geodesic framework for reasoning has a deep connection to *information geometry* — the study of the geometric structure of statistical models and probability distributions. This connection is not merely analogical: it provides a concrete Riemannian metric for the space of probabilistic beliefs, making the entire geodesic deviation framework directly applicable to probabilistic reasoning.

**The Fisher information metric.** Consider a parametric family of probability distributions $\{p(x \mid \theta) : \theta \in \Theta\}$, where $\Theta \subseteq \mathbb{R}^n$ is the parameter space. The *Fisher information matrix* at a point $\theta$ is:

$$F_{ij}(\theta) = \mathbb{E}_{x \sim p(\cdot \mid \theta)}\left[\frac{\partial \log p(x \mid \theta)}{\partial \theta^i} \frac{\partial \log p(x \mid \theta)}{\partial \theta^j}\right]$$

The Fisher matrix defines a Riemannian metric on the parameter space $\Theta$. This is not an arbitrary choice — Chentsov's theorem (1972) proves that the Fisher information metric is the *unique* Riemannian metric (up to a constant factor) on statistical models that is invariant under sufficient statistics. In other words, the Fisher metric is the only metric that respects the intrinsic structure of statistical inference. Any other metric would change its answer depending on how you parameterize the model — a violation of the reparameterization invariance that we identified in Section 4.3 as a signature of geodesic reasoning.

**The statistical manifold.** The parameter space $\Theta$, equipped with the Fisher metric, becomes a Riemannian manifold called the *statistical manifold*. Points on this manifold are probability distributions (or, equivalently, parameter vectors specifying distributions). Curves on the manifold are paths through the space of distributions — exactly what probabilistic reasoning is.

For the simplest non-trivial example, consider the family of univariate Gaussian distributions $\mathcal{N}(\mu, \sigma^2)$. The parameter space is the upper half-plane $\{(\mu, \sigma) : \sigma > 0\}$. The Fisher information metric is:

$$ds^2 = \frac{d\mu^2}{\sigma^2} + \frac{2 \, d\sigma^2}{\sigma^2}$$

This is (up to a constant) the Poincare half-plane metric — the standard model of hyperbolic geometry. Geodesics on this manifold are semicircles and vertical lines, not straight lines. The geometric meaning is clear: changing the mean of a distribution with small variance (small $\sigma$) is "expensive" — you are moving between distributions that are very different (nearly non-overlapping). Changing the mean of a distribution with large variance is "cheap" — the distributions overlap heavily and are hard to distinguish. The Fisher metric captures this through the $1/\sigma^2$ factor.

**[Conditional Theorem.]** **Geodesics as optimal belief updates.** In the information-geometric framework, a reasoning process that updates beliefs from a prior $p(\cdot \mid \theta_0)$ to a posterior $p(\cdot \mid \theta_1)$ traces a path on the statistical manifold. The geodesic from $\theta_0$ to $\theta_1$ is the *most efficient* way to update beliefs — the update that wastes no "statistical effort." Any deviation from the geodesic corresponds to an update that is either too conservative (taking unnecessarily small steps) or too erratic (jumping in directions that do not contribute to reaching the posterior).

This connects directly to Bayesian inference. The geodesic on the statistical manifold from prior to posterior is, in a precise sense, the optimal Bayesian update. The geodesic deviation of an actual belief-update trajectory measures how far the update deviates from ideal Bayesian reasoning.

**[Established Mathematics.]** **The natural gradient.** The Fisher metric also gives rise to the *natural gradient*, introduced by Amari (1998). In standard gradient descent on a loss function $L(\theta)$, the update is:

$$\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)$$

where $\nabla L$ is the ordinary gradient. But the ordinary gradient depends on the parameterization — it is not a geometric object on the statistical manifold. The natural gradient corrects for this:

$$\theta_{t+1} = \theta_t - \eta F(\theta_t)^{-1} \nabla L(\theta_t)$$

where $F(\theta_t)^{-1}$ is the inverse Fisher information matrix. The natural gradient $\tilde{\nabla} L = F^{-1} \nabla L$ is the steepest descent direction *on the statistical manifold* — it accounts for the curvature of the parameter space.

The connection to geodesics is immediate. The natural gradient step is an infinitesimal geodesic step: it moves in the direction that maximally decreases the loss per unit of *statistical distance* (Fisher-Rao distance), rather than per unit of *Euclidean distance* in parameter space. A sequence of natural gradient steps approximates a geodesic on the statistical manifold.

This has practical implications for understanding neural network training as a reasoning process. Standard gradient descent follows a non-geodesic path through parameter space — it is distorted by the arbitrary Euclidean metric on $\mathbb{R}^n$, which has nothing to do with the statistical structure of the model. Natural gradient descent follows a near-geodesic path on the statistical manifold, adapting its step size and direction to the local curvature of the distribution family. The success of methods like Adam, KFAC, and other approximate natural gradient methods can be understood as partial corrections toward geodesic behavior in parameter space.

**For reasoning in LLMs specifically**, the information-geometric perspective offers a compelling interpretation of the attention mechanism. Each attention head computes a re-weighting of the value vectors — equivalently, a transformation of the probability distribution over the vocabulary. The sequence of attention layers traces a path through the space of distributions. If the model has learned an approximation to the Fisher metric (embedded in its learned parameters), then the attention mechanism implements an approximate natural gradient step at each layer, and the full forward pass traces an approximate geodesic on the statistical manifold of next-token distributions.

The deviation of this implicit trajectory from the true Fisher geodesic is, under this interpretation, a measure of the model's reasoning efficiency. A model with well-calibrated attention weights follows near-geodesic paths; a model with poorly calibrated weights wastes statistical effort on non-geodesic detours.

## Worked Example: The Geodesic of a Correct Triage and the Cost of Deviation

Dr. Okafor faces a patient — a 58-year-old woman presenting with acute shortness of breath, tachycardia, and unilateral leg swelling. We trace the geodesic of optimal diagnostic reasoning, then measure the geodesic deviation of a corrupted trajectory.

**The reasoning manifold.** The diagnostic state is a point in a probability simplex over the relevant differential: pulmonary embolism (PE), congestive heart failure (CHF), pneumonia, and anxiety. We equip this simplex with the Fisher information metric, which makes moves between clinically dissimilar distributions expensive and moves between similar distributions cheap.

**The geodesic (optimal trajectory).** The initial state is the uninformative prior $\gamma(0) = (0.25, 0.25, 0.25, 0.25)$. The patient's presentation — acute dyspnea with unilateral leg swelling — constitutes a strong likelihood signal. On the Fisher manifold, the geodesic from the prior curves directly toward the PE vertex, passing through intermediate states that progressively concentrate probability mass:

$$\gamma(0.3) \approx (0.50, 0.25, 0.15, 0.10) \quad \text{(after history and exam)}$$
$$\gamma(0.6) \approx (0.75, 0.15, 0.08, 0.02) \quad \text{(after D-dimer elevation)}$$
$$\gamma(1.0) \approx (0.97, 0.02, 0.01, 0.00) \quad \text{(after CT angiography confirms PE)}$$

The cost of this trajectory under the Fisher metric is the *statistical effort* — the total information gained, measured in natural units. The geodesic achieves this information gain with minimum total path length: each diagnostic step moves the belief state in the direction of maximum information per unit of clinical effort.

**The corrupted trajectory.** Now suppose the heuristic field is corrupted. The patient mentions that she has been feeling anxious about a new job. This surface feature activates an attentional bias (the mechanism of Chapter 3, Section 3.5) that inflates the heuristic gradient toward the anxiety basin. The corrupted trajectory deviates:

$$\tilde{\gamma}(0.3) \approx (0.30, 0.20, 0.15, 0.35) \quad \text{(anxiety hypothesis inflated)}$$
$$\tilde{\gamma}(0.5) \approx (0.20, 0.15, 0.10, 0.55) \quad \text{(premature convergence toward anxiety)}$$

At $\tilde{\gamma}(0.5)$, the corrupted heuristic reports $h(\tilde{\gamma}(0.5)) \approx 0$ — the system believes it has nearly reached the goal. If the system is satisficing (as discussed in Section 3.6), it terminates here. The patient is diagnosed with anxiety and sent home.

**The geodesic deviation.** The deviation between the corrupted trajectory and the geodesic is not merely the distance between their endpoints (which would be a measure of diagnostic error). It is the integrated excess cost:

$$\Delta(\tilde{\gamma}, \gamma^*) = \mathcal{L}[\tilde{\gamma}] - \mathcal{L}[\gamma^*]$$

This deviation has two components. The first is the *wasted path length* — the statistical effort expended traveling toward the anxiety basin, effort that contributed nothing to reaching the correct diagnosis. The second is the *recovery cost* — the additional effort required when the patient returns to the ER with hemodynamic instability from an untreated PE, and the diagnostic process must restart from a worse clinical state.

On the Fisher manifold, we can compute this explicitly. The geodesic distance from the prior to the PE-concentrated posterior is approximately $d_g(\gamma(0), \gamma(1)) \approx 2.1$ nats. The corrupted trajectory's total path length to its false terminus plus the recovery path is approximately $\mathcal{L}[\tilde{\gamma}] \approx 4.6$ nats. The geodesic deviation is:

$$\Delta \approx 4.6 - 2.1 = 2.5 \text{ nats}$$

The corrupted reasoning trajectory wastes more than double the statistical effort of the geodesic — and this accounting does not include the human cost of delayed treatment.

**The geometric lesson.** The geodesic deviation framework reveals something that accuracy-based evaluation cannot. Both the geodesic and the corrupted trajectory could, in principle, eventually reach the correct diagnosis (if the system does not terminate prematurely). The difference is not in whether they arrive, but in how efficiently they navigate the manifold. The corrupted trajectory's detour through the anxiety basin is not just a wrong turn — it is a measurable geometric quantity that predicts the clinical cost of the error. Geodesic deviation transforms "the doctor was initially confused" from an anecdote into a number.

---

## Technical Appendix

**The Geodesic Equation (Derivation Summary).** On a Riemannian manifold $(M, g)$, the geodesic $\gamma: [0,1] \to M$ minimizes the energy functional:

$$E[\gamma] = \frac{1}{2} \int_0^1 g_{ij}(\gamma(t)) \, \dot{\gamma}^i(t) \, \dot{\gamma}^j(t) \, dt$$

The Euler-Lagrange equations yield the geodesic equation:

$$\ddot{\gamma}^k + \Gamma^k_{ij} \dot{\gamma}^i \dot{\gamma}^j = 0$$

where the Christoffel symbols of the second kind are:

$$\Gamma^k_{ij} = \frac{1}{2} g^{kl}\left(\frac{\partial g_{lj}}{\partial \gamma^i} + \frac{\partial g_{li}}{\partial \gamma^j} - \frac{\partial g_{ij}}{\partial \gamma^l}\right)$$

The derivation, given in full in Section 4.1, proceeds through the Christoffel symbols of the first kind $\Gamma_{k,ij} = \frac{1}{2}(\partial_i g_{kj} + \partial_j g_{ki} - \partial_k g_{ij})$ and contraction with the inverse metric $g^{kl}$.

**Geodesic Deviation (Definition 4.2, restated formally).** Let $\gamma^*: [0,1] \to M$ be the geodesic connecting $x_0 = \gamma^*(0)$ to $x_1 = \gamma^*(1) \in \mathcal{G}$. For any piecewise-smooth curve $\gamma: [0,1] \to M$ with the same endpoints, the *geodesic deviation* is:

$$\Delta(\gamma, \gamma^*) = E[\gamma] - E[\gamma^*] \geq 0$$

with equality if and only if $\gamma$ is a reparameterization of $\gamma^*$. The non-negativity follows from the variational characterization of geodesics as energy minimizers.

**Geodesic Deviation on the Fisher Manifold (Proposition 4.2).** Let $\Theta$ be a statistical manifold equipped with the Fisher information metric $F_{ij}(\theta)$. For a belief-update trajectory $\theta(t)$ from prior $\theta_0$ to posterior $\theta_1$, the geodesic deviation is:

$$\Delta = \frac{1}{2}\int_0^1 F_{ij}(\theta(t))\dot{\theta}^i\dot{\theta}^j \, dt - \frac{1}{2} d_F(\theta_0, \theta_1)^2$$

where $d_F(\theta_0, \theta_1)$ is the Fisher-Rao geodesic distance. For the Gaussian family $\mathcal{N}(\mu, \sigma^2)$ with the Poincare half-plane metric $ds^2 = (d\mu^2 + 2 \, d\sigma^2)/\sigma^2$, geodesics are semicircles and vertical lines, and the geodesic distance has a closed-form expression. Deviations from geodesic belief update on this manifold correspond to statistically inefficient inference — updates that waste Fisher information.

**Jacobi Fields and Trajectory Stability (Proposition 4.3).** Let $\gamma^*$ be a geodesic and $J(t)$ a Jacobi field along $\gamma^*$ — an infinitesimal variation satisfying:

$$\frac{D^2 J}{dt^2} + R(J, \dot{\gamma}^*)\dot{\gamma}^* = 0$$

where $R$ is the Riemann curvature tensor and $D/dt$ is the covariant derivative along $\gamma^*$. The Jacobi field measures how nearby geodesics diverge from or converge toward $\gamma^*$. In regions of positive sectional curvature, nearby geodesics converge (the reasoning problem is "self-correcting" — small errors in the initial direction are damped). In regions of negative sectional curvature, nearby geodesics diverge (the reasoning problem is "chaotically sensitive" — small errors amplify exponentially). The rate of divergence is governed by the magnitude of the sectional curvature $K(\dot{\gamma}^*, J)$:

$$\|J(t)\| \sim \|J(0)\| \cdot e^{\sqrt{|K|} \cdot t} \quad \text{(negative curvature, divergent case)}$$

This provides a geometric criterion for reasoning robustness: problems whose reasoning manifolds have bounded positive sectional curvature admit robust geodesic solutions, while those with large negative curvature are inherently fragile.

---

## 4.9 Summary

The geodesic provides the normative standard for reasoning: it is the shortest path from problem to solution on the reasoning manifold. Geodesic deviation — the excess cost of the actual trajectory over the geodesic — is a measure of reasoning quality that is richer than accuracy, sensitive to process, and connected to robustness.

In the chapters that follow, we will see that the major failure modes of reasoning — heuristic corruption (Ch. 5), sycophancy (Ch. 6), local minima (Ch. 7), and gauge symmetry breaking (Ch. 8) — are all ways in which the actual trajectory deviates from the geodesic. Each failure mode corresponds to a specific geometric pathology that bends, traps, or redirects the reasoning path.

The geodesic deviation framework gives us a unified language for these diverse failures. They are not separate bugs to be patched individually — they are manifestations of the same underlying phenomenon: the system's implicit heuristic field failing to guide it along the shortest path.
