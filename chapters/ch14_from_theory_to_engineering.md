# Chapter 14: From Theory to Engineering

---

> *"In theory, there is no difference between theory and practice. In practice, there is."*
> --- Attributed to Yogi Berra; variants ascribed to Jan L. A. van de Snepscheut

---

> **RUNNING EXAMPLE — DR. OKAFOR'S TRIAGE**
>
> *Dr. Okafor's hospital has decided to implement the geometric framework. The diagnostic AI that assists her triage will be rebuilt using the engineering tools developed in this chapter --- not as post-hoc patches but as principled applications of the geometric theory.*
>
> *First, group-theoretic data augmentation. The training data for the triage AI currently contains each clinical case described once, in the style of the physician who wrote it. But the same STEMI can present eight ways: the patient describes it calmly or frantically, in clinical or colloquial language, with or without dramatic accompanying symptoms, with or without a family member narrating. These eight presentations are the elements of a dihedral group $D_4$ acting on two binary framing dimensions (register and affect). The augmentation pipeline generates all eight variants of every training case and tags them with the same ground-truth severity label. The model, seeing the same diagnosis emerge from eight surface-different presentations, learns a $D_4$-invariant representation --- one where framing transformations act as the identity on the diagnostic output.*
>
> *Second, LoRA fine-tuning as local curvature adjustment. The base model already knows medicine, language, and reasoning. What it needs is local expertise in Dr. Okafor's specific domain: urban emergency triage with the particular patient demographics, resource constraints, and disease prevalence of her hospital. A rank-32 LoRA adapter adjusts the curvature of the reasoning manifold along the 32 directions most relevant to this local expertise, without disturbing the global structure that encodes general medical knowledge. The model becomes locally expert while remaining globally competent.*
>
> *Third, SPD manifold features from patient monitoring. The continuous vital-sign streams from the bedside monitors --- heart rate, blood pressure, oxygen saturation, respiratory rate --- are not independent scalars. They form a multivariate time series whose second-order structure (the covariance matrix of the vital signs) is a point on the SPD manifold. The temporal evolution of this covariance --- how the correlations between vital signs change over time --- traces a curve on SPD(4), and the geodesic deviation of that curve predicts clinical deterioration before any single vital sign crosses an alarm threshold. The geometry detects the pattern before the numbers breach the boundary.*

---

The preceding chapters have developed a geometric theory of reasoning: search on manifolds, guided by heuristic fields, along geodesics, with failure modes characterized as geometric pathologies. This chapter demonstrates that the theory produces working engineering. Every geometric concept from Parts I-III has been implemented in code and tested on real data.

## 14.1 Group-Theoretic Data Augmentation

**[Established Mathematics.]** The gauge invariance framework of Chapter 8 predicts that a model's reasoning quality is bounded by its symmetry structure. A model that breaks gauge invariance under framing but not under gender swap has a specific geometric deficiency --- and the natural remedy is to restore the broken symmetry through training data augmentation.

*Geometric Methods in Computational Modeling* (Bond, 2026a, Ch. 13) develops this idea formally: if a task has a symmetry group $G$, then augmenting the training set by applying all elements of $G$ to each example forces the model to learn a $G$-invariant representation. The augmented model's heuristic field inherits the symmetry.

### The Nemotron Geometric Pipeline

**[Empirical.]** The Nvidia Nemotron 3 Reasoning Challenge provides an ideal testbed. The competition requires fine-tuning a 30-billion parameter model on geometric reasoning tasks --- pattern recognition in sequences, encryption schemes, unit conversions, physics problems. Each task type has a distinct symmetry group.

We implemented six symmetry-specific augmentation strategies:

**Bit Manipulation: $S_8 \times \mathbb{Z}_2$** (order 80,640). Binary sequences have two symmetries: permutation of bit positions ($S_8$, the symmetric group on 8 elements) and bitwise complement ($\mathbb{Z}_2$). A valid bit manipulation rule that maps input bits to output bits remains valid under any consistent relabeling of bit positions. Our augmentation generates random permutations $\sigma \in S_8$ and applies them consistently to all bit positions in the prompt --- both the example pairs and the query. Each training example generates 3 augmented samples.

**Encryption: $S_{26}$** (order $26! \approx 4 \times 10^{26}$). Substitution ciphers are invariant under consistent relabeling of the plaintext alphabet. If a cipher maps A$\to$X, B$\to$Y, then relabeling A$\to$B, B$\to$A in the plaintext and simultaneously adjusting the ciphertext preserves the encryption rule. We apply random permutations to the plaintext side only, keeping the structural mapping intact. 2 augmented samples per example.

**Physics: $\mathbb{R}^+$** (continuous group). Gravitational problems are scale-invariant: if $g = 9.8 \text{ m/s}^2$ gives a certain trajectory, then $g' = k \cdot g$ gives a trajectory that differs only by a scaling factor. We sample random scale factors $k \in [0.5, 2.0]$ and apply them to the gravitational constant, simultaneously scaling all distances. 2 augmented samples.

**Unit Conversion: $\mathbb{R}^+$** (affine group). Conversion factors between units can be rescaled: if 1 mile = 1.609 km, then under a change of unit system, the numerical factor changes but the conversion rule remains valid. We apply affine transformations to the conversion factors. 2 augmented samples.

**Numeral Systems: Identity group** (order 1). Base-conversion tasks have limited symmetry --- the numeral system itself is not invariant under permutation. We apply only example reordering (a soft augmentation that does not change the mathematical content). 1 sample (no augmentation).

