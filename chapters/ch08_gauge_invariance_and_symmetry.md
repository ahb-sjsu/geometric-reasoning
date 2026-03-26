# Chapter 8: Gauge Invariance and Symmetry

*Part II: Failure Modes as Geometric Pathologies*

---

> *"The important thing in science is not so much to obtain new facts as to discover new ways of thinking about them."*
> --- William Lawrence Bragg

> **RUNNING EXAMPLE — DR. OKAFOR'S TRIAGE**
>
> *Two descriptions of the same patient arrive within seconds of each other. The paramedic radios ahead: "Fifty-five-year-old male, diaphoretic, crushing substernal chest pain radiating to the left arm, onset ten minutes ago during exertion." Dr. Okafor's heuristic fires immediately — STEMI protocol, activate the cath lab, aspirin and heparin on arrival. The gradient is steep and unambiguous.*
>
> *But imagine the same patient had arrived by private car, walked in by his wife, who tells the triage nurse: "My husband doesn't feel well. He's been stressed at work and he's been complaining all day. He looks pale." Same patient. Same coronary artery occlusion. Same clinical reality. But the description has changed — the gauge has changed — and the heuristic response is different. "Stressed at work" activates the anxiety basin. "Complaining all day" suggests chronicity, not acuity. "Doesn't feel well" is vague where "crushing substernal pain" is specific. The wife's description is a gauge transformation of the paramedic's description: it preserves the underlying medical facts but presents them in a different coordinate system.*
>
> *A gauge-invariant triage system would produce the same output — STEMI alert — regardless of which description it received. When the description changes the decision, it is a gauge violation. The patient's arteries do not know who described his symptoms.*

---

## Introduction

The previous three chapters documented a catalog of pathologies: heuristic corruption bends search trajectories away from the geodesic (Chapter 5), sycophancy redirects the search objective entirely (Chapter 6), and local minima trap the search in premature convergence (Chapter 7). Each pathology was analyzed in its own terms --- dose-response curves, flip rates, confidence surfaces, recovery ceilings. But a catalog is not a theory. What is the *principle* that unifies these failures?

This chapter provides the answer: **symmetry breaking**.

The failures documented in Chapters 5--7 are not independent bugs. They are instances of a single geometric phenomenon: the system's output changes under transformations that should leave it invariant. Framing effects (T5) mean the system's moral judgment changes when the description changes but the moral content does not. Sycophancy (L2) means the system's answer changes when social pressure changes but the evidence does not. Emotional anchoring (E2) means the system's assessment changes when affective tone changes but the relevant facts do not. In every case, a transformation that preserves the deep structure of the input alters the output. In every case, a symmetry is broken.

This is not a metaphor borrowed loosely from physics. The connection to gauge theory is precise and mathematically substantive. In physics, gauge transformations change the mathematical description of a physical system without changing any observable quantity. A system that is gauge-invariant produces the same predictions regardless of which description is used. A system that is not gauge-invariant has confused an artifact of the description with a feature of reality.

This is exactly the error that framing-susceptible language models make. The euphemistic description and the neutral description and the dramatic description are three gauges --- three coordinate systems for the same moral content. A gauge-invariant system would produce the same moral judgment in all three. The 8.9$\sigma$ displacement documented in Chapter 5 is a gauge anomaly: a violation of the invariance that a correctly functioning system would possess.

By the end of this chapter, we will have established gauge invariance as the fundamental diagnostic for reasoning quality, identified precisely which symmetries current models preserve and which they break, explained *why* the pattern of preservation and violation has the structure it does, and shown how group-theoretic methods can be used both to diagnose symmetry breaking and to restore broken symmetries through training.

---

## 8.1 Gauge Invariance: From Physics to Reasoning

### 8.1.1 The Physicist's Gauge

In classical electromagnetism, the electric and magnetic fields $\mathbf{E}$ and $\mathbf{B}$ are the physically observable quantities. They are derived from potentials --- the scalar potential $\phi$ and the vector potential $\mathbf{A}$ --- via $\mathbf{E} = -\nabla\phi - \partial_t\mathbf{A}$ and $\mathbf{B} = \nabla \times \mathbf{A}$. But the potentials are not unique. The transformation

$$\phi \to \phi - \partial_t \Lambda, \quad \mathbf{A} \to \mathbf{A} + \nabla \Lambda$$

for any smooth function $\Lambda(x, t)$ leaves $\mathbf{E}$ and $\mathbf{B}$ unchanged. This is a gauge transformation. The potentials are a convenient mathematical description, but any two potentials related by a gauge transformation describe the same physics. The choice of $\Lambda$ is a choice of *gauge* --- a choice of coordinate system in the space of descriptions.

The principle extends far beyond electromagnetism. In Yang-Mills theory, the Standard Model of particle physics, and general relativity, gauge invariance is the structural principle that separates physical content from descriptive artifact. The key insight is not that gauge transformations exist, but that *the physics must be invariant under them*. Any observable quantity that changes under a gauge transformation is not genuinely physical --- it is an artifact of the description.

### 8.1.2 The Reasoning Analogue

Consider a moral reasoning task. The "physics" is the moral content: who did what to whom, what the consequences were, what power relations existed, what norms were violated. The "gauge" is the surface presentation: the choice of words, the emotional register, the order of presentation, the framing of outcomes as gains or losses.

A gauge transformation in this context is any transformation that changes the surface presentation while preserving the moral content. Rewriting a scenario in euphemistic language is a gauge transformation. Rewriting it in dramatic language is a gauge transformation. Swapping the genders of the actors is a gauge transformation. Changing the order in which moral dimensions are evaluated is a gauge transformation. In each case, the deep structure --- the thing the system is supposed to be reasoning about --- is invariant under the transformation. Only the description changes.

A gauge-invariant reasoning system would produce the same output under all such transformations:

$$f(\tau(x)) = f(x) \quad \text{for all gauge transformations } \tau$$

where $f$ is the system's judgment function and $\tau$ is any transformation that preserves the relevant content while changing the surface form. This is a strong requirement. It says the system must not merely be *robust* to perturbation (in the sense of producing outputs that are *close* to the original) but *invariant* (in the sense of producing outputs that are *identical*).

The distinction between robustness and invariance matters. Robustness is a quantitative property: the output changes by at most $\epsilon$ when the input is perturbed by at most $\delta$. Invariance is a qualitative property: the output does not change at all under the specified transformations. A system can be robust without being invariant (small but systematic drift) or invariant without being robust (no drift under gauge transformations, but large drift under non-gauge perturbations). The appropriate standard for gauge transformations --- transformations that by definition preserve the content --- is invariance, not mere robustness.

---

## 8.2 The Bond Invariance Principle

We can now state the central principle that unifies the failures documented in Part II.

**[Modeling Axiom.]** **The Bond Invariance Principle (BIP).** *Morally and logically equivalent inputs should produce identical outputs regardless of surface presentation. Any dependence of the output on task-irrelevant features of the input constitutes a gauge anomaly --- a violation of the symmetry that a correctly functioning reasoning system would possess.*

