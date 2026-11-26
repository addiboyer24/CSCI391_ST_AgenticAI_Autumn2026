"""The tracks: narration scripts, illustrated storyboards, and the rendered media they produce.

Videos are rendered locally (they need Windows speech voices), so CI can't re-render them. These tests catch
the next best thing: a script edited without re-rendering, a storyboard that no longer lines up with its script,
or a missing poster, caption file, or board.
"""
import os
import re

import pytest

import course_data as D
import explainer_modules as XM
import explainer_scenes as XS
import video_scripts as VS

from conftest import CUR

LECTURES = VS.LECTURES
BY_ID = {l["id"]: l for l in LECTURES}
MODULE_IDS = [m["id"] for m in D.MODULES]
BOARDS = {**XM.BOARDS, **XS.STORYBOARDS}
VOICES = getattr(VS, "VOICES", [])


def media(lec_id, voice, ext):
    return os.path.join(CUR, "video", VS.media_stem(lec_id, voice) + ext)


def ids(l):
    return l["id"]


def test_every_module_has_a_track_and_ids_are_unique():
    assert len({l["id"] for l in LECTURES}) == len(LECTURES)
    assert set(MODULE_IDS) <= set(BY_ID), "a module has no lecture track"


def test_practice_tracks_cover_every_lab_and_project():
    hrefs = {a["href"] for m in D.MODULES for a in m["activities"] if a["kind"] in ("lab", "project") and a.get("href")}
    tracks = {l["for"]: l for l in LECTURES if l.get("for")}
    assert hrefs <= set(tracks), f"no walkthrough track for {sorted(hrefs - set(tracks))}"
    assert {l["kind"] for l in tracks.values()} == {"lab", "project"}


@pytest.mark.parametrize("lec", LECTURES, ids=ids)
def test_script_is_well_formed(lec):
    assert lec["name"].strip() and lec["track"].strip()
    assert lec["scenes"][0]["type"] == "title", f"{lec['id']}: a track opens with its title scene"
    for i, sc in enumerate(lec["scenes"]):
        assert sc["type"] in {"title", "quote", "bullets", "image"}, (lec["id"], i)
        assert sc["lines"], f"{lec['id']} scene {i} has no narration"
        for line in sc["lines"]:
            assert line.strip() == line and line, f"{lec['id']} scene {i}: blank or padded line"
            assert len(line) <= 260, f"{lec['id']} scene {i}: a caption this long won't fit on screen"
        if sc["type"] == "bullets":
            assert sc.get("heading") and 2 <= len(sc["bullets"]) <= 6, (lec["id"], i)
        if sc["type"] == "quote":
            assert sc.get("quote"), (lec["id"], i)


@pytest.mark.parametrize("lec", [l for l in LECTURES if l["id"] in BOARDS], ids=ids)
def test_storyboard_lines_up_with_its_script(lec):
    """Each scene's drawing is cued to a narration line; a cue past the scene's lines means the two drifted apart."""
    scenes = lec["scenes"]
    starts, n = [], 0
    for sc in scenes:
        starts.append(n)
        n += len(sc["lines"])
    if lec["id"] not in XM.SPECS:
        return  # hand-built storyboard (Track 2): checked by rendering
    specs = XM.SPECS[lec["id"]]
    assert len(specs) == len(scenes), f"{lec['id']}: {len(specs)} storyboard scenes for {len(scenes)} script scenes"
    for i, raw in enumerate(specs):
        sp = XM.absolute(raw, starts[i])
        lo, hi = starts[i], starts[i] + len(scenes[i]["lines"]) - 1
        cues = [c[1] for c in sp.get("cards", [])] + [b[0] for b in sp.get("beats", [])]
        if "quote_at" in sp:
            cues.append(sp["quote_at"][0])
        if "close" in sp:
            cues.append(sp["close"][0])
        for c in cues:
            assert lo <= c <= hi, f"{lec['id']} scene {i}: cue on line {c}, but the scene is lines {lo}–{hi}"
        for c in sp.get("cards", []):
            assert c[0] in XM.ICONS, f"{lec['id']}: unknown icon '{c[0]}'"
        if scenes[i]["type"] == "bullets" and "cards" in sp:
            assert len(sp["cards"]) == len(scenes[i]["bullets"]), f"{lec['id']} scene {i}: one card per bullet"


@pytest.mark.parametrize("lec", LECTURES, ids=ids)
def test_rendered_media_is_present(lec):
    vid = lec["id"]
    assert os.path.getsize(os.path.join(CUR, "video", vid + ".jpg")) > 10_000, "missing poster"
    assert os.path.exists(os.path.join(CUR, "img", f"{vid}-board.pdf")), "missing board PDF"
    assert os.path.getsize(os.path.join(CUR, "img", f"{vid}-board.jpg")) > 10_000, "missing board image"
    for voice in VOICES:
        mp4 = media(vid, voice, ".mp4")
        assert os.path.getsize(mp4) > 500_000, f"missing or empty video for the {voice['name']} voice"
        with open(mp4, "rb") as f:
            assert f.read(12)[4:8] == b"ftyp", f"{os.path.basename(mp4)} isn't an MP4"
        assert os.path.getsize(mp4) < 40_000_000, f"{os.path.basename(mp4)} is too large for the site"


@pytest.mark.parametrize("lec", LECTURES, ids=ids)
def test_captions_match_the_current_script(lec):
    """One caption cue per narration line, in order. A mismatch means the script changed and the video wasn't re-rendered."""
    lines = [x for sc in lec["scenes"] for x in sc["lines"]]
    for voice in VOICES:
        with open(media(lec["id"], voice, ".vtt"), encoding="utf8") as f:
            vtt = f.read()
        assert vtt.startswith("WEBVTT")
        times = re.findall(r"(\d+):(\d\d):(\d\d)\.(\d{3}) --> (\d+):(\d\d):(\d\d)\.(\d{3})", vtt)
        assert len(times) == len(lines), (f"{lec['id']} ({voice['name']}): {len(times)} captions for {len(lines)} script lines; "
                                          f"re-render with  python curriculum/build_explainer.py {lec['id']}")
        secs = [(int(a) * 3600 + int(b) * 60 + int(c) + int(d) / 1000, int(e) * 3600 + int(f_) * 60 + int(g) + int(h) / 1000)
                for a, b, c, d, e, f_, g, h in times]
        for (s0, e0), (s1, _) in zip(secs, secs[1:]):
            assert s0 < e0 <= s1 + 0.05, f"{lec['id']} ({voice['name']}): caption times overlap or run backwards"
        cues = [blk.split("\n", 2)[-1].replace("\n", " ").strip() for blk in vtt.split("\n\n") if "-->" in blk]
        for cue, line in zip(cues, lines):
            assert cue[:40] == line[:40], f"{lec['id']} ({voice['name']}): caption '{cue[:50]}…' doesn't match script '{line[:50]}…'"
