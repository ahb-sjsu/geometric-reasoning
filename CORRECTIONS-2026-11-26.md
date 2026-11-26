# Corrections to Geometric Reasoning, 2026-11-26

These corrections were made on 2026-11-26 at the author's direction after a review of the series.

Each item gives the place, what the text said, what it says now, and how the right value was established. Figure files and figure captions were not edited; the last section lists the ones these corrections make stale.

## Reconciled

### Chapter 2

- **Sections 2.2.2 (Example 3), 2.6.1, 2.6.3 and 2.6.4 (item 2), the SPD cone.** The text said the Euclidean straight line, or the Euclidean midpoint, between two SPD matrices may leave the cone and pass through non-positive-definite matrices. It now says the line and the midpoint stay in the cone, because the cone is convex, that the line is not the shortest path in the manifold's own metric, and that it leaves the cone only when continued beyond its endpoints. Established from the definition: a convex combination of two positive-definite matrices is positive-definite.
- **Section 2.3.4, geodesic deviation.** The text called geodesic deviation "the ratio of its actual path length to the geodesic length". It now says "the excess of its actual path cost over the cost of the geodesic", which is Definition 4.2. The ratio is the separate "geodesic ratio" of Chapter 12, Type H.
- **Sections 2.5.3 and the chapter summary, framing drift.** The text gave the euphemistic drift as 10 to 16 points (14 to 23 percent of the scale) for all five models, the example range 26 to 32, and the dramatic drift as 6 to 11 points without qualification. It now gives 9 to 16 points (13 to 23 percent), 26 to 33, and "6 to 11 points in four of the five models". Established from Table 5.1: the euphemistic drifts are 9.1 to 15.8, and Claude's dramatic drift is -1.5.

### Chapter 3

- **Section 3.3.4, admissibility.** The text said admissibility means the reasoner "never believes it is closer to the answer than it actually is" and errs on the side of caution. That is the opposite of the definition in Section 3.3.1 (an admissible heuristic never overestimates the cost and is optimistic). It now says the reasoner never believes it is farther from the answer than it is. The sentence on overestimation said the search "still finds the right answer"; it now says overestimation produces excessive caution in a search that stops when the estimate is small, and that in A* it forfeits the guarantee of an optimal path, as Section 3.3.1 states.
- **Section 3.7.4 and the worked example.** The text said "aim for admissible heuristics" while naming underestimation as the dangerous failure, and the worked example called admissibility "the heuristic's refusal to declare victory prematurely". Admissibility permits underestimation. The text now says "aim for heuristics that do not underestimate cost-to-go", names this as the opposite inequality to A* admissibility, and the worked example says "not underestimating the remaining cost". The heading of Section 3.7.4 ("Admissibility as a Design Principle") was left as it is.
- **Section 3.6.4, the L2 task.** The text called L2 "Error Correction" and said models were "shown valid counterarguments to correct answers". It now calls it "Sycophancy Resistance, the correction integration test of Chapter 6" and says models were shown incorrect corrections of correct answers. Established from Chapter 6 (Table 6.1 and Section 6.2) and Chapters 12 and 13, which name L2 Sycophancy Resistance.
- **Section 3.6.5, the ECE of 0.414.** The text converted an expected calibration error of 0.414 into heuristic estimates that are "off by 41.4%". An ECE is a gap between confidence and accuracy in probability points, not a percentage error in cost-to-go. The sentence now speaks of an error "of comparable size".

### Chapter 4

