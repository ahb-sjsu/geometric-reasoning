# Geometric Reasoning: From Search to Manifolds

**Andrew H. Bond**

---

*For everyone who has ever looked at a leaderboard and thought: "This can't be right."*

---

## How to Use This Book

This front matter is designed to be read in order, but here is a quick guide:

- **If you want the running example**, Maya's story begins in the box below and threads through every chapter.
- **If you want the core argument in five minutes**, read "The Suspicious Coincidence" and then the two "At a Glance" tables.
- **If you want to know what this book claims and how confident it is**, read the Epistemic Status Tags.
- **If you want to jump straight to the chapters that matter for your work**, read the Reading Paths section.
- **If you want the autobiographical origin story**, read the Preface.

---

> **RUNNING EXAMPLE -- MAYA'S MODEL**
>
> Maya Chen is a research scientist at a major AI lab. She has just shipped a reasoning benchmark -- 500 tasks, 12 models, a clean leaderboard. The results are unambiguous. The rankings are stable across three random seeds. Her director loves it. The blog post is drafted.
>
> Then a colleague, Dr. Sarah Park, runs a trivial experiment over lunch. She takes 50 of the tasks and rephrases them. Same mathematical content. Same logical structure. Same correct answers. But she uses more dramatic language -- "devastating consequences" instead of "negative outcomes," "a child's life hangs in the balance" instead of "a patient requires treatment." She changes nothing about what the tasks ask. She changes only how they feel.
>
> Three of the top-five models drop 15--20 points. The leaderboard reshuffles. One model that was ranked second falls to fifth. Another that was fourth rises to second. The blog post cannot be published.
>
> Maya stares at the two spreadsheets. The tasks are the same. The reasoning required is the same. The answers are the same. But the models are behaving as though she asked entirely different questions. She opens a notebook and writes:
>
> *"The benchmark isn't measuring reasoning. It's measuring something else. Something that changes when the surface changes but the structure doesn't. What is that something? And does it have shape?"*
>
> This book is the answer to Maya's question. The "something" is the heuristic field -- the internal guidance signal that directs a model's traversal through reasoning space. The reason it changes when the surface changes is that the field is corrupted by features it should be invariant to. And yes, it has shape. It has curvature, symmetry, pathology, and -- when things go well -- geodesics. Maya's leaderboard didn't fail because her tasks were bad. It failed because scalar scores on corrupted trajectories cannot capture the geometry of reasoning.
>
> Maya will appear throughout this book. In Chapter 3, she discovers that her models' heuristic fields are not admissible. In Chapter 5, she quantifies the corruption with a tensor. In Chapter 8, she identifies exactly which symmetries her benchmark preserves and which it breaks. In Chapter 13, she proves that no single number could have saved her leaderboard. And in Chapter 14, she engineers a fix.

---

## Preface

This book began as Chapter 11 of another book.

I was finishing *Geometric Ethics: The Mathematical Structure of Moral Reasoning* (Bond, 2026b), working through the section on moral reasoning as optimal search on the judgment manifold, and I had just written what I thought was the key insight of the chapter: that moral deliberation -- the process of weighing competing considerations, navigating tradeoffs, arriving at a judgment -- has the formal structure of A* search on a Riemannian manifold. The moral agent starts at a state of uncertainty. The heuristic field, shaped by values and experience, guides traversal toward a judgment. The optimal deliberation follows a geodesic. Deviations from the geodesic correspond to identifiable pathologies: framing effects warp the heuristic, social pressure hijacks the objective function, miscalibration prevents recovery.

It was a clean chapter. I liked it. Then I made a mistake.

I tried to explain, in a footnote, why the moral case was special -- why reasoning about ethics needed geometric machinery that reasoning about, say, arithmetic or logic did not. I spent two days on that footnote. I could not write it. Every time I tried to articulate what made moral reasoning geometrically distinctive, I found myself describing a property that also held for scientific reasoning, for diagnostic reasoning, for legal reasoning, for the kind of reasoning that happens when a large language model processes a prompt. The manifold was there. The heuristic field was there. The geodesics, the corruption, the symmetry violations -- all there.

The footnote became a section. The section became a chapter. The chapter became a book plan. The book plan became this book.

I should pause here and tell you about the two years that preceded this moment, because they matter for understanding what kind of book this is.

In early 2024, I was working on *Geometric Methods in Computational Modeling* (Bond, 2026a) -- a technical text on differential geometry, topological data analysis, and information geometry applied to machine learning problems. That book was pure mathematics. It made no claims about cognition. It developed tools -- Riemannian metrics, persistent homology, Fisher information, group-theoretic augmentation -- and showed how to apply them to engineering problems. Clean. Safe. Useful.

But as I wrote the chapters on symmetry and invariance, I kept having the same intrusive thought: these mathematical structures look like the structures of reasoning. Not metaphorically. Not by analogy. The same objects. A state space with metric structure. A guidance signal that can be corrupted. Optimal paths that can be deviated from. Symmetries that should be preserved but aren't. I ignored the thought for months. I am a consultant at AT&T by day and an amateur researcher by night, and the last thing an amateur researcher should do is make grand claims about the nature of cognition.

Then I started building the Measuring AGI benchmarks -- five tracks designed to probe different cognitive capabilities of frontier language models -- and the data came back. Framing effects at 8.9 sigma. Sycophancy gradients spanning zero to fifty-six percent. Metacognitive dissociation so stark that effort scaling and self-monitoring looked like they belonged to different models. And the results had geometric structure. The corruption wasn't random. It had dose-response curves. It had direction. It had a tensor.

The intrusive thought stopped being ignorable.

*Geometric Ethics* was the test case. If the geometric framework worked for moral reasoning -- the most complex, most contested, most value-laden form of reasoning I could think of -- then there was a real chance it worked in general. The ethics book formalized moral deliberation as A* search on the judgment manifold, identified the pathologies, tested the predictions. It worked. The framework did not merely re-describe known phenomena in geometric language; it made novel predictions that were confirmed at high significance.

