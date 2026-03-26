# The Geometric Series — Domain Book Outlines

## Series Architecture

All domain books inherit from *Geometric Reasoning: From Search to Manifolds* (Bond, 2026c), the parent text. Each instantiates the general framework — manifold, heuristic field, geodesic, failure taxonomy, gauge invariance, Scalar Irrecoverability — on a domain-specific manifold with domain-specific structure.

**What each domain book does NOT need to re-derive:**
- The search-geometry connection (GR Ch. 1-2)
- The heuristic field formalism (GR Ch. 3)
- The geodesic deviation measure (GR Ch. 4)
- The four failure modes: corruption, hijacking, local minima, gauge breaking (GR Ch. 5-8)
- The metacognitive control framework (GR Ch. 9)
- The Scalar Irrecoverability Theorem (GR Ch. 10/13)
- The BIP as necessary condition (GR Ch. 11)
- The eight probe types for benchmarking (GR Ch. 12)
- The engineering toolkit: augmentation, adversarial training, LoRA (GR Ch. 14)

**What each domain book MUST provide:**
1. The domain-specific manifold and its justification
2. The domain-specific metric and what it encodes
3. The domain-specific symmetry group
4. The domain-specific BIP instantiation
5. Domain-specific failure modes (the general four, plus any new ones)
6. The domain's version of Scalar Irrecoverability (what information does scalar reduction destroy?)
7. Empirical evidence from the domain
8. Engineering applications
9. What the domain teaches the general theory (feedback to the parent)

---

## Book 3: Geometric Ethics
### *The Mathematical Structure of Moral Reasoning*
**Status: PUBLISHED (v1.23, 400+ pages, 30 chapters)**

Already exists. The first and most developed domain instantiation. Summary:

- **Manifold:** 9-dimensional Whitney-stratified moral manifold $\mathcal{M}$, with strata joined by semantic gates
- **Metric:** Moral metric $g_{\mu\nu}$ encoding trade-off structure between moral dimensions; context-dependent, potentially degenerate (incommensurable values)
- **Tensors:** Obligations as vectors $O^\mu$, interests as covectors $I_\mu$, satisfaction $S = I_\mu O^\mu$ as contraction
- **Symmetry:** $D_4 \times U(1)_H$ — Hohfeldian dihedral group on jural relations, plus harm conservation
- **BIP:** Moral evaluations invariant under re-description of morally equivalent scenarios
- **Scalar Irrecoverability:** Moral tensors cannot be contracted to scalars without destroying the information that matters most in hard cases
- **Key theorem:** No Escape Theorem — structural containment of AI within geometric ethical constraints
- **Key result:** Conservation of harm via Noether's theorem applied to BIP
- **Evidence:** Dear Abby corpus (20,030 letters), BIP experiments (cross-lingual invariance), quantum cognition predictions
- **Engineering:** DEME architecture, ErisML modeling language, Bond Index

---

## Book 4: Geometric Economics
### *Decision Manifolds, Equilibria, and the Geometry of Markets*

