"""Render a 9:16 scary-story Short from story.json + voice.mp3 + words.json.

Everything visual (phone UI, captions, grain, glitches) and every sound effect
(drone, buzz, knocks, stings) is generated here. No video-generation AI.

Usage: python3 render.py <episode_dir>
  expects <episode_dir>/story.json, voice.mp3, words.json -> writes short.mp4
"""
import json
import os
import re
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FPS, SR = 30, 44100

EP = sys.argv[1]
STORY = json.load(open(os.path.join(EP, "story.json")))
W, H = STORY.get("size", [1080, 1920])  # [1920, 1080] = landscape long-form; default = vertical Short
LAND = W > H
SPEED = float(STORY.get("speed", 1.0))

# ---------- fonts (macOS system fonts) ----------
SUP = "/System/Library/Fonts/Supplemental/"
F_BOLD, F_REG, F_CAP = SUP + "Arial Bold.ttf", SUP + "Arial.ttf", SUP + "Impact.ttf"
F_THIN = "/System/Library/Fonts/HelveticaNeue.ttc"
F_SERIF_B, F_SERIF_I = SUP + "Times New Roman Bold.ttf", SUP + "Times New Roman Italic.ttf"
if not os.path.exists(F_CAP):  # Linux (cloud/CI): Liberation = metric clones of Arial/Times; Anton ~ Impact (fonts/)
    LIB = "/usr/share/fonts/truetype/liberation/"
    F_BOLD, F_REG = LIB + "LiberationSans-Bold.ttf", LIB + "LiberationSans-Regular.ttf"
    F_SERIF_B, F_SERIF_I = LIB + "LiberationSerif-Bold.ttf", LIB + "LiberationSerif-Italic.ttf"
    F_CAP = os.environ.get("CAPTION_FONT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Anton-Regular.ttf"))
    F_THIN = LIB + "LiberationSans-Regular.ttf"


def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.truetype(F_REG, size)


FONT_CLOCK = font(F_THIN, 300, 7 if F_THIN.endswith(".ttc") else 0)
FONT_DATE = font(F_REG, 48)
FONT_NOTE_T = font(F_BOLD, 40)
FONT_NOTE_B = font(F_REG, 40)
FONT_HDR = font(F_BOLD, 50)
FONT_SUB = font(F_REG, 34)
FONT_BUB = font(F_REG, 62)
FONT_CAP = font(F_CAP, 76 if LAND else 104)
FONT_BIG = font(F_CAP, 170)

# ---------- words + anchors ----------
raw = json.load(open(os.path.join(EP, "words.json")))
if isinstance(raw, dict):
    raw = raw.get("words", [])
words, _in_tag = [], False  # drop ElevenLabs delivery tags like [whispering] / [long pause]
for w in raw:
    if w.get("type", "word") != "word" or not w["text"].strip():
        continue
    if w["text"].lstrip().startswith("[") or _in_tag:
        _in_tag = "]" not in w["text"]
        continue
    words.append(w)
for w in words:
    w["start"] = float(w["start"]) / SPEED
    w["end"] = float(w["end"]) / SPEED
    w["clean"] = "".join(c for c in w["text"].lower() if c.isalnum() or c == ":")
VOICE_END = words[-1]["end"]

ANCHOR = re.compile(r"^(?P<tok>[^#+\-]+?)(?:#(?P<n>\d+))?(?P<off>[+\-][\d.]+)?$")


def at(spec, after=0.0):
    """Anchor -> seconds. Number = seconds. 'word', 'word#2' (2nd match),
    'word+0.3' (offset). Words are matched by prefix, searching from `after`."""
    if spec is None:
        return after
    if isinstance(spec, (int, float)):
        return float(spec)
    m = ANCHOR.match(spec.strip().lower())
    if not m:
        raise SystemExit(f"bad anchor: {spec}")
    tok, n, off = m["tok"].strip(), int(m["n"] or 1), float(m["off"] or 0)
    for w in words:
        if w["start"] + max(off, 0) >= after - 1e-6 and w["clean"].startswith(tok):
            n -= 1
            if n == 0:
                return w["start"] + off
    raise SystemExit(f"anchor word not found in voiceover: {spec!r} (after {after:.2f}s)")


# resolve scene start times in order
SCENES = STORY["scenes"]
prev = 0.0
for i, s in enumerate(SCENES):
    s["_t"] = 0.0 if i == 0 else at(s.get("start"), prev)
    prev = s["_t"]
for i, s in enumerate(SCENES):
    s["_end"] = SCENES[i + 1]["_t"] if i + 1 < len(SCENES) else 1e9

DUR = VOICE_END + float(STORY.get("tail", 2.8))
NFRAMES = int(DUR * FPS)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def prog(t, start, length=0.35):
    return ease((t - start) / length)


# effects: resolve all anchors once
def resolve_list(key):
    return [at(a) for a in STORY.get(key, [])]


GLITCH = resolve_list("glitch")
SHAKE = resolve_list("shake")
SFX = [(e["type"], at(e["at"]) + float(e.get("delay", 0))) for e in STORY.get("sfx", [])]
HEAVY_SHAKE = [t for k, t in SFX if k == "knock"]
SILENCE_FROM = at(STORY["silence_from"]) if STORY.get("silence_from") else None

# ---------- captions ----------
chunks, cur = [], []
for w in words:
    cur.append(w)
    nxt = words[words.index(w) + 1] if words.index(w) + 1 < len(words) else None
    if len(cur) == 3 or w["text"].rstrip()[-1:] in ".?!,:\"" or (nxt and nxt.get("speaker") != w.get("speaker")):
        chunks.append(cur)
        cur = []
if cur:
    chunks.append(cur)


def caption_at(t):
    for c in chunks:
        if c[0]["start"] - 0.05 <= t <= c[-1]["end"] + 0.25:
            return c
    return None


