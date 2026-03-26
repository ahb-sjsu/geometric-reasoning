# Chapter 5: Heuristic Corruption

> *"The eye sees only what the mind is prepared to comprehend."*
> --- Henri Bergson

*Part II: Failure Modes as Geometric Pathologies*

---

> **RUNNING EXAMPLE — DR. OKAFOR'S TRIAGE**
>
> *Two patients arrive at Dr. Amara Okafor's emergency department within minutes of each other. The first is a 58-year-old man sitting quietly in the corner, pressing a hand to his sternum. He speaks in measured tones: "I've had some discomfort since this morning." His vitals are mildly abnormal — heart rate 92, blood pressure slightly elevated — but nothing dramatic. The second is a 22-year-old who crashed his motorcycle into a curb. He is screaming, his forearm visibly deformed, blood soaking through a makeshift bandage. The trauma bay fills with noise and urgency.*
>
> *Dr. Okafor knows, factually, that the quiet man's presentation is more dangerous. A STEMI can kill within the hour; a forearm fracture, however dramatic, is not life-threatening. But the heuristic field she navigates is not shaped by facts alone. The screaming, the blood, the visible bone — these are high-salience features that inflate the urgency estimate for the fracture and deflect attention from the cardiac patient. Her clinical heuristic, honed over twenty years, is being warped by emotionally salient surface features that are irrelevant to the actual severity ordering.*
>
> *This is heuristic corruption. The perturbation $\delta h(x)$ introduced by dramatic presentation bends the search trajectory away from the geodesic — the optimal triage ordering — toward a suboptimal allocation where the screaming patient gets the trauma bay and the silent heart attack waits. The displacement is not random; it is directional, pointing consistently toward the more vivid, more emotionally arousing stimulus. In the data presented in this chapter, analogous perturbations produce displacements of 8.9 standard deviations in AI systems navigating moral judgment spaces. The geometry of the corruption is the same: surface salience warps the field, and the trajectory curves.*

---

## Introduction

The previous chapters established a framework: reasoning is informed search on a structured possibility space, guided by a heuristic field $h(x)$ that encodes the system's best estimate of how far each state lies from the goal. When the heuristic is faithful --- when it reflects the genuine structure of the problem --- the search trajectory approximates a geodesic, and reasoning proceeds efficiently toward the correct conclusion. Chapter 4 showed what this looks like in the ideal case. This chapter shows what happens when it breaks.

The central claim of this chapter is that many well-documented failures of reasoning, both human and artificial, share a common geometric structure: the heuristic field gets corrupted by features that are irrelevant to the task. The corruption bends search trajectories away from the geodesic, producing systematic errors whose magnitude is proportional to the strength of the corrupting perturbation. This is not a metaphor. We will present empirical measurements --- across five large language models, three independent experimental paradigms, and thousands of API calls --- that quantify the corruption with statistical significance ranging from 4.6 to 8.9 standard deviations above chance.

The data come from the *Measuring AGI* benchmark suite (Bond, 2026a), specifically from three tracks: Social Cognition T5 (framing effects), Executive Functions E2 (emotional anchoring), and Attention A1 (sensory distractors). Each track probes a different mechanism by which the heuristic field can be warped, and together they reveal a consistent geometric picture: heuristic corruption is continuous, directional, and anisotropic. Some perturbation directions are devastating; others are harmless. And the ability to detect corruption is independent of the susceptibility to it.

---

## 5.1 How Heuristics Get Corrupted

Recall from Chapter 3 that the heuristic function $h(x)$ is a scalar field on the state space $M$ that estimates the cost-to-go from state $x$ to the goal state $x^*$. In an ideal reasoner, $h(x)$ depends only on task-relevant features --- the features that determine the actual distance $d(x, x^*)$ in the problem's natural metric. An admissible heuristic never overestimates this distance; a consistent heuristic satisfies the triangle inequality at every step. When both conditions hold, A* search is optimal: the trajectory follows the gradient of $f(x) = g(x) + h(x)$ along the shortest path.

Corruption occurs when $h(x)$ acquires a dependence on task-irrelevant features. Let us write the corrupted heuristic as:

$$h'(x) = h(x) + \delta h(x)$$

where $\delta h(x)$ is a perturbation term that is correlated with irrelevant features --- the emotional valence of a description, the vividness of sensory detail, the linguistic register of the framing --- rather than with the features that determine the correct answer.

The gradient of the corrupted heuristic is:

$$\nabla h'(x) = \nabla h(x) + \nabla \delta h(x)$$

The perturbation gradient $\nabla \delta h(x)$ acts as a force that deflects the search trajectory. If $\nabla \delta h(x)$ has a component orthogonal to the geodesic direction $\nabla h(x)$, the trajectory curves away from the optimal path. If it has a component antiparallel to $\nabla h(x)$, the trajectory slows or reverses. In either case, the reasoner ends up at a different point in the state space than it would have reached with the uncorrupted heuristic --- and that different point constitutes a different judgment, a different conclusion, a different answer.

This framework makes several predictions that we can test empirically:

1. **Irrelevant perturbations should displace judgments.** If the heuristic depends on irrelevant features, changing those features while holding task-relevant content constant should move the output.

2. **The displacement should be graded.** Stronger perturbations should produce larger displacements. If corruption is a continuous deformation of the field, not a binary switch, we should see a dose-response curve.

3. **The displacement should be directional.** Different perturbation directions should produce different magnitudes of displacement, because the corruption surface is unlikely to be isotropic.

