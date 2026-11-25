"""Encore sprite animation for the lecture videos.

Cuts poses out of curriculum/img/encore-sprites.webp, mirrors them to face the slide, normalizes
their size by helmet width, and renders full-frame (1280x720) transparent overlay frames on demand.

Timeline helpers return [(frame_png, seconds), ...] lists for ffmpeg's concat demuxer.
"""
import os
import random

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SHEET = os.path.join(HERE, "img", "encore-sprites.webp")
W, H = 1280, 720
HEAD_X = 1035          # where the antenna (head centre) sits on screen
BASE = 2.05            # sheet px -> screen px for a standard bust
HELMET = 96            # typical (median-row) helmet width on the sheet

# (x0, y0, x1, y1) on the sheet, reading order; props (bulb, ?, thought bubble) are merged into their pose.
BOXES = {
    "face_smile": (74, 18, 216, 185), "face_grin": (274, 18, 421, 186), "face_happy": (480, 18, 616, 186),
    "face_wink": (673, 18, 810, 186), "face_bright": (890, 18, 1030, 186), "face_squee": (1103, 18, 1241, 186),
    "face_oh": (1320, 18, 1459, 186),
    "wave": (15, 195, 196, 378), "point_up": (241, 195, 407, 376), "shrug": (434, 201, 665, 377),
    "present_low": (672, 200, 848, 376), "thumbs_up": (864, 198, 994, 376), "excited": (1328, 199, 1521, 377),
    "tablet_a": (49, 390, 191, 575), "tablet_b": (250, 389, 394, 574), "chin": (465, 392, 593, 573),
    "arms_crossed": (651, 392, 785, 570), "idea": (832, 389, 999, 575), "cheer": (1035, 389, 1295, 574),
    "hands_together": (1339, 391, 1471, 574),
    "idle": (40, 586, 165, 781), "turn": (257, 586, 355, 787),
    "walk1": (806, 592, 903, 777), "walk2": (938, 592, 1037, 776), "walk3": (1081, 592, 1183, 776),
    "walk4": (1231, 596, 1322, 778), "walk5": (1364, 597, 1471, 778),
    "question": (25, 800, 195, 1003), "thought": (239, 808, 398, 999), "fists": (432, 809, 615, 1002),
    "clasped": (647, 812, 775, 999), "present": (804, 788, 1021, 999), "holo_globe": (1060, 806, 1240, 1000),
    "holo_chart": (1317, 810, 1502, 1002),
}
FACES = ["face_smile", "face_grin", "face_oh", "face_bright"]           # mouth shapes for talking
WALK = ["walk1", "walk2", "walk3", "walk4", "walk5"]


class Encore:
    def __init__(self, cache_dir):
        self.dir = os.path.join(cache_dir, "encore_frames")
        os.makedirs(self.dir, exist_ok=True)
        sheet = Image.open(SHEET).convert("RGBA")
        a = sheet.getchannel("A").point(lambda v: 0 if v < 12 else (255 if v > 235 else v))
        sheet.putalpha(a)
        self.sprites = {}
        for name, (x0, y0, x1, y1) in BOXES.items():
            s = sheet.crop((x0 - 2, y0 - 2, x1 + 3, y1 + 3)).transpose(Image.FLIP_LEFT_RIGHT)  # face the slide
            self.sprites[name] = (s, self._antenna(s), self._helmet(s))

    @staticmethod
    def _antenna(s):
        a = s.getchannel("A").load()
        w, h = s.size
        best = (10**6, w // 2)
        for x in range(int(w * .15), int(w * .8)):
            for y in range(h):
                if a[x, y] > 128:
                    best = min(best, (y, x))
                    break
        return best[1], best[0]

    def _helmet(self, s):
        a = s.getchannel("A").load()
        ax, ay = self._antenna(s)
        widths = []
        for y in range(ay + 30, min(s.size[1], ay + 110)):
            if a[ax, y] <= 128:
                continue
            l = r = ax
            while l > 0 and a[l - 1, y] > 128:
                l -= 1
            while r < s.size[0] - 1 and a[r + 1, y] > 128:
                r += 1
            widths.append(r - l + 1)
        widths.sort()
        w = widths[len(widths) // 2] if widths else HELMET   # median ignores raised arms / props at head height
        return min(max(w, 95), 130)

    def frame(self, pose, dy=0, x=None, walk=False):
        """Path to a cached full-frame RGBA PNG with `pose` drawn in place."""
        key = f"{pose}_{dy}_{x}_{int(walk)}"
        png = os.path.join(self.dir, key + ".png")
        if os.path.exists(png):
            return png
        s, (ax, ay), helm = self.sprites[pose]
        k = 1.75 if walk else BASE * HELMET / helm
        w, h = round(s.width * k), round(s.height * k)
        big = s.convert("RGBa").resize((w, h), Image.LANCZOS).convert("RGBA")
        big = big.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
        cx = HEAD_X if x is None else x
        left = round(cx - ax * k)
        top = (700 - h) if walk else (H - h + dy + 6)       # busts bleed off the bottom edge; walkers stand on stage
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.paste(big, (left, top))     # plain copy onto a transparent canvas keeps alpha exact and clips at the edges
        canvas.save(png, optimize=False, compress_level=1)
        return png

    # ── timeline helpers ──
    def walk_in(self, seconds=1.5, step=0.1):
        out, n = [], int(round(seconds / step))
        for i in range(n):
            x = round(1420 - (1420 - HEAD_X) * (i + 1) / n)
            out.append((self.frame(WALK[i % len(WALK)], x=x, walk=True), step))
        return out

    def hold(self, pose, seconds):
        return [(self.frame(pose), seconds)] if seconds > 0 else []

    def speak(self, pose, seconds, rnd):
        """Talking animation: lip-flap through face sprites, or a speaking bob for a held gesture."""
        out, left, i = [], seconds, 0
        while left > 1e-6:
            step = min(left, rnd.choice([0.09, 0.11, 0.13]))
            if pose == "talk":
                out.append((self.frame(rnd.choice(FACES)), step))
            else:
                out.append((self.frame(pose, dy=[0, 4, 8, 4][i % 4]), step))
            left -= step
            i += 1
        return out

    def rest(self, pose, seconds, rnd):
        if pose == "talk":
            return self.hold("face_happy" if rnd.random() < 0.3 else "face_smile", seconds)
        return self.hold(pose, seconds)


GESTURES = ["talk", "present", "present_low", "point_up", "talk", "holo_chart", "shrug",
            "talk", "thumbs_up", "holo_globe", "excited", "talk", "hands_together", "arms_crossed"]


def choose_pose(scene, si, li, n_scenes, line, salt):
    """Pick a pose that suits the scene and the sentence."""
    last_scene, last_line = si == n_scenes - 1, li == len(scene["lines"]) - 1
    kicker = scene.get("kicker", "") or ""
    if si == 0:
        return "wave" if li == 0 else ("talk" if li % 2 else "present")
    if last_scene and last_line:
        return "cheer" if salt % 2 else "fists"
    if line.rstrip().endswith("?"):
        return "question" if (si + li) % 2 else "thought"
    if "From the field" in kicker:
        return "tablet_a" if li % 2 == 0 else "tablet_b"
    if scene.get("type") == "quote":
        return "idea" if li == 0 else "chin"
    return GESTURES[(salt + si * 3 + li) % len(GESTURES)]


def rng(seed):
    return random.Random(seed)