# ---------- reusable layers ----------
rng = np.random.default_rng(7)
GRAIN = [rng.normal(0, 14, (H // 2, W // 2)).astype(np.float32) for _ in range(8)]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
rr = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIGNETTE = np.clip(1.15 - float(STORY.get("vignette", 0.75)) * rr ** 1.6, 0.0, 1.0)[..., None]


def wallpaper():
    g = np.zeros((H, W, 3), np.float32)
    g[..., 0] = 8 + 10 * (yy / H)
    g[..., 1] = 10 + 14 * (yy / H)
    g[..., 2] = 22 + 30 * (yy / H)
    glow = np.exp(-(((xx - W / 2) / 260) ** 2) - (((yy - H * 0.93) / 30) ** 2))
    g += glow[..., None] * np.array([70, 55, 30], np.float32)
    return Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))


WALL = wallpaper()


def centered(d, y, text, fnt, fill):
    d.text(((W - d.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)


def wrap(d, text, fnt, maxw):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if d.textlength(test, font=fnt) <= maxw:
            line = test
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


# ---------- scene types ----------
def s_lock(s, t):
    img = WALL.copy()
    d = ImageDraw.Draw(img)
    red = prog(t, at(s["red_at"], s["_t"]), 1.0) if s.get("red_at") else 0.0
    centered(d, 230, s.get("date", "Tuesday, October 31"), FONT_DATE, (200, 205, 220))
    centered(d, 290, s.get("clock", "3:00"), FONT_CLOCK,
             (235, int(235 - 160 * red), int(240 - 170 * red)))
    if s.get("note_from"):
        nt = at(s.get("note_at"), s["_t"])
        if t >= nt:
            p = prog(t, nt, 0.4)
            y, a = 760 - int(120 * (1 - p)), int(215 * p)
            layer = Image.new("RGBA", (W, H))
            ld = ImageDraw.Draw(layer)
            ld.rounded_rectangle((60, y, W - 60, y + 190), 42, fill=(40, 42, 52, a))
            ld.ellipse((95, y + 45, 175, y + 125), fill=(70, 190, 90, a))
            ld.text((205, y + 40), s["note_from"], font=FONT_NOTE_T, fill=(255, 255, 255, a))
            ld.text((W - 210, y + 42), "now", font=FONT_SUB, fill=(170, 170, 180, a))
            ld.text((205, y + 100), s.get("note_body", ""), font=FONT_NOTE_B, fill=(220, 220, 228, a))
            img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    return img


def s_chat(s, t):
    img = Image.new("RGB", (W, H), (6, 6, 9))
    d = ImageDraw.Draw(img)
    contact = s.get("contact", "Mom")
    d.rectangle((0, 0, W, 250), fill=(22, 22, 28))
    d.ellipse((W / 2 - 50, 50, W / 2 + 50, 150), fill=(90, 90, 105))
    centered(d, 75, contact[:1].upper(), FONT_HDR, (230, 230, 235))
    centered(d, 160, contact, FONT_HDR, (240, 240, 245))
    typing = None
    for ty in s.get("typing", []):
        a0, a1 = at(ty["from"], s["_t"]), at(ty["to"], s["_t"]) if ty.get("to") else s["_end"]
        if a0 <= t < a1:
            typing = True
    centered(d, 215, "typing..." if typing else s.get("status", "online"), FONT_SUB, (130, 135, 150))
    y = 520
    for b in s.get("bubbles", []):
        ba = at(b.get("at"), s["_t"]) if b.get("at") else 0.0
        if t < ba:
            continue
        p = prog(t, ba, 0.25)
        lines = wrap(d, b["text"], FONT_BUB, 620)
        bw = max(d.textlength(l, font=FONT_BUB) for l in lines) + 70
        bh = 66 * len(lines) + 44
        mine = b.get("mine", False)
        x0 = W - 60 - bw if mine else 60
        off = int(40 * (1 - p))
        fill = tuple(b["color"]) if b.get("color") else ((10, 132, 255) if mine else (44, 44, 52))
        d.rounded_rectangle((x0, y + off, x0 + bw, y + bh + off), 40, fill=fill)
        for i, l in enumerate(lines):
            d.text((x0 + 35, y + 22 + 66 * i + off), l, font=FONT_BUB, fill=(255, 255, 255))
        y += bh + 34
    if typing:
        d.rounded_rectangle((60, y, 250, y + 110), 40, fill=(44, 44, 52))
        for i in range(3):
            ph = (t * 3.2 - i * 0.33) % 1.0
            v = 120 + int(120 * max(0, np.sin(ph * np.pi)))
            cx = 105 + i * 50
            d.ellipse((cx - 14, y + 41, cx + 14, y + 69), fill=(v, v, v))
    return img


def s_card(s, t):
    """Fading memorial/info card: avatar letter, title, sub-lines."""
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    c = int(220 * prog(t, s["_t"], 1.2))
    if s.get("avatar"):
        d.ellipse((W / 2 - 110, 560, W / 2 + 110, 780), outline=(c, c, c), width=4)
        centered(d, 610, s["avatar"], font(F_BOLD, 120), (c, c, c))
    centered(d, 840, s.get("title", ""), font(F_BOLD, 80), (c, c, c))
    for i, line in enumerate(s.get("lines", [])):
        f = FONT_DATE if i == 0 else FONT_SUB
        centered(d, 950 + i * 80, line, f, (int(c * (0.7 - 0.15 * i)),) * 3)
    return img


def s_title(s, t):
    """Big red words stacking in on anchors, plus optional white footer."""
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    lines = s.get("lines", [])
    y0 = 830 - 95 * len(lines)
    for i, ln in enumerate(lines):
        if t >= at(ln.get("at"), s["_t"]) + float(ln.get("delay", 0)):
            centered(d, y0 + i * 190, ln["text"], FONT_BIG, tuple(s.get("color", (200, 20, 20))))
    f = s.get("footer")
    if f and t >= at(f.get("at"), s["_t"]) + float(f.get("delay", 0)):
        centered(d, y0 + len(lines) * 190 + 80, f["text"], font(F_BOLD, 64), (230, 230, 230))
    return img


# ---------- animated scenes ----------
def flicker_at(t, seed=0.0):
    """1.0 normally, dips toward dark for a few frames now and then (deterministic)."""
    v = np.sin(t * 13.1 + seed) + np.sin(t * 7.7 + 2 * seed) + np.sin(t * 29.3)
    return 0.25 if v > 2.3 else (0.7 if v > 2.0 else 1.0)


def big_lines(d, s, t):
    y0 = int(s.get("title_y", 1230))
    for i, ln in enumerate(s.get("title_lines", [])):
        if t >= at(ln.get("at"), s["_t"]) + float(ln.get("delay", 0)):
            txt = ln["text"]
            d.text(((W - d.textlength(txt, font=FONT_BIG)) / 2, y0 + i * 180), txt, font=FONT_BIG,
                   fill=(215, 20, 20), stroke_width=10, stroke_fill=(0, 0, 0))


def hallway_base(s):
    if "_base" in s:
        return s["_base"], s["_geo"]
    BW, BH = 1404, 2496
    img = Image.new("RGB", (BW, BH), (0, 0, 0))
    d = ImageDraw.Draw(img)
    vx, vy, iw, ih = BW / 2, BH * 0.47, 300, 520
    inner = (vx - iw / 2, vy - ih * 0.55, vx + iw / 2, vy + ih * 0.45)
    outer = (0, 0, BW, BH)

    def rect(f):
        return tuple(o + (i - o) * f for o, i in zip(outer, inner))

    N = 28
    for k in range(N):
        f0, f1 = (k / N) ** 0.55, ((k + 1) / N) ** 0.55
        a, b = rect(f0), rect(f1)
        sh = 0.18 + 0.82 * (1 - k / N) ** 1.3
        col = lambda c: tuple(int(v * sh) for v in c)
        d.polygon([(a[0], a[3]), (a[2], a[3]), (b[2], b[3]), (b[0], b[3])], fill=col((70, 50, 38)))
        d.polygon([(a[0], a[1]), (a[2], a[1]), (b[2], b[1]), (b[0], b[1])], fill=col((34, 33, 36)))
        d.polygon([(a[0], a[1]), (b[0], b[1]), (b[0], b[3]), (a[0], a[3])], fill=col((58, 62, 64)))
        d.polygon([(a[2], a[1]), (b[2], b[1]), (b[2], b[3]), (a[2], a[3])], fill=col((52, 56, 58)))
    for j in range(-7, 8):  # floor boards
        d.line([(vx + j * BW / 7, BH), (vx + j * iw / 14, inner[3])], fill=(20, 14, 10), width=3)
    for f0, f1, left in ((0.30, 0.42, True), (0.52, 0.60, False), (0.70, 0.76, True)):  # side doors
        a, b = rect(f0 ** 0.55), rect(f1 ** 0.55)
        x0, x1 = (a[0], b[0]) if left else (a[2], b[2])
        top0, top1 = a[1] + (a[3] - a[1]) * 0.22, b[1] + (b[3] - b[1]) * 0.22
        d.polygon([(x0, top0), (x1, top1), (x1, b[3]), (x0, a[3])], fill=(14, 11, 9))
    d.rectangle(inner, fill=(7, 7, 9))
    dw, dh = iw * 0.5, ih * 0.8
    dx0, dy1 = vx - dw / 2, inner[3]
    d.rectangle((dx0, dy1 - dh, dx0 + dw, dy1), fill=(30, 22, 17))
    d.line([(dx0 + 4, dy1 - 2), (dx0 + dw - 4, dy1 - 2)], fill=(255, 190, 110), width=4)
    lr = rect(0.45 ** 0.55)
    lx, ly = vx, lr[1] + 18
    d.ellipse((lx - 46, ly - 12, lx + 46, ly + 12), fill=(255, 240, 200))
    a = np.asarray(img).astype(np.float32)
    gy, gx = np.mgrid[0:BH, 0:BW].astype(np.float32)
    glow = np.exp(-((gx - lx) ** 2 + ((gy - ly) * 0.8) ** 2) / (2 * 420.0 ** 2))
    a += glow[..., None] * np.array([120, 100, 70], np.float32)
    s["_base"] = np.clip(a, 0, 255).astype(np.uint8)
    s["_geo"] = dict(vx=vx, vy=vy, inner=inner, outer=outer, BW=BW, BH=BH, rect=rect)
    return s["_base"], s["_geo"]


def draw_figure(d, cx, foot, h, alpha, eyes=0.0, color=(2, 2, 3)):
    """Tall thin silhouette with long arms; eyes glow red when eyes > 0. color=(230,190,40) = yellow raincoat."""
    w, c = h * 0.26, tuple(color) + (int(255 * alpha),)
    hr = h * 0.075
    d.ellipse((cx - hr, foot - h, cx + hr, foot - h + 2.3 * hr), fill=c)
    d.polygon([(cx - w * 0.5, foot - h * 0.8), (cx + w * 0.5, foot - h * 0.8),
               (cx + w * 0.32, foot), (cx - w * 0.32, foot)], fill=c)
    for sgn in (-1, 1):  # arms hanging to the knees
        d.polygon([(cx + sgn * w * 0.5, foot - h * 0.8), (cx + sgn * w * 0.62, foot - h * 0.78),
                   (cx + sgn * w * 0.66, foot - h * 0.25), (cx + sgn * w * 0.55, foot - h * 0.25)], fill=c)
    if eyes > 0:
        e = int(255 * eyes * alpha)
        for sgn in (-1, 1):
            ex, ey, r = cx + sgn * hr * 0.38, foot - h + hr * 1.0, max(2, hr * 0.1)
            d.ellipse((ex - r * 2.5, ey - r * 2.5, ex + r * 2.5, ey + r * 2.5), fill=(120, 0, 0, e // 3))
            d.ellipse((ex - r, ey - r, ex + r, ey + r), fill=(255, 40, 30, e))


def s_hallway(s, t):
    """Perspective corridor: slow dolly, flickering light, figure at the far end that approaches."""
    base, g = hallway_base(s)
    img = Image.fromarray(base).convert("RGBA")
    fa = at(s.get("figure_at"), s["_t"]) if s.get("figure_at") else None
    if fa is not None and t >= fa:
        appr = at(s["approach_at"], s["_t"]) if s.get("approach_at") else 1e9
        f = 1.0 - 0.32 * ease((t - appr) / 4.0) if t >= appr else 1.0
        r = g["rect"](f ** 0.55)
        h = (r[3] - r[1]) * 0.66
        eyes = prog(t, at(s["eyes_at"], s["_t"]), 0.6) if s.get("eyes_at") else 0.0
        layer = Image.new("RGBA", img.size)
        draw_figure(ImageDraw.Draw(layer), g["vx"], r[3] - 4, h, prog(t, fa, 1.2), eyes)
        img = Image.alpha_composite(img, layer.filter(ImageFilter.GaussianBlur(3)))
    dur = max(0.5, min(s["_end"], DUR) - s["_t"])
    z = 1.0 + float(s.get("dolly", 0.25)) * ((t - s["_t"]) / dur)
    cw, ch = g["BW"] / z, g["BH"] / z
    x0 = min(max(0, g["vx"] - cw / 2), g["BW"] - cw)
    y0 = min(max(0, g["vy"] - ch * 0.47), g["BH"] - ch)
    img = img.convert("RGB").crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)
    big_lines(ImageDraw.Draw(img), s, t)
    if s.get("flicker", True):
        fl = flicker_at(t)
        if fl < 1:
            img = Image.fromarray((np.asarray(img).astype(np.float32) * fl).astype(np.uint8))
    return img


DOOR = (250, 430, 830, 1690)


def door_base():
    if "base" in DOOR_CACHE:
        return DOOR_CACHE["base"], DOOR_CACHE["glow"]
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(0, H, 8):
        v = 20 - 12 * y / H
        d.rectangle((0, y, W, y + 8), fill=(int(v), int(v * 0.9), int(v * 1.1)))
    x0, y0, x1, y1 = DOOR
    d.rectangle((x0 - 24, y0 - 24, x1 + 24, y1), fill=(30, 26, 24))
    d.rectangle(DOOR, fill=(54, 40, 30))
    pw, ph = (x1 - x0 - 90) / 2, (y1 - y0 - 120) / 3
    for cx in range(2):
        for cy in range(3):
            px, py = x0 + 30 + cx * (pw + 30), y0 + 30 + cy * (ph + 30)
            d.rectangle((px, py, px + pw, py + ph), outline=(36, 26, 19), width=7)
    d.rectangle((0, y1, W, H), fill=(13, 10, 8))
    base = np.asarray(img).astype(np.float32)
    yy2, xx2 = np.mgrid[0:H, 0:W].astype(np.float32)
    xmask = 1 / (1 + np.exp(-(xx2 - x0 - 12) / 6)) * 1 / (1 + np.exp((xx2 - x1 + 12) / 6))
    down = np.where(yy2 >= y1, np.exp(-(yy2 - y1) / 70), 0)
    up = np.where(yy2 < y1, np.exp(-(y1 - yy2) / 18) * 0.35, 0)
    strip = np.where((yy2 >= y1) & (yy2 < y1 + 12), 1.0, 0)
    glow = (np.maximum(down * 0.75, strip) + up) * xmask
    DOOR_CACHE["base"], DOOR_CACHE["glow"] = base, glow[..., None] * np.array([255, 185, 105], np.float32)
    return DOOR_CACHE["base"], DOOR_CACHE["glow"]


DOOR_CACHE = {}


def s_door(s, t):
    """Bedroom door at night: light under it, feet shadows, turning handle, creaking open, eyes."""
    base, glow = door_base()
    x0, y0, x1, y1 = DOOR
    cols = np.ones(W, np.float32)
    if s.get("shadows_at") and t >= at(s["shadows_at"], s["_t"]):
        k = prog(t, at(s["shadows_at"], s["_t"]), 0.8)
        fx = 470 + 25 * np.sin(t * 0.8)
        xs = np.arange(W, dtype=np.float32)
        for c in (fx, fx + 150):
            cols -= 0.92 * k * np.exp(-((xs - c) / 38) ** 4)
    a = base + glow * np.clip(cols, 0.05, 1)[None, :, None]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    hx, hy = 780, 1080
    ang = 0.0
    if s.get("handle_at") and t >= at(s["handle_at"], s["_t"]):
        ht = at(s["handle_at"], s["_t"])
        ang = 38 * ease((t - ht) / 1.5) + (4 * np.sin(t * 40) if t - ht < 2.5 else 0)
    th = np.radians(ang)  # lever points left, swings down as it turns
    ex, ey = hx - 85 * np.cos(th), hy + 85 * np.sin(th)
    nx, ny = np.sin(th) * 9, np.cos(th) * 9
    d.polygon([(hx + nx, hy + ny), (ex + nx, ey + ny), (ex - nx, ey - ny), (hx - nx, hy - ny)], fill=(150, 128, 88))
    d.ellipse((hx - 24, hy - 24, hx + 24, hy + 24), fill=(165, 142, 98))
    if s.get("open_at") and t >= at(s["open_at"], s["_t"]):
        gap = 150 * ease((t - at(s["open_at"], s["_t"])) / 2.5)
        d.rectangle((x1 - gap, y0, x1, y1), fill=(2, 2, 3))
        if s.get("eyes_at") and t >= at(s["eyes_at"], s["_t"]) and gap > 40:
            e = prog(t, at(s["eyes_at"], s["_t"]), 0.5)
            blink = 0 if (t * 0.9) % 3.0 < 0.12 else 1
            for sgn in (-1, 1):
                ex2, ey2 = x1 - gap / 2 + sgn * 18, 930
                d.ellipse((ex2 - 18, ey2 - 18, ex2 + 18, ey2 + 18), fill=(int(90 * e), 0, 0))
                if blink:
                    d.ellipse((ex2 - 7, ey2 - 5, ex2 + 7, ey2 + 5), fill=(int(255 * e), int(40 * e), 30))
    big_lines(d, s, t)
    return img


# rain overlay (any scene with "rain": true)
RAIN = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(40, 110), rng.uniform(1600, 2600)) for _ in range(170)]


def add_rain(img, t):
    layer = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(layer)
    for x, y, ln, sp in RAIN:
        yy_ = (y + sp * t) % (H + 200) - 100
        xx_ = x - 0.12 * (yy_ % H)
        d.line([(xx_, yy_), (xx_ - ln * 0.12, yy_ + ln)], fill=(170, 180, 200, 70), width=2)
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


# ---------- bright / colorful animated scenes ----------
_GK = {}


def add_glow(a, cx, cy, r, color, k=1.0):
    """Additive soft light blob onto float array a (H, W, 3)."""
    if k <= 0:
        return
    r = int(r)
    if r not in _GK:
        gy_, gx_ = np.mgrid[-2 * r:2 * r + 1, -2 * r:2 * r + 1].astype(np.float32)
        _GK[r] = np.exp(-(gx_ ** 2 + gy_ ** 2) / (2 * (r * 0.6) ** 2))
    g = _GK[r]
    x0, y0 = int(cx) - 2 * r, int(cy) - 2 * r
    xa, ya = max(0, x0), max(0, y0)
    xb, yb = min(a.shape[1], x0 + g.shape[1]), min(a.shape[0], y0 + g.shape[0])
    if xa < xb and ya < yb:
        a[ya:yb, xa:xb] += g[ya - y0:yb - y0, xa - x0:xb - x0, None] * np.array(color, np.float32) * k


def vgrad(a, y0, y1, c0, c1):
    t_ = np.linspace(0, 1, y1 - y0, dtype=np.float32)[:, None, None]
    a[y0:y1] = np.array(c0, np.float32) * (1 - t_) + np.array(c1, np.float32) * t_


PAL = {
    "day": dict(sky=((92, 152, 228), (196, 222, 244)), ground=((96, 158, 84), (58, 118, 56)),
                wall=(234, 230, 216), roof=(118, 76, 60), trim=(250, 250, 246), door=(140, 46, 46),
                win=(150, 192, 224), road=(128, 128, 134), tree=(52, 118, 58), trunk=(96, 66, 46),
                cloud=(255, 255, 255), ck=0.55, lit=0.0),
    "dusk": dict(sky=((62, 46, 118), (252, 156, 96)), ground=((62, 84, 58), (34, 48, 36)),
                 wall=(186, 150, 156), roof=(78, 52, 62), trim=(222, 206, 212), door=(104, 38, 44),
                 win=(70, 70, 104), road=(84, 78, 88), tree=(40, 58, 46), trunk=(56, 42, 38),
                 cloud=(255, 176, 160), ck=0.4, lit=0.75),
    "night": dict(sky=((10, 12, 36), (40, 52, 100)), ground=((20, 34, 28), (10, 15, 12)),
                  wall=(70, 76, 104), roof=(30, 30, 44), trim=(120, 126, 150), door=(52, 28, 34),
                  win=(34, 38, 58), road=(34, 36, 46), tree=(14, 26, 20), trunk=(20, 18, 20),
                  cloud=(100, 106, 140), ck=0.16, lit=1.0),
}
MAIN = dict(body=(250, 760, 830, 1180), roof=[(205, 770), (540, 470), (875, 770)], attic=(540, 640, 46),
            up=[(320, 820, 450, 960), (630, 820, 760, 960)], down=[(300, 1010, 440, 1130), (640, 1010, 780, 1130)],
            door=(490, 1000, 590, 1180), porch=(616, 1030))
NEIGH = [dict(body=(-170, 880, 190, 1180), roof=[(-200, 890), (10, 700), (222, 890)],
              wins=[(-60, 940, 40, 1030), (90, 940, 160, 1030)], porch=(160, 1080)),
         dict(body=(890, 880, 1250, 1180), roof=[(858, 890), (1070, 700), (1282, 890)],
              wins=[(920, 940, 990, 1030), (1040, 940, 1140, 1030)], porch=(920, 1080))]
HOUSE_CACHE = {}


def house_base(time_):
    if time_ in HOUSE_CACHE:
        return HOUSE_CACHE[time_]
    p = PAL[time_]
    a = np.zeros((H, W, 3), np.float32)
    vgrad(a, 0, 1180, *p["sky"])
    vgrad(a, 1180, H, *p["ground"])
    if time_ == "night":
        r_ = np.random.default_rng(3)
        for _ in range(140):
            x_, y_ = int(r_.uniform(0, W)), int(r_.uniform(0, 1000))
            a[y_:y_ + 3, x_:x_ + 3] = r_.uniform(140, 255)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 1560, W, 1730), fill=p["road"])
    for x_ in range(0, W, 160):
        d.rectangle((x_ + 40, 1638, x_ + 110, 1650), fill=tuple(min(255, c + 60) for c in p["road"]))
    d.polygon([(495, 1180), (585, 1180), (640, 1560), (440, 1560)], fill=tuple(int(c * 0.8) for c in p["trim"]))
    for n in NEIGH:
        d.rectangle(n["body"], fill=tuple(int(c * 0.82) for c in p["wall"]))
        d.polygon(n["roof"], fill=tuple(int(c * 0.85) for c in p["roof"]))
        for w_ in n["wins"]:
            d.rectangle(w_, fill=p["win"], outline=p["trim"], width=6)
    b = MAIN["body"]
    d.rectangle(b, fill=p["wall"])
    d.polygon(MAIN["roof"], fill=p["roof"])
    d.line(MAIN["roof"], fill=p["trim"], width=10)
    ax, ay, ar = MAIN["attic"]
    d.ellipse((ax - ar - 8, ay - ar - 8, ax + ar + 8, ay + ar + 8), fill=p["trim"])
    d.ellipse((ax - ar, ay - ar, ax + ar, ay + ar), fill=p["win"])
    for w_ in MAIN["up"] + MAIN["down"]:
        d.rectangle((w_[0] - 10, w_[1] - 10, w_[2] + 10, w_[3] + 10), fill=p["trim"])
        d.rectangle(w_, fill=p["win"])
    d.rectangle((470, 972, 612, 992), fill=p["trim"])
    d.rectangle(MAIN["door"], fill=p["door"])
    d.ellipse((570, 1085, 580, 1095), fill=(220, 190, 120))
    d.rectangle((476, 1180, 604, 1200), fill=p["trim"])
    HOUSE_CACHE[time_] = np.asarray(img).astype(np.float32)
    return HOUSE_CACHE[time_]


