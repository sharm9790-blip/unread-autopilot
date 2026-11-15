#!/usr/bin/env python3
"""Paid AI visuals through fal.ai, with a hard daily spending cap.

    image(prompt, out_jpg)                    FLUX.2 dev still, 1080x1920, house horror style added
    video(image_url, motion, out_mp4, dur=6)  Boreal 720p 9:16 clip animated from that still

Key: env FAL_KEY, else ~/.config/fal/key. Cap: env FAL_DAILY_CAP (USD per IST day, default 0.64).
Every charge is logged in state/fal_spend.json (committed by the workflow), so the cap holds across runs.
Raises Unavailable when there is no key, the cap would be crossed, or fal fails, so callers can fall back
to free Pixabay footage + parallax and the daily run never breaks.

    python3 pipeline/falgen.py --prices             # live unit prices for the models we use
    python3 pipeline/falgen.py --test "prompt"      # one image + one clip into ./fal_test_*
"""
import datetime
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "..", "state", "fal_spend.json")
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
IMAGE_MODEL = os.environ.get("FAL_IMAGE_MODEL", "fal-ai/flux-2")
VIDEO_MODEL = os.environ.get("FAL_VIDEO_MODEL", "creatify/boreal")
# fallback prices if the pricing API is unreachable (USD); deliberately on the high side
FAST_IMAGE_MODEL = os.environ.get("FAL_FAST_IMAGE_MODEL", "fal-ai/flux/schnell")  # cheap in-between 2D pictures
FALLBACK = {"fal-ai/flux-2": ("megapixels", 0.015), "creatify/boreal": ("seconds", 0.012),
            "fal-ai/flux/schnell": ("megapixels", 0.003)}
STYLE = ("Realistic cinematic horror film still, vertical 9:16 frame, dark low-key lighting, deep shadows, "
         "muted desaturated colors, subtle 35mm film grain, shallow depth of field, photographic, eerie and quiet. "
         "No text, no watermark, no captions, no logos.")
# 2D + 2.5D look (story "look": "2d"): illustrated storybook horror, one fixed style so the channel is recognisable
STYLE_2D = ("Dark 2D illustrated horror storybook art, hand-painted digital illustration, flat shapes with soft "
            "painterly shading, heavy black shadows, limited palette of deep navy, teal and dim amber light, "
            "clean silhouettes, subtle paper texture, vertical 9:16 frame, eerie and quiet, no gore. "
            "No text, no watermark, no captions, no logos.")
_lock = threading.Lock()


class Unavailable(Exception):
    pass


def key():
    k = os.environ.get("FAL_KEY", "").strip()
    if not k:
        p = os.path.expanduser("~/.config/fal/key")
        k = open(p).read().strip() if os.path.exists(p) else ""
    return k


def _ctx():
    try:
        import ssl, certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # noqa: BLE001
        return None


def _req(url, payload=None, method=None, timeout=120):
    k = key()
    if not k:
        raise Unavailable("no FAL_KEY")
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(url, data=data, method=method or ("POST" if data else "GET"),
                               headers={"Authorization": f"Key {k}", "Content-Type": "application/json",
                                        "User-Agent": "unread-autopilot"})
    try:
        with urllib.request.urlopen(r, timeout=timeout, context=_ctx()) as resp:
            return json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:300]
        raise Unavailable(f"fal HTTP {e.code} on {url.split('?')[0]}: {body}") from None
    except urllib.error.URLError as e:
        raise Unavailable(f"fal unreachable: {e.reason}") from None


_PRICES = {}


def price(model):
    """(unit, unit_price) from fal's pricing API, cached; FALLBACK if that fails."""
    if model not in _PRICES:
        try:
            p = _req(f"https://api.fal.ai/v1/models/pricing?endpoint_id={model}")["prices"][0]
            _PRICES[model] = (str(p["unit"]).lower(), float(p["unit_price"]))
        except Exception:  # noqa: BLE001
            _PRICES[model] = FALLBACK.get(model, ("unknown", 0.05))
    return _PRICES[model]


def cost(model, megapixels=0.0, seconds=0.0):
    unit, up = price(model)
    if "pixel" in unit:
        import math
        return up * max(1, math.ceil(megapixels))
    if "second" in unit:
        return up * seconds
    if "image" in unit or "video" in unit or "request" in unit or "generation" in unit:
        return up
    return FALLBACK.get(model, (None, 0.05))[1] * max(1.0, seconds or megapixels)


def _today():
    return datetime.datetime.now(IST).date().isoformat()


def _ledger():
    try:
        return json.load(open(LEDGER))
    except Exception:  # noqa: BLE001
        return {}


def spent_today():
    return round(float(_ledger().get(_today(), {}).get("usd", 0.0)), 4)


def cap():
    return float(os.environ.get("FAL_DAILY_CAP", "0.64"))


