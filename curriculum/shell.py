"""The Aideation shell shared by every page: brand fonts, top bar, footer, and the join / log-in dialog.

Pages include SHELL_CSS in their <style>, topbar() and footer() in their body, join_dialog() once, and SHELL_JS once.
"""
import html

import catalog as K

E = lambda s: html.escape(str(s), quote=True)  # noqa: E731

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@600;700&display=swap" rel="stylesheet">')

HEAD = (f'<link rel="icon" type="image/png" href="{K.BRAND["favicon"]}">'
        f'<meta name="aideation-api" content="{E(K.API_BASE)}">' + FONTS)

SHELL_CSS = r"""
:root{
  --navy:#143a75; --a-blue:#1d4f9c; --sky:#1e8fd6; --teal:#1fc3c4; --lime:#7cc242;
  --sun:#ffd21f; --orange:#ff8a1f; --flame:#f2522e; --pink:#e0306a;
  --grad-cool:linear-gradient(135deg,#1d4f9c,#1e8fd6 45%,#1fc3c4 75%,#7cc242);
  --grad-warm:linear-gradient(135deg,#ffd21f,#ff8a1f 50%,#f2522e 80%,#e0306a);
  --grad:linear-gradient(90deg,#1d4f9c,#1e8fd6,#1fc3c4,#7cc242,#ffd21f,#ff8a1f,#e0306a);
}
h1,h2,h3{font-family:Poppins,Inter,'Segoe UI',system-ui,sans-serif;letter-spacing:-.01em}
.atop{position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid #e1e7ef}
.atop::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:3px;background:var(--grad);opacity:.9}
.atop .bar-in{max-width:1280px;margin:0 auto;padding:0 24px;height:68px;display:flex;align-items:center;gap:18px}
.alogo{display:flex;align-items:center;gap:10px;text-decoration:none;flex:none}
.alogo img{width:40px;height:40px;object-fit:contain}
.alogo .wm{display:flex;flex-direction:column;line-height:1}
.alogo .wm b{font-family:Poppins,Inter,sans-serif;font-size:22px;font-weight:700;letter-spacing:-.01em}
.alogo .wm b .c1{background:linear-gradient(90deg,#1d4f9c,#1e8fd6);-webkit-background-clip:text;background-clip:text;color:transparent}
.alogo .wm b .c2{background:linear-gradient(90deg,#ff8a1f,#f2522e);-webkit-background-clip:text;background-clip:text;color:transparent}
.alogo .wm small{font-size:10.5px;color:#566173;font-weight:600;letter-spacing:.06em;text-transform:uppercase;margin-top:3px}
.atop .explore{font-weight:700;font-size:14px;color:#fff;background:var(--a-blue);border-radius:6px;padding:9px 14px;text-decoration:none}
.atop .explore:hover{background:var(--navy)}
.asearch{flex:1;max-width:460px;position:relative}
.asearch input{width:100%;border:1px solid #c3d2e6;border-radius:999px;padding:10px 16px 10px 40px;font:inherit;font-size:14px;background:#f5f8fc}
.asearch input:focus{outline:2px solid var(--sky);background:#fff}
.asearch svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);width:16px;height:16px;stroke:#566173;fill:none;stroke-width:2}
.anav{margin-left:auto;display:flex;align-items:center;gap:18px}
.anav a{color:#1b2533;text-decoration:none;font-size:14px;font-weight:600}
.anav a:hover{color:var(--a-blue)}
.anav a.cur{color:var(--a-blue)}
.abtn{white-space:nowrap;display:inline-flex;align-items:center;justify-content:center;gap:8px;border-radius:6px;padding:9px 16px;font:inherit;font-size:14px;font-weight:700;cursor:pointer;text-decoration:none;border:1.5px solid var(--a-blue);background:#fff;color:var(--a-blue)}
.abtn:hover{background:#eef4fb}
.abtn.solid{background:var(--a-blue);color:#fff}
.abtn.solid:hover{background:var(--navy);border-color:var(--navy)}
.abtn.warm{background:var(--grad-warm);border:0;color:#fff;padding:10.5px 17.5px}
.abtn.warm:hover{filter:brightness(1.05)}
.abtn.lg{padding:13px 24px;font-size:15.5px}
.abtn.warm.lg{padding:14.5px 25.5px}
@media (max-width:900px){.asearch,.anav .hide-sm{display:none}}
@media (max-width:560px){.atop .explore{display:none}.anav{gap:8px}.anav .abtn{padding:8px 11px;font-size:13px}.alogo .wm small{display:none}}

.afoot{background:#0d1b33;color:#c9d4e2;font-size:14px;margin-top:40px}
.afoot::before{content:"";display:block;height:4px;background:var(--grad)}
.afoot .in{max-width:1280px;margin:0 auto;padding:40px 24px;display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:28px}
.afoot h4{color:#fff;font-size:14px;margin:0 0 10px}
.afoot a{display:block;color:#c9d4e2;text-decoration:none;margin:6px 0}
.afoot a:hover{color:#fff}
.afoot .who{display:flex;gap:12px;align-items:flex-start}
.afoot .who img{width:48px;height:48px;border-radius:10px;background:#fff;padding:3px}
.afoot .fine{max-width:1280px;margin:0 auto;padding:16px 24px 28px;border-top:1px solid #22324f;font-size:12.5px;color:#93a3bb}
@media (max-width:760px){.afoot .in{grid-template-columns:1fr 1fr}}

/* join / log in */
dialog.join{border:0;border-radius:18px;padding:0;width:min(640px,calc(100vw - 24px));max-height:calc(100vh - 32px);box-shadow:0 30px 80px rgba(13,27,51,.35);color:#1b2533}
dialog.join::backdrop{background:rgba(13,27,51,.55)}
.join .hd{background:var(--grad-cool);color:#fff;padding:22px 26px 20px;position:relative}
.join .hd small{font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:11.5px;opacity:.9}
.join .hd h2{font-size:24px;margin:4px 0 0;color:#fff}
.join .x{position:absolute;right:14px;top:12px;background:rgba(255,255,255,.18);border:0;color:#fff;width:34px;height:34px;border-radius:50%;font-size:20px;cursor:pointer}
.join .bd{padding:20px 26px 24px}
.join .jstep[hidden]{display:none}
.roles{display:grid;gap:10px;margin:6px 0 16px}
.role{display:flex;gap:12px;align-items:flex-start;border:1.5px solid #e1e7ef;border-radius:12px;padding:13px 14px;cursor:pointer}
.role:hover{border-color:#9fb6d6}
.role input{margin-top:4px;accent-color:var(--a-blue)}
.role b{display:block;font-size:15.5px}
.role span.who{display:block;color:#566173;font-size:14px}
.role ul{margin:6px 0 0;padding-left:18px;font-size:13.5px;color:#1b2533}
.role em{display:inline-block;margin-top:6px;font-style:normal;font-size:12px;font-weight:700;color:#b8560b;background:#fff3e0;border-radius:999px;padding:2px 9px}
.role:has(input:checked){border-color:var(--a-blue);background:#f2f7fd;box-shadow:0 0 0 3px rgba(30,143,214,.15)}
.providers{display:grid;gap:10px;margin:8px 0 12px}
.prov{display:flex;align-items:center;justify-content:center;gap:10px;border:1.5px solid #c9d4e2;background:#fff;border-radius:10px;padding:12px;font:inherit;font-weight:700;font-size:15px;cursor:pointer;color:#1b2533}
.prov:hover{background:#f5f8fc;border-color:#9fb6d6}
.prov svg{width:20px;height:20px}
.join .fine{font-size:12.5px;color:#566173;margin:8px 0 0}
.join .row-btns{display:flex;gap:10px;justify-content:space-between;align-items:center;flex-wrap:wrap}
.join .back{background:none;border:0;color:#1d4f9c;font:inherit;font-weight:700;cursor:pointer;padding:6px 0}
.join .soon{background:#fff8e6;border:1px solid #ffe2a3;border-radius:10px;padding:12px 14px;font-size:14px;margin-top:10px}
.join .soon[hidden]{display:none}
.join .chosen{font-size:14px;color:#566173;margin:0 0 6px}
"""

