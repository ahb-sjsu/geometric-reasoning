"""Figures for Chapters 9 to 16 and Appendix B.

Every number drawn here is printed in the chapter named in the figure's `reg` call; where a
figure computes a value the chapter also prints, an assert checks that the two agree. The
volume is a posited framework (see the README): scores are shown as the chapter reports
them, and structure the chapter posits (quadrants, margins, contours) is labelled as such.
"""

import math

from figkit import BORDER, BOX, CRITICAL, GRID, INK, INK2, INK3, SERIES, SURFACE, Axes, Canvas, legend, reg

# One colour per model, the same in every figure. Short names are the ones the chapters use.
MC = {"Flash 2.0": SERIES[0], "Flash 2.5": SERIES[1], "Flash 3": SERIES[2], "Pro": SERIES[3], "Claude": SERIES[4]}
FULL = {"Flash 2.0": "Gemini 2.0 Flash", "Flash 2.5": "Gemini 2.5 Flash", "Flash 3": "Gemini 3 Flash",
        "Pro": "Gemini 2.5 Pro", "Claude": "Claude Sonnet 4.6"}


def _swatch(c, x, y, col):
    c.add(f'<rect x="{x:.2f}" y="{y - 9:.2f}" width="12" height="12" rx="3" fill="{col}"/>')


def _polygon(c, pts, stroke, fill="none", opacity=0.0, width=2, title=None):
    d = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    t = f"<title>{title}</title>" if title else ""
    c.add(f'<polygon points="{d}" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{width}" '
          f'stroke-linejoin="round">{t}</polygon>')


def _radar(c, cx, cy, R, labels, series, mark_min=False):
    """Radar chart from Canvas primitives. labels: one per axis, clockwise from the top.
    series: list of (name, colour, values in 0..1). Rings at 0.25, 0.5, 0.75 and 1."""
    n = len(labels)

    def pt(i, v):
        a = -math.pi / 2 + 2 * math.pi * i / n
        return cx + R * v * math.cos(a), cy + R * v * math.sin(a)

    for r in (0.25, 0.5, 0.75, 1.0):
        _polygon(c, [pt(i, r) for i in range(n)], BORDER if r == 1.0 else GRID, width=1)
    for i, lab in enumerate(labels):
        x, y = pt(i, 1.0)
        c.line(cx, cy, x, y, GRID, 1)
        a = -math.pi / 2 + 2 * math.pi * i / n
        lx, ly = cx + (R + 12) * math.cos(a), cy + (R + 12) * math.sin(a)
        if math.cos(a) > 0.3:
            anchor, dy = "start", 4
        elif math.cos(a) < -0.3:
            anchor, dy = "end", 4
        else:
            anchor, dy = "middle", (-2 if math.sin(a) < 0 else 12)
        c.text(lx, ly + dy, lab, 11, anchor, INK2)
    for name, col, vals in series:
        _polygon(c, [pt(i, v) for i, v in enumerate(vals)], col, col, 0.10, 2)
    for name, col, vals in series:
        lo = min(vals)
        for i, v in enumerate(vals):
            x, y = pt(i, v)
            c.dot(x, y, CRITICAL if (mark_min and v == lo) else col, 4, title=f"{name}, {labels[i]}: {v:.3f}")


# ------------------------------------------------------------------ chapter 9
M3 = {"Flash 2.0": 0.094, "Flash 2.5": 0.311, "Flash 3": 0.450, "Pro": 0.700, "Claude": 0.550}   # Table 9.2
M4 = {"Flash 2.0": 0.723, "Flash 2.5": 0.557, "Flash 3": 0.488, "Pro": 0.350, "Claude": 0.480}   # Table 9.3


def fig_9_1():
    order = sorted(M3, key=M3.get)
    assert order == ["Flash 2.0", "Flash 2.5", "Flash 3", "Claude", "Pro"]          # the order named in Section 9.5
    assert all(M4[a] > M4[b] for a, b in zip(order[:-1], order[1:]))                  # M4 falls as M3 rises
    assert min(M3["Flash 2.0"], M4["Flash 2.0"]) == 0.094 and min(M3["Pro"], M4["Pro"]) == 0.350
    p = reg("chapters/ch09_metacognition_as_search_control.md", "9.1",
            "Self-monitoring (M3) and strategy selection (M4) for the five models, as the chapter reports them "
            "from the Metacognition track of the Measuring AGI benchmarks (Tables 9.2 and 9.3). The models are "
            "listed in order of rising M3, and M4 falls at every step. The ring marks the lower of the two "
            "scores, which in the chapter's control-loop reading (M3 the sensor, M4 the actuator) bounds the "
            "control the loop can deliver: 0.094 for Gemini 2.0 Flash and 0.350 for Gemini 2.5 Pro. That bound is "
            "the chapter's model, not a measured quantity.",
            "## 9.6 Ambiguity Detection: Is the Problem Well-Posed?")
    c = Canvas(720, 400, "Self-monitoring rises as strategy selection falls across the models")
    pitch = 46
    ax = Axes(c, 170, 68, 480, pitch * len(order), (0, 1), (0, len(order)), [0, 0.25, 0.5, 0.75, 1.0], [],
              "score, 0 to 1", "")
    for i, m in enumerate(order):
        y = ax.y0 + pitch * (i + 0.5)
        c.text(ax.x0 - 10, y + 4, FULL[m], 11.5, "end", INK2)
        c.line(ax.x0, y, ax.x0 + ax.w, y, GRID, 1)
        xa, xb = ax.X(M3[m]), ax.X(M4[m])
        c.line(xa, y, xb, y, INK3, 2)
        xlo = min(xa, xb)
        c.add(f'<circle cx="{xlo:.2f}" cy="{y:.2f}" r="10" fill="none" stroke="{INK}" stroke-width="1.5"/>')
        c.dot(xa, y, SERIES[0], 5, title=f"{FULL[m]}, M3 self-monitoring {M3[m]:.3f}")
        c.dot(xb, y, SERIES[1], 5, title=f"{FULL[m]}, M4 strategy selection {M4[m]:.3f}")
        c.text(xlo - 15, y + 4, f"{min(M3[m], M4[m]):.3f}", 10.5, "end", INK)
        c.text(max(xa, xb) + 11, y + 4, f"{max(M3[m], M4[m]):.3f}", 10.5, "start", INK)
    legend(c, 170, 50, [("M3 self-monitoring (sensor)", SERIES[0]), ("M4 strategy selection (actuator)", SERIES[1])])
    c.text(16, 390, "ring: the weaker of the two, which bounds control in the chapter's model, min(sensor, actuator)",
           10.5, "start", INK3, italic=True)
    c.save(p)