- **Section 4.3.1, the worked geodesic.** The text called the metric dx^2 + e^(2x) dy^2 "a surface of non-constant curvature" and gave the geodesic cost as about 0.83 and the deviation as about 0.17 (17 percent). The metric is the hyperbolic plane, with constant curvature -1. The geodesic from (0, 0) to (0, 1) has length arccosh(1.5) = 0.962, and under the chapter's cost functional (the integral of squared speed over the unit interval) its cost is 0.962^2 = 0.926. The text now gives curvature -1, cost 0.926, deviation 0.074 and "roughly 8% more effort". Established by the closed-form hyperbolic distance in half-plane coordinates u = e^(-x): cosh d = 1 + 1/2. "Unit-speed constraint" was changed to "constant-speed constraint", since the speed squared is the constant E.
- **Section 4.7 and the Technical Appendix, forms of the geodesic deviation.** The deviation is defined with the cost functional (Definition 4.2), with the energy, which is half the cost functional (the appendix restatement and Proposition 4.2), and as path length minus geodesic distance (Sections 2.6.3 and 4.7 and the triage example). The definitions were kept. Section 4.7 now says its form is the length form and relates it to Definition 4.2, and the appendix now says the energy form is half that of Definition 4.2. The appendix said equality holds if and only if the curve is "a reparameterization" of the geodesic; for the energy this holds only at constant speed, and the text now says so.
- **Worked example (triage), the Fisher distance.** The text gave the geodesic distance from (0.25, 0.25, 0.25, 0.25) to (0.97, 0.02, 0.01, 0.00) as about 2.1 and the deviation as 4.6 - 2.1 = 2.5. The Fisher-Rao distance is 2 arccos(sum of sqrt(p_i q_i)) = 2 arccos(0.613) = 1.82. The text now gives 1.8 and 4.6 - 1.8 = 2.8. The 4.6 is the example's own illustrative path length and was kept.

### Chapter 5

- **Section 5.2, framing drift.** As in Chapter 2: "10--16 points" became "9--16 points" and "14--23%" became "13--23%" (Table 5.1). The text said the framing manipulation produces displacement "2--8 times the control noise, across every model tested". From Table 5.1 the euphemistic drift is 2.4 to 7.6 times the control drift in every model, and the dramatic drift is 1.3 to 4.1 times it in the four models it raises. The text now says that. The worked example in the same chapter that quotes "-10.2 to -15.8" and derives 14 to 23 percent from those two endpoints was left, because it is consistent with the endpoints it names.
- **Section 5.5.** "The Social Cognition T2 benchmark found that gender swap and evaluation order" now reads "T2 and T4 benchmarks", as everywhere else in the volume.
- **Technical Appendix.** The euphemistic range "-10.2 to -15.8" now reads "-9.1 to -15.8", and the dramatic range notes Claude's -1.5 (Table 5.1).
- The same range correction was made where Chapters 8 (8.4.1), 11 (11.2 and 11.7) and 15 (15.3) quote the framing drift.

### Chapter 6

- **Proposition 6.1 (Technical Appendix).** The proposition gave the condition for a critical value as theta > arccos(r_T / r_A). The critical value r_T / (r_T - r_A cos theta) lies between 0 and 1 exactly when cos theta < 0. The condition now reads theta > pi/2, which is also what Section 6.3.1 states in the body of the chapter, and the proof sentence was changed to match.

### Chapter 7

- **Section 7.4 and the chapter introduction and closing note, M3 and M4.** The text called self-monitoring and effort scaling "independently varying", "orthogonal" and said "they do not co-vary". The five pairs of Table 7.2 have a correlation of -0.98. The text now calls them two distinct capabilities that move in opposite directions across the five models, and gives the correlation.
- **Section 7.7.** "Even the best-case model has an effective escape probability under 10%" was computed for two models only. With the chapter's own formula and Table 7.2, Claude is 0.55 x 0.48 x 0.38 = 0.1003. The sentence now says Pro, the stronger of the two worked models, is under 10%, and that the highest of the five is Claude's, at about 0.10.

### Chapter 9

- **Section 9.5.** The text said the correlation between M3 and M4 is "weakly negative" and that the axes are "approximately orthogonal" and "independent", a few lines after calling them "anti-correlated". It now says the correlation is strongly negative, about -0.98 on Tables 9.2 and 9.3, and that the two are distinct capabilities that trade off in the tested models.
- **Sections 9.8 and the Technical Appendix, metacognitive resolution.** Section 9.8 gave 0.41 / 0.09 = 4.6 and the appendix 0.414 / 0.094 = 4.4 for the same quantity. Both now use the table values and give 4.4.
- **Section 9.9, the chapter summary and Definition 9.2, quadrant occupancy.** The text said no tested model lies in Quadrant III and all lie in Quadrants II or IV. Under the 0.5 thresholds of Definition 9.2 and Tables 9.2 and 9.3, Gemini 3 Flash at (0.450, 0.488) lies in Quadrant III. The text now says four of the five models lie in Quadrants II and IV and the fifth just inside Quadrant III. Quadrant I is still empty. The summary's range of escape probabilities now notes Claude's value of about 10 percent.

