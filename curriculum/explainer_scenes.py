"""Storyboards for the illustrated explainer lectures (no on-screen presenter; narrated off-screen).

Each storyboard places hand-drawn-style line illustrations and hand-lettered words in one continuous world,
and moves a camera between "stations" (one per script scene). Every beat is pinned to a narration line:
    at(li, off)  ->  seconds after line `li` starts speaking.

Illustrations are original, simple line drawings in the course palette.
"""
import html
import math

INK, MAROON, TEAL, COPPER, SAGE, CREAM, SKY = "#2a2420", "#8a1c3c", "#2f6f8f", "#d9822b", "#6f9264", "#f3ead7", "#cfe3ea"
SW = 5  # base stroke width


def E(s):
    return html.escape(str(s))


# ───────────────────────── drawing primitives ─────────────────────────
def P(d, stroke=INK, fill="none", w=SW, op=1):
    return f'<path d="{d}" stroke="{stroke}" stroke-width="{w}" fill="{fill}" fill-opacity="{op}" stroke-linecap="round" stroke-linejoin="round"/>'


def C(cx, cy, r, stroke=INK, fill="none", w=SW, op=1):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{stroke}" stroke-width="{w}" fill="{fill}" fill-opacity="{op}"/>'


def T(x, y, s, size=54, color=INK, anchor="middle", weight="700"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{E(s)}</text>'


def rrect(x, y, w, h, r=18):
    return f"M{x+r} {y} H{x+w-r} Q{x+w} {y} {x+w} {y+r} V{y+h-r} Q{x+w} {y+h} {x+w-r} {y+h} H{x+r} Q{x} {y+h} {x} {y+h-r} V{y+r} Q{x} {y} {x+r} {y}Z"


def arrow(x1, y1, x2, y2, color=INK, w=SW, bend=0):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    nx, ny = -(y2 - y1), (x2 - x1)
    L = math.hypot(nx, ny) or 1
    cx, cy = mx + nx / L * bend, my + ny / L * bend
    ang = math.atan2(y2 - cy, x2 - cx)
    a1, a2 = ang + 2.6, ang - 2.6
    head = f"M{x2 + 22*math.cos(a1):.1f} {y2 + 22*math.sin(a1):.1f} L{x2} {y2} L{x2 + 22*math.cos(a2):.1f} {y2 + 22*math.sin(a2):.1f}"
    return P(f"M{x1} {y1} Q{cx:.1f} {cy:.1f} {x2} {y2}", color, w=w) + P(head, color, w=w)


def dotted(points, color=INK):
    d = "M" + " L".join(f"{x} {y}" for x, y in points)
    return f'<path d="{d}" stroke="{color}" stroke-width="4" fill="none" stroke-dasharray="2 18" stroke-linecap="round" opacity=".55"/>'


# ───────────────────────── illustration library ─────────────────────────
def bubble(x, y, w, h, fill="#fff", tail="left"):
    tx = x + 60 if tail == "left" else x + w - 60
    return P(rrect(x, y, w, h, 30), fill=fill) + P(f"M{tx-20} {y+h-2} L{tx-40} {y+h+50} L{tx+20} {y+h-2}", fill=fill)


def kettle(cx, cy, s=1.0, dent=True):
    k = lambda v: v * s  # noqa: E731
    body = f"M{cx-k(110)} {cy+k(80)} Q{cx-k(130)} {cy-k(60)} {cx} {cy-k(70)} Q{cx+k(130)} {cy-k(60)} {cx+k(110)} {cy+k(80)} Z"
    out = P(body, fill=TEAL, op=.85)
    out += P(f"M{cx+k(95)} {cy+k(5)} Q{cx+k(170)} {cy-k(10)} {cx+k(190)} {cy-k(70)}", w=SW + 2)
    out += P(f"M{cx-k(70)} {cy-k(70)} Q{cx} {cy-k(170)} {cx+k(70)} {cy-k(70)}", w=SW + 1)
    out += P(f"M{cx-k(40)} {cy-k(72)} Q{cx} {cy-k(95)} {cx+k(40)} {cy-k(72)}") + C(cx, cy - k(98), k(9), fill=INK)
    if dent:
        out += P(f"M{cx-k(30)} {cy+k(10)} l{k(18)} {k(16)} l{k(14)} {-k(20)} l{k(16)} {k(18)}", stroke=CREAM, w=SW)
    return out


def magnifier(cx, cy, s=1.0, color=INK):
    return C(cx, cy, 46 * s, color, fill="#fff", op=.7) + P(f"M{cx+34*s} {cy+34*s} L{cx+86*s} {cy+86*s}", color, w=SW + 5)


def checklist(x, y, s=1.0, n=3, color=INK):
    out = P(rrect(x, y, 150 * s, 190 * s, 14), color, fill="#fff")
    for i in range(n):
        yy = y + (45 + i * 50) * s
        out += P(f"M{x+22*s} {yy} l{12*s} {12*s} l{20*s} {-24*s}", SAGE, w=SW + 1) + P(f"M{x+70*s} {yy} H{x+128*s}", color, w=4)
    return out


def wrench(cx, cy, s=1.0, color=INK, ang=-40):
    return (f'<g transform="rotate({ang} {cx} {cy})">' + P(rrect(cx - 12 * s, cy - 70 * s, 24 * s, 140 * s, 10), color, fill=COPPER, op=.9)
            + P(f"M{cx-34*s} {cy-70*s} a{34*s} {34*s} 0 1 1 {68*s} 0 l-{16*s} {-4*s} l-{10*s} {22*s} h-{16*s} l-{10*s} {-22*s} Z", color, fill=COPPER, op=.9) + "</g>")


def coin(cx, cy, s=1.0):
    return C(cx, cy, 52 * s, fill=COPPER, op=.9) + T(cx, cy + 20 * s, "$", int(58 * s), INK)


def check(cx, cy, s=1.0, color=SAGE):
    return P(f"M{cx-50*s} {cy} L{cx-12*s} {cy+38*s} L{cx+58*s} {cy-46*s}", color, w=SW + 7)


def scroll(cx, cy, s=1.0):
    x, y, w, h = cx - 90 * s, cy - 110 * s, 180 * s, 220 * s
    out = P(f"M{x} {y+20*s} H{x+w} V{y+h-20*s} H{x} Z", fill="#fff")
    out += P(f"M{x-20*s} {y+20*s} a20 20 0 0 1 40 0 M{x+w-20*s} {y+h-20*s} a20 20 0 0 0 40 0")
    for i in range(4):
        out += P(f"M{x+25*s} {y+(60+i*36)*s} H{x+w-25*s - (40*s if i == 3 else 0)}", w=4)
    return out


def toolbox(cx, cy, s=1.0):
    out = P(rrect(cx - 130 * s, cy - 40 * s, 260 * s, 130 * s, 12), fill=MAROON, op=.85)
    out += P(f"M{cx-50*s} {cy-40*s} V{cy-80*s} H{cx+50*s} V{cy-40*s}", w=SW + 2)
    out += P(f"M{cx-130*s} {cy+10*s} H{cx+130*s}")
    return out + wrench(cx + 70 * s, cy - 70 * s, .55 * s, ang=30)


def gear(cx, cy, r=60, color=INK, fill=SKY):
    pts = []
    for i in range(16):
        a = i * math.pi / 8
        rr = r if i % 2 == 0 else r * .78
        pts.append(f"{cx + rr*math.cos(a):.1f} {cy + rr*math.sin(a):.1f}")
    return P("M" + " L".join(pts) + "Z", color, fill=fill) + C(cx, cy, r * .3, color, fill="#fff")


def brain(cx, cy, s=1.0, fill="#f5c9d3"):
    d = (f"M{cx-80*s} {cy+30*s} Q{cx-110*s} {cy-10*s} {cx-70*s} {cy-45*s} Q{cx-60*s} {cy-90*s} {cx-10*s} {cy-75*s} "
         f"Q{cx+30*s} {cy-100*s} {cx+60*s} {cy-60*s} Q{cx+110*s} {cy-40*s} {cx+85*s} {cy+15*s} Q{cx+90*s} {cy+60*s} {cx+40*s} {cy+60*s} "
         f"Q{cx} {cy+85*s} {cx-35*s} {cy+60*s} Q{cx-75*s} {cy+70*s} {cx-80*s} {cy+30*s}Z")
    return P(d, fill=fill) + P(f"M{cx} {cy-70*s} Q{cx-20*s} {cy-20*s} {cx+5*s} {cy+60*s} M{cx-60*s} {cy-10*s} Q{cx-30*s} {cy-25*s} {cx-15*s} {cy} M{cx+30*s} {cy-35*s} Q{cx+55*s} {cy-5*s} {cx+40*s} {cy+25*s}", w=4)


def notebook(cx, cy, s=1.0):
    out = P(rrect(cx - 80 * s, cy - 100 * s, 160 * s, 200 * s, 10), fill=SAGE, op=.75)
    for i in range(5):
        out += C(cx - 80 * s, cy - 75 * s + i * 38 * s, 8 * s, fill="#fff")
    return out + P(f"M{cx-40*s} {cy-40*s} H{cx+50*s} M{cx-40*s} {cy} H{cx+50*s} M{cx-40*s} {cy+40*s} H{cx+20*s}", w=4)


def monitor(cx, cy, s=1.0):
    return (P(rrect(cx - 110 * s, cy - 80 * s, 220 * s, 150 * s, 12), fill=SKY) + P(f"M{cx} {cy+70*s} V{cy+105*s} M{cx-50*s} {cy+108*s} H{cx+50*s}", w=SW + 2)
            + P(f"M{cx-30*s} {cy-20*s} l{50*s} {30*s} l{-18*s} {6*s} l{14*s} {26*s} l{-12*s} {6*s} l{-14*s} {-26*s} l{-16*s} {14*s} Z", fill="#fff"))


def network(cx, cy, s=1.0):
    pts = [(cx - 90 * s, cy - 40 * s), (cx + 10 * s, cy - 80 * s), (cx + 100 * s, cy - 20 * s), (cx + 60 * s, cy + 70 * s), (cx - 50 * s, cy + 60 * s)]
    out = ""
    for i, (x, y) in enumerate(pts):
        for x2, y2 in pts[i + 1:]:
            out += P(f"M{x:.0f} {y:.0f} L{x2:.0f} {y2:.0f}", w=3)
    for (x, y), c in zip(pts, [MAROON, TEAL, COPPER, SAGE, MAROON]):
        out += C(f"{x:.0f}", f"{y:.0f}", 26 * s, fill=c, op=.9)
    return out


def hourglass(cx, cy, s=1.0):
    return (P(f"M{cx-60*s} {cy-100*s} H{cx+60*s} M{cx-60*s} {cy+100*s} H{cx+60*s}", w=SW + 3)
            + P(f"M{cx-45*s} {cy-100*s} Q{cx-45*s} {cy-20*s} {cx} {cy} Q{cx-45*s} {cy+20*s} {cx-45*s} {cy+100*s} M{cx+45*s} {cy-100*s} Q{cx+45*s} {cy-20*s} {cx} {cy} Q{cx+45*s} {cy+20*s} {cx+45*s} {cy+100*s}")
            + P(f"M{cx-30*s} {cy+95*s} Q{cx} {cy+40*s} {cx+30*s} {cy+95*s}Z", fill=COPPER, op=.9))


def blocks(cx, cy, s=1.0):
    out = ""
    for (x, y, c) in [(-110, 20, MAROON), (-10, 20, TEAL), (-60, -80, COPPER)]:
        out += P(rrect(cx + x * s, cy + y * s, 95 * s, 95 * s, 6), fill=c, op=.85)
    return out + P(f"M{cx+120*s} {cy-150*s} V{cy-40*s} M{cx+120*s} {cy-150*s} H{cx-10*s} V{cy-100*s}", w=SW)  # a little crane arm


def rulecard(cx, cy, s=1.0, a="IF fever", b="THEN test"):
    return P(rrect(cx - 120 * s, cy - 70 * s, 240 * s, 140 * s, 12), fill="#fff") + T(cx, cy - 10 * s, a, int(34 * s)) + T(cx, cy + 40 * s, b, int(34 * s), MAROON)


def venn3(cx, cy, s=1.0):
    return (C(cx - 55 * s, cy - 30 * s, 85 * s, MAROON, fill=MAROON, op=.25) + C(cx + 55 * s, cy - 30 * s, 85 * s, TEAL, fill=TEAL, op=.25)
            + C(cx, cy + 60 * s, 85 * s, COPPER, fill=COPPER, op=.25))


def plug(cx, cy, s=1.0):
    return (P(rrect(cx - 50 * s, cy - 40 * s, 100 * s, 90 * s, 16), fill=TEAL, op=.85) + P(f"M{cx-22*s} {cy-40*s} V{cy-85*s} M{cx+22*s} {cy-40*s} V{cy-85*s}", w=SW + 3)
            + P(f"M{cx} {cy+50*s} Q{cx} {cy+120*s} {cx+90*s} {cy+130*s}", w=SW + 1))


def compass(cx, cy, s=1.0):
    return (C(cx, cy - 90 * s, 14 * s, fill=INK) + P(f"M{cx} {cy-80*s} L{cx-60*s} {cy+90*s} M{cx} {cy-80*s} L{cx+60*s} {cy+90*s}", w=SW + 2)
            + P(f"M{cx-120*s} {cy+110*s} Q{cx} {cy+40*s} {cx+120*s} {cy+110*s}", TEAL, w=4))


def molecule(cx, cy, s=1.0):
    pts = [(cx + 60 * s * math.cos(a), cy + 60 * s * math.sin(a)) for a in [i * math.pi / 3 + math.pi / 6 for i in range(6)]]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
    return P(d, fill=SKY) + P(f"M{pts[0][0]:.1f} {pts[0][1]:.1f} l{50*s} {28*s} M{pts[3][0]:.1f} {pts[3][1]:.1f} l{-50*s} {-28*s}") + C(f"{pts[0][0]+50*s:.1f}", f"{pts[0][1]+28*s:.1f}", 12 * s, fill=MAROON)


def bacteria(cx, cy, s=1.0):
    out = ""
    for dx, dy, a in [(-40, -20, 20), (45, 25, -30), (10, -60, 70)]:
        out += f'<g transform="rotate({a} {cx+dx*s} {cy+dy*s})">' + P(rrect(cx + (dx - 45) * s, cy + (dy - 18) * s, 90 * s, 36 * s, 18 * s), fill=SAGE, op=.85) + P(f"M{cx+(dx+45)*s} {cy+dy*s} q{15*s} {-12*s} {30*s} 0 t{30*s} 0", w=3) + "</g>"
    return out


def calendar(cx, cy, s=1.0):
    out = ""
    for i in range(3):
        o = i * 22 * s
        out += P(rrect(cx - 90 * s + o, cy - 90 * s - o, 180 * s, 170 * s, 10), fill="#fff") + P(f"M{cx-90*s+o} {cy-50*s-o} H{cx+90*s+o}", MAROON, w=SW + 4)
    return out + T(cx + 44 * s, cy + 20 * s - 44 * s, "yrs", int(46 * s), MAROON)


def scale(cx, cy, s=1.0):
    return (P(f"M{cx} {cy-110*s} V{cy+100*s} M{cx-70*s} {cy+100*s} H{cx+70*s}", w=SW + 2) + P(f"M{cx-130*s} {cy-40*s} L{cx+130*s} {cy-100*s}", w=SW + 2)
            + P(f"M{cx-130*s} {cy-40*s} l{-40*s} {70*s} h{80*s} Z", fill=MAROON, op=.85) + P(f"M{cx+130*s} {cy-100*s} l{-40*s} {70*s} h{80*s} Z", fill=COPPER, op=.85)
            + T(cx - 130 * s, cy + 78 * s, "cost", int(34 * s), MAROON) + T(cx + 130 * s, cy + 18 * s, "value", int(34 * s), COPPER))


def beaker(cx, cy, s=1.0):
    return (P(f"M{cx-40*s} {cy-110*s} V{cy-30*s} L{cx-100*s} {cy+90*s} Q{cx-105*s} {cy+110*s} {cx-80*s} {cy+110*s} H{cx+80*s} Q{cx+105*s} {cy+110*s} {cx+100*s} {cy+90*s} L{cx+40*s} {cy-30*s} V{cy-110*s}")
            + P(f"M{cx-70*s} {cy+40*s} H{cx+70*s} L{cx+92*s} {cy+92*s} Q{cx+95*s} {cy+104*s} {cx+80*s} {cy+104*s} H{cx-80*s} Q{cx-95*s} {cy+104*s} {cx-92*s} {cy+92*s}Z", fill=SAGE, op=.8)
            + C(cx - 20 * s, cy + 70 * s, 9 * s, fill="#fff") + C(cx + 25 * s, cy + 55 * s, 6 * s, fill="#fff"))


def ladder(x, y, h, rungs, w=260):
    out = P(f"M{x} {y} V{y-h} M{x+w} {y} V{y-h}", w=SW + 3)
    step = h / (rungs + 0.4)
    return out, [y - step * (i + 0.7) for i in range(rungs)], step


def lisp(cx, cy, s=1.0):
    return T(cx, cy, "(defun draw (part) ...)", int(46 * s), TEAL)


def cross(cx, cy, s=1.0):
    return P(f"M{cx-60*s} {cy-60*s} L{cx+60*s} {cy+60*s} M{cx+60*s} {cy-60*s} L{cx-60*s} {cy+60*s}", MAROON, w=SW + 6)


def pit(cx, cy, s=1.0):
    return P(f"M{cx-170*s} {cy} Q{cx-150*s} {cy+20*s} {cx-110*s} {cy+18*s} Q{cx} {cy+140*s} {cx+110*s} {cy+18*s} Q{cx+150*s} {cy+20*s} {cx+170*s} {cy}", fill="#c7a98a", op=.6) + P(f"M{cx-210*s} {cy} H{cx+210*s}", w=SW + 1)


# ───────────────────────── storyboard builder ─────────────────────────
class Board:
    def __init__(self, cues, scene_starts):
        self.cues, self.ss = cues, scene_starts
        self.items, self.cam, self.n = [], [], 0

    def at(self, li, off=0.0):
        return self.cues[li][0] + off

    def add(self, svg, fx="draw", li=0, off=0.0, dur=1.2, out=None, path=None):
        self.n += 1
        it = {"id": f"i{self.n}", "svg": svg, "fx": fx, "t0": round(self.at(li, off), 3), "dur": dur}
        if out is not None:
            it["out"] = round(out, 3)
        if path:
            it["path"] = path
        self.items.append(it)

    def write(self, x, y, s, li, off=0.0, size=54, color=INK, anchor="middle", dur=None):
        self.add(T(x, y, s, size, color, anchor), "write", li, off, dur or max(0.5, 0.045 * len(s)))

    def look(self, li, x, y, w=1600, off=-0.6, dur=None, t=None):
        if dur is None:   # longer trips across the board get a little more time
            last = max(self.cam, key=lambda k: k["t"]) if self.cam else {"x": x, "y": y, "w": w}
            dur = round(1.3 + min(1.3, (math.hypot(x - last["x"], y - last["y"]) + abs(w - last["w"])) / 4500), 2)
        self.cam.append({"t": round(t if t is not None else self.at(li, off), 3), "dur": dur, "x": x, "y": y, "w": w})

    # ── the whole board: where the stations sit, the zoom-out, and the printable map ──
    cells = None

    def bbox(self, pad=80):
        xs = [c[0] for c in self.cells]; ys = [c[1] for c in self.cells]
        return (min(xs) - 860 - pad, min(ys) - 500 - pad, max(xs) + 860 + pad, max(ys) + 500 + pad)

    def overview(self, li=None, off=-0.3, t=None):
        x0, y0, x1, y1 = self.bbox(40)
        w = max(x1 - x0, (y1 - y0) * 16 / 9)
        self.look(li, (x0 + x1) / 2, (y0 + y1) / 2, w, off=off, t=t, dur=2.4)

    def finale(self):
        """After the last word, pull back to show the whole board (the module's map)."""
        self.overview(t=self.cues[-1][1] + 0.3)

    def timeline(self):
        return {"items": self.items, "cam": sorted(self.cam, key=lambda k: k["t"])}


def grid(n, cols=None, cw=2000, ch=1150):
    cols = cols or (2 if n <= 4 else 3)
    return [((i % cols) * cw, (i // cols) * ch) for i in range(n)]


# ───────────────────────── Module 2 · First Riff ─────────────────────────
def m02(b):
    # a 3×3 board read left-to-right; the loop station's "narrow tools" sub-area fills the cell below it
    S = [(0, 0), (2000, 0), (4000, 0), (0, 1250), (2000, 1250), (0, 2500), (2000, 2500), (4000, 2500)]
    b.cells = S + [(4000, 1100)]

    # 0 · title
    x, y = S[0]
    b.look(0, x, y, 1500, t=0)
    b.add(P(f"M{x-460} {y+40} Q{x} {y+10} {x+460} {y+40}", MAROON, w=10), "draw", 0, 0.1, 0.9)
    b.write(x, y - 30, "First Riff", 0, -0.4, 160, MAROON, dur=1.4)
    b.write(x, y + 130, "Track 02 · the minimum viable agent", 0, 1.2, 60, INK)
    b.write(x, y + 290, "concepts after Caldwell, The Agentic AI Bible · ch. 2", 1, 0.0, 42, TEAL)
    b.add(gear(x - 560, y - 270, 60), "draw", 1, 0.8, 0.9)
    b.add(blocks(x + 560, y - 200, .7), "draw", 1, 2.6, 1.0)

    # 1 · a single request
    x, y = S[1]
    b.look(2, x, y, 1700)
    b.add(bubble(x - 790, y - 400, 740, 230), "draw", 2, 0.0, 1.0)
    b.write(x - 420, y - 310, "“My kettle arrived dented.", 2, 0.5, 54)
    b.write(x - 420, y - 235, "I'd like a refund.”", 2, 1.5, 54)
    b.add(kettle(x - 420, y + 190, 1.5), "draw", 2, 1.0, 1.5)
    b.write(x + 330, y - 380, "chatbot", 3, 0.0, 66, TEAL)
    b.add(bubble(x + 50, y - 340, 560, 140, "#fff", "right"), "draw", 3, 0.4, 0.8)
    b.write(x + 330, y - 252, "“Sorry! Contact support.”", 3, 1.0, 44)
    b.add(cross(x + 690, y - 270, .55), "draw", 3, 2.6, 0.5)
    b.write(x + 340, y - 30, "agent", 4, 0.0, 66, MAROON)
    steps = [(x - 10, magnifier(x - 20, y + 120, 1.0), "look up"), (x + 230, checklist(x + 160, y + 25, 1.0), "eligible?"),
             (x + 480, coin(x + 480, y + 120, 1.05), "refund"), (x + 720, check(x + 720, y + 120, 1.05), "confirm")]
    for k, (sx, art, label) in enumerate(steps):
        b.add(art, "draw", 4, 0.6 + k * 1.3, 0.9)
        b.write(sx, y + 300, label, 4, 1.0 + k * 1.3, 48)
        if k:
            b.add(arrow(steps[k - 1][0] + 75, y + 120, sx - 75, y + 120, MAROON, 5, -22), "draw", 4, 0.4 + k * 1.3, 0.5)
    b.look(5, x + 330, y + 60, 1650)
    b.write(x + 340, y + 420, "each step depends on what it observed", 5, 0.4, 54, MAROON)

    # 2 · minimum viable agent: three ingredients and a loop
    x, y = S[2]
    b.look(6, x, y, 1700)
    b.write(x, y - 390, "Three ingredients and a loop", 6, 0.0, 84, MAROON)
    b.add(scroll(x - 580, y - 170, .85), "draw", 6, 1.2, 0.9); b.write(x - 580, y + 10, "system prompt", 6, 1.8, 50)
    b.add(toolbox(x - 580, y + 110, .75), "draw", 6, 2.6, 0.9); b.write(x - 580, y + 245, "tools", 6, 3.1, 50)
    b.add(bubble(x - 760, y + 290, 360, 100), "draw", 6, 3.8, 0.7); b.write(x - 580, y + 355, "user message", 6, 4.2, 42)
    cx, cy, r = x + 300, y + 40, 240
    b.add(arrow(cx - 30, cy - r, cx + r * .87, cy + r * .5 - 30, MAROON, 8, -100), "draw", 7, 0.2, 0.8)
    b.add(arrow(cx + r * .87 - 20, cy + r * .5 + 25, cx - r * .87 + 20, cy + r * .5 + 25, TEAL, 8, -100), "draw", 7, 1.0, 0.8)
    b.add(arrow(cx - r * .87, cy + r * .5 - 30, cx - 30, cy - r, COPPER, 8, -100), "draw", 7, 1.8, 0.8)
    b.write(cx + 260, cy - 190, "reason", 7, 0.4, 62, MAROON)
    b.write(cx, cy + 380, "act", 7, 1.2, 62, TEAL)
    b.write(cx - 270, cy - 190, "observe", 7, 2.0, 62, COPPER)
    b.add(brain(cx, cy, 1.0), "draw", 7, 2.6, 1.0)
    b.add(C(0, 0, 18, MAROON, fill=MAROON), "orbit", 7, 3.2, 0.4, path=[cx, cy, r + 12, r + 12, 0.3])
    # below the loop: narrow tools, then the blast radius
    b.look(8, x, y + 1000, 1650)
    b.write(x - 420, y + 640, "one narrow job each", 8, 0.0, 62, INK)
    for k, (name, c) in enumerate([("lookup_order(order_id)", TEAL), ("check_eligibility(order)", COPPER), ("issue_refund(order, amount)", MAROON)]):
        yy = y + 800 + k * 170
        b.add(wrench(x - 720, yy, .42, ang=45), "draw", 8, 0.6 + k * 0.7, 0.5)
        b.write(x - 650, yy + 16, name, 8, 0.9 + k * 0.7, 46, c, "start")
    for k, rr in enumerate([170, 265, 360]):
        b.add(C(x + 420, y + 1000, rr, MAROON, w=5), "draw", 9, 0.2 + k * 0.45, 0.6)
    b.add(toolbox(x + 420, y + 1010, .9), "draw", 9, 0.0, 0.7)
    b.write(x + 420, y + 1440, "toolset = blast radius", 9, 1.3, 62, MAROON)

    # 3 · five-level ladder
    x, y = S[3]
    b.look(10, x, y, 1600)
    lad, ys, step = ladder(x - 600, y + 430, 880, 6, 200)
    b.add(lad, "draw", 10, 0.0, 1.0)
    labels = ["L0  scripted", "L1  text function", "L2  + tools", "L3  + planning", "L4  + memory", "L5  multi-agent"]
    colors = [INK, TEAL, COPPER, MAROON, SAGE, MAROON]
    when = [(11, 0.2), (12, 0.0), (12, 2.4), (13, 0.0), (13, 2.0), (14, 0.0)]
    for k, (lab, (li, off), yy) in enumerate(zip(labels, when, ys)):
        b.add(P(f"M{x-600} {yy:.0f} H{x-400}", w=SW + 3), "draw", li, off, 0.4)
        b.write(x - 350, yy + 20, lab, li, off + 0.3, 62, colors[k], "start")
        ix = x + 330
        art = {0: gear(ix, yy, 44), 1: T(ix, yy + 22, "Aa", 74, TEAL), 2: wrench(ix, yy, .48, ang=40), 3: checklist(ix - 60, yy - 72, .7),
               4: notebook(ix, yy, .55), 5: network(ix, yy, .55)}[k]
        b.add(art, "pop" if k == 1 else "draw", li, off + 0.6, 0.6)
    b.write(x + 430, ys[4] + 14, "⚠ memory poisoning", 13, 3.6, 40, MAROON, "start")
    b.look(14, x, ys[5] + 300, 1650)

    # 4 · pitfalls
    x, y = S[4]
    b.look(15, x, y - 50, 1650)
    b.write(x, y - 380, "Three traps", 15, 0.0, 96, MAROON)
    for px, li in [(x - 540, 16), (x, 17), (x + 540, 18)]:
        b.add(pit(px, y + 280, 1.05), "draw", li, 0.0, 0.8)
    b.add(brain(x - 540, y - 80, 1.15), "draw", 16, 0.4, 0.8); b.write(x - 540, y + 150, "ground truth?", 16, 1.2, 54, MAROON)
    b.add(cross(x - 540, y - 80, .9), "draw", 16, 2.4, 0.5)
    b.add(hourglass(x, y - 80, 1.15), "draw", 17, 0.4, 1.0); b.write(x, y + 150, "longer ≠ better", 17, 1.4, 54, MAROON)
    for k in range(5):
        b.add(wrench(x + 450 + k * 45, y - 80 - (k % 2) * 40, .62, ang=-60 + k * 30), "draw", 18, 0.3 + k * 0.25, 0.4)
    b.write(x + 540, y + 150, "more tools ≠ capability", 18, 1.8, 54, MAROON)

    # 5 · a short, honest history
    x, y = S[5]
    b.look(19, x, y, 1750)
    b.write(x, y - 400, "Old problems, new substrate", 19, 0.0, 88, MAROON)
    b.add(arrow(x - 800, y + 230, x + 800, y + 230, INK, 7), "draw", 19, 1.0, 1.4)
    marks = [(x - 600, "1971–72", "STRIPS · SHRDLU", blocks(x - 600, y + 30, .95), 20),
             (x - 200, "1980s", "expert systems", rulecard(x - 200, y + 50, 1.05), 21),
             (x + 200, "1990s", "BDI", venn3(x + 200, y + 30, 1.0), 22),
             (x + 600, "today", "tools + MCP", plug(x + 600, y + 30, 1.15), 23)]
    for mx, yr, lab, art, li in marks:
        b.add(P(f"M{mx} {y+205} V{y+255}", w=SW + 3), "draw", li, 0.0, 0.3)
        b.write(mx, y + 320, yr, li, 0.2, 56, TEAL)
        b.add(art, "draw", li, 0.4, 1.0)
        b.write(mx, y + 395, lab, li, 1.2, 48)
    b.write(x - 200, y - 150, "the frame problem", 21, 2.4, 46, MAROON)
    b.write(x + 240, y - 250, "beliefs · desires · intentions", 22, 1.4, 42, MAROON)

    # 6 · from the field
    x, y = S[6]
    b.look(24, x, y, 1650)
    b.write(x, y - 390, "From the field · Addison Boyer", 24, 0.0, 78, COPPER)
    b.add(compass(x - 520, y - 110, 1.2), "draw", 25, 0.4, 1.0)
    b.write(x - 520, y + 140, "Lisp inside AutoCAD", 25, 1.2, 54)
    b.write(x - 520, y + 225, "(defun draw (part) …)", 25, 2.4, 46, TEAL)
    b.add(molecule(x, y - 110, 1.35), "draw", 26, 0.4, 1.0); b.write(x, y + 90, "DENDRAL", 26, 1.2, 58, TEAL)
    b.add(bacteria(x + 480, y - 110, 1.35), "draw", 26, 3.2, 1.0); b.write(x + 480, y + 90, "MYCIN", 26, 3.8, 58, SAGE)
    b.add(calendar(x + 140, y + 330, .95), "draw", 27, 0.3, 1.0)
    b.look(28, x + 330, y + 240, 1450)
    b.add(scale(x + 620, y + 330, 1.0), "draw", 28, 0.2, 1.2)
    b.write(x + 620, y + 540, "scope the cost", 28, 1.8, 62, MAROON)

    # 7 · the whole board is the map; then name it honestly, and off to lab
    x, y = S[7]
    b.overview(29)
    b.look(30, x, y, 1650)
    b.write(x - 330, y - 260, "name the level", 30, 0.6, 70, MAROON)
    b.write(x - 330, y - 170, "honestly", 30, 1.4, 70, MAROON)
    b.write(x - 330, y + 40, "L1–L2 ≠ L4", 30, 3.0, 96, MAROON)
    b.add(beaker(x + 420, y - 40, 1.4), "draw", 31, 0.2, 1.0)
    b.write(x + 420, y + 260, "see you in lab", 31, 1.0, 72, TEAL)
    b.finale()


STORYBOARDS = {"m02": m02}