def fill_win(a, box, color, k):
    x0, y0, x1, y1 = [int(v) for v in box]
    x0, x1 = max(0, x0), min(W, x1)
    if k > 0 and x0 < x1:
        a[y0:y1, x0:x1] = a[y0:y1, x0:x1] * (1 - k) + np.array(color, np.float32) * k


def s_house(s, t):
    """House on the street, day/dusk/night: drifting clouds, swaying trees, porch light, attic,
    a waving figure upstairs, neighbors standing on their lawns, front door opening."""
    tm = s.get("time", "night")
    p = PAL[tm]
    a = house_base(tm).copy()
    for k in range(3):
        cx = (180 + k * 420 + t * 16 * (1 + 0.4 * k)) % 1500 - 200
        cy = 170 + k * 120
        for dx in (-95, 0, 95):
            add_glow(a, cx + dx, cy + (14 if dx else 0), 95 + 15 * k, p["cloud"], p["ck"])
    if tm == "night":
        add_glow(a, 860, 250, 70, (210, 220, 255), 0.7)
        a[226:274, 836:884] = np.maximum(a[226:274, 836:884], 230)
    lit = p["lit"] * float(s.get("lights", 1.0))
    warm = (255, 198, 112)
    for w_ in MAIN["up"] + MAIN["down"]:
        fill_win(a, w_, warm, 0.85 * lit)
        if lit:
            add_glow(a, (w_[0] + w_[2]) / 2, (w_[1] + w_[3]) / 2, 90, warm, 0.18 * lit)
    for n in NEIGH:
        for w_ in n["wins"]:
            fill_win(a, w_, warm, 0.7 * lit)
        add_glow(a, *n["porch"], 85, (255, 200, 120), 0.75 * p["lit"])
    porch = float(s.get("porch", 1.0))
    if s.get("porch_off_at"):
        po = at(s["porch_off_at"], s["_t"])
        if t >= po:
            porch = (1.0 if np.sin((t - po) * 47) > 0 else 0.15) if t - po < 0.9 else 0.0
    px, py = MAIN["porch"]
    a[py - 9:py + 9, px - 7:px + 7] = np.array((255, 236, 180), np.float32) * (0.3 + 0.7 * porch)
    add_glow(a, px, py, 120, (255, 205, 130), (0.95 if p["lit"] else 0.25) * porch)
    if s.get("attic_glow_at") and t >= at(s["attic_glow_at"], s["_t"]):
        k = prog(t, at(s["attic_glow_at"], s["_t"]), 0.8)
        ax, ay, ar = MAIN["attic"]
        yy_, xx_ = np.ogrid[ay - ar:ay + ar, ax - ar:ax + ar]
        m = ((xx_ - ax) ** 2 + (yy_ - ay) ** 2) < ar ** 2
        reg = a[ay - ar:ay + ar, ax - ar:ax + ar]
        reg[m] = reg[m] * (1 - 0.8 * k) + np.array((255, 110, 60), np.float32) * 0.8 * k
        add_glow(a, ax, ay, 80, (255, 90, 40), 0.35 * k)
    if s.get("door_open_at") and t >= at(s["door_open_at"], s["_t"]):
        k = ease((t - at(s["door_open_at"], s["_t"])) / 1.5)
        x0, y0, x1, y1 = MAIN["door"]
        fill_win(a, (x1 - (x1 - x0) * k, y0, x1, y1), (255, 196, 120), 0.95)
        add_glow(a, x1 - 20, (y0 + y1) / 2, 110, (255, 190, 110), 0.5 * k)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    layer = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(layer)
    eyes = prog(t, at(s["eyes_at"], s["_t"]), 0.6) if s.get("eyes_at") else 0.0
    if s.get("attic_figure_at") and t >= at(s["attic_figure_at"], s["_t"]):
        al = prog(t, at(s["attic_figure_at"], s["_t"]), 1.0)
        ax, ay, ar = MAIN["attic"]
        d.ellipse((ax - 15, ay - 30, ax + 15, ay + 2), fill=(5, 5, 8, int(255 * al)))
        d.chord((ax - 38, ay - 4, ax + 38, ay + 70), 180, 360, fill=(5, 5, 8, int(255 * al)))
    if s.get("wave_at") and t >= at(s["wave_at"], s["_t"]):
        al = prog(t, at(s["wave_at"], s["_t"]), 0.8)
        x0, y0, x1, y1 = MAIN["up"][0]
        cx_, c = (x0 + x1) / 2, (5, 5, 8, int(255 * al))
        d.ellipse((cx_ - 16, y0 + 30, cx_ + 16, y0 + 64), fill=c)
        d.rectangle((cx_ - 28, y0 + 64, cx_ + 28, y1), fill=c)
        ang = np.radians(40 + 30 * np.sin(t * 7))
        d.line([(cx_ + 24, y0 + 72), (cx_ + 24 + 60 * np.sin(ang), y0 + 72 - 60 * np.cos(ang))], fill=c, width=12)
    if s.get("neighbors_at") and t >= at(s["neighbors_at"], s["_t"]):
        al = prog(t, at(s["neighbors_at"], s["_t"]), 1.2)
        for i, (x_, f_, h_) in enumerate(((60, 1400, 300), (190, 1470, 330), (900, 1470, 330),
                                          (1030, 1400, 300), (330, 1830, 420), (780, 1850, 430))):
            draw_figure(d, x_, f_, h_, al * (0.85 if i < 4 else 1.0), eyes)
    img = Image.alpha_composite(img, layer.filter(ImageFilter.GaussianBlur(1.6)))
    d = ImageDraw.Draw(img)
    for k, tx in enumerate((-30, 1110)):  # foreground trees, swaying
        sw = 12 * np.sin(t * 1.2 + k * 2)
        d.polygon([(tx - 26, H), (tx + 26, H), (tx + 18 + sw * 0.3, 1320), (tx - 18 + sw * 0.3, 1320)], fill=p["trunk"])
        for dx, dy, r_ in ((0, 0, 190), (-110, 90, 140), (110, 80, 150), (0, -140, 150)):
            cx_, cy_ = tx + dx + sw, 1250 + dy
            d.ellipse((cx_ - r_, cy_ - r_, cx_ + r_, cy_ + r_), fill=p["tree"])
    big_lines(d, s, t)
    return img.convert("RGB")


ROOM_CACHE = {}


def room_bases():
    if ROOM_CACHE:
        return ROOM_CACHE["lit"], ROOM_CACHE["dark"]
    a = np.zeros((H, W, 3), np.float32)
    vgrad(a, 0, 260, (150, 108, 76), (176, 132, 94))
    vgrad(a, 260, 1450, (214, 170, 120), (162, 114, 76))
    vgrad(a, 1450, H, (126, 82, 52), (84, 52, 34))
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.line([(0, 260), (W, 260)], fill=(110, 76, 52), width=8)
    d.rectangle((0, 1430, W, 1452), fill=(232, 220, 200))
    for x_ in range(-200, W + 200, 150):
        d.line([(x_, H), (x_ + (x_ - W / 2) * -0.25, 1452)], fill=(70, 44, 28), width=3)
    d.rectangle((84, 414, 436, 906), fill=(236, 226, 206))
    d.rectangle((102, 432, 418, 888), fill=(36, 54, 104))
    d.ellipse((300, 486, 368, 554), fill=(226, 230, 244))
    d.line([(260, 432), (260, 888)], fill=(236, 226, 206), width=12)
    d.line([(102, 660), (418, 660)], fill=(236, 226, 206), width=12)
    d.polygon([(40, 380), (150, 380), (126, 980), (30, 980)], fill=(156, 52, 46))
    d.polygon([(370, 380), (480, 380), (490, 980), (394, 980)], fill=(156, 52, 46))
    d.rectangle((596, 476, 774, 684), fill=(70, 46, 30))
    d.rectangle((612, 492, 758, 668), fill=(160, 200, 236))
    d.rectangle((640, 580, 730, 668), fill=(240, 236, 226))
    d.polygon([(628, 584), (685, 530), (742, 584)], fill=(120, 76, 60))
    d.rectangle((250, 1040, 830, 1262), fill=(92, 56, 36))
    d.ellipse((300, 1196, 522, 1296), fill=(244, 240, 232))
    d.ellipse((558, 1196, 780, 1296), fill=(244, 240, 232))
    d.rectangle((200, 1262, 880, 1310), fill=(236, 230, 218))
    d.rectangle((200, 1300, 880, 1590), fill=(84, 104, 156))
    d.line([(200, 1360), (880, 1360)], fill=(64, 82, 128), width=6)
    d.rectangle((890, 1330, 1060, 1590), fill=(104, 66, 40))
    d.line([(900, 1440), (1050, 1440)], fill=(70, 44, 28), width=5)
    d.rectangle((960, 1256, 988, 1332), fill=(180, 160, 120))
    d.polygon([(912, 1160), (1036, 1160), (1056, 1258), (892, 1258)], fill=(248, 230, 186))
    lit = np.asarray(img).astype(np.float32)
    add_glow(lit, 974, 1210, 520, (255, 190, 110), 0.35)
    add_glow(lit, 974, 1210, 110, (255, 230, 170), 0.9)
    dark = np.asarray(img).astype(np.float32) * np.array((0.16, 0.2, 0.36), np.float32)
    add_glow(dark, 260, 1480, 320, (90, 120, 200), 0.35)
    add_glow(dark, 260, 660, 220, (80, 110, 190), 0.3)
    ROOM_CACHE["lit"], ROOM_CACHE["dark"] = lit, dark
    return lit, dark


