"""The site in a real browser: scripts run without errors and the interactive pieces work.

Needs Playwright with a browser:  python -m playwright install chromium
Skipped automatically when no browser is available; skip on purpose with  -m "not browser".
"""
import os
import re

import pytest

from conftest import ROOT

pytestmark = pytest.mark.browser
sync_api = pytest.importorskip("playwright.sync_api")


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as p:
        b = None
        for kw in ({}, {"channel": "msedge"}, {"channel": "chrome"}):
            try:
                b = p.chromium.launch(**kw)
                break
            except Exception:
                continue
        if b is None:
            pytest.skip("no Chromium-family browser installed")
        yield b
        b.close()


@pytest.fixture
def open_page(browser, server):
    pages = []

    def go(path="csci391.html", **ctx):
        context = browser.new_context(**ctx)
        page = context.new_page()
        page.errors = []
        page.on("pageerror", lambda e: page.errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and page.errors.append(m.text))
        page.goto(f"{server}/{path}")
        pages.append(context)
        return page

    yield go
    for c in pages:
        c.close()


def test_home_loads_without_script_errors(open_page):
    page = open_page()
    page.wait_for_timeout(500)
    real = [e for e in page.errors if "favicon" not in e]
    assert not real, f"errors on load: {real}"


def test_setlist_stage_shows_the_clicked_track(open_page):
    page = open_page()
    songs = page.locator("#setlist .song")
    assert songs.count() >= 21
    target = songs.nth(5)
    name = target.get_attribute("data-name")
    target.click()
    assert name in page.locator("#np").inner_text()
    assert page.locator("#screen img.on").get_attribute("data-i") == target.get_attribute("data-i")
    assert page.locator("#np-go").get_attribute("href") == target.get_attribute("href")


def test_watch_track_opens_its_video(open_page):
    page = open_page()
    page.locator("#setlist .song").first.click()
    href = page.locator("#np-go").get_attribute("href")
    page.locator("#np-go").click()
    page.wait_for_timeout(300)
    assert page.evaluate("h => document.querySelector(h).closest('details').open", href), "the track's video row should open"


def test_practice_quiz_scores_and_remembers(open_page):
    page = open_page()
    sec = page.locator("section.check").first
    mod = sec.get_attribute("data-mod")
    sec.evaluate("s => s.closest('details') && (s.closest('details').open = true)")
    for q in sec.locator(".q").all():
        ans = q.get_attribute("data-answer")
        q.locator(f'input[value="{ans}"]').check()
    sec.locator(".submit").click()
    assert "Passed" in sec.locator(".score").inner_text()
    assert page.locator("#prog-n").inner_text() == "1"
    page.reload()
    assert page.locator("#prog-n").inner_text() == "1", "a passed check should persist across reloads"
    page.locator("#prog-reset").click()
    assert page.locator("#prog-n").inner_text() == "0"


def test_voice_picker_swaps_and_remembers(open_page):
    page = open_page()
    fig = page.locator("figure.player").first
    fig.evaluate("f => f.closest('details') && (f.closest('details').open = true)")
    fig.locator('.voices button[data-voice="zira"]').click()
    assert fig.locator("source").get_attribute("src").endswith("-zira.mp4")
    page.reload()
    assert page.locator("figure.player").nth(3).locator('button[data-voice="zira"]').get_attribute("aria-pressed") == "true"


def test_every_video_and_caption_file_is_served(open_page, server):
    page = open_page()
    urls = page.evaluate("""() => [...document.querySelectorAll('figure.player source, figure.player track, .voices button')]
        .map(e => e.getAttribute('src') || (e.dataset.stem && e.dataset.stem + '.vtt')).filter(Boolean)""")
    bad = [u for u in set(urls) if page.request.head(f"{server}/{u}").status != 200]
    assert not bad, f"not served: {bad[:10]}"


def test_contents_groups_collapse(open_page):
    page = open_page(viewport={"width": 1280, "height": 900})
    grp = page.locator(".contents details.grp").first
    summary = grp.locator("summary")
    was = grp.evaluate("d => d.open")
    summary.click()
    assert grp.evaluate("d => d.open") != was