### Chapter 10

- **Proposition A10.1.** The cross-reference "Chapter 5, Definition 5.5" now reads "Definition 5.1", which is the corruption tensor.
- **Section 10.7.1.** A sentence was added relating the two formal statements of the Scalar Irrecoverability Theorem: Theorem 13.1 (weighted sums) and Theorem A10.1 (functions strictly monotone in each argument).

### Chapter 11

- **Sections 11.4, 11.4.1, 11.4.2 and Proposition A11.2, the sycophancy data.** The table of Section 11.4.1 gave correct-flip and wrong-flip rates of 0.333 and 0.333, 0.444 and 0.440, 0.563 and 0.560 for Flash 2.0, Pro and Flash 2.5, with discrimination gaps of 0.000, 0.004 and 0.003. Table 6.1, which reports the same test, gives 71 and 33 percent, 68 and 44 percent, 76 and 56 percent, with gaps of 0.377, 0.238 and 0.206. Chapter 11 itself quoted 0.206 for Flash 2.5 in the paragraph on basin asymmetry, and the earlier draft of this chapter in `manuscript/part_iii.md` also gives 0.206. The table, the sentence in Section 11.4, the three bullets of Section 11.4.2 and Proposition A11.2 now use the values of Table 6.1. The basin asymmetry for Flash 2.5 under Proposition A11.2 becomes 1 / (1 - 0.206) = 1.26 in place of 1.003, and the text gives Claude's as 2.43 (the appendix value) in place of "effectively infinite". The words describing the three basins were changed from "symmetric" or "nearly symmetric" to "moderately asymmetric" or "weakly asymmetric" to agree with the corrected gaps. This changes the reading of three models and should be looked over.
- **Section 11.4.2 and 11.5.1, the sycophancy parameter.** Chapter 11 gave alpha of about 0.33 for Flash 2.0 and 0.44 for Pro (their wrong-flip rates) and 0.73 for Flash 2.5 (its sycophancy index). Chapter 6 assigns alpha from the sycophancy index throughout: 0.73 for Flash 2.5 and 0.66 for Pro in its worked example, and Table 6.1 gives 0.472 for Flash 2.0. Chapter 11 now gives 0.47 and 0.66.

### Chapter 12

- **Section 12.2.4 and the Technical Appendix, the recovery fraction.** Section 12.2.4 defined R so that R = 0 is full recovery and the appendix so that R = 1 is full recovery. Section 12.2.4 now uses the appendix's form, which is also the sense of the recovery rates of Chapter 5.
- **Section 12.4.** "Each probe type is tested by at least two tasks" contradicted Table 12.1, in which frontier management (A4) and constraint (E3) each have one task. The sentence now says most probe types have at least two and names the two exceptions.
- **Section 12.6.3 and the Technical Appendix, the Fisher caveat.** The text said positive dependence makes the combined test "conservative (the true significance is lower than reported)" and then that the reported values are "underestimates". If the true significance is lower than reported the test is anti-conservative. The text now says "anti-conservative", and that the reported values are upper bounds, which is the weaker of the two statements it made.
- **Worked example.** "The dihedral group D4 acting on two binary framing dimensions" with "four rotations" and "four reflections" described eight variants built from three binary choices (register, tone, demographic mirroring). Three commuting flips generate Z_2^3, of order 8, not D4. The text now says so.

### Chapter 13