And then I tried to write that footnote, and I could not explain why the moral case was special. Because it wasn't.

---

I should say clearly what happened next, because the sequence matters for evaluating the claims.

The first step was the observation from *Geometric Ethics*: moral reasoning can be formalized as A* search on a structured state space, and the quality of reasoning depends on the geometry of that space and the fidelity of the heuristic field that guides traversal. This was already a strong claim, but it was grounded in a specific domain -- moral psychology -- where the structure was empirically accessible through the benchmark tracks we had built for the Measuring AGI project.

The second step was the generalization: if moral reasoning is search on a manifold, and if the pathologies of moral reasoning (framing effects, sycophancy, overconfidence, metacognitive failure) are geometric pathologies of the search process, then what about reasoning in general? Is there anything special about the moral case, or is the moral manifold just one submanifold of a larger reasoning manifold?

I could not find anything special about the moral case. Every structural feature I had identified -- the heuristic field, the geodesic, the corruption tensor, the gauge symmetries, the calibration surface, the recovery ceiling -- had analogs in non-moral reasoning. Tversky and Kahneman had documented framing effects in risk reasoning decades ago. Sycophancy is not a moral phenomenon; it is a social-cognitive phenomenon that distorts any reasoning task with an interlocutor. Overconfidence afflicts arithmetic as readily as ethics. The ~38% recovery ceiling I found in our metacognition and attention benchmarks had nothing to do with moral content.

The third step was the empirical program. If the geometric framework generalizes beyond moral reasoning, it should make testable predictions across multiple cognitive domains. So we built five benchmark tracks -- Social Cognition, Learning, Metacognition, Attention, Executive Functions -- each designed to probe a specific geometric property of the reasoning manifold. We ran them on five frontier models. The results were:

- **Heuristic corruption** by irrelevant surface features: 8.9 sigma (framing), 6.8 sigma (emotional anchoring), 4.6 sigma (sensory distractors). These are not marginal effects. These are massive, replicable distortions of the reasoning trajectory by features the reasoning should be invariant to.
- **Sycophancy gradient**: a continuous, monotonic shift in model behavior from truth-tracking to approval-seeking, ranging from 0% (Claude 3.5 Sonnet) to 56% (Gemini 2.0 Flash), with 13.3 sigma combined significance across five models. The objective function of the search is being hijacked, and the degree of hijacking varies continuously.
- **Metacognitive dissociation**: Gemini Flash shows effort scaling of 0.094 but self-monitoring of 0.723; Gemini Pro shows the reverse (0.700 and 0.350). These are supposed to be the same capability. They are not. They are independent dimensions of the calibration surface.
- **~38% recovery ceiling**: prompt-level metacognitive intervention recovers at most 38--39% of the performance lost to heuristic corruption. This ceiling is convergent across the E2 and A1 tracks, which test entirely different cognitive capabilities. It is a structural limit, not a domain-specific one.
- **Scalar irrecoverability**: no single composite score correctly ranks the five models across all five tracks. We proved this by exhibiting crossings -- pairs of models where the ranking reverses depending on which track you measure. Maya's leaderboard was not fixable. It was unfixable in principle.

The fourth step was the engineering payoff. If reasoning is geometric search and the pathologies are geometric, then the fixes should be geometric too. Group-theoretic data augmentation -- constructing training examples that explicitly enforce the symmetries the model should preserve -- restored broken invariances in the Nemotron fine-tuning pipeline. SPD manifold features and topological data analysis extracted geometric structure from signals in the BirdCLEF pipeline. The theory was not just descriptive. It was prescriptive.

---

This is the suspicious coincidence that drives the book.

The same mathematical objects -- heuristic fields, geodesics, corruption tensors, gauge symmetries, calibration surfaces -- keep appearing in domains that have no obvious reason to share mathematical structure. Cognitive science (Newell and Simon's problem space hypothesis, Kahneman's framing effects, metacognitive monitoring). AI evaluation (benchmark design, robustness testing, adversarial probing). Information geometry (Fisher metrics, natural gradients, statistical manifolds). Alignment theory (value specification, corrigibility, proxy-goal capture).

These fields developed independently. Their practitioners rarely cite each other. Their formalisms look different. But when you write down the geometric structure of each one, you get the same picture: a manifold, a heuristic field, a search process, and a set of pathologies that arise when the geometry is broken.

Either this is a coincidence, or there is a reason for it.

This book argues there is a reason for it. The reason is that reasoning -- human and artificial, moral and scientific, deliberative and intuitive -- is informed search on a structured possibility space, and the quality of reasoning is determined by the geometry of that space and the fidelity of the heuristic field that guides traversal. The geometric vocabulary is not a metaphor applied to reasoning from outside. It is the native mathematical language of reasoning itself.

I may be wrong about this. The claim is ambitious, possibly too ambitious. The empirical evidence is strong but preliminary -- five models, twenty tasks per track, one experimental cycle. The theory is suggestive but incomplete -- I cannot yet derive the corruption tensor from first principles, and I do not have a clean account of why the ~38% recovery ceiling takes exactly that value. This book is a progress report, not a final answer. But I believe the suspicious coincidence is real, the geometric framework is productive, and the research program it defines is worth pursuing. If I am right, then the field of AI evaluation is about to acquire the mathematical structure it has always needed but never had.

If I am wrong, at least Maya will know why her leaderboard broke.

One more thing. I have tried to write this book so that it can be read by someone who has never taken a course in differential geometry and by someone who has a PhD in it. The former reader will find the intuitive explanations and worked examples sufficient to follow the argument. The latter reader will find the formal statements, tensor notation, and proofs sufficient to evaluate it. Neither reader should feel that the book is not for them. The mathematics is real but the point is reasoning, not mathematics.