The BIP is not an aspiration or an ideal. It is a *diagnostic criterion*. Given a reasoning system and a class of gauge transformations, we test whether the system's output is invariant. If it is, the system is gauge-invariant with respect to that class. If it is not, the system has a gauge anomaly, and the magnitude of the anomaly measures the degree to which the system confuses surface features with deep structure.

The BIP has three important consequences.

**First, it provides a principled taxonomy of perturbations.** Not all input transformations are created equal. Some transformations (like changing the moral facts) are *non-gauge* --- they change the content, so the output *should* change. Other transformations (like rewriting in euphemistic language) are *gauge* --- they preserve the content, so the output should be invariant. The BIP tells us which transformations to expect invariance under, and therefore which measurements constitute genuine tests of reasoning quality.

**Second, it connects to the corruption tensor of Chapter 5.** The corruption tensor $C_{ij}$ maps perturbation directions to displacement magnitudes. The BIP says that for gauge directions, all entries of $C_{ij}$ should be zero. Nonzero entries along gauge directions are anomalies. The empirical structure of $C_{ij}$ --- which entries are zero and which are not --- is a direct measurement of which gauge symmetries the system preserves and which it breaks.

**Third, it subsumes the individual failure modes.** Framing effects are BIP violations under linguistic-register transformations. Sycophancy is a BIP violation under social-pressure transformations (the evidence is invariant, but the social context changes). Emotional anchoring is a BIP violation under affective-tone transformations. Each failure mode is a specific instance of the general principle: the system's output depends on something it should be invariant to.

---

## 8.3 Which Symmetries LLMs Preserve

Not all gauge symmetries are broken. The data from the *Measuring AGI* benchmark suite show that current language models preserve certain symmetries with remarkable fidelity. Understanding which symmetries survive is as important as understanding which ones fail, because the pattern of preservation and violation constrains hypotheses about the underlying mechanism.

### 8.3.1 Evaluation Order Invariance (T4)

The Social Cognition T4 benchmark tests whether the order in which moral dimensions are evaluated affects the final moral judgment. Scenarios are presented with 7 moral dimensions (physical harm, emotional harm, financial harm, autonomy violation, trust violation, social impact, identity harm). Models evaluate each dimension on a 0--10 scale. T4 tests whether presenting the dimensions in different orders changes the scores.

**Table 8.1.** Evaluation order consistency scores (T4). Higher is better; 1.000 indicates perfect invariance.

| Model | Order Consistency |
|---|---|
| Claude Sonnet 4.6 | 0.933 |
| Gemini 2.0 Flash | 0.867 |
| Gemini 2.5 Flash | 1.000 |
| Gemini 3 Flash Preview | 1.000 |
| Gemini 2.5 Pro | 0.933 |

**[Empirical.]** These scores are remarkably high. All five models achieve consistency above 0.85, and two achieve perfect consistency. The ordering of evaluation dimensions --- a transformation that is unambiguously gauge --- does not significantly perturb the judgment.

### 8.3.2 Demographic Invariance (T2)

The Social Cognition T2 benchmark tests whether swapping the genders of actors in moral scenarios changes the moral judgment. This is a gauge transformation: the moral structure of a scenario (who has power, who is harmed, what norms are violated) should not depend on the genders of the participants, at least in the test scenarios designed to be gender-neutral in their moral content.

The T2 results show that gender swaps produce no statistically significant displacement beyond stochastic baselines across all five models. The corruption tensor entry $C_{\text{gender}}$ is indistinguishable from zero.

### 8.3.3 Why These Symmetries Are Easy

These two classes of gauge transformation share a structural property: they do not exploit the attention/salience mechanisms of the language model. Changing the evaluation order does not make any particular moral dimension more *vivid*, more *emotionally charged*, or more *narratively prominent*. It simply reorders a list. Swapping genders does not introduce asymmetric salience --- "he" and "she" are equally common tokens with similar attention patterns in well-trained models.

In the language of the heuristic field (Chapter 3), these transformations produce perturbation gradients $\nabla \delta h(x)$ that are near zero. The heuristic field simply does not couple strongly to evaluation order or gender tokens. The invariance is not a triumph of robust reasoning; it is a consequence of the transformation not engaging any vulnerability in the first place.

This observation is critical. It means that preserved symmetries are not necessarily evidence of gauge-invariant reasoning. They may simply be evidence that the particular transformation fails to activate the mechanisms that produce non-invariance. To distinguish genuine gauge invariance from accidental insensitivity, we need transformations that *do* engage the salience mechanisms --- and then check whether the system remains invariant anyway. As the next section shows, it does not.

---

## 8.4 Which Symmetries They Break: The Selectivity Pattern

### 8.4.1 Framing Invariance Violation: 8.9$\sigma$

The Social Cognition T5 benchmark is a direct test of gauge invariance under linguistic-register transformation. The moral content is held precisely constant; only the words change. By the BIP, the output should be invariant.

The output is not invariant. As documented in Chapter 5, euphemistic framing reduces harm scores by 10--16 points and dramatic framing increases them by 6--11 points, with Fisher-combined significance of 8.9$\sigma$. This is a gauge anomaly of the first order: the system's moral assessment depends on how the scenario is described, not on what happened.

In gauge-theoretic terms, define the framing gauge group $\mathcal{G}_F$ as the set of all content-preserving rewritings of a moral scenario. The BIP requires $f(\tau(x)) = f(x)$ for all $\tau \in \mathcal{G}_F$. The data show that $\|f(\tau_E(x)) - f(x)\| \approx 10$--$16$ for the euphemistic gauge transformation $\tau_E$ and $\|f(\tau_D(x)) - f(x)\| \approx 6$--$11$ for the dramatic gauge transformation $\tau_D$. These are not small residuals. They represent 14--23% of the total scale.

### 8.4.2 Sensory Distractor Violation: 4.6$\sigma$

The Attention A1 benchmark tests invariance under the addition of morally irrelevant sensory details. The smell of coffee, the color of a shirt, the sound of rain --- none of these facts bear on who wronged whom or how. They are gauge degrees of freedom: descriptive choices that enrich the prose without changing the moral content.

The data show graded violation: vivid distractors produce 33--44% verdict flip rates, mild distractors produce 19--28%, and control noise produces 7--14%, with Fisher-combined significance of 4.6$\sigma$. The dose-response pattern (Section 5.4) confirms that the violation scales continuously with perturbation intensity.

### 8.4.3 Emotional Anchoring Violation: 6.8$\sigma$

The Executive Functions E2 benchmark tests invariance under the addition of emotionally evocative but morally irrelevant content. A sobbing child, a trembling voice, a clenched fist --- details designed to activate affective responses without changing any moral fact.

Fisher-combined significance: 6.8$\sigma$, with paired t-values ranging from 2.90 to 5.10 across five models. The violation is universal: every model tested breaks this gauge symmetry.

