## The Geometric Series

This book is the second in a series and the theoretical parent of all that follow.

The series has three tiers.

**Tier 1: The Toolkit.** *Geometric Methods in Computational Modeling* (Bond, 2026a) develops the mathematical apparatus: manifolds, metrics, curvature, persistent homology, group-theoretic augmentation, SPD manifolds, topological data analysis, hyperbolic geometry, and the Bond Geodesic Equilibrium. It is a mathematics book. Its domain is computation. It provides the tools; it does not commit them to any particular subject.

**Tier 2: The General Theory.** *Geometric Reasoning: From Search to Manifolds* — this book — commits the tools to a subject: cognition. It claims that reasoning, human and artificial, is informed search on a structured manifold, that reasoning quality is determined by the geometry of the heuristic field, and that reasoning failures are geometric pathologies. It develops this claim through five parts, grounds it in empirical data from the Measuring AGI benchmarks, and demonstrates that the theory produces working engineering. This is the parent text. Every domain-specific book in the series inherits its framework.

**Tier 3: Domain Instantiations.** Each domain text takes the general framework and instantiates it on a domain-specific manifold. The core objects specialize:

| General Object (this book) | Geometric Ethics | Geometric Economics | Geometric Law |
|---|---|---|---|
| Reasoning manifold $M$ | Moral manifold $\mathcal{M}$ (9D, Whitney-stratified) | Economic decision complex $E$ (9D, Mahalanobis metric) | Judicial reasoning space $\mathcal{J}$ |
| Heuristic field $h(x)$ | Obligation vectors $O^\mu$ (rank-1 tensors) | Price signals, utility gradients | Precedent weights, statutory constraints |
| Geodesic $\gamma^*$ | Path of least moral resistance | Pareto-optimal trade path (BGE) | Chain of legal reasoning |
| Failure modes (Ch. 5--7) | Framing effects, moral sycophancy, overconfident moral judgment | Market bubbles (local minima), herding (sycophancy), mispricing (heuristic corruption) | Framing in sentencing, judicial deference (sycophancy), precedent traps (local minima) |
| Symmetry group $G$ | $D_4 \times U(1)_H$ (Hohfeldian gauge group) | Market symmetries (currency relabeling, unit scaling) | Constitutional symmetries (equal protection, due process invariance) |
| BIP | Moral evaluations invariant under re-description | Economic evaluations invariant under unit changes | Legal judgments invariant under party relabeling |
| Scalar Irrecoverability | Moral tensors cannot be reduced to scalars without loss | GDP is an irrecoverable contraction of the economic tensor | Sentencing guidelines lose the structure of the judicial tensor |
| Engineering output | DEME architecture, ErisML, Bond Index | Bond Geodesic Equilibrium algorithm | Judicial decision complex, constitutional path homology |
| Benchmark method | Dear Abby corpus, BIP experiments, cross-lingual invariance | Market invariance tests, BGE convergence | Sentencing invariance tests, precedent consistency |

The table is not decoration. It is a claim: the same mathematical architecture — manifold, heuristic, geodesic, failure modes, symmetry, scalar irrecoverability, engineering — instantiates differently in each domain, but the *structure* is invariant. The parent text captures the invariant structure. The domain texts capture the specializations.

### The Inheritance Principle

Each domain text inherits the following from *Geometric Reasoning* without re-derivation:

- The **heuristic field formalism** (Chapter 3): the interpretation of guidance signals as scalar fields on the domain manifold, with attention as the mechanism in neural implementations.
- The **geodesic deviation measure** (Chapter 4): the quantification of reasoning quality as excess path length over the optimal trajectory.
- The **failure taxonomy** (Chapters 5--8): heuristic corruption, objective hijacking, local minima, and gauge breaking as the four geometric pathologies of reasoning. Each domain exhibits all four, but with domain-specific triggers and consequences.
- The **metacognitive control framework** (Chapter 9): calibration, self-monitoring, strategy selection, and the ~38% recovery ceiling as structural features of prompted reasoning systems.
- The **Scalar Irrecoverability Theorem** (Chapters 10, 13): the proof that collapsing a multi-dimensional reasoning profile into a single score destroys information that cannot be recovered. Every domain has its own version of this theorem — for ethics, it is the inadequacy of scalar moral evaluation; for economics, it is the inadequacy of GDP; for law, it is the inadequacy of sentencing guidelines.
- The **Bond Invariance Principle** as a necessary condition (Chapter 11): gauge invariance violation implies misalignment in the general case, which specializes to misalignment in moral reasoning, mispricing in economics, and injustice in law.
- The **benchmark methodology** (Chapter 12): the eight types of geometric probes — invariance, sensitivity, bottleneck, recovery, frontier, meta-search, constraint, path efficiency — which each domain instantiates with domain-specific tasks.
- The **engineering toolkit** (Chapter 14): group-theoretic augmentation, adversarial training, LoRA as curvature adjustment, SPD features, TDA, and hyperbolic embeddings, which each domain deploys on its specific data.