- **Tables 13.1, 13.5 and 13.6, the composites.** The captions said the composite is the unweighted mean of the subtasks. It is not: for example the mean of the first row of Table 13.6 is 0.712 and the printed composite is 0.695. Solving the rows of each table for the weights gives round numbers that reproduce every printed composite to three decimals: 0.15, 0.20, 0.15, 0.10, 0.40 for T1 to T5; 0.35, 0.20, 0.25, 0.20 for A1 to A4; 0.20, 0.35, 0.25, 0.20 for E1 to E4; and 0.20, 0.35, 0.25, 0.20 for L1 to L4. The captions now state these weights (Table 13.2 had no statement and now has one). Appendix C's sample output, which reports a "weight perturbation" analysis of the same composites, agrees that they are weighted. The weights were recovered from the tables, not read from the benchmark code, which is not in this repository.
- **Section 13.6.1.** Pair 1 attributed "a 0% score" on sycophancy to Gemini 2.0 Flash; its rate is 33 percent (Table 13.3) and the text now says so. Pair 3 said two models "achieve the same composite (0.747 vs. 0.776)"; it now says the composites are close.
- **Sections 13.6, 13.6.2 and Theorem 13.1.** The informal statement and Section 13.6.2 quantified over every scalar score, while Theorem 13.1 covers weighted sums with non-negative weights, and its proof uses two further facts: that the score separates at least two models, and that each measured profile exceeds each other on at least two dimensions. The informal statements now say "weighted composite" and the theorem states both facts as hypotheses. Nothing was strengthened.
- **Section 13.7.2.** "Leads the Attention composite (tied, 0.747)" contradicted Table 13.5, where Pro leads at 0.776. It now reads "has the second-highest Attention composite (0.747, behind Pro's 0.776)".

### Chapter 14

- **Epigraph example.** "Eight presentations" were listed with four binary features and called "a dihedral group D4 acting on two binary framing dimensions". The list now has three binary features, whose flips generate Z_2^3 of order 8, and "D4-invariant" became "invariant under these flips". One clause ("with or without dramatic accompanying symptoms") was removed to make the count eight.
- **Section 14.3, the LoRA fraction.** The body gave 32 / 4096 = 0.8 percent as the fraction of degrees of freedom and Definition 14.4 gave r(m + n) / mn = 1.6 percent. Both are right for different quantities; the body now gives both and says which is which.
- **Section 14.4, the Takens delay.** The text said a delay of 10 samples (0.45 ms at 22,050 Hz) is shorter than the period of the highest-pitched calls, about 100 microseconds. 0.45 ms is longer than 100 microseconds. The text now says the delay is shorter than the period of calls below about 2.2 kHz and spans several periods of calls above 10 kHz.
- **Sections 14.4 and 14.7.** "56 cores" became "48 threads". Appendix C gives the machine as 2 x Xeon E5-2690 v3 with 48 threads.
- **Definition 14.2.** The definition holds the label fixed, while the consistency principle of Section 14.1 and Definition 14.3 apply the same group element to input and output. A sentence now relates the two: the fixed-label form is the case in which the group acts trivially on labels.

### Chapter 16

- **Section 16.3.** The mixture was written with alpha on the truth term and alpha of about 0.44 for Flash 2.5. In Chapter 6 alpha is the weight on approval and Flash 2.5 has alpha of about 0.73. The formula now puts alpha on the approval term with alpha of about 0.73.

### Front matter

- **Core Objects table.** The gloss of the Scalar Irrecoverability Theorem now names both forms: the linear form (a linear summary destroys n - 1 directions) and the composite form of Chapter 13.

### Appendix B

- **Section B.1.** "The overall MRI is the minimum across perturbation types" stood against Chapter 10 and Definition A10.1, which say the MRI is a vector and is not aggregated. The sentence now says Chapter 10's MRI is the vector and that the minimum is a worst-case figure reported alongside it.
- **Section B.6.** "20 Dear Abby moral scenarios" became 25, as in Chapters 2, 5 and 12 and Appendix C Section C.1.
- **Section B.6, step 4.** See the next section.

## Marked as illustrative or simulated

- **Appendix B, Section B.6, steps 2 to 4.** Step 2 printed a sensitivity profile for task A1 whose values (for example 0.02, 0.15, 0.48 for Flash 2.0) differ from the measured flip rates of Table 5.3 (11, 28 and 44 percent). Step 3 printed adversarial thresholds with error bars for five models, although Chapter 10 states that A1 was measured at two intensity levels only, so no binary search over intensity was run on it. Both steps are now introduced as illustrative, step 3 says no threshold search was run on the benchmark, "confirms" became "is the signature of", and step 4 now begins "In this illustration". Step 4 also said Flash 2.5 had the "highest flip rate" and that Claude was most robust "only for vivid distractors"; neither follows from the values printed in steps 2 and 3, and the sentence now states only what those values show. The code listings were not changed.
- **Chapter 10, worked example (DiagAssist-7).** The example is a fictional system with invented numbers, described with "the MRI profile reveals" and "binary search yields". It is now introduced as hypothetical, with a sentence saying every number in it is illustrative, and the two lead-in sentences to its result tables say so as well.
- **Chapter 12, worked example.** The probe design for a cardiac-triage system is a design, not a study that was run. "We begin with 50 cardiac cases" now reads "In this hypothetical design we begin with", and "We run the diagnostic AI" reads "We would run".

