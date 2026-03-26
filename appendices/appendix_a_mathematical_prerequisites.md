# Appendix A: Mathematical Prerequisites

This appendix provides a concise review of the mathematical tools used throughout the book. It is not a substitute for a textbook treatment; the goal is to establish notation, state key definitions, and build the intuitions that the main text relies on. Readers seeking a fuller development should consult do Carmo (1992) for Riemannian geometry, Bhatia (2007) for SPD manifolds, Edelsbrunner and Harer (2010) for persistent homology, and Artin (1991) for group theory.

---

## A.1 Manifolds and Tangent Spaces

### Smooth Manifolds

A **smooth manifold** of dimension $n$ is a topological space $M$ that is locally homeomorphic to $\mathbb{R}^n$ and equipped with a smooth structure. "Locally homeomorphic" means that every point $p \in M$ has a neighborhood $U$ and a homeomorphism $\varphi: U \to \varphi(U) \subseteq \mathbb{R}^n$. The pair $(U, \varphi)$ is a **chart**, and the components of $\varphi(p) = (x^1, \ldots, x^n)$ are **local coordinates** of $p$.

A collection of charts $\{(U_\alpha, \varphi_\alpha)\}$ that covers $M$ (i.e., $\bigcup_\alpha U_\alpha = M$) is an **atlas**. The smooth structure requires that whenever two charts overlap --- $U_\alpha \cap U_\beta \neq \emptyset$ --- the **transition map** $\varphi_\beta \circ \varphi_\alpha^{-1}: \varphi_\alpha(U_\alpha \cap U_\beta) \to \varphi_\beta(U_\alpha \cap U_\beta)$ is a smooth (infinitely differentiable) map between open subsets of $\mathbb{R}^n$.

**The key intuition.** A manifold is a space that looks like $\mathbb{R}^n$ in every small neighborhood, but may have a different global shape. The surface of a sphere is a 2-manifold: every small patch looks flat, but the global topology is that of $S^2$, not $\mathbb{R}^2$. The reasoning manifold of this book (Chapter 2) is, by hypothesis, a manifold: every small neighborhood of reasoning states is parameterizable by a finite number of coordinates, even though the global structure may be complex.

### Tangent Vectors and the Tangent Bundle

At each point $p \in M$, the **tangent space** $T_p M$ is the vector space of all "directions" in which one can move from $p$. Formally, a tangent vector $v \in T_p M$ can be defined as a derivation --- a linear map $v: C^\infty(M) \to \mathbb{R}$ satisfying the Leibniz rule $v(fg) = f(p)v(g) + g(p)v(f)$.

In local coordinates $(x^1, \ldots, x^n)$, the partial derivatives $\partial / \partial x^1 |_p, \ldots, \partial / \partial x^n |_p$ form a basis for $T_p M$, and any tangent vector can be written as $v = v^i \frac{\partial}{\partial x^i}|_p$ (using the Einstein summation convention: repeated upper and lower indices are summed over).

The **tangent bundle** $TM = \bigsqcup_{p \in M} T_p M$ is the disjoint union of all tangent spaces, itself a smooth manifold of dimension $2n$. A point in $TM$ is a pair $(p, v)$ where $p \in M$ and $v \in T_p M$. A smooth curve $\gamma: [0,1] \to M$ has a velocity vector $\dot{\gamma}(t) = \frac{d\gamma^i}{dt} \frac{\partial}{\partial x^i} \in T_{\gamma(t)} M$ at each time $t$ --- the velocity is a section of the tangent bundle along the curve.

In the reasoning framework, a tangent vector at a reasoning state represents an *infinitesimal reasoning step*: the direction and rate of change of the state at a particular instant. The velocity $\dot{\gamma}(t)$ of a reasoning trajectory is the "direction of thought" at time $t$.

---

## A.2 Riemannian Metrics and Distance

### The Metric Tensor

A **Riemannian metric** on a smooth manifold $M$ is a smooth assignment of an inner product $g_p: T_p M \times T_p M \to \mathbb{R}$ to each tangent space $T_p M$. In local coordinates, the metric is represented by a symmetric positive definite matrix:

$$g = g_{ij}(x) \, dx^i \otimes dx^j$$

where $g_{ij}(x) = g\left(\frac{\partial}{\partial x^i}, \frac{\partial}{\partial x^j}\right)$. The matrix $(g_{ij})$ is positive definite at each point, which ensures that the inner product is non-degenerate: every nonzero tangent vector has positive length.