Each domain text *adds* domain-specific structure — the specific manifold, the specific metric, the specific symmetry group, the specific boundary conditions — and develops domain-specific consequences that the general theory cannot anticipate. The stratified structure of moral space, with its Whitney conditions and semantic gates, is a discovery of *Geometric Ethics*, not a prediction of *Geometric Reasoning*. The conservation of harm, derived from Noether's theorem applied to the BIP, is a domain-specific consequence that the parent text's gauge invariance framework enables but does not itself produce. The No Escape Theorem for structural containment of AI systems within ethical constraints is a theorem about the specific geometry of the moral manifold — it requires the domain-specific features of stratification, grounded evaluation, and canonicalization that the general theory does not assume.

### The Current State of the Series

**Geometric Ethics** (Bond, 2026b) is the first and most developed domain instantiation. At over 400 pages across thirty chapters, it demonstrates that moral reasoning has the full geometric structure predicted by the parent theory: a 9-dimensional stratified manifold, a tensor hierarchy (obligations as vectors, interests as covectors, satisfaction as contraction), a $D_4$ dihedral gauge group on Hohfeldian normative relations, a conservation law for harm derived from Noether's theorem, and a No Escape Theorem for structural containment of AI systems. It also extends the parent theory in directions specific to moral reasoning: quantum normative dynamics (superposition and interference in moral deliberation), collective moral agency (tensorial aggregation with emergent properties), and the philosophy of moral contraction (the irreversible, informationally lossy process by which a tensor becomes a decision). These extensions are domain-specific — they arise from features of moral space that do not have obvious analogues in other domains — and they illustrate the depth that domain instantiation can achieve.

**Geometric Economics** exists in embryonic form in the Bond Geodesic Equilibrium (Chapter 14 of this book and Chapter 20 of *Geometric Methods*). The economic decision complex is a 9-dimensional space with a Mahalanobis metric encoding the covariance structure of economic dimensions and boundary penalties for sacred values (constraints so fundamental that no trade-off is permitted). Nash equilibrium is the scalar projection of the BGE — and the information lost in this projection is precisely the information the Scalar Irrecoverability Theorem says cannot be recovered. The full development of geometric economics — market dynamics as flows on the decision manifold, financial crises as curvature singularities, regulation as boundary enforcement — remains ahead.

**Geometric Law** is the least developed but perhaps the most structurally constrained. The Hohfeldian $D_4$ group — discovered in the ethics domain — has its natural home in law, where Wesley Newcomb Hohfeld's original analysis of jural relations was developed in 1913. The eight-element dihedral symmetry of obligation, claim, liberty, and no-claim under correlative and negation operations is a mathematical fact about the structure of legal relations, not a metaphor imported from physics. Constitutional review as path homology preservation (a constitutional amendment must not break the topological connectivity of the rights manifold), equal protection as gauge invariance (outcomes must not depend on protected characteristics), and sentencing disparities as gauge violation tensors (measured, diagnosed, and correctable by the same methods used in Chapter 11) are natural applications of the framework that await full development.

### The Vision

The ambition is not to geometrize everything. It is to notice that the same mathematical structures — manifolds, metrics, symmetries, conservation laws — keep appearing whenever we look carefully at structured reasoning. The parent theory captures what they share. The domain texts capture what makes each domain distinctive.

If the program succeeds, it will have provided something that currently does not exist: a common mathematical language for reasoning across domains. A moral philosopher discussing the structure of obligation and an economist discussing the structure of equilibrium would discover they are using the same mathematics — not by coincidence, but because the reasoning they study has the same geometric character. The domain-specific details differ. The architecture is shared.

Whether this vision will prove correct is an empirical question. It will be answered not by philosophical argument but by the accumulation of domain instantiations, each tested against its own data, each confirming or falsifying the prediction that the parent theory's architecture transfers. *Geometric Ethics* is the first test. It has passed. The question is whether the others will follow.
