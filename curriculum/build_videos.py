"""Render the robot-narrated "Encore Lectures" for each module.

    python curriculum/build_videos.py            # all modules
    python curriculum/build_videos.py m03 m07    # selected modules

Inputs : curriculum/video_scripts.py (anonymized scripts — no student names, voices, or faces)
Outputs: curriculum/video/<id>[-<voice>].mp4  (720p, narration + soft subtitle stream, one per voice)
         curriculum/video/<id>.vtt  (WebVTT captions for the site player)
         curriculum/video/<id>.jpg  (poster frame)

Requirements (Windows): ffmpeg on PATH (or FFMPEG env var), Microsoft Edge (for
rendering slides), and the built-in Windows speech voices (System.Speech).
"""
import hashlib
import html
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import video_scripts as V  # noqa: E402
import encore_sprites as ES  # noqa: E402

OUT = os.path.join(HERE, "video")
IMG = os.path.join(HERE, "img")
WORK = os.path.join(tempfile.gettempdir(), "csci391_video_build")
FFMPEG = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
EDGE = next((p for p in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                         r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"] if os.path.exists(p)), None)
RATE = 22050
GAP = 0.38          # silence between sentences (s)
LEAD, TAIL = 0.7, 0.9  # silence at the start / end of each scene (s)
WALK_IN = 1.5          # Encore walks on stage at the start of each lecture (s)
E = lambda s: html.escape(str(s))  # noqa: E731


# ─────────────────────────── speech ───────────────────────────
PS_TTS = r"""
Add-Type -AssemblyName System.Speech
$items = Get-Content -Raw -Encoding UTF8 $args[0] | ConvertFrom-Json
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
try { $s.SelectVoice($args[1]) } catch { }
$s.Rate = 0
$fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(22050, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
foreach ($it in $items) {
  if (Test-Path $it.out) { continue }
  $s.SetOutputToWaveFile($it.out, $fmt)
  $s.Speak($it.say)
}
$s.SetOutputToNull(); $s.Dispose()
"""

SAY_FIXES = [  # spoken-form fixes so captions stay readable while the voice pronounces things well
    (r"\bHITL\b", "H-I-T-L"), (r"\bHOTL\b", "H-O-T-L"), (r"\bMCP\b", "M-C-P"), (r"\bRAG\b", "rag"),
    (r"\bLLMs\b", "L-L-Ms"), (r"\bLLM\b", "L-L-M"), (r"\bJSON-RPC\b", "jason R-P-C"), (r"\bJSON\b", "jason"),
    (r"\bCUSUM\b", "cue-sum"), (r"3σ", "three sigma"), (r"σ", "sigma"), (r"\bstdio\b", "standard I-O"),
    (r"\bMVP\b", "M-V-P"), (r"\bPII\b", "P-I-I"), (r"\bregex\b", "rej-ex"), (r"\.env\b", "dot env"), (r"\bMBIDs?\b", "M-B-I-Ds"),
    (r"\bHTTPS\b", "H-T-T-P-S"), (r"\bVS Code\b", "V-S Code"), (r"\bUI\b", "U-I"),
    (r"\bReAct\b", "re-act"), (r"\bRLHF\b", "R-L-H-F"), (r"\bSETNX\b", "set-N-X"), (r"\bAPI\b", "A-P-I"),
    (r"\bAPIs\b", "A-P-Is"), (r"\bSSE\b", "S-S-E"), (r"\bBM25\b", "B-M-25"), (r"—", ", "), (r"\$(\d+)", r"\1 dollars"),
]


def spoken(text):
    for pat, rep in SAY_FIXES:
        text = re.sub(pat, rep, text)
    return text


def synthesize(items, engine):
    todo = [it for it in items if not os.path.exists(it["out"])]
    if not todo:
        return
    d = os.path.dirname(todo[0]["out"])          # per-lecture folder, so parallel builds never share these files
    jf = os.path.join(d, "tts.json")
    ps = os.path.join(d, "tts.ps1")
    with open(jf, "w", encoding="utf-8") as f:
        json.dump(todo, f)
    with open(ps, "w", encoding="utf-8") as f:
        f.write(PS_TTS)
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps, jf, engine], check=True)