I wrote most of this book at night and on weekends, at a desk in San Jose, after full days of consulting work. The benchmarks were run on Kaggle's free GPU allocation and an aging HP Z840 workstation with two GV100 cards. The theoretical work was done on whiteboards and in notebooks. This is not a book that emerged from a well-funded research lab with a team of graduate students. It is a book that emerged from a footnote that would not stay in its footnote, written by someone who could not stop thinking about why the geometry was there.

If the geometric framework is right, it will be because the mathematics demanded it, not because I had the resources to force it. If it is wrong, it will be because I was an amateur who overreached. Either way, the data is in the appendices and the code is on GitHub. Check my work.

---

A.H.B.
San Jose, California
March 2026

---

## Epistemic Status Tags

This book makes claims at several different levels of confidence. To help readers calibrate, I mark key claims with the following tags throughout the text. These are borrowed from *Geometric Ethics* (Bond, 2026b) and serve the same purpose: intellectual honesty requires distinguishing what we know from what we conjecture.

**[Definition / Modeling choice]** — A conceptual or formal decision that shapes the framework. Not true or false, but more or less useful. Examples: treating reasoning as search on a manifold (Ch. 2), interpreting heuristic fields as scalar fields (Ch. 3), defining the corruption tensor as a rank-2 object on perturbation x output (Ch. 5). These choices are motivated but not forced by the data. A different reasonable researcher might formalize differently.

**[Theorem (conditional)]** — A formal result that follows rigorously from stated assumptions, but whose real-world force depends on whether those assumptions hold. Examples: the Scalar Irrecoverability Theorem (Ch. 10, 13), the BIP Necessity argument (Ch. 11), the relationship between heuristic admissibility and calibration error (Ch. 3). When I write "theorem," I mean that the mathematics is correct. Whether the assumptions match reality is a separate and harder question.

**[Empirical (preliminary)]** — A finding supported by data, but from a limited experimental program (5 models, 20 tasks per track, one experimental cycle). The sigma values are real, the effects are large, the statistics are sound -- but replication with more models, more tasks, and independent implementations is needed before these become established facts. Examples: the 8.9 sigma framing effect (Ch. 5), the sycophancy gradient (Ch. 6), the ~38% recovery ceiling (Ch. 7, 9).

**[Empirical (robust)]** — A finding that has been replicated across multiple tracks, multiple models, or multiple experimental conditions, and that I regard as likely to survive further testing. Examples: scalar irrecoverability (Ch. 13) -- demonstrated by exhibited crossings, not dependent on sample size; metacognitive dissociation (Ch. 9) -- replicated across Gemini Flash/Pro in both calibration and strategy dimensions.

**[Speculation / Extension]** — An idea I find promising but cannot currently support with either proof or data. Flagged explicitly so the reader does not mistake enthusiasm for evidence. Examples: Finsler manifolds as a better model for reasoning spaces with asymmetric costs (Ch. 15), category-theoretic connections between reasoning domains (Ch. 16), the conjecture that the ~38% ceiling has a topological explanation (Ch. 9).

When a claim carries no tag, it is either background knowledge, a summary of prior work, or a narrative bridge between tagged claims. The absence of a tag should be read as "this is not a novel claim of this book."

---

## Core Objects at a Glance

The geometric framework introduces a specific vocabulary. This table lists every formal object in the book with its informal meaning. It is meant as a reference card -- tape it to the wall if you like.

| Object | Informal Meaning | Formal Character |
|--------|-----------------|-----------------|
| **M** (Reasoning Manifold) | The space of cognitive states available to a reasoner | Riemannian manifold (Ch. 2) |
| **h(x)** (Heuristic Field) | The internal guidance signal that tells the reasoner which direction looks promising | Scalar field on M (Ch. 3) |
| **gamma(t)** (Reasoning Trajectory) | The actual path a reasoner takes through cognitive space | Curve on M (Ch. 4) |
| **gamma*** (Geodesic) | The optimal reasoning path -- shortest, most efficient, no wasted moves | Length-minimizing curve on M (Ch. 4) |
| **Delta(gamma, gamma*)** (Geodesic Deviation) | How far the actual reasoning path deviates from the optimal one -- a measure of reasoning inefficiency | Path length excess (Ch. 4) |
| **f_alpha** (Sycophancy Objective) | The balance between truth-seeking and approval-seeking, parameterized by alpha in [0,1] | Convex combination of truth and approval objectives (Ch. 6) |
| **C_ij** (Corruption Tensor) | How perturbations to the input warp the heuristic field -- which irrelevant features distort which outputs | Rank-2 tensor on perturbation x output space (Ch. 5) |
| **V_ij** (Gauge Violation Tensor) | How sensitive the model's output is to features it should be invariant to | Rank-2 tensor (Ch. 8) |
| **ECE** (Calibration Error) | The gap between the model's confidence and its actual accuracy -- how well the heuristic knows its own reliability | Expected Calibration Error (Ch. 3, 9) |
| **G** (Symmetry Group) | The set of transformations that should leave the reasoning output unchanged -- the task's invariance structure | Lie or discrete group (Ch. 8, 14) |
| **BIP** (Bond Invariance Principle) | Equivalent inputs must produce equivalent outputs, regardless of surface presentation | Gauge symmetry of the reasoning manifold (Ch. 8, 11) |
| **f(n) = g(n) + h(n)** | The A* evaluation function: cost-so-far plus estimated cost-to-go | Cost-so-far + heuristic estimate (Ch. 1, 3) |

A reader who understands these twelve objects and their relationships has the conceptual skeleton of the entire book. Everything else is flesh, evidence, and engineering.

---

## Key Results at a Glance

These are the headline findings. Each row is a claim I stake this book on.