The metric determines the **length of a tangent vector**: $\|v\|_g = \sqrt{g_{ij} v^i v^j}$, the **angle between tangent vectors**: $\cos \theta = g_{ij} v^i w^j / (\|v\| \|w\|)$, and the **length of a curve** $\gamma: [a,b] \to M$:

$$L[\gamma] = \int_a^b \sqrt{g_{ij}(\gamma(t)) \dot{\gamma}^i(t) \dot{\gamma}^j(t)} \, dt$$

The **geodesic distance** between two points $p, q \in M$ is the infimum of the lengths of all smooth curves connecting them:

$$d(p, q) = \inf_{\gamma: \gamma(0) = p, \gamma(1) = q} L[\gamma]$$

This is a true metric in the topological sense (non-negative, symmetric, satisfies the triangle inequality) and makes $(M, d)$ a metric space compatible with its manifold topology.

### The Levi-Civita Connection and Christoffel Symbols

To differentiate vector fields on a manifold, we need a **connection**: a rule for comparing tangent vectors at different points. The Riemannian metric determines a unique connection --- the **Levi-Civita connection** $\nabla$ --- characterized by two properties:

1. **Metric compatibility**: $\nabla g = 0$, i.e., parallel transport preserves inner products.
2. **Torsion-free**: $\nabla_X Y - \nabla_Y X = [X, Y]$ for all vector fields $X, Y$.

In local coordinates, the connection is encoded by the **Christoffel symbols of the second kind**:

$$\Gamma^k_{ij} = \frac{1}{2} g^{kl}\left(\frac{\partial g_{jl}}{\partial x^i} + \frac{\partial g_{il}}{\partial x^j} - \frac{\partial g_{ij}}{\partial x^l}\right)$$

where $g^{kl}$ is the inverse metric: $g^{kl} g_{lm} = \delta^k_m$. The Christoffel symbols measure how the coordinate basis vectors change from point to point and are needed for the geodesic equation and curvature computations.

---

## A.3 Geodesics and Curvature

### The Geodesic Equation

A **geodesic** is a curve $\gamma(t)$ that parallel-transports its own velocity vector --- intuitively, a curve that is "as straight as possible" given the curvature of the manifold. In local coordinates, it satisfies:

$$\frac{d^2 \gamma^k}{dt^2} + \Gamma^k_{ij} \frac{d\gamma^i}{dt} \frac{d\gamma^j}{dt} = 0$$

This is a system of $n$ coupled second-order ODEs. Given an initial point $\gamma(0) = p$ and initial velocity $\dot{\gamma}(0) = v \in T_p M$, the geodesic exists and is unique in a neighborhood of $p$ (by the standard existence and uniqueness theorem for ODEs). In flat Euclidean space ($\Gamma^k_{ij} = 0$), geodesics are straight lines: $\gamma(t) = p + tv$. On a sphere, they are great circles. The derivation from the energy functional via the Euler-Lagrange equations is given in Chapter 4.

### Curvature

Curvature measures how the manifold deviates from being flat. There are several notions, each capturing a different aspect of the geometry.

**The Riemann curvature tensor** $R^l_{\ ijk}$ is the fundamental curvature object, measuring the failure of parallel transport around an infinitesimal loop:

$$R^l_{\ ijk} = \frac{\partial \Gamma^l_{jk}}{\partial x^i} - \frac{\partial \Gamma^l_{ik}}{\partial x^j} + \Gamma^l_{im} \Gamma^m_{jk} - \Gamma^l_{jm} \Gamma^m_{ik}$$

**Sectional curvature** $K(\sigma)$ is the curvature of a 2-dimensional section of the tangent space. Given two linearly independent tangent vectors $u, v \in T_p M$ spanning a 2-plane $\sigma$:

$$K(\sigma) = \frac{R_{ijkl} u^i v^j u^k v^l}{(g_{ik} g_{jl} - g_{il} g_{jk}) u^i v^j u^k v^l}$$

where $R_{ijkl} = g_{lm} R^m_{\ ijk}$.

**Ricci curvature** $\text{Ric}_{ij}$ is the trace of the Riemann tensor over two indices:

$$\text{Ric}_{ij} = R^k_{\ ikj}$$

It measures the average sectional curvature over all 2-planes containing a given direction. **Scalar curvature** $R = g^{ij} \text{Ric}_{ij}$ is the full trace --- a single number at each point summarizing the average curvature.

**Geometric effects of curvature.** The sign of curvature determines how geodesics behave:

- **Positive curvature** (like a sphere): initially parallel geodesics converge. Triangles have angle sums greater than $\pi$. The manifold is "compact" in a local sense.
- **Zero curvature** (like flat space): initially parallel geodesics remain parallel. Triangles have angle sum exactly $\pi$.
- **Negative curvature** (like a saddle or hyperbolic space): initially parallel geodesics diverge. Triangles have angle sums less than $\pi$. There is "more room" at each point than in flat space.

In the reasoning framework, positive curvature means that distinct reasoning trajectories starting from nearby initial states tend to converge --- the manifold funnels reasoning toward a shared conclusion. Negative curvature means they diverge --- small differences in initial state lead to increasingly different reasoning paths. This is why the hyperbolic geometry of Section 14.5 is natural for hierarchical reasoning: the exponential growth of volume with distance in negatively curved space matches the branching structure of hierarchical decomposition.

---

## A.4 The SPD Manifold

### Definition

The space $\text{SPD}(n)$ consists of all $n \times n$ real symmetric matrices $P$ such that $x^T P x > 0$ for all nonzero $x \in \mathbb{R}^n$. Equivalently, $P \in \text{SPD}(n)$ if and only if $P = P^T$ and all eigenvalues of $P$ are strictly positive.

$\text{SPD}(n)$ is an open cone in the vector space of symmetric matrices: it is closed under addition and positive scalar multiplication, and it is an open subset of $\mathbb{R}^{n(n+1)/2}$ (the space of symmetric matrices). As an open subset of Euclidean space, it is automatically a smooth manifold of dimension $n(n+1)/2$.

### The Affine-Invariant Metric

The standard Riemannian metric on $\text{SPD}(n)$ is the **affine-invariant metric**. At a point $P \in \text{SPD}(n)$, the tangent space $T_P \text{SPD}(n)$ is the space of symmetric matrices, and the inner product is:

$$\langle S_1, S_2 \rangle_P = \text{tr}(P^{-1} S_1 P^{-1} S_2)$$

where $S_1, S_2$ are symmetric matrices (tangent vectors). The resulting geodesic distance between $P, Q \in \text{SPD}(n)$ is:

$$d(P, Q) = \|\log(P^{-1/2} Q P^{-1/2})\|_F = \left(\sum_{i=1}^n \log^2 \lambda_i\right)^{1/2}$$

where $\lambda_1, \ldots, \lambda_n$ are the eigenvalues of $P^{-1} Q$ and $\|\cdot\|_F$ is the Frobenius norm. This metric is **affine-invariant**: for any invertible matrix $A$, $d(A P A^T, A Q A^T) = d(P, Q)$.

### The Log-Euclidean Approximation

Computing the affine-invariant distance requires matrix square roots and logarithms, which can be expensive for large $n$. The **log-Euclidean metric** provides a computationally cheaper alternative:

$$d_{\text{LE}}(P, Q) = \|\log P - \log Q\|_F$$

where $\log$ is the matrix logarithm. This maps each SPD matrix to the vector space of symmetric matrices via $P \mapsto \log P$, after which the Euclidean (Frobenius) distance is used. The log-Euclidean metric is a first-order approximation to the affine-invariant metric and is exact when $P$ and $Q$ commute.

### Why SPD Matters

SPD matrices arise naturally in several contexts relevant to this book:

- **Covariance matrices.** The sample covariance matrix of a multivariate distribution is SPD (when the sample size exceeds the dimension). Comparing covariance matrices --- e.g., comparing the spectral characteristics of different audio recordings (Section 14.4) --- is a problem on $\text{SPD}(n)$.
- **Fisher information matrices.** The Fisher information matrix $g_{ij}(\theta)$ is an SPD matrix (under regularity conditions). The space of Fisher information matrices, as the parameter $\theta$ varies, traces a curve on $\text{SPD}(n)$.
- **Diffusion tensors.** In diffusion MRI, each voxel's diffusion characteristics are described by a $3 \times 3$ SPD matrix.

The BirdCLEF pipeline of Section 14.4 uses $\text{SPD}(16)$: 16-band covariance matrices computed from mel spectrograms. The 136-dimensional feature vector (the upper triangle of the $16 \times 16$ covariance matrix) lives on the SPD manifold, and the log-Euclidean distance between these feature vectors measures spectral dissimilarity in a geometrically principled way.

---

## A.5 Persistent Homology

### Simplicial Complexes and Filtrations