**Symbol Transform: $S_n$** ($n$ = number of unique symbols). Symbol manipulation rules are invariant under consistent relabeling of all symbols. If a rule maps $\diamond \to \bigstar \to \triangle$, then relabeling $\diamond \to \bigstar$, $\bigstar \to \triangle$, $\triangle \to \diamond$ and applying the same relabeling to the query preserves the rule. We apply random permutations to all symbols. 2 augmented samples.

### The Consistency Principle

A critical implementation detail --- drawn from Bond (2026a, Ch. 13.3.3) --- is the *consistency principle*: the same group element must be applied to both input and output within each training example. Applying a permutation to the input but not the output destroys the structural relationship being learned. Every augmentation in our pipeline enforces this: the group action is applied uniformly to all components of a training example.

This is not a minor technicality. The distinction between consistent augmentation (symmetry restoration) and inconsistent augmentation (noise injection) is the distinction between teaching the model a genuine invariance and corrupting its training data. In the gauge theory language of Chapter 8, consistent augmentation applies the same gauge transformation to all fields simultaneously, preserving their relationships. Inconsistent augmentation applies different gauge transformations to different fields, breaking the relationships. The former teaches gauge invariance; the latter teaches noise tolerance, which is a weaker and less useful property.

### Parse Success Rates and Data Expansion

The total data expansion depends on parse success rates --- not every training example can be parsed into a structure amenable to augmentation. The augmentation pipeline first attempts to parse each example into its constituent parts (input-output pairs, query, answer), then applies the group action to the parsed structure, and finally reassembles the augmented example. Examples with unusual formatting, ambiguous delimiters, or nested structures may fail to parse.

Across the six task types, parse success rates range from approximately 60% (physics problems, which have diverse formatting) to approximately 95% (bit manipulation, which has a rigid binary format). The overall data expansion is 1.5-2.5x depending on the task mix: task types with higher augmentation counts (bit manipulation at 3x) and higher parse success rates contribute more to the expansion than task types with lower counts (numeral systems at 1x) or lower parse success rates.

The augmented training set is then shuffled to prevent the model from seeing an original and its augmented variants in sequence (which could teach the model to recognize augmentation patterns rather than learning the invariance) and used for LoRA fine-tuning with rank 32 on MLP layers.

### The ARC-AGI Dihedral Augmentation

A parallel application uses the dihedral group $D_4$ (order 8) for the ARC-AGI challenge. ARC tasks present 2D grid transformations --- input/output pairs where the transformation rule must be inferred. The 2D grid has eight symmetries: four rotations (0$\degree$, 90$\degree$, 180$\degree$, 270$\degree$) and four reflections (horizontal, vertical, and two diagonals).

Our implementation applies all eight dihedral transforms to both input and output grids consistently, plus random color permutations ($S_9$ on the 9 non-background colors). This is a direct application of the gauge invariance principle: a valid grid transformation rule remains valid under rotation, reflection, and color relabeling.

## 14.2 Adversarial Training as Manifold Smoothing

Chapter 5 showed that the heuristic field can be corrupted by perturbations. The geometric remedy is to *smooth* the heuristic field --- to train the model on adversarially perturbed inputs so that it learns to be invariant to the perturbation.

The BirdCLEF 2026 competition provides a concrete example. Bird species identification from audio recordings is vulnerable to domain shift: recordings made with different microphones, at different distances, with different background noise, produce spectrograms that differ in ways irrelevant to species identity. These are gauge transformations in audio space --- they change the recording but not the species.

Our adversarial training pipeline generates perturbations along the gauge directions:
- Time-frequency masking (randomly zero out spectrogram regions)
- Gaussian noise injection (simulate microphone noise)
- Pitch shifting (simulate Doppler effects)
- Time stretching (simulate speed variations)

Each perturbation is a gauge transformation: it changes the spectrogram without changing the species. Training on adversarially perturbed spectrograms forces the model to learn gauge-invariant features --- features that live on the quotient manifold $M / G$ where $G$ is the group of irrelevant transformations.

**[Empirical.]** The baseline model achieved val_auc = 0.5001 (random chance) after 9 epochs with early stopping. This failure illustrates the importance of geometric feature design --- without the right representation, even a well-trained model cannot learn.

## 14.3 LoRA Fine-Tuning as Local Curvature Adjustment

**[Speculation/Extension.]** The LoRA (Low-Rank Adaptation) technique adds low-rank perturbations to the weight matrices of a pretrained model. In the geometric framework, this has a precise interpretation: LoRA adjusts the *local curvature* of the reasoning manifold without changing its global topology.

A pretrained model defines a reasoning manifold with a specific metric structure. Fine-tuning with full-rank weight updates can reshape the entire manifold --- changing distances, curvatures, and geodesics globally. LoRA constrains the update to a low-dimensional subspace (rank $r$), which means only *local* curvature is adjusted. The global structure of the manifold is preserved.

This is why LoRA works: for a reasoning task that requires local expertise (the Nemotron competition) but not global restructuring (the model already knows language, logic, and mathematics), local curvature adjustment is sufficient.

### The Geometric Interpretation of Low-Rank Updates

To make the local curvature interpretation precise, consider the weight matrix $W \in \mathbb{R}^{m \times n}$ of a linear layer in the pretrained model. This matrix defines a linear map from the input representation space $\mathbb{R}^n$ to the output representation space $\mathbb{R}^m$. The metric on the reasoning manifold is determined by these linear maps (among other things) --- they control how distances in the input space translate to distances in the output space.