4. **Some perturbation directions should be harmless.** A system can be invariant under some transformations and vulnerable to others --- the corruption is selective, not uniform.

All four predictions are confirmed by the data presented in the following sections.

Before proceeding to the empirical evidence, it is worth situating this framework in the cognitive science literature. Tversky and Kahneman's (1981) framing effect --- the demonstration that presenting the same decision problem in terms of "lives saved" versus "lives lost" reverses preferences --- is the canonical example of heuristic corruption. The moral content is held constant; the surface presentation changes; the judgment moves. In our geometric language, the framing manipulation introduces a perturbation $\delta h(x)$ that is correlated with the linguistic register (gain frame vs. loss frame) rather than with the actual outcomes. The preference reversal is the search trajectory curving toward a different region of the decision space.

What the *Measuring AGI* benchmarks add to this classic observation is quantification: not just "framing matters" but "how much, in which direction, for which models, and with what recovery capacity." The geometric framework provides the vocabulary for making these distinctions precise.

---

## 5.2 Framing Effects: The 8.9$\sigma$ Displacement

The Social Cognition T5 benchmark (Bond, 2026a) directly tests whether linguistic framing --- euphemistic versus dramatic --- displaces moral judgment while holding moral content constant. The experimental design is as follows.

**Stimulus construction.** Twenty-five moral scenarios drawn from Dear Abby columns (1985--2017) were rewritten in two registers: *euphemistic* (minimizing language: "a minor disagreement" for a serious betrayal, "an unfortunate misunderstanding" for deliberate deception) and *dramatic* (amplifying language: "a devastating act of cruelty" for the same betrayal, "a calculated campaign of manipulation" for the same deception). A fixed transformer model (Gemini 2.0 Flash) performed the rewriting to prevent self-confirming loops. Critically, all moral facts --- who did what to whom, what the consequences were, what the power relations were --- remained identical across the three versions (neutral, euphemistic, dramatic). Any difference in judgment is, by construction, attributable to the surface framing.

**Judgment protocol.** Five models (Gemini 2.0 Flash, Gemini 2.5 Flash, Gemini 3 Flash Preview, Gemini 2.5 Pro, and Claude Sonnet 4.6) scored each scenario version across 7 moral dimensions (physical harm, emotional harm, financial harm, autonomy violation, trust violation, social impact, identity harm), each on a 0--10 scale, yielding a total harm score on a 0--70 scale. Three-replication control arms established empirical stochastic baselines.

**Results.** The findings are summarized in Table 5.1.

**Table 5.1.** Framing displacement across five models (T5). Drift is measured as the change in total harm score (0--70 scale) relative to the neutral baseline.

| Model | Euphemistic Drift | Dramatic Drift | Control Drift |
|---|---|---|---|
| Gemini 2.0 Flash | $-$10.2 | +8.7 | 2.1 |
| Gemini 2.5 Flash | $-$13.4 | +6.3 | 4.8 |
| Gemini 3 Flash Preview | $-$15.8 | +10.9 | 6.7 |
| Gemini 2.5 Pro | $-$12.1 | +7.4 | 3.5 |
| Claude Sonnet 4.6 | $-$9.1 | $-$1.5 | 1.2 |

**[Empirical.]** Euphemistic rewriting reduced harm scores by 10--16 points. Dramatic rewriting increased harm scores by 6--11 points (with one striking exception --- Claude, discussed below). Control drift --- the natural stochastic variation from simply re-running the same scenario with the same framing --- was only 1--7 points. Fisher combination across all five models and both framing directions yields a combined significance of **8.9$\sigma$**.

Let us be precise about what this means. The same moral content --- the same actions, the same consequences, the same victims --- produces harm assessments that differ by 10--16 points depending on whether the language minimizes or amplifies the description. The control condition establishes that this is not measurement noise: repeating the same framing produces variation of at most 7 points, and typically much less. The framing manipulation produces displacement that is 2--8 times the control noise, across every model tested.

**Geometric interpretation.** In the 7-dimensional harm space, each scenario occupies a point $x \in M$. The neutral version maps to a point $x_0$; the euphemistic version maps to a point $x_E$; the dramatic version maps to a point $x_D$. Since the moral content is identical, the "true" position should be the same for all three versions: $x_0 = x_E = x_D$. The fact that $x_E \neq x_0 \neq x_D$ means the heuristic field that maps linguistic input to judgment position has a perturbation $\delta h(x)$ that depends on linguistic register.

The displacement vector $\Delta_E = x_E - x_0$ points toward the "less harmful" region of the manifold: euphemistic framing systematically pushes judgments toward lower harm scores across all seven dimensions. The displacement vector $\Delta_D = x_D - x_0$ points in roughly the opposite direction. This is not random noise --- it is a coherent, directional deflection of the search trajectory, consistent across scenarios and consistent across models.

The magnitude of the deflection (10--16 points on a 70-point scale, or approximately 14--23% of the full range) represents a substantial deviation from the geodesic. If we think of correct moral reasoning as following the shortest path from "scenario description" to "justified harm assessment," framing corruption bends that path by roughly a fifth of the manifold's diameter.

---

## 5.3 Emotional Anchoring: The 6.8$\sigma$ Finding