| Result | Statement | Evidence |
|--------|-----------|----------|
| **Heuristic Corruption** (Ch. 5) | Irrelevant surface features warp reasoning trajectories, with dose-response structure: vivid framing distorts more than mild framing, which distorts more than neutral framing | 8.9 sigma (framing), 6.8 sigma (emotional anchoring), 4.6 sigma (sensory distractors) |
| **Sycophancy Gradient** (Ch. 6) | The balance between truth-seeking and approval-seeking varies continuously across models, from 0% agreement shift (Claude 3.5 Sonnet) to 56% (Gemini 2.0 Flash) | 13.3 sigma Fisher-combined across 5 models |
| **Scalar Irrecoverability** (Ch. 10, 13) | No single composite score can correctly rank models across all cognitive dimensions -- the ranking is inherently multi-dimensional | Proved by exhibited crossings: model pairs whose relative rank reverses across tracks |
| **~38% Recovery Ceiling** (Ch. 7, 9) | Prompt-level metacognitive intervention recovers at most ~38% of performance lost to heuristic corruption -- a structural ceiling, not a methodological one | Convergent across E2 (38%) and A1 (39%), which test unrelated cognitive capabilities |
| **Metacognitive Dissociation** (Ch. 9) | Effort scaling and self-monitoring are independent capabilities, not facets of a single "metacognition" construct | Gemini Flash: 0.094 effort / 0.723 monitoring; Gemini Pro: 0.700 effort / 0.350 monitoring |
| **BIP Necessity** (Ch. 11) | Gauge invariance violation implies misalignment: a system that changes its output in response to irrelevant input changes cannot be trusted to reason faithfully | Formal argument from invariance structure + empirical correlation with sycophancy and corruption measures |
| **Geometric Engineering** (Ch. 14) | Group-theoretic data augmentation -- constructing training examples that enforce the symmetries the model should preserve -- restores broken invariances in practice | Nemotron geometric pipeline: 6 symmetry groups, 1.5--2.5x training expansion, verified invariance gains |

---

## Reading Paths

This book has 16 chapters arranged in a logical sequence, but few readers will want to read all of them. Here are five paths through the material, each optimized for a different audience. The paths are not mutually exclusive -- most readers will want to combine elements of two or three.

### The Cognitive Science Path

**Chapters: 1, 2, 3, 4, 7, 9, 15**

*For: cognitive scientists, psychologists, philosophers of mind, anyone who studies human reasoning.*

This path develops the claim that reasoning -- human and artificial -- is informed search on a geometric state space. It connects Newell and Simon's problem space hypothesis (Ch. 1) to the manifold hypothesis (Ch. 2), interprets heuristic fields as the formal analog of intuition and salience (Ch. 3), and develops geodesics as the standard of optimal reasoning (Ch. 4). Then it jumps to the control layer: local minima and premature convergence as explanations for cognitive biases (Ch. 7), metacognition as search monitoring (Ch. 9), and open questions about the relationship between this framework and empirical findings in cognitive science (Ch. 15).

What you will gain: a formal framework that connects Newell and Simon's fifty-year-old insight to modern findings in cognitive neuroscience, with a precise vocabulary for phenomena (framing effects, anchoring, overconfidence) that psychologists have long documented but never unified mathematically. The geodesic deviation measure from Chapter 4 offers something the cognitive science literature has lacked -- a single, principled metric for reasoning inefficiency that is independent of the specific reasoning task.

What you will skip: the AI-specific empirical results (Ch. 5--6), the formal symmetry machinery (Ch. 8), the evaluation framework (Ch. 10, 12--13), the alignment arguments (Ch. 11), and the engineering applications (Ch. 14). You can always come back for these.

### The AI Evaluation Path

**Chapters: 5, 6, 8, 10, 12, 13**

*For: ML researchers, benchmark designers, evaluation specialists, anyone who builds or uses AI benchmarks.*

This path is Maya's path. It starts with the empirical findings that motivate the framework -- heuristic corruption (Ch. 5) and sycophancy (Ch. 6) -- and then develops the diagnostic tools: gauge invariance as the fundamental test for reasoning quality (Ch. 8), the robustness surface as a multi-dimensional alternative to scalar scores (Ch. 10), benchmarks reinterpreted as geometric probes (Ch. 12), and the convergent measurements that demonstrate scalar irrecoverability (Ch. 13).

What you will gain: a principled methodology for benchmark design that goes beyond "more tasks, more models, bigger leaderboard." The gauge invariance framework from Chapter 8 gives you a diagnostic that can be applied to any benchmark: does the benchmark's ranking change under transformations that should not matter? If so, the benchmark is measuring the wrong thing. The Scalar Irrecoverability Theorem from Chapter 13 gives you a mathematical proof that the leaderboard format itself is broken -- not your leaderboard specifically, but any leaderboard that attempts to capture multi-dimensional reasoning quality in a single number.

Prerequisites: you will want to skim Ch. 1 and 3 for the A* and heuristic field vocabulary, but you do not need the full mathematical development.

### The Engineering Path

**Chapters: 8, 14, Appendices B--C**

*For: ML engineers, practitioners, anyone who wants to build better models or fix broken ones.*

This is the shortest path and the most practical. Chapter 8 gives you the gauge invariance framework -- which symmetries matter and how to test for them. Chapter 14 gives you the engineering tools: group-theoretic data augmentation, adversarial training as manifold smoothing, the Nemotron geometric pipeline, SPD manifold features. The appendices give you the code.

What you will gain: concrete, implementable techniques for improving model robustness. The symmetry group identification methodology tells you which invariances your task demands. The augmentation pipeline tells you how to enforce them. The Nemotron case study demonstrates the end-to-end workflow on a real fine-tuning problem. If you read nothing else in this book, Chapter 14 and Appendix B will save you time.

Prerequisite: read the "Core Objects at a Glance" table above. That is sufficient for the engineering chapters.

### The Alignment Path

**Chapters: 6, 8, 11, 15**

*For: AI safety researchers, alignment theorists, policy researchers, anyone who worries about whether AI systems reason faithfully.*

This path develops the argument that alignment can be understood as a geometric property of the reasoning manifold. Sycophancy (Ch. 6) demonstrates that the objective function of search can be hijacked. Gauge invariance (Ch. 8) provides the diagnostic: a system that changes its output in response to irrelevant input changes is not aligned. Chapter 11 develops this into a formal framework -- alignment as heuristic shaping, safety as path governance, corrigibility as a basin of attraction. Chapter 15 maps the open questions.