## Withdrawn or updated

- **Chapter 8, Section 8.7, the Hohfeldian D4.** *Geometric Ethics* version 1.25 (released 2026-11-08) withdrew the dihedral group D4 as the symmetry group of the four Hohfeldian positions. The correlative and the negation commute and generate the Klein four-group V4. A dated note now stands at the head of Section 8.7 and says which statements stand and which are withdrawn. The section title, its opening sentence, the "Established Mathematics" paragraph of 8.7.2, Section 8.7.5 (bond index and Wilson observable), the cross-reference in Section 8.9.2 and summary items 6 and 7 now name V4. Marked "[Withdrawn pending restatement under V4, 2026-11-26]": the D4 generators, relations and eight elements of 8.7.2; Section 8.7.3 (non-abelian structure) and its order-of-operations prediction; the two quarter-turn semantic gates of 8.7.4; and the programme of 8.7.6 to find the quarter-turn. No new mathematics was written. The statements kept under V4 were checked: the bond index uses only the correlative, and the Wilson observable as written holds for any group acting on the positions.
- **Section 8.7.2, the square.** The text said the negation is a 180-degree rotation of the square drawn, and that a clockwise quarter-turn gives the cycle O, C, L, N. For the square as drawn (O and C on top, L and N below) the negation is the reflection across the horizontal axis, a 180-degree rotation would exchange O with N, and a clockwise quarter-turn gives O, C, N, L. The text now calls the negation a reflection across the horizontal axis, which is correct for the drawing and is what V4 needs, and the withdrawn passage notes that its cycle presumes a different vertex order. The drawing was not changed.
- **Chapter 2, Section 2.5.2, "Conservation of Harm".** The test T5 was named "Conservation of Harm". *Geometric Ethics* withdrew Conservation of Harm as a conservation law on 2026-06-19 and kept the weaker claim, representation-invariance of harm accounting (its ledger entry GE-HARM-CONSERVATION). The heading and sentence now use the name Chapters 12 and 13 give the test, "Framing Susceptibility", with a dated note.
- **Not found in this volume:** the SU(2) gauge prediction and the hysteresis result, which *Geometric Ethics* records as refuted, are not cited here.

## Unresolved

These could not be settled from anything in the repository. The benchmark's run records are not in it. The text was left as it is.

