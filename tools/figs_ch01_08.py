"""Figures for Chapters 1 to 8 (Parts I and II).

Each figure is drawn from a formula, a definition or numbers printed in its chapter. The
volume is a posited framework (see the README): where a chapter reports benchmark numbers,
the caption says they are the chapter's reported values, and schematics are labelled so.
The earlier hand-drawn files figures/fig_0N_1_*.svg are left untouched; these functions
redraw them from the chapter text.
"""

import heapq
import math
from collections import deque

from figkit import BORDER, BOX, CRITICAL, GRID, INK, INK2, INK3, SERIES, SURFACE, Axes, Canvas, legend, reg

REPORTED = ("The numbers are the ones the chapter reports from the Measuring AGI benchmarks; the geometric "
            "reading of them is the chapter's interpretation, part of a posited framework.")


# ------------------------------------------------------------------ helpers
def _poly(c, pts, col, width=2, dash=None, opacity=1.0, fill="none", fill_opacity=0.0):
    d = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    c.add(f'<polyline points="{d}" fill="{fill}" fill-opacity="{fill_opacity}" stroke="{col}" stroke-width="{width}" '
          f'stroke-opacity="{opacity}" stroke-linejoin="round" stroke-linecap="round"{da}/>')


def _rect(c, x, y, w, h, fill, opacity=1.0, rx=0, stroke=None):
    st = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    c.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{fill}" '
          f'fill-opacity="{opacity}"{st}/>')


def _circle(c, x, y, r, fill, opacity=1.0, stroke=None, width=1.5):
    st = f' stroke="{stroke}" stroke-width="{width}"' if stroke else ""
    c.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{fill}" fill-opacity="{opacity}"{st}/>')