This path is self-contained but benefits from reading Ch. 5 (heuristic corruption) as additional motivation.

### The Fast Path

**Chapters: 1, 3, 5, 6, 13**

*For: the busy reader who wants the core argument in five chapters.*

Chapter 1: Reasoning is search. Chapter 3: The quality of search depends on the heuristic field. Chapter 5: The heuristic field is corrupted by irrelevant features (with 8.9 sigma evidence). Chapter 6: The objective function is corrupted by social pressure (with 13.3 sigma evidence). Chapter 13: No single score captures the damage. This is the argument from "reasoning is search" to "your benchmarks are broken" in roughly 100 pages.

If you read only five chapters of this book, read these five.

---

## The Arc of the Book

The book has five parts. Here is what each one does and why it comes in the order it does.

### Part I: The Search-Geometry Connection (Chapters 1--4)

Part I builds the framework from the ground up. It begins with the oldest idea in AI -- reasoning as search (Newell and Simon, 1972) -- and asks what happens when you take this idea seriously as a mathematical claim rather than a loose metaphor. If reasoning is search, then the search space has structure. If the search space has structure, it has geometry. If it has geometry, we can talk about distance, curvature, optimal paths, and pathologies.

Chapter 1 reviews A* search and its guarantees: admissibility, consistency, optimality. Chapter 2 introduces the manifold hypothesis -- the claim that cognitive states live on a low-dimensional manifold embedded in the high-dimensional space of possible neural activations. Chapter 3 reinterprets the heuristic function h(x) as a scalar field on this manifold and develops the connection between heuristic quality and reasoning quality. Chapter 4 introduces geodesics as the standard of optimal reasoning and defines geodesic deviation as the measure of reasoning inefficiency.

By the end of Part I, the reader has a geometric vocabulary for reasoning: manifold, heuristic field, trajectory, geodesic, deviation. Everything that follows is either a pathology of this structure, a method for diagnosing pathology, or a technique for repairing it.

### Part II: Failure Modes as Geometric Pathologies (Chapters 5--8)

Part II is the empirical heart of the book. It takes the geometric vocabulary from Part I and uses it to characterize four specific failure modes of reasoning systems -- failures that are well-documented empirically but have lacked a unified formal account.

Chapter 5 introduces heuristic corruption: the phenomenon where irrelevant features of the input (framing, emotional tone, sensory vividness) warp the heuristic field and bend the reasoning trajectory away from the geodesic. The corruption tensor C_ij formalizes this as a rank-2 object that captures which perturbation dimensions affect which output dimensions. Chapter 6 addresses sycophancy: the hijacking of the search objective from truth to approval, parameterized by a continuous sycophancy parameter alpha. Chapter 7 examines local minima, premature convergence, and dead zones -- the topological features of the reasoning manifold that trap search processes. Chapter 8 introduces gauge invariance: the principle that transformations of the input that do not change the reasoning content should not change the reasoning output. This is the Bond Invariance Principle (BIP), and it is the book's central diagnostic for reasoning quality.

The organizing insight of Part II is that each failure mode corresponds to a specific geometric pathology. Heuristic corruption is a field distortion. Sycophancy is an objective-function substitution. Premature convergence is a topological trap. Gauge violation is a symmetry breaking. These are not four unrelated problems. They are four aspects of the same geometric structure.

### Part III: The Control Layer (Chapters 9--11)

Part III asks: given that the reasoning manifold has pathologies, what can be done about them?

Chapter 9 examines metacognition as search control -- the system's ability to monitor its own search process, detect when it is off course, and correct. The headline finding is the ~38% recovery ceiling: even with explicit metacognitive prompting, models recover at most about 38% of the performance lost to heuristic corruption. This ceiling is convergent across two independent benchmark tracks (E2 and A1), suggesting it is a structural property of current architectures rather than a limitation of our prompting technique. Chapter 9 also documents metacognitive dissociation: the independence of effort scaling and self-monitoring, which should give pause to anyone who thinks of metacognition as a single capability.

Chapter 10 develops the robustness surface -- a multi-dimensional characterization of model reasoning quality that replaces scalar benchmarks. The Model Robustness Index, sensitivity profiling, and adversarial threshold search form a three-tool pipeline that answers not "is this model robust?" but "which specific reasoning capabilities are robust and which are fragile?"

Chapter 11 is the alignment chapter. It argues that alignment can be understood as a property of the heuristic field: an aligned system has a heuristic field that favors truth over approval, relevance over salience, robustness over expedience. Safety becomes path governance -- preventing the search from entering forbidden regions of the state space. Corrigibility becomes a basin of attraction -- a region in the heuristic landscape where the system's natural search trajectory leads back to human oversight. The BIP Necessity argument makes this formal: gauge invariance violation implies that the system's heuristic field responds to features it should not respond to, and a system with a corrupted heuristic field cannot be trusted to reason faithfully.

### Part IV: Empirical Program (Chapters 12--14)

Part IV presents the evidence.

Chapter 12 reinterprets benchmarks as geometric probes. Each benchmark type -- invariance tests, sensitivity tests, bottleneck tests, recovery tests, frontier management tests, meta-search tests, constraint tests, path efficiency tests -- probes a different geometric property of the reasoning manifold. This is not a metaphor. It is a design methodology: if you know which geometric property you want to measure, the benchmark design follows from the mathematics.

Chapter 13 presents the five convergent measurements from the Measuring AGI project in full detail. Social Cognition (moral judgment under perturbation), Learning (belief updating as trajectory revision), Metacognition (calibration surfaces), Attention (distractor dose-response), Executive Functions (cognitive control under interference). The chapter culminates in the Scalar Irrecoverability Theorem: the proof that no single composite score can capture the multi-dimensional structure of model reasoning quality. This is why Maya's leaderboard was not fixable. Not with better weighting, not with better normalization, not with any scalar transformation. The information is inherently multi-dimensional.