def read_wav(path):
    with wave.open(path) as w:
        assert w.getframerate() == RATE and w.getsampwidth() == 2 and w.getnchannels() == 1, path
        return w.readframes(w.getnframes())


def silence(sec):
    return b"\x00\x00" * int(RATE * sec)


# ─────────────────────────── visuals ───────────────────────────
def edge_shot(html_text, png, w=1280, h=720, transparent=False):
    page = png[:-4] + ".html"
    with open(page, "w", encoding="utf-8") as f:
        f.write(html_text)
    args = [EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
            f"--user-data-dir={os.path.join(WORK, 'edge-profile')}", f"--window-size={w},{h}",
            f"--screenshot={png}", "file:///" + page.replace("\\", "/")]
    if transparent:
        args.insert(1, "--default-background-color=00000000")
    if os.path.exists(png):
        os.remove(png)
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Edge's launcher can exit before the screenshot is flushed; wait for a stable file.
    last = -1
    for _ in range(150):
        size = os.path.getsize(png) if os.path.exists(png) else -1
        if size > 0 and size == last:
            return
        last = size
        time.sleep(0.2)
    raise RuntimeError("Edge did not render " + page)



SLIDE_CSS = """
*{box-sizing:border-box;margin:0}
body{width:1280px;height:720px;overflow:hidden;font-family:'Segoe UI',Arial,sans-serif;color:#1f1a1c;
 background:radial-gradient(circle at 82% 105%,rgba(255,60,200,.55),transparent 38%),
 radial-gradient(circle at 105% 10%,rgba(80,200,255,.45),transparent 35%),
 radial-gradient(circle at 60% -10%,rgba(150,80,255,.5),transparent 45%),
 linear-gradient(160deg,#120b2e,#2a0d3d 55%,#3b0a2a)}
.beam{position:absolute;bottom:0;width:4px;height:760px;transform-origin:bottom;opacity:.35;
 background:linear-gradient(to top,rgba(255,255,255,.9),transparent)}
.stage{position:absolute;right:0;bottom:0;width:430px;height:60px;
 background:linear-gradient(to top,rgba(255,70,200,.65),transparent);border-top:3px solid #ff4fd8;box-shadow:0 -6px 30px #ff4fd8}
.top{position:absolute;left:44px;top:22px;color:#9ff6ff;font-size:15px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;text-shadow:0 0 10px #5ff3ff}
.top b{color:#ffb347;text-shadow:0 0 10px #ff8a00}
.card{position:absolute;left:44px;top:62px;width:830px;height:556px;background:#fff;border-radius:18px;
 box-shadow:0 0 0 3px rgba(95,243,255,.35),0 18px 50px rgba(0,0,0,.45);padding:40px 46px;overflow:hidden}
.kicker{font-size:15px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#c96500;margin-bottom:10px}
h1{font-size:44px;line-height:1.1;color:#70002e;font-weight:800;margin-bottom:18px}
h2{font-size:34px;line-height:1.15;color:#70002e;font-weight:800;margin-bottom:22px}
ul{list-style:none;padding:0}
li{font-size:25px;line-height:1.35;margin:0 0 16px 0;padding-left:36px;position:relative}
li:before{content:'';position:absolute;left:4px;top:12px;width:14px;height:14px;border-radius:50%;background:#ff8a00;box-shadow:0 0 0 4px #ffe2bf}
.sub{font-size:24px;color:#5b5559;line-height:1.4}
.title .card{display:flex;flex-direction:column;justify-content:center}
.track{display:inline-block;background:#70002e;color:#fff;border-radius:999px;padding:6px 16px;font-size:16px;font-weight:700;letter-spacing:.08em;margin-bottom:22px;align-self:flex-start}
.credit{position:absolute;left:46px;bottom:28px;right:46px;font-size:14px;color:#77707a;border-top:1px solid #eee;padding-top:12px}
.img .card{padding:16px}
.img img{width:100%;height:100%;object-fit:contain}
.quote{font-size:31px;line-height:1.35;color:#70002e;font-weight:700;border-left:8px solid #ff8a00;padding-left:24px}
"""