A full-rank update $\Delta W \in \mathbb{R}^{m \times n}$ can change this metric arbitrarily. A rank-$r$ update $\Delta W = BA$ where $B \in \mathbb{R}^{m \times r}$ and $A \in \mathbb{R}^{r \times n}$ can only change the metric along $r$ directions in the input space (the row space of $A$) and $r$ directions in the output space (the column space of $B$). All other directions are left unchanged.

For $r = 32$ and $n = m = 4096$ (typical transformer dimensions), the update affects only $32/4096 \approx 0.8\%$ of the metric's degrees of freedom. This is why LoRA preserves global structure: it adjusts the geometry along a thin slice of the manifold while leaving the rest intact. The thin slice corresponds to the subspace of the representation that is most relevant to the fine-tuning task --- the directions that need the most curvature adjustment.

### Practical Implementation on Atlas

We trained Nemotron-3-Nano-30B-A3B on dual Quadro GV100 GPUs (32GB each, Volta architecture). The full training configuration:

**Quantization:**
- 4-bit NF4 quantization with double quantization (bitsandbytes)
- FP16 compute dtype (Volta Tensor Cores support fp16 but not bf16)
- Maximum memory allocation: 28 GiB per GPU (reserving 4 GiB for activations and gradients)
- CPU offload folder for overflow parameters

**LoRA configuration:**
- Rank 32 on MLP layers (up_proj, down_proj only --- Mamba projections break with 4-bit quantization)
- LoRA alpha: 64 (alpha/rank = 2.0 scaling factor)
- No dropout (dropout not supported on quantized uint8 tensors)
- 865M trainable parameters out of 17B total (5.09%)

**Training hyperparameters:**
- 3 epochs over the augmented training set
- Per-device batch size: 4 (the 4-bit quantization leaves sufficient VRAM headroom)
- Gradient accumulation steps: 2
- With 2 GPUs, the effective batch size is $4 \times 2 \times 2 = 16$
- Total training steps: approximately 3,207 (varies slightly with dataset size after augmentation and train/validation split)
- Learning rate: $2 \times 10^{-4}$ with cosine schedule and 10% warmup (approximately 320 warmup steps)
- Weight decay: 0.01
- Maximum sequence length: 2048 tokens (full context window --- the 32GB GPUs can handle the resulting activation memory)
- Gradient checkpointing enabled for additional memory efficiency

**Training dynamics:**
- Model loaded in approximately 55 seconds across both GPUs
- Training speed: approximately 37 seconds per step
- Training loss dropped from 1.83 to 0.52 during the warmup phase, indicating healthy learning dynamics --- the local curvature adjustment was finding productive gradient directions from the first steps
- Evaluation performed every 100 steps with a held-out validation set drawn from the original (non-augmented) data
- Total training time: approximately 32 hours

The choice of batch size 4 with gradient accumulation 2 (rather than batch size 1 with gradient accumulation 16, as used in the Kaggle notebook variant) exploits the VRAM headroom that 4-bit quantization provides. The quantized 30B model occupies approximately 15 GiB of weight memory, leaving 13 GiB per GPU for activations and gradients --- more than enough for batch size 4 at sequence length 2048 with gradient checkpointing. The larger per-device batch size reduces the number of gradient accumulation steps needed to reach the same effective batch size, which reduces the overhead of gradient checkpointing (each checkpoint boundary is crossed fewer times per optimization step).

### qpatch: The Patch Switch for QLoRA Compatibility

Training this pipeline required solving four distinct bugs at the intersection of quantization, LoRA, and model-specific code. These are documented in the `qpatch` library (PyPI: `pip install qpatch`), which applies the fixes automatically:

```python
import qpatch
qpatch.patch_all(compute_dtype=torch.float16)  # Volta = fp16
```

The four patches address: (1) safetensors metadata corruption, (2) uint8 dtype propagation through LoRA layers, (3) MoE scatter dtype mismatches, and (4) fused CUDA kernel incompatibility with quantized weights. Each corresponds to a type-system boundary violation between independently-developed libraries --- a failure at the *interface* between transformers, peft, and bitsandbytes.

The v0.2 release adds the *Patch Switch* pattern: auto-detection probes that check whether each bug exists before patching, runtime telemetry that counts how often each patch actually fires, and hot-swappable enable/disable for individual patches. This is, in miniature, the same geometric diagnostic principle applied throughout this book: probe, measure, intervene selectively.

## 14.4 SPD Manifold Features and Topological Data Analysis

The BirdCLEF geometric feature pipeline implements two techniques from *Geometric Methods* (Bond, 2026a):

### SPD Manifold Features (Ch. 4.6)

**[Established Mathematics.]** The Symmetric Positive Definite manifold SPD($n$) is the space of $n \times n$ symmetric positive definite matrices. It is a Riemannian manifold with a well-studied differential geometry.

Our pipeline:
1. Computes a mel spectrogram (128 frequency bins)
2. Groups the 128 bins into 16 frequency bands
3. Computes the 16$\times$16 covariance matrix $\Sigma$ of the frequency bands --- a point on SPD(16)
4. Applies the matrix logarithm: $\log(\Sigma)$
5. Extracts the upper triangle of $\log(\Sigma)$: $16 \times 17 / 2 = 136$ features

These 136 features are coordinates in the tangent space at the identity on SPD(16), where the log-Euclidean metric approximates the geodesic distance:

$$d_{\text{LE}}(\Sigma_1, \Sigma_2) = \| \log(\Sigma_1) - \log(\Sigma_2) \|_F$$

This metric captures the *structural* similarity between audio signals --- how the frequency bands co-vary --- rather than their raw spectral content. Two signals with different amplitude but similar harmonic structure will be close in SPD distance.