A **simplicial complex** $K$ is a collection of simplices --- vertices (0-simplices), edges (1-simplices), triangles (2-simplices), tetrahedra (3-simplices), etc. --- that is closed under taking faces. A **filtration** is a nested sequence of simplicial complexes:

$$\emptyset = K_0 \subseteq K_1 \subseteq K_2 \subseteq \cdots \subseteq K_N = K$$

typically parameterized by a scale parameter $\epsilon$: $K_\epsilon$ includes all simplices whose vertices are within distance $\epsilon$ of each other. As $\epsilon$ increases, more simplices are added, and the complex grows.

The two standard constructions are:

- **Vietoris-Rips complex** $\text{VR}_\epsilon(X)$: a simplex $\{x_0, \ldots, x_k\}$ is included if $d(x_i, x_j) \leq \epsilon$ for all $i, j$. Easy to compute; may be large.
- **Cech complex** $\check{C}_\epsilon(X)$: a simplex $\{x_0, \ldots, x_k\}$ is included if the balls $B_\epsilon(x_0), \ldots, B_\epsilon(x_k)$ have a common intersection. Harder to compute; gives exact topological information via the Nerve Theorem.

### Betti Numbers

The **Betti numbers** $\beta_0, \beta_1, \beta_2, \ldots$ of a simplicial complex count its topological features:

- $\beta_0$: the number of connected components.
- $\beta_1$: the number of independent loops (1-dimensional holes).
- $\beta_2$: the number of independent voids (2-dimensional cavities).
- $\beta_k$: the number of independent $k$-dimensional holes.

Formally, $\beta_k = \text{rank}(H_k(K))$, where $H_k(K)$ is the $k$-th homology group of $K$. These are computed as $\beta_k = \text{rank}(\ker \partial_k) - \text{rank}(\text{im} \, \partial_{k+1})$, where $\partial_k$ is the boundary operator mapping $k$-chains to $(k-1)$-chains.

### Persistence Diagrams and Stability

As the filtration parameter $\epsilon$ increases, topological features appear (are "born") and disappear ("die"). A connected component is born when a new vertex appears and dies when it merges with another component. A loop is born when a cycle of edges forms and dies when a triangle fills it in.

A **persistence diagram** is a multiset of points $(b_i, d_i)$ in the plane, where $b_i$ is the birth time and $d_i$ is the death time of the $i$-th feature. Points far from the diagonal $d = b$ represent persistent (long-lived) features --- likely genuine topological structure. Points near the diagonal represent short-lived features --- likely noise.

The **stability theorem** (Cohen-Steiner, Edelsbrunner, and Harer, 2007) guarantees that small perturbations of the input data produce small perturbations of the persistence diagram (in the bottleneck or Wasserstein distance). This makes persistent homology robust to noise.

### The Takens Embedding Theorem

Takens' theorem (1981) provides the bridge from time series to topology. Given a dynamical system with state space $M$ and a smooth observation function $\phi: M \to \mathbb{R}$, the **delay embedding** $\Phi: M \to \mathbb{R}^d$ defined by:

$$\Phi(x) = (\phi(x), \phi(F(x)), \phi(F^2(x)), \ldots, \phi(F^{d-1}(x)))$$

where $F$ is the dynamics map, is generically an embedding when $d > 2 \dim(M)$. That is, the delay embedding recovers the topology of the state space from a single scalar time series.

The BirdCLEF pipeline (Section 14.4) uses Takens embedding with delay $\tau = 10$ and embedding dimension $d = 3$ to reconstruct the attractor of the audio signal dynamics. Persistent homology is then applied to the embedded point cloud to extract topological features: $\beta_0$ (number of components --- related to the number of distinct spectral modes), $\beta_1$ (number of loops --- related to periodicity in the signal). The resulting 16-dimensional TDA feature vector (persistence statistics across multiple frequency bands) captures topological structure that is invisible to pointwise spectral features.

---

## A.6 Group Theory for Data Augmentation

### Groups and Subgroups

A **group** $(G, \cdot)$ is a set $G$ equipped with a binary operation $\cdot$ satisfying:

1. **Closure**: $a \cdot b \in G$ for all $a, b \in G$.
2. **Associativity**: $(a \cdot b) \cdot c = a \cdot (b \cdot c)$ for all $a, b, c \in G$.
3. **Identity**: There exists $e \in G$ such that $e \cdot a = a \cdot e = a$ for all $a$.
4. **Inverses**: For each $a \in G$, there exists $a^{-1} \in G$ such that $a \cdot a^{-1} = a^{-1} \cdot a = e$.