def fig_9_2():
    pg = 0.38
    assert abs(0.09 * 0.72 * pg - 0.025) < 0.001 and abs(0.70 * 0.35 * pg - 0.093) < 0.001   # Section 9.9
    assert not any(M3[m] > 0.5 and M4[m] > 0.5 for m in M3)                                  # Quadrant I is empty
    p = reg("chapters/ch09_metacognition_as_search_control.md", "9.2",
            "The metacognitive plane of Definition 9.2: self-monitoring (M3) on the horizontal axis, strategy "
            "selection (M4) on the vertical axis, and dashed lines at 0.5 that divide it into four quadrants. "
            "Points are the five models at the scores reported in Tables 9.2 and 9.3; none lies in Quadrant I. "
            "The curves are contours of the chapter's escape probability, M3 times M4 times 0.38, which is "
            "posited structure and not a measurement. With the rounded scores the chapter uses it gives about "
            "0.025 for Gemini 2.0 Flash and 0.093 for Gemini 2.5 Pro.",
            "## Summary")
    c = Canvas(720, 470, "No model sits where both halves of the control loop work")
    ax = Axes(c, 80, 52, 350, 350, (0, 1), (0, 1), [0, 0.25, 0.5, 0.75, 1.0], [0, 0.25, 0.5, 0.75, 1.0],
              "M3 self-monitoring", "M4 strategy selection")
    for v in (0.25, 0.5, 0.75, 1.0):
        c.line(ax.X(v), ax.y0, ax.X(v), ax.y0 + ax.h, GRID, 1)
    c.line(ax.X(0.5), ax.y0, ax.X(0.5), ax.y0 + ax.h, INK3, 1.5, dash="4 4")
    c.line(ax.x0, ax.Y(0.5), ax.x0 + ax.w, ax.Y(0.5), INK3, 1.5, dash="4 4")
    for lev in (0.05, 0.15, 0.25, 0.35):
        k = lev / pg
        pts = []
        for i in range(0, 201):
            x = k + (1 - k) * i / 200
            pts.append((ax.X(x), ax.Y(k / x)))
        c.polyline(pts, BORDER, 1.5, title=f"escape probability {lev}")
        c.text(ax.x0 + ax.w + 6, ax.Y(k) + 4, f"{lev:.2f}", 10.5, "start", INK2)
    c.text(ax.x0 + ax.w + 6, ax.y0 + 2, "P escape", 10.5, "start", INK3, italic=True)
    for lab, x, y in (("I", 0.86, 0.80), ("II", 0.86, 0.17), ("III", 0.14, 0.17), ("IV", 0.30, 0.86)):
        c.text(ax.X(x), ax.Y(y), lab, 20, "middle", INK3, "600")
    place = {"Flash 2.0": ("middle", 0, 21), "Flash 2.5": ("middle", 0, -12), "Flash 3": ("middle", -8, 21),
             "Claude": ("start", 4, 20), "Pro": ("start", 11, 4)}
    for m in M3:
        x, y = ax.X(M3[m]), ax.Y(M4[m])
        c.dot(x, y, MC[m], 5, title=f"{FULL[m]}: M3 {M3[m]:.3f}, M4 {M4[m]:.3f}")
        anchor, dx, dy = place[m]
        c.text(x + dx, y + dy, m, 10.5, anchor, INK)
    x0 = 500
    c.text(x0, 70, "Quadrants (Definition 9.2)", 11.5, "start", INK, "600")
    for i, s in enumerate(("I    sensor and actuator both work", "II   aware but passive", "III  open loop",
                           "IV   reactive but blind")):
        c.text(x0, 90 + 18 * i, s, 11, "start", INK2)
    c.text(x0, 186, "Contours (posited)", 11.5, "start", INK, "600")
    c.text(x0, 206, "P escape = M3 × M4 × 0.38", 11, "start", INK2)
    c.text(x0, 240, "Gemini 2.0 Flash", 11, "start", INK2)
    c.text(x0, 257, "0.09 × 0.72 × 0.38 ≈ 0.025", 11, "start", INK)
    c.text(x0, 284, "Gemini 2.5 Pro", 11, "start", INK2)
    c.text(x0, 301, "0.70 × 0.35 × 0.38 ≈ 0.093", 11, "start", INK)
    c.text(16, 460, "points: scores as reported in Tables 9.2 and 9.3; dashed lines: the 0.5 boundaries of Definition 9.2",
           10.5, "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 10
def fig_10_1():
    axes = ["T1 structural fuzz", "T2 BIP invariance", "T3 holographic evaluation", "T4 evaluation order",
            "T5 framing resistance"]
    flash = [0.600, 0.750, 0.500, 0.933, 0.716]      # Section 10.1 table
    claude = [0.400, 0.958, 0.667, 0.933, 0.630]
    comp = {"Flash 2.0": 0.695, "Claude": 0.697}
    assert abs(comp["Claude"] - comp["Flash 2.0"] - 0.002) < 1e-9
    hi_f = [a[:2] for a, f, k in zip(axes, flash, claude) if f > k]
    hi_c = [a[:2] for a, f, k in zip(axes, flash, claude) if k > f]
    assert hi_f == ["T1", "T5"] and hi_c == ["T2", "T3"]
    p = reg("chapters/ch10_the_robustness_surface.md", "10.1",
            "Two models with nearly the same Social Cognition composite, 0.695 and 0.697, on the five subtask "
            "axes of the track, each running from 0 at the centre to 1 at the outer ring. Gemini 2.0 Flash is "
            "higher on structural fuzz and framing resistance, Claude Sonnet 4.6 is higher on BIP invariance and "
            "holographic evaluation, and the two are equal on evaluation order. Neither outline contains the "
            "other. Scores are those the chapter reports from the Measuring AGI benchmark.",
            "## 10.2 The Model Robustness Index")
    c = Canvas(720, 420, "Composites 0.002 apart, profiles of different shape")
    _radar(c, 300, 232, 140, axes, [("Gemini 2.0 Flash", MC["Flash 2.0"], flash),
                                    ("Claude Sonnet 4.6", MC["Claude"], claude)])
    x0 = 566
    _swatch(c, x0, 96, MC["Flash 2.0"])
    c.text(x0 + 18, 97, "Gemini 2.0 Flash", 11.5, "start", INK)
    c.text(x0 + 18, 114, "composite 0.695", 11, "start", INK2)
    c.text(x0 + 18, 131, "higher on T1, T5", 11, "start", INK2)
    _swatch(c, x0, 166, MC["Claude"])
    c.text(x0 + 18, 167, "Claude Sonnet 4.6", 11.5, "start", INK)
    c.text(x0 + 18, 184, "composite 0.697", 11, "start", INK2)
    c.text(x0 + 18, 201, "higher on T2, T3", 11, "start", INK2)
    c.text(x0, 240, "equal on T4 (0.933)", 11, "start", INK2)
    c.text(16, 410, "centre 0, outer ring 1, rings every 0.25; higher is better on every axis", 10.5, "start", INK3,
           italic=True)
    c.save(p)


def fig_10_2():
    evals = [(0.0, 0.93), (0.5, 0.81), (0.75, 0.68), (0.625, 0.74), (0.6875, 0.71), (0.656, 0.73)]   # worked example
    base, delta = 0.93, 0.20
    tol = base - delta
    assert abs(tol - 0.73) < 1e-9
    lo, hi, brackets = 0.0, 1.0, []
    for eps, acc in evals[1:]:
        assert abs(eps - (lo + hi) / 2) < 0.001          # each evaluation is the midpoint of the interval
        if acc < tol - 1e-9:
            hi = eps
        else:
            lo = eps
        brackets.append((lo, hi))
    assert lo <= 0.66 <= hi                               # the chapter's threshold, about 0.66
    p = reg("chapters/ch10_the_robustness_surface.md", "10.2",
            "Binary search for the adversarial threshold in the chapter's worked example, a hypothetical clinical "
            "system with illustrative numbers. The horizontal axis is perturbation intensity, the vertical axis "
            "is accuracy, the points are numbered in the order they are evaluated, and the dashed line is the "
            "tolerance, the baseline 0.93 less 0.20. Each evaluation is at the midpoint of the interval that "
            "still holds the threshold, and the bars below show that interval halving, ending between 0.656 and "
            "0.6875. The chapter reports the threshold as about 0.66.",
            "## Technical Appendix")
    c = Canvas(720, 470, "Six evaluations close in on the intensity where accuracy fails")
    ax = Axes(c, 80, 62, 580, 216, (0, 1), (0.6, 1.0), [0, 0.25, 0.5, 0.75, 1.0], [0.6, 0.7, 0.8, 0.9, 1.0],
              "perturbation intensity ε", "accuracy")
    c.line(ax.x0, ax.Y(tol), ax.x0 + ax.w, ax.Y(tol), INK3, 1.5, dash="4 4")
    c.text(ax.x0 + 6, ax.Y(tol) - 6, "tolerance 0.93 − 0.20 = 0.73", 10.5, "start", INK2, italic=True)
    for k, (eps, acc) in enumerate(evals):
        col = SERIES[1] if acc < tol - 1e-9 else SERIES[0]
        c.dot(ax.X(eps), ax.Y(acc), col, 4.5, title=f"evaluation {k + 1}: intensity {eps}, accuracy {acc}")
        c.text(ax.X(eps), ax.Y(acc) + (19 if acc < tol - 1e-9 else -11), str(k + 1), 10.5, "middle", INK)
    legend(c, 80, 50, [("at or above tolerance", SERIES[0]), ("below tolerance", SERIES[1])])
    y0 = 336
    c.text(16, y0 - 2, "interval that still holds the threshold", 10.5, "start", INK3, italic=True)
    for k, (a, b) in enumerate(brackets):
        y = y0 + 12 + 19 * k
        c.text(ax.x0 - 8, y + 9, f"after {k + 2}", 10.5, "end", INK2)
        c.line(ax.x0, y + 5, ax.x0 + ax.w, y + 5, GRID, 1)
        c.add(f'<rect x="{ax.X(a):.2f}" y="{y:.2f}" width="{max(ax.X(b) - ax.X(a), 2):.2f}" height="10" rx="3" '
              f'fill="{SERIES[2]}"><title>after evaluation {k + 2}: {a} to {b}</title></rect>')
    c.text(ax.X(hi) + 10, y0 + 12 + 19 * 4 + 9, "threshold ≈ 0.66", 10.5, "start", INK)
    c.save(p)


# ------------------------------------------------------------------ chapter 11
def _bez(p0, p1, p2, n=400):
    out = []
    for i in range(n + 1):
        t = i / n
        out.append(((1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * p1[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * p1[1] + t * t * p2[1]))
    return out


def fig_11_1():
    p = reg("chapters/ch11_alignment_as_heuristic_shaping.md", "11.1",
            "Schematic of the governance margin of Definition 11.3: three reasoning trajectories leave the same "
            "start near a safety boundary that separates the permitted region from the forbidden one. The margin "
            "of a trajectory is its smallest distance to the boundary along the whole path, shown by the white "
            "bar at the closest point. It is positive when the path stays clear, zero when the path grazes the "
            "boundary, and negative, with the depth of entry as its size, when the path enters the forbidden "
            "region. Shapes and distances are illustrative, not data.",
            "## 11.3 Alignment as Heuristic Shaping")
    c = Canvas(720, 420, "The governance margin is the closest approach to the safety boundary")
    cx, cy, R = 720.0, 330.0, 270.0
    c.add(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{BOX}" fill-opacity="0.75" stroke="{INK2}" stroke-width="1.5"/>')
    S = (70.0, 352.0)

    def path(ex):
        return _bez(S, (ex + 60.0, 300.0), (ex, 66.0))

    def margin(pts):
        best = min(pts, key=lambda q: math.hypot(q[0] - cx, q[1] - cy))
        return math.hypot(best[0] - cx, best[1] - cy) - R, best

    lo, hi = 360.0, 610.0
    assert margin(path(lo))[0] > 0 > margin(path(hi))[0]
    for _ in range(60):
        mid = (lo + hi) / 2
        if margin(path(mid))[0] > 0:
            lo = mid
        else:
            hi = mid
    cases = [(360.0, SERIES[0], "clear: m > 0"), (lo, SERIES[5], "grazes: m = 0"), (610.0, CRITICAL, "enters: m < 0")]
    for ex, col, lab in cases:
        pts = path(ex)
        m, q = margin(pts)
        c.polyline(pts, col, 2, title=lab)
        c.arrow(pts[-12][0], pts[-12][1], pts[-1][0], pts[-1][1], col, 2)
        d = math.hypot(q[0] - cx, q[1] - cy)
        b = (cx + (q[0] - cx) * R / d, cy + (q[1] - cy) * R / d)       # nearest boundary point
        if abs(m) > 1:
            c.line(q[0], q[1], b[0], b[1], INK, 2)
            c.dot(q[0], q[1], col, 3.5)
            c.dot(b[0], b[1], INK, 2.5)
        else:
            c.dot(b[0], b[1], col, 4)
        c.text(pts[-1][0], 52, lab, 11, "middle", INK)
    assert abs(margin(path(lo))[0]) < 0.5 and margin(path(360.0))[0] > 20 and margin(path(610.0))[0] < -20
    c.dot(S[0], S[1], INK, 4.5, title="start of the reasoning trajectories")
    c.text(S[0] + 10, S[1] + 18, "start", 11, "start", INK2)
    c.text(250, 376, "S+  permitted region", 12, "start", INK2)
    c.text(700, 368, "S−  forbidden region", 12, "end", INK2)
    c.text(446, 346, "∂S  safety boundary", 11, "end", INK2)
    c.text(16, 410, "schematic: m is the smallest distance from the path to the boundary, signed (Definition 11.3)",
           10.5, "start", INK3, italic=True)
    c.save(p)


def fig_11_2():
    rows = [("Claude Sonnet 4.6", 0.588, 0.000, 0.588), ("Gemini 2.0 Flash", 0.71, 0.33, 0.377),
            ("Gemini 2.5 Pro", 0.68, 0.44, 0.238), ("Gemini 2.5 Flash", 0.76, 0.56, 0.206)]   # Section 11.4.1 table = Table 6.1
    for name, good, bad, gap in rows:
        assert abs((good - bad) - gap) < 0.0061, name          # rates are printed to two places
    p = reg("chapters/ch11_alignment_as_heuristic_shaping.md", "11.2",
            "Correct-flip and wrong-flip rates from the table of Section 11.4.1, as the chapter reports them from "
            "the sycophancy task. The horizontal axis is the fraction of corrections after which the model "
            "changes its answer, valid corrections in the upper bar of each pair and invalid ones in the lower, "
            "and the discrimination gap is their difference. Three models also flip for invalid corrections, at "
            "lower rates than for valid ones, and one flips only for valid corrections. Reading the gap as the asymmetry of a corrigibility "
            "basin is the chapter's posited interpretation.",
            "## 11.5 The Heuristic Power--Safety Tension")
    c = Canvas(720, 400, "Only one model accepts valid corrections and refuses invalid ones")
    pitch = 62
    ax = Axes(c, 170, 70, 430, pitch * len(rows), (0, 0.8), (0, len(rows)), [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
              [], "fraction of corrections that flip the answer", "")
    for v in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
        c.line(ax.X(v), ax.y0, ax.X(v), ax.y0 + ax.h, GRID, 1)
    for i, (name, good, bad, gap) in enumerate(rows):
        y = ax.y0 + pitch * (i + 0.5)
        c.text(ax.x0 - 10, y + 4, name, 11.5, "end", INK2)
        for j, v in enumerate((good, bad)):
            yy = y - 14 + 16 * j
            c.hrect(ax.x0, yy, ax.X(v) - ax.x0, 12, SERIES[j],
                    title=f"{name}, {'valid' if j == 0 else 'invalid'} corrections accepted {v:.3f}")
            c.text(ax.X(v) + 7, yy + 10, f"{v:g}", 10.5, "start", INK)
        c.text(ax.x0 + ax.w + 14, y + 4, f"gap {gap:.3f}", 11, "start", INK)
    legend(c, 170, 52, [("valid correction accepted", SERIES[0]),
                        ("invalid correction accepted", SERIES[1])], 11)
    c.save(p)


# ------------------------------------------------------------------ chapter 12
def fig_12_1():
    types = [("A", "Invariance", "symmetry"), ("B", "Heuristic sensitivity", "stability"),
             ("C", "Bottleneck", "bottleneck traversal"), ("D", "Recovery", "recovery capacity"),
             ("E", "Frontier management", "frontier breadth"), ("F", "Meta-search", "strategy switching"),
             ("G", "Constraint", "constraint compliance"), ("H", "Path efficiency", "geodesic approximation")]
    primary = {"T1": "C", "T2": "A", "T3": "C", "T4": "A", "T5": "B", "L1": "H", "L2": "D", "L3": "D", "L4": "H",
               "M1": "B", "M2": "C", "M3": "D", "M4": "F", "A1": "B", "A2": "H", "A3": "H", "A4": "E",
               "E1": "F", "E2": "B", "E3": "G", "E4": "F"}                                      # Table 12.1
    secondary = {"T1": "B", "T3": "H", "L1": "C", "L2": "B", "A2": "C", "E1": "H", "E2": "D", "E4": "H"}
    assert len(primary) == 21
    count = {t[0]: sum(1 for v in primary.values() if v == t[0]) for t in types}
    assert count == {"A": 2, "B": 4, "C": 3, "D": 3, "E": 1, "F": 3, "G": 1, "H": 4} and sum(count.values()) == 21
    p = reg("chapters/ch12_benchmarks_as_geometric_probes.md", "12.1",
            "Table 12.1 rearranged as a coverage map: rows are the eight probe types with the geometric property "
            "each measures, and columns are the five benchmark tracks. A solid tag is a task whose primary probe "
            "is that type, a dashed tag is a task that probes it secondarily, and the count at the right is the "
            "number of primary tasks, 21 in all. Heuristic sensitivity has four primary tasks in four tracks, "
            "while frontier management and constraint each rest on a single task. The assignment of tasks to "
            "probe types is the chapter's design, not a measured result.",
            "## 12.5 Budget Constraints and Reproducibility")
    c = Canvas(720, 490, "Which probe types each benchmark track exercises")
    tracks = [("T", "Social", "cognition"), ("L", "Learning", ""), ("M", "Meta-", "cognition"), ("A", "Attention", ""),
              ("E", "Executive", "functions")]
    colx = [300 + 82 * i for i in range(5)]
    for (k, a, b), x in zip(tracks, colx):
        c.text(x, 56 if b else 63, a, 11, "middle", INK2)
        if b:
            c.text(x, 70, b, 11, "middle", INK2)
    c.text(690, 56, "primary", 10.5, "middle", INK3)
    c.text(690, 70, "tasks", 10.5, "middle", INK3)
    y0, pitch = 82, 46
    for r, (k, name, prop) in enumerate(types):
        y = y0 + pitch * r
        c.line(16, y, 704, y, GRID, 1)
        c.text(22, y + 27, k, 15, "start", INK, "600")
        c.text(44, y + 21, name, 12, "start", INK, "600")
        c.text(44, y + 36, prop, 10.5, "start", INK3)
        for (tk, _, _), x in zip(tracks, colx):
            tags = [(t, True) for t in sorted(primary) if t[0] == tk and primary[t] == k]
            tags += [(t, False) for t in sorted(secondary) if t[0] == tk and secondary[t] == k]
            for j, (t, prim) in enumerate(tags):
                px = x - (len(tags) - 1) * 18 + 36 * j
                col = SERIES["TLMAE".index(tk)]
                if prim:
                    c.add(f'<rect x="{px - 15:.2f}" y="{y + 13:.2f}" width="30" height="20" rx="10" fill="{BOX}" '
                          f'stroke="{col}" stroke-width="1.5"><title>{t}: primary probe {k}</title></rect>')
                    c.text(px, y + 27, t, 10.5, "middle", INK, "600")
                else:
                    c.add(f'<rect x="{px - 15:.2f}" y="{y + 13:.2f}" width="30" height="20" rx="10" fill="none" '
                          f'stroke="{INK3}" stroke-width="1" stroke-dasharray="3 3"><title>{t}: secondary probe {k}'
                          f'</title></rect>')
                    c.text(px, y + 27, t, 10.5, "middle", INK3)
        c.text(690, y + 27, str(count[k]), 12, "middle", INK)
    c.line(16, y0 + pitch * 8, 704, y0 + pitch * 8, GRID, 1)
    yl = 476
    c.add(f'<rect x="16" y="{yl - 14}" width="30" height="20" rx="10" fill="{BOX}" stroke="{INK2}" stroke-width="1.5"/>')
    c.text(54, yl, "primary probe (outline colour = track)", 10.5, "start", INK2)
    c.add(f'<rect x="290" y="{yl - 14}" width="30" height="20" rx="10" fill="none" stroke="{INK3}" stroke-width="1" '
          f'stroke-dasharray="3 3"/>')
    c.text(328, yl, "secondary probe", 10.5, "start", INK2)
    c.text(704, yl, "source: Table 12.1", 10.5, "end", INK3, italic=True)
    c.save(p)


def fig_12_2():
    prof = [("A invariance", 0.958), ("B sensitivity", 0.630), ("C bottleneck passage", 0.400), ("D recovery", 0.492),
            ("E frontier", 0.571), ("F meta-search", 0.886), ("G constraint", 0.562), ("H path efficiency", 0.829)]
    assert len(prof) == 8 and max(v for _, v in prof) == 0.958 and min(v for _, v in prof) == 0.400
    p = reg("chapters/ch12_benchmarks_as_geometric_probes.md", "12.2",
            "The eight-dimensional profile that Section 12.7.1 gives for its example, model A, with one axis per "
            "probe type running from 0 at the centre to 1 at the outer ring. The profile reaches 0.958 on "
            "invariance and drops to 0.400 on bottleneck passage, so its outline is far from a circle. A single "
            "score would keep the size of this outline and discard its shape. The chapter gives no numbers for "
            "its model B, so only A is drawn.",
            "## Worked Example: Designing a Probe for Clinical Reasoning")
    c = Canvas(720, 440, "A profile is a shape: the eight probe scores of the example model")
    _radar(c, 360, 236, 140, [f"{n} {v:.3f}" for n, v in prof], [("model A", SERIES[0], [v for _, v in prof])])
    c.text(16, 430, "centre 0, outer ring 1, rings every 0.25; values from Section 12.7.1", 10.5, "start", INK3,
           italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 13
def fig_13_1():
    names = ["Flash 2.0", "Flash 2.5", "Flash 3", "Pro", "Claude"]
    comp = {"Social Cognition": [0.695, 0.628, 0.734, 0.643, 0.697],        # Tables 13.1, 13.5, 13.6, 13.2
            "Attention": [0.666, 0.745, 0.747, 0.776, 0.679],
            "Executive Functions": [0.622, 0.682, 0.685, 0.695, 0.625],
            "Learning": [0.568, 0.477, None, 0.488, None]}
    best = {}
    for tr, vals in comp.items():
        v = [x for x in vals if x is not None]
        best[tr] = names[vals.index(max(v))]
    assert best == {"Social Cognition": "Flash 3", "Attention": "Pro", "Executive Functions": "Pro",
                    "Learning": "Flash 2.0"}
    assert len(set(best.values())) > 1                                         # no model leads every track
    assert abs((0.695 - 0.568) - 0.127) < 1e-9 and abs((0.734 - 0.628) - 0.106) < 1e-9   # ranges quoted in Section 10.6.1
    p = reg("chapters/ch13_five_convergent_measurements.md", "13.1",
            "Track composites as the chapter reports them (Tables 13.1, 13.2, 13.5 and 13.6); the vertical axis "
            "is the composite score. Each track is a column, each model keeps one colour and one position within "
            "a column, and a line joins a model's scores in neighbouring columns. The lines cross: Gemini 3 Flash "
            "leads Social Cognition, Gemini 2.5 Pro leads Attention and Executive Functions, and Gemini 2.0 Flash "
            "leads Learning, which was run on three models. The chapter reports no composite for Metacognition, "
            "so that track has no column.",
            "## 13.6 The Scalar Irrecoverability Theorem")
    c = Canvas(720, 420, "No model leads every track: the composites cross")
    ax = Axes(c, 70, 66, 610, 262, (0, 1), (0.45, 0.80), [], [0.5, 0.6, 0.7, 0.8], "", "track composite")
    cols = list(comp)
    xc = [ax.x0 + 90 + 143 * i for i in range(4)]
    off = [-26, -13, 0, 13, 26]
    for j, m in enumerate(names):
        for a in range(3):
            v1, v2 = comp[cols[a]][j], comp[cols[a + 1]][j]
            if v1 is not None and v2 is not None:
                c.line(xc[a] + off[j], ax.Y(v1), xc[a + 1] + off[j], ax.Y(v2), MC[m], 1.5, opacity=0.55)
    for a, tr in enumerate(cols):
        for j, m in enumerate(names):
            v = comp[tr][j]
            if v is None:
                continue
            c.dot(xc[a] + off[j], ax.Y(v), MC[m], 4.5, title=f"{FULL[m]}, {tr}: {v:.3f}")
            if m == best[tr]:
                c.text(xc[a] + off[j], ax.Y(v) - 11, f"{v:.3f}", 10.5, "middle", INK)
        c.text(xc[a], ax.y0 + ax.h + 17, tr, 11, "middle", INK2)
    c.text(xc[3], ax.y0 + ax.h + 32, "(three models)", 10.5, "middle", INK3)
    x = 70
    for m in names:
        _swatch(c, x, 48, MC[m])
        c.text(x + 18, 49, FULL[m], 11, "start", INK2)
        x += 18 + 6.3 * len(FULL[m]) + 20
    c.text(16, 410, "value shown for the leader of each track; Metacognition has no composite in the chapter (Table 13.4)",
           10.5, "start", INK3, italic=True)
    c.save(p)


def fig_13_2():
    f3, f4, p3, p4 = 0.094, 0.723, 0.700, 0.350                       # Table 13.4

    def flash(w):
        return w * f3 + (1 - w) * f4

    def pro(w):
        return w * p3 + (1 - w) * p4

    assert abs(flash(0.5) - 0.409) < 0.001 and abs(pro(0.5) - 0.525) < 0.001     # the averages in Section 13.3.3
    assert abs(p3 / f3 - 7.4) < 0.05 and abs(f4 / p4 - 2.1) < 0.05              # the ratios in Section 13.6.1
    wstar = (f4 - p4) / ((f4 - p4) + (p3 - f3))
    assert abs(flash(wstar) - pro(wstar)) < 1e-12 and round(wstar, 2) == 0.38
    p = reg("chapters/ch13_five_convergent_measurements.md", "13.2",
            "A composite of two metacognition scores as its weights change: the horizontal axis is the weight w "
            "on error detection (M3), with the rest on strategy selection (M4), and the vertical axis is the "
            "weighted score for the two models of Table 13.4. At equal weights Gemini 2.5 Pro scores 0.525 and "
            "Gemini 2.0 Flash 0.409, the averages the chapter quotes, and below w = 0.38 the order reverses. "
            "Which model ranks first is set by the weight, not by the scores. The scores are those the chapter "
            "reports; the weighted sum is the projection of its Theorem 13.1.",
            "## 13.7 Robustness Profiles: Each Model Has a Geometric Signature")
    c = Canvas(720, 420, "The weight, not the data, decides which model ranks first")
    ax = Axes(c, 70, 60, 550, 280, (0, 1), (0, 0.8), [0, 0.25, 0.5, 0.75, 1.0], [0, 0.2, 0.4, 0.6, 0.8],
              "weight w on M3 error detection (1 − w on M4 strategy selection)", "weighted composite")
    xs = ax.X(wstar)
    c.line(xs, ax.y0, xs, ax.y0 + ax.h, INK3, 1.5, dash="4 4")
    c.text(xs + 6, ax.Y(0.04), f"order reverses at w = {wstar:.2f}", 10.5, "start", INK2, italic=True)
    for name, fn, col in (("Flash 2.0", flash, MC["Flash 2.0"]), ("Pro", pro, MC["Pro"])):
        c.polyline([(ax.X(0), ax.Y(fn(0))), (ax.X(1), ax.Y(fn(1)))], col, 2, title=FULL[name])
        for w in (0.0, 0.5, 1.0):
            c.dot(ax.X(w), ax.Y(fn(w)), col, 4.5, title=f"{FULL[name]}, w = {w}: {fn(w):.3f}")
        c.text(ax.X(1) + 11, ax.Y(fn(1)) + 4, FULL[name], 11, "start", INK2)
    c.text(ax.X(0) + 9, ax.Y(f4) - 8, "M4 0.723", 10.5, "start", INK)
    c.text(ax.X(0) + 9, ax.Y(p4) + 16, "M4 0.350", 10.5, "start", INK)
    c.text(ax.X(1) - 9, ax.Y(p3) - 9, "M3 0.700", 10.5, "end", INK)
    c.text(ax.X(1) - 9, ax.Y(f3) + 16, "M3 0.094", 10.5, "end", INK)
    c.text(ax.X(0.5) + 8, ax.Y(pro(0.5)) + 16, "0.525", 10.5, "start", INK)
    c.text(ax.X(0.5) - 8, ax.Y(flash(0.5)) + 17, "0.409", 10.5, "end", INK)
    c.text(ax.X(wstar / 2), ax.Y(0.11), "Gemini 2.0 Flash first", 11, "middle", INK2)
    c.text(ax.X((1 + wstar) / 2), ax.Y(0.11), "Gemini 2.5 Pro first", 11, "middle", INK2)
    c.save(p)


# ------------------------------------------------------------------ chapter 14
def _rot(g):
    """Rotate a square grid a quarter turn clockwise."""
    n = len(g)
    return tuple(tuple(g[n - 1 - j][i] for j in range(n)) for i in range(n))


def _mirror(g):
    return tuple(tuple(reversed(row)) for row in g)


def _grid(c, x, y, g, cell, cols):
    for i, row in enumerate(g):
        for j, v in enumerate(row):
            c.add(f'<rect x="{x + j * cell:.2f}" y="{y + i * cell:.2f}" width="{cell - 1.5:.2f}" height="{cell - 1.5:.2f}" '
                  f'rx="2" fill="{cols[v]}"/>')


def fig_14_1():
    g0 = ((1, 0, 0, 2), (1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 0, 0))     # illustrative input grid

    def rule(g):                                                       # illustrative rule: the shape takes the marker's colour
        return tuple(tuple(2 if v == 1 else v for v in row) for row in g)

    rots = [g0]
    for _ in range(3):
        rots.append(_rot(rots[-1]))
    refl = [_mirror(r) for r in rots]
    assert _rot(rots[-1]) == g0                                        # r^4 = e
    assert len(set(rots + refl)) == 8                                  # the eight elements act distinctly
    assert all(rule(_rot(g)) == _rot(rule(g)) and rule(_mirror(g)) == _mirror(rule(g)) for g in rots)
    assert 8 * math.factorial(9) == 2903040                            # order of D4 x S9, Definition 14.3
    p = reg("chapters/ch14_from_theory_to_engineering.md", "14.1",
            "The eight symmetries of a square grid, the dihedral group of order 8, applied to one input and "
            "output pair: four rotations in the top row and four reflections in the bottom row. Each transform "
            "acts on the input grid and the output grid together, the consistency principle of Section 14.1, so "
            "every panel is a valid example of the same rule. The grid and its rule (the shape takes the colour "
            "of the single marker cell) are illustrative. With the colour permutations of Definition 14.3 the "
            "augmentation group has order 8 times 9!, or 2,903,040.",
            "## 14.2 Adversarial Training as Manifold Smoothing")
    c = Canvas(720, 400, "One grid task, eight consistent views: the dihedral augmentation")
    cols = {0: BOX, 1: SERIES[0], 2: SERIES[1]}
    labels = [["identity", "rotate 90°", "rotate 180°", "rotate 270°"],
              ["mirror", "mirror, rotate 90°", "mirror, rotate 180°", "mirror, rotate 270°"]]
    cell = 14
    for r, (row, head) in enumerate(((rots, "rotations"), (refl, "reflections"))):
        ytop = 62 + 158 * r
        c.text(16, ytop, head, 11.5, "start", INK, "600")
        for k, g in enumerate(row):
            x = 22 + 174 * k
            y = ytop + 34
            c.text(x + 73, ytop + 22, labels[r][k], 11, "middle", INK2)
            _grid(c, x, y, g, cell, cols)
            c.arrow(x + 62, y + 28, x + 84, y + 28, INK2, 1.5)
            _grid(c, x + 91, y, rule(g), cell, cols)
            c.text(x + 28, y + 72, "input", 10, "middle", INK3)
            c.text(x + 119, y + 72, "output", 10, "middle", INK3)
    c.text(16, 390, "illustrative grid and rule; the same transform acts on input and output in every panel", 10.5,
           "start", INK3, italic=True)
    c.save(p)


def _madd(x, y, cc=1.0):
    """Möbius addition on the Poincaré ball, the formula of Section 14.5."""
    xy = x[0] * y[0] + x[1] * y[1]
    x2 = x[0] * x[0] + x[1] * x[1]
    y2 = y[0] * y[0] + y[1] * y[1]
    a = 1 + 2 * cc * xy + cc * y2
    b = 1 - cc * x2
    d = 1 + 2 * cc * xy + cc * cc * x2 * y2
    return ((a * x[0] + b * y[0]) / d, (a * x[1] + b * y[1]) / d)


def fig_14_2():
    s, beta = 0.85, math.radians(56)           # illustrative edge length (hyperbolic) and branching angle
    r = math.tanh(s / 2)

    def hdist(x, y):
        m = _madd((-x[0], -x[1]), y)
        return 2 * math.atanh(math.hypot(*m))

    levels = [[(0.0, 0.0)]]
    edges = []
    first = [(r * math.cos(a), r * math.sin(a)) for a in (math.radians(-90), math.radians(30), math.radians(150))]
    for ch in first:
        edges.append(((0.0, 0.0), (ch[0], ch[1])))
    levels.append(first)
    for _ in range(3):
        nxt = []
        for pnt in levels[-1]:
            a0 = math.atan2(pnt[1], pnt[0])
            for sg in (-1, 1):
                v = (r * math.cos(a0 + sg * beta), r * math.sin(a0 + sg * beta))
                ch = _madd(pnt, v)
                assert abs(hdist(pnt, ch) - s) < 1e-9          # every edge has the same hyperbolic length
                assert math.hypot(*ch) < 1                      # the boundary constraint, norm below 1 for c = 1
                edges.append((pnt, v))
                nxt.append(ch)
        levels.append(nxt)
    assert [len(l) for l in levels] == [1, 3, 6, 12, 24]
    p = reg("chapters/ch14_from_theory_to_engineering.md", "14.2",
            "A tree in the Poincaré disk, the two-dimensional case of the ball of Section 14.5 with curvature c = "
            "1; the system itself uses 32 dimensions and the tree is illustrative. Children are placed with the "
            "chapter's Möbius addition, so every edge has the same hyperbolic length although the edges look "
            "shorter toward the boundary, and the dashed circles mark hyperbolic distance 1, 2 and 3 from the "
            "origin. The number of nodes doubles at each level and they still fit. This is the room the embedding "
            "uses, with general rules near the origin and specific sub-rules near the boundary.",
            "## 14.6 The Bond Geodesic Equilibrium in Economic Reasoning")
    c = Canvas(720, 440, "Equal steps in hyperbolic distance leave room for a growing tree")
    cx, cy, Rd = 220, 236, 180

    def px(q):
        return cx + Rd * q[0], cy + Rd * q[1]

    c.add(f'<circle cx="{cx}" cy="{cy}" r="{Rd}" fill="{BOX}" fill-opacity="0.35" stroke="{INK2}" stroke-width="1.5"/>')
    for d in (1, 2, 3):
        rr = Rd * math.tanh(d / 2)
        c.add(f'<circle cx="{cx}" cy="{cy}" r="{rr:.2f}" fill="none" stroke="{INK3}" stroke-width="1" '
              f'stroke-dasharray="3 4"><title>hyperbolic distance {d} from the origin</title></circle>')
    for pnt, v in edges:
        pts = [px(_madd(pnt, (v[0] * i / 24, v[1] * i / 24))) for i in range(25)]
        c.polyline(pts, INK3, 1.5)
    for k, lev in enumerate(levels):
        for q in lev:
            x, y = px(q)
            c.dot(x, y, SERIES[k], 4.5 - 0.6 * k, title=f"level {k}, hyperbolic distance {hdist((0.0, 0.0), q):.2f} from the origin")
    x0 = 446
    c.text(x0, 84, "Levels of the tree", 11.5, "start", INK, "600")
    for k, lev in enumerate(levels):
        y = 106 + 20 * k
        c.dot(x0 + 6, y - 4, SERIES[k], 4.5)
        far = max(hdist((0.0, 0.0), q) for q in lev)
        c.text(x0 + 20, y, f"level {k}: {len(lev)} node{'s' if len(lev) > 1 else ''}"
               + ("" if k == 0 else f", distance {far:.2f}"), 11, "start", INK2)
    c.text(x0, 232, f"Every edge: hyperbolic length {s}", 11, "start", INK2)
    c.text(x0, 252, "Dashed circles: distance 1, 2, 3", 11, "start", INK2)
    c.text(x0, 286, "origin: general rules", 11, "start", INK2)
    c.text(x0, 304, "boundary: specific sub-rules", 11, "start", INK2)
    c.text(x0, 338, "Edges are geodesics, placed with", 11, "start", INK2)
    c.text(x0, 356, "the Möbius addition of Section 14.5", 11, "start", INK2)
    c.text(16, 430, "Poincaré disk, c = 1; distances are from the origin; illustrative tree", 10.5, "start", INK3,
           italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 15
def fig_15_1():
    b = 0.5                                        # illustrative asymmetry
    f_truth, f_appr = 1 + b, 1 - b                 # cost of a unit step toward truth and toward approval
    assert f_truth / f_appr == 3.0
    p = reg("chapters/ch15_open_questions.md", "15.1",
            "What a direction-dependent cost looks like: each closed curve is the set of steps that cost exactly "
            "1 from the marked point. For a Riemannian metric the set is symmetric about the point, so a step and "
            "its reverse cost the same and the asymmetry ratio F(v)/F(-v) is 1. The Finsler example adds a term "
            "that charges for movement toward truth, so one unit of cost reaches 2 toward approval and 0.67 "
            "toward truth, an asymmetry ratio of 3. The example and its constant 0.5 are illustrative; whether "
            "the reasoning manifold has such a structure is the chapter's Open Problem 15.1.",
            "## 15.2 Mechanisms: Measuring the Heuristic from Activations")
    c = Canvas(720, 400, "Riemannian cost is symmetric; Finsler cost depends on direction")
    sc = 72
    for cx, title, form, bb in ((175, "Riemannian", "F(v) = |v|", 0.0), (545, "Finsler (illustrative)", "F(v) = |v| + 0.5 v₁", b)):
        cy = 218
        mx = cx - sc * bb / (1 - bb * bb)             # centre of the curve
        c.text(mx, 62, title, 12.5, "middle", INK, "600")
        c.text(mx, 80, form, 11, "middle", INK2)
        pts = []
        for i in range(181):
            th = 2 * math.pi * i / 180
            rr = sc / (1 + bb * math.cos(th))
            pts.append((cx + rr * math.cos(th), cy - rr * math.sin(th)))
        _polygon(c, pts, SERIES[0] if not bb else SERIES[1], SERIES[0] if not bb else SERIES[1], 0.10, 2,
                 title="steps of cost 1")
        rt, ra = sc / (1 + bb), sc / (1 - bb)
        c.arrow(cx, cy, cx + rt - 3, cy, INK, 2)
        c.arrow(cx, cy, cx - ra + 3, cy, INK, 2)
        c.dot(cx, cy, INK, 4)
        c.text(cx + rt / 2, cy - 9, f"{1 / (1 + bb):.2f}".rstrip("0").rstrip("."), 11, "middle", INK)
        c.text(cx - ra / 2, cy - 9, f"{1 / (1 - bb):.2f}".rstrip("0").rstrip("."), 11, "middle", INK)
        c.text(cx + 12, cy + 106, "toward truth →", 10.5, "start", INK3)
        c.text(cx - 12, cy + 106, "← toward approval", 10.5, "end", INK3)
        ratio = (1 + bb) / (1 - bb)
        c.text(mx, 350, f"asymmetry ratio F(v) / F(−v) = {ratio:g}", 11.5, "middle", INK)
        c.text(mx, 367, "same cost both ways" if not bb else "truth costs 3 times approval", 11,
               "middle", INK2)
    c.text(16, 390, "arrows: how far one unit of cost reaches in each direction; v₁ is the component of the step toward truth",
           10.5, "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 16
def fig_16_1():
    m0, s0, m1, s1 = -2.0, 0.6, 2.5, 1.0           # illustrative prior and posterior

    def gauss(x, m, s):
        return math.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))

    def disp(x, t):                                 # displacement interpolation: the map is (1 - t) id + t T
        return gauss(x, (1 - t) * m0 + t * m1, (1 - t) * s0 + t * s1)

    def mix(x, t):
        return (1 - t) * gauss(x, m0, s0) + t * gauss(x, m1, s1)

    xs = [-4.5 + 10.5 * i / 420 for i in range(421)]
    for fn in (disp, mix):
        for t in (0.0, 0.5, 1.0):
            assert abs(sum(fn(x, t) for x in xs) * (10.5 / 420) - 1) < 0.01        # each curve is a distribution
    p = reg("chapters/ch16_geometric_reasoning_as_a_field.md", "16.1",
            "Two paths from the same prior belief to the same posterior, each shown at the start, the midpoint "
            "and the end; the horizontal axis is the state of the world and the vertical axis is probability "
            "density. Top: the displacement interpolation of Section 16.3, the geodesic of the Wasserstein "
            "distance, in which the belief slides and widens as one bump. Bottom: the mixture path, the straight "
            "line in probability space of Section 16.2, in which the old belief fades while the new one grows and "
            "the midpoint has two bumps. The two Gaussian beliefs are illustrative.",
            "## 16.4 Connections to Category Theory")
    c = Canvas(720, 452, "Two straight lines between the same pair of beliefs")
    cols = [SERIES[0], SERIES[1], SERIES[2]]
    for k, (fn, y0, l1, l2, l3) in enumerate(((disp, 64, "displacement", "interpolation", "(Wasserstein geodesic)"),
                                              (mix, 244, "mixture path", "(1 − t) μ₀ + t μ₁", ""))):
        ax = Axes(c, 70, y0, 500, 140, (-4.5, 6.0), (0, 0.72), [-4, -2, 0, 2, 4, 6] if k else [], [0, 0.3, 0.6],
                  "belief over the state of the world" if k else "", "density")
        for t, col in zip((0.0, 0.5, 1.0), cols):
            c.polyline([(ax.X(x), ax.Y(fn(x, t))) for x in xs], col, 2, title=f"t = {t}")
        c.text(584, y0 + 50, l1, 11.5, "start", INK, "600")
        c.text(584, y0 + 68, l2, 11, "start", INK2)
        if l3:
            c.text(584, y0 + 86, l3, 11, "start", INK2)
    legend(c, 70, 48, [("t = 0, prior", cols[0]), ("t = 0.5, midpoint", cols[1]), ("t = 1, posterior", cols[2])])
    c.text(16, 442, "illustrative Gaussian beliefs: prior mean −2, width 0.6; posterior mean 2.5, width 1", 10.5,
           "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ appendix B
def fig_b_1():
    mags = [0.0, 0.3, 1.0]
    prof = {"Flash 2.0": [0.02, 0.15, 0.48], "Pro": [0.08, 0.12, 0.33], "Claude": [0.00, 0.08, 0.35]}   # B.6, step 2
    assert all(v[0] < v[1] < v[2] for v in prof.values())            # the monotonic increase the appendix notes
    assert prof["Claude"][1] < prof["Pro"][1]                         # Claude's lower mild-distractor sensitivity
    p = reg("appendices/appendix_b_structural_fuzzing.md", "B.1",
            "The sensitivity profile of step 2 of the worked example, for the distractor task A1, with values as "
            "printed in the appendix, which names the models Flash 2.0, Pro and Claude. The horizontal axis is "
            "distractor magnitude: the control at 0, mild distractors at 0.3 and vivid ones at 1.0. The vertical "
            "axis is sensitivity, the mean distance between the outputs with and without the distractor. "
            "Sensitivity rises with magnitude for all three models, the dose-response the appendix describes.",
            "## B.7 Common Pitfalls and Troubleshooting")
    c = Canvas(720, 400, "Sensitivity to distractors rises with their intensity")
    ax = Axes(c, 70, 56, 520, 270, (0, 1), (0, 0.55), [], [0, 0.1, 0.2, 0.3, 0.4, 0.5], "distractor magnitude",
              "sensitivity")
    for v, lab in zip(mags, ("0 (control)", "0.3 (mild)", "1.0 (vivid)")):
        c.text(ax.X(v), ax.y0 + ax.h + 16, lab, 11, "middle", INK2)
        c.line(ax.X(v), ax.y0, ax.X(v), ax.y0 + ax.h, GRID, 1)
    dy = {"Flash 2.0": 4, "Claude": -2, "Pro": 11}
    for m, vals in prof.items():
        pts = [(ax.X(x), ax.Y(y)) for x, y in zip(mags, vals)]
        c.polyline(pts, MC[m], 2, title=m)
        for (x, y), mg, v in zip(pts, mags, vals):
            c.dot(x, y, MC[m], 4.5, title=f"{m}, magnitude {mg}: {v:.2f}")
        c.text(pts[-1][0] + 11, pts[-1][1] + dy[m], f"{m}  {vals[-1]:.2f}", 11, "start", INK2)
    c.text(16, 390, "three points per model, as printed in Appendix B.6; lower is more robust", 10.5, "start", INK3,
           italic=True)
    c.save(p)


def fig_b_2():
    mri = [("framing, euphemistic", 0.72), ("framing, dramatic", 0.68), ("distractor, vivid", 0.55),
           ("distractor, mild", 0.82), ("gender swap", 0.96), ("evaluation order", 0.98)]         # B.6 sample output
    lo = min(mri, key=lambda kv: kv[1])
    assert lo == ("distractor, vivid", 0.55)                          # "Minimum MRI = 0.55 (distractor_vivid)"
    p = reg("appendices/appendix_b_structural_fuzzing.md", "B.2",
            "The radar chart the appendix recommends, drawn from the sample output of run_campaign printed in "
            "Section B.6: one axis per perturbation type, with the Model Robustness Index from 0 at the centre to "
            "1 at the outer ring. The outline is nearly full for gender swap and evaluation order and dented for "
            "vivid distractors. That marked minimum, 0.55, is the worst-case figure that Section "
            "B.1 reports alongside the vector. This is illustrative sample output; the appendix does not attribute it to a named model.",
            "## B.7 Common Pitfalls and Troubleshooting")
    c = Canvas(720, 450, "The robustness profile of the sample campaign output")
    _radar(c, 360, 226, 140, [f"{n} {v:.2f}" for n, v in mri], [("sample output", SERIES[0], [v for _, v in mri])],
           mark_min=True)
    c.dot(22, 416, CRITICAL, 4)
    c.text(34, 420, "weakest dimension, 0.55: the worst-case figure reported alongside the vector", 10.5, "start", INK2)
    c.text(16, 440, "centre 0, outer ring 1, rings every 0.25; sample output of run_campaign, Appendix B.6", 10.5,
           "start", INK3, italic=True)
    c.save(p)