def beams():
    out = []
    for i, ang in enumerate([-38, -24, -12, 0, 12, 24, 38]):
        out.append(f"<div class='beam' style='left:{1060 + (i - 3) * 14}px;transform:rotate({ang}deg)'></div>")
    return "".join(out)


def slide_html(scene, lec, n):
    kind = scene["type"]
    head = f"<div class='top'>Encore Lectures · <b>{E(lec['track'])}</b> · {E(lec['name'])}</div>"
    if kind == "title":
        body = (f"<div class='card'><span class='track'>{E(lec['track'])} · Module {n}</span>"
                f"<h1>{E(lec['name'])}</h1><p class='sub'>{E(lec['module'])}</p>"
                f"<div class='credit'>Concepts after Thomas R. Caldwell, <i>The Agentic AI Bible</i>, {E(lec['chapters'])} · "
                f"Curriculum &amp; enterprise lens by Addison Boyer · Narrated by Encore, a synthetic lecturer</div></div>")
    elif kind == "bullets":
        lis = "".join(f"<li>{E(b)}</li>" for b in scene["bullets"])
        kick = f"<div class='kicker'>{E(scene['kicker'])}</div>" if scene.get("kicker") else ""
        body = f"<div class='card'>{kick}<h2>{E(scene['heading'])}</h2><ul>{lis}</ul></div>"
    elif kind == "quote":
        kick = f"<div class='kicker'>{E(scene.get('kicker', 'Big idea'))}</div>"
        body = f"<div class='card' style='display:flex;flex-direction:column;justify-content:center'>{kick}<p class='quote'>{E(scene['quote'])}</p></div>"
    elif kind == "image":
        src = "file:///" + os.path.join(IMG, scene["src"]).replace("\\", "/")
        body = f"<div class='card'><img src='{src}'></div>"
    else:
        raise ValueError(kind)
    return f"<html><head><meta charset='utf-8'><style>{SLIDE_CSS}</style></head><body class='{kind if kind in ('title', 'img') else ''}{' img' if kind == 'image' else ''}'>{beams()}<div class='stage'></div>{head}{body}</body></html>"


# ─────────────────────────── assembly ───────────────────────────
def ts(sec, vtt=True):
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}" if vtt else f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


