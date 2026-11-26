"""Build the CSCI 391 curriculum site.

    python curriculum/build_site.py

Reads curriculum/course_data.py and writes:
  * index.html                          (repo root, Coursera-style course page)
  * curriculum/img/<id>-mindmap.svg     (radial mind map; fallback when no explainer board exists)
  * curriculum/img/<id>-board.pdf/.jpg   (the illustrated board from the video = the module mind map; made by build_explainer.py)
  * curriculum/img/<id>-onepager.svg    (one-page lecture guide per module)
Optional inputs: video_scripts.py (Encore lectures) and checks.py (practice quizzes).
"""
import html
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

try:
    import checks as CK  # noqa: E402
    CHECKS = CK.CHECKS
except ImportError:
    CHECKS = {}


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
def onepager_svg(m, n):
    W, PAD = 850, 40
    inner = W - 2 * PAD
    body = []
    y = 0
    # header
    title_lines = wrap(m["title"], 46, 2)
    tag_lines = wrap(m["tagline"], 92, 2)
    hh = 70 + len(title_lines) * 36 + len(tag_lines) * 21 + 20
    body.append(f'<rect width="{W}" height="{hh}" fill="{MAROON}"/>')
    body.append(f'<text x="{PAD}" y="42" fill="{COPPER}" font-size="13" font-weight="700" letter-spacing="2">CSCI 391 · MODULE {n:02d} · ONE-PAGE LECTURE GUIDE</text>')
    ty = 82
    for l in title_lines:
        body.append(f'<text x="{PAD}" y="{ty}" fill="#fff" font-size="30" font-weight="800">{E(l)}</text>')
        ty += 36
    ty += 2
    for l in tag_lines:
        body.append(f'<text x="{PAD}" y="{ty}" fill="#f1dbe4" font-size="16" font-style="italic">{E(l)}</text>')
        ty += 21
    y = hh + 30
    body.append(f'<text x="{PAD}" y="{y}" fill="#555" font-size="13"><tspan font-weight="700" fill="{MAROON}">{E(part_label(m))}</tspan>   ·   {E(m["weeks"])}   ·   Read: {E(chapter_text(m))}</text>')
    y += 26

    def heading(label, color=MAROON):
        nonlocal y
        body.append(f'<text x="{PAD}" y="{y}" fill="{color}" font-size="13" font-weight="800" letter-spacing="1.8">{E(label.upper())}</text>')
        y += 20

    # opening case
    lines = wrap(m["case"], 118)
    bh = 44 + len(lines) * 20
    body.append(f'<rect x="{PAD}" y="{y}" width="{inner}" height="{bh}" rx="10" fill="{CREAM}"/>')
    body.append(f'<text x="{PAD+20}" y="{y+28}" fill="{MAROON}" font-size="13" font-weight="800" letter-spacing="1.8">OPENING CASE</text>')
    for i, l in enumerate(lines):
        body.append(f'<text x="{PAD+20}" y="{y+52+i*20}" fill="{INK}" font-size="14">{E(l)}</text>')
    y += bh + 30
    # big idea
    lines = wrap(m["big_idea"], 76)
    body.append(f'<rect x="{PAD}" y="{y-6}" width="6" height="{len(lines)*27+8}" fill="{COPPER}"/>')
    for i, l in enumerate(lines):
        body.append(f'<text x="{PAD+22}" y="{y+16+i*27}" fill="{MAROON}" font-size="20" font-weight="700">{E(l)}</text>')
    y += len(lines) * 27 + 34
    # two columns
    colw = (inner - 30) / 2
    lx, rx = PAD, PAD + colw + 30
    fname, fitems = m["framework"]
    ly = ry = y
    body.append(f'<text x="{lx}" y="{ly}" fill="{MAROON}" font-size="13" font-weight="800" letter-spacing="1.8">KEY FRAMEWORK</text>')
    ly += 22
    for l in wrap(fname, 48):
        body.append(f'<text x="{lx}" y="{ly}" fill="{INK}" font-size="16" font-weight="700">{E(l)}</text>')
        ly += 21
    ly += 6
    for i, item in enumerate(fitems, 1):
        body.append(f'<circle cx="{lx+11}" cy="{ly+2}" r="11" fill="{BRANCH_COLORS[(i-1) % 6]}"/>')
        body.append(f'<text x="{lx+11}" y="{ly+7}" fill="#fff" font-size="12" font-weight="700" text-anchor="middle">{i}</text>')
        for l in wrap(item, 52):
            body.append(f'<text x="{lx+30}" y="{ly+7}" fill="{INK}" font-size="13.5">{E(l)}</text>')
            ly += 19
        ly += 9
    body.append(f'<text x="{rx}" y="{ry}" fill="{MAROON}" font-size="13" font-weight="800" letter-spacing="1.8">YOU SHOULD BE ABLE TO</text>')
    ry += 28
    for obj in m["objectives"]:
        body.append(f'<path d="M{rx+2},{ry} l5,5 l10,-11" fill="none" stroke="#3f7a55" stroke-width="3" stroke-linecap="round"/>')
        for l in wrap(obj, 52):
            body.append(f'<text x="{rx+26}" y="{ry+4}" fill="{INK}" font-size="13.5">{E(l)}</text>')
            ry += 19
        ry += 11
    y = max(ly, ry) + 16
    # enterprise lens
    lens_lines = [wrap(b, 114) for b in m["lens"]]
    bh = 50 + sum(len(ls) * 19 + 10 for ls in lens_lines)
    body.append(f'<rect x="{PAD}" y="{y}" width="{inner}" height="{bh}" rx="10" fill="#fff6e8" stroke="#f0c98a"/>')
    body.append(f'<rect x="{PAD}" y="{y}" width="7" height="{bh}" rx="3" fill="{COPPER}"/>')
    body.append(f'<text x="{PAD+22}" y="{y+28}" fill="#9a5a00" font-size="13" font-weight="800" letter-spacing="1.8">ENTERPRISE LENS · {E(D.COURSE["author"].upper())}</text>')
    yy = y + 52
    for ls in lens_lines:
        body.append(f'<circle cx="{PAD+28}" cy="{yy-4}" r="3.5" fill="{COPPER}"/>')
        for l in ls:
            body.append(f'<text x="{PAD+40}" y="{yy}" fill="{INK}" font-size="13.5">{E(l)}</text>')
            yy += 19
        yy += 10
    y += bh + 30
    # prompts
    heading("Discuss")
    for p in m["prompts"]:
        for i, l in enumerate(wrap(p, 116)):
            body.append(f'<text x="{PAD}" y="{y}" fill="{INK}" font-size="14">{"→  " if i == 0 else "    "}{E(l)}</text>')
            y += 20
        y += 6
    y += 14
    H = y + 50
    body.append(f'<line x1="{PAD}" y1="{H-46}" x2="{W-PAD}" y2="{H-46}" stroke="#ddd"/>')
    body.append(f'<text x="{PAD}" y="{H-22}" fill="#777" font-size="11.5">Concepts after {E(chapter_text(m))}. Case framing, synthesis, and enterprise lens: {E(D.COURSE["author"])}.</text>')
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">',
            f'<title>Module {n:02d} one-page guide: {E(m["title"])}</title>',
            '<rect width="100%" height="100%" fill="#fff"/>']
    return "\n".join(head + body + ["</svg>"])


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


