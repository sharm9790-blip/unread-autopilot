#!/usr/bin/env python3
"""Free "2.5D" parallax: turn one still image into a short moving clip (no AI video credits).

A depth map says how far away each pixel is; the virtual camera then moves so near things shift
more than far things, which reads as real camera motion on a phone. The result is a plain .mp4
you drop into story.json as a {"type": "clip", "file": ...} scene, or use in any other pipeline.

    python3 pipeline/parallax.py photo.jpg out.mp4 --move dolly-in --dur 5
    python3 pipeline/parallax.py photo.jpg out.mp4 --move pan-right --strength 0.05 --fog 0.35 --dust 60
    python3 pipeline/parallax.py photo.jpg --depth-only        # just write photo.depth.png

Moves: dolly-in, dolly-out, pan-left, pan-right, rise, fall, orbit, sway (sway loops seamlessly).

Depth: uses <image>.depth.png if it exists (white = near). Otherwise runs Depth Anything V2 Small
(pip install torch transformers; ~100 MB model, fine on an 8 GB M1 or a CPU runner) and saves
that PNG for next time, so you can compute depth on the Mac once and commit it. If neither is
available it falls back to a simple "bottom is near" guess (a gentler, still usable effect).
Only numpy + Pillow + ffmpeg are required to render.
"""
import argparse
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

try:
    import cv2  # optional: ~5x faster remap
except Exception:  # noqa: BLE001
    cv2 = None

MOVES = ("dolly-in", "dolly-out", "pan-left", "pan-right", "rise", "fall", "orbit", "sway")


# ---------- depth ----------

def model_depth(img):
    """Depth Anything V2 Small -> float32 HxW, 1 = near, 0 = far. None if the libraries are missing."""
    try:
        import certifi
        os.environ.setdefault("SSL_CERT_FILE", certifi.where())  # system Python on this Mac has no certs
        os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())
    except Exception:  # noqa: BLE001
        pass
    os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")  # bicubic resize op is missing on MPS (torch 2.4)
    try:
        import torch
        from transformers import pipeline
    except Exception:  # noqa: BLE001
        return None
    dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    pipe = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device=dev)
    small = img.copy()
    small.thumbnail((1024, 1024))
    out = pipe(small)["predicted_depth"]
    d = out.squeeze().detach().float().cpu().numpy()  # relative inverse depth: bigger = nearer
    return np.array(Image.fromarray(d).resize(img.size, Image.BICUBIC), np.float32)


def guess_depth(img):
    """No model: bottom of frame near, top far, nudged by brightness (sky/light tends to be far)."""
    w, h = img.size
    y = np.linspace(0, 1, h, dtype=np.float32)[:, None].repeat(w, 1)
    lum = np.asarray(img.convert("L").filter(ImageFilter.GaussianBlur(25)), np.float32) / 255
    return y * 0.8 + (1 - lum) * 0.2


def normalize(d):
    lo, hi = np.percentile(d, 2), np.percentile(d, 98)
    return np.clip((d - lo) / max(hi - lo, 1e-6), 0, 1).astype(np.float32)


def load_depth(path, img, quiet=False):
    """Cached PNG -> model (then cache) -> heuristic. Returns (depth 0..1 at img size, source label)."""
    cache = os.path.splitext(path)[0] + ".depth.png"
    if os.path.exists(cache):
        d = Image.open(cache).convert("L").resize(img.size, Image.BICUBIC)
        return np.asarray(d, np.float32) / 255, "cached " + os.path.basename(cache)
    d = model_depth(img)
    if d is None:
        if not quiet:
            print("  (torch/transformers not installed: using simple bottom-near depth guess)", file=sys.stderr)
        return normalize(guess_depth(img)), "heuristic"
    d = normalize(d)
    Image.fromarray((d * 255).astype(np.uint8)).save(cache)
    return d, "Depth Anything V2 (saved " + os.path.basename(cache) + ")"