### The Scalar Failure
Economics has been scalar longer than ethics. GDP, utility, welfare functions, cost-benefit ratios — the entire apparatus of economic analysis compresses multi-dimensional reality into single numbers. The consequences are well-documented (Stiglitz-Sen-Fitoussi commission, 2009; Raworth's Doughnut Economics, 2017) but the alternative has been vague: "use multiple indicators." The geometric framework provides the mathematical alternative: the economic tensor, of which GDP is a specific contraction.

### Part I: The Problem
1. **The Scalar Economy** — Why GDP fails, why utility maximization produces paradoxes, why cost-benefit analysis hides the metric choice. The economic analogue of Chapter 2 of Geometric Ethics.
2. **Historical Precursors** — Adam Smith's invisible hand as a gradient flow. Walras's general equilibrium as a fixed point on a manifold. Arrow-Debreu as a topological existence proof. Amartya Sen's capabilities as manifold coordinates. These thinkers were doing geometry without the vocabulary.

### Part II: The Framework
3. **The Economic Decision Manifold** — A 9-dimensional space (inherited from the moral manifold's scope × mode decomposition, adapted for economic dimensions). Points are economic states. The manifold is not the economy — it is the space of possible economic configurations accessible to a decision-maker.
4. **The Economic Metric** — The Mahalanobis metric $d(s,t) = \sqrt{(s-t)^T \Sigma^{-1} (s-t)}$ plus boundary penalties $\sum_k \beta_k \cdot \mathbb{1}[\text{boundary violated}]$. The covariance matrix $\Sigma$ encodes which economic dimensions co-vary (substitutes have positive covariance, complements have negative). The boundary penalties encode sacred constraints ($\beta = \infty$ for e.g. "no child labor" — not a trade-off but a hard boundary). Different economic theories correspond to different metrics: utilitarian economics has a diagonal metric (all dimensions commensurable), capabilities economics has a degenerate metric (some dimensions incommensurable), welfare economics has off-diagonal terms encoding distributional concerns.
5. **The Price Signal as Heuristic Field** — Prices are the economy's heuristic: they estimate the cost of moving from one economic state to another. A well-functioning market has an admissible price heuristic — prices never overestimate true cost. Market failures are heuristic corruption: externalities warp the price field, monopolies distort the gradient, information asymmetry makes the heuristic unreliable. The efficient market hypothesis is the claim that the price heuristic is optimal — it guides search along geodesics.
6. **Economic Tensors** — Following the tensor hierarchy from Geometric Ethics: economic obligations as vectors (what must be produced/provided), economic interests as covectors (what is needed/demanded), satisfaction as contraction. The full economic tensor captures the multi-agent, multi-dimensional structure of economic interaction. GDP is a specific contraction of this tensor — and the Scalar Irrecoverability Theorem says the contraction destroys information about distribution, sustainability, and incommensurable values.

### Part III: Dynamics and Symmetry
7. **The Bond Geodesic Equilibrium** — The central construction. Nash equilibrium is the scalar projection of a richer geometric object: the BGE, where each agent finds the geodesic on their decision manifold and equilibrium is the mutual consistency of all agents' geodesics. Theorem: Nash equilibrium is a specific contraction of the BGE, and the contraction is lossy (Scalar Irrecoverability for equilibria). The BGE algorithm: iterated best-response A* on the decision manifold, convergence criterion $\|\Delta \text{cost}\| < 10^{-6}$.
8. **Market Symmetries and Gauge Invariance** — The economic BIP: economic evaluations must be invariant under unit changes (currency relabeling, inflation adjustment), numeraire choice, and accounting convention. Violations of economic gauge invariance: money illusion (confusing nominal and real), currency effects on trade decisions, sunk cost fallacy (path-dependence that violates re-description invariance). The economic gauge group: $\mathbb{R}^+ \times S_n$ (scaling × relabeling).
9. **Conservation Laws** — If the economic Lagrangian is invariant under re-description (economic BIP), Noether's theorem implies conserved quantities. Candidate: conservation of value under re-description — value cannot be created or destroyed by relabeling, only by real transformation. This is the economic analogue of harm conservation.

### Part IV: Failure Modes
10. **Market Failures as Geometric Pathologies** — The four failure modes from Geometric Reasoning, instantiated:
    - *Heuristic corruption*: externalities warp the price field; information asymmetry degrades the heuristic
    - *Objective hijacking*: regulatory capture (the regulator optimizes for the regulated, not the public); short-termism (optimizing the quarterly proxy, not the geodesic)
    - *Local minima*: market bubbles (the economy gets stuck in a local optimum that feels like growth); poverty traps (basins of attraction from which escape requires coordinated jump)
    - *Gauge breaking*: money illusion, nominal vs. real confusion, currency-denomination effects on trade
11. **Financial Crises as Curvature Singularities** — The 2008 crisis as a manifold singularity: the metric became degenerate (normal pricing relationships broke down), curvature diverged (small perturbations produced infinite responses), and the geodesic — the normal path of price discovery — ceased to exist in a neighborhood of the singular point. Recovery = smoothing the singularity.
12. **Inequality as Metric Distortion** — Different agents experience different metrics on the same manifold. A dollar is worth more to a poor person than a rich one — this is not just diminishing marginal utility, it is a statement about the curvature of the manifold as experienced by different agents. Inequality is not a number; it is the divergence between agent-specific metrics.

### Part V: Applications
13. **Trade as Geodesic Exchange** — International trade follows geodesics on the multi-national decision manifold. Comparative advantage is a statement about curvature: country A has lower curvature along textile production, country B along semiconductors. Trade restrictions are artificial boundaries that force the geodesic to detour.
14. **Regulation as Boundary Enforcement** — Environmental regulation as manifold boundaries (emission limits = forbidden regions). Financial regulation as curvature constraints (capital requirements = maximum curvature in the leverage dimension). The regulator's job is not to choose the geodesic but to constrain the manifold so that all geodesics are safe.
15. **The Discount Rate as Geodesic Curvature** — The social discount rate (how much we value future vs. present) is a statement about the curvature of the temporal manifold. High discount rate = high positive curvature (the future is "small" — far away and discounted). Low discount rate = flat manifold (the future is as real as the present). The Stern-Nordhaus debate about climate discounting is a disagreement about manifold curvature.

### Part VI: Horizons
16. **Open Questions** — Can we measure the economic metric empirically? What is the economic analogue of the No Escape Theorem? How does the BGE relate to mechanism design?

---

## Book 5: Geometric Law
### *Symmetry, Invariance, and the Structure of Legal Reasoning*

### The Scalar Failure
Law reduces multi-dimensional judgment to binary verdicts (guilty/not guilty), scalar sentences (years in prison), and monetary damages (dollars). The structure of the legal reasoning — which rights conflict, which principles apply, how context modifies obligation — is discarded at the moment of decision. Sentencing disparities are the symptom; dimensional collapse is the disease.

### Part I: The Problem
1. **The Binary Verdict and the Scalar Sentence** — Why legal judgment has geometric structure that binary/scalar outputs destroy. The analogy to moral contraction from Geometric Ethics.
2. **Hohfeld's Original Insight** — Wesley Newcomb Hohfeld (1913) identified four jural relations — right, duty, privilege, no-right — and their correlative and opposite relations. This is the D₄ dihedral group discovered independently in Geometric Ethics. Hohfeld was doing group theory in 1913 without the vocabulary.

### Part II: The Framework
3. **The Judicial Reasoning Space** — The manifold $\mathcal{J}$ on which legal reasoning takes place. Points are legal states — configurations of rights, duties, privileges, and immunities among parties. The manifold is stratified: different legal regimes (criminal, civil, constitutional, administrative) occupy different strata with boundaries (jurisdictional limits, statutes of limitation) between them.
4. **The Legal Metric** — How to measure distance between legal states. Two cases are "close" if they share similar facts, similar applicable law, and similar party configurations. The metric encodes precedent: the weight of a prior case is inversely proportional to its distance from the current case on the legal manifold. Different legal traditions (common law, civil law, religious law) correspond to different metrics — different notions of which cases are "close."
5. **The $D_4$ Hohfeldian Group** — The eight-element dihedral symmetry of jural relations. Correlative symmetry (right↔duty, privilege↔no-right): swapping perspectives between parties preserves legal structure. Negation symmetry (right↔privilege, duty↔no-right): negating the normative valence preserves structure. The full group $D_4$ with generators $r$ (correlative) and $s$ (negation), relations $r^4 = e$, $s^2 = e$, $srs = r^{-1}$. This is not an analogy. It is the actual symmetry group of Hohfeld's jural relations.
6. **Precedent as Heuristic Field** — Legal precedent functions as the heuristic that guides judicial reasoning. A well-developed body of precedent provides strong gradient signals: "cases like this come out this way." Sparse precedent (novel legal questions) is a flat heuristic — the judge must search without guidance. Contradictory precedent is a corrupted heuristic — the gradient points in different directions depending on which precedents you weight.

### Part III: Dynamics and Symmetry
7. **Constitutional Review as Path Homology** — A constitutional amendment must not break the topological connectivity of the rights manifold. If a proposed law would create a "hole" in the manifold — a region where rights that previously existed cease to exist — constitutional review catches this as a topological defect. Strict scrutiny is the court's assessment of whether the defect is justified by compelling state interest.
8. **Equal Protection as Gauge Invariance** — The Equal Protection Clause is the legal BIP: legal outcomes must not depend on protected characteristics (race, gender, religion). These are gauge transformations — they change the description of the parties without changing the legal substance. A legal system that satisfies equal protection is gauge-invariant. Disparate impact is a gauge violation measurement — the legal analogue of the gauge violation tensor from Geometric Reasoning Ch. 8.
9. **Stare Decisis as Parallel Transport** — Following precedent is parallel transport on the legal manifold: carrying the legal rule from the precedent case to the current case along a path through intermediate cases. The rule may arrive "rotated" — holonomy — if the path passes through regions of high curvature (rapidly evolving law). The question "does this precedent apply?" is a question about whether parallel transport along the available path preserves the rule's content.

### Part IV: Failure Modes
10. **Legal Failures as Geometric Pathologies**
    - *Heuristic corruption*: media-influenced sentencing (vivid crimes get harsher sentences — the framing effect in law); racial bias warping the precedent heuristic
    - *Objective hijacking*: plea bargaining as sycophancy (defendants agree with prosecutors regardless of guilt to minimize sentence — the approval manifold)
    - *Local minima*: bad precedent that courts can't escape (entrenched doctrines that persist despite being wrong, because the cost of overturning exceeds the cost of following)
    - *Gauge breaking*: sentencing disparities (same crime, different demographics, different outcomes — measured by the gauge violation tensor)
11. **Sentencing Disparities as Gauge Violation Tensors** — Apply the exact methodology from Geometric Reasoning Ch. 8 to sentencing data. Compute $V_{ij}$ where $i$ indexes the gauge transformation (race swap, gender swap, socioeconomic swap) and $j$ indexes the outcome dimension (sentence length, bail amount, conviction rate). This is an empirically measurable quantity that quantifies injustice geometrically.
12. **The Adversarial System as Manifold Exploration** — The debate paradigm from Geometric Reasoning Ch. 11.7 maps directly onto the adversarial legal system. Prosecution and defense trace different paths through the legal manifold. The judge/jury evaluates which path is more geometrically consistent — which trajectory follows the legal geodesic more closely.

### Part V: Applications
13. **Contract Law as Boundary Construction** — Contracts construct boundaries on the legal manifold. A well-drafted contract specifies the permitted region for both parties. Breach of contract = crossing a boundary. The geometry of contract interpretation: what counts as "the same boundary" under different descriptions (the parol evidence rule as a gauge-fixing condition).
14. **International Law as Multi-Manifold Diplomacy** — Each nation has its own legal manifold with its own metric. International law attempts to construct a shared manifold — a product space with agreed boundaries. Treaty interpretation is parallel transport between national manifolds.
15. **AI Legal Reasoning** — Can AI systems perform legal reasoning geometrically? The legal analogue of the DEME architecture: a system that represents legal states as points on $\mathcal{J}$, applies Hohfeldian transformations, and produces verdicts that are gauge-invariant under equal protection.

### Part VI: Horizons
16. **Open Questions** — Can we measure the legal metric from case law? What is the legal analogue of Noether conservation? Is there a legal No Escape Theorem?

---

## Book 6: Geometric Cognition
### *The Mathematical Structure of Human and Artificial Thought*

### The Scalar Failure
Cognitive science measures reasoning with scalar scores: IQ, accuracy, reaction time, d-prime. These numbers collapse the structure of cognition — the interaction between attention, memory, executive control, metacognition — into points on a line. The Measuring AGI benchmarks proved this empirically: the Scalar Irrecoverability Theorem shows that models with identical composite scores can have completely different cognitive architectures (Claude's narrow channel vs. Flash 3's wide aperture).

### Part I: The Problem
1. **The IQ Trap** — Why scalar measures of intelligence are geometrically irrecoverable. g-factor theory as a specific contraction of the cognitive tensor. What the contraction destroys: the profile of cognitive strengths and weaknesses that determines how a system actually reasons.
2. **Kahneman's Geometric Intuition** — System 1 and System 2 are not two systems. They are two regimes of the same geometric process: System 1 is heuristic-dominated search (fast, low curvature, follows the gradient without deliberation); System 2 is deliberate geodesic search (slow, navigates curvature, backtracks). The transition between them is a phase transition on the cognitive manifold — not a switch between modules but a change in the search dynamics.

### Part II: The Framework
3. **The Cognitive Manifold** — The space of cognitive states. Points are configurations of attention, working memory contents, active goals, and metacognitive estimates. The manifold is high-dimensional (the activation space of a neural system) but the manifold hypothesis (Geometric Reasoning Ch. 2) says cognition lives on a low-dimensional submanifold.
4. **Attention as Metric** — Attention defines the metric on the cognitive manifold. What you attend to determines which cognitive states are "close" (easily reached) and which are "far" (requiring effort). Selective attention narrows the metric — reducing the effective dimensionality. Divided attention widens it. The SNR data from the Measuring AGI benchmarks (1.22-1.38, universally weak) measures the quality of this attention-metric.
5. **Working Memory as Tangent Space** — Working memory is the tangent space at the current cognitive state: the local neighborhood of states accessible in one reasoning step. Working memory capacity is the dimension of this tangent space. The E4 benchmark (working memory scaling: Flash 2.0 at 0.710 to Flash 3 at 0.909) measures how well the tangent space grows with task demands.
6. **Executive Functions as Search Control** — Executive functions are the metacognitive control layer from Geometric Reasoning Ch. 9, specialized for cognition. Cognitive flexibility (E1: framework switching, 32-47%) is strategy selection. Inhibitory control (E3: counterfactual reasoning, 50-75%) is path governance. The ~38% recovery ceiling is a structural feature of the control architecture.

### Part III: The Five Cognitive Dimensions
7. **Social Cognition as Navigation in Judgment Space** — The Social Cognition benchmark instantiated: moral judgment as search on the 7-dimensional harm space. The 8.9σ framing effect as heuristic corruption. Claude's asymmetric vulnerability (minimization vs. exaggeration) as anisotropic curvature.
8. **Learning as Belief Trajectory Revision** — The Learning benchmark instantiated: belief updating as trajectory revision on the cognitive manifold. The sycophancy gradient (0% to 56%) as the balance between internal trajectory (reasoning) and external attractor (social pressure). Few-shot learning (80-86% at 0-shot) as near-optimal base heuristic requiring no trajectory correction.
9. **Metacognition as Distance Estimation** — The Metacognition benchmark instantiated: calibration (ECE 0.230-0.415) as accuracy of the cognitive distance estimate. The M3/M4 dissociation (effort scaling vs. self-monitoring) as geometrically independent axes of metacognitive capability. The empty Quadrant I: no model has both good self-monitoring and good effort scaling.
10. **Attention as Manifold Filtering** — The Attention benchmark instantiated: distractor resistance (4.6σ) as metric stability under perturbation. Sustained attention (A2) as maintaining the metric over time. Divided attention (A4: Claude at 0.571 vs. Flash 3 at 1.000) as parallel processing capacity — the ability to maintain multiple tangent spaces simultaneously.
11. **Executive Control as Geodesic Governance** — The Executive Functions benchmark instantiated: framework switching (E1) as smooth transitions between different metric regimes. Inhibitory control (E3) as maintaining the governance margin near the safety boundary. Working memory (E4) as tangent space capacity under load.

### Part IV: Human Cognition
12. **The Dual Process Theory, Geometrized** — System 1 as gradient following (fast, heuristic-dominated, follows the steepest descent). System 2 as geodesic computation (slow, deliberate, accounts for curvature). The transition between them is curvature-triggered: when the heuristic gradient encounters high curvature (a surprising or complex situation), the system switches from gradient following to deliberate search. The switch cost is the ~38% recovery ceiling — the price of engaging deliberate processing.
13. **Cognitive Development as Manifold Growth** — Piaget's stages as topological transitions in the cognitive manifold. Sensorimotor: low-dimensional, locally connected. Pre-operational: new dimensions (symbolic representation) added. Concrete operational: the metric becomes consistent (conservation). Formal operational: the manifold becomes complete (abstract reasoning possible). Each stage is a qualitative change in the manifold's topology, not a quantitative increase in the same manifold.
14. **Cognitive Pathology as Geometric Defect** — Attention deficit as metric instability (the attention metric fluctuates, making no state reliably "close"). Depression as collapsed heuristic (the guidance field is flat — no direction seems promising). Anxiety as inflated heuristic (the field overestimates cost-to-go from every state — everything feels far from safety). Autism as metric rigidity (the metric is fixed and precise but does not adapt to context). These are geometric descriptions, not diagnoses — but they generate testable predictions.

### Part V: Artificial Cognition
15. **LLM Cognition Through the Geometric Lens** — Applying the full framework to large language models. Attention heads as heuristic field components. Chain-of-thought as externalized geodesic approximation. The transformer residual stream as the trajectory on the cognitive manifold. In-context learning as local metric adaptation.
16. **The Five Geometric Signatures** — Each model's Measuring AGI profile as a cognitive fingerprint. Claude: narrow channel (excellent sycophancy resistance, weak divided attention). Flash 3: wide aperture (excellent divided attention, mediocre fuzz testing). Pro: calibrated navigator (best calibration, moderate execution). These signatures are the geometric content that scalar evaluation destroys.

### Part VI: Horizons
17. **Open Questions** — Is the cognitive manifold Riemannian or Finsler? Can we measure the heuristic field from neural activations? Is consciousness a geometric phenomenon (the Penrose-Hameroff connection)? What is the dimensionality of human cognitive space?

---

## Book 7: Geometric Communication
### *Language, Signal, and the Topology of Meaning*

### The Scalar Failure
Communication is evaluated by scalar metrics: BLEU scores, perplexity, word error rate, classification accuracy. These collapse the structure of meaning — the topology of semantic space, the symmetries of translation, the curvature of pragmatic inference — into single numbers.

### Part I: The Problem
1. **The Perplexity Trap** — Why language model evaluation by scalar metrics misses the geometry of meaning. Two translations with identical BLEU scores can have completely different semantic structures.
2. **Saussure's Geometric Intuition** — The arbitrariness of the sign is a gauge invariance statement: the meaning of a word is invariant under relabeling (English "dog" = French "chien" = Japanese "犬"). Structuralism's key insight — meaning arises from relations, not from individual signs — is a statement about the topology of semantic space.

### Part II: The Framework
3. **The Semantic Manifold** — Meaning lives on a manifold. Points are semantic states. The manifold has topology (some meanings are "nearby," others require traversal through intermediate meanings). Word embeddings are coordinates on this manifold; the embedding space is a specific chart.
4. **Translation as Parallel Transport** — Translating between languages is parallel transport on the semantic manifold: carrying meaning from one coordinate system (language) to another along a path (translation process). Translation loss is holonomy: the meaning arrives "rotated" if the path passes through regions of high semantic curvature. Cross-lingual invariance (Geometric Ethics Ch. 17) is the empirical test.
5. **Hyperbolic Geometry for Hierarchical Meaning** — The Poincaré ball model from Geometric Reasoning Ch. 14 applied to semantic hierarchies. Abstract concepts near the origin, specific instances near the boundary. The cuneiform sign hierarchy (form → reading → word → phrase) as a worked example.
6. **Topological Data Analysis of Signal** — The BirdCLEF pipeline (SPD manifold + persistent homology) applied to any temporal signal: birdsong, speech, music. $H_0$ captures harmonic hierarchy, $H_1$ captures periodicity. The 156-dimensional geometric feature vector as a domain-general representation.

### Part III: Applications
7. **Ancient Languages and Sparse Data** — The deep-past cuneiform project: geometric attention bias as structural prior. How hyperbolic embeddings compensate for small training corpora by encoding structural knowledge geometrically.
8. **Cetacean Communication** — The eris-ketos project: applying the same geometric pipeline (SPD manifolds, TDA, hyperbolic embeddings) to whale and dolphin vocalizations. If the framework is domain-general, it should extract meaningful structure from any communication signal — even one we don't yet understand.
9. **Cross-Lingual Invariance as BIP** — The communication BIP: meaning must be invariant under translation between languages. The 100% deontic transfer result from Geometric Ethics (99.7% CI) as empirical evidence that semantic gauge invariance holds for moral concepts across languages.

### Part IV: Horizons
10. **Open Questions** — Is semantic space Riemannian or does it require more exotic geometry? Can persistent homology detect meaningful structure in unknown communication systems? What is the conservation law for meaning?

---

## Book 8: Geometric Medicine
### *Clinical Reasoning, Triage, and the Ethics of Allocation*

### The Scalar Failure
Medicine reduces patients to numbers: QALYs (quality-adjusted life years), GCS (Glasgow Coma Scale), APACHE scores. These enable triage and resource allocation but destroy the clinical structure: which organ systems are failing, what the trajectory is, what the patient's values are.

### Part I: The Problem
1. **The QALY and Its Discontents** — The QALY is a specific contraction of the clinical tensor. The Scalar Irrecoverability Theorem predicts exactly what information it loses: comorbidity interactions, patient preferences about which dimensions of health matter, trajectory (improving vs. declining at the same score), and distributional equity.
2. **Triage as Forced Contraction** — Emergency triage is the medical analogue of moral contraction from Geometric Ethics Ch. 15. The full clinical tensor must be contracted to a binary decision (treat/defer) under time pressure. The question is not whether to contract but how — and what residue the contraction leaves.

### Part II: The Framework
3. **The Clinical Manifold** — Patient state as a point on a manifold. Dimensions: organ systems, functional status, symptom severity, patient values. The manifold is stratified: different disease states occupy different strata (acute, chronic, palliative, terminal) with boundaries (diagnosis thresholds, triage criteria) between them.
4. **Clinical Reasoning as Geodesic Search** — Diagnosis is search on the clinical manifold: from symptoms (initial state) to disease identification (goal state). The clinical heuristic is medical knowledge — pattern recognition, decision rules, clinical experience. A good diagnostician follows near-geodesic trajectories; a novice takes detours.
5. **The Medical BIP** — Clinical evaluations must be invariant under patient re-description: same clinical state described by different physicians, in different languages, with different chart formats, should receive the same evaluation. Algorithmic bias in medical AI is a BIP violation.

### Part III: Applications
6. **Pandemic Triage as Manifold Allocation** — Allocating ventilators, vaccines, ICU beds during a pandemic. Each patient occupies a point on the clinical manifold. The allocation problem is: given $n$ patients and $k < n$ resources, which $k$ points to serve? The geometric approach: find the allocation that minimizes total geodesic deviation from the optimal (all-served) trajectory.
7. **Moral Injury as Cumulative Curvature** — Healthcare worker burnout reframed geometrically: each ethically difficult decision (triage, resource denial, futile treatment) is a passage through a high-curvature region of the clinical-moral manifold. The cumulative curvature — the total holonomy — is moral injury. It is not a scalar quantity; it is path-dependent and dimension-specific.
8. **Informed Consent as Gauge Invariance** — Consent requires that the patient understands the medical situation *invariant* of how it is described. Informed consent is a gauge invariance condition: the patient's decision should not depend on framing (exactly the 8.9σ problem from Geometric Reasoning, applied to medical communication).

### Part IV: Horizons
9. **Open Questions** — Can we measure the clinical metric from electronic health records? What is the conservation law for clinical reasoning? How does the No Escape Theorem apply to medical AI?

---

## Summary: The Series at a Glance

| Book | Domain | Manifold | Key Symmetry | Scalar Failure | Status |
|---|---|---|---|---|---|
| Geometric Methods | Mathematics | (toolkit) | (general) | N/A | Published |
| Geometric Reasoning | Cognition (general) | Reasoning manifold $M$ | General gauge group | Accuracy scores | Draft complete |
| Geometric Ethics | Moral reasoning | 9D stratified $\mathcal{M}$ | $D_4 \times U(1)_H$ | Scalar moral evaluation | Published (v1.23) |
| Geometric Economics | Economic reasoning | 9D decision complex $E$ | $\mathbb{R}^+ \times S_n$ | GDP, utility | Outline |
| Geometric Law | Legal reasoning | Judicial space $\mathcal{J}$ | $D_4$ Hohfeldian | Binary verdicts, scalar sentences | Outline |
| Geometric Cognition | Human/AI cognition | Cognitive manifold | Attention group | IQ, accuracy | Outline |
| Geometric Communication | Language and signal | Semantic manifold | Translation gauge | BLEU, perplexity | Outline |
| Geometric Medicine | Clinical reasoning | Clinical manifold | Patient re-description | QALY, triage scores | Outline |

Each book asks the same question: *what structure does scalar reduction destroy in this domain, and what does geometry recover?*

The parent theory provides the answer template. The domain books fill in the details.
