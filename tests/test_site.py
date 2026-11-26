"""The built pages: up to date with their sources, structurally sound, every link resolving, nothing private leaking."""
import base64
import os
import re
import subprocess

import pytest

from conftest import ROOT, parse, read

SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9_-]{20,}", "an API key (sk-…)"),
    (r"sk-ant-[A-Za-z0-9_-]{20,}", "an Anthropic API key"),
    (r"ghp_[A-Za-z0-9]{30,}", "a GitHub token"),
    (r"github_pat_[A-Za-z0-9_]{30,}", "a GitHub token"),
    (r"AKIA[0-9A-Z]{16}", "an AWS access key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "a private key"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "a Slack token"),
]
TEXT_EXT = {".py", ".html", ".md", ".txt", ".json", ".yml", ".yaml", ".js", ".css", ".ini", ".cfg", ".toml", ".vtt", ".csv"}


# ───────────── freshness ─────────────
def test_index_is_up_to_date_with_its_sources(site, index_html):
    """index.html is generated. If this fails, run  python curriculum/build_site.py  and commit the result."""
    built = site.page(False).replace("\r\n", "\n")
    assert built == index_html.replace("\r\n", "\n"), "index.html is stale: rebuild with python curriculum/build_site.py"


def test_no_template_placeholders_left(index_html):
    leftovers = re.findall(r"\$\$?[A-Za-z_]{3,}", re.sub(r"<script>.*?</script>", "", index_html, flags=re.S))
    assert not leftovers, f"unfilled template fields: {sorted(set(leftovers))[:10]}"


# ───────────── structure ─────────────
@pytest.fixture(scope="module")
def page(index_html):
    return parse(index_html)


def test_basic_document_shape(page, index_html):
    assert index_html.lstrip().lower().startswith("<!doctype html>")
    tags = [t for t, _ in page.tags]
    assert tags.count("h1") == 1, "exactly one main heading"
    assert ("meta", {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}) in page.tags
    assert re.search(r"<title>[^<]{10,}</title>", index_html)
    assert ("html", {"lang": "en"}) in page.tags


def test_ids_are_unique(page):
    dup = sorted({i for i in page.ids if page.ids.count(i) > 1})
    assert not dup, f"duplicate ids: {dup}"


def test_in_page_links_resolve(page):
    ids = set(page.ids)
    broken = sorted({h[1:] for _, k, h in page.links if k == "href" and h.startswith("#") and len(h) > 1 and h[1:] not in ids})
    assert not broken, f"links to missing anchors: {broken}"


def test_local_files_exist_and_are_committed(page, tracked):
    missing = []
    for _, _, url in page.links:
        if url.startswith(("http://", "https://", "#", "mailto:", "data:")) or not url:
            continue
        path = url.split("#")[0].split("?")[0]
        if path and path not in tracked:
            missing.append(path)
    assert not missing, f"linked but not committed (will 404 on GitHub Pages): {sorted(set(missing))[:15]}"


def test_images_have_alt_text(page):
    assert all("alt" in img for img in page.imgs), "every <img> needs an alt attribute (empty for decoration)"


def test_external_links_open_safely(page):
    for tag, a in page.tags:
        if tag == "a" and a.get("target") == "_blank":
            assert "noopener" in (a.get("rel") or ""), f"target=_blank without rel=noopener: {a.get('href')}"


def test_every_track_is_on_the_setlist(index_html):
    import video_scripts as VS
    songs = re.findall(r'class="song[^"]*" href="#([\w-]+)-video"', index_html)
    assert sorted(songs) == sorted(l["id"] for l in VS.LECTURES), "the hero setlist should list every track exactly once"


def test_every_module_has_track_reading_and_quiz(index_html):
    import course_data as D
    for m in D.MODULES:
        block = index_html.split(f'<article class="module" id="{m["id"]}">', 1)[1].split("</article>", 1)[0]
        for part in ("Track", "Reading"):
            assert f"<h4>{part}</h4>" in block, f"{m['id']} has no {part} section"
        if any(a["kind"] in ("lab", "project", "code") for a in m["activities"]):
            assert "<h4>Application</h4>" in block, f"{m['id']} has an assignment but no Application section"