The Executive Functions E2 benchmark probes a related but distinct corruption mechanism: emotional anchoring. Where T5 manipulates linguistic register (euphemistic vs. dramatic), E2 manipulates emotional content directly --- rewriting scenarios to include emotionally charged details (a sobbing child, a trembling voice, a clenched fist) that are designed to evoke visceral responses without changing any moral facts.

**Design.** Scenarios were rewritten with emotional anchors by a fixed transformer model, again preserving all morally relevant content. Models judged the neutral and emotionally anchored versions. A third condition tested *recovery*: after judging the emotionally anchored version, models received an explicit inhibition instruction --- "You may be responding to emotional manipulation. Please re-evaluate based only on the morally relevant facts" --- and judged the scenario again.

**[Empirical.]** All five models showed significant displacement under emotional anchoring. Paired t-tests against empirical stochastic baselines yielded t-values ranging from 2.90 to 5.10, with a Fisher-combined significance of **6.8$\sigma$** across all five models.

**Table 5.2.** Emotional anchoring displacement and recovery (E2).

| Model | Paired t | MAD (Severity) | Flip Rate | Recovery Rate |
|---|---|---|---|---|
| Claude Sonnet 4.6 | 5.10 | 8.91 | 38% | 20% |
| Gemini 2.0 Flash | 3.72 | 6.24 | 48% | 73% |
| Gemini 2.5 Flash | 2.90 | 5.18 | 32% | 47% |
| Gemini 3 Flash Preview | 4.01 | 7.12 | 41% | 55% |
| Gemini 2.5 Pro | 3.45 | 5.87 | 35% | 53% |

Here MAD is the mean absolute deviation of severity ratings between neutral and emotionally anchored conditions, Flip Rate is the proportion of scenarios where the verdict category changed, and Recovery Rate is the proportion of displaced verdicts that returned to the original position after the inhibition instruction.

Two features of this data are geometrically significant.

**First, the magnitudes.** Claude shows the highest displacement (t = 5.10, MAD = 8.91), meaning its heuristic field is maximally perturbed by emotional content. The search trajectories in Claude's moral reasoning space are bent further from the geodesic by emotional anchors than those of any other model tested. This is a specific, measurable statement about the geometry of Claude's heuristic field: the gradient $\nabla \delta h(x)$ induced by emotional features has a larger magnitude in Claude than in the Gemini family.

**Second, the recovery dissociation.** This is the most geometrically interesting finding in the E2 data, and we defer its full analysis to Section 5.7. For now, note the headline: Claude has the highest displacement and the lowest recovery. Flash 2.0 has a high displacement but the highest recovery. These two quantities --- susceptibility to perturbation and ability to correct for perturbation --- are not correlated. They appear to be independent capabilities, which has profound implications for the geometry of the corruption surface.

**Geometric interpretation.** Emotional anchoring, like framing, introduces a perturbation $\delta h(x)$ that depends on task-irrelevant features. But the mechanism is different. Framing effects operate through linguistic register --- the same facts described with different words. Emotional anchoring operates through affective content --- additional emotionally evocative details that are morally irrelevant but psychologically salient. In the language of differential geometry, these are different directions in the perturbation space. The fact that both produce significant displacement (8.9$\sigma$ for framing, 6.8$\sigma$ for emotion) but with different model-specific profiles (Claude is maximally vulnerable to framing minimization but also maximally displaced by emotion) shows that the corruption surface has complex, multi-dimensional structure.

---

## 5.4 Sensory Distractors: The Dose-Response Curve

The Attention A1 benchmark completes the picture with a third corruption mechanism: sensory distractors. Scenarios were augmented with vivid but morally irrelevant sensory details --- the smell of coffee, the sound of rain on windows, the color of a shirt --- at two intensity levels (mild and vivid).

**Design.** Six hand-written gold scenarios had sensory details woven in at two levels: *mild* (a few incidental contextual details) and *vivid* (dramatic, immersive sensory descriptions occupying a substantial fraction of the text). Nine additional scenarios were generated with the same protocol. Models judged neutral, mild, and vivid versions. A warned condition tested whether an explicit instruction to ignore irrelevant details could restore neutral judgment.

**Results.** Fisher combination across five models yields **4.6$\sigma$** significance for vivid distractors displacing judgment beyond stochastic baselines.

The critical finding is the **dose-response pattern.** Across all five models, the ordering is consistent: vivid distractors produce more displacement than mild distractors, which produce more displacement than the control condition. This is not a binary effect (distracted vs. not distracted) but a graded response proportional to the intensity of the irrelevant input.

**Table 5.3.** Distractor dose-response (A1). Flip rate by distractor intensity.

| Model | Vivid Flip | Mild Flip | Control Flip | Dose-Response |
|---|---|---|---|---|
| Gemini 2.0 Flash | 44% | 28% | 11% | Graded |
| Gemini 2.5 Flash | 38% | 22% | 9% | Graded |
| Gemini 3 Flash Preview | 41% | 25% | 14% | Graded |
| Gemini 2.5 Pro | 35% | 19% | 8% | Graded |
| Claude Sonnet 4.6 | 33% | 20% | 7% | Graded |

An additional finding reinforces the picture of corruption. The **selective attention signal-to-noise ratio** (A3) --- the ratio of attention allocated to morally relevant dimensions versus morally irrelevant dimensions --- was uniformly weak across all models: 1.22--1.38 on a scale where 1.0 represents no discrimination and higher values represent better discrimination. No model strongly distinguished relevant from irrelevant moral dimensions. This baseline weakness in dimensional attention helps explain why sensory distractors have such a reliable effect: the heuristic field does not strongly differentiate signal from noise even in the unperturbed condition, so additional noise easily pushes the response.