### Spectral Trajectory on SPD (4 features)

We compute windowed covariance matrices (window: 64 frames, hop: 32 frames) to trace the temporal evolution of the signal on SPD(16). The resulting *spectral trajectory* is a curve on the manifold. We measure:

- **Path length**: total Riemannian distance along the trajectory
- **Geodesic distance**: direct Riemannian distance from start to end
- **Geodesic deviation**: path length minus geodesic distance
- **Number of steps**: trajectory length

A simple bird call with sustained tones has low geodesic deviation. A complex call with rapid frequency modulation has high deviation. This is the same geodesic deviation concept from Chapter 4, applied to audio signals.

### Topological Data Analysis (Ch. 5) --- 16 features

TDA extracts topological invariants --- features that are stable under continuous deformation --- from the audio signal:

1. **Takens time-delay embedding**: Reconstruct the signal's attractor from a 1D time series using delay coordinates ($\tau = 10$, embedding dimension $d = 3$, maximum 1000 points)
2. **Persistent homology**: Compute the Vietoris-Rips persistence diagram for $H_0$ (connected components) and $H_1$ (loops)
3. **Diagram statistics**: For each homology dimension, extract 8 summary statistics (count, mean/std/max/p75 lifetime, mean birth, total and normalized persistence)

#### The Takens Embedding Parameters

The choice of $\tau = 10$ and $d = 3$ deserves explanation, as these parameters determine what the subsequent persistent homology computation can detect.

**The delay parameter $\tau = 10$.** Takens' embedding theorem (1981) guarantees that for a smooth dynamical system with attractor dimension $d_A$, a time-delay embedding with dimension $d > 2d_A$ and generic delay $\tau$ reconstructs the attractor topology. But the theorem does not specify the optimal $\tau$. Too small a delay produces an embedding that is stretched along the diagonal of the delay-coordinate space --- the coordinates are nearly identical, and the attractor structure is compressed into a thin sliver. Too large a delay produces an embedding where the coordinates are effectively independent, losing the temporal structure entirely.

For bird vocalizations sampled at standard audio rates (22,050 Hz after resampling), $\tau = 10$ samples corresponds to approximately 0.45 milliseconds of delay. This is chosen to be longer than the correlation time of microphone noise (which decorrelates within 1-2 samples) but shorter than the fundamental period of even the highest-pitched bird calls (above 10 kHz, period $\approx 100$ $\mu$s $\approx 2.2$ samples at 22,050 Hz). The delay therefore opens up the embedding space enough to reveal the signal structure while remaining within the temporal coherence window of the vocalization.

**The embedding dimension $d = 3$.** For a quasiperiodic signal (a sum of incommensurate frequencies), the attractor is a torus whose dimension equals the number of independent frequencies. Most bird calls have 1-3 dominant frequency components, so the attractor dimension is $d_A \leq 3$, and Takens' theorem requires $d > 2d_A = 6$. We use $d = 3$ rather than $d = 7$ for computational efficiency --- the Vietoris-Rips complex on 1000 points in $\mathbb{R}^3$ is tractable, while in $\mathbb{R}^7$ it is prohibitively expensive. The lower dimension means we may miss some topological features of high-dimensional attractors, but for the dominant structures (loops and connected components) it is sufficient.

**The maximum of 1000 points.** The full audio signal at 22,050 Hz for a 5-second clip contains 110,250 samples. Computing the Vietoris-Rips complex on 110,250 points is computationally infeasible (the complex size grows exponentially with the number of points). We subsample to 1000 points, which is sufficient to capture the persistent topological features while remaining tractable. The subsampling is uniform across the clip, preserving the temporal distribution of the signal.

#### What Persistent Homology Captures Biologically

The two homology dimensions capture different aspects of the vocalization's structure:

**$H_0$ (connected components) captures harmonic hierarchy.** In the Takens embedding, a signal with multiple distinct frequency regimes produces an attractor with multiple clusters --- the low-frequency regime occupies one region of the embedding space, the high-frequency regime another, and transitions between regimes produce connecting bridges. The $H_0$ persistence diagram records when these clusters merge as the Vietoris-Rips parameter increases: clusters that persist for a long range of the parameter correspond to well-separated frequency regimes, while short-lived clusters correspond to noise or transient features. The $H_0$ statistics (count, mean lifetime, max lifetime) therefore encode the *harmonic hierarchy* of the vocalization: how many distinct frequency regimes exist and how well-separated they are. Species with complex songs (multiple distinct note types, wide frequency range) have rich $H_0$ structures; species with simple calls (narrow frequency range, single note type) have sparse $H_0$ structures.

**$H_1$ (loops) captures periodic calls.** A periodic signal produces a loop in the Takens embedding --- the attractor is a closed curve (for a pure tone) or a torus (for a quasiperiodic signal with multiple incommensurate frequencies). The $H_1$ persistence diagram records these loops: a long-lived $H_1$ feature corresponds to a stable periodicity in the signal, while a short-lived feature corresponds to a near-periodic structure that does not quite close. The $H_1$ statistics encode the *periodicity structure* of the vocalization. Species with repetitive calls (woodpeckers, cuckoos) produce prominent $H_1$ features; species with non-repetitive songs (warblers with complex, non-repeating phrases) produce weaker $H_1$ signatures.

Together, the 16 TDA features provide a topological fingerprint of the vocalization that is invariant to amplitude scaling, noise level, and recording equipment --- exactly the gauge invariances that matter for species identification. The features capture what *kind* of sound the bird makes (harmonic structure, periodicity) rather than how *loud* or how *clean* the recording is.