ICON_SEARCH = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
ICON_GITHUB = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#1b2533" d="M12 .5a11.5 11.5 0 0 0-3.64 22.42c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.05-.71.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.68 0-1.26.45-2.28 1.19-3.09-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.83 1.19 3.09 0 4.41-2.69 5.38-5.25 5.67.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5Z"/></svg>')
ICON_GOOGLE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M23.5 12.27c0-.85-.08-1.67-.22-2.45H12v4.64h6.45a5.5 5.5 0 0 1-2.39 3.62v3h3.87c2.26-2.09 3.57-5.17 3.57-8.81Z"/>'
               '<path fill="#34A853" d="M12 24c3.24 0 5.95-1.07 7.93-2.91l-3.87-3c-1.07.72-2.45 1.15-4.06 1.15-3.13 0-5.78-2.11-6.72-4.95h-4v3.1A12 12 0 0 0 12 24Z"/>'
               '<path fill="#FBBC05" d="M5.28 14.29A7.2 7.2 0 0 1 4.9 12c0-.8.14-1.57.38-2.29V6.6h-4A12 12 0 0 0 0 12c0 1.94.46 3.77 1.28 5.4l4-3.11Z"/>'
               '<path fill="#EA4335" d="M12 4.77c1.76 0 3.34.61 4.59 1.8l3.43-3.43A11.5 11.5 0 0 0 12 0 12 12 0 0 0 1.28 6.6l4 3.11C6.22 6.88 8.87 4.77 12 4.77Z"/></svg>')