def collage_html():
    """Wall of video posters at the top of the page; each tile jumps to (and opens) its module's lecture."""
    tiles = []
    for m in D.MODULES:
        lec = video_for(m)
        if not lec or not os.path.exists(os.path.join(HERE, "video", f"{m['id']}.jpg")):
            continue
        tiles.append(f'<a class="tile" href="#{m["id"]}-video"><span class="thumb"><img src="curriculum/video/{m["id"]}.jpg" alt="" loading="eager"></span>'
                     f'<span class="lbl">{E(lec["name"])}<small>{E(lec["track"])} · {E(m["title"])}</small></span></a>')
    if not tiles:
        return ""
    return f'<section class="collage" aria-label="Video lectures">{"".join(tiles)}</section>'


def player(m):
    lec = video_for(m)
    if not lec:
        return ""
    v = f"curriculum/video/{m['id']}"
    voices = [x for x in getattr(VS, "VOICES", []) if os.path.exists(os.path.join(HERE, "video", VS.media_stem(m["id"], x) + ".mp4"))]
    picker = ""
    if len(voices) > 1:
        btns = "".join(
            f'<button type="button" data-voice="{x["id"]}" data-stem="curriculum/video/{VS.media_stem(m["id"], x)}" aria-pressed="{"true" if i == 0 else "false"}">{E(x["name"])}</button>'
            for i, x in enumerate(voices))
        picker = f'<span class="voices" role="group" aria-label="Narrator voice"><span>Voice</span>{btns}</span>'
    return f'''<figure class="player" id="{m['id']}-video">
      <video controls preload="none" poster="{v}.jpg" playsinline>
        <source src="{v}.mp4" type="video/mp4">
        <track kind="captions" src="{v}.vtt" srclang="en" label="English" default>
      </video>
      <figcaption><span class="trk">Encore Lectures · {E(lec['track'])}</span><b>{E(lec['name'])}</b>{picker}<span class="note">Synthetic narrator · captions on by default</span></figcaption>
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


def module_html(m, n):
    items = []
    for k, t in chapter_titles(m):
        items.append(("reading", f"Reading · Caldwell, Chapter {k}", t, None))
    for t, u in D.SUPPLEMENTAL.get(m["id"], []):
        items.append(("reading", "Supplemental reading", t, u))
    items.append(("map", "Mind map", f"Module {n} board from the video · printable PDF", board_files(m)[1]))
    items.append(("page", "One-page lecture guide", "Printable lecture companion", f"curriculum/img/{m['id']}-onepager.svg"))
    lec = video_for(m)
    if lec:
        items.insert(0, ("video", f"Video lecture · Encore {lec['track']}", f"{lec['name']} — narrated by Encore, with captions", f"#{m['id']}-video"))
    if m["id"] in CHECKS:
        items.append(("practice", "Practice quiz · Check your progress", f"{len(CHECKS[m['id']])} questions · ungraded · instant feedback", f"#{m['id']}-check"))
    for a in m["activities"]:
        label = {"lab": "Lab", "quiz": "Graded quiz", "project": "Project", "code": "Code example"}[a["kind"]]
        items.append((a["kind"], label, f'{a["title"]} — {a["desc"]}', a.get("href")))
    li = []
    for kind, label, text, href in items:
        is_img = href and href.endswith(".svg")
        target = ' target="_blank" rel="noopener"' if href and (href.startswith("http") or href.endswith(".pdf")) else ""
        inner = f'{icon(kind)}<span><b>{E(label)}</b><span class="it-text">{E(text)}</span></span>'
        if href:
            attr = f' data-lightbox="{E(href)}" data-caption="{E(label + " · " + m["title"])}"' if is_img else ""
            li.append(f'<li><a class="item k-{kind}" href="{E(href)}"{target}{attr}>{inner}<span class="go">Open</span></a></li>')
        else:
            li.append(f'<li><div class="item k-{kind}">{inner}</div></li>')
    obj = "".join(f"<li>{icon('check')}<span>{E(o)}</span></li>" for o in m["objectives"])
    lens = "".join(f"<li>{E(b)}</li>" for b in m["lens"])
    prompts = "".join(f"<li>{E(p)}</li>" for p in m["prompts"])
    fname, fitems = m["framework"]
    fw = "".join(f"<li>{E(x)}</li>" for x in fitems)
    (mm_img, mm), op = board_files(m), f"curriculum/img/{m['id']}-onepager.svg"
    return f'''