def s_room(s, t):
    """Warm lamp-lit bedroom. lamp_off_at -> flicker to moonlit dark; steps_at -> four footsteps
    across the ceiling with falling dust; figure_at -> silhouette by the window (visible in the dark)."""
    lit, dark = room_bases()
    L = 0.0 if s.get("dark") else 1.0
    if s.get("lamp_off_at"):
        lo = at(s["lamp_off_at"], s["_t"])
        if t >= lo:
            L = (1.0 if np.sin((t - lo) * 41) > 0.2 else 0.2) if t - lo < 0.7 else 0.0
    a = dark + (lit - dark) * L
    if s.get("steps_at"):
        st0 = at(s["steps_at"], s["_t"])
        for k in range(4):
            dt = t - (st0 + k * 0.62)
            if 0 <= dt < 1.8:
                x_ = 250 + 190 * k
                if dt < 0.35:
                    a[262:300, x_ - 70:x_ + 70] *= 0.75
                r_ = np.random.default_rng(k)
                for _ in range(16):
                    ox, sp = r_.uniform(-60, 60), r_.uniform(0.6, 1.3)
                    yy_ = int(270 + 520 * sp * dt * dt)
                    if yy_ < 1440:
                        xx_ = int(x_ + ox + 10 * np.sin(dt * 6 + ox))
                        a[yy_:yy_ + 4, xx_:xx_ + 4] = a[yy_:yy_ + 4, xx_:xx_ + 4] * 0.3 + 200 * (0.4 + 0.6 * L) * (1 - dt / 1.8)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if s.get("figure_at") and t >= at(s["figure_at"], s["_t"]):
        al = prog(t, at(s["figure_at"], s["_t"]), 1.2) * (1 - 0.75 * L)
        eyes = prog(t, at(s["eyes_at"], s["_t"]), 0.6) if s.get("eyes_at") else 0.0
        layer = Image.new("RGBA", (W, H))
        draw_figure(ImageDraw.Draw(layer), 560, 1440, 800, al, eyes)
        img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(2.5))).convert("RGB")
    big_lines(ImageDraw.Draw(img), s, t)
    return img




def newspaper_page(s):
    if "_page" in s:
        return s["_page"]
    PW, PH = 960, 1680
    rr_ = np.random.default_rng(5)
    a = np.ones((PH, PW, 3), np.float32) * np.array((242, 235, 216), np.float32)
    a += rr_.normal(0, 4, (PH, PW, 1))
    pg = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(pg)
    title = s.get("paper", "THE ALDER GAZETTE")
    fsz = 84
    while fsz > 30 and d.textlength(title, font=font(F_SERIF_B, fsz)) > PW - 110:
        fsz -= 4
    fm = font(F_SERIF_B, fsz)
    d.text(((PW - d.textlength(title, font=fm)) / 2, 36), title, font=fm, fill=(20, 20, 20))
    d.line([(40, 146), (PW - 40, 146)], fill=(30, 30, 30), width=4)
    d.line([(40, 156), (PW - 40, 156)], fill=(30, 30, 30), width=2)
    fs = font(F_SERIF_I, 32)
    dl = s.get("date", "Thursday, October 29, 1998")
    d.text(((PW - d.textlength(dl, font=fs)) / 2, 166), dl, font=fs, fill=(60, 60, 60))
    hand = s.get("hand", False)
    fh = font("/System/Library/Fonts/MarkerFelt.ttc", 92) if hand else font(F_SERIF_B, 86)
    lines = wrap(d, s.get("headline", "FAMILY OF FOUR VANISHES"), fh, PW - 100)
    y = 230 if not hand else 420
    for ln in lines:
        d.text(((PW - d.textlength(ln, font=fh)) / 2, y), ln, font=fh, fill=(150, 20, 20) if hand else (15, 15, 15))
        y += 104 if hand else 96
    if not s.get("photo", True):
        s["_face"] = (PW / 2, 230 + 52 * len(lines))
        if not hand:
            for row in range(int((PH - 80 - y) / 34)):
                d.rectangle((50, y + 40 + row * 34, PW - 50 - (90 if row % 5 == 4 else 0), y + 52 + row * 34), fill=(150, 145, 135))
        s["_page"] = pg
        return pg
    bx0, by0, bx1, by1 = 50, y + 24, PW - 50, y + 24 + 600
    hb = house_base("day")
    crop = Image.fromarray(np.clip(hb, 0, 255).astype(np.uint8)).crop((150, 430, 930, 1400))
    cd = ImageDraw.Draw(crop)
    for i, x_ in enumerate((330, 400, 470, 540)):  # the family on the porch (crop coords)
        draw_figure(cd, x_ - 150 + 60, 1185 - 430, 150 - 25 * (i % 2) - (40 if i == 3 else 0), 0.75)
    ax, ay, ar = MAIN["attic"]
    fx, fy = ax - 150, ay - 430
    cd.ellipse((fx - 15, fy - 20, fx + 15, fy + 18), fill=(230, 222, 204))
    cd.ellipse((fx - 8, fy - 6, fx - 3, fy - 1), fill=(20, 20, 20))
    cd.ellipse((fx + 3, fy - 6, fx + 8, fy - 1), fill=(20, 20, 20))
    ph = crop.resize((bx1 - bx0, by1 - by0))
    g = np.asarray(ph).astype(np.float32).mean(axis=2, keepdims=True)
    sep = np.clip(g * np.array((1.08, 0.96, 0.78), np.float32) * 0.92 + 10, 0, 255).astype(np.uint8)
    pg.paste(Image.fromarray(sep), (bx0, by0))
    d.rectangle((bx0, by0, bx1, by1), outline=(30, 30, 30), width=3)
    s["_face"] = (bx0 + fx * (bx1 - bx0) / 780, by0 + fy * (by1 - by0) / 970)
    fc = font(F_SERIF_I, 30)
    d.text((bx0, by1 + 12), s.get("caption", "The family at their Alder Lane home, summer 1998."), font=fc, fill=(50, 50, 50))
    y = by1 + 70
    for col in range(2):
        x0_ = 50 + col * (PW - 100) // 2
        for row in range(int((PH - 60 - y) / 34)):
            ln_ = (PW - 100) // 2 - 30 - (int(rr_.uniform(0, 120)) if row % 6 == 5 else 0)
            d.rectangle((x0_, y + row * 34, x0_ + ln_, y + row * 34 + 12), fill=(150, 145, 135))
    s["_page"] = pg
    return pg


def s_newspaper(s, t):
    """Bright old newspaper sliding onto a desk; zoom_at pushes into the photo's attic window;
    circle_at draws a red marker round the face."""
    pg = newspaper_page(s).copy()
    fx, fy = s["_face"]
    if pg.height > H * 0.9:  # landscape: shrink the page so the whole headline fits
        sf = H * 0.9 / pg.height
        pg = pg.resize((int(pg.width * sf), int(pg.height * sf)), Image.LANCZOS)
        fx, fy = fx * sf, fy * sf
    if s.get("circle_at") and t >= at(s["circle_at"], s["_t"]):
        k = prog(t, at(s["circle_at"], s["_t"]), 0.9)
        ImageDraw.Draw(pg).arc((fx - 46, fy - 52, fx + 46, fy + 50), -90, -90 + 360 * k, fill=(210, 20, 20), width=7)
    canvas = Image.new("RGB", (W, H), (78, 52, 36))
    cd = ImageDraw.Draw(canvas)
    for y_ in range(0, H, 46):
        cd.line([(0, y_ + 10 * np.sin(y_)), (W, y_ + 14)], fill=(66, 43, 29), width=3)
    e = ease((t - s["_t"]) / 0.8)
    ang = -6 * (1 - e) - 1.2
    rot = pg.convert("RGBA").rotate(ang, expand=True, resample=Image.BICUBIC)
    ox = (W - rot.width) // 2
    oy = (H - rot.height) // 2 + int(500 * (1 - e))
    shadow = Image.new("RGBA", rot.size, (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 110), mask=rot.split()[3])
    canvas.paste(shadow, (ox + 18, oy + 22), shadow)
    canvas.paste(rot, (ox, oy), rot)
    z, cx_, cy_ = 1.0 + 0.05 * min(1.0, (t - s["_t"]) / 6), W / 2, H / 2
    if s.get("zoom_at") and t >= at(s["zoom_at"], s["_t"]):
        k = ease((t - at(s["zoom_at"], s["_t"])) / 2.4)
        z = z + (float(s.get("zoom", 3.4)) - z) * k
        tx, ty = (W - pg.width) / 2 + fx, (H - pg.height) / 2 + fy
        cx_, cy_ = cx_ + (tx - cx_) * k, cy_ + (ty - cy_) * k
    cw, ch = W / z, H / z
    x0 = min(max(0, cx_ - cw / 2), W - cw)
    y0 = min(max(0, cy_ - ch / 2), H - ch)
    return canvas.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC)


MAP_PATH = [(540, 1900), (540, 1100), (260, 1100), (260, 1500), (540, 1500)]
MAP_CACHE = {}


def map_base():
    if "img" in MAP_CACHE:
        return MAP_CACHE["img"]
    img = Image.new("RGB", (W, H), (238, 235, 228))
    d = ImageDraw.Draw(img)
    d.rectangle((640, 560, 1080, 980), fill=(200, 226, 190))
    d.ellipse((-200, 1580, 200, 2100), fill=(172, 208, 238))
    r_ = np.random.default_rng(9)
    for _ in range(90):
        x_, y_ = r_.uniform(0, W), r_.uniform(300, H)
        w_, h_ = r_.uniform(40, 90), r_.uniform(30, 70)
        d.rectangle((x_, y_, x_ + w_, y_ + h_), fill=(226, 222, 214))
    for x_ in (130, 400, 680, 950):
        d.line([(x_, 0), (x_, H)], fill=(255, 255, 255), width=16)
    for y_ in (800, 1300, 1700):
        d.line([(0, y_), (W, y_)], fill=(255, 255, 255), width=16)
    for x_ in (260, 540, 820):
        d.line([(x_, 0), (x_, H)], fill=(214, 208, 200), width=42)
        d.line([(x_, 0), (x_, H)], fill=(255, 255, 255), width=34)
    for y_ in (500, 1100, 1500):
        d.line([(0, y_), (W, y_)], fill=(214, 208, 200), width=42)
        d.line([(0, y_), (W, y_)], fill=(255, 255, 255), width=34)
    fl = font(F_REG, 30)
    for txt, x_, y_ in (("Alder Ln", 600, 1455), ("Birch St", 300, 1055), ("Elm St", 120, 1300),
                        ("Main St", 560, 760), ("Oak Ave", 700, 455)):
        d.text((x_, y_), txt, font=fl, fill=(120, 120, 120))
    MAP_CACHE["img"] = img
    return img


def path_point(u):
    segs = list(zip(MAP_PATH[:-1], MAP_PATH[1:]))
    lens = [abs(b[0] - a_[0]) + abs(b[1] - a_[1]) for a_, b in segs]
    dist = u * sum(lens)
    for i, ((x0, y0), (x1, y1)) in enumerate(segs):
        if dist <= lens[i] or i == len(segs) - 1:
            f = min(1.0, dist / lens[i])
            return x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, i, (x1 - x0, y1 - y0)
        dist -= lens[i]


def s_map(s, t):
    """Bright navigation map: the route keeps turning left and arrives back on Alder Ln."""
    t0 = at(s.get("drive_from"), s["_t"]) if s.get("drive_from") else s["_t"]
    t1 = at(s["arrive_at"], s["_t"]) if s.get("arrive_at") else s["_end"]
    u = min(1.0, max(0.0, (t - t0) / max(0.5, t1 - t0)))
    cx, cy, seg, (dx, dy) = path_point(u)
    img = map_base().copy()
    d = ImageDraw.Draw(img)
    d.line(MAP_PATH, fill=(66, 133, 244), width=24, joint="curve")
    done = [MAP_PATH[i] for i in range(seg + 1)] + [(cx, cy)]
    d.line(done, fill=(170, 172, 182), width=24, joint="curve")
    ex, ey = MAP_PATH[-1]
    arrived = t >= t1
    bounce = -30 * abs(np.sin((t - t1) * 6)) * np.exp(-(t - t1) * 2) if arrived else 0
    d.ellipse((ex - 30, ey - 92 + bounce, ex + 30, ey - 32 + bounce), fill=(220, 50, 50))
    d.polygon([(ex - 24, ey - 50 + bounce), (ex + 24, ey - 50 + bounce), (ex, ey + bounce)], fill=(220, 50, 50))
    d.ellipse((ex - 11, ey - 73 + bounce, ex + 11, ey - 51 + bounce), fill=(255, 255, 255))
    d.ellipse((cx - 32, cy - 32, cx + 32, cy + 32), fill=(255, 255, 255))
    d.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), fill=(66, 133, 244))
    nrm = max(1, abs(dx) + abs(dy))
    ux, uy = dx / nrm, dy / nrm
    d.polygon([(cx + ux * 18, cy + uy * 18), (cx - ux * 8 + uy * 12, cy - uy * 8 - ux * 12),
               (cx - ux * 8 - uy * 12, cy - uy * 8 + ux * 12)], fill=(255, 255, 255))
    z = 1.35
    cw, ch = W / z, H / z
    x0 = min(max(0, cx - cw / 2), W - cw)
    y0 = min(max(0, cy - ch * 0.55), H - ch)
    img = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC)
    d = ImageDraw.Draw(img)
    texts = s.get("turn_texts", ["Turn left onto Birch St", "Turn left onto Elm St",
                                 "Turn left onto Alder Ln", "Arriving at Alder Ln"])
    bc = (24, 110, 72) if not arrived else (150, 24, 24)
    d.rounded_rectangle((30, 60, W - 30, 250), 34, fill=bc)
    msg = "You have arrived" if arrived else texts[min(seg, len(texts) - 1)]
    d.polygon([(80, 175), (120, 115), (120, 145), (170, 145), (170, 205), (120, 205), (120, 235)]
              if not arrived else [(95, 120), (165, 120), (165, 230), (95, 230)], fill=(255, 255, 255))
    d.text((200, 108), msg, font=font(F_BOLD, 58), fill=(255, 255, 255))
    d.text((200, 180), "Alder Ln" if arrived else f"{max(0.0, (1 - u) * 0.8):.1f} mi", font=FONT_SUB, fill=(225, 240, 230))
    d.rounded_rectangle((30, 1610, W - 30, 1790), 34, fill=(255, 255, 255))
    d.text((80, 1645), s.get("dest", "Anywhere but here"), font=font(F_BOLD, 50), fill=(30, 30, 30))
    d.text((80, 1715), "ETA " + ("now" if arrived else f"{max(1, int((1 - u) * 4))} min") + " · rerouting", font=FONT_SUB, fill=(110, 110, 110))
    return img