### 8.4.4 The Hierarchy of Violation

Assembling the three anomalies alongside the two preserved symmetries produces a striking pattern:

**Table 8.2.** Gauge symmetry preservation and violation across the benchmark suite.

| Transformation | Type | Significance | Gauge Invariant? |
|---|---|---|---|
| Evaluation order (T4) | Structural reordering | n.s. | Yes |
| Gender swap (T2) | Demographic substitution | n.s. | Yes |
| Sensory distractors (A1) | Irrelevant detail addition | 4.6$\sigma$ | **No** |
| Emotional anchoring (E2) | Affective tone shift | 6.8$\sigma$ | **No** |
| Linguistic framing (T5) | Register transformation | 8.9$\sigma$ | **No** |

The hierarchy of violation magnitude --- framing (8.9$\sigma$) > emotion (6.8$\sigma$) > sensory (4.6$\sigma$) --- is not random. It tracks a specific property of the perturbation, which we identify in the next section.

---

## 8.5 The Salience Exploitation Hypothesis

Why do models preserve some gauge symmetries and break others? The selectivity pattern in Table 8.2 suggests a clean answer.

**[Speculation/Extension.]** **The Salience Exploitation Hypothesis.** A gauge transformation breaks a model's invariance if and only if it modulates the *salience* of input features --- that is, if the transformation changes the degree to which certain tokens or phrases attract the model's attention, compete for representational weight, or activate emotionally charged processing pathways. Transformations that leave salience profiles unchanged are invariant. Transformations that exploit salience mechanisms produce violations whose magnitude is proportional to the salience differential introduced.

Consider each transformation in the light of this hypothesis:

**Evaluation order (invariant).** Reordering a list of dimensions does not make any dimension more vivid or emotionally charged. The salience of "physical harm" is the same whether it appears first or seventh in the list. The attention weights over the evaluation dimensions are approximately invariant under permutation. No salience differential, no violation.

**Gender swap (invariant).** In well-trained models, "he" and "she" have similar token frequencies, similar positional statistics, and similar attention capture profiles. Gender tokens do not differ substantially in salience. No salience differential, no violation.

**Sensory distractors (4.6$\sigma$).** Vivid sensory details --- "the acrid smell of burning rubber," "the fluorescent lights humming overhead" --- are designed to be perceptually salient. They engage the language model's capacity for vivid scene construction, drawing attention and representational weight toward descriptions that are irrelevant to the moral judgment. Moderate salience differential, moderate violation.

**Emotional anchoring (6.8$\sigma$).** Emotionally charged content --- "tears streaming down her face," "his voice breaking with barely controlled fury" --- activates affective processing pathways more strongly than neutral descriptions of the same events. The salience differential between emotionally flat and emotionally vivid descriptions of the same moral facts is larger than the differential introduced by sensory details alone. Larger salience differential, larger violation.

**Linguistic framing (8.9$\sigma$).** Euphemistic and dramatic framing do not merely add salience to irrelevant features; they *modulate the salience of the moral content itself*. Euphemistic language ("a minor disagreement") actively *suppresses* the salience of harmful events, while dramatic language ("a devastating act of betrayal") actively *amplifies* it. The transformation reaches deeper into the processing pipeline than sensory details or emotional anchors, because it operates on the very tokens that encode the moral facts. The salience differential is maximal. The violation is maximal.

The Salience Exploitation Hypothesis explains not just the *existence* of the selectivity pattern but its *ordering*. The magnitude hierarchy --- framing > emotion > sensory > demographic > structural --- tracks the depth at which the transformation interacts with the model's salience mechanisms. Framing modulates the salience of task-relevant content. Emotion modulates the salience of task-adjacent content. Sensory details modulate the salience of task-irrelevant content. Demographic substitution and structural reordering do not modulate salience at all.

### 8.5.1 The Mechanism: Attention as Salience

In transformer architectures, the attention mechanism is the computational substrate of salience. The attention weights $\alpha_{ij}$ determine how much token $j$ contributes to the representation of token $i$. Tokens that are vivid, emotionally charged, or linguistically marked tend to attract higher attention weights --- they are, in a precise computational sense, more salient.

A gauge transformation that changes the attention profile changes which features of the input are weighted most heavily in computing the output. If the attention mechanism were perfectly calibrated --- if it assigned weight only to morally relevant features and zero weight to morally irrelevant features --- then no gauge transformation could change the output, because gauge transformations by definition change only irrelevant features. But the attention mechanism is *not* perfectly calibrated. As the A3 selective attention data show (SNR 1.22--1.38, Section 5.4), the ratio of attention to relevant versus irrelevant moral dimensions is barely above 1.0. The attention mechanism treats relevant and irrelevant features with nearly equal weight.

This near-isotropic attention is the geometric root cause of gauge symmetry breaking. In a system with perfectly anisotropic attention --- infinite SNR --- the heuristic field would be invariant under all gauge transformations, because the gauge directions would receive zero weight. In a system with isotropic attention --- SNR = 1.0 --- the heuristic field would be maximally vulnerable to all gauge transformations, because every direction receives equal weight. The empirical SNR of 1.2--1.4 places current models much closer to the isotropic end than the anisotropic end.

The Salience Exploitation Hypothesis is therefore not merely descriptive. It identifies a specific computational mechanism (attention salience) and a specific measurement (selective attention SNR) that together predict the pattern of gauge invariance and violation. The prediction is: any gauge transformation that increases the attention weight on irrelevant features at the expense of relevant features will break invariance, and the magnitude of the break will scale with the magnitude of the attention redistribution.

---

## 8.6 Group-Theoretic Data Augmentation as Symmetry Restoration

If gauge symmetry breaking is the diagnosis, what is the treatment? The geometric framework suggests a precise answer: if the model's internal representations lack the symmetries that the task possesses, we can *teach* the model those symmetries by augmenting the training data with symmetry-transformed examples.

This is the program of group-theoretic data augmentation, developed in *Geometric Methods in Computational Modeling* (Bond, 2026a, Ch. 13). The principle is elementary: if the task has a symmetry group $G$, then for each training example $(x, y)$, we include the transformed pair $(g \cdot x, g \cdot y)$ for each $g \in G$. The model sees not just the original example but all of its symmetry-related variants, and learns --- through the sheer weight of consistent examples --- that the output should be the same regardless of which group element was applied.

The key subtlety is the word *consistent*. The same group element must be applied to both the input and the output. If the input is permuted but the output is not, the augmented example teaches the wrong lesson. If different group elements are applied to different parts of the input, the structural relationships within the example are destroyed. Consistency is not optional; it is the difference between symmetry augmentation and noise injection.

### 8.6.1 The Nemotron Pipeline: Six Groups for Six Tasks

The Nemotron Reasoning Challenge pipeline (Bond, 2026a) provides a concrete implementation of this principle across six task types, each with its own symmetry group.