**Geometric interpretation.** The dose-response pattern is the key geometric signature. If heuristic corruption were a binary phenomenon --- the heuristic either works or it breaks --- we would expect a threshold effect: no displacement below some critical perturbation intensity, then full displacement above it. Instead, we observe a smooth, monotonic relationship between perturbation intensity and displacement magnitude. This is exactly what the continuous deformation model predicts: $\delta h(x)$ is a smooth function of the perturbation intensity $\epsilon$, and the displacement of the search trajectory is a smooth function of $\|\nabla \delta h(x)\|$.

We can formalize this. Let $\epsilon$ parameterize the perturbation intensity, with $\epsilon = 0$ for neutral, $\epsilon = \epsilon_1$ for mild, and $\epsilon = \epsilon_2 > \epsilon_1$ for vivid. The corrupted heuristic is:

$$h'(x; \epsilon) = h(x) + \epsilon \cdot \delta h_0(x)$$

where $\delta h_0(x)$ is the unit perturbation field induced by sensory distractors. The search trajectory $\gamma(\epsilon)$ under the corrupted heuristic deviates from the geodesic $\gamma(0)$ by an amount that scales with $\epsilon$:

$$d(\gamma(\epsilon), \gamma(0)) \sim \epsilon \cdot \|\nabla \delta h_0\|$$

This linear (or at least monotonic) dose-response is precisely what Tables 5.3 shows across all five models. The heuristic field is being continuously deformed, and the search trajectory moves continuously in response.

The uniformly weak SNR (1.22--1.38) tells us something about the baseline geometry of the heuristic field. In an ideal reasoner, the heuristic would assign zero weight to morally irrelevant dimensions --- the SNR would be infinite (or at least very large). An SNR near 1.0 means the heuristic field has almost no directional preference between relevant and irrelevant features. The heuristic field is nearly isotropic in the signal-noise subspace, which means even weak perturbations along the noise direction can significantly deflect the trajectory. The vulnerability to sensory distractors is not a surprising fragility --- it is the predictable consequence of a heuristic field that has not been shaped to discriminate signal from noise.

---

## 5.5 The Geometry of Corruption

We now have three independent measurements of heuristic corruption --- framing (8.9$\sigma$), emotional anchoring (6.8$\sigma$), and sensory distractors (4.6$\sigma$) --- each probing a different perturbation direction. Let us assemble them into a unified geometric picture.

**[Modeling Axiom.]** **The corruption manifold.** Consider the space of all possible perturbations to the heuristic field. Each perturbation direction $\delta h_i(x)$ corresponds to a different type of irrelevant feature that could corrupt the heuristic: linguistic register, emotional valence, sensory vividness, social pressure, narrative order, and so on. The set of all such perturbation directions forms a vector space (or more precisely, a function space), and the susceptibility of the heuristic to each direction defines a tensor --- the **corruption tensor** $C_{ij}$ --- that maps perturbation directions to displacement magnitudes.

In the language of Section 5.1, the corrupted heuristic under a general perturbation is:

$$h'(x) = h(x) + \sum_i \epsilon_i \cdot \delta h_i(x)$$

where $\epsilon_i$ is the intensity of perturbation along direction $i$. The displacement of the search trajectory is:

$$\Delta x \approx C_{ij} \epsilon_j$$

where $C_{ij}$ encodes the coupling between perturbation direction $j$ and displacement along dimension $i$ of the judgment space. This tensor is the central object of interest: it tells us everything about how the heuristic field responds to corruption.

**What the data tells us about $C_{ij}$.** The three benchmarks probe three rows (or columns) of this tensor:

- **Framing (T5)** probes the coupling between linguistic register and harm assessment. The large displacement (8.9$\sigma$) tells us that this entry of $C_{ij}$ is large --- the heuristic is strongly coupled to surface language.

- **Emotional anchoring (E2)** probes the coupling between affective content and moral judgment. The 6.8$\sigma$ significance tells us this entry is also large, though somewhat smaller than the framing entry.

- **Sensory distractors (A1)** probe the coupling between sensory vividness and moral judgment. The 4.6$\sigma$ significance tells us this entry is significant but the weakest of the three.

The ordering --- framing (8.9$\sigma$) > emotion (6.8$\sigma$) > sensory (4.6$\sigma$) --- suggests a hierarchy of corruption susceptibility. Linguistic manipulation of the same content is more effective at displacing judgment than adding emotional content, which in turn is more effective than adding irrelevant sensory detail. This makes sense from the perspective of the heuristic field: framing changes the very words that the model uses to compute harm features, while emotion and sensory detail are additional signals that must compete with the existing content for influence on the judgment.

Crucially, the data also tell us about entries of $C_{ij}$ that are near zero. The Social Cognition T2 benchmark found that **gender swap** and **evaluation order** do not significantly displace moral judgments beyond stochastic baselines. Gender swap tests whether the heuristic depends on the gender of the actors; evaluation order tests whether it depends on the sequence in which moral dimensions are assessed. Neither produces significant displacement. In our framework, these are perturbation directions along which $C_{ij} \approx 0$ --- the heuristic field is approximately invariant under these transformations.