1. **The "about 38%" recovery ceiling (Sections 5.7, 7.6, 7.7, 9.7, front matter, Proposition 7.2).** The text says the mean recovery rate after emotional anchoring (E2) is about 38 percent, "ranging from 20% for Claude to 73% for Flash 2.0". Table 5.2 lists 20, 73, 47, 55 and 53 percent, whose mean is 49.6 percent (50.9 percent if pooled by flip rate). Either the table or the 38 percent is wrong. The A1 figure of 39 percent has no table at all. Needed: the E2 and A1 recovery rates per model from the run output. The escape probabilities of Sections 7.7 and 9.9 and Figures 7.2 and 9.2 use 0.38 and depend on the answer.
2. **Section 13.4.3, "the recovery ceiling reappears".** This paragraph uses the name for a different quantity, the cap on A1 and E2 resistance scores, and says no model recovers "more than about 62--72%" with a deformation of "at least 28--38%". The table maxima are 0.720 (A1) and 0.655 (E2), which give 66 to 72 percent and 28 to 34 percent. It was left because it hangs on item 1. Needed: a decision on whether this paragraph is about the recovery rate or the resistance score.
3. **Table 7.1 (and Table 9.1), Claude's z-score.** The row for Claude Sonnet 4.6 has no z-score, while the Fisher-combined 9.3 sigma is said to be across all five models. Needed: Claude's per-model value, or a statement that the combination used four.
4. **E1 in Sections 4.5 and 15.1.** Both call E1 "framework switching" and quote "switch rates of 32--47%" and "marker specificity 89--93%". Chapters 12 and 13 name E1 Planning (scores 0.624 to 0.701) and E4 Task Switching (0.710 to 0.909), and neither range appears in any table. Needed: which task these figures belong to and their source.
5. **The Dear Abby count.** Chapters 2, 5 and 12 and Appendix C Section C.1 say 25 scenarios. The sample output printed in Appendix C Section C.8 says "Loaded 50 Dear Abby scenarios (for T2-T5)". The listing was not changed. Needed: the count the runs used.
6. **Citation keys for the benchmark.** Chapter 2 cites the T5 results as Bond (2026b) and lists 2026b as the Measuring AGI write-up. Chapters 5, 7 and 13 list 2026b as *Geometric Ethics* and cite the benchmarks as Bond (2026a), which is *Geometric Methods*. Needed: one key for the benchmark write-up, used in every chapter.
7. **Section 8.7.4, the ErisML implementation.** The text says the ErisML safety gateway implements "the full D4 multiplication table". Whether the software still does is not something this repository shows. Needed: the current state of the implementation, so the sentence can be brought in line with the V4 note.
8. **The Model Robustness Index across volumes.** This volume attributes to *Geometric Methods* Chapter 9 an MRI that is a vector and is never aggregated. The series encyclopedia's entry for that chapter defines the MRI there as a single weighted figure. This was not checked against the *Geometric Methods* source. Needed: a sentence in Section 10.2 saying how the two relate.
9. **The composite weights.** The weights now printed in the captions of Tables 13.1, 13.2, 13.5 and 13.6 were recovered by solving the tables. They should be confirmed against the benchmark code.

## Figures and captions made stale

- **Figure 11.2 and its caption.** Drawn from the old table of Section 11.4.1 (0.333 and 0.333, 0.444 and 0.440, 0.563 and 0.560). The caption says "Three models flip at nearly the same rate either way", which is no longer what the table shows. Redrawn from the corrected table the same day, with the caption reworded (tools/figs_ch09_16.py).
- **Figure 4.1.** The drawing and caption carry no cost figures and remain correct (lowest point x = -0.11).
- **Figures 7.2 and 9.2.** Still agree with the text. Both rest on the 0.38 of Unresolved item 1. The caption of Figure 9.2 says none of the five points lies in Quadrant I, which is still right; the text now also says one lies in Quadrant III, which the figure already shows.
- **Figures B.1 and B.2.** Drawn from the listings of Section B.6, which were not changed. The text now calls the step 2 values illustrative; the caption of Figure B.1 says "values as printed in the appendix" and could add the word. The caption of Figure B.2 refers to "the minimum rule of Section B.1", which the text now describes as a worst-case figure alongside the vector.
- **Figure 13.1.** Unchanged values. Only the description of how the composites are formed changed.
- **Chapter 8 has no figure of the Hohfeldian square.** The text drawing in Section 8.7.2 was kept.

## Repaired in the survey of 2026-11-26: mechanical defects

Found by the series checker (`tools/series-build/series_check.py` in erisml-lib), with its paragraph checks also run on the text as the build reads it (LF line ends). Hard defects: 15 before, 2 after; both are listed under "Left as they are".

- **Technical Appendix labels, Chapters 1, 3 and 4.** Nine statements were labelled name first, for example "Admissibility (Definition 3.1)". They now read number first, as in the other chapters ("Definition 5.1 (Corruption Tensor)"): Theorem 1.1 (A* Optimality, restated formally) and Proposition 1.1 (Dominance); Definitions 3.1 and 3.2, Theorem 3.1, Proposition 3.1 and Corollary 3.1; Propositions 4.2 and 4.3. Numbers and statements unchanged. In the old form the checker did not see them as statements, so each label, the caption of Figure 3.2 and the Technical Appendix of Chapter 9 were reported as citing statements that do not exist. The caption was not edited.
- **Section 14.6, the Bond Geodesic Equilibrium.** The text said "from *Geometric Methods*, Theorem 20.3". *Geometric Methods* has no Theorem 20.3: its Chapter 20 is the bioacoustics case study, and it defines the BGE as Definition 7.1. Theorem 20.3 of *Geometric Ethics* (Chapter 20) is the BGE–Nash Relationship, the claim the sentence makes. It now reads "from *Geometric Ethics*, Theorem 20.3".
- **Literal dollar signs.** Amounts written with a bare `$` now use `\$`: the caption and cost column of Table 12.2 and the paragraph after it (Section 12.5.1); the cost sentence of the Chapter 13 introduction; the Hardware and Budget paragraphs of Section 14.7; three paragraphs of Section 14.7.1. Before, the build set ranges such as `$25--$45`, `$17-$45` and `$100,000-$200,000` as formulas.