def topbar(home, here=""):
    """home: link to the catalog ('#' on the catalog itself). here: 'courses' | 'instructors' | course id."""
    srch = ('<label class="asearch">' + ICON_SEARCH +
            '<input type="search" id="asearch" placeholder="What do you want to learn?" aria-label="Search courses"></label>') if home == "#" else ""
    cur = lambda k: ' class="cur"' if here == k else ""  # noqa: E731
    base = "" if home == "#" else "index.html"
    return f'''<header class="atop">
  <div class="bar-in">
    <a class="alogo" href="{"#" if home == "#" else "index.html"}" aria-label="{K.BRAND["name"]} home"><img src="{K.BRAND["mark"]}" alt="" width="40" height="40"><span class="wm"><b><span class="c1">Aid</span><span class="c2">eation</span></b><small>{E(K.BRAND["parent"])}</small></span></a>
    <a class="explore" href="{base}#courses">Explore</a>
    {srch}
    <nav class="anav" aria-label="Account">
      <a class="hide-sm" href="{base}#paths"{cur("paths")}>How it works</a>
      <a class="hide-sm" href="{base}#instructors"{cur("instructors")}>For instructors</a>
      <button type="button" class="abtn" data-join="login">Log in</button>
      <button type="button" class="abtn warm" data-join="join">Join for free</button>
    </nav>
  </div>
</header>'''


def footer():
    links = "".join(f'<a href="{c["page"]}">{E(c["code"])} · {E(c["title"])}</a>' for c in K.COURSES)
    return f'''<footer class="afoot">
  <div class="in">
    <div class="who"><img src="{K.BRAND["mark"]}" alt=""><div><b style="color:#fff;font-size:16px">{K.BRAND["name"]}</b><br>{E(K.BRAND["parent"])}<br><span style="color:#93a3bb">{E(K.BRAND["tagline"])}</span></div></div>
    <div><h4>Courses</h4>{links}</div>
    <div><h4>Learn</h4><a href="index.html#paths">How it works</a><a href="index.html#courses">Explore courses</a><button type="button" class="linklike" data-join="join" style="all:unset;cursor:pointer;display:block;margin:6px 0">Join for free</button></div>
    <div><h4>Teach</h4><a href="index.html#instructors">For instructors</a><a href="instructor-guide.html">Instructor's guide</a><a href="https://github.com/addiboyer24/CSCI391_ST_AgenticAI_Autumn2026" target="_blank" rel="noopener">Course repository</a></div>
  </div>
  <div class="fine">© {K.BRAND["name"]}, {E(K.BRAND["parent"].replace("A ", "a "))}. Course content is free and open. Logos and course names belong to their owners; no university endorsement is implied.</div>
</footer>'''