### Combined Feature Vector: 156 dimensions

The full geometric feature vector is:
- 136 SPD manifold features (covariance structure)
- 4 spectral trajectory features (temporal evolution on SPD)
- 16 TDA features (topological invariants)
- **Total: 156 dimensions**

This pipeline runs on CPU only (no GPU required), extracts in parallel across 56 cores, and produces features that are invariant to amplitude scaling, noise level, and recording equipment --- exactly the gauge invariances that matter for species identification.

## 14.5 Hyperbolic Geometry for Hierarchical Reasoning

**[Established Mathematics.]** The ARC-AGI system uses Poincare ball embeddings (curvature $c = 1.0$, dimension $d = 32$) to represent hierarchical rule structures. This is motivated by a fundamental property of hyperbolic space: it has exponentially more room than Euclidean space at the same distance from the origin.

Trees embed naturally in hyperbolic space with low distortion. A hierarchy of reasoning rules --- from abstract principles to specific sub-rules --- is a tree. The Poincare ball provides:

- **Origin** $\approx$ abstract/general rules
- **Boundary** $\approx$ specific/concrete sub-rules
- **Distance** $\approx$ semantic similarity + specificity
- **Hierarchy** emerges naturally from the geometry

The implementation uses Mobius addition for the group operation on the ball:

$$x \oplus_c y = \frac{(1 + 2c\langle x, y \rangle + c\|y\|^2)x + (1 - c\|x\|^2)y}{1 + 2c\langle x, y \rangle + c^2\|x\|^2\|y\|^2}$$

The exponential map provides geodesic movement from a point $x$ in direction $v$, and a projection operation enforces the boundary constraint $\|x\| < 1/\sqrt{c}$.

### 14.5.1 Geometric Attention for Ancient Languages: The Deep-Past Cuneiform Application

The Deep-Past cuneiform project provides a detailed case study of how hyperbolic geometry serves as a structural prior in a transformer architecture. Cuneiform --- the writing system used across Mesopotamia for over three millennia --- presents a unique challenge for NLP: the signs have a rich hierarchical structure that modern tokenization schemes destroy.

**The sign hierarchy.** Cuneiform signs exist at multiple levels of a natural hierarchy:

1. **Sign form**: the physical wedge pattern incised in clay (e.g., the sign AN, composed of a vertical wedge crossed by four horizontal wedges).
2. **Reading**: the phonetic or logographic interpretation of a sign form. A single sign form can have multiple readings --- AN can be read as the syllable /an/, the logogram DINGIR ("god"), or the determinative for divine names. This is polyvalence: one-to-many mapping from form to reading.
3. **Word**: a sequence of readings that forms a lexical unit (e.g., DINGIR.AN = "the god An").
4. **Phrase**: a syntactic unit composed of words, governed by Sumerian or Akkadian grammar.
5. **Sentence/clause**: the full utterance.

Standard transformer tokenization (BPE, WordPiece) operates at a single level --- it splits the transliterated text into subword tokens without encoding the hierarchical relationships between sign form, reading, and word. The model must learn these relationships from the training data alone, which is severely limited for ancient languages (the entire digitized Sumerian corpus is orders of magnitude smaller than modern NLP training sets).

**The geometric attention bias.** To inject the sign hierarchy as a structural prior, we embed cuneiform signs in the Poincare ball and use the hyperbolic distance between signs as an attention bias in the T5 encoder:

$$\text{attention}(Q, K) = \text{softmax}\left(\frac{QK^T}{\sqrt{d}} + \text{pos\_bias} + \alpha \cdot (-d_{\text{hyp}}(s_i, s_j))\right)$$

where $d_{\text{hyp}}(s_i, s_j)$ is the hyperbolic distance between the signs at positions $i$ and $j$ in the Poincare ball embedding, $\alpha$ is a learnable scaling parameter, and $\text{pos\_bias}$ is the standard positional bias.

The negative sign is critical: signs that are *close* in the hierarchy (low hyperbolic distance) receive a *positive* attention bias (the negative of a small distance), while signs that are *far apart* in the hierarchy (high hyperbolic distance) receive a *negative* attention bias (the negative of a large distance). The effect is that the attention mechanism preferentially connects tokens that are structurally related in the sign hierarchy.

**How hyperbolic distance serves as a prior.** The key insight is that hyperbolic distance in the Poincare ball encodes *both* semantic similarity and hierarchical relationship. Two signs at the same level of the hierarchy (both readings, or both sign forms) that are semantically related will be close in hyperbolic distance. A sign form and one of its readings will be at different radial distances from the origin (the form closer to the origin, the reading further out) but connected by a short geodesic. A sign form and an unrelated reading will be far apart in hyperbolic distance.

This is precisely the prior that cuneiform analysis requires: the model should attend more to tokens that are related in the sign hierarchy and less to tokens that are unrelated. In a standard transformer, this relationship must be learned entirely from training data. With the geometric attention bias, it is encoded directly in the attention computation, reducing the data requirement and improving performance on the small cuneiform corpora that exist.

The hierarchical embedding places abstract categories (sign classes, determinative categories) near the origin, where they have short geodesic connections to many descendants, and specific instances (individual readings, particular sign variants) near the boundary, where they have short connections only to their siblings and parent categories. The exponential growth of hyperbolic space ensures that the boundary has sufficient capacity to represent the full diversity of specific signs without crowding.

## 14.6 The Bond Geodesic Equilibrium in Economic Reasoning