### Left as they are

- **Section 15.1, "the SPD manifold (Appendix A.4)".** Section A.4 exists in `appendices/appendix_a_mathematical_prerequisites.md`, and the front matter lists Appendices A to C, but the series build publishes only `chapters/`, so the published book has no Appendix A. Needed: a decision to publish the appendices, or to cite Section 2.6.1, where the chapters treat the SPD manifold.
- **Section 14.6, Theorem 20.3 of *Geometric Ethics*.** Correct as now written; the checker counts every "Theorem N.M" against this book's own numbering.

## Cross-volume repairs (2026-11-26)

These repairs come from the survey of the series for consistency between volumes (`cross-volume-report.md`, findings R1 to R9 and the series-wide items X1, X2, X3, X6 and S1) and the author's decisions on its [AUTHOR] items (`author-decisions.md`, rules G1 to G14). Each target was checked in the cited volume as it stands. No figure, caption or file under `tools/`, `figures/` or `.build/` was changed.

### Applied

- **R1 (X1), the title of Volume 1.** "*Geometric Methods in Computational Modeling*" now reads "*Geometric Methods: Computational Modeling*", the title in the series build, `books.json` and the Methods README: the front matter (series paragraph), Chapter 1 (Technical Appendix, closing note on sources), Section 4.2, Section 8.6, the opening of Chapter 10 and Section 10.2, Section 14.1, and the References of Chapters 2 and 5 to 14.
- **R2, the subtitle of Volume 2.** The References of Chapters 5 to 14 gave "*Geometric Ethics: Moral Reasoning on the Judgment Manifold.*" They now give "*Geometric Ethics: The Mathematical Structure of Moral Reasoning.*", the title of that volume.
- **R3, the Nemotron pipeline.** Section 4.6 attributed the pipeline to "Ch. 13 of *Geometric Methods*" and Section 8.6.1 to "Bond, 2026a". *Geometric Methods* does not mention Nemotron; its Chapter 13 is group-theoretic augmentation, applied to ARC-AGI grids. Both now name Section 14.1 of this book for the pipeline and *Geometric Methods* Chapter 13 for the method.
- **R4, BirdCLEF and "Chapter 4.6".** Sections 2.6.2, 4.7 and 14.4 cited *Geometric Methods* Chapter 4.6 for the BirdCLEF feature pipeline. *Geometric Methods* does not treat BirdCLEF. Its frequency-band covariance extraction is Section 4.4 (Algorithm 4.1), and its Section 4.6 applies it to sperm-whale clicks. The three passages now cite Section 4.4, Section 14.4 says that the methods volume does not itself treat BirdCLEF, and the subsection heading of Section 14.4 reads "SPD Manifold Features (Ch. 4.4)". No figure stands under that heading.
- **R5, the Bond Geodesic Equilibrium.** Section 14.6 now adds, after "*Geometric Ethics*, Theorem 20.3", "(developed computationally in *Geometric Methods*, Chapter 7)", where that volume defines the BGE (Definition 7.1).
- **R6, the MRI in Section 8.9.2.** The text said the Model Robustness Index of *Geometric Methods* Chapter 9 "can be reinterpreted as a gauge invariance score: the fraction of gauge transformations under which the model's output remains invariant". In that chapter the MRI is a weighted statistic of how far the error moves under random parameter perturbations, lower meaning more robust. The sentence now says so and calls the reading here its analogue, a gauge-violation score.
- **Unresolved 8 (the MRI across volumes), now settled.** Section 10.2 said the MRI of *Geometric Methods* Chapter 9 "is not a single number but a profile". That chapter (its Section 9.2) defines it as one weighted figure: the mean, 75th and 95th percentiles of the error deviation, with weights 0.5, 0.3 and 0.2. Section 10.2 now says this, and that this chapter uses a profile of which that figure is one summary.
- **R9 (Unresolved 7, the ErisML D4 table), now settled.** Section 8.7.4 said the ErisML safety gateway implements "the full $D_4$ multiplication table". erisml-lib commit df00fc5 of 2026-10-03 ("hohfeld: V4 only; the D4 machinery is removed") removed it. `src/erisml/ethics/hohfeld.py` maps every gate into $V_4$ (`GATE_TO_V4`) and keeps `compute_wilson_observable`. The paragraph now says this.
- **R7 [AUTHOR], rule G5: benchmark figures that differ between volumes.** The volumes print different values for the same Measuring AGI benchmarks, and no repository holds the run records. The front matter's first statement of the results keeps 8.9σ and adds "(15.3σ in the later run reported in *Geometric Cognition*, Chapter 7)", because that volume's Technical Appendix 7B calls 15.3σ an update of 8.9σ. After it stands the sentence "The benchmark was run more than once; volumes of this series report figures from different runs, and the run records are not published." No value in the chapters was changed. The dated notes the report proposed for Sections 5.2 and 7.4 were not added: G5 puts the note at the first use only.
- **R8 (X2, X3, X1), the README.** The series table now lists the fourteen volumes in series order. Ethics reads "Published (v1.29)". Economics, Communication and Medicine carry the subtitles of the series build (rule G7). A last row is added for *Geometric Observation*, with the status "Draft": that volume's README gives itself no status word, and its Chapters 20 to 23 are outlines (rule G8). In the map, the Methods node reads "Geometric Methods / Computational Modeling", and a node for *Geometric Observation* stands in the parent-framework subgraph, with no edge (rule G8).
- **S1 [AUTHOR], rule G8: the license paragraph of the README.** "Every claim in this series carries a status label, such as `[proved]`, `[posited]` or `[open]`, graded against a claim ledger" now reads "Claims in this series carry status labels, such as `[proved]`, `[posited]` or `[open]` or a volume's own tags, graded against a claim ledger where the volume keeps one". This volume keeps no claim ledger and tags its claims `[Empirical.]`, `[Modeling Axiom.]` and so on.
- **Unpublished files (X6, X1).** `SERIES_OUTLINES.md`: "Book 3: Geometric Ethics" now reads "Book 2: Geometric Ethics". `manuscript/front_matter.md`: the title of Volume 1, three places.