RAINCOAT = (232, 192, 40)
VPX, VPY = 540, 820  # road vanishing point
ROAD_HALF = 520.0    # road half-width at depth 1 (screen px)
ROAD_F = 580.0       # ground y offset at depth 1


def road_y(dd):
    return VPY + ROAD_F / dd


def road_x(xw, dd):
    return VPX + xw / dd


def s_road(s, t):
    """Night drive on a two-lane road. pov "car": windshield + dashboard, rain, moving wipers, lane dashes,
    passing pines, a "13" mile marker at marker_at[], the raincoat figure at figure_at[] (figure_closer
    moves it toward the road), lights_off_at (engine dies), mirror_at (raincoat figure in the mirror).
    pov "roadside": you stand on the shoulder; headlights approach at headlights_at and stop at stop_at."""
    pov = s.get("pov", "car")
    a = np.zeros((H, W, 3), np.float32)
    vgrad(a, 0, VPY + 2, (8, 10, 28), (44, 50, 84))
    vgrad(a, VPY, H, (14, 14, 18), (30, 30, 36))
    add_glow(a, 800, 300, 90, (220, 225, 255), 0.8)
    add_glow(a, 800, 300, 300, (120, 130, 180), 0.25)
    off = at(s["lights_off_at"], s["_t"]) if s.get("lights_off_at") else None
    lights = 1.0 if off is None or t < off else max(0.0, 1 - (t - off) / 0.6) * (1.0 if np.sin((t - off) * 50) > 0 else 0.3)
    speed = 9.0 if pov == "car" else 0.0
    if off is not None and t > off:
        speed *= max(0.0, 1 - (t - off) / 2.5)
    travel = speed * (t - s["_t"]) if off is None or t < off else speed * (off - s["_t"]) + 9.0 * min(2.5, t - off) * (1 - min(2.5, t - off) / 5)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.polygon([(road_x(-ROAD_HALF, 0.55), H), (road_x(ROAD_HALF, 0.55), H), (VPX + 6, VPY), (VPX - 6, VPY)], fill=(40, 40, 46))
    for sgn in (-1, 1):
        d.line([(road_x(sgn * ROAD_HALF * 0.92, 0.6), H), (VPX + sgn * 5, VPY)], fill=(150, 150, 140), width=6)
    for k in range(40):  # yellow centre dashes, moving toward us
        z0 = 1.0 + ((k * 4.0 - travel) % 120.0)
        z1 = z0 + 1.6
        if z0 < 1.0:
            continue
        hw0, hw1 = 9 / z0, 9 / z1
        d.polygon([(VPX - hw0, road_y(z0)), (VPX + hw0, road_y(z0)), (VPX + hw1, road_y(z1)), (VPX - hw1, road_y(z1))],
                  fill=(210, 170, 40))
    for k in range(26):  # pines on both shoulders
        z = 1.0 + ((k * 4.6 + (k % 3) * 1.3 - travel) % 120.0)
        for sgn in (-1, 1):
            xw = sgn * (ROAD_HALF * 1.35 + (k * 97) % 380)
            x_, y_ = road_x(xw, z), road_y(z)
            hh = 1900 / z
            col = (8, 16, 12) if z < 30 else tuple(int(8 + (26 - 8) * min(1, (z - 30) / 60)) for _ in range(3))
            d.polygon([(x_, y_ - hh), (x_ - hh * 0.2, y_), (x_ + hh * 0.2, y_)], fill=col)
    arr = np.asarray(img).astype(np.float32)
    if pov == "car":
        add_glow(arr, 400, 1180, 330, (255, 240, 200), 0.32 * lights)
        add_glow(arr, 680, 1180, 330, (255, 240, 200), 0.32 * lights)
        add_glow(arr, VPX, VPY + 120, 260, (255, 240, 210), 0.12 * lights)
    else:
        ha = at(s["headlights_at"], s["_t"]) if s.get("headlights_at") else s["_t"]
        sa = at(s["stop_at"], s["_t"]) if s.get("stop_at") else s["_end"]
        if t >= ha:
            u = min(1.0, (t - ha) / max(0.5, sa - ha))
            z = 60 * (1 - ease(u)) + 5.5
            for sgn in (-1, 1):
                add_glow(arr, road_x(sgn * 160, z), road_y(z) - 70 / z, max(6, 700 / z), (255, 246, 220), 0.75)
            add_glow(arr, VPX, road_y(z), max(10, 2600 / z), (255, 240, 210), min(0.5, 6 / z))
    img = Image.fromarray(np.clip(arr * (0.55 + 0.45 * lights if pov == "car" else 1.0), 0, 255).astype(np.uint8)).convert("RGBA")
    layer = Image.new("RGBA", (W, H))
    ld = ImageDraw.Draw(layer)
    for ma in s.get("marker_at", []):  # "13" mile marker rushing past on the right shoulder
        m0 = at(ma, s["_t"])
        if 0 <= t - m0 < 3.0:
            z = max(0.9, 30 - (t - m0) * 10)
            x_, y_ = road_x(ROAD_HALF * 1.05, z), road_y(z)
            ph, pw = 900 / z, 260 / z
            ld.rectangle((x_ - 8 / z, y_ - ph, x_ + 8 / z, y_), fill=(120, 120, 120, 255))
            ld.rectangle((x_ - pw / 2, y_ - ph, x_ + pw / 2, y_ - ph + pw * 1.3), fill=(20, 110, 60, 255), outline=(240, 240, 240, 255), width=max(1, int(10 / z)))
            fz = max(8, int(150 / z))
            fm = font(F_BOLD, fz)
            ld.text((x_ - ld.textlength("13", font=fm) / 2, y_ - ph + pw * 0.25), "13", font=fm, fill=(255, 255, 255, 255))
    for i, fa in enumerate(s.get("figure_at", [])):
        f0 = at(fa, s["_t"])
        if 0 <= t - f0 < 3.0:
            z = max(0.9, 26 - (t - f0) * 9)
            closer = float(s.get("figure_closer", [0, 0.2, 0.4])[min(i, 2)] if isinstance(s.get("figure_closer"), list) else 0)
            xw = ROAD_HALF * (1.25 - closer)
            draw_figure(ld, road_x(xw, z), road_y(z), 1700 / z, 1.0, 0.0, RAINCOAT)
            ld.ellipse((road_x(xw, z) - 70 / z, road_y(z) - 1700 / z - 40 / z, road_x(xw, z) + 70 / z, road_y(z) - 1700 / z + 120 / z), fill=RAINCOAT + (255,))
    if pov == "roadside" and s.get("raincoat_sleeve", True):
        ld.polygon([(W, 1500), (W, H), (760, H), (900, 1600)], fill=RAINCOAT + (255,))
    img = Image.alpha_composite(img, layer.filter(ImageFilter.GaussianBlur(1.2)))
    d = ImageDraw.Draw(img)
    if pov == "car":
        for x_, y_ in ((RAIN[i][0], RAIN[i][1] * 0.75) for i in range(0, 120)):  # drops on the glass
            d.ellipse((x_ - 4, y_ - 5, x_ + 4, y_ + 5), fill=(70, 78, 96))
        ang = np.radians(15 + 70 * (0.5 + 0.5 * np.sin(t * 2.4)))
        px, py = 300, 1450
        d.line([(px, py), (px + 820 * np.cos(ang), py - 820 * np.sin(ang))], fill=(10, 10, 12), width=16)
        d.polygon([(0, 0), (150, 0), (40, 1450), (0, 1450)], fill=(10, 10, 12))
        d.polygon([(W, 0), (W - 150, 0), (W - 40, 1450), (W, 1450)], fill=(10, 10, 12))
        d.rectangle((0, 0, W, 40), fill=(10, 10, 12))
        d.rounded_rectangle((400, 60, 680, 150), 20, fill=(16, 16, 20), outline=(40, 40, 46), width=6)
        if s.get("mirror_at") and t >= at(s["mirror_at"], s["_t"]):
            k = prog(t, at(s["mirror_at"], s["_t"]), 0.6)
            d.ellipse((510, 76, 570, 150), fill=tuple(int(c * k) for c in RAINCOAT))
            d.ellipse((528, 98, 552, 136), fill=(10, 10, 12))
        d.pieslice((-200, 1380, W + 200, 2500), 180, 360, fill=(18, 18, 22))
        glow = (60, 140, 255) if lights > 0.1 else (20, 24, 30)
        for cx_ in (380, 700):
            d.ellipse((cx_ - 90, 1530, cx_ + 90, 1710), outline=glow, width=6)
            ang2 = np.radians(200 - 120 * (speed / 9.0) + 3 * np.sin(t * 3))
            d.line([(cx_, 1620), (cx_ + 70 * np.cos(ang2), 1620 - 70 * np.sin(ang2))], fill=(255, 80, 60), width=6)
        d.arc((120, 1560, 960, 2400), 200, 340, fill=(30, 30, 34), width=60)
    big_lines(d, s, t)
    return img.convert("RGB")


WOODS = [((np.random.default_rng(21).uniform(-1, 1)) * 2600, 1.0 + k * 1.15, 40 + (k * 37) % 70) for k in range(70)]


def s_woods(s, t):
    """Walking into a forest (real parallax): dusk = purple fog, fireflies; night = dark blue.
    lanterns_at lights lanterns one by one along the path (warm, bright); lanterns_off_at kills them;
    flashlight: true narrows the view to a swaying beam; figure_at (+ raincoat) on the path."""
    tm = s.get("time", "dusk")
    sky = ((70, 50, 110), (210, 120, 120)) if tm == "dusk" else ((6, 8, 20), (24, 30, 54))
    fog = np.array((150, 120, 160) if tm == "dusk" else (40, 46, 70), np.float32)
    a = np.zeros((H, W, 3), np.float32)
    vgrad(a, 0, VPY + 230, *sky)
    vgrad(a, VPY + 230, H, (40, 44, 34) if tm == "dusk" else (10, 14, 12), (22, 26, 20) if tm == "dusk" else (6, 8, 7))
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    gy = VPY + 230
    d.polygon([(380, H), (700, H), (VPX + 14, gy), (VPX - 14, gy)], fill=(96, 80, 64) if tm == "dusk" else (34, 30, 26))
    walk = float(s.get("walk", 1.4)) * (t - s["_t"])
    rng_ = np.random.default_rng(21)
    xs = rng_.uniform(-1, 1, len(WOODS))
    trees = []
    for k, (_, z0, w0) in enumerate(WOODS):
        z = 0.6 + ((z0 - walk) % 80.0)
        xw = xs[k] * 2600
        if abs(xw) < 260:
            xw = 260 * np.sign(xw or 1) + xw
        trees.append((z, xw, w0))
    trees.sort(key=lambda q: -q[0])
    trunk = np.array((30, 22, 26) if tm == "dusk" else (8, 10, 12), np.float32)
    lant = []
    if s.get("lanterns_at"):
        l0 = at(s["lanterns_at"], s["_t"])
        loff = at(s["lanterns_off_at"], s["_t"]) if s.get("lanterns_off_at") else 1e9
        for k in range(12):
            z = 0.8 + ((3 + k * 3.2 - walk) % 40.0)
            on = (t >= l0 + k * 0.3) and t < loff
            lant.append((z, (-1) ** k * 330, on))
    for z, xw, w0 in trees:
        x_ = VPX + xw / z
        wpx = max(2, w0 * 4 / z)
        foot = gy + 1100 / z
        f = min(1.0, (z - 1) / 40)
        col = tuple(int(v) for v in trunk * (1 - f) + fog * f * 0.9)
        d.rectangle((x_ - wpx / 2, -10, x_ + wpx / 2, foot), fill=col)
    arr = np.asarray(img).astype(np.float32)
    band = np.exp(-((np.arange(H, dtype=np.float32) - (gy - 60)) / 260) ** 2)[:, None, None]
    drift = 0.5 + 0.5 * np.sin(np.arange(W, dtype=np.float32)[None, :, None] / 180 + t * 0.4)
    arr += band * drift * fog * 0.45
    for z, xw, on in lant:
        x_, y_ = VPX + xw / z, gy + 1100 / z - 520 / z
        if on:
            add_glow(arr, x_, y_, max(8, 260 / z), (255, 190, 90), 0.9)
            r_ = max(2, 26 / z)
            arr[int(y_ - r_):int(y_ + r_), int(max(0, x_ - r_)):int(min(W, x_ + r_))] = (255, 225, 150)
    if tm == "dusk" and not s.get("flashlight"):
        r_ = np.random.default_rng(4)
        for k in range(40):
            fx = (r_.uniform(0, W) + 40 * np.sin(t * 0.7 + k)) % W
            fy = r_.uniform(gy - 300, H - 200) + 30 * np.sin(t * 1.1 + k * 2)
            if np.sin(t * 3 + k * 1.7) > 0.2:
                add_glow(arr, fx, fy, 14, (255, 240, 140), 0.9)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    if s.get("figure_at") and t >= at(s["figure_at"], s["_t"]):
        al = prog(t, at(s["figure_at"], s["_t"]), 1.0)
        layer = Image.new("RGBA", (W, H))
        z = float(s.get("figure_depth", 5))
        draw_figure(ImageDraw.Draw(layer), VPX + float(s.get("figure_x", 120)) / z * 3, gy + 1100 / z, 3800 / z, al,
                    prog(t, at(s["eyes_at"], s["_t"]), 0.6) if s.get("eyes_at") else 0.0,
                    (196, 158, 30) if s.get("raincoat") else (4, 4, 6))
        img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(3.5))).convert("RGB")
    if s.get("flashlight"):
        bx = W / 2 + 140 * np.sin(t * 1.7) + 40 * np.sin(t * 5.3)
        by = H * 0.55 + 70 * np.sin(t * 1.3)
        yy_, xx_ = np.ogrid[0:H, 0:W]
        m = np.exp(-(((xx_ - bx) / 340.0) ** 2 + ((yy_ - by) / 480.0) ** 2))
        lit = (0.16 + 0.84 * m).astype(np.float32)[..., None]
        if s.get("lanterns_off_at") and t >= at(s["lanterns_off_at"], s["_t"]):
            lit = lit * (0.25 if (t - at(s["lanterns_off_at"], s["_t"])) % 1.3 < 0.08 else 1.0)
        img = Image.fromarray(np.clip(np.asarray(img).astype(np.float32) * lit * np.array((1.0, 0.97, 0.88)), 0, 255).astype(np.uint8))
    big_lines(ImageDraw.Draw(img), s, t)
    return img