def soften(d, size):
    """Blur + grow near regions slightly so foreground edges stretch instead of tearing."""
    im = Image.fromarray((d * 255).astype(np.uint8))
    im = im.filter(ImageFilter.MaxFilter(max(3, (size // 400) | 1)))
    im = im.filter(ImageFilter.GaussianBlur(max(2, size // 300)))
    return np.asarray(im, np.float32) / 255


# ---------- camera ----------

def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def camera(move, u, s):
    """Camera state at progress u (0..1): (shift_x, shift_y, zoom). s = strength."""
    e = ease(u)
    if move == "dolly-in":
        return 0.0, 0.0, s * 1.6 * e
    if move == "dolly-out":
        return 0.0, 0.0, s * 1.6 * (1 - e)
    if move == "pan-left":
        return s * (1 - 2 * e), 0.0, s * 0.3
    if move == "pan-right":
        return -s * (1 - 2 * e), 0.0, s * 0.3
    if move == "rise":
        return 0.0, -s * (1 - 2 * e), s * 0.3
    if move == "fall":
        return 0.0, s * (1 - 2 * e), s * 0.3
    if move == "orbit":
        return -s * np.cos(np.pi * e), 0.0, s * 0.6 * e
    if move == "sway":  # full loop: start == end
        a = 2 * np.pi * u
        return s * np.sin(a), s * 0.35 * np.sin(2 * a), s * 0.4 * (1 - np.cos(a)) / 2
    raise ValueError(move)


def remap(src, mx, my):
    if cv2 is not None:
        return cv2.remap(src, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    h, w = src.shape[:2]
    mx = np.clip(mx, 0, w - 1.001)
    my = np.clip(my, 0, h - 1.001)
    x0, y0 = mx.astype(np.int32), my.astype(np.int32)
    fx, fy = (mx - x0)[..., None], (my - y0)[..., None]
    a, b = src[y0, x0], src[y0, x0 + 1]
    c, d = src[y0 + 1, x0], src[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


class Parallax:
    """Precomputes the enlarged source + depth once; frame(u) renders progress u in 0..1."""

    def __init__(self, img, depth, size, move, strength, focus, margin):
        W, H = size
        self.W, self.H, self.move, self.s, self.focus = W, H, move, strength, focus
        # cover-crop the photo to the output aspect, at (1 + margin) x output size so moves never show edges
        sw, sh = int(W * (1 + margin)), int(H * (1 + margin))
        iw, ih = img.size
        k = max(sw / iw, sh / ih)
        cw, ch = sw / k, sh / k
        box = ((iw - cw) / 2, (ih - ch) / 2, (iw + cw) / 2, (ih + ch) / 2)
        self.src = np.asarray(img.convert("RGB").resize((sw, sh), Image.LANCZOS, box=box), np.float32)
        dimg = Image.fromarray((depth * 255).astype(np.uint8)).resize((sw, sh), Image.BICUBIC, box=box)
        self.dep = soften(np.asarray(dimg, np.float32) / 255, max(sw, sh))
        self.sw, self.sh = sw, sh
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
        self.ux = (xs - W / 2) / (W / 2)  # output pixel in -1..1 (x relative to half-width)
        self.uy = (ys - H / 2) / (W / 2)  # same scale on y so motion is isotropic

    def _sample_depth(self, px, py):
        if cv2 is not None:
            return cv2.remap(self.dep, px, py, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        return remap(self.dep[..., None], px, py)[..., 0]

    def frame(self, u):
        sx, sy, z = camera(self.move, u, self.s)
        cx, cy, half = self.sw / 2, self.sh / 2, self.W / 2
        d = np.full(self.ux.shape, self.focus, np.float32)
        for _ in range(3):  # fixed-point: look up depth where we'll actually sample from
            rel = d - self.focus  # focus plane stays put; nearer moves with camera, farther against it
            scale = 1 + z * (0.35 + d)  # near things grow faster on a dolly
            px = cx + ((self.ux - sx * rel) / scale) * half
            py = cy + ((self.uy - sy * rel) / scale) * half
            d = self._sample_depth(px.astype(np.float32), py.astype(np.float32))
        return remap(self.src, px.astype(np.float32), py.astype(np.float32))


# ---------- atmosphere (all procedural, free) ----------

def fog_layer(W, H, seed=7):
    """Soft value-noise field, 2W wide, that wraps horizontally so it can scroll forever."""
    rng = np.random.default_rng(seed)
    field = np.zeros((H, W * 2), np.float32)
    for gx, gy, wgt in ((6, 10, 0.55), (14, 24, 0.3), (32, 56, 0.15)):
        n = rng.random((gy, gx), dtype=np.float32)
        n = np.concatenate([n, n[:, :1]], 1)  # wrap so the scroll seam is invisible
        field += np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W * 2, H), Image.BICUBIC), np.float32) / 255 * wgt
    return field


class Atmosphere:
    def __init__(self, W, H, fog, dust, grain, vignette, depth_out=None, seed=7):
        self.W, self.H, self.fog, self.grain = W, H, fog, grain
        self.rng = np.random.default_rng(seed)
        self.field = fog_layer(W, H, seed) if fog > 0 else None
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xs - W / 2) / (W / 2)) ** 2 + ((ys - H / 2) / (H / 2)) ** 2)
        self.vig = (1 - vignette * np.clip(r - 0.35, 0, 1) ** 1.6)[..., None].astype(np.float32)
        n = int(dust)
        self.dust = np.column_stack([self.rng.random(n) * W, self.rng.random(n) * H, self.rng.random(n) * 2.2 + 0.8,
                                     self.rng.random(n) * 0.6 + 0.4, self.rng.random(n) * 6.28]) if n else None

    def apply(self, a, t, dur):
        if self.field is not None:
            off = int((t / max(dur, 0.1)) * self.W * 0.35) % self.W
            f = self.field[:, off:off + self.W]
            f = np.clip((f - 0.35) * 1.8, 0, 1)[..., None] * self.fog
            a = a * (1 - f * 0.7) + 205 * f * 0.7
        if self.dust is not None:
            x, y, rad, al, ph = self.dust.T
            px = (x + 14 * np.sin(t * 0.7 + ph) + t * 9) % self.W
            py = (y - t * 22 * al) % self.H
            for xx, yy, rr, aa in zip(px.astype(int), py.astype(int), rad, al * (0.6 + 0.4 * np.sin(t * 2 + ph))):
                r = int(rr) + 1
                y0, y1, x0, x1 = max(yy - r, 0), min(yy + r + 1, self.H), max(xx - r, 0), min(xx + r + 1, self.W)
                if y1 > y0 and x1 > x0:
                    a[y0:y1, x0:x1] = a[y0:y1, x0:x1] * (1 - aa * 0.5) + 235 * aa * 0.5
        a = a * self.vig
        if self.grain:
            a = a + self.rng.normal(0, self.grain, (self.H // 2, self.W // 2, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1)
        return a


# ---------- main ----------

def render(image, out, move="dolly-in", dur=5.0, fps=30, size=(1080, 1920), strength=0.06, focus=0.35,
           margin=None, fog=0.0, dust=0, grain=6.0, vignette=0.45, crf=18, quiet=False):
    img = Image.open(image).convert("RGB")
    depth, how = load_depth(image, img, quiet)
    if margin is None:
        margin = min(0.45, strength * 3.2 + 0.06)
    if not quiet:
        print(f"  depth: {how}; move {move}, {dur}s @ {fps}fps, {size[0]}x{size[1]}", file=sys.stderr)
    px = Parallax(img, depth, size, move, strength, focus, margin)
    atm = Atmosphere(size[0], size[1], fog, dust, grain, vignette)
    n = max(1, int(round(dur * fps)))
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{size[0]}x{size[1]}", "-r", str(fps), "-i", "-",
                            "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p",
                            "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(n):
        u = i / n if move == "sway" else i / max(n - 1, 1)
        a = atm.apply(px.frame(u), i / fps, dur)
        enc.stdin.write(np.clip(a, 0, 255).astype(np.uint8).tobytes())
        if not quiet and i % fps == 0:
            print(f"\r  frame {i}/{n}", end="", file=sys.stderr)
    enc.stdin.close()
    if enc.wait():
        raise SystemExit("ffmpeg failed")
    if not quiet:
        print(f"\r  wrote {out}            ", file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("out", nargs="?", help="output .mp4 (default: <image>.parallax.mp4)")
    ap.add_argument("--move", choices=MOVES, default="dolly-in")
    ap.add_argument("--dur", type=float, default=5.0)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--size", default="1080x1920", help="WxH; 1920x1080 for long-form")
    ap.add_argument("--strength", type=float, default=0.06, help="0.03 subtle, 0.06 normal, 0.10 dramatic")
    ap.add_argument("--focus", type=float, default=0.35, help="depth (0 far..1 near) that stays still")
    ap.add_argument("--fog", type=float, default=0.0, help="drifting fog 0..1 (0.3 is moody)")
    ap.add_argument("--dust", type=int, default=0, help="floating dust/ember particles (e.g. 60)")
    ap.add_argument("--grain", type=float, default=6.0)
    ap.add_argument("--vignette", type=float, default=0.45)
    ap.add_argument("--depth-only", action="store_true", help="just compute and save <image>.depth.png")
    a = ap.parse_args()
    if a.depth_only:
        img = Image.open(a.image).convert("RGB")
        print(load_depth(a.image, img)[1])
        return
    w, h = (int(v) for v in a.size.lower().split("x"))
    out = a.out or os.path.splitext(a.image)[0] + ".parallax.mp4"
    render(a.image, out, a.move, a.dur, a.fps, (w, h), a.strength, a.focus, None, a.fog, a.dust, a.grain, a.vignette)


if __name__ == "__main__":
    main()