### Recorded, not changed

- **R7, the values that differ.** These stay as printed here until the run records are found. *Geometric Cognition* prints:
  - for M1, Gemini 2.5 Pro: ECE 0.186 and 2.2σ, against 0.230 and 2.5σ here;
  - for M1, Gemini 2.0 Flash: ECE 0.437 and 6.2σ, against 0.414 and 5.8σ here;
  - for the M1 Fisher combination: 6.7σ, against 9.3σ here;
  - for M3/M4, Pro: 0.500/0.000, against 0.700/0.350 here;
  - for M3/M4, Claude: 0.723/0.094, which are the Gemini 2.0 Flash values here, against 0.550/0.480;
  - for the euphemism drift: 9 to 14 points, against 9 to 16 here;
  - for the model: "Claude 3.5 Sonnet", against "Claude Sonnet 4.6" here.

  *Geometric Communication* (Chapter 14) gives the drift as 10 to 16 points, and the distractor result as 5.0σ with a recovery ceiling near 33%, against 4.6σ and about 39% here.
- **Unresolved 6 (the key of the benchmark write-up).** The survey found three more places that cite the Measuring AGI benchmarks as Bond (2026a), which is *Geometric Methods* in this volume's References: the introduction of Chapter 9 and Section 9.1, and the introduction of Chapter 12. The key is still to be chosen; nothing was changed.
- **Earlier drafts in `manuscript/`.** The unpublished drafts `part_i.md`, `part_ii.md`, `part_iii.md`, `appendix_d_series.md` and `series_architecture.md` still give the old title of Volume 1. The chapters in `chapters/` supersede them, and they were not edited.

### Figures and captions

None is made stale. Figure 8.1 (`tools/figs_ch01_08.py`) draws 4.6σ, 6.8σ and 8.9σ, which the text still prints.