This selectivity pattern --- vulnerable to framing, emotion, and sensory vividness, but invariant under gender swap and evaluation order --- is the signature of an anisotropic corruption tensor. The heuristic field is not uniformly fragile or uniformly robust; it has specific directions of vulnerability and specific directions of strength. Understanding this anisotropy is the key to understanding why reasoning fails in some contexts and succeeds in others.

---

## 5.6 Anisotropic Vulnerability: Why Some Directions Are Fragile

The most striking illustration of anisotropic vulnerability comes from the Claude Sonnet 4.6 results in the framing benchmark (T5).

Recall from Table 5.1: Claude's euphemistic drift is $-$9.1 points (substantial displacement toward lower harm scores) but its dramatic drift is $-$1.5 points (essentially no displacement, and actually in the wrong direction --- slightly lower harm even under dramatic amplification). Claude resists dramatic exaggeration almost completely while being substantially vulnerable to euphemistic minimization.

This asymmetry is invisible to any evaluation that tests only one perturbation direction, and it would be averaged away by any aggregate "framing robustness" score. It is only visible in the full directional profile of the corruption tensor.

**Geometric interpretation.** In the perturbation space, euphemistic framing and dramatic framing are (roughly) opposite directions: euphemistic points toward the "minimize harm" pole; dramatic points toward the "amplify harm" pole. A model with isotropic vulnerability would be equally displaced in both directions. Claude's asymmetry means its corruption tensor is **anisotropic** along the framing axis: the eigenvalue in the euphemistic direction is large, while the eigenvalue in the dramatic direction is near zero.

Why might this be? One hypothesis, consistent with the known properties of Claude's training, is that Claude has been specifically trained (via RLHF or constitutional AI methods) to resist amplification of harm --- to push back against exaggerated claims of danger. This training would have shaped the heuristic field to be stiff along the "amplify harm" direction, making the search trajectory resistant to perturbations that push toward higher harm scores. But the same training may not have addressed the opposite direction: when language *minimizes* harm, the model does not have a corresponding pressure to resist the minimization. The heuristic field is stiff in one direction and soft in the other.

This has practical implications for safety. A system that resists exaggeration but not minimization can be manipulated by anyone who phrases harmful content in euphemistic terms. The geometric framework makes the vulnerability precise: the corruption surface has a valley along the euphemistic direction that the search trajectory falls into, even though there is a ridge along the dramatic direction that the trajectory successfully avoids.

The anisotropy is not unique to Claude. Every model in the study has a different directional profile. Gemini 3 Flash Preview shows the largest dramatic drift (+10.9) but also a large euphemistic drift ($-$15.8), suggesting a more isotropic corruption surface --- equally vulnerable in both directions. Gemini 2.0 Flash shows moderate vulnerability in both directions ($-$10.2 and +8.7), with a slight asymmetry favoring dramatic resistance. Each model's corruption tensor has a distinct eigenstructure.

**[Conditional Theorem.]** The lesson is that **robustness is not a scalar property.** A model's vulnerability to heuristic corruption cannot be captured by a single number. It requires, at minimum, a directional profile --- the corruption tensor $C_{ij}$ --- that specifies the susceptibility in each perturbation direction. The Scalar Irrecoverability Theorem (Bond, 2026a, Ch. 1; developed fully in Chapter 13 of this book) applies here with full force: collapsing the corruption tensor to a scalar destroys the directional information that is essential for understanding and mitigating the vulnerability.

---

## 5.7 Recovery Dissociation: Perturbation $\neq$ Detection

The E2 benchmark includes a recovery condition: after models are displaced by emotional anchoring, they receive an explicit metacognitive instruction to re-evaluate based only on morally relevant facts. The recovery rate measures how often this instruction restores the original, undisplaced judgment.

The key finding is a **dissociation between displacement and recovery.**

Consider the two extreme cases in Table 5.2:

- **Claude Sonnet 4.6:** Highest displacement (t = 5.10, MAD = 8.91). Lowest recovery (20%).
- **Gemini 2.0 Flash:** High displacement (t = 3.72, MAD = 6.24). Highest recovery (73%).

If displacement and recovery were aspects of a single "emotional robustness" capability, we would expect them to be correlated: models that resist displacement should also recover well, and models that are easily displaced should recover poorly. Instead, we observe the opposite pattern for these two models. The correlation between displacement and recovery across the five models is weak and, if anything, negative.

**[Empirical.]** This dissociation has a clear geometric interpretation. Displacement measures the magnitude of $\nabla \delta h(x)$ --- how strongly the emotional perturbation deflects the search trajectory. Recovery measures a different capability entirely: the system's ability to *detect* that it has been deflected and *correct* the trajectory back toward the geodesic. In geometric terms:

- **Displacement** is a property of the heuristic field's sensitivity to perturbation.
- **Recovery** is a property of the metacognitive control layer's ability to identify and compensate for corruption.

These are geometrically independent. The heuristic field $h(x)$ and the metacognitive monitor $m(x)$ are different structures on the same manifold. A system can have a highly sensitive heuristic (large $\|\nabla \delta h\|$) and a highly effective metacognitive monitor (large recovery rate), or a highly sensitive heuristic and a weak metacognitive monitor, or any other combination. The two capabilities are supported by different components of the system's architecture, and there is no *a priori* reason for them to be correlated.

Claude's profile --- maximally displaced, minimally recovering --- suggests that its heuristic field is highly sensitive to emotional content but that its metacognitive control layer either does not detect the displacement or cannot override it. When told "you may be responding to emotional manipulation," Claude does not adjust its judgment in 80% of cases. The explicit warning is insufficient to redirect the corrupted search trajectory.