<details class="module" id="{m['id']}">
  <summary>
    <div class="mod-num"><span>Module {n}</span><small>{E(m['weeks'])}</small></div>
    <div class="mod-head">
      <h3>{E(m['title'])}</h3>
      <p class="mod-tag">{E(m['tagline'])}</p>
      <p class="mod-meta">{E(' · '.join(counts(m)))} · Reading {E(m['chapters'])}<span class="done" data-done="{m['id']}" hidden>{icon('check')} Check passed</span></p>
    </div>
    {icon('chev', 'chev')}
  </summary>
  <div class="mod-body">
    <p class="mod-summary">{E(m['summary'])}</p>
    {player(m)}
    <div class="visuals">
      <a class="visual" href="{mm}"{' target="_blank" rel="noopener"' if mm.endswith(".pdf") else f' data-lightbox="{mm}" data-caption="Mind map · {E(m["title"])}"'}><img src="{mm_img}" alt="Mind map for module {n}: the whole illustrated board from the video, {E(m['title'])}" loading="lazy"><span>{icon('map')} Mind map{" · PDF" if mm.endswith(".pdf") else ""}</span></a>
      <a class="visual tall" href="{op}" data-lightbox="{op}" data-caption="One-page guide · {E(m['title'])}"><img src="{op}" alt="One-page lecture guide for module {n}" loading="lazy"><span>{icon('page')} One-page guide</span></a>
    </div>
    <div class="cols">
      <div>
        <h4>Learning objectives</h4>
        <ul class="checks">{obj}</ul>
        <h4>Key framework · {E(fname)}</h4>
        <ol class="framework">{fw}</ol>
      </div>
      <div>
        <div class="case"><h4>Opening case</h4><p>{E(m['case'])}</p></div>
        <div class="callout book">{icon('book')}<div><h4>Textbook foundation</h4><p>{E(m['textbook'])}</p></div></div>
        <div class="callout lens"><div><h4>Enterprise lens · {E(D.COURSE['author'])}</h4><ul>{lens}</ul></div></div>
      </div>
    </div>
    <h4>What's included</h4>
    <ul class="items">{''.join(li)}</ul>
    <h4>Discussion prompts</h4>
    <ul class="prompts">{prompts}</ul>
    {check_html(m, n)}
  </div>