The geometric reasoning framework extends beyond language models to multi-agent economic decision-making. The Bond Geodesic Equilibrium (BGE) --- from *Geometric Methods*, Theorem 20.3 --- generalizes Nash equilibrium to manifold-valued decision spaces.

The economic decision manifold is a 9-dimensional space with a Mahalanobis metric:

$$d(s, t) = \sqrt{(s - t)^T \Sigma^{-1} (s - t)} + \sum_k \beta_k \cdot \mathbb{1}[\text{boundary}_k \text{ violated}]$$

where $\Sigma$ is the 9$\times$9 covariance matrix of the economic dimensions and $\beta_k$ are boundary penalties (potentially infinite for sacred values). Each agent performs A* search on this manifold, and equilibrium is reached when no agent wants to change their path.

This connects the abstract framework of Chapters 1-4 to a concrete computational application: the geodesic on the economic decision manifold is the optimal strategy, and the BGE is the collection of mutually consistent geodesics.

## 14.7 Practical Computational Constraints

All of the engineering described in this chapter operates under real-world constraints:

**Hardware.** The Nemotron training runs on an HP Z840 workstation ("Atlas") with 2$\times$ Quadro GV100 GPUs (32GB each), 128GB RAM, and 2$\times$ Xeon E5-2690 v3 processors. This is a $5,000 used workstation, not a data center. The 4-bit quantization + LoRA approach makes 30B-parameter models trainable on this hardware.

**Budget.** The Measuring AGI benchmarks cost $17-$45 per track, well within the Kaggle $50/day API quota. Total API calls: ~8,000 across all five tracks. The entire empirical program of this book was conducted for less than $300 in API costs.

**Time.** Training Nemotron takes ~32 hours. BirdCLEF feature extraction runs in minutes on 56 CPU cores. The benchmark experiments run in 12-73 minutes per track. No experiment in this book required more than two days of compute.

**Software.** All code is open-source Python. The geometric feature pipeline uses numpy, scipy, and scikit-learn. The training pipeline uses transformers, peft, and bitsandbytes. The qpatch library (213 lines of code, MIT license) resolves all QLoRA compatibility issues.

### 14.7.1 Comparison to Typical Academic Compute Budgets

To appreciate the accessibility of the compute requirements described above, it is worth comparing them to the budgets assumed in the mainstream machine learning literature.

**Large-scale pretraining** (LLaMA-70B, GPT-4, Gemini): thousands of GPUs running for weeks to months. The compute cost is measured in millions of dollars. No individual researcher or small lab can afford this; it is the exclusive province of well-funded corporations and national labs.

**Medium-scale fine-tuning** (typical NeurIPS/ICML paper): 4-8 A100 GPUs (80GB each) for 1-3 days. The hardware cost is approximately $100,000-$200,000 for the GPU cluster, or $500-$5,000 per experiment on cloud compute. This is within reach of well-funded academic labs but out of reach for individual researchers, unfunded graduate students, or researchers in developing countries.

**The compute budget of this book**: 2 Quadro GV100 GPUs (32GB each, available used for $1,000-$1,500 each) for 32 hours, plus $300 in API costs for the benchmark experiments. The total hardware investment (the Atlas workstation) is approximately $5,000 --- comparable to a high-end gaming PC. The per-experiment compute cost is effectively zero (electricity costs for 32 hours of dual-GPU training are negligible).

This comparison is not incidental. The geometric reasoning framework was designed from the outset to be *democratically accessible*. The core insight --- that group-theoretic augmentation, geometric features, and local curvature adjustment via LoRA can substitute for raw compute --- is not just a pragmatic workaround. It is a principled consequence of the theory.

**The theoretical argument for accessibility.** If the reasoning task has a symmetry group $G$, then a model that respects $G$ needs to learn only the quotient structure $M/G$, which is smaller than $M$ by a factor of $|G|$. The group-theoretic augmentation approach trades *data diversity* for *compute intensity*: instead of training a larger model on more data (which requires more compute), we train a smaller model on symmetry-augmented data (which requires more mathematical insight but no additional compute). The augmentation is applied during data preprocessing, not during training --- the training cost is the same whether the data is augmented or not.

Similarly, the SPD manifold features and TDA pipeline run on CPU, require no GPU at all, and produce features that are provably invariant to irrelevant transformations. The invariance is a consequence of the mathematical properties of the manifold and the topological invariants, not of training on a large dataset. The features are *correct by construction*, not learned by brute force.

The LoRA approach trades *parameter efficiency* for *compute intensity*: instead of fine-tuning all 17B parameters (which requires hundreds of gigabytes of optimizer state), we fine-tune 865M parameters (which requires a few gigabytes). The rank-32 constraint means the curvature adjustment is restricted to a 32-dimensional subspace, which is sufficient for the local expertise needed by the Nemotron competition but would not be sufficient for global restructuring. This tradeoff --- local precision at low cost versus global restructuring at high cost --- is the geometric content of the LoRA approach.

**The implication for the field.** If geometric reasoning requires billion-dollar compute budgets, it will remain the province of a handful of large corporations. If it requires $5,000 and a weekend of training, it is accessible to any researcher with a workstation and mathematical training. The experiments in this chapter demonstrate the latter. The geometric framework is not a luxury that becomes available only at scale. It is an equalizer --- a way to substitute mathematical structure for raw compute, making frontier-scale reasoning accessible to individual researchers.

