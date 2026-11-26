"""index.html: the Aideation catalog. Every course as a card; each card opens a preview with its overview track,
and from there you enroll (choose a role, then sign in) or go straight to the course."""
import html
import os

import build_site as BS
import catalog as K
import course_data as D
import shell as SH

E = lambda s: html.escape(str(s), quote=True)  # noqa: E731

# Old links pointed into the course page at the site root (index.html#m03). They now live on the course page.
LEGACY = r"^#(intro|start|about|modules|projects|textbook|author|adopt|faq|m\d\d.*|lab\d.*|encore.*|ensemble.*|overview.*)$"

CSS = r"""
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:84px}
body{margin:0;font-family:Inter,'Segoe UI',system-ui,Arial,sans-serif;color:#1b2533;background:#fff;line-height:1.55;font-size:16px}
img{max-width:100%;display:block}
a{color:#1d4f9c}
h1,h2,h3{margin:0;line-height:1.15}
.w{max-width:1280px;margin:0 auto;padding:0 24px}
[hidden]{display:none!important}
section{padding:56px 0}
.kick{display:inline-block;font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#1d4f9c}
.sub{color:#566173;font-size:17px;max-width:720px;margin:10px 0 0}

/* hero */
.hero{position:relative;overflow:hidden;background:linear-gradient(180deg,#f2f7fd,#fff)}
.hero .w{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:40px;align-items:center;padding-top:56px;padding-bottom:56px}
.hero h1{font-size:clamp(34px,4.6vw,56px);font-weight:700;letter-spacing:-.02em;margin:12px 0 16px}
.hero h1 .g{background:var(--grad-warm);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{font-size:18.5px;color:#3b4658;max-width:560px;margin:0}
.ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.stats{display:flex;gap:28px;flex-wrap:wrap;margin-top:34px;padding-top:22px;border-top:1px solid #e1e7ef}
.stats b{display:block;font-family:Poppins,Inter,sans-serif;font-size:26px;color:#143a75}
.stats span{font-size:13.5px;color:#566173}
.art{position:relative;aspect-ratio:1/1;max-width:500px;justify-self:center;width:100%}
.art::before{content:"";position:absolute;inset:6%;border-radius:50%;background:conic-gradient(from 200deg,#1d4f9c33,#1fc3c433,#7cc24233,#ffd21f33,#ff8a1f33,#e0306a33,#1d4f9c33);filter:blur(30px)}
.art img.logo{position:absolute;inset:12%;width:76%;height:76%;object-fit:contain;mix-blend-mode:multiply}
.peek{position:absolute;left:-4%;bottom:8%;display:flex;gap:12px;align-items:center;background:#fff;border-radius:14px;padding:10px 14px 10px 10px;box-shadow:0 14px 40px rgba(13,27,51,.18);border:0;font:inherit;text-align:left;cursor:pointer;max-width:300px}
.peek img{width:92px;aspect-ratio:16/9;object-fit:cover;border-radius:8px}
.peek small{display:block;color:#566173;font-size:12px;font-weight:600}
.peek b{font-size:14.5px}
.peek:hover{box-shadow:0 18px 46px rgba(13,27,51,.25)}

/* course cards */
.head{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap}
.head h2{font-size:clamp(26px,3vw,34px)}
.count{color:#566173;font-size:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:22px;margin-top:26px}
.card{display:flex;flex-direction:column;text-align:left;background:#fff;border:1px solid #e1e7ef;border-radius:14px;overflow:hidden;padding:0;font:inherit;color:inherit;cursor:pointer;transition:box-shadow .2s,transform .2s}
.card:hover{box-shadow:0 16px 36px rgba(13,27,51,.14);transform:translateY(-2px)}
.card .cv{position:relative;aspect-ratio:16/9;background:#0d1b33}
.card .cv img{width:100%;height:100%;object-fit:cover}
.card .cv .play{position:absolute;right:12px;bottom:12px;background:rgba(255,255,255,.95);border-radius:999px;padding:5px 12px 5px 9px;font-size:12.5px;font-weight:700;display:flex;gap:6px;align-items:center;color:#143a75}
.card .cv .play::before{content:"";border-left:9px solid #1d4f9c;border-top:6px solid transparent;border-bottom:6px solid transparent}
.badges{position:absolute;left:12px;top:12px;display:flex;gap:6px}
.badges span{background:#fff;color:#143a75;font-size:11.5px;font-weight:800;border-radius:6px;padding:3px 8px;letter-spacing:.03em}
.badges span:nth-child(2){background:var(--grad-warm);color:#fff}
.card .bd{padding:16px 18px 18px;display:flex;flex-direction:column;gap:8px;flex:1}
.partner{display:flex;align-items:center;gap:8px;font-size:13px;color:#566173;font-weight:600}
.partner img{width:24px;height:24px;border:1px solid #e1e7ef;border-radius:6px;padding:1px}
.card h3{font-size:18.5px;line-height:1.3}
.card .sk{font-size:13.5px;color:#3b4658}
.card .sk b{color:#1b2533}
.card .mt{margin-top:auto;font-size:13px;color:#566173;padding-top:6px}
.card.soon{border-style:dashed;cursor:default;justify-content:center;align-items:center;text-align:center;padding:30px;background:#f8fafd;color:#566173}
.card.soon:hover{box-shadow:none;transform:none}
.card.soon b{display:block;font-family:Poppins,Inter,sans-serif;color:#143a75;font-size:18px;margin-bottom:4px}
.empty{margin-top:20px;color:#566173}

/* paths + steps */
.alt{background:#f5f8fc}
.paths{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:28px}
.path{background:#fff;border:1px solid #e1e7ef;border-radius:16px;padding:24px;display:flex;flex-direction:column;gap:10px;position:relative;overflow:hidden}
.path::before{content:"";position:absolute;left:0;right:0;top:0;height:5px}
.path:nth-child(1)::before{background:linear-gradient(90deg,#1d4f9c,#1e8fd6)}
.path:nth-child(2)::before{background:linear-gradient(90deg,#1fc3c4,#7cc242)}
.path:nth-child(3)::before{background:var(--grad-warm)}
.path h3{font-size:21px}
.path .who{color:#566173}
.path ul{margin:0;padding-left:20px;font-size:14.5px;flex:1}
.path li{margin:4px 0}
.path em{font-style:normal;font-size:12.5px;font-weight:700;color:#b8560b}
.path .abtn{align-self:flex-start;margin-top:6px}
.steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin-top:28px;counter-reset:s}
.step{border-radius:14px;padding:20px;background:#fff;border:1px solid #e1e7ef}
.step::before{counter-increment:s;content:counter(s);display:grid;place-items:center;width:34px;height:34px;border-radius:50%;color:#fff;font-weight:800;margin-bottom:10px;background:var(--grad-cool)}
.step:nth-child(even)::before{background:var(--grad-warm)}
.step b{display:block;font-size:17px;margin-bottom:4px}
.step span{color:#566173;font-size:14.5px}
.teach{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:36px;align-items:center}
.teach ul{padding-left:20px;margin:16px 0 22px}
.teach li{margin:6px 0}
.teach .panel{border-radius:18px;padding:26px;background:linear-gradient(150deg,#143a75,#1d4f9c 55%,#1e8fd6);color:#dde9f8}
.teach .panel b{color:#fff;font-family:Poppins,Inter,sans-serif;font-size:20px;display:block;margin-bottom:6px}
.teach .panel .abtn{margin-top:14px;background:#fff}

/* course preview */
dialog.cmodal{border:0;border-radius:18px;padding:0;width:min(1040px,calc(100vw - 24px));max-height:calc(100vh - 32px);box-shadow:0 30px 80px rgba(13,27,51,.35);color:#1b2533}
dialog.cmodal::backdrop{background:rgba(13,27,51,.6)}
.cm-top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;padding:20px 24px 14px;border-bottom:1px solid #e1e7ef;position:sticky;top:0;background:#fff;z-index:2}
.cm-top small{color:#566173;font-weight:600;font-size:13px}
.cm-top h2{font-size:24px;margin-top:2px}
.cm-x{border:0;background:#eef4fb;width:36px;height:36px;border-radius:50%;font-size:20px;cursor:pointer;color:#143a75;flex:none}
.cm-body{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:24px;padding:20px 24px 26px}
.player{margin:0}
.player video{width:100%;aspect-ratio:16/9;border-radius:12px;background:#0d1b33;display:block}
.player figcaption{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;margin-top:8px;font-size:13px;color:#566173}
.player figcaption b{color:#1b2533;font-size:14px}
.voices{display:inline-flex;gap:4px;align-items:center}
.voices button{border:1px solid #c9d4e2;background:#fff;border-radius:999px;padding:2px 10px;font:inherit;font-size:12.5px;cursor:pointer}
.voices button[aria-pressed=true]{background:#1d4f9c;color:#fff;border-color:#1d4f9c}
.player .note{display:none}
.facts{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.facts li{display:flex;gap:10px;align-items:baseline;font-size:14.5px}
.facts li b{min-width:92px;color:#566173;font-weight:600;font-size:13px}
.cm-ctas{display:grid;gap:10px;margin:18px 0}
.cm-ctas .abtn{width:100%}
.dlmap{display:flex;gap:12px;align-items:center;border:1px solid #e1e7ef;border-radius:12px;padding:10px;text-decoration:none;color:#1b2533}
.dlmap img{width:110px;border-radius:8px;border:1px solid #e1e7ef}
.dlmap small{display:block;color:#566173}
.dlmap:hover{border-color:#9fb6d6;background:#f5f8fc}
.cm-more{grid-column:1/-1;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;border-top:1px solid #e1e7ef;padding-top:18px}
.cm-more h3{font-size:17px;margin-bottom:8px}
.cm-more ul{margin:0;padding-left:20px;font-size:14.5px}
.cm-more li{margin:4px 0}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.chips span{background:#eef4fb;color:#143a75;border-radius:999px;padding:4px 11px;font-size:12.5px;font-weight:600}
.mods{columns:2;column-gap:28px;font-size:14px;padding-left:30px!important}.mods li{padding-left:2px;break-inside:avoid}

@media (max-width:900px){
  .hero .w,.teach{grid-template-columns:minmax(0,1fr)}
  .art{max-width:340px}
  .paths{grid-template-columns:minmax(0,1fr)}
  .steps{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .cm-body,.cm-more{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:560px){
  .w{padding:0 16px}
  section{padding:40px 0}
  .steps{grid-template-columns:minmax(0,1fr)}
  .peek{left:0;max-width:260px}
  .mods{columns:1}
  .stats{gap:18px}
}
"""

