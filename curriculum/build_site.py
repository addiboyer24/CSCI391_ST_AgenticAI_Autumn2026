"""Build the CSCI 391 curriculum site.

    python curriculum/build_site.py

Reads curriculum/course_data.py and writes:
  * index.html                          (repo root, the course page)
  * instructor-guide.html               (repo root, the same course with module maps and track scripts instead of videos)
  * curriculum/img/<id>-mindmap.svg     (radial mind map; fallback when no explainer board exists)
  * curriculum/img/<id>-board.pdf/.jpg   (the illustrated board from the video = the module mind map; made by build_explainer.py)
Optional inputs: video_scripts.py (Encore lectures) and checks.py (practice quizzes).
"""
import html
import re
import string
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import course_data as D  # noqa: E402

try:
    import video_scripts as VS  # noqa: E402
    LECTURE = {l["id"]: l for l in VS.LECTURES}
except ImportError:
    LECTURE = {}

PRIVATE = os.path.join(HERE, "private")  # gitignored: graded quizzes and the guide password
sys.path.insert(0, PRIVATE)
try:
    import graded_quizzes as GQ  # noqa: E402  (questions only, never answers: the guide is public)
    GRADED = GQ.QUIZZES
except ImportError:
    GRADED = {}

try:
    import checks as CK  # noqa: E402
    CHECKS = CK.CHECKS
except ImportError:
    CHECKS = {}


def track_video(lec_id):
    """A lab or project walkthrough track, if its rendered MP4 exists."""
    lec = LECTURE.get(lec_id)
    return lec if lec and os.path.exists(os.path.join(HERE, "video", lec_id + ".mp4")) else None


TRACK_FOR = {l["for"]: l["id"] for l in LECTURE.values() if l.get("for")}


def video_for(m):
    """The Encore lecture for a module, if its rendered MP4 exists."""
    lec = LECTURE.get(m["id"])
    if lec and os.path.exists(os.path.join(HERE, "video", m["id"] + ".mp4")):
        return lec
    return None

IMG = os.path.join(HERE, "img")
os.makedirs(IMG, exist_ok=True)

E = lambda s: html.escape(str(s), quote=True)  # noqa: E731
FONT = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MAROON, COPPER, INK, CREAM = "#70002e", "#ED8B00", "#1f1a1c", "#efe8d4"
BRANCH_COLORS = ["#70002e", "#b8432f", "#c77700", "#2d6a87", "#3f7a55", "#5a4787"]
TINTS = ["#f6e9ee", "#f9ebe7", "#fdf1df", "#e6f0f5", "#e7f1ea", "#eeeaf5"]


def wrap(text, width, max_lines=None):
    lines = textwrap.wrap(text, width) or [""]
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" ,.;") + "…"
    return lines


def tspans(lines, x, y, lh, anchor="middle", **attrs):
    extra = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    first = y - (len(lines) - 1) * lh / 2
    spans = "".join(f'<tspan x="{x}" y="{first + i * lh:.1f}">{E(l)}</tspan>' for i, l in enumerate(lines))
    return f'<text text-anchor="{anchor}" dominant-baseline="middle" {extra}>{spans}</text>'


def part_label(m):
    p = D.PARTS[m["part"]]
    return f"{p[0]} · {p[1]}"


def chapter_text(m):
    return f"Caldwell, The Agentic AI Bible, {m['chapters']}"