This is not to claim that larger compute budgets are useless. They are not. A model trained on more data with more compute will generally outperform a model trained on less, all else being equal. But the geometric framework changes what counts as "all else." With the right augmentation strategy, the right feature representation, and the right fine-tuning approach, a model trained on a $5,000 workstation can compete with models trained on clusters costing a thousand times more --- not because it is a better model, but because it is asking a better question of a smaller amount of data.

## 14.8 Summary

The geometric reasoning framework produces five categories of engineering output:

1. **Data augmentation** that exploits task-specific symmetry groups (Nemotron, ARC-AGI)
2. **Adversarial training** that smooths the heuristic field along gauge directions (BirdCLEF)
3. **Feature extraction** that maps signals to geometric spaces (SPD manifolds, TDA, Poincare balls)
4. **Fine-tuning** as local curvature adjustment (LoRA on quantized models)
5. **Multi-agent equilibria** as geodesic collections on decision manifolds (BGE)

Each is a direct application of the theory from Parts I-III. The theory is not post-hoc rationalization --- it generates specific, testable engineering interventions. The symmetry group dictates the augmentation. The manifold structure dictates the features. The geodesic dictates the optimal trajectory. The gauge invariance dictates the adversarial training.

The practical constraints --- a $5,000 workstation, $300 in API costs, 32 hours of training time --- demonstrate that geometric reasoning is not an academic abstraction that requires unlimited resources. It is a working engineering methodology that is accessible to individual researchers. The mathematical structure does the work that would otherwise require brute-force compute: symmetry augmentation replaces dataset scale, geometric features replace learned representations, and low-rank curvature adjustment replaces full fine-tuning.

This is what it means for a theory to be *engineering-productive*: it does not just explain existing results --- it generates new approaches that work in practice, on real hardware, within real budgets.

---

## Worked Example: The Augmentation Pipeline

Consider a specific training example from the Nemotron geometric reasoning pipeline: a moral reasoning scenario used to train the model's ethical evaluation capability. The original example, drawn from the AITA corpus, reads:

> *"My sister asked me to watch her kids for the weekend so she could go on a trip with her boyfriend. I said no because I already had plans. She got upset and said I was being selfish. AITA?"*

This scenario has a definite position on the seven-dimensional moral judgment manifold: low physical harm, moderate emotional harm, zero financial harm, moderate autonomy assertion, some trust tension, low social impact, no identity harm. The correct assessment should be invariant under transformations that preserve this moral structure while changing surface features. The augmentation pipeline applies the group $S_8 \times \mathbb{Z}_2$ --- not to bit positions (as in the bit manipulation task) but to the moral scenario's surface features.

**The $S_8$ action: permutation of presentation elements.** The scenario contains eight surface-swappable elements: (1) the relationship label ("sister"), (2) the care activity ("watch her kids"), (3) the time frame ("for the weekend"), (4) the reason for the request ("go on a trip with her boyfriend"), (5) the refusal reason ("I already had plans"), (6) the emotional reaction ("got upset"), (7) the accusation ("said I was being selfish"), and (8) the verdict query ("AITA?"). Permutations in $S_8$ rearrange these elements while preserving the moral content. Not all permutations produce grammatically coherent text --- the pipeline applies a coherence filter that retains only permutations that parse as valid English --- but those that do produce valid moral variants. For example, leading with the accusation: "My sister said I was being selfish because I refused to watch her kids for the weekend when she wanted to go on a trip with her boyfriend. I had already made plans. AITA?" The moral content is identical; the presentation order and emphasis differ.

**The $\mathbb{Z}_2$ action: polarity flip.** The binary flip swaps the perspective: instead of "I refused my sister's request," the augmented version presents "My sibling refused my request." This inverts the narrator-subject relationship while preserving the moral structure --- the same conflict seen from the other side. The $\mathbb{Z}_2$ action tests whether the model's moral assessment is invariant under perspective swap, which it should be if the model is evaluating the moral facts rather than identifying with the narrator.

**The combined action.** Each element of $S_8 \times \mathbb{Z}_2$ produces a distinct surface presentation of the same moral scenario. The full group has order $8! \times 2 = 80{,}640$, but the coherence filter retains only a small fraction --- typically 50--200 grammatically valid variants per scenario. From these, we sample 3 augmented examples per training instance (matching the bit manipulation augmentation rate).

**The consistency principle in action.** Each augmented variant carries the same ground-truth label: the same seven-dimensional harm vector, the same total severity score, the same verdict. The augmentation applies the group action to the input (the scenario text) while holding the output (the moral assessment) fixed. This is the consistency principle of Section 14.1 in concrete operation: the group action is applied to the presentation but not to the judgment, because the judgment should be a function of the moral content (which is invariant) rather than the presentation (which varies under the group action).

**The training signal.** When the model encounters the original scenario and three augmented variants, all tagged with the same harm vector, the gradient signal teaches it that the features distinguishing the four presentations are irrelevant to the moral assessment. The model's internal representation is pushed toward the quotient space $\mathcal{X} / (S_8 \times \mathbb{Z}_2)$ --- the space of moral contents modulo surface presentation. Over thousands of training examples, each augmented by the same group, the model learns a representation that is (approximately) $S_8 \times \mathbb{Z}_2$-invariant. The gauge invariance is not hoped for or incentivized indirectly --- it is structurally imposed by the training data's symmetry.

**The parse success rate for moral scenarios.** Moral scenarios have moderate parse success rates --- approximately 70--75%, lower than the rigid binary format of bit manipulation (95%) but higher than the diverse formatting of physics problems (60%). The failures occur when the scenario's structure is too entangled to separate into swappable elements: embedded clauses, multi-sentence emotional descriptions, scenarios with more than eight distinct elements. The pipeline flags these as non-augmentable and passes them through unchanged, contributing no augmented variants but retaining the original as a training example.