def s_sign(s, t):
    """Wooden roadside sign at dusk with painted lines; change_at paints over line `change_line`
    with a brush stroke and writes `new_text` in red."""
    a = np.zeros((H, W, 3), np.float32)
    vgrad(a, 0, 1250, (92, 64, 130), (250, 160, 100))
    vgrad(a, 1250, H, (54, 76, 48), (28, 40, 26))
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    for k in range(30):
        x_ = k * 40 - 20 + 12 * np.sin(k * 3)
        hh = 160 + (k * 53) % 140
        d.polygon([(x_, 1250 - hh), (x_ - 40, 1255), (x_ + 40, 1255)], fill=(34, 30, 44))
    for xp in (300, 780):
        d.rectangle((xp - 22, 1000, xp + 22, 1480), fill=(70, 48, 32))
    d.rectangle((150, 560, 930, 1080), fill=(120, 82, 50), outline=(70, 46, 28), width=14)
    for y_ in range(590, 1060, 34):
        d.line([(170, y_ + 6 * np.sin(y_)), (910, y_)], fill=(104, 70, 42), width=3)
    lines = list(s.get("lines", ["WELCOME TO", "HOLLOW CREEK", "POPULATION 13"]))
    fsz = [70, 96, 70]
    ch = s.get("change_at")
    ci = int(s.get("change_line", len(lines) - 1))
    y = 610
    for i, ln in enumerate(lines):
        fm = font(F_SERIF_B, fsz[min(i, 2)])
        d.text(((W - d.textlength(ln, font=fm)) / 2, y), ln, font=fm, fill=(244, 232, 206))
        if ch and i == ci and t >= at(ch, s["_t"]):
            k = ease((t - at(ch, s["_t"])) / 0.9)
            d.rectangle((180, y - 8, 180 + 720 * k, y + fsz[min(i, 2)] + 18), fill=(66, 40, 28))
            if k >= 1:
                nt = s.get("new_text", "POPULATION 14")
                fr = font(F_SERIF_B, fsz[min(i, 2)])
                d.text(((W - d.textlength(nt, font=fr)) / 2, y), nt, font=fr, fill=(210, 30, 30))
                for dx in (300, 420, 610):  # paint drips
                    dl = 60 * prog(t, at(ch, s["_t"]) + 1.0, 2.0)
                    d.line([(dx, y + fsz[min(i, 2)]), (dx, y + fsz[min(i, 2)] + dl)], fill=(190, 24, 24), width=7)
        y += fsz[min(i, 2)] + 60
    big_lines(d, s, t)
    return img


def s_call(s, t):
    """Phone call screen (bright gradient): 'calling…' with pulsing rings until connect_at, then a running
    timer and live waveform; end_at shows 'Call ended'."""
    a = np.zeros((H, W, 3), np.float32)
    vgrad(a, 0, H, (52, 40, 110), (20, 110, 130))
    add_glow(a, 300, 500, 400, (160, 80, 200), 0.4)
    add_glow(a, 800, 1400, 420, (40, 180, 200), 0.35)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    name = s.get("contact", "Home")
    ca = at(s["connect_at"], s["_t"]) if s.get("connect_at") else 1e9
    ea = at(s["end_at"], s["_t"]) if s.get("end_at") else 1e9
    cx, cy = W / 2, 620
    if t < ca:
        for k in range(3):
            ph = ((t - s["_t"]) * 0.8 + k / 3) % 1.0
            r_ = 150 + 200 * ph
            d.ellipse((cx - r_, cy - r_, cx + r_, cy + r_), outline=tuple(int(255 * (1 - ph)) for _ in range(3)), width=3)
    d.ellipse((cx - 140, cy - 140, cx + 140, cy + 140), fill=(230, 230, 240))
    fa = font(F_BOLD, 140)
    d.text((cx - d.textlength(name[:1], font=fa) / 2, cy - 82), name[:1], font=fa, fill=(80, 70, 140))
    fn = font(F_BOLD, 84)
    d.text(((W - d.textlength(name, font=fn)) / 2, 830), name, font=fn, fill=(255, 255, 255))
    if t >= ea:
        st = "Call ended"
    elif t >= ca:
        sec = int(t - ca)
        st = f"{sec // 60:02d}:{sec % 60:02d}"
    else:
        st = s.get("status", "calling…")
    fs = font(F_REG, 50)
    d.text(((W - d.textlength(st, font=fs)) / 2, 940), st, font=fs, fill=(220, 225, 240))
    if ca <= t < ea:
        for k in range(28):
            hgt = 20 + 70 * abs(np.sin(t * 9 + k * 0.7)) * abs(np.sin(t * 2.3 + k))
            x_ = 260 + k * 20
            d.rounded_rectangle((x_, 1110 - hgt / 2, x_ + 10, 1110 + hgt / 2), 5, fill=(255, 255, 255))
    for i, lbl in enumerate(("mute", "keypad", "speaker")):
        x_ = 250 + i * 290
        d.ellipse((x_ - 70, 1230, x_ + 70, 1370), outline=(240, 240, 255), width=4)
        fl = font(F_REG, 32)
        d.text((x_ - d.textlength(lbl, font=fl) / 2, 1385), lbl, font=fl, fill=(230, 230, 245))
    d.ellipse((cx - 80, 1470, cx + 80, 1630), fill=(230, 50, 50))
    d.rounded_rectangle((cx - 44, 1538, cx + 44, 1562), 10, fill=(255, 255, 255))
    big_lines(d, s, t)
    return img


# ---------- character "stage" scenes (real images + cutout characters) ----------
ASSETS = STORY.get("assets", os.path.join(EP, "..", "..", "characters"))
if not os.path.isabs(ASSETS):
    ASSETS = os.path.normpath(os.path.join(EP, ASSETS))
_SEGS = STORY.get("segments")
if _SEGS is None and os.path.exists(os.path.join(EP, "segments.json")):
    _SEGS = json.load(open(os.path.join(EP, "segments.json")))
SEGMENTS = [(g["speaker"], g["start"] / SPEED, g["end"] / SPEED) for g in (_SEGS or [])]
_ENV = {}


def voice_env():
    """Loudness envelope of the voice track, one value per video frame (0..1)."""
    if "v" not in _ENV:
        try:
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(EP, "voice.mp3"), "-af", f"atempo={SPEED}",
                                  "-ac", "1", "-ar", "12000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
            x = np.frombuffer(raw, np.float32)
            hop = 12000 // FPS
            n = len(x) // hop
            r = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(axis=1))
            r = np.convolve(r, np.ones(3) / 3, mode="same")
            _ENV["v"] = np.clip(r / (np.percentile(r, 95) + 1e-6), 0, 1.3)
        except Exception:
            _ENV["v"] = np.zeros(1)
    return _ENV["v"]


def speaking(spk, t):
    if not spk:
        return 0.0
    for sp, a0, a1 in SEGMENTS:
        if sp == spk and a0 <= t <= a1:
            v = voice_env()
            i = int(t * FPS)
            return float(v[i]) if i < len(v) else 0.0
    return 0.0


_IMG = {}


def unmark(im):
    """Hide the AI-generator sparkle watermark (bottom-right, ~91-95% x, 84-90% y): clone the texture just left of it
    over it with a feathered mask. Only matters when the whole width is on screen (landscape long-form)."""
    w, h = im.size
    x0, y0, x1, y1 = int(w * 0.905), int(h * 0.83), int(w * 0.952), int(h * 0.915)
    pw = x1 - x0
    patch = im.crop((x0 - pw - 6, y0, x0 - 6, y1))
    m = Image.new("L", (pw, y1 - y0), 0)
    ImageDraw.Draw(m).ellipse((2, 2, pw - 2, y1 - y0 - 2), fill=255)
    im = im.copy(); im.paste(patch, (x0, y0), m.filter(ImageFilter.GaussianBlur(6)))
    return im


def stage_bg(path, grade):
    key = (path, json.dumps(grade, sort_keys=True))
    if key not in _IMG:
        im = unmark(Image.open(os.path.join(ASSETS, path)).convert("RGB"))
        sc = H / im.height
        im = im.resize((max(W, int(im.width * sc)), H), Image.LANCZOS)
        a = np.asarray(im).astype(np.float32)
        a = a * float(grade.get("dim", 1.0)) * np.array(grade.get("tint", [1, 1, 1]), np.float32)
        if grade.get("contrast"):
            a = (a - 128) * float(grade["contrast"]) + 128
        _IMG[key] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _IMG[key]