JS = r"""
(function () {
  // old course links (index.html#m03) now live on the course page
  if (new RegExp(LEGACY_RE).test(location.hash)) { location.replace('csci391.html' + location.hash); return; }
  function openCourse(id) {
    var d = document.getElementById('course-' + id);
    if (d && !d.open) d.showModal();
  }
  document.addEventListener('click', function (e) {
    var c = e.target.closest('[data-course-open]');
    if (c) { openCourse(c.dataset.courseOpen); return; }
    var x = e.target.closest('[data-cm-close]');
    if (x) x.closest('dialog').close();
  });
  Array.prototype.forEach.call(document.querySelectorAll('dialog.cmodal'), function (d) {
    d.addEventListener('click', function (e) { if (e.target === d) d.close(); });
    d.addEventListener('close', function () {
      var v = d.querySelector('video'); if (v) v.pause();
      if (location.hash === '#' + d.id) history.replaceState(null, '', location.pathname);
    });
    d.addEventListener('toggle', function () { if (d.open) history.replaceState(null, '', '#' + d.id); });
  });
  var m = location.hash.match(/^#course-([\w-]+)$/);
  if (m) openCourse(m[1]);

  // search filters the course cards
  var q = document.getElementById('asearch'), cards = document.querySelectorAll('.grid .card[data-text]');
  var empty = document.getElementById('empty'), count = document.getElementById('count');
  if (q) q.addEventListener('input', function () {
    var t = q.value.trim().toLowerCase(), n = 0;
    Array.prototype.forEach.call(cards, function (c) { var ok = !t || c.dataset.text.indexOf(t) >= 0; c.hidden = !ok; if (ok) n++; });
    empty.hidden = n > 0;
    count.textContent = n + (n === 1 ? ' course' : ' courses');
    if (t && document.getElementById('courses').getBoundingClientRect().top > 200) document.getElementById('courses').scrollIntoView();
  });

  // narrator voice
  var VKEY = 'csci391-voice';
  function setVoice(id) {
    Array.prototype.forEach.call(document.querySelectorAll('figure.player'), function (f) {
      var b = f.querySelector('.voices button[data-voice="' + id + '"]');
      if (!b || b.getAttribute('aria-pressed') === 'true') return;
      var v = f.querySelector('video'), stem = b.getAttribute('data-stem');
      f.querySelector('source').src = stem + '.mp4'; f.querySelector('track').src = stem + '.vtt'; v.load();
      Array.prototype.forEach.call(f.querySelectorAll('.voices button'), function (x) { x.setAttribute('aria-pressed', String(x === b)); });
    });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.voices button'); if (!b) return;
    try { localStorage.setItem(VKEY, b.dataset.voice); } catch (err) {}
    setVoice(b.dataset.voice);
  });
  try { var s = localStorage.getItem(VKEY); if (s) setVoice(s); } catch (err) {}
})();
"""