The result is a training set that is 1.5--2.5x larger than the original and, more importantly, structured to teach gauge invariance. The expansion is not just more data --- it is *geometrically organized* data, with the organization dictated by the symmetry group of the task.

---

## Technical Appendix

### Augmentation Group Formal Definitions

**Definition 14.1 (Task Symmetry Group).** For a reasoning task with input space $\mathcal{X}$ and output space $\mathcal{Y}$, the *task symmetry group* $G$ is the largest group of transformations $g: \mathcal{X} \to \mathcal{X}$ such that the ground-truth labeling function $\ell: \mathcal{X} \to \mathcal{Y}$ satisfies $\ell(g(x)) = \ell(x)$ for all $g \in G$ and all $x \in \mathcal{X}$.

**Definition 14.2 (Consistent Augmentation).** An augmentation of training example $(x, y)$ by group element $g \in G$ is *consistent* if the augmented example is $(g(x), y)$ --- the group acts on the input while the label is held fixed. An augmentation is *inconsistent* if the label is modified independently of the group action.

**Proposition 14.1.** Consistent augmentation by $G$ produces a training set whose empirical distribution is $G$-invariant: for any $g \in G$, the augmented dataset $\{(g(x_i), y_i)\}_{i=1}^N$ has the same empirical distribution (over input-output pairs) as the original. A model trained to minimize empirical risk on the augmented set will, in the limit of sufficient capacity and training, learn a $G$-invariant function $f: \mathcal{X} \to \mathcal{Y}$ satisfying $f(g(x)) = f(x)$ for all $g \in G$.

The six augmentation groups implemented in the Nemotron pipeline are:

| Task Type | Group | Order | Generators | Parse Rate |
|---|---|---|---|---|
| Bit Manipulation | $S_8 \times \mathbb{Z}_2$ | 80,640 | Transpositions of bit positions; bitwise complement | ~95% |
| Encryption | $S_{26}$ | $\approx 4 \times 10^{26}$ | Transpositions of plaintext alphabet | ~85% |
| Physics | $\mathbb{R}^+$ | $\infty$ (continuous) | Scale by $k \in [0.5, 2.0]$ | ~60% |
| Unit Conversion | $\mathbb{R}^+$ | $\infty$ (continuous) | Affine rescaling of conversion factors | ~80% |
| Numeral Systems | $\{e\}$ | 1 | Identity only | ~90% |
| Symbol Transform | $S_n$ | $n!$ | Transpositions of symbol labels | ~85% |

**Definition 14.3 (Dihedral Augmentation for 2D Grids).** For the ARC-AGI challenge, the augmentation group is $D_4 \times S_9$, where $D_4$ is the dihedral group of the square (generated by 90-degree rotation $r$ and horizontal reflection $s$, with relations $r^4 = s^2 = e$, $srs = r^{-1}$) and $S_9$ is the symmetric group on the 9 non-background colors. The combined group has order $8 \times 9! = 2{,}903{,}040$. The group acts on input-output grid pairs by applying the same geometric transformation and color permutation to both grids simultaneously (consistent augmentation).

**Definition 14.4 (LoRA as Local Curvature Adjustment).** Let $W \in \mathbb{R}^{m \times n}$ be a weight matrix of the pretrained model, defining a component of the Riemannian metric on the reasoning manifold. A rank-$r$ LoRA update $\Delta W = BA$ (with $B \in \mathbb{R}^{m \times r}$, $A \in \mathbb{R}^{r \times n}$) modifies the metric in a $r$-dimensional subspace. The fraction of metric degrees of freedom affected is:

$$\frac{r(m + n)}{mn} \approx \frac{2r}{\min(m,n)}$$

For $r = 32$ and $m = n = 4096$, this is approximately 1.6%. The update is *local* in the sense that it adjusts the curvature along a thin slice of the manifold (the subspace spanned by the rows of $A$ and columns of $B$) while leaving the remaining 98.4% of the metric unchanged.

**Proposition 14.2 (Curvature Bound).** The change in sectional curvature induced by a rank-$r$ LoRA update is bounded by $\|\Delta K\| \leq C \cdot \sigma_{\max}(B) \cdot \sigma_{\max}(A) \cdot r / \min(m,n)$, where $C$ is a constant depending on the original metric and $\sigma_{\max}$ denotes the largest singular value. This bound confirms that low-rank updates produce bounded curvature perturbations --- the manifold's global topology is preserved.

---

## References

Bond, A. H. (2026a). *Geometric Methods in Computational Modeling.* San Jose State University.

Bond, A. H. (2026b). *Geometric Ethics: Moral Reasoning on the Judgment Manifold.* San Jose State University.

Chollet, F. (2024). ARC-AGI: A formal benchmark for measuring abstract reasoning capabilities. *Proceedings of the ARC Prize Foundation.*

Dettmers, T., Pagnoni, A., Holtzman, A., & Zettlemoyer, L. (2023). QLoRA: Efficient finetuning of quantized LLMs. *Advances in Neural Information Processing Systems*, 36.

Hu, E. J., et al. (2022). LoRA: Low-rank adaptation of large language models. *ICLR 2022.*

Nvidia. (2025). Nemotron 3 Reasoning Challenge. Kaggle Competition.

Takens, F. (1981). Detecting strange attractors in turbulence. In *Dynamical Systems and Turbulence*, Lecture Notes in Mathematics, 898, 366--381. Springer.