def stage_char(cid, img, shade, tint, rim):
    key = (cid, img, shade, tuple(tint), tuple(rim) if rim else None)
    if key not in _IMG:
        im = Image.open(os.path.join(ASSETS, cid, f"cut_{img}.png")).convert("RGBA")
        a = np.asarray(im).astype(np.float32)
        rgb = a[..., :3] * shade * np.array(tint, np.float32)
        al = a[..., 3]
        if rim:
            inner = np.asarray(Image.fromarray(al.astype(np.uint8)).filter(ImageFilter.MinFilter(15))).astype(np.float32)
            edge = np.clip(al - inner, 0, 255)[..., None] / 255.0
            edge = np.asarray(Image.fromarray((edge[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))).astype(np.float32)[..., None] / 255.0
            rgb = rgb + edge * np.array(rim, np.float32) * 0.6
        out = np.dstack([np.clip(rgb, 0, 255), al]).astype(np.uint8)
        red = (a[..., 0] > 140) & (a[..., 1] < 80) & (a[..., 2] < 80) & (al > 200)
        eyes = []
        if red.sum() > 10:
            from scipy import ndimage as ndi
            lab, n = ndi.label(red)
            if n:
                sizes = ndi.sum(red, lab, range(1, n + 1))
                for i in np.argsort(sizes)[::-1][:2]:
                    cy, cx = ndi.center_of_mass(red, lab, i + 1)
                    eyes.append((cx / im.width, cy / im.height))
        _IMG[key] = (Image.fromarray(out, "RGBA"), eyes)
    return _IMG[key]


def s_stage(s, t):
    """A real background image (or full-frame character photo) with camera pan/zoom, plus cutout characters
    that enter (rise/fade/slide/flicker), breathe, sway, bounce with their own voice, approach, glow."""
    grade = s.get("grade", {})
    bg = stage_bg(s["bg"], grade)
    dur = max(0.5, min(s["_end"], DUR) - s["_t"])
    u = ease((t - s["_t"]) / dur) if s.get("ease", True) else (t - s["_t"]) / dur
    cx0, cx1 = s.get("cx", [0.5, 0.5])
    z0, z1 = s.get("zoom", [1.0, 1.08])
    z = z0 + (z1 - z0) * u + 0.025 * speaking(s.get("pulse_speaker"), t)
    if s.get("zoom_at") and t >= at(s["zoom_at"], s["_t"]):
        z += (float(s.get("zoom_to", 1.6)) - z) * ease((t - at(s["zoom_at"], s["_t"])) / float(s.get("zoom_dur", 1.2)))
    cw, ch = W / z, H / z
    px = (cx0 + (cx1 - cx0) * u) * bg.width
    py = float(s.get("cy", 0.5)) * H
    x0 = min(max(0, px - cw / 2), bg.width - cw)
    y0 = min(max(0, py - ch / 2), H - ch)
    img = bg.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC).convert("RGBA")
    if s.get("fit"):  # whole landscape image (wider than a 9:16 crop) over a blurred, darkened fill
        fw = int(W * float(s["fit"]) * z)
        fh = int(bg.height * fw / bg.width)
        fg = bg.resize((fw, fh), Image.BICUBIC)
        img = Image.blend(img.filter(ImageFilter.GaussianBlur(28)).convert("RGB"), Image.new("RGB", (W, H)), 0.35).convert("RGBA")
        img.paste(fg, (int(W / 2 - px / bg.width * fw), int(float(s.get("fit_y", 0.42)) * H - fh / 2)))
    glows = []
    for c in s.get("chars", []):
        ca = at(c.get("at"), s["_t"]) if c.get("at") else s["_t"]
        if t < ca:
            continue
        p = prog(t, ca, float(c.get("enter_dur", 0.7)))
        alpha = 1.0
        ox, oy = 0.0, 0.0
        en = c.get("enter", "rise")
        if en == "rise":
            oy = 260 * (1 - p)
            alpha = p
        elif en == "fade":
            alpha = p
        elif en == "slide-l":
            ox = -700 * (1 - p)
        elif en == "slide-r":
            ox = 700 * (1 - p)
        elif en == "flicker":
            alpha = (1.0 if np.sin((t - ca) * 37) > -0.2 else 0.15) if t - ca < 1.3 else 1.0
        if c.get("exit_at") and t >= at(c["exit_at"], s["_t"]):
            alpha *= 1 - prog(t, at(c["exit_at"], s["_t"]), 0.5)
        if alpha <= 0.01:
            continue
        cut, eyes = stage_char(c["id"], c.get("img", "master"), float(c.get("shade", s.get("char_shade", 0.85))),
                               c.get("tint", s.get("char_tint", [1, 1, 1])), c.get("rim", s.get("rim")))
        hgt = float(c.get("h", 0.62)) * H
        hgt *= 1 + 0.008 * np.sin(t * 1.7 + hash(c["id"]) % 7)
        if c.get("approach"):
            aa, scl = c["approach"]
            if t >= at(aa, s["_t"]):
                hgt *= 1 + (float(scl) - 1) * ease((t - at(aa, s["_t"])) / float(c.get("approach_dur", 2.5)))
        bob = speaking(c.get("speaker"), t)
        hgt *= 1 + 0.02 * bob
        oy -= 16 * bob
        wid = int(cut.width * hgt / cut.height)
        im = cut.resize((max(1, wid), max(1, int(hgt))), Image.BICUBIC)
        if c.get("sway"):
            im = im.rotate(float(c["sway"]) * np.sin(t * 2.4), resample=Image.BICUBIC, center=(im.width / 2, im.height))
        if alpha < 1:
            im.putalpha(im.split()[3].point(lambda v: int(v * alpha)))
        cxp = float(c.get("x", 0.5)) * W + ox
        by = float(c.get("y", 1.0)) * H + oy
        img.alpha_composite(im, (int(cxp - im.width / 2), int(by - im.height)))
        if c.get("eyes_glow") and eyes:
            for ex, ey in eyes:
                glows.append((cxp - im.width / 2 + ex * im.width, by - im.height + ey * im.height, alpha))
    img = img.convert("RGB")
    if glows or s.get("flicker"):
        a = np.asarray(img).astype(np.float32)
        for gx, gy, al in glows:
            add_glow(a, gx, gy, 26, (255, 40, 30), (0.8 + 0.3 * np.sin(t * 6)) * al)
        if s.get("flicker"):
            a *= flicker_at(t, 1.3)
        img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    if s.get("chip"):
        fc = font(F_BOLD, 38)
        tw = d.textlength(s["chip"], font=fc)
        d.rounded_rectangle((W / 2 - tw / 2 - 70, 70, W / 2 + tw / 2 + 40, 140), 35, fill=(14, 14, 18))
        if int(t * 2) % 2 == 0:
            d.ellipse((W / 2 - tw / 2 - 50, 92, W / 2 - tw / 2 - 24, 118), fill=(230, 30, 30))
        d.text((W / 2 - tw / 2 - 10, 84), s["chip"], font=fc, fill=(255, 255, 255))
        if s.get("chip_speaker"):
            lv = speaking(s["chip_speaker"], t)
            for k in range(24):
                hh = 6 + 46 * lv * abs(np.sin(t * 11 + k * 0.9))
                xx = W / 2 - 240 + k * 20
                d.rounded_rectangle((xx, 190 - hh / 2, xx + 10, 190 + hh / 2), 5, fill=(255, 255, 255))
    big_lines(d, s, t)
    if s.get("subtitle") and t >= at(s["subtitle"]["at"], s["_t"]) + float(s["subtitle"].get("delay", 0)):
        fs = font(F_BOLD, 58)
        tx = s["subtitle"]["text"]
        d.text(((W - d.textlength(tx, font=fs)) / 2, int(s.get("title_y", 1230)) + 190 * len(s.get("title_lines", []))),
               tx, font=fs, fill=(240, 240, 240), stroke_width=6, stroke_fill=(0, 0, 0))
    return img


# ---------- real stock footage ("clip" scenes, e.g. Pixabay videos) ----------
_CLIP = {}