# ───────────────────────── mind map ─────────────────────────
def mindmap_svg(m, n):
    W, H = 1280, 840
    cx, cy = 640, 440
    rows = [220, 440, 660]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">',
           f'<title>Module {n:02d} mind map: {E(m["title"])}</title>',
           '<rect width="100%" height="100%" fill="#fbfaf7"/>',
           f'<rect width="{W}" height="66" fill="{MAROON}"/>',
           f'<text x="32" y="40" fill="#fff" font-size="17" font-weight="700" letter-spacing="2">CSCI 391 · MODULE {n:02d} · MIND MAP</text>',
           f'<text x="{W-32}" y="40" fill="#f3c98b" font-size="15" text-anchor="end">{E(part_label(m))}</text>']
    edges, nodes = [], []
    for i, (branch, leaves) in enumerate(m["branches"][:6]):
        side = -1 if i % 2 == 0 else 1
        by = rows[i // 2]
        bx = 375 if side < 0 else 905
        lx = 130 if side < 0 else 1150
        col, tint = BRANCH_COLORS[i], TINTS[i]
        # center → branch
        x0 = cx + side * 125
        x1 = bx - side * 105
        edges.append(f'<path d="M{x0},{cy} C{(x0+x1)/2},{cy} {(x0+x1)/2},{by} {x1},{by}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" opacity=".85"/>')
        nodes.append(f'<rect x="{bx-105}" y="{by-31}" width="210" height="62" rx="31" fill="{col}"/>')
        nodes.append(tspans(wrap(branch, 20, 2), bx, by, 19, fill="#fff", font_size="16", font_weight="700"))
        k = len(leaves)
        for j, leaf in enumerate(leaves):
            ly = by + (j - (k - 1) / 2) * 56
            x2 = bx + side * 105
            x3 = lx - side * 110
            edges.append(f'<path d="M{x2},{by} C{(x2+x3)/2},{by} {(x2+x3)/2},{ly} {x3},{ly}" fill="none" stroke="{col}" stroke-width="2" opacity=".6"/>')
            nodes.append(f'<rect x="{lx-110}" y="{ly-23}" width="220" height="46" rx="10" fill="{tint}" stroke="{col}" stroke-width="1.5"/>')
            nodes.append(tspans(wrap(leaf, 29, 2), lx, ly, 16, fill=INK, font_size="13.5"))
    out += edges + nodes
    out.append(f'<rect x="{cx-125}" y="{cy-75}" width="250" height="150" rx="22" fill="#fff" stroke="{MAROON}" stroke-width="5"/>')
    out.append(f'<text x="{cx}" y="{cy-46}" text-anchor="middle" fill="{COPPER}" font-size="13" font-weight="700" letter-spacing="1.5">MODULE {n:02d}</text>')
    out.append(tspans(wrap(m["title"], 19, 4), cx, cy + 8, 25, fill=MAROON, font_size="21", font_weight="800"))
    out.append(f'<line x1="32" y1="{H-50}" x2="{W-32}" y2="{H-50}" stroke="#ddd"/>')
    out.append(f'<text x="32" y="{H-24}" fill="#666" font-size="13">Concepts after {E(chapter_text(m))} · Lecture synthesis and enterprise lens by {E(D.COURSE["author"])}</text>')
    out.append("</svg>")
    return "\n".join(out)


# ───────────────────────── one-pager ─────────────────────────
# ───────────────────────── HTML ─────────────────────────
ICON = {
    "video": '<path d="M4 6h11v12H4zM15 10l5-3v10l-5-3z"/>',
    "reading": '<path d="M4 5c3-1 6-1 8 1 2-2 5-2 8-1v13c-3-1-6-1-8 1-2-2-5-2-8-1zM12 6v13"/>',
    "map": '<circle cx="12" cy="12" r="3"/><circle cx="4.5" cy="6" r="2"/><circle cx="19.5" cy="6" r="2"/><circle cx="4.5" cy="18" r="2"/><circle cx="19.5" cy="18" r="2"/><path d="M9.5 10.5 6 7M14.5 10.5 18 7M9.5 13.5 6 17M14.5 13.5 18 17"/>',
    "page": '<path d="M6 3h8l4 4v14H6zM14 3v4h4M9 12h6M9 16h6"/>',
    "lab": '<path d="M9 3h6M10 3v6l-5 10a1.5 1.5 0 0 0 1.4 2h11.2a1.5 1.5 0 0 0 1.4-2L14 9V3"/>',
    "quiz": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="m8.5 13 2.5 2.5L15.5 11"/>',
    "project": '<path d="M3 9.5 12 5l9 4.5-9 4.5zM7 11.5v4.5c2.8 2 7.2 2 10 0v-4.5"/>',
    "code": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>',
    "practice": '<circle cx="12" cy="12" r="9"/><path d="M9.6 9.3a2.5 2.5 0 1 1 3.3 2.4c-.6.3-.9.8-.9 1.4v.6M12 16.8v.2"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4.5 4.2-6.5 8-6.5s7 2 8 6.5"/>',
    "book": '<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3zM5 17a3 3 0 0 1 3-3h11"/>',
    "script": '<path d="M6 3h9l3 3v15H6zM9 9h6M9 12.5h6M9 16h4"/>',
}


def icon(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICON[name]}</svg>'


def counts(m):
    c = {"video": 1 if video_for(m) else 0, "reading": 1 + len(D.SUPPLEMENTAL.get(m["id"], [])), "lab": 0, "quiz": 0, "project": 0}
    for a in m["activities"]:
        if a["kind"] in c:
            c[a["kind"]] += 1
    if m["id"] in CHECKS:
        c["practice"] = 1
    names = {"video": "video", "reading": "reading", "lab": "lab", "quiz": "graded quiz", "project": "project milestone", "practice": "practice quiz"}
    parts = [f'{v} {names[k]}{"s" if v != 1 else ""}' if not k.endswith("quiz") and k != "practice" else f'{v} {names[k][:-4]}quiz{"zes" if v != 1 else ""}' for k, v in c.items() if v]
    return parts


def chapter_titles(m):
    import re
    nums = [int(x) for x in re.findall(r"\d+", m["chapters"])]
    if len(nums) == 2:
        nums = list(range(nums[0], nums[1] + 1))
    return [(k, D.CHAPTERS[k - 1]) for k in nums]


def board_files(m):
    """(preview image, link) for the module's map: the finished explainer board as a PDF when it exists."""
    if os.path.exists(os.path.join(IMG, f"{m['id']}-board.pdf")):
        return f"curriculum/img/{m['id']}-board.jpg", f"curriculum/img/{m['id']}-board.pdf"
    return (f"curriculum/img/{m['id']}-mindmap.svg",) * 2


# Hero tiles: flat illustrations drawn from the explainer's own icon set, plus the two project covers.
TILES = [  # (slot, art, background, glow, link, label)
    ("a", "brain", "#2f6f8f", "#cfe6ef", "#m06", "Module 6 · LLMs as reasoning engines"),
    ("b", "cover:encore", None, None, "#projects", "Encore · the midterm project"),
    ("c", "cover:ensemble", None, None, "#projects", "Encore Ensemble · the capstone"),
    ("d", "toolbox", "#70002e", "#f3c98b", "#m05", "Module 5 · tools as contracts"),
    ("e", "hierarchy", "#3f7a55", "#d9ecdf", "#m10", "Module 10 · multi-agent systems"),
    ("f", "shield", "#5a4787", "#e4def3", "#m14", "Module 14 · security and alignment"),
]
COVER = {"encore": "curriculum/img/encore-cover.webp", "ensemble": "curriculum/img/encore-ensemble-cover.webp"}


def tile_svgs():
    """Write curriculum/img/tiles/<icon>.svg: one big hand-drawn icon on a flat color, with a few sparkles."""
    try:
        import explainer_modules as XM
    except ImportError:
        return
    os.makedirs(os.path.join(IMG, "tiles"), exist_ok=True)
    for _, art, bg, glow, _, _ in TILES:
        if art.startswith("cover:"):
            continue
        dots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{glow}" opacity=".55"/>'
                       for x, y, r in [(-230, -150, 7), (210, -170, 5), (250, 120, 8), (-260, 140, 5), (150, 200, 4), (-160, -210, 4)])
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-200 -200 400 400" preserveAspectRatio="xMidYMid slice">'
               f'<rect x="-2000" y="-2000" width="4000" height="4000" fill="{bg}"/>{dots}'
               f'<circle cx="0" cy="0" r="150" fill="{glow}" opacity=".9"/>'
               f'<g transform="scale(1.05)">{XM.ICONS[art](0, 0, 1)}</g></svg>')
        with open(os.path.join(IMG, "tiles", art + ".svg"), "w", encoding="utf8") as f:
            f.write(svg)