def _reserve(usd, what):
    """Book the estimated cost before calling fal; refuse if it would cross today's cap."""
    with _lock:
        led = _ledger()
        day = led.setdefault(_today(), {"usd": 0.0, "items": []})
        if day["usd"] + usd > cap() + 1e-9:
            raise Unavailable(f"daily cap ${cap():.2f} reached (spent ${day['usd']:.2f}, next {what} ${usd:.3f})")
        day["usd"] = round(day["usd"] + usd, 4)
        day["items"].append({"what": what, "usd": round(usd, 4), "at": datetime.datetime.now(IST).strftime("%H:%M")})
        for old in sorted(led)[:-60]:  # keep ~2 months
            led.pop(old)
        os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
        json.dump(led, open(LEDGER, "w"), indent=1)


def _refund(usd, what):
    with _lock:
        led = _ledger()
        day = led.get(_today())
        if day:
            day["usd"] = round(max(0.0, day["usd"] - usd), 4)
            day["items"].append({"what": f"refund {what}", "usd": -round(usd, 4)})
            json.dump(led, open(LEDGER, "w"), indent=1)


def _run(model, payload, timeout=900):
    """fal queue: submit, poll, fetch. Robust for multi-minute video jobs."""
    sub = _req(f"https://queue.fal.run/{model}", payload)
    status_url, resp_url = sub.get("status_url"), sub.get("response_url")
    if not status_url:
        raise Unavailable(f"fal queue gave no status url: {str(sub)[:200]}")
    t0 = time.time()
    while time.time() - t0 < timeout:
        st = _req(status_url).get("status")
        if st == "COMPLETED":
            return _req(resp_url)
        if st not in ("IN_QUEUE", "IN_PROGRESS"):
            raise Unavailable(f"fal job {st}")
        time.sleep(4)
    raise Unavailable(f"fal job timed out after {timeout}s")


def _download(url, out):
    r = urllib.request.Request(url, headers={"User-Agent": "unread-autopilot"})
    with urllib.request.urlopen(r, timeout=300, context=_ctx()) as resp:
        data = resp.read()
    if len(data) < 10_000:
        raise Unavailable(f"fal file too small ({len(data)} bytes)")
    open(out, "wb").write(data)


def image(prompt, out, w=1088, h=1920, style=True, look="cinematic", fast=False):
    """FLUX.2 dev still -> out (jpeg). Returns {"url", "usd", "model"}. 1088 wide (multiple of 16); parallax crops.
    look="2d" -> STYLE_2D; fast=True -> FLUX schnell (~1/7 the price) for in-between pictures."""
    model = FAST_IMAGE_MODEL if fast else IMAGE_MODEL
    usd = cost(model, megapixels=w * h / 1e6)
    _reserve(usd, f"image {model}")
    sty = STYLE_2D if look == "2d" else STYLE
    try:
        r = _run(model, {"prompt": f"{prompt.strip()}. {sty}" if style else prompt,
                               "image_size": {"width": w, "height": h}, "num_images": 1,
                               "output_format": "jpeg", "enable_safety_checker": True}, timeout=300)
        if any(r.get("has_nsfw_concepts") or []):
            raise Unavailable("image flagged by fal safety checker")
        url = r["images"][0]["url"]
        _download(url, out)
    except Exception as e:
        _refund(usd, "image")
        raise e if isinstance(e, Unavailable) else Unavailable(f"image failed: {e}")
    return {"url": url, "usd": round(usd, 4), "model": model}


def video(image_url, motion, out, dur=6.0):
    """Boreal 720p 9:16 clip that starts on image_url. motion = what moves (camera + subject), keep it subtle."""
    usd = cost(VIDEO_MODEL, seconds=dur)
    _reserve(usd, f"video {VIDEO_MODEL} {dur:g}s")
    try:
        r = _run(VIDEO_MODEL, {
            "prompt": f"[VISUAL] {motion.strip()}. Slow, subtle, realistic motion; the camera barely moves; "
                      f"keep the scene, lighting and composition of the first frame. Dark cinematic horror mood. "
                      f"[SOUNDS] quiet room tone.",
            "image_url": image_url, "duration": float(dur), "resolution": "720p", "aspect_ratio": "9:16"})
        _download(r["video"]["url"], out)
    except Exception as e:
        _refund(usd, "video")
        raise e if isinstance(e, Unavailable) else Unavailable(f"video failed: {e}")
    return {"url": r["video"]["url"], "usd": round(usd, 4), "model": VIDEO_MODEL}


if __name__ == "__main__":
    if "--prices" in sys.argv:
        for m in (IMAGE_MODEL, VIDEO_MODEL):
            u, p = price(m)
            print(f"{m}: ${p} per {u}  ->  one 1088x1920 image ${cost(m, megapixels=2.09):.3f}" if m == IMAGE_MODEL
                  else f"{m}: ${p} per {u}  ->  one 6 s clip ${cost(m, seconds=6):.3f}")
        print(f"spent today ${spent_today():.3f} of cap ${cap():.2f}")
    elif "--test" in sys.argv:
        prompt = sys.argv[sys.argv.index("--test") + 1]
        im = image(prompt, "fal_test_image.jpg")
        print("image", im)
        print("video", video(im["url"], "the shadow in the doorway slowly leans forward", "fal_test_clip.mp4", 6))
        print(f"spent today ${spent_today():.3f}")