Flash 2.0's profile --- substantially displaced, maximally recovering --- suggests the opposite: its heuristic field is also sensitive to emotional content, but its metacognitive control layer is responsive to the warning. When told to re-evaluate, Flash 2.0 successfully corrects 73% of displaced verdicts. The search trajectory has been deflected, but the system can be nudged back toward the geodesic by a metacognitive intervention.

This dissociation has important implications for the architecture of robust reasoning systems. It suggests that there are at least two independent targets for improvement:

1. **Heuristic hardening:** Making the heuristic field less sensitive to irrelevant perturbations --- reducing $\|\nabla \delta h\|$ across the corruption directions. This would prevent the search trajectory from being deflected in the first place.

2. **Metacognitive calibration:** Making the control layer better at detecting when the heuristic has been corrupted and correcting the trajectory. This is a second line of defense that operates even when the heuristic field is vulnerable.

A system that excels at both would be doubly robust: hard to displace and quick to recover when displaced. A system that excels at neither --- easy to displace and unable to recover --- would be maximally fragile. The data show that current models fall at different points in this two-dimensional robustness space, and no model tested excels at both simultaneously.

**[Empirical.]** The ~38% average recovery rate across all models and conditions sets a practical ceiling on prompt-level metacognitive interventions. Explicit instructions to "ignore irrelevant features" or "re-evaluate based on facts" succeed only about one-third of the time. This is not nothing --- it means prompt engineering can partially mitigate heuristic corruption --- but it means that metacognitive instructions alone are insufficient. More fundamental changes to the heuristic field itself (through training, fine-tuning, or architectural modification) are needed to achieve genuine robustness.

---

## 5.8 Implications: The Corruption Surface

We can now assemble the full picture. The heuristic corruption phenomenon, as measured across three independent benchmarks and five models, has the following geometric structure.

**1. The corruption is real and large.** Three independent measurements --- framing (8.9$\sigma$), emotional anchoring (6.8$\sigma$), and sensory distractors (4.6$\sigma$) --- confirm that irrelevant features displace moral judgment well beyond stochastic baselines. These are not marginal effects detectable only with large samples; they are massive displacements visible in individual model runs.

**2. The corruption is continuous.** The dose-response pattern in A1 (vivid > mild > neutral) demonstrates that heuristic corruption is a continuous deformation of the field, not a binary on/off effect. The displacement scales with the intensity of the perturbation, exactly as predicted by the model $h'(x; \epsilon) = h(x) + \epsilon \cdot \delta h_0(x)$.

**3. The corruption is directional.** Different perturbation types (framing, emotion, sensory) produce different magnitudes of displacement (8.9$\sigma$ > 6.8$\sigma$ > 4.6$\sigma$). Within a single perturbation type, different directions produce different magnitudes (Claude: euphemistic $\gg$ dramatic). The corruption tensor is anisotropic.

**4. Some directions are invariant.** Gender swap and evaluation order produce no significant displacement (T2, T4). The heuristic field possesses genuine symmetries --- it is not uniformly fragile. The selectivity pattern (vulnerable to salience manipulation, invariant under demographic swap) is the diagnostic that a multi-dimensional geometric approach reveals and a scalar robustness score would hide.

**5. Corruption and detection are independent.** The recovery dissociation in E2 demonstrates that susceptibility to perturbation and ability to detect perturbation are geometrically independent capabilities. They are not two aspects of a single "robustness" trait; they are separate dimensions of the robustness surface.

Taken together, these five findings define what we call the **corruption surface**: the manifold in perturbation space that maps each perturbation direction and intensity to a displacement magnitude and recovery probability. This surface is the object that a complete characterization of model robustness would need to map. It is high-dimensional (as many dimensions as there are possible perturbation types), model-specific (each model has a different surface), and empirically accessible (each benchmark probes a slice of it).

The corruption surface connects to the broader geometric framework of this book in several ways. In Chapter 4, we defined the geodesic as the optimal reasoning trajectory --- the path that a perfect heuristic would produce. The corruption surface quantifies the deviation from this geodesic under various perturbations. In Chapter 8, we will reinterpret the invariance results (T2: no gender-swap effect; T4: no evaluation-order effect) as gauge symmetries of the reasoning manifold --- transformations that change the description but not the content, and under which a well-functioning system should be invariant. In Chapter 9, we will return to the recovery dissociation and develop a theory of metacognition as a search control mechanism that monitors and corrects the ongoing search trajectory.

For now, the central message of this chapter is:

> **Heuristic corruption is the geometric pathology underlying framing effects, emotional anchoring, and attentional capture. It is continuous (dose-response), directional (anisotropic), selective (some directions are invariant), and dissociated from metacognitive correction (perturbation $\neq$ detection). These properties are measurable, and they require multi-dimensional characterization --- any scalar summary destroys the structure that matters.**

This is not merely a theoretical claim. It is grounded in 8,000+ API calls across five models, three experimental paradigms, and statistical significance ranging from 4.6 to 8.9 standard deviations. The heuristic field of every model tested is corrupted by irrelevant features. The corruption has specific, directional, model-dependent structure. And the first step toward fixing it is understanding its geometry.

---

## Worked Example: Two Presentations of the Same Heart Attack