def mosaic_html(guide):
    tiles = []
    for slot, art, _, _, href, lbl in TILES:
        img = COVER[art[6:]] if art.startswith("cover:") else f"curriculum/img/tiles/{art}.svg"
        tiles.append(f'<a class="tile t-{slot}" href="{href}" title="{E(lbl)}" aria-label="{E(lbl)}"><img src="{img}" alt="" loading="eager"></a>')
    return "\n    ".join(tiles)


def contents_html():
    """Sticky table of contents. Modules is a collapsible group; each part inside it collapses too."""
    out = ['<nav class="contents" aria-label="Contents"><h2>Contents</h2>', '<a href="#intro">Introduction</a>',
           '<a href="#about">What you\'ll learn</a>',
           '<details class="lvl" open><summary>Modules</summary>', '<a class="sub" href="#modules">Overview</a>']
    current = None
    for n, m in enumerate(D.MODULES, 1):
        if m["part"] != current:
            if current:
                out.append("</details>")
            current = m["part"]
            out.append(f'<details class="grp"><summary>{E(D.PARTS[current][0])} · {E(D.PARTS[current][1])}</summary>')
        out.append(f'<a class="sub" href="#{m["id"]}"><span>{n:02d}</span>{E(m["title"])}</a>')
    out += ["</details>", "</details>", '<a href="#projects">Projects</a>', '<a href="#textbook">Textbook</a>', '<a href="#author">Author</a>',
            '<a href="#adopt">Adopt this course</a>', '<a href="#faq">FAQ</a>', "</nav>"]
    return "\n".join(out)