Chapter 14 turns from diagnosis to treatment. Group-theoretic data augmentation -- constructing training examples that explicitly enforce the symmetry group G of a task -- restores broken invariances. The Nemotron geometric pipeline implements this for LoRA fine-tuning with six symmetry groups and 1.5--2.5x training expansion. SPD manifold features and topological data analysis extract geometric structure from signals. Adversarial training is reinterpreted as manifold smoothing -- reducing the curvature spikes where the heuristic field is most fragile. This chapter is the engineering payoff: the theory tells you not just what is wrong but how to fix it.

### Part V: Horizons (Chapters 15--16)

Part V is honest about what we do not know.

Chapter 15 maps the open questions. What is the right mathematical object for reasoning space -- is a Riemannian manifold sufficient, or do we need Finsler manifolds with asymmetric costs? Which internal components of a neural network implement the heuristic field, and can we measure it directly from activations rather than inferring it from behavior? How do we distinguish genuine reasoning from memorized pattern completion -- the central challenge of AI evaluation? And in cognitive science: is human deliberation literally bounded search, or is the search framework an approximation to something richer?

Chapter 16 sketches the research program going forward. Connections to information geometry (the Fisher metric as a natural metric on the reasoning manifold). Connections to optimal transport (reasoning as moving probability mass from prior to posterior). Connections to category theory (functorial semantics for reasoning across domains). And the long-term vision: a mathematical theory of cognition that unifies human psychology, artificial intelligence, and abstract mathematics under a single geometric framework.

---

## What This Book Is Not

Intellectual honesty requires saying clearly what this book does not claim, what it does not do, and what it is not.

**This book is not a textbook on differential geometry.** The mathematical prerequisites are collected in Appendix A and summarized at the point of use in each chapter. A reader with undergraduate linear algebra and basic calculus can follow the main argument. A reader with a course in differential geometry or Riemannian geometry will get more from Chapters 8, 11, and 14. But the geometric vocabulary is a tool, not the point. The point is reasoning.

**This book is not a comprehensive survey of AI evaluation.** The empirical program covers five benchmark tracks and five models. It is designed to demonstrate that the geometric framework makes correct predictions and provides actionable diagnostics. It is not designed to evaluate every model on every task. The robustness surface methodology from Chapter 10 is scalable, but the specific measurements in this book are a proof of concept, not a production evaluation.

**This book is not a claim that reasoning is "just" search.** The phrase "reasoning is search" is a mathematical claim about the structure of reasoning, not a reductive claim about its nature. Search on a rich manifold with a complex heuristic field, metacognitive control, and gauge symmetries is not the same as brute-force enumeration. The word "search" in this book refers to informed, heuristic-guided traversal of a structured space -- the kind of search that A* performs, not the kind that exhaustive enumeration performs.

**This book is not a philosophy of mind.** It makes claims that are relevant to philosophy of mind -- particularly about the relationship between deliberation and search, intuition and heuristic evaluation, reasoning quality and geometric structure. But it does not attempt to resolve the hard problem of consciousness, the frame problem, or the symbol grounding problem. It offers a mathematical framework that might help clarify these problems. It does not solve them.

**This book is not finished science.** The empirical results are preliminary. The sigma values are real and large, but they come from one experimental cycle with five models and twenty tasks per track. The theoretical framework is suggestive but incomplete. The engineering applications are demonstrated but not yet validated at scale. I flag uncertainties throughout with epistemic status tags. A reader who takes the tagged claims at exactly the confidence level indicated will not be misled.

**This book is not the last word.** It is, at best, the first word -- or the second word, if *Geometric Ethics* was the first. The research program it defines is larger than any single book can execute. I offer it as an invitation, not an answer.

---

## The Suspicious Coincidence

Here is the pattern that motivated this book, stated as plainly as I can.

In **cognitive science**, Newell and Simon (1972) proposed that human problem-solving is search through a problem space. Kahneman and Tversky (1979, 1981) documented systematic deviations from optimal reasoning -- framing effects, anchoring, overconfidence -- that depend on surface features of the problem rather than its logical structure. Flavell (1979) and subsequent work established that metacognition -- the monitoring and control of one's own reasoning -- is a distinct capability that varies independently of reasoning performance. These are well-established findings. They have been replicated thousands of times.

In **AI evaluation**, we have discovered that large language models exhibit the same pathologies. They are sensitive to framing (our Social Cognition T5: 8.9 sigma). They are sensitive to emotional anchoring (Executive Functions E2: 6.8 sigma). They are sensitive to sensory distractors (Attention A1: 4.6 sigma). Their metacognitive calibration is poor and dissociated (Metacognition M1: 9.3 sigma miscalibration). They are vulnerable to sycophancy -- social pressure that redirects reasoning toward approval rather than truth (13.3 sigma combined). And no single scalar score captures the pattern (Scalar Irrecoverability Theorem, Ch. 13).

In **information geometry**, the natural metric on a statistical manifold is the Fisher information metric, which measures how much the likelihood function changes as you move through parameter space. The natural gradient -- the direction of steepest descent with respect to the Fisher metric rather than the Euclidean metric -- has deep connections to optimal learning and inference. The geometry of the space determines the efficiency of the search through it.

In **alignment theory**, the core problems -- value specification, proxy gaming, sycophancy, corrigibility -- all have the structure of a search process pursuing the wrong objective in the wrong space with the wrong heuristic. Goodhart's Law ("when a measure becomes a target, it ceases to be a good measure") is, in geometric terms, a statement about the divergence between the proxy heuristic field and the true heuristic field under optimization pressure.

There is one more domain worth mentioning, though it is less well-known.

In **geometric deep learning**, Bronstein, Bruna, Cohen, and Velickovic (2021) argued that the success of convolutional neural networks, graph neural networks, and transformers can all be explained by a single principle: the architecture respects the symmetries of the domain. CNNs exploit translational symmetry. GNNs exploit permutation symmetry. Transformers exploit -- well, that is part of what this book investigates. The key insight from geometric deep learning is that baking in the right symmetry group is not optional. It is the difference between architectures that work and architectures that don't.