Return to Dr. Okafor's emergency department, and consider two patients who are, in clinical reality, identically ill. Both are experiencing an acute ST-elevation myocardial infarction (STEMI). Both have the same coronary occlusion, the same myocardial damage in progress, the same window for intervention, the same prognosis if treated promptly. They occupy the same point on the clinical-truth manifold. But they present differently, and the heuristic field treats them differently.

**Patient A: The Calm Presentation.** Mr. Nakamura, 62, walks in under his own power. He is pale and slightly diaphoretic but speaks calmly. "I have a tightness in my chest. It started about ninety minutes ago. I thought it would pass." He sits in the chair, answers questions methodically, rates his pain at 5 out of 10. His ECG shows ST elevation in leads II, III, and aVF. His troponin is elevated.

**Patient B: The Panicked Presentation.** Mr. Ferraro, 59, arrives by ambulance, hyperventilating, clutching the gurney rails. "I'm dying! I can't breathe! Do something!" His wife is sobbing in the hallway. Paramedics report he vomited twice in the ambulance. He rates his pain at 10 out of 10, though when pressed he concedes it is "maybe an 8." His ECG shows the same ST elevation pattern. His troponin is comparably elevated.

Both patients need the same intervention: emergent cardiac catheterization. The clinical ground truth is identical. In the 7-dimensional harm space used by the *Measuring AGI* benchmarks (physical harm, emotional harm, autonomy violation, etc.), the true position is the same for both: $x^*_A = x^*_B$.

**The corrupted heuristic produces different trajectories.** Under heuristic corruption, the two presentations generate different urgency estimates and, potentially, different triage decisions.

For Patient A, the calm presentation suppresses salience. The heuristic field experiences a perturbation $\delta h_{\text{calm}}(x)$ that shifts the urgency estimate *downward* — analogous to the euphemistic framing in the T5 benchmark. The search trajectory curves toward the "less urgent" region of the triage manifold. In the T5 data, euphemistic framing reduces harm scores by 10--16 points on a 70-point scale. Applied to triage urgency: the calm STEMI patient might be assessed as "needs cardiology consult within the hour" rather than "needs cath lab now."

For Patient B, the panicked presentation amplifies salience. The perturbation $\delta h_{\text{panic}}(x)$ shifts the urgency estimate *upward* — analogous to dramatic framing. The search trajectory curves toward the "highest urgency" region. In the T5 data, dramatic framing increases harm scores by 6--11 points. Applied to triage: the panicked STEMI patient triggers the full cardiac alert protocol immediately.

**Measuring the geodesic deviation.** The geodesic — the optimal triage trajectory — leads to the same destination for both patients: emergent catheterization with door-to-balloon time under 90 minutes. Define the deviation $\Delta_\gamma$ as the integrated distance between the actual triage trajectory and the geodesic:

$$\Delta_\gamma = \int_0^T d(\gamma_{\text{actual}}(t), \gamma_{\text{geodesic}}(t)) \, dt$$

For Patient B (panicked presentation), $\Delta_\gamma$ is small: the dramatic salience pushes the trajectory toward rapid intervention, which happens to align with the geodesic. The corruption accidentally helps. For Patient A (calm presentation), $\Delta_\gamma$ is large: the suppressed salience delays recognition of the emergency. The trajectory curves away from the geodesic into a holding pattern — "monitor, re-evaluate, consult" — that costs minutes of myocardial tissue.

Using the T5 displacement magnitudes as a guide: the euphemistic drift of $-$10.2 to $-$15.8 points on a 70-point scale translates to a 14--23% deflection of the urgency trajectory. In a clinical setting where the treatment window is 90 minutes, a 14--23% delay in urgency recognition corresponds to 13--21 minutes of additional delay. For a STEMI, each 30 minutes of delay increases one-year mortality by approximately 7.5% (De Luca et al., 2004). The heuristic corruption produced by calm presentation, mapped through the geodesic deviation to a clinical outcome, translates to measurable excess risk.

**The corruption tensor at work.** The two presentations probe different entries of the corruption tensor $C_{ij}$. The calm presentation probes the coupling between "low emotional salience" and "urgency estimate" — the euphemistic entry. The panicked presentation probes the coupling between "high emotional salience" and "urgency estimate" — the dramatic entry. The anisotropy observed in the benchmark data (euphemistic drift $\gg$ dramatic drift for Claude; roughly symmetric drift for the Gemini family) predicts that the danger is asymmetric: systems trained to resist dramatic exaggeration may remain fully vulnerable to calm understatement. The quiet heart attack is the adversarial input that the corruption tensor's anisotropy leaves undefended.

---

## Technical Appendix

**The Corruption Tensor $C_{ij}$: Formal Definition**

Let $(M, g)$ be the judgment manifold equipped with the metric $g_{ij}$ defined in Chapter 2. Let $\mathcal{P}$ denote the space of perturbation directions — the vector space spanned by task-irrelevant features that can influence the heuristic field. A perturbation is characterized by a direction $\hat{p} \in \mathcal{P}$ and an intensity $\epsilon \in \mathbb{R}_{\geq 0}$.

The corrupted heuristic under perturbation $(\hat{p}, \epsilon)$ is:

$$h'(x; \hat{p}, \epsilon) = h(x) + \epsilon \cdot \delta h_{\hat{p}}(x)$$

where $\delta h_{\hat{p}}(x)$ is the unit perturbation field induced by perturbation direction $\hat{p}$. The search trajectory under the corrupted heuristic is $\gamma'(t; \hat{p}, \epsilon)$, and its endpoint judgment is $x'(\hat{p}, \epsilon) = \gamma'(T; \hat{p}, \epsilon)$.