def duration(vid):
    """Running time from the last caption cue, e.g. '3 min'."""
    try:
        h, mi, sec = re.findall(r"--> (\d+):(\d+):(\d+(?:\.\d+)?)", open(os.path.join(HERE, "video", vid + ".vtt"), encoding="utf8").read())[-1]
    except (OSError, IndexError):
        return ""
    return f"{max(1, round((int(h) * 3600 + int(mi) * 60 + float(sec)) / 60))} min"


def thumb(kind, img=None, play=False):
    inner = f'<img src="{E(img)}" alt="" loading="lazy">' if img else icon(kind if kind in ICON else "page")
    return f'<span class="th k-{kind}">{inner}{"<i class=play></i>" if play else ""}</span>'


def text(meta, title, sub=""):
    return (f'<span class="tx"><span class="meta">{E(meta)}</span><span class="ttl">{E(title)}</span>'
            + (f'<span class="sub">{E(sub)}</span>' if sub else "") + "</span>")


def row(kind, meta, title, sub="", href=None, img=None):
    if not href:
        return f'<div class="row">{thumb(kind, img)}{text(meta, title, sub)}</div>'
    ext = href.startswith("http") or href.endswith(".pdf")
    return (f'<a class="row" href="{E(href)}"{" target=_blank rel=noopener" if ext else ""}>{thumb(kind, img)}{text(meta, title, sub)}'
            f'<span class="go">{"Open" if not href.startswith("#") else "Go"}</span></a>')


def fold(kind, meta, title, sub, body, img=None, play=False, open_=False, rid=None):
    return (f'<details class="row"{f" id={rid}" if rid else ""}{" open" if open_ else ""}><summary>{thumb(kind, img, play)}{text(meta, title, sub)}'
            f'{icon("chev", "chev")}</summary><div class="body">{body}</div></details>')


def script_html(lec):
    """The track's narration as readable text, with what appears on screen in each scene."""
    out = []
    for i, sc in enumerate(lec["scenes"], 1):
        t = sc["type"]
        kick = sc.get("kicker") or {"title": "Opening", "image": "Closing"}.get(t, "")
        head = sc.get("heading") or ""
        screen = ""
        if t == "quote":
            screen = f'<div class="screen"><b>On screen</b><br><q>{E(sc["quote"])}</q></div>'
        elif t == "bullets":
            screen = '<div class="screen"><b>On screen</b><ul>' + "".join(f"<li>{E(x)}</li>" for x in sc["bullets"]) + "</ul></div>"
        elif t == "image":
            screen = '<div class="screen"><b>On screen</b><br>The finished board — the module map.</div>'
        lines = "".join(f"<p>{E(x)}</p>" for x in sc["lines"])
        out.append(f'<div class="scene"><span class="sk">Scene {i} · {E(kick)}</span>{f"<h5>{E(head)}</h5>" if head else ""}{screen}{lines}</div>')
    return f'<div class="script">{"".join(out)}</div>'