A **subgroup** $H \leq G$ is a subset that is itself a group under the same operation. The **order** $|G|$ is the number of elements (for finite groups).

### Key Examples

**The symmetric group** $S_n$ is the group of all permutations of $\{1, 2, \ldots, n\}$, with composition as the group operation. It has order $|S_n| = n!$. In Section 14.1, $S_8$ acts on bit positions (permuting which bit is which), $S_{26}$ acts on the alphabet (permuting letters in a cipher), and $S_n$ acts on symbols (permuting symbol labels).

**The dihedral group** $D_n$ is the group of symmetries of a regular $n$-gon, consisting of $n$ rotations and $n$ reflections, with order $|D_n| = 2n$. In Section 14.1, $D_8$ (often written $D_4$ in the convention that indexes by the polygon rather than the group order) acts on 2D grids by rotation and reflection. The Hohfeldian $D_4$ of Section 8.8 acts on the four-element set $\{O, C, L, N\}$ (Obligation, Claim, Liberty, No-Right) by the symmetries of the Hohfeldian square.

**The cyclic group** $\mathbb{Z}_n$ is the group of integers modulo $n$ under addition. $\mathbb{Z}_2 = \{0, 1\}$ acts as a binary flip: in Section 14.1, it is the bitwise complement operation.

**Continuous groups.** The multiplicative group $\mathbb{R}^+ = (\mathbb{R}_{>0}, \times)$ of positive reals under multiplication is a one-dimensional Lie group. In Section 14.1, it acts by rescaling physical constants (gravitational constant, conversion factors).

### Group Actions

A **group action** of $G$ on a set $X$ is a map $\rho: G \times X \to X$, written $\rho(g, x) = g \cdot x$, satisfying:

1. $e \cdot x = x$ for all $x \in X$ (the identity acts trivially).
2. $(gh) \cdot x = g \cdot (h \cdot x)$ for all $g, h \in G$ and $x \in X$ (the action is compatible with the group operation).

The **orbit** of a point $x$ under $G$ is $G \cdot x = \{g \cdot x : g \in G\}$ --- the set of all points reachable from $x$ by applying group elements. The **stabilizer** of $x$ is $G_x = \{g \in G : g \cdot x = x\}$ --- the subgroup of elements that fix $x$.

### Invariant and Equivariant Maps

A function $f: X \to Y$ is **$G$-invariant** if $f(g \cdot x) = f(x)$ for all $g \in G$ and $x \in X$. The function's output does not depend on which element of the orbit $G \cdot x$ is presented as input. This is the mathematical formulation of the Bond Invariance Principle (Chapter 8): a reasoning process should be invariant under gauge transformations.

A function $f: X \to Y$ is **$G$-equivariant** (where $G$ also acts on $Y$) if $f(g \cdot x) = g \cdot f(x)$ for all $g \in G$ and $x \in X$. The function commutes with the group action: transforming the input and then applying $f$ gives the same result as applying $f$ and then transforming the output. Equivariance is a weaker condition than invariance but still imposes strong structural constraints.

### The Orbit-Stabilizer Theorem

**Theorem.** *For a finite group $G$ acting on a set $X$, and any $x \in X$:*

$$|G| = |G \cdot x| \times |G_x|$$

*That is, the order of the group equals the size of the orbit times the order of the stabilizer.*

This theorem is directly relevant to data augmentation. If we augment a training example $x$ by applying all elements of a symmetry group $G$, the number of distinct augmented examples is $|G \cdot x| = |G| / |G_x|$. If $x$ has no symmetries (the stabilizer is trivial, $G_x = \{e\}$), we get $|G|$ augmented examples. If $x$ has symmetries (e.g., a palindromic bit string is fixed by certain permutations), we get fewer.

In the Nemotron pipeline (Section 14.1), the orbit-stabilizer theorem explains why the augmentation expansion factor varies: some training examples have non-trivial stabilizers under the relevant symmetry group (e.g., a bit manipulation rule that is invariant under certain bit permutations), yielding fewer distinct augmented versions. The 1.5--2.5x expansion range reflects the average orbit size across the dataset --- a direct consequence of the distribution of stabilizer sizes.

This completes the mathematical prerequisites. The main text uses these tools freely; this appendix is intended as a reference for readers who encounter an unfamiliar definition or who wish to verify the precise formulation of a statement used in the argument.