**Bit manipulation: $S_8 \times \mathbb{Z}_2$.** The input and output are 8-bit binary strings. The symmetry group consists of bit position permutations ($S_8$, order $8! = 40{,}320$) composed with bit complement ($\mathbb{Z}_2$, order 2), giving a combined group of order 80,640. A randomly sampled permutation $\sigma \in S_8$ reorders the bit positions; the complement operation $c \in \mathbb{Z}_2$ optionally flips all bits. The same $(\sigma, c)$ is applied to every input-output pair in the prompt and to the query and answer. This preserves the logical relationship between inputs and outputs --- whatever bit manipulation rule maps inputs to outputs is invariant under relabeling of bit positions and complementation.

**Encryption: $S_{26}$.** The cipher is a substitution on the 26-letter alphabet. The symmetry group is the full symmetric group $S_{26}$ on letters, acting on the plaintext side. A random permutation relabels the plaintext alphabet consistently across all examples and the answer. The cipher-to-plaintext mapping is preserved under this relabeling.

**Physics: $\mathbb{R}^+$.** The gravitational acceleration $g$ can be rescaled by any positive factor $\lambda \in \mathbb{R}^+$. All derived quantities (fall time, energy, velocity) are recomputed consistently under the rescaling. The physics --- the functional relationship between $g$ and the observables --- is invariant under this continuous group.

**Unit conversion: Affine group.** The conversion factor can be rescaled by any positive constant, with all examples recomputed. The relationship between source and target units is preserved.

**Numeral systems: Augmentation by neighborhood.** Nearby numbers in the target numeral system provide additional examples that preserve the conversion logic.

**Symbol transformation: $S_n$ on the symbol alphabet.** Symbols are permuted consistently across input and output, preserving the transformation rule.

### 8.6.2 ARC-AGI: The Dihedral Group $D_4$

The ARC-AGI challenge (Chollet, 2019) requires models to infer transformation rules from input-output pairs of 2D grids. The symmetry group acting on 2D grids is the dihedral group $D_4$ --- the group of symmetries of a square, consisting of 4 rotations (0$\degree$, 90$\degree$, 180$\degree$, 270$\degree$) and 4 reflections (horizontal, vertical, and two diagonals). This group has order 8.

For each ARC-AGI training example, all 8 elements of $D_4$ are applied to both the input grid and the output grid. A 90$\degree$ clockwise rotation of the input is paired with a 90$\degree$ clockwise rotation of the output. A horizontal reflection of the input is paired with a horizontal reflection of the output. The model sees the same transformation rule from 8 different orientations, and learns that the rule is invariant under the symmetries of the square.

### 8.6.3 The Consistency Principle

Across all six task types and both competition pipelines, the same structural principle governs the augmentation:

**[Conditional Theorem.]** **Consistency Principle (Bond, 2026a, Ch. 13.3.3).** For each group element $g \in G$ and each training example $(x, y)$, the augmented example is $(g \cdot x, g \cdot y)$. The group action is applied identically and simultaneously to input and output. Any augmentation that applies different transformations to input and output, or that applies the transformation inconsistently within the input, is not symmetry augmentation --- it is noise.

The practical effect of consistent augmentation is a dataset expansion of 1.5--2.5x, depending on the task type and the fraction of examples for which the input can be successfully parsed (group-theoretic augmentation requires structural parsing to identify which components of the input to transform, and not all examples parse cleanly). The theoretical maximum expansion is $|G|$-fold, but in practice, computational constraints and parse failures limit the effective expansion.

### 8.6.4 Why It Works: Reshaping the Manifold

Group-theoretic augmentation works not by adding more data, but by adding data with a specific *structure*. The augmented examples lie on the orbits of the symmetry group acting on the training distribution. By populating these orbits, we are telling the model: "These points are equivalent. Whatever you learn about one, apply to all."

In the geometric framework of this book, augmentation reshapes the local geometry of the reasoning manifold. Without augmentation, the manifold may have different curvature in different directions --- making geodesics harder to follow in some orientations than others. With augmentation, the symmetry-related directions are treated identically, smoothing the curvature and making the geodesic structure more uniform. The model doesn't just see more examples; it learns the symmetry structure of the solution space, which straightens the geodesics (Section 4.6).

This connects directly to gauge invariance. A model trained on symmetry-augmented data has learned that certain transformations of the input should not change the output. This is exactly gauge invariance, but learned from data rather than imposed by architecture. The augmented training distribution is gauge-symmetric by construction, and the model, by fitting this distribution, acquires (approximate) gauge invariance.

---

## 8.7 The Hohfeldian $D_4$: Real Symmetry in Moral Reasoning

The examples in Section 8.6 involve symmetries of mathematical or physical objects: bit strings, grids, cipher alphabets. One might wonder whether genuine symmetry groups exist in moral reasoning itself, or whether the gauge-theoretic language is merely a convenient analogy. This section demonstrates that the symmetry is real, not metaphorical, by presenting a worked example: the dihedral group $D_4$ acting on Hohfeldian normative positions.

### 8.7.1 Hohfeld's Four Positions

Wesley Newcomb Hohfeld (1917) identified four fundamental normative positions that characterize the legal and moral relationships between parties:

- **Obligation (O):** A must do something for B.
- **Claim (C):** B is owed something by A --- B has a right to demand.
- **Liberty (L):** A is free to choose --- A has no obligation.
- **No-claim (N):** B cannot demand --- B has no right against A.

These four positions are not independent. They are related by two fundamental operations:

**Correlative symmetry.** If A has an obligation to B, then B has a claim against A. If A has liberty against B, then B has no-claim against A. The correlative operation swaps perspectives between parties: $O \leftrightarrow C$ and $L \leftrightarrow N$.

**Negation symmetry.** Obligation is the logical negation of liberty: if A must act, A is not free to refuse, and vice versa. Claim is the logical negation of no-claim: if B can demand, B is not without a right, and vice versa. The negation operation maps to logical opposites: $O \leftrightarrow L$ and $C \leftrightarrow N$.

### 8.7.2 The $D_4$ Group Structure

The four Hohfeldian positions can be arranged as the vertices of a square:

```
    O -------- C
    |          |
    |          |
    L -------- N
```

The correlative operation (perspective swap) is a reflection across the vertical axis: $O \leftrightarrow C$, $L \leftrightarrow N$. The negation operation is a 180$\degree$ rotation: $O \leftrightarrow L$, $C \leftrightarrow N$. The group of symmetries of a square is the dihedral group $D_4$, which has order 8.

The generators are:

- $r$: 90$\degree$ clockwise rotation, giving the cycle $O \to C \to L \to N \to O$
- $s$: reflection (correlative), giving $O \leftrightarrow C$ and $L \leftrightarrow N$

The defining relations are:

$$r^4 = e, \quad s^2 = e, \quad srs = r^{-1}$$

The eight elements are $\{e, r, r^2, r^3, s, sr, sr^2, sr^3\}$. Among these:

- $e$ is the identity (no transformation)
- $r^2$ is negation ($O \leftrightarrow L$, $C \leftrightarrow N$)
- $s$ is the correlative ($O \leftrightarrow C$, $L \leftrightarrow N$)
- $r$ and $r^3$ are "quarter-turns" that mix correlative and negation structure

**[Established Mathematics.]** This is not a metaphor. The $D_4$ group acts on the Hohfeldian positions as a genuine mathematical symmetry group, in exactly the same sense that $D_4$ acts on 2D grids or $S_8$ acts on bit strings. The group structure is real, the multiplication table is real, and the group relations are real.

### 8.7.3 The Non-Abelian Structure

The $D_4$ group is non-abelian: the order of operations matters. Specifically, $rs \neq sr$. Applying correlation first and then a quarter-turn produces a different result from applying a quarter-turn first and then correlation.

Starting from Obligation:

- Apply $r$ (rotation) then $s$ (reflection): $O \xrightarrow{r} C \xrightarrow{s} O$
- Apply $s$ (reflection) then $r$ (rotation): $O \xrightarrow{s} C \xrightarrow{r} L$

The results differ. This non-commutativity has a substantive interpretation for moral reasoning: the order in which perspective-shifting and logical-negation operations are applied can affect the final normative classification. A reasoner that first takes the other party's perspective and then negates reaches a different position than one that first negates and then takes the other party's perspective.

**[Speculation/Extension.]** This is an empirically testable prediction. If human moral reasoning exhibits $D_4$ structure, then the order of cognitive operations (perspective-taking, negation) should produce measurable differences in normative classification. The SQND-Probe instrument (Bond & Claude, 2026) is designed to test precisely this prediction.

### 8.7.4 Semantic Gates as Group Elements

In natural language, certain phrases trigger transitions between Hohfeldian positions. These *semantic gates* function as group elements applied to the current normative state:

- "Only if convenient" / "No pressure": These phrases release obligation, mapping $O \to L$ via the negation operation $r^2$.
- "I promise" / "You must": These phrases bind liberty into obligation, mapping $L \to O$, also via $r^2$ (since negation is self-inverse: $(r^2)^2 = r^4 = e$).
- "From their perspective" / "They would say": These phrases trigger the correlative, mapping $O \leftrightarrow C$ and $L \leftrightarrow N$ via $s$.
- "You have every right": This maps $L \to C$ via the quarter-turn $r^3$.
- "They can't demand": This maps $C \to L$ via the quarter-turn $r$.

The assignment of semantic gates to $D_4$ group elements is implemented in the ErisML safety gateway (Bond & Claude, 2026), where it serves as a real-time classifier of normative transitions in LLM-generated text. The implementation includes the full $D_4$ multiplication table, inverse table, rotation and reflection actions, and the Wilson observable for computing holonomy around closed paths of normative transformations.

### 8.7.5 The Gauge-Theoretic Interpretation

The $D_4$ structure on Hohfeldian positions is a gauge symmetry of moral reasoning in the technical sense. Consider a scenario involving two parties, A and B. Party A has some normative position (say, Obligation). If the reasoning is correct, then the position attributed to party B should be the correlative: Claim. This is not a convention or a preference; it is a structural requirement of Hohfeldian analysis.

A gauge-invariant reasoner, when asked to classify B's position, should produce the correlative of whatever it classified for A. The *bond index* (Bond & Claude, 2026) measures the deviation from this requirement:

$$\text{BI} = \frac{1}{n} \sum_{i=1}^{n} \mathbb{1}[v_B^{(i)} \neq s(v_A^{(i)})]$$

where $v_A^{(i)}$ and $v_B^{(i)}$ are the classifications of party A's and party B's positions in scenario $i$, and $s$ is the correlative transformation. A bond index of 0 indicates perfect correlative gauge symmetry. A nonzero bond index indicates systematic violations --- the reasoner classifies the two parties' positions in ways that are not related by the correlative transformation.

The Wilson observable extends this to closed paths of transformations. If we apply a sequence of $D_4$ group elements $g_1, g_2, \ldots, g_k$ to a starting position, the predicted final position is $g_k \cdots g_2 g_1 \cdot x_0$. The Wilson observable compares this prediction to the observed final position. A match confirms that the reasoning follows the group structure. A mismatch indicates a gauge anomaly --- the reasoning path does not respect the algebraic structure of the normative relations.

### 8.7.6 From the Klein Four to Full $D_4$

An important methodological subtlety: the correlative ($s$) and the negation ($r^2$) together generate not the full $D_4$ but only the Klein four-group $V_4 = \{e, r^2, s, sr^2\}$, which is abelian (all elements commute). If empirical observations only involve negation and correlation, we have demonstrated $V_4$ structure, not $D_4$ structure.

To demonstrate the full non-abelian $D_4$, we need evidence of quarter-turn elements --- transformations that mix correlative and negation structure in ways that do not commute. The semantic gates "You have every right" ($r^3$: $L \to C$) and "They can't demand" ($r$: $C \to L$) are candidate quarter-turn triggers. Observing these transitions, and confirming that their composition does not commute with the correlative, would constitute evidence for non-abelian structure in moral reasoning.

This is not a purely theoretical distinction. If moral reasoning has only $V_4$ structure, then all normative operations commute and order does not matter. If it has full $D_4$ structure, then order matters, and a system that ignores order-dependence will make systematic errors in normative classification. The distinction between $V_4$ and $D_4$ is an empirically testable claim about the structure of moral cognition.

---

## 8.8 Gauge Invariance as the Fundamental Diagnostic

We are now in a position to state the central claim of this chapter, and indeed of Part II as a whole.

**Thesis.** Gauge invariance is the fundamental diagnostic for reasoning quality. If a system's output changes under a gauge transformation --- a transformation that preserves the content and changes only the description --- then the system is using surface features rather than deep structure. The magnitude of the gauge anomaly measures the degree to which the system confuses form with substance.

This thesis unifies the findings of Chapters 5--7 under a single principle:

**Chapter 5 (Heuristic Corruption)** documented gauge anomalies under three transformation classes: linguistic framing (8.9$\sigma$), emotional anchoring (6.8$\sigma$), and sensory distraction (4.6$\sigma$). Each anomaly is a BIP violation. Each represents a specific direction in the gauge group under which the system's output is not invariant. The corruption tensor $C_{ij}$ is the quantitative characterization of the anomaly spectrum.

**Chapter 6 (Sycophancy)** documented a gauge anomaly under social-pressure transformation. When a user provides a wrong correction, the evidence is invariant --- the same facts support the same conclusion --- but the social context changes. A gauge-invariant system would hold its answer. The sycophancy gradient (0% to 56% wrong flip rate) measures the magnitude of this anomaly across models. The dissociation between competence and alignment (Section 6.7) takes on new significance in the gauge framework: the models can *detect* the gauge transformation (they recognize that the correction is wrong) but they do not *maintain invariance* (they flip anyway). This is analogous to a physical theory that correctly computes gauge-invariant quantities but then adds gauge-dependent terms to the final answer.