def track_block(lec, series, guide, pid=None):
    """One track: a video row on the site, a script row in the guide."""
    vid, d = lec["id"], duration(lec["id"])
    if guide:
        n = sum(len(sc["lines"]) for sc in lec["scenes"])
        return fold("script", f"Script · {d} track · {lec['track']}", lec["name"], f"{len(lec['scenes'])} scenes · {n} narration lines",
                    script_html(lec), open_=True, rid=f"{pid or vid}-script")
    return fold("video", f"Video · {d} · {lec['track']}", lec["name"], "Narrated by Encore · captions on · choose a voice",
                player_for(lec, series, pid), img=f"curriculum/video/{vid}.jpg", play=True)


def player(m):
    lec = video_for(m)
    return player_for(lec, "Encore Lectures") if lec else ""


def player_for(lec, series, pid=None):
    vid = lec["id"]
    v = f"curriculum/video/{vid}"
    voices = [x for x in getattr(VS, "VOICES", []) if os.path.exists(os.path.join(HERE, "video", VS.media_stem(vid, x) + ".mp4"))]
    picker = ""
    if len(voices) > 1:
        btns = "".join(
            f'<button type="button" data-voice="{x["id"]}" data-stem="curriculum/video/{VS.media_stem(vid, x)}" aria-pressed="{"true" if i == 0 else "false"}">{E(x["name"])}</button>'
            for i, x in enumerate(voices))
        picker = f'<span class="voices" role="group" aria-label="Narrator voice"><span>Voice</span>{btns}</span>'
    return f'''<figure class="player" id="{pid or vid}-video">
      <video controls preload="none" poster="{v}.jpg" playsinline>
        <source src="{v}.mp4" type="video/mp4">
        <track kind="captions" src="{v}.vtt" srclang="en" label="English" default>
      </video>
      <figcaption><span class="trk">{E(series)} · {E(lec['track'])}</span><b>{E(lec['name'])}</b>{picker}<span class="note">Synthetic narrator · captions on by default</span></figcaption>
    </figure>'''


def check_html(m, n):
    qs = CHECKS.get(m["id"])
    if not qs:
        return ""
    graded = [a["title"].split(" — ")[0] for a in m["activities"] if a["kind"] == "quiz"]
    note = f" Graded in class: {E(graded[0])}." if graded else ""
    need = max(1, round(len(qs) * 2 / 3))
    out = []
    for qi, q in enumerate(qs):
        opts = "".join(
            f'<label class="opt" data-why="{E(why)}"><input type="radio" name="{m["id"]}-q{qi}" value="{oi}"><span>{E(text)}</span></label>'
            for oi, (text, why) in enumerate(q["options"]))
        out.append(f'<li class="q" data-answer="{q["answer"]}"><p class="stem">{E(q["q"])}</p>'
                   f'<div class="opts" role="radiogroup" aria-label="Question {qi + 1}">{opts}</div><p class="fb" hidden></p></li>')
    return f'''<section class="check" id="{m['id']}-check" data-mod="{m['id']}" data-pass="{need}">
      <div class="check-head">{icon('practice')}<div><span class="kicker">Check your progress · Practice quiz</span>
        <h4>Module {n}: {E(m['title'])}</h4>
        <p>{len(qs)} questions · ungraded · instant feedback · pass with {need} of {len(qs)}.{note}</p></div>
        <span class="best" hidden></span></div>
      <ol class="qs">{''.join(out)}</ol>
      <div class="check-foot"><button type="button" class="btn primary submit" disabled>Submit answers</button>
        <button type="button" class="btn ghost retry" hidden>Try again</button><span class="score" aria-live="polite"></span></div>
    </section>'''


TAILOR = ("Use these as a starting point, not as the quiz. Each semester you teach, write tailored questions in your own quiz style — "
          "your format (multiple choice, short answer, scenario, code reading), your examples from that term's discussions and labs, "
          "and fresh scenarios and distractors — so the quiz fits your teaching and old answers don't carry over between terms.")