def course_card(c, n_tracks):
    text = " ".join([c["code"], c["title"], c["blurb"], c["subject"], " ".join(c["skills"])]).lower()
    badges = "".join(f"<span>{E(b)}</span>" for b in c["badges"])
    return f'''<button type="button" class="card" data-course-open="{c["id"]}" data-text="{E(text)}" aria-haspopup="dialog">
      <span class="cv"><img src="{c["cover"]}" alt="" loading="lazy"><span class="badges">{badges}</span><span class="play">Preview · Track 00</span></span>
      <span class="bd">
        <span class="partner"><img src="{K.BRAND["mark"]}" alt="">{K.BRAND["name"]} · {E(c["partner"])}</span>
        <h3>{E(c["code"])} · {E(c["title"])}</h3>
        <span class="sk"><b>Skills you'll gain:</b> {E(", ".join(c["skills"][:6]))}</span>
        <span class="mt">{E(c["level"])} · {E(c["kind"])} · {E(c["length"])} · {n_tracks} tracks</span>
      </span>
    </button>'''


def course_modal(c, n_tracks):
    lec = BS.track_video(c["overview"])
    video = BS.player_for(lec, "Course overview", f'{c["id"]}-overview') if lec else ""
    jpg = c["map"].replace(".pdf", ".jpg")
    dl = (f'<a class="dlmap" href="{c["map"]}" download="{BS.pdf_name(c["map"])}"><img src="{jpg}" alt="" loading="lazy">'
          f'<span><b>Download the course map</b><small>The whole course on one board · PDF</small></span></a>') if os.path.exists(os.path.join(BS.ROOT, c["map"])) else ""
    parts = {}
    for m in D.MODULES:
        parts.setdefault(m["part"], []).append(m)
    mods = "".join(f"<li>{E(m['title'])}</li>" for m in D.MODULES)
    learn = "".join(f"<li>{E(o)}</li>" for o in D.OUTCOMES[:5])
    chips = "".join(f"<span>{E(s)}</span>" for s in c["skills"])
    n_labs = sum(1 for m in D.MODULES for a in m["activities"] if a["kind"] == "lab")
    return f'''<dialog class="cmodal" id="course-{c["id"]}" aria-labelledby="cm-{c["id"]}-t">
  <div class="cm-top"><div><small>{K.BRAND["name"]} · {E(c["partner"])}</small><h2 id="cm-{c["id"]}-t">{E(c["code"])} · {E(c["title"])}</h2></div>
    <button type="button" class="cm-x" data-cm-close aria-label="Close">×</button></div>
  <div class="cm-body">
    <div>{video}<p style="margin:14px 0 0;color:#3b4658">{E(c["blurb"])}</p></div>
    <div>
      <ul class="facts">
        <li><b>Level</b>{E(c["level"])} · {E(D.COURSE["level"])}</li>
        <li><b>Length</b>{E(D.COURSE["length"])}</li>
        <li><b>Includes</b>{len(D.MODULES)} modules · {n_tracks} narrated tracks · {n_labs} labs · 2 projects</li>
        <li><b>Prerequisite</b>{E(D.COURSE["prereq"])}</li>
        <li><b>Cost</b>Free and open</li>
      </ul>
      <div class="cm-ctas">
        <button type="button" class="abtn warm lg" data-join="join" data-course="{c["id"]}">Enroll for free</button>
        <a class="abtn lg" href="{c["page"]}">Go to the course →</a>
      </div>
      {dl}
    </div>
    <div class="cm-more">
      <div><h3>What you'll learn</h3><ul>{learn}</ul><div class="chips">{chips}</div></div>
      <div><h3>{len(D.MODULES)} modules</h3><ol class="mods">{mods}</ol></div>
    </div>
  </div>
</dialog>'''