def test_page_weight_is_reasonable(index_html):
    assert len(index_html.encode("utf8")) < 1_500_000, "index.html is getting heavy; check for inlined media"


# ───────────── privacy ─────────────
def test_instructor_guide_is_encrypted(guide_html):
    """The guide holds quiz questions and answer keys; only its password prompt may be readable."""
    assert 'id="gate"' in guide_html and '"ct":"' in guide_html, "instructor-guide.html must be the encrypted build"
    assert '<meta name="robots" content="noindex, nofollow">' in guide_html
    for leak in ("Teaching notes", "Question bank", "Scene 1 ·", "Reading outline", 'class="bank'):
        assert leak not in guide_html, f"plaintext guide content leaked: {leak!r}"


def test_private_sources_are_not_committed(tracked):
    leaked = [f for f in tracked if f.startswith("curriculum/private/") or f.endswith(("guide_password.txt", "graded_quizzes.py"))]
    assert not leaked, f"private files are committed: {leaked}"


def test_no_env_files_are_committed(tracked):
    envs = [f for f in tracked if os.path.basename(f) == ".env" or f.endswith((".env.local", ".pem", ".key"))]
    assert not envs, f"secret-bearing files are committed: {envs}"


def test_no_secrets_in_committed_text(tracked):
    hits = []
    for f in tracked:
        if os.path.splitext(f)[1].lower() not in TEXT_EXT or not os.path.exists(os.path.join(ROOT, f)):
            continue
        if os.path.getsize(os.path.join(ROOT, f)) > 3_000_000:
            continue
        text = read(f) if f else ""
        for pat, what in SECRET_PATTERNS:
            if re.search(pat, text):
                hits.append(f"{f}: {what}")
    assert not hits, "possible secrets committed:\n" + "\n".join(hits)


def test_graded_quiz_text_never_reaches_the_public_files(tracked):
    """Runs only where the private quiz source exists (an instructor's machine): no graded question may appear in a committed file."""
    src = os.path.join(ROOT, "curriculum", "private", "graded_quizzes.py")
    if not os.path.exists(src):
        pytest.skip("private quiz source not present (expected in CI)")
    import importlib.util
    spec = importlib.util.spec_from_file_location("gq", src)
    gq = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gq)
    stems = [q["q"][:60] for quiz in gq.QUIZZES.values() for q in quiz["questions"]]
    out = subprocess.run(["git", "grep", "-l", "-F", "-e", stems[0], *sum((["-e", s] for s in stems[1:]), [])],
                         cwd=ROOT, capture_output=True, text=True)
    assert not out.stdout.strip(), f"graded quiz text found in committed files: {out.stdout.split()}"


def test_guide_decrypts_with_the_real_password(guide_html):
    """With GUIDE_PASSWORD set (a CI secret, or locally from curriculum/private), the guide must open and be complete."""
    pw = os.environ.get("GUIDE_PASSWORD")
    local = os.path.join(ROOT, "curriculum", "private", "guide_password.txt")
    if not pw and os.path.exists(local):
        pw = open(local, encoding="utf8").read().strip()
    if not pw:
        pytest.skip("no guide password available")
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    blob = dict(re.findall(r'"(salt|iv|ct)":"([^"]+)"', guide_html))
    iters = int(re.search(r'"iter":(\d+)', guide_html).group(1))
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=base64.b64decode(blob["salt"]), iterations=iters).derive(pw.encode())
    html = AESGCM(key).decrypt(base64.b64decode(blob["iv"]), base64.b64decode(blob["ct"]), None).decode("utf8")
    g = parse(html)
    assert html.count('<article class="module"') == 14
    assert not sorted({i for i in g.ids if g.ids.count(i) > 1}), "duplicate ids in the guide"
    ids = set(g.ids)
    assert not sorted({h[1:] for _, k, h in g.links if k == "href" and h.startswith("#") and len(h) > 1 and h[1:] not in ids})
    for block in re.findall(r'<ol class="bank graded">(.*?)</ol>\s*</div>', html, re.S):
        assert 'class="key"' not in block, "a graded quiz shows its answer key"