def join_dialog():
    roles = "".join(
        f'''<label class="role"><input type="radio" name="role" value="{r["id"]}"{" checked" if not i else ""}>
          <span><b>{E(r["name"])}</b><span class="who">{E(r["who"])}</span><ul>{"".join(f"<li>{E(g)}</li>" for g in r["gets"])}</ul>{f'<em>{E(r["note"])}</em>' if r.get("note") else ""}</span></label>'''
        for i, r in enumerate(K.ROLES))
    courses = "".join(f'<option value="{c["id"]}">{E(c["code"])} · {E(c["title"])}</option>' for c in K.COURSES)
    return f'''<dialog class="join" id="join" aria-labelledby="join-title">
  <div class="hd"><small id="join-kicker">Join {K.BRAND["name"]}</small><h2 id="join-title">Who are you joining as?</h2>
    <button type="button" class="x" data-close aria-label="Close">×</button></div>
  <div class="bd">
    <div class="jstep" data-step="role">
      <label class="chosen" {"hidden" if len(K.COURSES) < 2 else ""}>Course <select id="join-course">{courses}</select></label>
      <p class="chosen">Your role decides what you can open. You can ask to change it later.</p>
      <div class="roles">{roles}</div>
      <div class="row-btns"><span class="fine">Free · no payment details, ever</span><button type="button" class="abtn solid lg" data-next>Continue</button></div>
    </div>
    <div class="jstep" data-step="sign" hidden>
      <p class="chosen" id="join-summary"></p>
      <div class="providers">
        <button type="button" class="prov" data-provider="github">{ICON_GITHUB}Continue with GitHub</button>
        <button type="button" class="prov" data-provider="google">{ICON_GOOGLE}Continue with Google</button>
      </div>
      <p class="fine">We only receive your name, email, and profile picture. Instructors then add a passkey or an authenticator app before the guide unlocks.</p>
      <div class="soon" id="join-soon" hidden role="status"><b>Accounts open soon.</b> Sign-in arrives with the {K.BRAND["name"]} accounts service. Until then, everything here is open — no account needed. <a href="{K.COURSES[0]["page"]}">Start {E(K.COURSES[0]["code"])} now →</a></div>
      <div class="row-btns" style="margin-top:12px"><button type="button" class="back" data-back>← Back</button></div>
    </div>
  </div>
</dialog>'''


SHELL_JS = r"""
(function () {
  var dlg = document.getElementById('join');
  if (!dlg) return;
  var api = (document.querySelector('meta[name="aideation-api"]') || {}).content || '';
  var steps = dlg.querySelectorAll('.jstep'), course = document.getElementById('join-course');
  var mode = 'join';
  function step(name) { Array.prototype.forEach.call(steps, function (s) { s.hidden = s.dataset.step !== name; }); }
  function role() { var r = dlg.querySelector('input[name=role]:checked'); return r ? r.value : 'explorer'; }
  function roleName() { var r = dlg.querySelector('input[name=role]:checked'); return r ? r.closest('.role').querySelector('b').textContent : ''; }
  function open(how, opts) {
    opts = opts || {};
    mode = how;
    document.getElementById('join-soon').hidden = true;
    if (opts.course && course) course.value = opts.course;
    if (opts.role) { var r = dlg.querySelector('input[name=role][value="' + opts.role + '"]'); if (r) r.checked = true; }
    document.getElementById('join-kicker').textContent = how === 'login' ? 'Welcome back' : 'Join for free';
    if (how === 'login') {
      document.getElementById('join-title').textContent = 'Log in';
      document.getElementById('join-summary').textContent = 'Use the account you joined with.';
      dlg.querySelector('[data-back]').hidden = true;
      step('sign');
    } else {
      document.getElementById('join-title').textContent = 'Who are you joining as?';
      dlg.querySelector('[data-back]').hidden = false;
      step('role');
    }
    if (!dlg.open) dlg.showModal();
  }
  window.aideationJoin = open;
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-join]');
    if (!b) return;
    e.preventDefault();
    var other = document.querySelector('dialog[open]:not(#join)');
    if (other) other.close();
    open(b.dataset.join, { course: b.dataset.course, role: b.dataset.role });
  });
  dlg.querySelector('[data-next]').onclick = function () {
    document.getElementById('join-title').textContent = 'Create your account';
    var c = course ? course.options[course.selectedIndex].text : '';
    document.getElementById('join-summary').textContent = 'Joining ' + c + ' as ' + roleName() + '.';
    step('sign');
  };
  dlg.querySelector('[data-back]').onclick = function () { open('join'); };
  dlg.querySelector('[data-close]').onclick = function () { dlg.close(); };
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  Array.prototype.forEach.call(dlg.querySelectorAll('[data-provider]'), function (b) {
    b.onclick = function () {
      if (!api) { document.getElementById('join-soon').hidden = false; return; }
      var q = new URLSearchParams({ return_to: location.href.split('#')[0] });
      if (mode === 'join') { q.set('intent', 'signup'); q.set('role', role()); if (course) q.set('course', course.value); }
      location.href = api.replace(/\/$/, '') + '/auth/' + b.dataset.provider + '/start?' + q.toString();
    };
  });
})();
"""