def build(lec, n, enc, voice):
    d = os.path.join(WORK, lec["id"], voice["id"])
    stem = V.media_stem(lec["id"], voice)
    os.makedirs(d, exist_ok=True)
    # 1. speech
    items, idx = [], 0
    for scene in lec["scenes"]:
        for line in scene["lines"]:
            say = spoken(line)
            key = hashlib.sha1(f"{voice['engine']}|{say}".encode("utf-8")).hexdigest()[:16]
            items.append({"say": say, "out": os.path.join(d, f"tts_{key}.wav")})
            idx += 1
    synthesize(items, voice["engine"])
    # 2. timeline
    audio, cues, robot, slides = [], [], [], []
    t, idx = 0.0, 0
    rnd = random.Random(lec["id"])
    salt = int(hashlib.sha1(lec["id"].encode()).hexdigest(), 16) % 97
    n_scenes = len(lec["scenes"])
    for si, scene in enumerate(lec["scenes"]):
        png = os.path.join(d, f"slide_{si:02d}.png")
        edge_shot(slide_html(scene, lec, n), png)
        start = t
        poses = [ES.choose_pose(scene, si, li, n_scenes, line, salt) for li, line in enumerate(scene["lines"])]
        if si == 0:  # Encore walks on stage before the first line
            walk = enc.walk_in(WALK_IN)
            audio.append(silence(WALK_IN)); robot += walk; t += WALK_IN
        audio.append(silence(LEAD)); robot += enc.rest(poses[0], LEAD, rnd); t += LEAD
        for li, line in enumerate(scene["lines"]):
            pcm = read_wav(items[idx]["out"]); idx += 1
            dur = len(pcm) / 2 / RATE
            audio.append(pcm)
            cues.append((t, t + dur, line))
            robot += enc.speak(poses[li], dur, rnd)
            t += dur
            gap = GAP if li < len(scene["lines"]) - 1 else TAIL
            audio.append(silence(gap))
            robot += enc.rest(poses[li + 1] if li + 1 < len(poses) else poses[li], gap, rnd); t += gap
        slides.append((png, t - start))
    wav_path = os.path.join(d, "narration.wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(b"".join(audio))
    # 3. concat lists
    def concat_file(name, entries):
        p = os.path.join(d, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write("ffconcat version 1.0\n")
            for path, dur in entries:
                f.write(f"file '{path.replace(chr(92), '/')}'\nduration {dur:.3f}\n")
            f.write(f"file '{entries[-1][0].replace(chr(92), '/')}'\n")
        return p
    # Repeat each still in short chunks so the fps/overlay filters never starve waiting for the next frame.
    chunked = []
    for png, dur in slides:
        while dur > 1e-6:
            step = min(0.2, dur)
            chunked.append((png, step))
            dur -= step
    slides_txt = concat_file("slides.txt", chunked)
    robot_txt = concat_file("robot.txt", robot)
    # 4. captions
    os.makedirs(OUT, exist_ok=True)
    vtt = os.path.join(OUT, f"{stem}.vtt")
    srt = os.path.join(d, "captions.srt")
    with open(vtt, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, (a, b, text) in enumerate(cues, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{text}\n\n")
    with open(srt, "w", encoding="utf-8") as f:
        for i, (a, b, text) in enumerate(cues, 1):
            f.write(f"{i}\n{ts(a, False)} --> {ts(b, False)}\n{text}\n\n")
    # 5. video
    mp4 = os.path.join(OUT, f"{stem}.mp4")
    raw = os.path.join(d, "raw.mp4")
    # Pass 1: picture only. (Muxing audio + subtitles in the same pass stalls the overlay graph.)
    subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y",
                    "-f", "concat", "-safe", "0", "-i", slides_txt,
                    "-f", "concat", "-safe", "0", "-i", robot_txt,
                    "-filter_complex", "[0:v]fps=25,scale=1280:720,format=yuv420p[bg];[1:v]fps=25,format=rgba[r];[bg][r]overlay=x=0:y=0,format=yuv420p[v]",
                    "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-t", f"{t:.2f}", raw], check=True)
    # Pass 2: encode narration to ADTS AAC. (64k: ffmpeg 9.1 AAC hangs at 96k for 22.05 kHz mono.)
    aac = os.path.join(d, "narration.aac")
    subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y", "-i", wav_path, "-c:a", "aac", "-b:a", "64k", aac],
                   check=True, timeout=300)
    # Pass 3: stream-copy picture + audio + soft English subtitles into a fresh file in the work dir,
    # then copy it into the site. (Encoding while muxing straight into the site folder stalled on Windows.)
    final = os.path.join(d, f"final_{int(time.time())}.mp4")
    subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y", "-i", raw, "-i", aac, "-i", srt,
                    "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c:v", "copy", "-c:a", "copy",
                    "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-movflags", "+faststart", final],
                   check=True, timeout=300)
    shutil.copyfile(final, mp4)
    os.remove(final)
    if stem == lec["id"]:  # one shared poster, taken from the default voice
        subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y", "-ss", "3", "-i", mp4, "-frames:v", "1", "-q:v", "4",
                        os.path.join(OUT, f"{lec['id']}.jpg")], check=True)
    return t


def main():
    if not FFMPEG or not EDGE:
        sys.exit("Need ffmpeg (on PATH or FFMPEG env var) and Microsoft Edge.")
    os.makedirs(WORK, exist_ok=True)
    want = set(sys.argv[1:])
    only = os.environ.get("CSCI391_VOICES")  # e.g. "zira" to render just one voice
    voices = [v for v in V.VOICES if not only or v["id"] in only.split(",")]
    enc = ES.Encore(WORK)
    for voice in voices:
        for n, lec in enumerate(V.LECTURES, 1):
            if want and lec["id"] not in want:
                continue
            dur = build(lec, int(lec["id"][1:]), enc, voice)
            print(f"{lec['id']}  {voice['name']:<6} {lec['track']}  {lec['name']}  {dur/60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