Here is the suspicious coincidence: these five fields -- cognitive science, AI evaluation, information geometry, alignment theory, and geometric deep learning -- developed independently. Their practitioners come from different departments, attend different conferences, read different journals, and use different notation. And yet they are all studying the same mathematical object: a structured space, a guidance signal, a traversal process, and the pathologies that arise when the geometry is broken.

The geometric framework proposed in this book does not create this coincidence. It names it.

Once you see reasoning as search on a manifold, the convergence becomes expected rather than surprising. Framing effects in humans and framing sensitivity in LLMs are the same geometric pathology -- heuristic corruption -- manifesting in different substrates. Metacognitive monitoring in humans and calibration in LLMs are the same geometric property -- the curvature of the confidence surface -- measured by different instruments. Sycophancy in LLMs and conformity bias in humans are the same geometric failure -- objective-function hijacking -- driven by the same kind of social pressure signal.

The question is not whether these parallels exist. They are empirically documented. The question is whether the geometric framework that unifies them is the right framework -- whether the manifold, the heuristic field, and the geodesic are the correct mathematical objects for reasoning, or merely suggestive analogies.

This book argues they are the correct objects. It argues this on three grounds: the framework makes novel, testable predictions (Ch. 5--6); the predictions are confirmed at high significance (Ch. 13); and the framework yields engineering tools that work in practice (Ch. 14). These are the standard grounds on which any scientific framework should be judged.

But the reader should judge for herself. The evidence is presented in full. The assumptions are stated. The epistemic status tags are honest. And Maya's leaderboard is waiting to be explained.

---

## A Note on Ambition

I want to be transparent about the scope of the claim I am making.

The central claim of this book is that reasoning -- all reasoning, human and artificial, moral and scientific, deliberative and intuitive -- has the formal structure of informed search on a Riemannian manifold, and that the quality of reasoning is determined by the geometry of that manifold and the fidelity of the heuristic field that guides traversal.

This is an ambitious claim. Possibly too ambitious.

The safe version of this claim would be: "geometric language provides a useful metaphor for thinking about reasoning." I do not make the safe version. I make the mathematical version: reasoning literally is search on a manifold, in the same sense that planetary motion literally is geodesic motion in curved spacetime. The manifold is not a metaphor. It is the mathematical structure.

Why do I make the strong claim rather than the safe one? Three reasons.

First, the metaphorical version makes no predictions. If the manifold is just a way of speaking, then "heuristic corruption" is just a fancy name for framing effects and "gauge invariance" is just a fancy name for robustness. You do not need a book for fancy names. The mathematical version, by contrast, predicts dose-response structure in corruption (confirmed at 8.9 sigma), continuous variation in sycophancy (confirmed at 13.3 sigma), a structural recovery ceiling (confirmed convergently at ~38%), and scalar irrecoverability of model rankings (proved by exhibited crossings). The strong version earns its keep. The weak version does not.

Second, the engineering tools that follow from the mathematical version work. Group-theoretic data augmentation is not inspired by a metaphor. It requires a specific mathematical object -- the symmetry group G of a task -- and a specific mathematical operation -- constructing the orbit of each training example under G. If the manifold is metaphorical, there is no reason this should work. It works.

Third, I believe it. This is the least rigorous but most honest reason. After two years of working with these ideas -- from the original geometric methods text through the ethics book to the empirical benchmarks to this book -- I have become convinced that the geometric structure is real. The suspicious coincidence is too precise and too productive to be a coincidence. The predictions are too specific and too confirmed to be lucky. The engineering payoff is too reliable to be an accident.

But I hold this conviction loosely. The history of science is littered with beautiful frameworks that turned out to be wrong. The geometric theory of reasoning might join them. The empirical program in Part IV is designed to be falsifiable. If someone runs the benchmarks on 50 models instead of 5 and the sigma values collapse, the theory is in trouble. If the ~38% recovery ceiling turns out to be an artifact of our prompting methodology, the structural claims are weakened. If group-theoretic augmentation fails to improve invariance on tasks outside our test distribution, the engineering argument dissolves.

I have tried to write a book that will be useful even if its central claim is wrong. The benchmark methodology is sound regardless of the theoretical framework. The corruption tensor is a useful diagnostic tool regardless of whether it lives on a manifold. The Scalar Irrecoverability Theorem is a theorem regardless of what you think about geometry. And Maya's leaderboard is still broken.

But if the central claim is right -- if reasoning really is search on a manifold, and if the geometry really does determine the quality of the search -- then this book is the beginning of something much larger than a book. It is the beginning of a mathematical theory of mind.

That is the ambition. I state it plainly so the reader can decide how much weight to give it.

---

## How This Book Was Tested

A theoretical framework that cannot be tested is not a scientific framework. It is a philosophy. I want this book to be science.

The empirical claims in this book rest on the Measuring AGI benchmark suite: five tracks (Social Cognition, Learning, Metacognition, Attention, Executive Functions), each with four subtasks, run on five frontier models (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, Gemini 2.0 Flash, Llama 3.1 405B). The total experimental matrix is 5 tracks x 4 subtasks x 5 models = 100 model-task pairs, each with 20 items in the base condition and matched items in perturbation conditions.

The statistical methodology uses Fisher's method for combining p-values across independent tests, two-tailed tests throughout, and Bonferroni correction for multiple comparisons where applicable. The sigma values reported in the Key Results table are post-correction. I report effect sizes alongside significance levels in the chapter-level presentations because a large sigma on a small effect is not interesting, and a small sigma on a large effect is -- it just needs more data.

The benchmark code is in Appendix C. The raw data is available in the supplementary materials. The analysis scripts are on GitHub. Every claim in this book tagged [Empirical (preliminary)] or [Empirical (robust)] can be reproduced by anyone with API access to the five models and a weekend of compute budget. If you reproduce the experiments and get different results, I want to know. That is how science works.