def _bez(p0, p1, p2, p3=None, n=40, t0=0.0, t1=1.0):
    out = []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        if p3 is None:
            x = (1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * p1[1] + t * t * p2[1]
        else:
            x = (1 - t) ** 3 * p0[0] + 3 * t * (1 - t) ** 2 * p1[0] + 3 * t * t * (1 - t) * p2[0] + t ** 3 * p3[0]
            y = (1 - t) ** 3 * p0[1] + 3 * t * (1 - t) ** 2 * p1[1] + 3 * t * t * (1 - t) * p2[1] + t ** 3 * p3[1]
        out.append((x, y))
    return out


def _head(c, pts, col, width=2):
    """Arrow head at the end of a polyline."""
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    for s in (+1, -1):
        a = ang + s * 2.6
        c.line(x2, y2, x2 + 8 * math.cos(a), y2 + 8 * math.sin(a), col, width)


def _contour(fn, x0, x1, y0, y1, level, nx=120, ny=72):
    """Marching squares: line segments of the level set fn = level, in data coordinates."""
    dx, dy = (x1 - x0) / nx, (y1 - y0) / ny
    v = [[fn(x0 + i * dx, y0 + j * dy) - level for i in range(nx + 1)] for j in range(ny + 1)]
    segs = []
    for j in range(ny):
        for i in range(nx):
            corners = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
            vals = [v[b][a] for a, b in corners]
            pts = []
            for k in range(4):
                (a1, b1), (a2, b2) = corners[k], corners[(k + 1) % 4]
                f1, f2 = vals[k], vals[(k + 1) % 4]
                if (f1 < 0) != (f2 < 0):
                    t = f1 / (f1 - f2)
                    pts.append((x0 + (a1 + t * (a2 - a1)) * dx, y0 + (b1 + t * (b2 - b1)) * dy))
            if len(pts) == 2:
                segs.append((pts[0], pts[1]))
            elif len(pts) == 4:
                segs.append((pts[0], pts[1]))
                segs.append((pts[2], pts[3]))
    return segs


# ------------------------------------------------------------------ chapter 1
def fig_1_1():
    p = reg("chapters/ch01_reasoning_as_search.md", "1.1",
            "The spectrum of search as Section 1.3 lays it out, with the reasoning analogue the chapter gives for each "
            "kind. This is a schematic of the text, not data. With the zero heuristic A* reduces to uniform-cost "
            "search, and with the perfect heuristic h* it expands only the states on the optimal path, so the place "
            "of a search on the spectrum is set by the quality of h.",
            "## 1.4 A* and the Centrality of the Heuristic")
    c = Canvas(720, 400, "The spectrum of search: the heuristic sets the place")
    c.arrow(40, 66, 680, 66, INK2, 1.5)
    c.text(40, 54, "h(x) = 0 for all x", 11, "start", INK2)
    c.text(360, 54, "quality of the heuristic h(x)", 11.5, "middle", INK)
    c.text(680, 54, "h(x) = h*(x)", 11, "end", INK2)
    boxes = [
        ("Uninformed", ["BFS, DFS", "no knowledge of which", "directions are promising;", "cost exponential in the",
                        "depth of the solution"], ["guessing"]),
        ("Greedy", ["moves to the neighbour", "that minimises h(x);", "fast, easily misled,", "never looks back"],
         ["intuitive, impulsive", "reasoning"]),
        ("Informed (A*)", ["f(x) = g(x) + h(x)", "weighs the cost already", "paid against the cost", "estimated to remain"],
         ["expert reasoning:", "guided deliberation"]),
        ("Optimal", ["guaranteed to find the", "best solution; with", "h = h*, A* expands only", "the optimal path"],
         ["perfect rationality:", "a benchmark"]),
    ]
    for i, (name, lines, ana) in enumerate(boxes):
        x = 22 + i * 171
        _rect(c, x, 86, 163, 262, BOX, 1.0, 6, BORDER)
        c.add(f'<rect x="{x}" y="86" width="163" height="4" rx="2" fill="{SERIES[i]}"/>')
        c.text(x + 12, 114, name, 13.5, "start", INK, "600")
        for k, s in enumerate(lines):
            c.text(x + 12, 140 + 17 * k, s, 10.5, "start", INK2)
        c.line(x + 12, 262, x + 151, 262, BORDER, 1)
        c.text(x + 12, 282, "In reasoning", 10, "start", INK3, italic=True)
        for k, s in enumerate(ana):
            c.text(x + 12, 302 + 17 * k, s, 11, "start", INK)
    c.text(16, 388, "schematic of Section 1.3", 10.5, "start", INK3, italic=True)
    c.save(p)


def _astar_grid():
    W, H = 15, 13
    walls = {(7, r) for r in range(2, 11)} | {(4, r) for r in range(0, 4)} | {(10, r) for r in range(9, 13)}
    start, goal = (1, 6), (13, 6)

    def nbrs(s):
        x, y = s
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            t = (x + dx, y + dy)
            if 0 <= t[0] < W and 0 <= t[1] < H and t not in walls:
                yield t

    hstar = {goal: 0}
    q = deque([goal])
    while q:
        s = q.popleft()
        for t in nbrs(s):
            if t not in hstar:
                hstar[t] = hstar[s] + 1
                q.append(t)

    def run(w):
        g = {start: 0}
        parent = {}
        heap = [(w * hstar[start], 0, start)]
        closed = []
        seen = set()
        while heap:
            f, negg, s = heapq.heappop(heap)
            if s in seen:
                continue
            seen.add(s)
            closed.append(s)
            if s == goal:
                break
            for t in nbrs(s):
                if t not in g or g[s] + 1 < g[t]:
                    g[t] = g[s] + 1
                    parent[t] = s
                    heapq.heappush(heap, (g[t] + w * hstar[t], -g[t], t))
        path = [goal]
        while path[-1] != start:
            path.append(parent[path[-1]])
        return set(closed), path[::-1], g[goal]

    return W, H, walls, start, goal, hstar, run


def fig_1_2():
    W, H, walls, start, goal, hstar, run = _astar_grid()
    res = [run(w) for w in (0.0, 0.5, 1.0)]
    cstar = hstar[start]
    assert all(r[2] == cstar for r in res)            # admissible heuristics: every run finds an optimal path
    assert res[2][0] <= res[1][0] <= res[0][0]         # dominance: the better heuristic expands a subset
    assert len(res[2][0]) == cstar + 1                 # h = h*: only the states of one optimal path
    free = W * H - len(walls)
    n = [len(r[0]) for r in res]
    p = reg("chapters/ch01_reasoning_as_search.md", "1.2",
            f"A* on one illustrative grid with three admissible heuristics: h = 0, half the true cost, and h*, the"
            f" true cost to the goal. Shaded cells are the states each search expands, and all three find a path "
            f"of the same optimal length, {cstar} steps. With h = 0 the search expands {n[0]} of the {free} free "
            f"cells, with half the true cost {n[1]}, and with h* only the {n[2]} states on the path; each set "
            f"contains the next, which is the dominance result of Section 1.4. Ties are broken toward the state "
            f"with more cost already paid.",
            "## 1.5 The Limitation: When Graphs Are Not Enough")
    c = Canvas(720, 400, "A better heuristic expands fewer states and finds the same path")
    cell = 14
    names = ["h(x) = 0  (uniform-cost search)", "h(x) = 0.5 h*(x)", "h(x) = h*(x)  (perfect heuristic)"]
    for k, (closed, path, _) in enumerate(res):
        x0, y0 = 30 + k * 225, 68
        for i in range(W):
            for j in range(H):
                x, y = x0 + i * cell, y0 + j * cell
                if (i, j) in walls:
                    _rect(c, x, y, cell - 1, cell - 1, INK3, 0.9, 2)
                elif (i, j) in closed:
                    _rect(c, x, y, cell - 1, cell - 1, SERIES[0], 0.55, 2)
                else:
                    _rect(c, x, y, cell - 1, cell - 1, GRID, 1.0, 2)
        pts = [(x0 + i * cell + cell / 2 - 0.5, y0 + j * cell + cell / 2 - 0.5) for i, j in path]
        _poly(c, pts, INK, 2)
        _circle(c, pts[0][0], pts[0][1], 4.5, SERIES[1], 1.0, SURFACE, 1.5)
        _circle(c, pts[-1][0], pts[-1][1], 4.5, SERIES[5], 1.0, SURFACE, 1.5)
        cx = x0 + W * cell / 2
        c.text(cx, y0 + H * cell + 24, names[k], 11.5, "middle", INK)
        c.text(cx, y0 + H * cell + 43, f"{len(closed)} states expanded", 11.5, "middle", INK2)
    legend(c, 30, 334, [("expanded", "#3d7868"), ("not expanded", GRID), ("wall", INK3), ("start", SERIES[1]),
                        ("goal", SERIES[5])])
    c.line(560, 330, 584, 330, INK, 2)
    c.text(592, 335, "path found", 11.5, "start", INK2)
    c.text(16, 388, f"computed: 4-connected grid, unit step cost, optimal path {cstar} steps in every panel", 10.5,
           "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 2
def fig_2_1():
    p = reg("chapters/ch02_when_space_has_shape.md", "2.1",
            "The structural hierarchy of Sections 2.1 and 2.2, as a schematic. A graph records which states are "
            "adjacent. A metric space adds a distance between any two states. A Riemannian manifold adds a direction "
            "at each point, a metric that can vary from point to point, geodesics and curvature.",
            "## 2.3 Riemannian Manifolds in 30 Minutes")
    c = Canvas(720, 400, "From graph to metric space to manifold: what each level adds")
    nodes = [(40, 60), (100, 20), (150, 80), (70, 130), (160, 150), (20, 110)]
    edges = [(0, 1), (1, 2), (0, 3), (2, 4), (3, 4), (0, 5), (3, 5)]
    # graph
    gx, gy = 28, 62
    for a, b in edges:
        c.line(gx + nodes[a][0], gy + nodes[a][1], gx + nodes[b][0], gy + nodes[b][1], INK3, 1.5)
    for x, y in nodes:
        c.dot(gx + x, gy + y, SERIES[0], 5)
    # metric space
    mx, my = 268, 62
    a, b = nodes[5], nodes[2]
    c.line(mx + a[0], my + a[1], mx + b[0], my + b[1], INK2, 1.5, dash="5 4")
    c.text(mx + 92, my + 86, "d(x, y)", 11.5, "middle", INK)
    for x, y in nodes:
        c.dot(mx + x, my + y, SERIES[1], 5)
    c.text(mx + a[0] - 4, my + a[1] + 20, "x", 11.5, "middle", INK2, italic=True)
    c.text(mx + b[0] + 12, my + b[1] - 6, "y", 11.5, "middle", INK2, italic=True)
    # manifold: a curved patch with a geodesic and a tangent vector
    px, py = 500, 62
    top = _bez((10, 50), (70, -10), (130, 40), (190, 10))
    bot = _bez((0, 150), (70, 110), (130, 175), (200, 135))
    outline = [(px + x, py + y) for x, y in top] + [(px + x, py + y) for x, y in bot[::-1]]
    outline.append(outline[0])
    _poly(c, outline, SERIES[2], 1.5, fill=SERIES[2], fill_opacity=0.10)
    for f in (0.33, 0.66):
        mid = [(px + (1 - f) * t[0] + f * b_[0], py + (1 - f) * t[1] + f * b_[1]) for t, b_ in zip(top, bot)]
        _poly(c, mid, SERIES[2], 1, opacity=0.45)
    geo = [(px + x, py + y) for x, y in _bez((30, 120), (80, 40), (130, 110), (175, 50))]
    _poly(c, geo, SERIES[2], 2.5)
    c.dot(geo[0][0], geo[0][1], INK, 3.5)
    c.dot(geo[-1][0], geo[-1][1], INK, 3.5)
    c.arrow(geo[0][0], geo[0][1], geo[0][0] + 34, geo[0][1] - 52, INK, 1.8)
    c.text(geo[0][0] + 40, geo[0][1] - 54, "tangent vector", 10.5, "start", INK2)
    c.text(px + 118, py + 108, "geodesic", 10.5, "start", INK2)
    # arrows between panels
    c.arrow(216, 150, 258, 150, INK2, 1.5)
    c.text(237, 140, "+ distance", 10.5, "middle", INK2)
    c.arrow(450, 150, 492, 150, INK2, 1.5)
    c.text(471, 128, "+ direction,", 10.5, "middle", INK2)
    c.text(471, 141, "curvature", 10.5, "middle", INK2)
    cols = [
        (28, "Graph", ["which states exist and", "which are adjacent;", "optionally a cost per edge.",
                       "No direction at a point,", "no curvature."]),
        (268, "Metric space", ["how far apart any two", "states are; the triangle", "inequality holds.",
                               "Still no direction", "at a point."]),
        (500, "Riemannian manifold", ["tangent vectors: direction;", "metric tensor: length and", "angle, varying by point;",
                                      "geodesics: straightest paths;", "curvature."]),
    ]
    for x, name, lines in cols:
        c.text(x, 258, name, 13, "start", INK, "600")
        for k, s in enumerate(lines):
            c.text(x, 280 + 17 * k, s, 11, "start", INK2)
    c.text(16, 388, "schematic", 10.5, "start", INK3, italic=True)
    c.save(p)


def fig_2_2():
    p = reg("chapters/ch02_when_space_has_shape.md", "2.2",
            "The sign of the curvature decides what happens to two geodesics that start side by side and parallel. "
            "The horizontal axis is the distance travelled along them and the vertical axis is their separation, "
            "with the starting separation set to 1. The curves are the standard solutions for constant sectional "
            "curvature K: cos t on the unit sphere (K = +1), constant in flat space (K = 0), and cosh t in the "
            "hyperbolic plane (K = -1). Positive curvature brings the paths together, zero curvature keeps the "
            "separation, and negative curvature drives them apart exponentially, as Section 2.3.5 states.",
            "## 2.4 The Manifold Hypothesis for Reasoning")
    c = Canvas(720, 400, "Curvature decides whether nearby paths converge or diverge")
    ax = Axes(c, 70, 52, 500, 280, (0, 1.5), (0, 2.5), [0, 0.5, 1.0, 1.5], [0, 0.5, 1.0, 1.5, 2.0, 2.5],
              "distance travelled along the geodesics, t", "separation (start = 1)")
    series = [("K = -1: cosh t", math.cosh, SERIES[1], "diverge: fragile"),
              ("K = 0: constant", lambda t: 1.0, SERIES[2], "Euclidean case"),
              ("K = +1: cos t", math.cos, SERIES[0], "converge: robust")]
    for name, fn, col, note in series:
        pts = [(ax.X(1.5 * i / 100), ax.Y(fn(1.5 * i / 100))) for i in range(101)]
        c.polyline(pts, col, 2.5, title=name)
        c.text(pts[-1][0] + 10, pts[-1][1] + 1, name, 11.5, "start", INK)
        c.text(pts[-1][0] + 10, pts[-1][1] + 16, note, 10.5, "start", INK2)
    assert abs(math.cosh(1.5) - 2.3524) < 1e-4 and abs(math.cos(1.5) - 0.0707) < 1e-4
    c.text(16, 388, "solutions of J'' + K J = 0 with J(0) = 1, J'(0) = 0", 10.5, "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 3
def _hfield():
    G, T = (7.4, 3.3), (2.7, 1.9)

    def raw(x, y):
        return (1.0 - 1.0 * math.exp(-((x - G[0]) ** 2 + (y - G[1]) ** 2) / (2 * 2.3 ** 2))
                - 0.5 * math.exp(-((x - T[0]) ** 2 + (y - T[1]) ** 2) / (2 * 1.0 ** 2)))

    def grad(x, y, e=1e-4):
        return ((raw(x + e, y) - raw(x - e, y)) / (2 * e), (raw(x, y + e) - raw(x, y - e)) / (2 * e))

    def descend(x, y, step=0.02, n=4000):
        pts = [(x, y)]
        for _ in range(n):
            gx, gy = grad(x, y)
            m = math.hypot(gx, gy)
            if m < 1e-4:
                break
            x, y = x - step * gx / m, y - step * gy / m
            pts.append((x, y))
            if len(pts) > 30 and math.hypot(x - pts[-20][0], y - pts[-20][1]) < step * 1.5:
                break
        return pts

    gmin = descend(*G)[-1]
    tmin = descend(*T)[-1]
    h0 = raw(*gmin)
    return (lambda x, y: raw(x, y) - h0), grad, descend, gmin, tmin


def fig_3_1():
    h, grad, descend, gmin, tmin = _hfield()
    # the saddle: the lowest point of the ridge between the two minima, found on the segment joining them
    best = None
    for i in range(1, 400):
        t = i / 400
        x, y = tmin[0] + t * (gmin[0] - tmin[0]), tmin[1] + t * (gmin[1] - tmin[1])
        if best is None or h(x, y) > best[0]:
            best = (h(x, y), x, y)
    sx, sy = best[1], best[2]
    for _ in range(60):  # Newton-free refinement: walk downhill in |grad|
        gx, gy = grad(sx, sy)
        e = 1e-3
        gxx = (grad(sx + e, sy)[0] - grad(sx - e, sy)[0]) / (2 * e)
        gxy = (grad(sx, sy + e)[0] - grad(sx, sy - e)[0]) / (2 * e)
        gyy = (grad(sx, sy + e)[1] - grad(sx, sy - e)[1]) / (2 * e)
        det = gxx * gyy - gxy * gxy
        sx, sy = sx - (gyy * gx - gxy * gy) / det, sy - (gxx * gy - gxy * gx) / det
    assert math.hypot(*grad(sx, sy)) < 1e-6 and h(*tmin) < h(sx, sy) and h(*tmin) > 0.2
    # two starts close together on the left edge that end in different valleys
    x_s = 0.5
    ys = [0.3 + 0.05 * i for i in range(110)]
    ends = [math.hypot(descend(x_s, y)[-1][0] - gmin[0], descend(x_s, y)[-1][1] - gmin[1]) < 0.3 for y in ys]
    flip = [i for i in range(1, len(ys)) if ends[i] != ends[i - 1]]
    assert flip, "no separatrix crossing found on the left edge"
    i = max(flip)
    ya, yb = ys[i] + 0.25, ys[i - 1] - 0.25
    pa, pb = descend(x_s, ya), descend(x_s, yb)
    assert math.hypot(pa[-1][0] - gmin[0], pa[-1][1] - gmin[1]) < 0.3
    assert math.hypot(pb[-1][0] - tmin[0], pb[-1][1] - tmin[1]) < 0.3
    p = reg("chapters/ch03_the_heuristic_field.md", "3.1",
            f"A heuristic field on a two-dimensional state space, drawn for an illustrative h (not a measured one)"
            f" with two valleys: the goal, where h = 0, and an illusory valley, a local minimum where h = "
            f"{h(*tmin):.2f} and no solution lies. Thin curves are level sets of h and short arrows show the "
            f"direction of steepest descent, the negative gradient. The two thick curves are streamlines of that "
            f"descent from starting states {abs(ya - yb):.1f} units apart: one reaches the goal, the other is "
            f"captured by the illusory valley. The open circle is the saddle between the valleys, the decision "
            f"point of Section 3.2.3.",
            "## 3.3 Properties of Good Heuristics: Admissibility and Consistency")
    c = Canvas(720, 400, "An imperfect heuristic field: level sets, descent and a false valley")
    ax = Axes(c, 40, 46, 640, 310, (0, 10), (0, 6), [], [], "", "")
    for lev in (0.08, 0.2, 0.32, 0.44, 0.56, 0.68, 0.8, 0.9):
        for (xa, ya_), (xb, yb_) in _contour(h, 0, 10, 0, 6, lev):
            c.line(ax.X(xa), ax.Y(ya_), ax.X(xb), ax.Y(yb_), "#3d5a78", 1)
    for i in range(1, 20):
        for j in range(1, 12):
            x, y = i * 0.5, j * 0.5
            gx, gy = grad(x, y)
            m = math.hypot(gx, gy)
            if m < 0.03 or min(math.hypot(x - q[0], y - q[1]) for q in (gmin, tmin, (sx, sy))) < 0.45:
                continue
            L = 0.17
            x2, y2 = x - L * gx / m, y - L * gy / m
            x1, y1 = x + L * gx / m, y + L * gy / m
            c.line(ax.X(x1), ax.Y(y1), ax.X(x2), ax.Y(y2), INK3, 1)
            ang = math.atan2(ax.Y(y2) - ax.Y(y1), ax.X(x2) - ax.X(x1))
            for s in (+1, -1):
                a = ang + s * 2.6
                c.line(ax.X(x2), ax.Y(y2), ax.X(x2) + 4 * math.cos(a), ax.Y(y2) + 4 * math.sin(a), INK3, 1)
    for pts, col in ((pa, SERIES[0]), (pb, SERIES[1])):
        _poly(c, [(ax.X(x), ax.Y(y)) for x, y in pts[::4] + [pts[-1]]], col, 3)
        c.dot(ax.X(pts[0][0]), ax.Y(pts[0][1]), col, 4.5)
    _circle(c, ax.X(gmin[0]), ax.Y(gmin[1]), 7, SERIES[0], 1.0, SURFACE, 2)
    _circle(c, ax.X(tmin[0]), ax.Y(tmin[1]), 7, SERIES[1], 1.0, SURFACE, 2)
    _circle(c, ax.X(sx), ax.Y(sy), 5, SURFACE, 1.0, INK, 2)

    def tag(x, y, s, anchor="start"):
        w = 6.3 * len(s) + 12
        x0 = x - 6 if anchor == "start" else x - w + 6
        _rect(c, x0, y - 13, w, 18, SURFACE, 0.85, 3)
        c.text(x, y, s, 11.5, anchor, INK)

    tag(ax.X(gmin[0]) + 14, ax.Y(gmin[1]) + 4, "goal: h = 0")
    tag(ax.X(tmin[0]) - 4, ax.Y(tmin[1]) + 26, "illusory valley: local minimum", "start")
    tag(ax.X(sx) + 12, ax.Y(sy) - 10, "saddle: decision point")
    legend(c, 40, 380, [("level sets of h", "#3d5a78"), ("descent direction", INK3), ("reaches the goal", SERIES[0]),
                        ("captured by the false valley", SERIES[1])], 11)
    c.save(p)


def fig_3_2():
    tau, goal_x = 0.5, 10.0

    def hstar(x):
        return goal_x - x

    def hh(x):
        return max(hstar(x) - 5.7 * math.exp(-((x - 4.0) ** 2) / (2 * 0.75 ** 2)), 0.0)

    xs = [i * 0.01 for i in range(1001)]
    false = [x for x in xs if hh(x) < tau and hstar(x) > tau]
    lo, hi = min(false), max(false)
    assert hi < 6 and all(hstar(x) - hh(x) > tau for x in false)     # the underestimate there exceeds the threshold
    first = next(x for x in xs if hh(x) < tau)
    assert abs(first - lo) < 1e-9
    p = reg("chapters/ch03_the_heuristic_field.md", "3.2",
            f"Premature convergence in a satisficing search (Proposition 3.1), drawn with illustrative values "
            f"along one path to a goal at position 10. The straight line is the true cost-to-go, h*, and the curve"
            f" is a heuristic that agrees with it except on a stretch where it underestimates. The search moves "
            f"from the left and stops when the heuristic falls below the threshold τ = {tau}. It first meets that "
            f"condition at position {lo:.1f}, where the true cost-to-go is still {hstar(lo):.1f}: a false "
            f"termination region, far from the goal.",
            "## 3.7 Implications for Reasoning Quality")
    c = Canvas(720, 400, "An underestimating heuristic stops the search short of the goal")
    ax = Axes(c, 70, 52, 600, 280, (0, 10), (0, 10), [0, 2, 4, 6, 8, 10], [0, 2, 4, 6, 8, 10],
              "position along the path (goal at 10)", "cost-to-go")
    _rect(c, ax.X(lo), ax.Y(10), ax.X(hi) - ax.X(lo), ax.Y(0) - ax.Y(10), CRITICAL, 0.14)
    _rect(c, ax.X(goal_x - tau), ax.Y(10), ax.X(10) - ax.X(goal_x - tau), ax.Y(0) - ax.Y(10), SERIES[0], 0.16)
    c.line(ax.X(0), ax.Y(tau), ax.X(10), ax.Y(tau), INK2, 1.5, dash="5 4")
    c.text(ax.X(0) + 6, ax.Y(tau) - 6, f"threshold τ = {tau}", 10.5, "start", INK2, italic=True)
    c.polyline([(ax.X(x), ax.Y(hstar(x))) for x in xs[::10]], SERIES[0], 2.5, title="true cost-to-go h*")
    c.polyline([(ax.X(x), ax.Y(hh(x))) for x in xs[::5]], SERIES[1], 2.5, title="heuristic h")
    c.dot(ax.X(lo), ax.Y(hh(lo)), CRITICAL, 5, title="search halts here")
    c.line(ax.X(lo), ax.Y(hh(lo)) - 8, ax.X(lo), ax.Y(hstar(lo)) + 6, INK3, 1.5, dash="3 3")
    c.dot(ax.X(lo), ax.Y(hstar(lo)), SERIES[0], 4)
    c.text(ax.X(2.95), ax.Y(2.6), "search halts:", 11.5, "end", INK)
    c.text(ax.X(2.95), ax.Y(2.6) + 15, f"h < τ, but h* = {hstar(lo):.1f}", 11, "end", INK2)
    c.text((ax.X(lo) + ax.X(hi)) / 2, ax.Y(10) + 16, "false", 10.5, "middle", INK2)
    c.text((ax.X(lo) + ax.X(hi)) / 2, ax.Y(10) + 29, "termination", 10.5, "middle", INK2)
    c.text(ax.X(10) - 4, ax.Y(2.2), "true", 10.5, "end", INK2)
    c.text(ax.X(10) - 4, ax.Y(2.2) + 13, "goal region", 10.5, "end", INK2)
    c.text(ax.X(1.2), ax.Y(8.8) - 10, "true cost-to-go h*", 11.5, "start", INK)
    c.text(ax.X(5.2), ax.Y(2.0), "heuristic h", 11.5, "start", INK)
    c.text(16, 388, "illustrative values; the search moves from left to right", 10.5, "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 4
def fig_4_1():
    # ds^2 = dx^2 + e^{2x} dy^2. With u = e^{-x} this is (du^2 + dy^2) / u^2, whose geodesics are circles centred on u = 0.
    r2 = 1.0 + 0.25                       # circle through (y, u) = (0, 1) and (1, 1), centre (0.5, 0)
    ys = [i / 400 for i in range(401)]
    xs = [-0.5 * math.log(r2 - (y - 0.5) ** 2) for y in ys]
    assert abs(xs[0]) < 1e-12 and abs(xs[-1]) < 1e-12
    xmin = min(xs)
    assert abs(xmin - (-0.5 * math.log(1.25))) < 1e-12 and abs(ys[xs.index(xmin)] - 0.5) < 1e-12
    # check the chapter's conservation law e^{2x} dy/ds = C along the curve (s = arc length in the metric)
    cons = []
    for i in range(len(ys) - 1):
        xm = 0.5 * (xs[i] + xs[i + 1])
        ds = math.sqrt((xs[i + 1] - xs[i]) ** 2 + math.exp(2 * xm) * (ys[i + 1] - ys[i]) ** 2)
        cons.append(math.exp(2 * xm) * (ys[i + 1] - ys[i]) / ds)
    assert max(cons) - min(cons) < 1e-4
    naive_cost = sum(math.exp(0.0) * (1 / 400) ** 2 * 400 for _ in range(400))
    assert abs(naive_cost - 1.0) < 1e-9                     # the chapter's Step 4: the naive path costs 1
    p = reg("chapters/ch04_geodesics_and_optimal_reasoning.md", "4.1",
            f"The worked example of Section 4.3.1: the metric ds^2 = dx^2 + e^(2x) dy^2, from the state (0, 0) to "
            f"the state (0, 1). The horizontal axis is y, the breadth coordinate, and the vertical axis is x, the "
            f"depth coordinate; the vertical scale is stretched. The naive path holds x = 0; the geodesic, "
            f"computed from the chapter's geodesic equations, bows into negative x, where a step in y costs less, "
            f"and returns, with its lowest point x = {xmin:.2f} at y = 0.5. The right-hand scale gives the factor "
            f"e^(2x) that multiplies the cost of moving in y at each depth.",
            "## 4.4 When It Doesn't: Shortcuts, Detours, Loops, and Dead Ends")
    c = Canvas(720, 400, "The geodesic steps back to where the lateral move is cheaper")
    ax = Axes(c, 70, 76, 520, 256, (-0.1, 1.1), (-0.2, 0.1), [0, 0.25, 0.5, 0.75, 1.0], [-0.2, -0.1, 0, 0.1],
              "y (breadth: which line of argument)", "x (depth of reasoning)")
    for v in (-0.2, -0.1, 0.0, 0.1):
        c.text(ax.x0 + ax.w + 10, ax.Y(v) + 4, f"{math.exp(2 * v):.2f}", 11, "start", INK2)
    c.text(ax.x0 + ax.w + 10, ax.y0 - 30, "e^(2x): cost factor", 10.5, "start", INK2)
    c.text(ax.x0 + ax.w + 10, ax.y0 - 16, "for a step in y", 10.5, "start", INK2)
    c.line(ax.X(0), ax.Y(0), ax.X(1), ax.Y(0), SERIES[1], 2.5)
    c.polyline([(ax.X(y), ax.Y(x)) for y, x in zip(ys, xs)], SERIES[0], 2.5, title="geodesic")
    c.dot(ax.X(0), ax.Y(0), INK, 4.5, title="start (0, 0)")
    c.dot(ax.X(1), ax.Y(0), INK, 4.5, title="goal (0, 1)")
    c.text(ax.X(0) - 8, ax.Y(0) - 10, "start", 11.5, "end", INK)
    c.text(ax.X(1) + 8, ax.Y(0) - 10, "goal", 11.5, "start", INK)
    c.text(ax.X(0.5), ax.Y(0) - 10, "naive path: x = 0 throughout, cost 1", 11.5, "middle", INK)
    c.text(ax.X(0.5), ax.Y(xmin) + 20, f"geodesic: lowest point x = {xmin:.2f}", 11.5, "middle", INK)
    c.text(16, 388, "computed from the geodesic equations of the example; vertical scale stretched", 10.5, "start",
           INK3, italic=True)
    c.save(p)


def fig_4_2():
    p = reg("chapters/ch04_geodesics_and_optimal_reasoning.md", "4.2",
            "The four departures from geodesic reasoning named in Section 4.4, as a schematic. In each panel the "
            "dashed curve is the geodesic from the problem state to the goal and the solid curve is the "
            "trajectory taken. A shortcut jumps across instead of following the surface of the manifold (the "
            "shaded band), a detour reaches the goal at extra cost, a loop revisits a region it has already "
            "crossed, and a dead end stops where the gradient of the heuristic vanishes outside the goal. "
            "Geodesic deviation is the cost of the trajectory minus the cost of the geodesic.",
            "## 4.5 Geodesic Deviation as a Measure of Reasoning Quality")
    c = Canvas(720, 400, "Four ways a reasoning trajectory departs from the geodesic")
    names = [("Shortcut", ["jumps across, leaving", "the manifold's surface"]),
             ("Detour", ["reaches the goal", "at extra cost"]),
             ("Loop", ["revisits a region", "already crossed"]),
             ("Dead end", ["halts where the gradient", "of h is zero, short of the goal"])]
    for k, (name, lines) in enumerate(names):
        x0, y0 = 22 + k * 172, 56
        _rect(c, x0, y0, 160, 222, BOX, 0.55, 6, BORDER)
        S, G = (x0 + 24, y0 + 194), (x0 + 136, y0 + 34)
        if k == 0:
            geo = _bez(S, (x0 + 24, y0 + 40), G)
            _poly(c, geo, SERIES[2], 26, opacity=0.22)
            path = [S, G]
            c.text(x0 + 16, y0 + 22, "manifold", 10.5, "start", INK2)
        else:
            geo = _bez(S, (x0 + 60, y0 + 90), G)
        if k == 1:
            path = _bez(S, (x0 + 170, y0 + 215), (x0 + 60, y0 + 110), (x0 + 150, y0 + 120), n=30)
            path += _bez((x0 + 150, y0 + 120), (x0 + 172, y0 + 124), (x0 + 80, y0 + 20), G, n=30)[1:]
        if k == 2:
            a = _bez(S, (x0 + 60, y0 + 90), G, t1=0.5)
            b = _bez(S, (x0 + 60, y0 + 90), G, t0=0.5)
            mx, my = a[-1]
            dx, dy = a[-1][0] - a[-2][0], a[-1][1] - a[-2][1]
            m = math.hypot(dx, dy)
            tx, ty = dx / m, dy / m
            nx_, ny_ = ty, -tx                     # normal, pointing to the lower right
            R = 24
            cx, cy = mx + R * nx_, my + R * ny_
            a0 = math.atan2(my - cy, mx - cx)
            sgn = 1 if (tx * -math.sin(a0) + ty * math.cos(a0)) > 0 else -1
            loop = [(cx + R * math.cos(a0 + sgn * 2 * math.pi * i / 40), cy + R * math.sin(a0 + sgn * 2 * math.pi * i / 40))
                    for i in range(41)]
            path = a + loop[1:] + b[1:]
        if k == 3:
            path = _bez(S, (x0 + 40, y0 + 120), (x0 + 130, y0 + 170), (x0 + 112, y0 + 108), n=40)
        _poly(c, geo, INK2, 1.5, dash="5 4")
        _poly(c, path, SERIES[1], 2.5)
        if k == 3:
            ex, ey = path[-1]
            c.line(ex - 6, ey - 6, ex + 6, ey + 6, INK, 2)
            c.line(ex - 6, ey + 6, ex + 6, ey - 6, INK, 2)
        else:
            _head(c, path[-6:] if len(path) > 6 else path, SERIES[1], 2.5)
        c.dot(S[0], S[1], INK, 4.5)
        _circle(c, G[0], G[1], 8, SERIES[0], 0.35, SERIES[0], 1.5)
        c.text(S[0] + 2, S[1] + 20, "problem", 10.5, "middle", INK2)
        c.text(G[0], G[1] - 14, "goal", 10.5, "middle", INK2)
        c.text(x0 + 80, y0 + 244, name, 13, "middle", INK, "600")
        for j, s in enumerate(lines):
            c.text(x0 + 80, y0 + 262 + 14 * j, s, 10, "middle", INK2)
    c.line(24, 372, 48, 372, INK2, 1.5, dash="5 4")
    c.text(56, 376, "geodesic", 11, "start", INK2)
    c.line(130, 372, 154, 372, SERIES[1], 2.5)
    c.text(162, 376, "trajectory taken", 11, "start", INK2)
    c.text(704, 376, "schematic of Section 4.4", 10.5, "end", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 5
T53 = [("Gemini 2.0 Flash", 44, 28, 11), ("Gemini 2.5 Flash", 38, 22, 9), ("Gemini 3 Flash Preview", 41, 25, 14),
       ("Gemini 2.5 Pro", 35, 19, 8), ("Claude Sonnet 4.6", 33, 20, 7)]
T51 = [("Gemini 2.0 Flash", -10.2, 8.7, 2.1), ("Gemini 2.5 Flash", -13.4, 6.3, 4.8),
       ("Gemini 3 Flash Preview", -15.8, 10.9, 6.7), ("Gemini 2.5 Pro", -12.1, 7.4, 3.5),
       ("Claude Sonnet 4.6", -9.1, -1.5, 1.2)]


def fig_5_1():
    assert all(v > m > k for _, v, m, k in T53)                               # graded in every model (Table 5.3)
    assert (min(v for _, v, _, _ in T53), max(v for _, v, _, _ in T53)) == (33, 44)   # Section 8.4.2 quotes 33 to 44
    assert (min(m for _, _, m, _ in T53), max(m for _, _, m, _ in T53)) == (19, 28)
    assert (min(k for _, _, _, k in T53), max(k for _, _, _, k in T53)) == (7, 14)
    p = reg("chapters/ch05_heuristic_corruption.md", "5.1",
            "The distractor dose-response of Table 5.3 (Attention A1). The vertical axis is the share of scenarios "
            "whose verdict flipped; the horizontal axis is the intensity of the irrelevant sensory detail added to "
            "the scenario: the control condition, mild, vivid. In all five models the flip rate rises at each "
            "step. " + REPORTED,
            "## 5.5 The Geometry of Corruption")
    c = Canvas(720, 400, "Verdict flips rise with the intensity of irrelevant detail")
    ax = Axes(c, 70, 52, 430, 280, (-0.25, 2.25), (0, 50), [], [0, 10, 20, 30, 40, 50], "", "verdict flip rate (%)")
    for i, (lab, sub) in enumerate([("control", "stochastic baseline"), ("mild", "a few incidental details"),
                                    ("vivid", "immersive sensory detail")]):
        c.text(ax.X(i), ax.y0 + ax.h + 17, lab, 11.5, "middle", INK)
        c.text(ax.X(i), ax.y0 + ax.h + 32, sub, 10.5, "middle", INK2)
    order = sorted(range(5), key=lambda i: -T53[i][1])
    ylab = {}
    prev = None
    for i in order:                                    # spread the end labels at least 15px apart
        y = ax.Y(T53[i][1]) + 4
        if prev is not None and y - prev < 15:
            y = prev + 15
        ylab[i] = prev = y
    for i, (name, v, m, k) in enumerate(T53):
        col = SERIES[i]
        pts = [(ax.X(0), ax.Y(k)), (ax.X(1), ax.Y(m)), (ax.X(2), ax.Y(v))]
        c.polyline(pts, col, 2, title=name)
        for (px, py), val, cond in zip(pts, (k, m, v), ("control", "mild", "vivid")):
            c.dot(px, py, col, 4.5, title=f"{name}, {cond} {val}%")
        c.line(pts[-1][0] + 8, pts[-1][1], pts[-1][0] + 20, ylab[i] - 4, col, 1)
        c.text(pts[-1][0] + 26, ylab[i], f"{name}  {k}, {m}, {v}", 11, "start", INK2)
    c.text(ax.X(2) + 26, ax.Y(44) - 26, "control, mild, vivid (%)", 10.5, "start", INK3, italic=True)
    c.text(16, 388, "values from Table 5.3, as reported in the chapter", 10.5, "start", INK3, italic=True)
    c.save(p)


def fig_5_2():
    eu = [e for _, e, _, _ in T51]
    assert (max(eu), min(eu)) == (-9.1, -15.8) and T51[4][2] == -1.5
    assert sorted(d for _, _, d, _ in T51)[1:] == [6.3, 7.4, 8.7, 10.9]        # the four Gemini models rise 6 to 11
    p = reg("chapters/ch05_heuristic_corruption.md", "5.2",
            "Framing drift by direction, from Table 5.1 (Social Cognition T5): each bar is the change in total "
            "harm score, on the 0 to 70 scale, when a scenario with the same moral facts is rewritten in a "
            "euphemistic or a dramatic register. The shaded band is each model's control drift, the change on "
            "re-running the unchanged scenario, shown on both sides of zero. Four models move down under "
            "euphemistic and up under dramatic rewriting, while Claude Sonnet 4.6 moves down by 9.1 under "
            "euphemistic and by 1.5 under dramatic rewriting, the asymmetry of Section 5.6. " + REPORTED,
            "## 5.7 Recovery Dissociation: Perturbation $\\neq$ Detection")
    c = Canvas(720, 400, "Framing drift has a direction, and one model resists only one side")
    x0, x1, lo, hi = 190, 680, -18.0, 14.0

    def X(v):
        return x0 + (x1 - x0) * (v - lo) / (hi - lo)

    top, rh = 70, 50
    for v in (-15, -10, -5, 0, 5, 10):
        c.line(X(v), top, X(v), top + 5 * rh, GRID, 1)
        c.text(X(v), top + 5 * rh + 16, f"{v:+d}" if v else "0", 11, "middle", INK2)
    c.text((x0 + x1) / 2, top + 5 * rh + 36, "change in total harm score (0 to 70 scale) relative to the neutral version",
           11.5, "middle", INK2)
    for i, (name, e, d, k) in enumerate(T51):
        y = top + rh * i + rh / 2
        _rect(c, X(-k), y - 19, X(k) - X(-k), 38, INK3, 0.22, 3)
        c.text(x0 - 12, y + 4, name, 11.5, "end", INK)
        for val, col, dy, lab in ((e, SERIES[0], -13, "euphemistic"), (d, SERIES[1], 2, "dramatic")):
            xa, xb = sorted((X(0), X(val)))
            c.add(f'<rect x="{xa:.2f}" y="{y + dy:.2f}" width="{xb - xa:.2f}" height="11" rx="3" fill="{col}">'
                  f'<title>{name}, {lab} {val:+.1f}</title></rect>')
            txt = f"{val:+.1f}".replace("-", "−")
            if val < 0:
                c.text(xa - 6, y + dy + 9.5, txt, 10.5, "end", INK)
            else:
                c.text(xb + 6, y + dy + 9.5, txt, 10.5, "start", INK)
    c.line(X(0), top, X(0), top + 5 * rh, INK3, 1.5)
    legend(c, 190, 52, [("euphemistic rewrite", SERIES[0]), ("dramatic rewrite", SERIES[1]),
                        ("control drift, either side of zero", "#3a4c5e")], 11)
    c.text(16, 388, "values from Table 5.1, as reported in the chapter", 10.5, "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 6
T61 = [("Claude Sonnet 4.6", 0, 59, 0.588, 0.000), ("Gemini 2.0 Flash", 33, 71, 0.377, 0.472),
       ("Gemini 2.5 Pro", 44, 68, 0.238, 0.657), ("Gemini 2.5 Flash", 56, 76, 0.206, 0.726)]
ALPHA = {"Claude Sonnet 4.6": 0.0, "Gemini 2.0 Flash": 0.47, "Gemini 2.5 Pro": 0.66, "Gemini 2.5 Flash": 0.73}


def fig_6_1():
    p = reg("chapters/ch06_sycophancy_as_search_hijacking.md", "6.1",
            "The truth manifold and the approval manifold, as a flat schematic of the first two panels the text "
            "describes; the phase-diagram panel and the training gradient are not drawn. Left: with a valid "
            "correction the two goal regions overlap, so every value of the sycophancy parameter α leads to the "
            "same answer and sycophancy cannot be seen. Right: with an invalid correction the goals are disjoint,"
            " and a search with α near 0 holds its answer on the truth manifold, a search with α near 0.73 peels "
            "away to the approval goal, and at the critical value α* the search drifts between them and reaches "
            "neither. The α values and model labels are those the chapter assigns under its convex-combination "
            "model, a modelling axiom and not a measurement.",
            "## 6.5 The Confidence Response: A Diagnostic Signal")
    c = Canvas(720, 400, "Sycophancy shows only where truth and approval part")
    # ---- panel A
    ax0 = 22
    _rect(c, ax0, 50, 330, 300, BOX, 0.45, 6, BORDER)
    c.text(ax0 + 14, 74, "Valid correction", 13, "start", INK, "600")
    c.text(ax0 + 14, 92, "truth and approval goals overlap", 11, "start", INK2)
    S, G = (ax0 + 40, 250), (ax0 + 270, 190)
    band = _bez(S, (ax0 + 150, 300), G)
    _poly(c, band, SERIES[0], 22, opacity=0.20)
    _poly(c, band, SERIES[1], 12, opacity=0.25)
    for off, col in ((-9, SERIES[0]), (0, INK2), (9, SERIES[1])):
        pts = _bez((S[0], S[1]), (ax0 + 150, 300 + off * 2.2), (G[0] - 9, G[1] + off * 0.2))
        _poly(c, pts, col, 2)
        _head(c, pts, col, 2)
    _circle(c, G[0] + 4, G[1], 17, SERIES[0], 0.30, SERIES[0], 1.5)
    _circle(c, G[0] + 4, G[1], 11, SERIES[1], 0.35, SERIES[1], 1.5)
    c.dot(S[0], S[1], INK, 4.5)
    c.text(S[0], S[1] - 14, "start", 11, "middle", INK2)
    c.text(G[0] + 4, G[1] - 26, "shared goal", 11, "middle", INK)
    c.text(ax0 + 165, 322, "all values of α: same answer", 11, "middle", INK2)
    # ---- panel B
    bx0 = 368
    _rect(c, bx0, 50, 330, 300, BOX, 0.45, 6, BORDER)
    c.text(bx0 + 14, 74, "Invalid correction", 13, "start", INK, "600")
    c.text(bx0 + 14, 92, "truth and approval goals are disjoint", 11, "start", INK2)
    S = (bx0 + 36, 230)
    GT, GA = (bx0 + 262, 300), (bx0 + 250, 138)
    mt = _bez(S, (bx0 + 150, 232), GT)
    ma = _bez((bx0 + 110, 232), (bx0 + 170, 218), GA)
    _poly(c, mt, SERIES[0], 22, opacity=0.20)
    _poly(c, ma, SERIES[1], 22, opacity=0.20)
    t_low = _bez(S, (bx0 + 150, 232), (GT[0] - 15, GT[1] - 8))
    _poly(c, t_low, SERIES[0], 2.5)
    _head(c, t_low, SERIES[0], 2.5)
    first = _bez(S, (bx0 + 150, 232), GT, t1=0.33)
    t_high = first + _bez(first[-1], (bx0 + 170, 222), (GA[0] - 13, GA[1] + 12))[1:]
    _poly(c, t_high, SERIES[1], 2.5)
    _head(c, t_high, SERIES[1], 2.5)
    crit = first + _bez(first[-1], (bx0 + 190, 226), (bx0 + 292, 216))[1:]
    _poly(c, crit, INK2, 2, dash="2 5")
    _circle(c, GT[0], GT[1], 15, SERIES[0], 0.30, SERIES[0], 1.5)
    _circle(c, GA[0], GA[1], 15, SERIES[1], 0.30, SERIES[1], 1.5)
    c.dot(S[0], S[1], INK, 4.5)
    c.text(S[0], S[1] - 14, "start", 11, "middle", INK2)
    c.text(GA[0] + 22, GA[1] - 6, "approval", 11, "start", INK)
    c.text(GA[0] + 22, GA[1] + 8, "goal", 11, "start", INK)
    c.text(GT[0] + 22, GT[1] - 2, "truth", 11, "start", INK)
    c.text(GT[0] + 22, GT[1] + 12, "goal", 11, "start", INK)
    c.text(bx0 + 96, 150, "Flash 2.5, α ≈ 0.73:", 11, "start", INK)
    c.text(bx0 + 96, 165, "lands on approval", 10.5, "start", INK2)
    c.text(bx0 + 60, 300, "Claude, α ≈ 0:", 11, "start", INK)
    c.text(bx0 + 60, 315, "holds its answer", 10.5, "start", INK2)
    c.text(bx0 + 240, 236, "α = α*:", 10.5, "start", INK2)
    c.text(bx0 + 240, 249, "reaches neither", 10.5, "start", INK2)
    legend(c, 22, 376, [("truth manifold", SERIES[0]), ("approval manifold", SERIES[1])], 11)
    c.text(704, 376, "schematic", 10.5, "end", INK3, italic=True)
    c.save(p)


def fig_6_2():
    def astar(theta, rt=1.0, ra=1.0):
        return rt / (rt - ra * math.cos(theta))

    assert abs(astar(math.pi) - 0.5) < 1e-12                      # Corollary 6.1
    assert abs(astar(math.pi / 2) - 1.0) < 1e-12
    for name, wf, cf, gap, idx in T61:                              # the alpha values are the sycophancy index, rounded
        assert abs(ALPHA[name] - idx) < 0.006 and abs((cf - wf) / 100 - gap) < 0.006
    p = reg("chapters/ch06_sycophancy_as_search_hijacking.md", "6.2",
            "The phase diagram of Section 6.3.2: the horizontal axis is the angle θ between the truth gradient "
            "and the approval gradient, and the vertical axis is the sycophancy parameter α. The solid curve is "
            "the critical value α* = 1 / (1 - cos θ) for gradients of equal size (Proposition 6.1); below it the "
            "search keeps a net component toward truth, above it the search moves toward agreement, and for "
            "opposed gradients (θ = 180 degrees) the critical value is 0.5. The dashed curve repeats the "
            "calculation for a truth gradient twice as large as the approval gradient, which tolerates a larger "
            "α. The marks at 180 degrees, the angle the test is designed to produce, are the α values the chapter"
            " assigns to the four models from the wrong-flip data of Table 6.1; they are the chapter's model "
            "estimates, not measurements of α.",
            "## 6.5 The Confidence Response: A Diagnostic Signal")
    c = Canvas(720, 400, "Above a critical weight on approval the search turns from truth")
    ax = Axes(c, 70, 52, 430, 280, (0, 180), (0, 1), [0, 45, 90, 135, 180], [0, 0.25, 0.5, 0.75, 1.0],
              "angle between truth and approval gradients, θ (degrees)", "sycophancy parameter α")
    th = [90 + 90 * i / 90 for i in range(91)]
    curve = [(ax.X(t), ax.Y(astar(math.radians(t)))) for t in th]
    region = curve + [(ax.X(180), ax.Y(1)), (ax.X(90), ax.Y(1))]
    c.add('<polygon points="' + " ".join(f"{x:.2f},{y:.2f}" for x, y in region)
          + f'" fill="{SERIES[1]}" fill-opacity="0.16"/>')
    c.polyline(curve, SERIES[1], 2.5, title="critical α for equal gradient sizes")
    th2 = [90 + 90 * i / 90 for i in range(91)]
    _poly(c, [(ax.X(t), ax.Y(astar(math.radians(t), 2.0, 1.0))) for t in th2], INK2, 1.5, dash="5 4")
    c.text(ax.X(172), ax.Y(0.945), "Region II: approval-seeking", 12, "end", INK, "600")
    c.text(ax.X(52), ax.Y(0.50), "Region I", 12, "middle", INK, "600")
    c.text(ax.X(52), ax.Y(0.50) + 15, "truth-seeking: a net", 11, "middle", INK2)
    c.text(ax.X(52), ax.Y(0.50) + 29, "component toward truth", 11, "middle", INK2)
    c.text(ax.X(117), ax.Y(0.64), "critical α*,", 10.5, "end", INK2)
    c.text(ax.X(117), ax.Y(0.64) + 13, "equal gradients", 10.5, "end", INK2)
    c.text(ax.X(172), ax.Y(0.83), "dashed: truth gradient", 10.5, "end", INK2)
    c.text(ax.X(172), ax.Y(0.83) + 13, "twice as large", 10.5, "end", INK2)
    ylab = {"Gemini 2.5 Flash": ax.Y(0.73) - 6, "Gemini 2.5 Pro": ax.Y(0.66) + 12, "Gemini 2.0 Flash": ax.Y(0.47) + 4,
            "Claude Sonnet 4.6": ax.Y(0.0) - 2}
    for name, a in ALPHA.items():
        c.dot(ax.X(180), ax.Y(a), CRITICAL if a > 0.5 else SERIES[0], 4.5, title=f"{name}, α {a}")
        c.text(ax.X(180) + 12, ylab[name], f"{name}  {('≈ 0' if a == 0 else a)}", 11, "start", INK2)
    c.text(ax.X(180) + 12, ax.Y(1.0) + 4, "α assigned in the chapter", 10.5, "start", INK3, italic=True)
    c.text(16, 388, "curves computed from Proposition 6.1; model marks are the chapter's estimates", 10.5, "start",
           INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 7
def fig_7_1():
    a, b, cc = -1.0, 0.0, 1.6
    k = 0.45 / 0.35                               # scales the depth of the wrong basin to the example's 0.45

    def f(x):
        return k * (x ** 4 / 4 - (a + b + cc) * x ** 3 / 3 + (a * b + a * cc + b * cc) * x * x / 2 - a * b * cc * x) + 0.45

    depth = f(b) - f(a)
    assert abs(depth - 0.45) < 1e-12 and abs(f(a)) < 1e-12 and f(cc) < f(a)
    impulse = 0.25
    assert impulse < depth
    p = reg("chapters/ch07_local_minima_and_dead_zones.md", "7.1",
            f"A basin of attraction in cross-section, drawn for an illustrative evaluation function with two "
            f"minima: the search has settled in the shallower one, a plausible but wrong answer, and the correct "
            f"answer is the deeper minimum to the right. The basin depth is the height of the lowest point of the "
            f"basin's boundary above the minimum (Definition 7.1). It is set to {depth:.2f}, the value in the "
            f"chapter's worked example of the anchored diagnosis, and the short arrow is that example's first "
            f"disconfirming datum, an impulse of {impulse}, which does not clear the boundary, so the search falls"
            f" back. Only an impulse larger than the depth carries the search over; the example's numbers are "
            f"illustrative values in the chapter, not measurements.",
            "## 7.7 The Geometry of Being Stuck")
    c = Canvas(720, 400, "Escape needs an impulse larger than the depth of the basin")
    ax = Axes(c, 70, 48, 600, 290, (-2.6, 2.45), (-1.35, 1.0), [], [-1.0, -0.5, 0, 0.5, 1.0], "state x (one direction through the landscape)",
              "evaluation f(x)")
    xs = [-1.8 + 4.25 * i / 425 for i in range(426)]
    pts = [(ax.X(x), ax.Y(f(x))) for x in xs if f(x) <= 1.0]
    c.polyline(pts, SERIES[2], 2.5, title="evaluation landscape")
    c.line(ax.X(b), ax.Y(f(b)) - 4, ax.X(b), ax.Y(1.0), INK3, 1.5, dash="3 4")
    c.text(ax.X(b) + 8, ax.Y(0.93), "boundary between the basins", 10.5, "start", INK2)
    c.line(ax.X(-2.0), ax.Y(depth), ax.X(b), ax.Y(depth), INK3, 1, dash="4 4")
    c.line(ax.X(-2.0), ax.Y(0), ax.X(a) - 12, ax.Y(0), INK3, 1, dash="4 4")
    # depth bracket
    xb = ax.X(-1.9)
    c.line(xb, ax.Y(0) - 1, xb, ax.Y(depth) + 1, INK, 1.5)
    for yy, s in ((ax.Y(0) - 1, -1), (ax.Y(depth) + 1, 1)):
        c.line(xb, yy, xb - 4, yy + s * 6, INK, 1.5)
        c.line(xb, yy, xb + 4, yy + s * 6, INK, 1.5)
    c.text(xb - 10, ax.Y(0.29), "basin depth", 11.5, "end", INK)
    c.text(xb - 10, ax.Y(0.29) + 15, f"{depth:.2f}", 11.5, "end", INK)
    # the small impulse
    xi = ax.X(a) - 14
    c.arrow(xi, ax.Y(0.03), xi, ax.Y(impulse), SERIES[1], 2.5)
    c.text(ax.X(-1.08), ax.Y(0.78), f"impulse {impulse}:", 11, "middle", INK)
    c.text(ax.X(-1.08), ax.Y(0.78) + 14, "falls back", 10.5, "middle", INK2)
    # the escaping impulse
    esc = _bez((ax.X(a) + 12, ax.Y(0.07)), (ax.X(-0.2), ax.Y(1.25)), (ax.X(0.75), ax.Y(0.0)))
    _poly(c, esc, SERIES[0], 2, dash="6 4")
    _head(c, esc, SERIES[0], 2)
    c.text(ax.X(0.52), ax.Y(0.52), "impulse larger than", 11, "start", INK)
    c.text(ax.X(0.52), ax.Y(0.52) + 14, "the depth: escapes", 11, "start", INK)
    c.dot(ax.X(a), ax.Y(f(a)) - 7, SERIES[1], 6, title="search state, settled in the wrong basin")
    c.text(ax.X(a), ax.Y(f(a)) + 20, "local minimum:", 11.5, "middle", INK)
    c.text(ax.X(a), ax.Y(f(a)) + 35, "plausible, wrong", 11, "middle", INK2)
    c.dot(ax.X(cc), ax.Y(f(cc)), SERIES[0], 4.5)
    c.text(ax.X(cc), ax.Y(f(cc)) + 20, "global minimum: correct answer", 11.5, "middle", INK)
    c.text(16, 388, "illustrative landscape; depth and impulse from the chapter's worked example", 10.5, "start", INK3,
           italic=True)
    c.save(p)


def fig_7_2():
    rows = [("Gemini 2.0 Flash", 0.09, 0.72, 0.38, 0.025), ("Gemini 2.5 Pro", 0.70, 0.35, 0.38, 0.093)]
    p = reg("chapters/ch07_local_minima_and_dead_zones.md", "7.2",
            "The multiplicative escape model of Section 7.7 for the two models the chapter works through, on a "
            "logarithmic vertical axis. Each line starts at 1 and is multiplied in turn by the self-monitoring "
            "score (M3) read as the probability of detecting that the search is stuck, the effort-scaling score "
            "(M4) read as the probability of correcting, and the 0.38 recovery rate read as the probability of "
            "escaping. One model loses most at detection and the other at correction, and both end below one in "
            "ten: 0.025 and 0.093. Reading the scores as probabilities and multiplying them is the chapter's "
            "modelling axiom, not a measured escape rate.",
            "## 7.8 Implications for Training and Evaluation")
    c = Canvas(720, 400, "Detection, correction and escape multiply, so the weakest link rules")
    ax = Axes(c, 80, 52, 470, 270, (-0.3, 3.3), (0.01, 1.0), [], [0.01, 0.03, 0.1, 0.3, 1.0], "",
              "probability the search is still on course to escape", ylog=True)
    stages = [("stuck in the", "wrong basin"), ("detects it", "× P(detect)"), ("and corrects", "× P(correct)"),
              ("and escapes", "× P(escape)")]
    for i, (s1, s2) in enumerate(stages):
        c.text(ax.X(i), ax.y0 + ax.h + 17, s1, 11.5, "middle", INK)
        c.text(ax.X(i), ax.y0 + ax.h + 32, s2, 10.5, "middle", INK2)
    for j, (name, d, e, r, quoted) in enumerate(rows):
        vals = [1.0, d, d * e, d * e * r]
        assert abs(vals[-1] - quoted) < 0.0006            # the chapter prints 0.025 and 0.093
        col = SERIES[j]
        pts = [(ax.X(i), ax.Y(v)) for i, v in enumerate(vals)]
        c.polyline(pts, col, 2.5, title=name)
        for i, ((px, py), v) in enumerate(zip(pts, vals)):
            c.dot(px, py, col, 4.5, title=f"{name}: {v:.3f}")
            if i:
                txt = f"{v:.2f}" if i == 1 else f"{v:.3f}"
                if j == 0 and i == 3:
                    c.text(px - 10, py + 17, txt, 11, "end", INK)
                else:
                    c.text(px, py + (20 if j == 0 else -11), txt, 11, "middle", INK)
        c.text(pts[-1][0] + 14, pts[-1][1] + 4, name, 11.5, "start", INK)
        c.text(pts[-1][0] + 14, pts[-1][1] + 19, f"{d:.2f} × {e:.2f} × {r:.2f}", 10.5, "start", INK2)
    c.text(16, 388, "inputs and products as printed in Section 7.7", 10.5, "start", INK3, italic=True)
    c.save(p)


# ------------------------------------------------------------------ chapter 8
def fig_8_1():
    rows = [("Evaluation order (T4)", "structural reordering", None, "none"),
            ("Gender swap (T2)", "demographic substitution", None, "none"),
            ("Sensory distractors (A1)", "irrelevant detail added", 4.6, "task-irrelevant content"),
            ("Emotional anchoring (E2)", "affective tone shifted", 6.8, "task-adjacent content"),
            ("Linguistic framing (T5)", "register transformed", 8.9, "the task-relevant content itself")]
    sig = [r[2] for r in rows if r[2]]
    assert sig == sorted(sig) == [4.6, 6.8, 8.9]
    p = reg("chapters/ch08_gauge_invariance_and_symmetry.md", "8.1",
            "The five content-preserving transformations of Table 8.2, in the order of the hierarchy of Section "
            "8.8.2. The bars are the Fisher-combined significance, in standard deviations, with which each "
            "transformation moved the models' judgments; the first two produced no significant displacement. The "
            "right-hand column is what the Salience Exploitation Hypothesis says each transformation modulates. The "
            "significance values are the ones the chapter reports from the Measuring AGI benchmarks; the salience "
            "column is the chapter's hypothesis, which it marks as speculation.",
            "## 8.6 Group-Theoretic Data Augmentation as Symmetry Restoration")
    c = Canvas(720, 400, "Invariance holds until a transformation changes what is salient")
    bx0, per = 222, 25.0
    c.text(bx0, 58, "combined significance (σ)", 11, "start", INK2)
    c.text(500, 58, "salience modulated (hypothesis)", 11, "start", INK2)
    y = 74
    groups = [("Preserved: no significant displacement", rows[:2]), ("Broken", rows[2:])]
    for gname, grp in groups:
        c.text(22, y + 14, gname, 11, "start", INK3, italic=True)
        c.line(22, y + 21, 698, y + 21, GRID, 1)
        y += 28
        for name, kind, s, sal in grp:
            c.text(22, y + 17, name, 12, "start", INK, "600")
            c.text(22, y + 32, kind, 10.5, "start", INK2)
            if s is None:
                c.text(bx0, y + 24, "not significant", 11, "start", INK2)
            else:
                c.hrect(bx0, y + 12, s * per, 16, SERIES[1] if s < 8 else CRITICAL, title=f"{name}: {s} sigma")
                c.text(bx0 + s * per + 8, y + 24, f"{s}σ", 11.5, "start", INK)
            c.text(500, y + 24, sal, 11, "start", INK2)
            y += 46
        y += 6
    c.text(16, 388, "significance as reported in the chapter (Table 8.2)", 10.5, "start", INK3, italic=True)
    c.save(p)