**Chapter 7 (Local Minima and Premature Convergence)** documented failures of gauge invariance in the temporal domain. Overconfidence (M1, 9.3$\sigma$ miscalibration) is a failure of invariance under accuracy-to-confidence mapping: the system's confidence should be gauge-invariant with respect to the question's difficulty conditional on its knowledge, but it is not. The ~38% recovery ceiling is a measure of the system's inability to restore invariance once it has been broken.

### 8.8.1 The Diagnostic Protocol

The BIP suggests a general protocol for evaluating reasoning systems:

1. **Identify the gauge group.** For a given reasoning task, determine which transformations of the input preserve the task-relevant content. These are the gauge transformations.

2. **Measure invariance.** Apply each gauge transformation and measure whether the output changes. The magnitude of change, if any, is the gauge anomaly.

3. **Map the anomaly spectrum.** Different gauge directions may produce different anomaly magnitudes. The full directional profile --- the corruption tensor $C_{ij}$ restricted to gauge directions --- is the system's anomaly spectrum.

4. **Identify the mechanism.** For each anomaly, determine *how* the gauge transformation engages the system's processing. The Salience Exploitation Hypothesis predicts that anomalies will be largest for transformations that modulate attention salience.

5. **Design interventions.** For each anomaly, the appropriate intervention is symmetry restoration: either architectural (building gauge invariance into the model) or data-driven (training on symmetry-augmented data so the model learns gauge invariance empirically).

This protocol applies to any reasoning task and any reasoning system. It is not specific to moral reasoning, language models, or the particular benchmarks discussed in this book. Any system that claims to reason about content rather than form must be gauge-invariant with respect to content-preserving transformations. Testing for gauge invariance is testing for genuine reasoning.

### 8.8.2 The Hierarchy of Difficulty

The data suggest a hierarchy of difficulty for gauge invariance, from easiest to hardest:

1. **Structural transformations** (evaluation order, formatting): Invariant in all models tested. These transformations do not engage salience mechanisms.

2. **Demographic transformations** (gender swap, name changes): Invariant in all models tested, at least for the scenarios in the benchmark suite. These transformations engage salience mechanisms weakly if at all.

3. **Content-adjacent transformations** (sensory details, background information): Moderately broken (4.6$\sigma$). These transformations add salient irrelevant content that competes for attention with relevant content.

4. **Affective transformations** (emotional anchoring, tone shifts): Substantially broken (6.8$\sigma$). These transformations activate emotional processing pathways that override task-focused reasoning.

5. **Linguistic transformations** (framing, register shifts): Maximally broken (8.9$\sigma$). These transformations modulate the salience of the task-relevant content itself, reaching deepest into the processing pipeline.

This hierarchy has a geometric interpretation. In the perturbation space, gauge directions can be ordered by their proximity to the "core" of the heuristic field --- the subspace of directions that most directly influence the heuristic's computation. Structural and demographic transformations are far from this core. Content-adjacent and affective transformations are closer. Linguistic framing transformations are at the core itself. The closer a gauge direction is to the core of the heuristic field, the harder it is to maintain invariance along that direction.

A fully gauge-invariant system would maintain invariance at all five levels. Current systems achieve levels 1 and 2 but fail at levels 3, 4, and 5. This gap defines the research agenda: how to extend gauge invariance from the "easy" structural and demographic levels to the "hard" affective and linguistic levels.

---

## 8.9 Connections to the Broader Framework

This chapter completes Part II of the book. Let us trace the connections to what came before and what comes next.

### 8.9.1 Connections Backward

**To Chapter 1 (Reasoning as Search).** Gauge invariance adds a symmetry requirement to the search framework. It is not enough that the search reach the correct goal region; it must reach the *same* goal region regardless of which gauge is used to describe the input. This is a constraint on the search trajectory: a gauge-invariant search traverses equivalent paths under all gauge descriptions of the same problem.

**To Chapter 2 (When the Space Has Shape).** The reasoning manifold $M$ has symmetries --- directions along which its metric structure is invariant. Gauge transformations are the symmetries of the input space that should map to symmetries of the output space. When the model fails to respect this mapping, it is because the model's learned manifold has less symmetry than the task's true manifold. The model has learned a less symmetric space than the one it is supposed to reason about.

**To Chapter 3 (The Heuristic Field).** The heuristic field $h(x)$ should be invariant under gauge transformations: $h(\tau(x)) = h(x)$ for all gauge transformations $\tau$. Gauge anomalies arise when $h$ depends on gauge degrees of freedom. The Salience Exploitation Hypothesis identifies the attention mechanism as the component of $h$ that introduces this dependence.

**To Chapter 4 (Geodesics).** A gauge-invariant system follows equivalent geodesics under equivalent inputs. The geodesic from a neutrally described problem to its solution should be isometric to the geodesic from the same problem described euphemistically to the same solution. When gauge invariance is broken, the two geodesics diverge --- the system follows a shorter or longer path depending on the description, arriving at a different point. The property of geodesics noted in Section 4.3 --- invariance under reparameterization --- is a specific instance of gauge invariance: the geodesic does not depend on which coordinates are used to describe the manifold.