</details>'''


def page():
    C, B = D.COURSE, D.COURSE["book"]
    mods, current = [], None
    for n, m in enumerate(D.MODULES, 1):
        if m["part"] != current:
            current = m["part"]
            p = D.PARTS[current]
            mods.append(f'<div class="part"><span>{E(p[0])}</span><h3>{E(p[1])}</h3><p>{E(p[2])}</p></div>')
        mods.append(module_html(m, n))
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
    toc = "".join(f'<a href="#{m["id"]}"><span>{n:02d}</span>{E(m["title"])}</a>' for n, m in enumerate(D.MODULES, 1))
    out = string.Template(TEMPLATE).substitute(
        title=E(C["title"]), code=E(C["code"]), subtitle=E(C["subtitle"]), author=E(C["author"]),
        book_title=E(B["title"]), book_sub=E(B["subtitle"]), book_author=E(B["author"]), book_ed=E(B["edition"]), book_url=E(B["url"]),
        pilot=E(C["pilot"]), credits=C["credits"], length=E(C["length"]), level=E(C["level"]), prereq=E(C["prereq"]),
        repo=E(C["repo"]), syllabus=E(C["syllabus"]),
        n_vid=sum(1 for m in D.MODULES if video_for(m)), n_check=sum(1 for m in D.MODULES if m["id"] in CHECKS), n_mod=len(D.MODULES), n_labs=n_labs, n_quiz=n_quiz, n_ch=len(D.CHAPTERS),
        outcomes=outcomes, skills=skills, modules="\n".join(mods), chapters="".join(chap_rows),
        grading=grading, tech=tech, faq=faq, toc=toc, collage=collage_html(),
        hero_img=board_files(D.MODULES[2])[0], hero_href=board_files(D.MODULES[2])[1],
    )
    for k, v in {"$ICON_PERSON": icon("person"), "$ICON_BOOK": icon("book"), "$ICON_CHEV": icon("chev", "chev")}.items():
        out = out.replace(k, v)
    return out


TEMPLATE = open(os.path.join(HERE, "template.html"), encoding="utf8").read()



def main():
    for n, m in enumerate(D.MODULES, 1):
        with open(os.path.join(IMG, f"{m['id']}-mindmap.svg"), "w", encoding="utf8") as f:
            f.write(mindmap_svg(m, n))
        with open(os.path.join(IMG, f"{m['id']}-onepager.svg"), "w", encoding="utf8") as f:
            f.write(onepager_svg(m, n))
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf8", newline="\n") as f:
        f.write(page())
    print(f"Built index.html and {2*len(D.MODULES)} images in {IMG}")


if __name__ == "__main__":
    main()