def graded_html(gq):
    out = []
    for q in gq["questions"]:
        tag = "Extra credit · " if q.get("extra") else ("Fill in the blanks · " if q.get("blank") else "")
        body = f'<p class="stem">{E(tag)}{E(q["q"])}</p>'
        if q.get("img"):  # inlined, so the figure only exists inside the encrypted guide
            import base64
            with open(os.path.join(PRIVATE, q["img"]), "rb") as f:
                uri = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")
            body += f'<div class="qimg"><img src="{uri}" alt="Figure for this question"></div>'
        if q.get("items"):
            body += "<ul>" + "".join(f"<li>{E(x)}</li>" for x in q["items"]) + "</ul>"
        if q.get("options"):
            body += '<ol type="A">' + "".join(f"<li>{E(o)}</li>" for o in q["options"]) + "</ol>"
        out.append(f"<li>{body}</li>")
    return (f'<div class="tailor"><b>Give it in class, unannounced — then retire it.</b> These are the pilot’s questions, shown without answers. '
            f'Write a fresh quiz in your own style each semester; this one shows the level and coverage to aim for.</div><ol class="bank graded">{"".join(out)}</ol>')


def bank_html(m):
    out = []
    for q in CHECKS[m["id"]]:
        opts = "".join(f'<li class="{"key" if i == q["answer"] else ""}">{E(t)}<span>{E(why)}</span></li>' for i, (t, why) in enumerate(q["options"]))
        out.append(f'<li><p class="stem">{E(q["q"])}</p><ol type="A">{opts}</ol></li>')
    graded = [a["title"] for a in m["activities"] if a["kind"] == "quiz"]
    g = f" This week's graded quiz: {E(graded[0])} — give it in class, unannounced." if graded else ""
    return f'<div class="tailor"><b>Write your own each semester.</b> {E(TAILOR)}{g}</div><ol class="bank">{"".join(out)}</ol>'


def module_html(m, n, guide, shown):
    """Track, reading, quiz and application (when one is assigned that week). The guide adds teaching notes."""
    sec = []
    lec = video_for(m)
    track = []
    mm_img, mm = board_files(m)
    if guide:
        track.append(f'<figure class="mapfig"><a href="{mm}" target="_blank" rel="noopener"><img src="{mm_img}" alt="Module {n} map: the finished illustrated board from the track, {E(m["title"])}" loading="lazy"></a>'
                     f'<figcaption>Module map · the board the track draws, scene by scene · <a href="{mm}" target="_blank" rel="noopener">printable PDF</a></figcaption></figure>')
    if lec:
        track.append(track_block(lec, "Encore Lectures", guide))
    if not guide:
        track.append(row("map", "PDF · Module map", "The finished board from the track", "Print it, annotate it, review with it", mm, mm_img))
    sec.append(("Track", track))

    reading = [row("reading", f"Required reading · Caldwell, Chapter {k}", t, D.COURSE["book"]["title"], "#textbook") for k, t in chapter_titles(m)]
    reading += [row("reading", "Supplemental reading", t, "", u) for t, u in D.SUPPLEMENTAL.get(m["id"], [])]
    if guide:
        outline = "".join(f"<li><b>{E(h)}</b><ul>{''.join(f'<li>{E(x)}</li>' for x in leaves)}</ul></li>" for h, leaves in m["branches"])
        reading.append(f'''<div class="outline"><h5>Reading outline · {E(m['chapters'])}</h5>
      <p class="big">{E(m['big_idea'])}</p><ol>{outline}</ol>
      <p class="src">{E(m['textbook'])} Outline written for this course; assign the chapter itself.</p></div>''')
    sec.append(("Reading", reading))

    quiz = []
    if m["id"] in CHECKS:
        k = len(CHECKS[m["id"]])
        if guide:
            quiz.append(fold("practice", f"Question bank · {k} questions · answer key", "Quiz questions for this module",
                             "Starting points — write your own each semester", bank_html(m), open_=True, rid=f"{m['id']}-bank"))
        else:
            quiz.append(fold("practice", f"Practice quiz · {k} questions · ungraded", "Check your progress", "Instant feedback · best score saved in this browser",
                             check_html(m, n)))
    for a in m["activities"]:
        if a["kind"] == "quiz":
            gq = GRADED.get(m["id"]) if guide else None
            if gq:
                quiz.append(fold("quiz", f"Graded quiz · {len(gq['questions'])} questions · questions only, no key", gq["title"],
                                 "As given in the pilot · keep your answer key private", graded_html(gq), open_=True, rid=f"{m['id']}-graded"))
            else:
                quiz.append(row("quiz", "Graded quiz · in class, unannounced", a["title"], a["desc"]))
    if quiz:
        sec.append(("Quiz", quiz))

    app = []
    for a in m["activities"]:
        if a["kind"] == "quiz":
            continue
        label = {"lab": "Lab", "project": "Project", "code": "Code example"}[a["kind"]]
        app.append(row(a["kind"], label, a["title"], a["desc"], a.get("href")))
        t = track_video(TRACK_FOR.get(a.get("href"), ""))
        if t and t["id"] not in shown:
            shown.add(t["id"])
            app.append(track_block(t, "Lab walkthrough" if a["kind"] == "lab" else "Project walkthrough", guide))
    if app:
        sec.append(("Application", app))

    if guide:
        obj = "".join(f"<li>{icon('check')}<span>{E(o)}</span></li>" for o in m["objectives"])
        fname, fitems = m["framework"]
        sec.append(("Teaching notes", [f'''<div class="notes">
      <div><h4>Learning objectives</h4><ul class="checks">{obj}</ul>
        <h4>Key framework · {E(fname)}</h4><ol class="framework">{"".join(f"<li>{E(x)}</li>" for x in fitems)}</ol>
        <h4>Discussion prompts</h4><ul class="prompts">{"".join(f"<li>{E(p)}</li>" for p in m["prompts"])}</ul></div>
      <div><div class="case"><h4>Opening case</h4><p>{E(m['case'])}</p></div>
        <div class="callout book">{icon('book')}<div><h4>Textbook foundation</h4><p>{E(m['textbook'])}</p></div></div>
        <div class="callout lens"><div><h4>Enterprise lens · {E(D.COURSE['author'])}</h4><ul>{"".join(f"<li>{E(b)}</li>" for b in m["lens"])}</ul></div></div></div>
    </div>''']))

    panel = "".join(f'<h4>{E(h)}</h4><div class="rows">{"".join(r)}</div>' for h, r in sec)
    return f'''
<article class="module" id="{m['id']}">
  <span class="eyebrow">Module {n} · {E(m['weeks'])} · Reading {E(m['chapters'])}</span><span class="done" data-done="{m['id']}" hidden>{icon('check')} Check passed</span>
  <h3>{E(m['title'])}</h3>
  <p class="mod-tag">{E(m['tagline'])}</p>
  <p class="mod-summary">{E(m['summary'])}</p>
  <div class="panel">{panel}</div>
</article>'''