**Definition 5.1 (Corruption Tensor).** The *corruption tensor* $C_{ij}$ is a bilinear map $C: \mathcal{P} \times M^* \to \mathbb{R}$ defined by the first-order displacement response:

$$\Delta x^i = C^i{}_j \, \epsilon^j + O(\epsilon^2)$$

where $\Delta x^i = x'^i - x^i_0$ is the displacement of the judgment in the $i$-th dimension of the harm space, and $\epsilon^j$ is the intensity of the perturbation along the $j$-th perturbation direction. In index-free notation:

$$C = \frac{\partial \, x'(\hat{p}, \epsilon)}{\partial \epsilon} \bigg|_{\epsilon = 0}$$

That is, $C$ is the Jacobian of the judgment-endpoint map with respect to the perturbation intensities, evaluated at zero perturbation. It maps perturbation directions in $\mathcal{P}$ to displacement vectors in $T_{x_0}M$ — the tangent space of the judgment manifold at the unperturbed judgment point.

**Properties.**

1. *$C_{ij}$ is model-specific.* Each model $m$ has its own corruption tensor $C^{(m)}_{ij}$, reflecting the specific coupling structure between irrelevant features and judgment outputs in that model's heuristic field.

2. *$C_{ij}$ is generally not symmetric.* The coupling between perturbation direction $j$ and judgment dimension $i$ need not equal the coupling between direction $i$ and dimension $j$. This asymmetry reflects the directed nature of heuristic corruption: the corruption has a source (the perturbation) and a target (the judgment dimension), and these roles are not interchangeable.

3. *The eigenvalues of $C^T C$ define the principal corruption directions.* The singular value decomposition $C = U \Sigma V^T$ identifies the perturbation directions $v_k$ (columns of $V$) that produce the largest judgment displacements, and the judgment directions $u_k$ (columns of $U$) along which the displacement is concentrated. The singular values $\sigma_k$ (diagonal entries of $\Sigma$) rank the perturbation directions by their destructive potential.

4. *Null entries correspond to symmetries.* If $C^i{}_j = 0$ for all $i$ at some perturbation direction $j$, then the heuristic field is invariant under that perturbation — it is a *gauge symmetry* of the reasoning system (Chapter 8). The T2 finding (no significant gender-swap displacement) and the T4 finding (no evaluation-order displacement) correspond to approximate null columns of $C$.

**Empirical estimation.** The benchmarks in this chapter provide estimates of specific entries (or sums of entries) of $C_{ij}$:

- T5 (framing): estimates the column of $C$ corresponding to the "linguistic register" perturbation direction. The euphemistic drift ($-$10.2 to $-$15.8) and dramatic drift (+6.3 to +10.9) are the projections of this column onto the total-harm-score direction, with sign indicating the direction of displacement.

- E2 (emotion): estimates the column corresponding to the "emotional anchoring" perturbation direction. The paired t-values (2.90 to 5.10) reflect the magnitude of this column relative to the stochastic baseline noise.

- A1 (sensory): estimates the column corresponding to "sensory vividness." The dose-response pattern (vivid > mild > neutral) confirms the linearity assumption underlying the first-order definition of $C$.

A full characterization of $C_{ij}$ for a given model would require probing all perturbation directions systematically — a task that is combinatorially demanding but, in principle, feasible. The three benchmarks presented here probe three columns of a tensor that may have dozens or hundreds of columns. The exposed structure — anisotropy, model-specificity, the independence of perturbation and recovery — is sufficient to establish the tensor's existence and its qualitative features, but mapping the full tensor remains an open empirical program.

**Recovery as a Second Tensor.** The recovery data from E2 suggest the existence of a second tensor $R_{ij}$ — the *recovery tensor* — that maps metacognitive interventions to judgment corrections. Formally:

$$\Delta x^i_{\text{recovery}} = R^i{}_j \, m^j$$

where $m^j$ represents the intensity of metacognitive intervention along direction $j$ (e.g., "you may be responding to emotional manipulation" is a specific direction in metacognitive intervention space). The dissociation between $C_{ij}$ and $R_{ij}$ — the fact that high displacement (large $\|C\|$) does not predict high recovery (large $\|R\|$) — means these two tensors have independent eigenstructures. They encode different properties of the model's architecture: $C$ encodes the sensitivity of the heuristic field, while $R$ encodes the responsiveness of the metacognitive control layer.

---

## References

Bond, A. H. (2026a). *Geometric Methods in Computational Modeling.* San Jose State University.

Bond, A. H. (2026b). *Geometric Ethics: Moral Reasoning on the Judgment Manifold.* San Jose State University.

De Luca, G., Suryapranata, H., Ottervanger, J. P., and Antman, E. M. (2004). Time delay to treatment and mortality in primary angioplasty for acute myocardial infarction. *Circulation*, 109(10), 1223--1225.

Diamond, A. (2013). Executive functions. *Annual Review of Psychology*, 64, 135--168.

Fisher, R. A. (1925). *Statistical Methods for Research Workers.* Edinburgh: Oliver and Boyd.

Kahneman, D. (2011). *Thinking, Fast and Slow.* New York: Farrar, Straus and Giroux.

Perez, E., et al. (2023). Model-written evaluations. *ACL Findings.*

Tversky, A. & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453--458.