def page():
    n_tracks = len(BS.setlist(False))
    c0 = K.COURSES[0]
    n_labs = sum(1 for m in D.MODULES for a in m["activities"] if a["kind"] == "lab")
    cards = "".join(course_card(c, n_tracks) for c in K.COURSES)
    soon = '<div class="card soon" aria-hidden="false"><span><b>More courses on the way</b>Join for free to hear when the next one opens.</span></div>'
    modals = "".join(course_modal(c, n_tracks) for c in K.COURSES)
    paths = "".join(
        f'''<div class="path"><h3>{E(r["name"])}</h3><span class="who">{E(r["who"])}</span>
          <ul>{"".join(f"<li>{E(g)}</li>" for g in r["gets"])}</ul>{f'<em>{E(r["note"])}</em>' if r.get("note") else ""}
          <button type="button" class="abtn{" solid" if r["id"] != "instructor" else ""}" data-join="join" data-role="{r["id"]}">Join as {E(r["name"].lower())}</button></div>'''
        for r in K.ROLES)
    lec = BS.track_video(c0["overview"])
    peek = (f'<button type="button" class="peek" data-course-open="{c0["id"]}"><img src="curriculum/video/{c0["overview"]}.jpg" alt="">'
            f'<span><small>Watch · {E(lec["track"])} · {BS.duration(lec["id"])}</small><b>{E(lec["name"])}: {E(c0["code"])} in one track</b></span></button>') if lec else ""
    legacy_js = JS.replace("LEGACY_RE", repr(LEGACY))
    return f'''<!DOCTYPE html>
<!-- GENERATED FILE: edit curriculum/catalog.py, catalog_page.py or shell.py, then run  python curriculum/build_site.py -->
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{K.BRAND["name"]} · Courses in agentic AI</title>
<meta name="description" content="{E(K.BRAND["tagline"])} Free courses from {K.BRAND["name"]}, {E(K.BRAND["parent"].lower())}.">
{SH.HEAD}
<style>{SH.SHELL_CSS}{CSS}</style>
</head>
<body>
{SH.topbar("#", "courses")}
<main>
<div class="hero">
  <div class="w">
    <div>
      <span class="kick">Free courses · open to everyone</span>
      <h1>Learn to build AI that <span class="g">acts</span> — and that you can trust.</h1>
      <p>Illustrated, narrated courses on agentic AI: how agents reason, use tools, remember, and plan, and how to keep them reliable, observable, and safe in production.</p>
      <div class="ctas"><button type="button" class="abtn warm lg" data-join="join">Join for free</button><a class="abtn lg" href="#courses">Explore courses</a></div>
      <div class="stats"><div><b>{len(K.COURSES)}</b><span>course, more coming</span></div><div><b>{n_tracks}</b><span>narrated tracks</span></div>
        <div><b>{n_labs}</b><span>hands-on labs</span></div><div><b>$0</b><span>always free</span></div></div>
    </div>
    <div class="art"><img class="logo" src="{K.BRAND["mark_lg"]}" alt="{K.BRAND["name"]}: half brain, half light bulb">{peek}</div>
  </div>
</div>

<section id="courses">
  <div class="w">
    <div class="head"><div><span class="kick">Explore</span><h2>Courses</h2></div><span class="count" id="count">{len(K.COURSES)} course{"s" if len(K.COURSES) != 1 else ""}</span></div>
    <div class="grid">{cards}{soon}</div>
    <p class="empty" id="empty" hidden>No course matches that yet. Try “agents”, “MCP”, or “memory”.</p>
  </div>
</section>

<section id="paths" class="alt">
  <div class="w">
    <span class="kick">Learn your way</span><h2 style="font-size:clamp(26px,3vw,34px)">Join as who you are</h2>
    <p class="sub">When you join, you pick a role. It decides what you can open — and you can ask to change it later.</p>
    <div class="paths">{paths}</div>
  </div>
</section>

<section>
  <div class="w">
    <span class="kick">How it works</span><h2 style="font-size:clamp(26px,3vw,34px)">Four steps, every week</h2>
    <div class="steps">
      <div class="step"><b>Track</b><span>An illustrated, narrated lecture, captioned, in your choice of voice — plus its printable map.</span></div>
      <div class="step"><b>Reading</b><span>The matching chapter of the textbook, with hand-picked extras.</span></div>
      <div class="step"><b>Quiz</b><span>A practice check you can retake until it clicks.</span></div>
      <div class="step"><b>Application</b><span>That week's lab or project: build it, break it, fix it.</span></div>
    </div>
  </div>
</section>

<section id="instructors" class="alt">
  <div class="w teach">
    <div>
      <span class="kick">For instructors</span><h2 style="font-size:clamp(26px,3vw,34px)">Teach it as your own</h2>
      <ul>
        <li>The full instructor's guide: every track script, reading outlines, lab scripts, and question banks</li>
        <li>Semester- and instructor-neutral: swap in your dates, your quizzes, your style</li>
        <li>Course repository access for adopting instructors, after a quick approval</li>
      </ul>
      <button type="button" class="abtn solid lg" data-join="join" data-role="instructor">Join as an instructor</button>
    </div>
    <div class="panel"><b>Already approved?</b>Open the instructor's guide with the password you were given. Signing in replaces the password once {K.BRAND["name"]} accounts launch.
      <br><a class="abtn" href="instructor-guide.html">Open the instructor's guide</a></div>
  </div>
</section>
</main>
{SH.footer()}
{modals}
{SH.join_dialog()}
<script>{legacy_js}</script>
<script>{SH.SHELL_JS}</script>
</body>
</html>
'''