def s_clip(s, t):
    """Real video footage: file (relative to the episode), from (seconds into the source), grade
    {dim, tint, contrast, desat}, speed (playback rate), focus_x/focus_y (0-1, where the 9:16 crop sits), title_lines/title_y, figure_at/eyes_at (silhouette).
    Frames are decoded on demand through one ffmpeg pipe per scene, read forward, cover-cropped to 9:16."""
    st = _CLIP.setdefault(id(s), {"proc": None, "idx": -1, "frame": None})
    want = max(0, int((t - s["_t"]) * FPS * float(s.get("speed", 1.0))))
    if st["proc"] is None or want < st["idx"]:  # (re)open: first use, or a preview asks for an earlier frame
        if st["proc"]:
            st["proc"].kill()
        t0 = float(s.get("from", 0)) + want / FPS
        st["proc"] = subprocess.Popen([
            "ffmpeg", "-v", "error", *(["-stream_loop", "-1"] if s.get("loop") else []),  # loop: repeat short clips instead of freezing
            "-ss", f"{t0:.3f}", "-i", os.path.join(EP, s["file"]),
            "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                   f"crop={W}:{H}:(iw-ow)*{float(s.get('focus_x', 0.5))}:(ih-oh)*{float(s.get('focus_y', 0.5))},fps={FPS}",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        st["idx"], st["base"] = want - 1, want
    while st["idx"] < want:
        raw = st["proc"].stdout.read(W * H * 3)
        if len(raw) < W * H * 3:  # clip ran out: hold the last frame
            break
        st["frame"], st["idx"] = raw, st["idx"] + 1
    if st["frame"] is None:
        return Image.new("RGB", (W, H))
    a = np.frombuffer(st["frame"], np.uint8).reshape(H, W, 3).astype(np.float32)
    g = s.get("grade", {})
    if g.get("desat"):
        a = a + (a.mean(axis=2, keepdims=True) - a) * float(g["desat"])
    if g.get("contrast"):
        a = (a - 128) * float(g["contrast"]) + 128
    a = a * float(g.get("dim", 0.8)) * np.array(g.get("tint", [1, 1, 1]), np.float32)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if s.get("figure_at") and t >= at(s["figure_at"], s["_t"]):
        al = prog(t, at(s["figure_at"], s["_t"]), 1.2) * float(s.get("figure_alpha", 0.85))
        eyes = prog(t, at(s["eyes_at"], s["_t"]), 0.6) if s.get("eyes_at") else 0.0
        layer = Image.new("RGBA", (W, H))
        fx, ff, fh = s.get("figure", [W // 2, 1500, 760])
        draw_figure(ImageDraw.Draw(layer), fx, ff, fh, al, eyes)
        img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(3))).convert("RGB")
    big_lines(ImageDraw.Draw(img), s, t)
    return img


SCENE_FN = {"lock": s_lock, "chat": s_chat, "card": s_card, "title": s_title, "clip": s_clip,
            "hallway": s_hallway, "door": s_door, "house": s_house, "room": s_room,
            "newspaper": s_newspaper, "map": s_map, "road": s_road, "woods": s_woods,
            "sign": s_sign, "call": s_call, "stage": s_stage}


def current(t):
    for s in SCENES:
        if s["_t"] <= t < s["_end"]:
            return s
    return SCENES[-1]


CAP_Y = int(STORY.get("caption_y", 1290))  # keeps captions above the Shorts title/channel overlay (safe zone ends ~1440)


def draw_caption(img, t, s):
    c = caption_at(t)
    if not c or not s.get("captions", True) or not STORY.get("captions", True):  # story-level off: multi-language long-form
        return img
    d = ImageDraw.Draw(img)
    spk = c[0].get("speaker")
    sp = STORY.get("speakers", {}).get(spk) if spk else None
    if sp:  # who is talking: small colored name tag above the caption
        fl = font(F_BOLD, 30 if LAND else 40)
        nm = sp.get("name", spk).upper()
        tw = d.textlength(nm, font=fl)
        col = tuple(sp.get("color", [255, 200, 60]))
        ty = H - 262 if LAND else CAP_Y - 90
        d.rounded_rectangle(((W - tw) / 2 - 20, ty, (W + tw) / 2 + 20, ty + (50 if LAND else 62)), 26, fill=(10, 10, 12), outline=col, width=4)
        d.text(((W - tw) / 2, ty + (8 if LAND else 10)), nm, font=fl, fill=col)
    parts = [w["text"].strip().strip("\"").upper() for w in c]
    space = d.textlength(" ", font=FONT_CAP)
    widths = [d.textlength(p, font=FONT_CAP) for p in parts]
    x = (W - sum(widths) - space * (len(parts) - 1)) / 2
    for w, p, wd in zip(c, parts, widths):
        active = w["start"] <= t <= w["end"] + 0.08
        d.text((x, H - 198 if LAND else CAP_Y), p, font=FONT_CAP, fill=(235, 30, 30) if active else (255, 255, 255),
               stroke_width=8, stroke_fill=(0, 0, 0))
        x += wd + space
    return img


FLASH = resolve_list("flash")  # lightning: white double-flash (+ thunder in sfx)
STATIC_FR = [rng.integers(0, 255, (H // 4, W // 4), dtype=np.uint8) for _ in range(4)]
TRANSITIONS = STORY.get("transitions", "static")


def post(img, t, i, s=None):
    if s is not None and s.get("rain"):
        img = add_rain(img, t)
    if s is not None and s["type"] != "hallway":  # slow push-in over each scene
        dur = max(0.5, min(s["_end"], DUR) - s["_t"])
        z = 1.0 + float(s.get("push", 0.04)) * min(1.0, (t - s["_t"]) / dur)
    else:
        z = 1.0 + 0.03 * ((t % 6) / 6)
    shake = 0
    for tb in SHAKE:
        if 0 <= t - tb < 0.5:
            shake = 10 * np.sin((t - tb) * 90)
    for tb in HEAVY_SHAKE:
        if 0 <= t - tb < 0.25:
            shake = 28 * (1 - (t - tb) / 0.25) * np.sin((t - tb) * 120)
    cw, ch = int(W / z), int(H / z)
    x0, y0 = (W - cw) // 2 + int(shake), (H - ch) // 2
    img = img.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
    a = np.asarray(img).astype(np.float32)
    for tg in GLITCH:
        if 0 <= t - tg < 0.6 and i % 3 != 2:
            sft = int(18 * (1 - (t - tg) / 0.6))
            a[..., 0] = np.roll(a[..., 0], sft, axis=1)
            a[..., 2] = np.roll(a[..., 2], -sft, axis=1)
    for tf in FLASH:
        dt = t - tf
        if 0 <= dt < 0.7:
            k = np.exp(-dt * 14) + (0.7 * np.exp(-(dt - 0.18) * 10) if dt > 0.18 else 0)
            a = a * (1 + 1.5 * k) + 150 * k
    if TRANSITIONS == "static" and s is not None and s is not SCENES[0] and 0 <= t - s["_t"] < 0.22:
        al = 0.85 * (1 - (t - s["_t"]) / 0.22)
        nz = np.repeat(np.repeat(STATIC_FR[i % 4], 4, 0), 4, 1)[..., None].astype(np.float32)
        a = a * (1 - al) + nz * al
    g = np.repeat(np.repeat(GRAIN[i % len(GRAIN)], 2, 0), 2, 1)[..., None]
    flicker = 1.0 - 0.06 * (np.sin(t * 23.0) * np.sin(t * 7.3) > 0.85)
    return np.clip((a + g) * VIGNETTE * flicker, 0, 255).astype(np.uint8)


# ---------- synthesized sound design ----------
def build_sfx(path):
    n = int(DUR * SR)
    tt = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    drone = (0.10 * np.sin(2 * np.pi * 48 * tt) + 0.07 * np.sin(2 * np.pi * 48.7 * tt)
             + 0.04 * np.sin(2 * np.pi * 96.3 * tt))
    noise = rng.normal(0, 1, n).astype(np.float32)
    wind = np.convolve(noise, np.ones(400) / 400, mode="same") * 0.9
    bed = (drone + wind) * (0.6 + 0.4 * np.sin(2 * np.pi * tt / 9)) * np.clip(tt / 2.0, 0, 1)
    if SILENCE_FROM is not None:
        bed[int(SILENCE_FROM * SR):] *= 0.25
    out += bed

    def add(sig, t0):
        s = int(t0 * SR)
        e = min(n, s + len(sig))
        if 0 <= s < n:
            out[s:e] += sig[: e - s]

    def buzz():
        d = np.arange(int(0.45 * SR)) / SR
        return 0.35 * np.sign(np.sin(2 * np.pi * 150 * d)) * ((d % 0.22) < 0.16) * np.exp(-d * 1.5)

    def knock():
        d = np.arange(int(0.35 * SR)) / SR
        return (0.9 * np.sin(2 * np.pi * (95 - 40 * d) * d) * np.exp(-d * 22)
                + 0.25 * rng.normal(0, 1, len(d)) * np.exp(-d * 120))

    def sting():
        d = np.arange(int(1.6 * SR)) / SR
        sig = sum(np.sin(2 * np.pi * f * d) for f in (220, 233.1, 311, 466.2))
        return 0.07 * sig * np.exp(-d * 2.0) * np.clip(d * 20, 0, 1)

    def heartbeat():
        d = np.arange(int(0.8 * SR)) / SR
        beat = lambda o: np.sin(2 * np.pi * 55 * (d - o)) * np.exp(-np.clip(d - o, 0, None) * 25) * (d >= o)
        return 0.8 * (beat(0) + 0.7 * beat(0.28))

    def lowpass(x, k):
        return np.convolve(x, np.ones(k) / k, mode="same")

    def creak():  # slow wooden door creak: wobbling sawtooth through a lowpass
        d = np.arange(int(1.8 * SR)) / SR
        f = 210 + 60 * np.sin(2 * np.pi * 1.3 * d) + 25 * np.sin(2 * np.pi * 7 * d)
        saw = 2 * ((np.cumsum(f) / SR) % 1.0) - 1
        return 0.22 * lowpass(saw, 6) * np.clip(d * 6, 0, 1) * np.exp(-d * 0.9)

    def thunder():
        d = np.arange(int(3.0 * SR)) / SR
        rumble = lowpass(rng.normal(0, 1, len(d)), 300) * 9
        return 0.9 * rumble * np.exp(-d * 1.1) * np.clip(d * 8, 0, 1)

    def static():
        d = np.arange(int(0.22 * SR)) / SR
        return 0.12 * rng.normal(0, 1, len(d)) * (1 - d / 0.22)

    def whoosh():
        d = np.arange(int(0.6 * SR)) / SR
        return 0.25 * lowpass(rng.normal(0, 1, len(d)), 40) * np.sin(np.pi * d / 0.6) ** 2

    def doorbell():
        d = np.arange(int(1.6 * SR)) / SR
        ding = np.sin(2 * np.pi * 659 * d) * np.exp(-d * 3)
        dong = np.where(d > 0.45, np.sin(2 * np.pi * 523 * (d - 0.45)) * np.exp(-(d - 0.45) * 2.5), 0)
        return 0.22 * (ding + dong)

    def paper():
        d = np.arange(int(0.5 * SR)) / SR
        nz = rng.normal(0, 1, len(d))
        return 0.18 * (nz - lowpass(nz, 4)) * np.exp(-d * 5) * (0.6 + 0.4 * np.sin(d * 90))

    def steps():  # four slow footsteps
        out_ = np.zeros(int(2.6 * SR), np.float32)
        for k in range(4):
            s0 = int(k * 0.62 * SR)
            d = np.arange(int(0.25 * SR)) / SR
            out_[s0:s0 + len(d)] += 0.5 * np.sin(2 * np.pi * 70 * d) * np.exp(-d * 30) * (0.7 + 0.1 * k)
        return out_

    if STORY.get("ambience") == "rain":
        hiss = rng.normal(0, 1, n).astype(np.float32)
        out += 0.05 * (hiss - lowpass(hiss, 5)) * np.clip(tt / 1.5, 0, 1)

    gen = {"buzz": buzz, "knock": knock, "sting": sting, "heartbeat": heartbeat,
           "creak": creak, "thunder": thunder, "static": static, "steps": steps,
           "whoosh": whoosh, "doorbell": doorbell, "paper": paper}
    for kind, t0 in SFX:
        add(gen[kind](), t0)
    for tf in FLASH:
        add(thunder(), tf + 0.25)
    if TRANSITIONS == "static":
        for s in SCENES[1:]:
            add(static(), s["_t"])
    elif TRANSITIONS == "fade":
        for s in SCENES[1:]:
            add(whoosh(), s["_t"] - 0.15)
    pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(pcm.tobytes())


FADE_T = 0.45


def subscribe_card(img, t):
    """End-of-video subscribe call to action: story "subscribe": {"at": anchor (default: last 5 s), "text": line,
    "sub": small line}. The scene dims, a red SUBSCRIBE button pops in, gets 'tapped' and turns to SUBSCRIBED + bell."""
    cfg = STORY["subscribe"] if isinstance(STORY["subscribe"], dict) else {}
    t0 = at(cfg["at"]) if cfg.get("at") else DUR - 5.0
    if t < t0:
        return img
    k = prog(t, t0, 0.4)
    u = min(W, H) / 1080  # scale: 1.0 for vertical 1080x1920 and landscape 1920x1080
    Y = (lambda y: int(y / 1920 * H)) if not LAND else (lambda y: int((y - 520) / 1920 * H * 1.25 + 0.08 * H))
    a = np.asarray(img).astype(np.float32) * (1 - 0.93 * k)  # dark enough that titles underneath don't show through
    img = Image.fromarray(a.astype(np.uint8))
    d = ImageDraw.Draw(img)
    line = cfg.get("text", "NEW SCARY STORY EVERY NIGHT")
    fl = font(F_CAP, int(74 * u))
    c = int(240 * k)
    d.text(((W - d.textlength(line, font=fl)) / 2, Y(720)), line, font=fl, fill=(c, c, c), stroke_width=6, stroke_fill=(0, 0, 0))
    pop = ease(min(1.0, (t - t0) / 0.45)) * (1 + 0.08 * np.exp(-max(0.0, t - t0 - 0.45) * 6))
    tapped = t >= t0 + 1.6
    bw, bh = int(640 * u * pop), int(150 * u * pop)
    if bw > 20:
        bx, by = (W - bw) // 2, Y(880) + (int(150 * u) - bh) // 2
        d.rounded_rectangle((bx, by, bx + bw, by + bh), bh // 2, fill=(70, 70, 74) if tapped else (215, 20, 20))
        lab = "SUBSCRIBED" if tapped else "SUBSCRIBE"
        fb = font(F_BOLD, max(10, int(60 * u * pop)))
        tw = d.textlength(lab, font=fb) + (80 * u * pop if tapped else 0)
        tx = bx + (bw - tw) / 2
        if tapped:  # bell icon inside the button, ringing for a moment after the tap
            sw = 8 * np.sin((t - t0 - 1.6) * 30) * np.exp(-(t - t0 - 1.6) * 3)
            cx, cy = int(tx + 28 + sw), int(by + bh / 2)
            d.pieslice((cx - 26, cy - 30, cx + 26, cy + 22), 180, 360, fill=(255, 215, 120))
            d.rectangle((cx - 26, cy - 5, cx + 26, cy + 14), fill=(255, 215, 120))
            d.ellipse((cx - 7, cy + 14, cx + 7, cy + 28), fill=(255, 215, 120))
            tx += 80 * u * pop
        d.text((tx, by + bh / 2 - 35 * u * pop), lab, font=fb, fill=(255, 255, 255))
        if not tapped and t >= t0 + 1.0:  # finger tap circle
            r = int(40 + 30 * prog(t, t0 + 1.0, 0.6))
            d.ellipse((W // 2 + 170 - r, by + bh // 2 - r, W // 2 + 170 + r, by + bh // 2 + r), outline=(255, 255, 255), width=6)
    sub = cfg.get("sub", "so you never miss the next one")
    if tapped and sub:
        fs = font(F_BOLD, int(42 * u))
        d.text(((W - d.textlength(sub, font=fs)) / 2, Y(1080)), sub, font=fs, fill=(205, 205, 210))
    return img


def beat_zoom(img, t, s):
    """Footage never sits still longer than `beat_zoom` seconds: alternate a quick punch-in / punch-out on clip scenes."""
    n = float(STORY.get("beat_zoom") or 0)
    if not n or s["type"] not in ("clip", "stage") or VOICE_END and t > VOICE_END:
        return img
    k = int((t - s["_t"]) // n)
    z0, z1 = (1.0, 1.07) if k % 2 == 0 else (1.07, 1.0)
    if k == 0:
        z0 = z1 = 1.0
    z = z0 + (z1 - z0) * ease(min(1.0, ((t - s["_t"]) - k * n) / 0.35))
    if z <= 1.001:
        return img
    cw, ch = W / z, H / z
    return img.crop((int((W - cw) / 2), int((H - ch) / 2), int((W + cw) / 2), int((H + ch) / 2))).resize((W, H), Image.BILINEAR)


def hook_card(img, t):
    """The on-screen hook, readable at frame 1 (most viewers start muted): story "hook": {"lines": [white, red], "until": s}."""
    hk = STORY.get("hook")
    if not hk or LAND:
        return img
    until = float(hk.get("until", 2.8))
    if t >= until:
        return img
    a = min(1.0, (until - t) / 0.35)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y = int(hk.get("y", 330))
    for k, txt in enumerate(hk["lines"][:2]):
        size = 150
        while size > 70 and d.textlength(txt, font=font(F_CAP, size)) > W - 140:
            size -= 6
        f = font(F_CAP, size)
        col = (255, 255, 255) if k == 0 else (230, 25, 25)
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=col + (int(255 * a),),
               stroke_width=9, stroke_fill=(0, 0, 0, int(255 * a)))
        y += int(size * 1.12)
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def frame(t, i):
    s = current(t)
    img = beat_zoom(SCENE_FN[s["type"]](s, t), t, s)
    idx = SCENES.index(s)
    if TRANSITIONS == "fade" and idx > 0 and t - s["_t"] < FADE_T:  # crossfade from the previous scene
        pv = SCENES[idx - 1]
        img = Image.blend(beat_zoom(SCENE_FN[pv["type"]](pv, t), t, pv), img, ease((t - s["_t"]) / FADE_T))
    img = hook_card(img, t)
    if STORY.get("subscribe"):
        img = subscribe_card(img, t)
    if STORY.get("badge"):
        d = ImageDraw.Draw(img)
        fb = font(F_BOLD, 34)
        bw = d.textlength(STORY["badge"], font=fb) + 50
        bx, by = (40, 36) if LAND else ((W - bw) / 2, 1812)
        d.rounded_rectangle((bx, by, bx + bw, by + 60), 30, fill=(0, 0, 0))
        d.text((bx + 25, by + 10), STORY["badge"], font=fb, fill=(255, 215, 120))
    return post(draw_caption(img, t, s), t, i, s)


COVER_T = 0.5  # first half second = the thumbnail, so YouTube's Shorts frame/cover matches it


def load_cover():
    p_ = os.path.join(EP, "thumbnail.png")
    if LAND or not STORY.get("cover", True) or not os.path.exists(p_):
        return None
    return np.asarray(Image.open(p_).convert("RGB").resize((W, H))).astype(np.float32)


def stills(path, times):
    tw_, th_ = (480, 270) if LAND else (270, 480)
    ims = [Image.fromarray(frame(t, int(t * FPS))).resize((tw_, th_)) for t in times]
    cols = 4
    sheet = Image.new("RGB", (tw_ * cols, th_ * ((len(ims) + cols - 1) // cols)))
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % cols) * tw_, (k // cols) * th_))
    sheet.save(path)


def main():
    out = os.path.join(EP, "short.mp4")
    if "--preview" in sys.argv:  # one contact sheet: a frame mid-way through each scene
        times = [min(DUR - 0.1, (s["_t"] + min(s["_end"], DUR)) / 2 + 0.6) for s in SCENES]
        stills(os.path.join(EP, "preview.png"), times)
        print(f"preview.png  scenes={len(SCENES)}  duration={DUR:.1f}s")
        return
    sfx = os.path.join(EP, "sfx.wav")
    build_sfx(sfx)
    proc = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", os.path.join(EP, "voice.mp3"), "-i", sfx,
        "-filter_complex",
        f"[1:a]atempo={SPEED},volume=1.6[v];[2:a]volume=0.9[s];"
        "[v][s]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-preset", "slow", "-crf", "26", "-tune", "grain", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR:.2f}", "-movflags", "+faststart", out,
    ], stdin=subprocess.PIPE)
    cover = load_cover()
    for i in range(NFRAMES):
        t = i / FPS
        fr = frame(t, i)
        if cover is not None and t < COVER_T:
            k = max(0.0, (t - 0.32) / (COVER_T - 0.32))
            fr = (cover * (1 - k) + fr.astype(np.float32) * k).astype(np.uint8)
        proc.stdin.write(fr.tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"done {out}  {DUR:.1f}s  {os.path.getsize(out) / 1e6:.0f} MB")


if __name__ == "__main__":
    main()
