"""Render illustrated, off-screen-narrated explainer lectures (storyboards in explainer_scenes.py).

    python curriculum/build_explainer.py m02            # all voices
    python curriculum/build_explainer.py --board m01    # just the board: img/<id>-board.pdf + .jpg (no video)
    CSCI391_VOICES=david python curriculum/build_explainer.py m02

Same outputs as build_videos.py (curriculum/video/<id>[-<voice>].mp4 / .vtt, <id>.jpg), so the site needs no change.
Needs: ffmpeg, Microsoft Edge, and `pip install playwright` (drives the installed Edge; no browser download).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_videos as BV  # noqa: E402  (speech, captions, ffmpeg settings)
import explainer_scenes as XS  # noqa: E402
import explainer_modules as XM  # noqa: E402
import video_scripts as V  # noqa: E402

BOARDS = {**XM.BOARDS, **XS.STORYBOARDS}

FPS = 25
INTRO = 0.8   # seconds of drawing before the first word


def timeline(lec, voice, d):
    items = []
    for scene in lec["scenes"]:
        for line in scene["lines"]:
            say = BV.spoken(line)
            key = hashlib.sha1(f"{voice['engine']}|{say}".encode("utf-8")).hexdigest()[:16]
            items.append({"say": say, "out": os.path.join(d, f"tts_{key}.wav")})
    BV.synthesize(items, voice["engine"])
    audio, cues, scene_starts, t, idx = [BV.silence(INTRO)], [], [], INTRO, 0
    for scene in lec["scenes"]:
        scene_starts.append(t)
        audio.append(BV.silence(BV.LEAD)); t += BV.LEAD
        for li, line in enumerate(scene["lines"]):
            pcm = BV.read_wav(items[idx]["out"]); idx += 1
            dur = len(pcm) / 2 / BV.RATE
            audio.append(pcm); cues.append((t, t + dur, line)); t += dur
            gap = BV.GAP if li < len(scene["lines"]) - 1 else BV.TAIL
            audio.append(BV.silence(gap)); t += gap
    audio.append(BV.silence(3.5)); t += 3.5   # let the last drawing land, then pull back to the whole board
    return b"".join(audio), cues, scene_starts, t


def export_board(page, board, lec, width=2400):
    """The finished board, flat and whole: <id>-board.pdf (the module's printable map) and <id>-board.jpg (its preview)."""
    x0, y0, x1, y1 = board.bbox()
    h = round(width * (y1 - y0) / (x1 - x0))
    page.set_viewport_size({"width": width, "height": h})
    page.evaluate(f"poster({x0}, {y0}, {x1}, {y1}, {width}, {h})")
    page.screenshot(path=os.path.join(BV.IMG, f"{lec['id']}-board.jpg"), type="jpeg", quality=82)
    page.emulate_media(media="screen")
    page.pdf(path=os.path.join(BV.IMG, f"{lec['id']}-board.pdf"), width=f"{width}px", height=f"{h + 2}px", print_background=True,
             margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})


def build(lec, voice, browser, board_only=False):
    d = os.path.join(BV.WORK, "explainer", lec["id"], voice["id"])
    os.makedirs(d, exist_ok=True)
    stem = V.media_stem(lec["id"], voice)
    pcm, cues, starts, total = timeline(lec, voice, d)
    wav_path = os.path.join(d, "narration.wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(BV.RATE); w.writeframes(pcm)
    # captions
    os.makedirs(BV.OUT, exist_ok=True)
    vtt, srt = os.path.join(BV.OUT, f"{stem}.vtt"), os.path.join(d, "captions.srt")
    with open(vtt, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n" + "".join(f"{i}\n{BV.ts(a)} --> {BV.ts(b)}\n{x}\n\n" for i, (a, b, x) in enumerate(cues, 1)))
    with open(srt, "w", encoding="utf-8") as f:
        f.write("".join(f"{i}\n{BV.ts(a, False)} --> {BV.ts(b, False)}\n{x}\n\n" for i, (a, b, x) in enumerate(cues, 1)))
    # storyboard -> page
    board = XS.Board(cues, starts)
    board.lec = lec
    BOARDS[lec["id"]](board)
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    page.goto("file:///" + os.path.join(HERE, "explainer", "engine.html").replace("\\", "/"))
    page.evaluate(f"setup({json.dumps(board.timeline())})")
    if board_only:
        export_board(page, board, lec)
        page.close()
        return total
    # frames -> ffmpeg
    raw = os.path.join(d, "raw.mp4")
    ff = subprocess.Popen([BV.FFMPEG, "-nostdin", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-tune", "animation", "-pix_fmt", "yuv420p", raw], stdin=subprocess.PIPE)
    n = int(total * FPS)
    for i in range(n):
        page.evaluate(f"render({i / FPS:.4f})")
        ff.stdin.write(page.screenshot(type="jpeg", quality=92))
        if i % (FPS * 30) == 0:
            print(f"  {lec['id']} {voice['id']}: {i / FPS:5.0f}s / {total:.0f}s", flush=True)
    ff.stdin.close()
    if ff.wait() != 0:
        raise RuntimeError("ffmpeg failed encoding frames")
    if stem == lec["id"]:
        export_board(page, board, lec)
    page.close()
    # audio + soft subtitles, same as the robot lectures
    aac = os.path.join(d, "narration.aac")
    subprocess.run([BV.FFMPEG, "-nostdin", "-v", "error", "-y", "-i", wav_path, "-c:a", "aac", "-b:a", "64k", aac], check=True, timeout=300)
    final = os.path.join(d, "final.mp4")
    subprocess.run([BV.FFMPEG, "-nostdin", "-v", "error", "-y", "-i", raw, "-i", aac, "-i", srt, "-map", "0:v", "-map", "1:a", "-map", "2:s",
                    "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-movflags", "+faststart", final],
                   check=True, timeout=300)
    shutil.copyfile(final, os.path.join(BV.OUT, f"{stem}.mp4"))
    if stem == lec["id"]:
        poster_t = cues[1][0] + 1.0 if len(cues) > 1 else 4
        subprocess.run([BV.FFMPEG, "-nostdin", "-v", "error", "-y", "-ss", f"{poster_t:.2f}", "-i", final, "-frames:v", "1", "-q:v", "3",
                        os.path.join(BV.OUT, f"{lec['id']}.jpg")], check=True)
    return total


def main():
    from playwright.sync_api import sync_playwright
    if not BV.FFMPEG:
        sys.exit("Need ffmpeg (on PATH or FFMPEG env var).")
    want = [a for a in sys.argv[1:] if not a.startswith("-")] or list(BOARDS)
    board_only = "--board" in sys.argv
    only = os.environ.get("CSCI391_VOICES")
    voices = [v for v in V.VOICES if not only or v["id"] in only.split(",")]
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        for voice in (voices[:1] if board_only else voices):
            for lec in V.LECTURES:
                if lec["id"] in want and lec["id"] in BOARDS:
                    total = build(lec, voice, browser, board_only)
                    print(f"{lec['id']}  {voice['name']:<6} {lec['name']}  {total/60:.1f} min", flush=True)
        browser.close()


if __name__ == "__main__":
    main()