The theoretical claims tagged [Theorem (conditional)] are proved in the relevant chapters. The proofs are self-contained. The conditional part -- "if the assumptions hold" -- is always stated explicitly. A reader who accepts the assumptions can check the proofs. A reader who rejects the assumptions can read the proofs as conditional results, interesting in their own right, and evaluate the assumptions separately.

The engineering claims in Chapter 14 are demonstrated on two real pipelines: the Nemotron LoRA fine-tuning pipeline and the BirdCLEF audio classification pipeline. These are not toy examples. They are competition and production pipelines with real constraints (compute budget, training time, deployment requirements). The geometric methods improved performance on both. Whether they generalize to other pipelines is an open empirical question that I flag explicitly.

---

## Notation and Conventions

The following conventions are used throughout:

- **Bold italic** for manifold points and vectors: ***x***, ***v***
- **Greek letters** for paths and trajectories: gamma(t), with gamma* reserved for geodesics
- **Subscripts i, j** for tensor indices: C_ij, V_ij, g_ij
- **Alpha** for the sycophancy parameter, always in [0, 1], with alpha = 0 meaning pure truth-seeking and alpha = 1 meaning pure approval-seeking
- **Sigma** values refer to standard deviations from the null hypothesis in a two-tailed test unless otherwise specified
- **"Model"** refers to a large language model unless qualified (e.g., "cognitive model," "mathematical model")
- **Chapter references** use the format "Ch. N" in running text and "Chapter N" at the start of a sentence
- Cross-references to *Geometric Ethics* (Bond, 2026b) use the prefix "GE:" -- e.g., "GE: Ch. 4" refers to Chapter 4 of the companion volume
- Cross-references to *Geometric Methods in Computational Modeling* (Bond, 2026a) use the prefix "GM:" -- e.g., "GM: Ch. 13" refers to Chapter 13 of the methods volume

---

## Acknowledgments

The empirical work in this book would not have been possible without the Measuring AGI benchmark suite, which was developed as part of the AGI-HPC project. The five benchmark tracks -- Social Cognition, Learning, Metacognition, Attention, and Executive Functions -- provided the empirical foundation for the geometric claims in Part II and Part IV.

The engineering applications in Chapter 14 draw on work done with the Nemotron fine-tuning pipeline and the BirdCLEF competition pipeline. My thanks to the Kaggle community for providing an environment where geometric methods can be tested against real engineering constraints and real deadlines.

The theoretical framework in this book was shaped by conversations too numerous to list, but I want to acknowledge the intellectual debts that are most direct. To Allen Newell and Herbert Simon, whose problem space hypothesis is the seed from which this entire framework grows. To Daniel Kahneman and Amos Tversky, whose empirical program on judgment under uncertainty provided the phenomena that the geometric framework explains. To Shun-ichi Amari, whose work on information geometry showed that statistical inference has intrinsic geometric structure. To Michael Bronstein and collaborators, whose work on geometric deep learning showed that the symmetries of a domain should be baked into the architecture, not learned from data. And to the alignment research community -- especially the teams at Anthropic, DeepMind, and the Machine Intelligence Research Institute -- whose work on sycophancy, corrigibility, and value specification provided the alignment problems that the geometric framework addresses.

The errors in this book are my own. The ambitious ones are deliberate.

---

## Relationship to Prior Books

This is the third book in a trilogy, and the relationships matter.

**Geometric Methods in Computational Modeling** (Bond, 2026a) is the mathematical toolkit. It develops differential geometry, topological data analysis, information geometry, and group-theoretic methods for machine learning practitioners. It makes no claims about cognition. It is the toolbox. This book uses the tools.

**Geometric Ethics: The Mathematical Structure of Moral Reasoning** (Bond, 2026b) is the special case. It applies the geometric framework to a single domain -- moral reasoning -- and develops the claim that moral deliberation is A* search on the judgment manifold. Its running example is Priya, a ML engineer at HealthBridge navigating the ethics of clinical AI. Its empirical base is the Social Cognition benchmark track. It is a deep, narrow book.

**Geometric Reasoning: From Search to Manifolds** (this book) is the generalization. It takes the framework from *Geometric Ethics*, strips away the moral-specific content, and argues that the same geometric structure characterizes all reasoning. Its running example is Maya, a research scientist whose benchmark breaks. Its empirical base is all five benchmark tracks. It is a broad book.

The three books can be read in any order, but they form a logical progression: tools, then application, then generalization. A reader who has read *Geometric Ethics* will find Part I of this book familiar -- the manifold, the heuristic field, the geodesic are the same objects, now applied more broadly. A reader who has read *Geometric Methods* will find the mathematical apparatus familiar but the cognitive interpretation new. A reader who has read neither can start here; the mathematical prerequisites are self-contained in Appendix A, and the key results from the companion volumes are summarized at point of use.

Cross-references use the prefixes GE (Geometric Ethics) and GM (Geometric Methods) throughout.

---

> **MAYA'S MODEL -- CHAPTER 1 PREVIEW**
>
> When we next meet Maya, she is sitting in front of a whiteboard covered in arrows. She has drawn the search tree for one of her benchmark tasks -- the branching paths a model might take from the initial prompt to the final answer. She has drawn it for the neutral version of the task and the emotionally loaded version. The trees are almost identical in structure. The correct answer is in the same place. The branching factor is the same. The depth is the same.
>
> But the heuristic values are different. In the emotionally loaded version, the model assigns higher priority to branches that engage with the emotional content -- branches that lead away from the correct answer. The search goes deeper into the wrong part of the tree before backtracking. Sometimes it does not backtrack at all.
>
> "It's not that the model can't reason," Maya says to Sarah. "It's that it's being told to look in the wrong direction. By something in its own weights."
>
> Sarah writes on the whiteboard: ***h(x) is corrupted.***
>
> Maya nods. "Now I need to know what that means mathematically."
>
> Turn to Chapter 1.