SITE_INTRO = ("Fourteen modules on building AI agents that act — and on keeping them reliable, observable, and safe. "
              "Every module works the same way: watch the track, do the reading, check yourself with a quiz, then apply it in that week's lab or project.")
SITE_MODS = ("Each module has a track (an illustrated, narrated video lecture, plus its finished board as a printable module map), "
             "the required reading, a quiz, and the application: the lab or project assigned that week, if there is one.")
GUIDE_INTRO = ("The whole course, arranged for teaching. In place of the videos, each module shows its module map and the full narration "
               "script of its track, scene by scene, followed by the reading, quizzes, assignments, and teaching notes.")
GUIDE_MODS = ("Each module: the module map and the track script, the required reading with an outline, a quiz question bank with its answer key, "
              "the lab or project assigned that week with its walkthrough script, and teaching notes (objectives, key framework, opening case, "
              "textbook foundation, enterprise lens, discussion prompts). Quiz questions are starting points: write tailored ones each semester.")


def page(guide=False):
    C, B = D.COURSE, D.COURSE["book"]
    mods, current, shown = [], None, set()
    for n, m in enumerate(D.MODULES, 1):
        if m["part"] != current:
            current = m["part"]
            p = D.PARTS[current]
            mods.append(f'<div class="part"><span>{E(p[0])}</span><h3>{E(p[1])}</h3><p>{E(p[2])}</p></div>')
        mods.append(module_html(m, n, guide, shown))
    n_labs = sum(1 for m in D.MODULES for a in m["activities"] if a["kind"] == "lab")
    n_quiz = sum(1 for m in D.MODULES for a in m["activities"] if a["kind"] == "quiz")
    outcomes = "".join(f"<li>{icon('check')}<span>{E(o)}</span></li>" for o in D.OUTCOMES)
    skills = "".join(f"<span class='chip'>{E(s)}</span>" for s in D.SKILLS)
    chap_rows = []
    for k, t in enumerate(D.CHAPTERS, 1):
        owner = next((n for n, m in enumerate(D.MODULES, 1) if k in [c for c, _ in chapter_titles(m)]), None)
        mod = D.MODULES[owner - 1] if owner else None
        link = f'<a href="#{mod["id"]}">Module {owner} · {E(mod["title"])}</a>' if mod else "—"
        chap_rows.append(f"<tr><td>{k}</td><td>{E(t)}</td><td>{link}</td></tr>")
    grading = "".join(f'<div class="grade"><b>{w}%</b><span>{E(name)}</span><i style="width:{w*2.6}%"></i></div>' for name, w in D.GRADING)
    tech = "".join(f"<span class='chip ghost'>{E(t)}</span>" for t in D.TECH)
    faq = "".join(f"<details class='faq'><summary>{E(q)}{icon('chev','chev')}</summary><p>{E(a)}</p></details>" for q, a in D.FAQ)
    out = string.Template(TEMPLATE).substitute(
        title=E(C["title"]), code=E(C["code"]), subtitle=E(C["subtitle"]), author=E(C["author"]),
        book_title=E(B["title"]), book_sub=E(B["subtitle"]), book_author=E(B["author"]), book_ed=E(B["edition"]), book_url=E(B["url"]),
        pilot=E(C["pilot"]), credits=C["credits"], length=E(C["length"]), level=E(C["level"]), prereq=E(C["prereq"]),
        repo=E(C["repo"]), syllabus=E(C["syllabus"]),
        n_vid=sum(1 for m in D.MODULES if video_for(m)) + sum(1 for l in LECTURE.values() if l.get("for") and track_video(l["id"])), n_check=sum(1 for m in D.MODULES if m["id"] in CHECKS), n_mod=len(D.MODULES), n_labs=n_labs, n_quiz=n_quiz, n_ch=len(D.CHAPTERS),
        outcomes=outcomes, skills=skills, modules="\n".join(mods), chapters="".join(chap_rows),
        grading=grading, tech=tech, faq=faq, mosaic=mosaic_html(guide), contents=contents_html(),
        encore_video=track_block(track_video("encore"), "Project walkthrough", guide, "encore-proj") if track_video("encore") else "",
        ensemble_video=track_block(track_video("ensemble"), "Project walkthrough", guide, "ensemble-proj") if track_video("ensemble") else "",
        kind="Instructor's guide" if guide else "Agentic AI Curriculum",
        label="Instructor's guide" if guide else "Course collection",
        switch='<a href="index.html">Student site</a>' if guide else '<a href="instructor-guide.html">Instructor\'s guide</a>',
        cta2='<a class="btn ghost" href="index.html">Open the student site</a>' if guide else '<a class="btn ghost" href="instructor-guide.html">Instructor\'s guide</a>',
        intro=E(GUIDE_INTRO if guide else SITE_INTRO), mod_intro=E(GUIDE_MODS if guide else SITE_MODS),
    )
    for k, v in {"$ICON_PERSON": icon("person"), "$ICON_BOOK": icon("book"), "$ICON_CHEV": icon("chev", "chev")}.items():
        out = out.replace(k, v)
    return out


TEMPLATE = open(os.path.join(HERE, "template.html"), encoding="utf8").read()



def main():
    tile_svgs()
    for n, m in enumerate(D.MODULES, 1):
        with open(os.path.join(IMG, f"{m['id']}-mindmap.svg"), "w", encoding="utf8") as f:
            f.write(mindmap_svg(m, n))
    import guide_lock
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf8", newline="\n") as f:
        f.write(page(False))
    # the guide holds quiz questions and answer keys: publish it encrypted, never as plaintext
    with open(os.path.join(ROOT, "instructor-guide.html"), "w", encoding="utf8", newline="\n") as f:
        f.write(guide_lock.locked_page(page(True), f"{D.COURSE['code']} · Instructor's guide"))
    print(f"Built index.html, instructor-guide.html and {len(D.MODULES)} fallback maps in {IMG}")


if __name__ == "__main__":
    main()