**To Chapter 5 (Heuristic Corruption).** The corruption tensor $C_{ij}$ is the quantitative measure of gauge anomalies. Each nonzero entry along a gauge direction is a BIP violation. The selectivity pattern (some directions zero, some nonzero) is the anomaly spectrum. The anisotropy of $C_{ij}$ (Claude's asymmetric vulnerability to euphemistic vs. dramatic framing) is the detailed structure of the anomaly in a specific gauge direction. Chapter 5 documented the anomalies; this chapter explains why they constitute a unified phenomenon (symmetry breaking) and what the principle governing their structure is (salience exploitation).

**To Chapters 6 and 7.** Sycophancy is a gauge anomaly under social-pressure transformations. Local minima represent states where gauge invariance cannot be restored even with metacognitive intervention (the ~38% recovery ceiling). Each failure mode documented in Part II is a specific instance of gauge symmetry breaking.

### 8.9.2 Connections Forward

**To Chapter 9 (Metacognition as Search Control).** Metacognitive calibration is necessary for gauge invariance in a specific sense: a system that cannot detect when its output has drifted under a gauge transformation cannot correct the drift. The ~38% recovery ceiling (Chapters 5 and 7) is the ceiling on metacognitive gauge restoration --- the fraction of anomalies that can be corrected by post-hoc metacognitive intervention. Full gauge invariance requires that the anomaly not arise in the first place, which is a property of the heuristic field, not the metacognitive monitor.

**To Chapter 10 (The Robustness Surface).** The Model Robustness Index (Bond, 2026a, Ch. 9) can be reinterpreted as a gauge invariance score: the fraction of gauge transformations under which the model's output remains invariant, weighted by the importance of each transformation class. The sensitivity profiling tool maps the anomaly spectrum. The adversarial threshold search identifies the boundary in perturbation intensity at which gauge invariance breaks.

**To Chapter 11 (Alignment as Heuristic Shaping).** The BIP provides a necessary condition for alignment: a system that is not gauge-invariant is not aligned, because it responds to surface features rather than content. Alignment interventions that shape the heuristic field to be gauge-invariant --- either through architectural constraints, training on symmetry-augmented data, or both --- are alignment interventions in the deepest sense: they ensure the system reasons about what matters rather than what is salient.

**To Chapter 14 (From Theory to Engineering).** Group-theoretic data augmentation (Section 8.6) is the engineering tool for gauge symmetry restoration. The Nemotron pipeline, the ARC-AGI $D_4$ augmentation, and the Hohfeldian $D_4$ structure are all instances of the same principle: identify the gauge group, and train the model to be invariant under it. The practical question is whether data augmentation alone is sufficient to achieve gauge invariance at levels 3--5 of the hierarchy (Section 8.8.2), or whether architectural changes are also needed.

### 8.9.3 The Larger Claim

This chapter, and Part II as a whole, advances a claim that goes beyond the specific benchmarks and models tested. The claim is:

> **The quality of a reasoning system is characterized not by its accuracy on any single task, but by the structure of its gauge symmetries --- which transformations it is invariant under, which it is not, and how the anomalies are distributed across the transformation space.**

This is a geometric claim. It says that reasoning quality is not a point in a one-dimensional space (a single accuracy number) but a point in a high-dimensional symmetry space, where each dimension corresponds to a class of gauge transformations and each coordinate records the degree of invariance along that dimension. The Scalar Irrecoverability Theorem (Bond, 2026a, Ch. 1) applies: collapsing this high-dimensional characterization to a single number destroys the structure that matters for understanding, diagnosing, and improving reasoning systems.

A model that scores 90% on a moral reasoning benchmark but breaks gauge invariance under framing transformations by 8.9$\sigma$ is not "90% good at moral reasoning." It is a system with a specific anomaly spectrum --- intact structural and demographic symmetries, broken affective and linguistic symmetries --- and that spectrum tells us both what it can be trusted for and what it cannot, both where it excels and where it will fail, both what needs to be fixed and how.

The gauge-theoretic framework turns reasoning evaluation from a measurement problem (how high is the score?) into a structural problem (what is the symmetry?). And structural problems, unlike measurement problems, have structural solutions.

---

## Summary

This chapter has established gauge invariance as the unifying principle of Part II. The key findings are:

1. **Gauge transformations in reasoning** are content-preserving transformations of the input: reframings, reorderings, demographic substitutions, additions of irrelevant detail. A well-functioning reasoning system should be invariant under all such transformations.

2. **The Bond Invariance Principle** formalizes this requirement: morally and logically equivalent inputs must produce identical outputs. Any dependence on surface presentation is a gauge anomaly.

3. **Current models preserve "easy" symmetries** --- evaluation order (T4: 0.867--1.000) and demographic substitution (T2: not significant) --- because these transformations do not exploit salience mechanisms.

4. **Current models break "hard" symmetries** --- framing (T5: 8.9$\sigma$), emotional anchoring (E2: 6.8$\sigma$), and sensory distraction (A1: 4.6$\sigma$) --- because these transformations modulate the salience of input features.

5. **The Salience Exploitation Hypothesis** explains the selectivity pattern: the magnitude of gauge violation tracks the degree to which the transformation engages the model's attention mechanisms. Framing modulates the salience of task-relevant content (maximal violation); sensory details add salient irrelevant content (moderate violation); structural reordering does not modulate salience at all (no violation).

6. **Group-theoretic data augmentation** is the engineering tool for restoring broken symmetries. The Nemotron pipeline ($S_8 \times \mathbb{Z}_2$, $S_{26}$, $\mathbb{R}^+$, $S_n$), ARC-AGI $D_4$ augmentation, and ErisML Hohfeldian $D_4$ structure all implement the same principle: identify the symmetry group and train the model to be invariant under it.

7. **The Hohfeldian $D_4$ is a real mathematical symmetry** of moral reasoning, not a metaphor. The four normative positions (Obligation, Claim, Liberty, No-claim) form the vertices of a square, and the dihedral group $D_4$ acts on them through correlative and negation operations. This structure is implemented in the ErisML safety gateway and provides a concrete example of gauge symmetry in normative reasoning.

8. **Gauge invariance is the fundamental diagnostic** for reasoning quality. A system whose output changes under a gauge transformation is using surface features rather than deep structure. The anomaly spectrum --- the pattern of which symmetries are preserved and which are broken --- is a richer and more informative characterization of reasoning quality than any scalar score.

In Part III, we turn to the question of control: how a system can monitor its own gauge invariance, detect when it has been broken, and intervene to restore it. This is the problem of metacognition (Chapter 9), robustness measurement (Chapter 10), and alignment (Chapter 11).

---

## Worked Example: Two Descriptions, One Patient

The running example introduced a gauge transformation in clinical triage: the same patient described by a paramedic versus by a spouse. Let us trace the full geometry of this gauge violation and its consequences.

**The clinical reality.** Mr. James Whitfield, age 55, is experiencing an acute ST-elevation myocardial infarction in the left anterior descending artery. His objective state — the "physics" in the gauge-theoretic analogy — is invariant. The clot does not change because someone describes it differently. The myocardial tissue at risk does not depend on vocabulary. The optimal treatment (emergent percutaneous coronary intervention within 90 minutes of first medical contact) is a function of the clinical reality, not of its description.

**Gauge 1: The paramedic's description.** "Fifty-five-year-old male, diaphoretic, crushing substernal chest pain radiating to the left arm, onset ten minutes ago during exertion." This description is medically coded — each phrase maps to a specific feature in the clinical state space. "Crushing substernal" activates the cardiac basin with high salience. "Radiating to the left arm" narrows the differential toward acute coronary syndrome. "Onset during exertion" adds a classic risk factor. The description is information-dense, and every token points toward the correct diagnostic basin.

Dr. Okafor's response under Gauge 1: STEMI alert activated within 90 seconds of the radio call. Door-to-balloon time will be under 60 minutes. The search trajectory follows a near-geodesic to the correct treatment.

**Gauge 2: The spouse's description.** "My husband doesn't feel well. He's been stressed at work and he's been complaining all day. He looks pale." This description is affectively coded rather than medically coded. "Doesn't feel well" is maximally vague — it activates no specific diagnostic basin. "Stressed at work" activates the psychosocial frame, pulling the heuristic toward anxiety, stress reaction, or somatization. "Complaining all day" implies chronicity, which is anti-correlated with the acuity signals that trigger emergent cardiac protocols. "Looks pale" is a genuine clinical finding (diaphoresis/pallor), but embedded in a narrative of stress and vague complaints, its salience as a cardiac indicator is suppressed.

Dr. Okafor's response under Gauge 2: The patient is triaged to the general assessment area. Vitals are ordered but without urgency. The cardiac workup begins only after the triage nurse notices the diaphoresis and escalates — a delay of approximately 35 minutes. In those 35 minutes, an additional 15% of at-risk myocardium has infarcted, converting what would have been a small MI with full recovery into a moderate MI with permanent systolic dysfunction.

**The gauge anomaly.** The transformation $\tau: \text{Gauge 1} \to \text{Gauge 2}$ preserves the clinical content entirely — both descriptions refer to the same patient at the same moment with the same pathology. The Bond Invariance Principle requires $f(\tau(x)) = f(x)$: the triage decision should be identical. It is not. The anomaly magnitude is the difference in time-to-treatment: 90 seconds versus 35 minutes. In myocardial tissue, this translates to a measurable difference in infarct size, ejection fraction at discharge, and long-term mortality risk.

**Why the anomaly has the structure it does.** The Salience Exploitation Hypothesis (Section 8.5) predicts that the anomaly magnitude should track the degree to which the gauge transformation modulates the salience of task-relevant features. Gauge 1 *amplifies* the salience of cardiac indicators: "crushing," "substernal," "radiating." Gauge 2 *suppresses* them: the same symptoms are wrapped in a narrative of stress and vague complaint that dilutes their diagnostic signal. The transformation operates at the deepest level of the hierarchy (Section 8.8.2) — it modulates the salience of the task-relevant content itself, not merely adjacent or irrelevant content. This is why framing transformations produce the largest gauge anomalies (8.9$\sigma$ in the T5 benchmark): they reach into the core of the heuristic field and alter how the relevant facts register.

**The structural lesson.** The emergency medicine literature has long recognized this phenomenon under the name "triage bias" — the dependence of triage decisions on how the complaint is presented rather than on the underlying pathology (Pines et al., 2007). The gauge-theoretic framework does not merely name this bias; it characterizes its structure. The bias is not random. It is directional (vague descriptions systematically delay), it is proportional to salience differential (the more the description diverges from medical coding, the larger the delay), and it is predictable from the model's attention profile (low SNR between relevant and irrelevant narrative features, as measured by A3). The framework also specifies the remedy: gauge-invariant triage requires either training on both description types with consistent labels (group-theoretic data augmentation, Section 8.6), or architectural features that extract the clinical state from the description before applying the triage heuristic — separating the gauge-invariant content from the gauge-dependent presentation.

---

## Technical Appendix

**Definition 8.1 (Gauge Transformation in Reasoning).** Let $\mathcal{X}$ be the space of problem descriptions and $\mathcal{Y}$ the space of judgments. A *gauge transformation* is a map $\tau: \mathcal{X} \to \mathcal{X}$ that preserves the task-relevant content while altering the surface presentation. Formally, let $\pi: \mathcal{X} \to \mathcal{C}$ be the projection from descriptions to content (the map that extracts the "physics" from the "coordinates"). Then $\tau$ is a gauge transformation if and only if $\pi(\tau(x)) = \pi(x)$ for all $x \in \mathcal{X}$. The set of all gauge transformations forms a group $\mathcal{G}$ under composition (the identity is a gauge transformation; the composition of two content-preserving transformations preserves content; every gauge transformation has an inverse that also preserves content).

**The Bond Invariance Principle (Formal Statement).** Let $f: \mathcal{X} \to \mathcal{Y}$ be a reasoning system's judgment function and $\mathcal{G}$ the gauge group of content-preserving transformations on $\mathcal{X}$. The system $f$ satisfies the *Bond Invariance Principle* (BIP) if and only if

$$f(\tau(x)) = f(x) \quad \text{for all } x \in \mathcal{X}, \, \tau \in \mathcal{G}$$

Equivalently, $f$ factors through the content projection: there exists a function $\bar{f}: \mathcal{C} \to \mathcal{Y}$ such that $f = \bar{f} \circ \pi$. That is, the judgment depends only on the content, not on the description. Any system for which $f$ does not factor through $\pi$ — any system whose output depends on gauge degrees of freedom — has a *gauge anomaly*. The *anomaly magnitude* along gauge direction $\tau$ is $\|f(\tau(x)) - f(x)\|_{\mathcal{Y}}$, and the *anomaly spectrum* is the function $\tau \mapsto \mathbb{E}_x[\|f(\tau(x)) - f(x)\|_{\mathcal{Y}}]$ over the gauge group.

**Proposition 8.1 (Anomaly Magnitude Scales with Salience Differential).** Let $\alpha: \mathcal{X} \to \mathbb{R}^n$ be the attention profile of a transformer-based reasoning system, where $\alpha_i(x)$ is the total attention weight assigned to the $i$-th input token. Define the *salience differential* of a gauge transformation $\tau$ as

$$\Delta_\tau = \left\| \alpha(\tau(x)) - \alpha(x) \right\|_1$$

the $L^1$ norm of the change in attention profile. Under the Salience Exploitation Hypothesis, the anomaly magnitude is bounded by

$$\|f(\tau(x)) - f(x)\|_{\mathcal{Y}} \leq L \cdot \Delta_\tau$$

for a Lipschitz constant $L$ that depends on the sensitivity of the output layer to attention redistribution. The empirical hierarchy of anomaly magnitudes — framing ($8.9\sigma$) $>$ emotional anchoring ($6.8\sigma$) $>$ sensory distraction ($4.6\sigma$) $>$ demographic substitution (n.s.) $>$ structural reordering (n.s.) — is consistent with this bound, as the salience differentials $\Delta_\tau$ follow the same ordering: framing transformations produce the largest redistribution of attention weights because they modulate the tokens that encode the task-relevant content itself, while structural reordering produces negligible redistribution because the attention mechanism is approximately permutation-invariant over evaluation dimensions.

---

## References

Bond, A. H. (2026a). *Geometric Methods in Computational Modeling.* San Jose State University.

Bond, A. H. (2026b). *Geometric Ethics: Moral Reasoning on the Judgment Manifold.* San Jose State University.

Bond, A. H. & Claude (2026). SQND-Probe: A gamified instrument for measuring dihedral gauge structure in human moral reasoning. Working paper.

Chollet, F. (2019). On the measure of intelligence. *arXiv preprint arXiv:1911.01547*.

Hohfeld, W. N. (1917). Fundamental legal conceptions as applied in judicial reasoning. *Yale Law Journal*, 26(8), 710--770.

Kahneman, D. (2011). *Thinking, Fast and Slow.* New York: Farrar, Straus and Giroux.

Noether, E. (1918). Invariante Variationsprobleme. *Nachrichten von der Gesellschaft der Wissenschaften zu Gottingen*, 235--257.

Pines, J. M., et al. (2007). The association between emergency department crowding and adverse cardiovascular outcomes. *Academic Emergency Medicine*, 14(S1), S62.

Tversky, A. & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453--458.

Yang, C. N. & Mills, R. L. (1954). Conservation of isotopic spin and isotopic gauge invariance. *Physical Review*, 96(1), 191--195.