@pytest.mark.parametrize("width", [375, 768])
def test_no_horizontal_scroll_on_small_screens(open_page, width):
    page = open_page(viewport={"width": width, "height": 800})
    page.wait_for_timeout(300)
    sw = page.evaluate("document.documentElement.scrollWidth")
    assert sw <= width, f"page is {sw}px wide on a {width}px screen"


def test_guide_rejects_a_wrong_password(open_page):
    page = open_page("instructor-guide.html")
    page.fill("#pw", "definitely-not-the-password")
    page.click("#go")
    page.wait_for_function("document.getElementById('err').textContent.length > 0", timeout=20000)
    assert page.locator("#gate").is_visible()


def test_guide_opens_with_the_right_password(open_page):
    pw = os.environ.get("GUIDE_PASSWORD")
    local = os.path.join(ROOT, "curriculum", "private", "guide_password.txt")
    if not pw and os.path.exists(local):
        pw = open(local, encoding="utf8").read().strip()
    if not pw:
        pytest.skip("no guide password available")
    page = open_page("instructor-guide.html")
    page.fill("#pw", pw)
    page.click("#go")
    page.wait_for_selector("article.module", timeout=30000)
    assert page.locator("article.module").count() == 14
    assert re.search(r"Instructor", page.title())


def test_nothing_marked_hidden_is_shown(open_page):
    """A fresh visitor has passed no checks: no "Check passed" badge, best score, or reset button may show."""
    page = open_page()
    shown = page.evaluate("""() => [...document.querySelectorAll('[hidden]')]
        .filter(e => getComputedStyle(e).display !== 'none').map(e => e.className || e.id || e.tagName)""")
    assert not shown, f"elements with the hidden attribute are visible: {shown[:10]}"
    assert page.locator('[data-done]:visible').count() == 0


# ───────────── the Aideation catalog ─────────────
def test_catalog_loads_without_errors(open_page):
    page = open_page("index.html")
    page.wait_for_timeout(400)
    assert not [e for e in page.errors if "favicon" not in e], page.errors


def test_course_card_opens_its_preview_and_enroll_starts_sign_up(open_page):
    page = open_page("index.html")
    page.locator('.card[data-course-open="csci391"]').click()
    dlg = page.locator("#course-csci391")
    assert dlg.is_visible() and dlg.locator("video").count() == 1
    dlg.locator('[data-join="join"]').click()
    join = page.locator("#join")
    assert join.is_visible() and not dlg.is_visible(), "enrolling should swap the preview for the join dialog"
    join.locator('input[value="instructor"]').check()
    join.locator("[data-next]").click()
    assert "as Instructor" in page.locator("#join-summary").inner_text()
    join.locator('[data-provider="google"]').click()
    if not page.evaluate("document.querySelector('meta[name=aideation-api]').content"):
        assert page.locator("#join-soon").is_visible(), "with no API yet, say accounts open soon"


def test_log_in_goes_straight_to_providers(open_page):
    page = open_page("csci391.html")
    page.locator('.atop [data-join="login"]').click()
    assert page.locator("#join-title").inner_text() == "Log in"
    assert page.locator('#join [data-step="sign"]').is_visible() and not page.locator('#join [data-step="role"]').is_visible()


def test_old_course_links_land_on_the_course_page(open_page):
    page = open_page("index.html#m03")
    page.wait_for_url("**/csci391.html#m03")


def test_catalog_search_filters(open_page):
    page = open_page("index.html")
    page.fill("#asearch", "zzzz-nothing")
    assert page.locator("#empty").is_visible()
    page.fill("#asearch", "mcp")
    assert page.locator('.card[data-course-open="csci391"]').is_visible() and not page.locator("#empty").is_visible()


@pytest.mark.parametrize("width", [375, 768])
def test_catalog_fits_small_screens(open_page, width):
    page = open_page("index.html", viewport={"width": width, "height": 800})
    page.wait_for_timeout(300)
    assert page.evaluate("document.documentElement.scrollWidth") <= width
