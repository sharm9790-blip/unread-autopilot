"""Produce and schedule one day of Shorts (runs in GitHub Actions; also works on the Mac).

Usage: python3 pipeline/produce.py daily/<YYYY-MM-DD> [--no-upload]
For each episode: Pixabay clips -> ElevenLabs voice -> thumbnail -> render -> upload scheduled at its slot.
Then: link 2-part series, update stories_index.json + state/, and send the Telegram report.
Env: PIXABAY_API_KEY, ELEVENLABS_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID (+ YouTube token files in ~/.config/scary-short).
"""
import datetime
import html
import io
import json
import os
import subprocess
import sys
import traceback
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
VOICE = os.environ.get("VOICE_ID", "BycOlIr9Aytiubl0LIIY")  # Gxl
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
DAY = sys.argv[1].rstrip("/")
UPLOAD = "--no-upload" not in sys.argv
day = json.load(open(os.path.join(DAY, "day.json")))
USED_P = os.path.join(ROOT, "state", "used_clips.json")
IG_LOCK = threading.Lock()  # ig_queue.json is written from 3 worker threads
used_clips = set(json.load(open(USED_P))) if os.path.exists(USED_P) else set()


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (unread-autopilot)"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    return data if binary else json.loads(data)


def brightness(url):
    from PIL import Image, ImageStat
    try:
        return ImageStat.Stat(Image.open(io.BytesIO(get(url, True))).convert("L")).mean[0]
    except Exception:
        return 80


MOOD = {"dark", "night", "scary", "creepy", "horror", "empty", "spooky", "old"}
NO = ("anime", "cartoon", "animation", "animated", "3d", "render", "christmas", "cute", "kawaii", "deer", "cooking", "food", "wedding", "party")


def crop_w(v):
    """Width of the 9:16 crop a rendition gives (the Short is 1080 wide; below ~900 it looks soft)."""
    return min(v.get("width") or 0, (v.get("height") or 0) * 9 / 16)


def sharp(h):
    """Smallest Pixabay rendition whose vertical crop is >= 900 px wide (medium was 405 px -> 2.7x upscale);
    else the sharpest one available. Skips 4K when a lighter file is already sharp enough."""
    vs = [h["videos"][k] for k in ("medium", "large", "xlarge") if h["videos"].get(k, {}).get("url")]
    return next((v for v in vs if crop_w(v) >= 900), max(vs, key=crop_w))


def fetch_clip(query, dest):
    """Best Pixabay hit: the query's nouns in its tags first (searching the full query and the nouns alone), then mood
    words; long enough, not reused, not cartoon, not black/blown-out."""
    key = os.environ["PIXABAY_API_KEY"]
    if isinstance(query, int) or str(query).isdigit():  # the writer pinned an exact Pixabay video id
        h = get(f"https://pixabay.com/api/videos/?key={key}&id={int(query)}")["hits"][0]
        v = sharp(h)
        open(dest, "wb").write(get(v["url"], True))
        used_clips.add(h["id"])
        return {"id": h["id"], "user": h["user"], "query": query, "tags": h.get("tags", "")}
    words = [w for w in query.lower().split() if len(w) > 2]
    nouns = [w for w in words if w not in MOOD] or words
    hits, seen = [], set()
    for q in dict.fromkeys([query, " ".join(nouns)]):
        for h in get(f"https://pixabay.com/api/videos/?key={key}&q={urllib.parse.quote(q)}&per_page=20&safesearch=true")["hits"]:
            if h["id"] not in seen:
                seen.add(h["id"])
                hits.append(h)
    has = lambda h, w: w.rstrip("s") in h.get("tags", "").lower()
    score = lambda h: 3 * sum(has(h, w) for w in nouns) + sum(has(h, w) for w in words if w in MOOD) \
        + (1 if crop_w(sharp(h)) >= 1000 else 0)  # tie-break toward footage that stays sharp in a 9:16 crop
    ok = [h for h in hits if h["id"] not in used_clips and h["duration"] >= 4 and not any(n in h.get("tags", "").lower() for n in NO)]
    ranked = sorted(ok, key=lambda h: -score(h))
    vid = sharp
    pick = next((h for h in ranked[:8] if 30 <= brightness(vid(h)["thumbnail"]) <= 165), ranked[0] if ranked else None)
    if not pick:
        info = fetch_photo({"photo": query}, dest, 0)  # no usable footage: animate a still instead (free parallax)
        info["fallback"] = "no Pixabay video"
        return info
    open(dest, "wb").write(get(vid(pick)["url"], True))
    used_clips.add(pick["id"])
    return {"id": pick["id"], "user": pick["user"], "query": query, "tags": pick.get("tags", "")}


PHOTO_MOVES = ("dolly-in", "orbit", "pan-right", "rise", "pan-left")
# cut-outs come down with junk where the transparency was, and parallax smears it into streaks
PHOTO_NO = ("isolated", "transparent", "png", "cutout", "cut out", "clipart", "clip art", "vector", "illustration", "white background")


def fetch_photo(spec, dest, i, log=None):
    """Pixabay still -> 2.5D parallax clip (pipeline/parallax.py), no AI video credits.
    spec: {"photo": "query words" or numeric image id, optional "move", "dur" (default 10 s), "strength", "fog", "dust"}."""
    key = os.environ["PIXABAY_API_KEY"]
    q = spec["photo"]
    if isinstance(q, int) or str(q).isdigit():
        hits = get(f"https://pixabay.com/api/?key={key}&id={int(q)}")["hits"]
    else:
        words = [w for w in str(q).lower().split() if len(w) > 2]
        nouns = [w for w in words if w not in MOOD] or words
        hits, seen = [], set()
        for qq in dict.fromkeys([str(q), " ".join(nouns)]):
            for h in get(f"https://pixabay.com/api/?key={key}&q={urllib.parse.quote(qq)}&image_type=photo"
                         f"&orientation=vertical&per_page=30&safesearch=true")["hits"]:
                if h["id"] not in seen and f"img:{h['id']}" not in used_clips and h["imageHeight"] >= 1600 \
                        and not any(n in h.get("tags", "").lower() for n in NO + PHOTO_NO):
                    seen.add(h["id"])
                    hits.append(h)
        has = lambda h, w: w.rstrip("s") in h.get("tags", "").lower()
        score = lambda h: 3 * sum(has(h, w) for w in nouns) + sum(has(h, w) for w in words if w in MOOD)
        hits.sort(key=lambda h: -score(h))
        if hits and score(hits[0]) > 0:  # stay on topic: only the best-matching tier (within one noun of the top)
            hits = [h for h in hits if score(h) >= max(1, score(hits[0]) - 2)]
        lit = {h["id"]: brightness(h["previewURL"]) for h in hits[:10]}  # horror: prefer dark, then not blown-out
        hits = [next((h for h in hits[:10] if 20 <= lit[h["id"]] <= 100),
                     next((h for h in hits[:10] if lit[h["id"]] <= 150), hits[0]))] if hits else []
    if not hits:
        raise RuntimeError(f"no Pixabay video or photo for {q!r}")
    h = hits[0]
    img = os.path.splitext(dest)[0] + "_photo.jpg"
    open(img, "wb").write(get(h["largeImageURL"], True))
    parallax(img, dest, i, spec, log)
    used_clips.add(f"img:{h['id']}")
    return {"id": h["id"], "user": h["user"], "query": q, "tags": h.get("tags", ""), "kind": "photo-parallax",
            "page": h.get("pageURL", "")}


def parallax(img, dest, i, spec, log=None):
    cmd = ["python3", os.path.join(HERE, "parallax.py"), img, dest,
           "--move", spec.get("move", PHOTO_MOVES[i % len(PHOTO_MOVES)]), "--dur", str(spec.get("dur", 10)),
           "--strength", str(spec.get("strength", 0.07)), "--fog", str(spec.get("fog", 0.2)), "--dust", str(spec.get("dust", 40))]
    run(cmd, log) if log else subprocess.run(cmd, check=True, capture_output=True)


def fetch_ai(spec, dest, i, log=None):
    """{"ai": "<shot description>", "motion": "<what moves>"?, "fallback": "<pixabay words>"?, "move": ...}
    ai only      -> FLUX.2 still (story-specific, native 1080x1920) -> free parallax clip
    ai + motion  -> FLUX.2 still -> Boreal AI video clip (the hero shot); parallax if the clip can't be paid for
    No key / daily cap reached / fal error -> the fallback words as a free Pixabay photo-parallax clip."""
    import falgen
    img = os.path.splitext(dest)[0] + "_ai.jpg"
    try:
        im = falgen.image(spec["ai"], img)
    except falgen.Unavailable as e:
        words = spec.get("fallback") or " ".join(w for w in spec["ai"].split()[:4])
        info = fetch_photo({**{k: v for k, v in spec.items() if k in ("move", "dur", "strength", "fog", "dust")},
                            "photo": words}, dest, i, log)
        return {**info, "fallback": f"fal: {e}"[:160], "usd": 0}
    info = {"kind": "ai-image-parallax", "prompt": spec["ai"], "model": im["model"], "usd": im["usd"]}
    if spec.get("motion"):
        try:
            v = falgen.video(im["url"], spec["motion"], dest, float(spec.get("clip_dur", 6)))
            return {**info, "kind": "ai-video", "motion": spec["motion"], "video_model": v["model"],
                    "usd": round(im["usd"] + v["usd"], 4)}
        except falgen.Unavailable as e:
            info["fallback"] = f"clip: {e}"[:160]
    parallax(img, dest, i, spec, log)
    return info


TARGET_S, MAX_SPEED = 29.5, 1.15  # Shorts <=30 s get ~3x the median views of 31-44 s ones (LEARNINGS.md)


def fit_length(ep):
    """After TTS: speed the voice up (max 1.15x) so voice + end card lands at <=29.5 s. Flags it if still long."""
    sp = os.path.join(ep, "story.json")
    story = json.load(open(sp))
    w = json.load(open(os.path.join(ep, "words.json")))
    w = w.get("words", w) if isinstance(w, dict) else w
    voice, tail = float(w[-1]["end"]), float(story.get("tail", 3.0))
    need = voice / max(TARGET_S - tail, 1.0)
    speed = round(min(MAX_SPEED, max(float(story.get("speed", 1.0)), need)), 3)
    if speed != story.get("speed"):
        story["speed"] = speed
        json.dump(story, open(sp, "w"), indent=1, ensure_ascii=False)
    est = round(voice / speed + tail, 1)
    return {"speed": speed, **({"long": est} if est > 30.5 else {})}


def run(cmd, log):
    r = subprocess.run(cmd, capture_output=True, text=True)
    open(log, "a").write(f"$ {' '.join(cmd)}\n{r.stdout}\n{r.stderr}\n")
    if r.returncode:
        raise RuntimeError(f"{os.path.basename(cmd[1])} failed: {(r.stderr or r.stdout).strip().splitlines()[-1][:200]}")
    return r.stdout


def busy_days():
    """Dates (IST) that already have a scheduled (future publishAt) video on the channel."""
    sys.path.insert(0, HERE)
    from youtube_upload import credentials
    from googleapiclient.discovery import build
    yt = build("youtube", "v3", credentials=credentials())
    up = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, tok = [], None
    for _ in range(4):  # newest 200 uploads cover everything still scheduled
        r = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50, pageToken=tok).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        tok = r.get("nextPageToken")
        if not tok:
            break
    days, now = set(), datetime.datetime.now(IST)
    for k in range(0, len(ids), 50):
        for v in yt.videos().list(part="status", id=",".join(ids[k:k + 50])).execute()["items"]:
            p = v["status"].get("publishAt")
            if p:
                t = datetime.datetime.fromisoformat(p.replace("Z", "+00:00")).astimezone(IST)
                if t > now:
                    days.add(t.date())
    return days


def move_to_free_day():
    """Never double up: if this day already has scheduled posts, shift the batch to the first empty day."""
    busy = busy_days()
    d = max(datetime.date.fromisoformat(day["date"]), datetime.datetime.now(IST).date())
    while d in busy:
        d += datetime.timedelta(days=1)
    if d.isoformat() != day["date"]:
        for slug, t in day["schedule"].items():
            day["schedule"][slug] = d.isoformat() + t[10:]
        day["moved_from"], day["date"] = day["date"], d.isoformat()
        for slug in day["order"]:  # lock screens show the new date
            sp = os.path.join(DAY, slug, "story.json")
            st = json.load(open(sp))
            for sc in st["scenes"]:
                if sc["type"] == "lock":
                    sc["date"] = d.strftime("%A, %B ") + str(d.day)
            json.dump(st, open(sp, "w"), indent=1, ensure_ascii=False)
        json.dump(day, open(os.path.join(DAY, "day.json"), "w"), indent=1)
    return day.get("moved_from")


def publish_time(slug, k):
    """Slot time; if it already passed (late run), push it to now + 30 min + 1 h per episode."""
    t = datetime.datetime.fromisoformat(day["schedule"][slug])
    soon = datetime.datetime.now(IST) + datetime.timedelta(minutes=30 + 60 * k)
    return (t if t > datetime.datetime.now(IST) + datetime.timedelta(minutes=15) else soon).isoformat(timespec="seconds")


def produce(args):
    k, slug = args
    ep = os.path.join(DAY, slug)
    log = os.path.join(ep, "produce.log")
    out = {"slug": slug, "title": json.load(open(os.path.join(ep, "story.json")))["title"]}
    try:
        st = "clips"
        credits = {}
        for i, q in enumerate(day["clips"][slug]):
            f = "clip.mp4" if i == 0 else f"clip{i + 1}.mp4"
            if not os.path.exists(os.path.join(ep, f)):
                if isinstance(q, dict) and "ai" in q:  # paid fal.ai still (+ hero clip), free fallback
                    credits[f] = fetch_ai(q, os.path.join(ep, f), i, log)
                elif isinstance(q, dict) or str(q).startswith("photo:"):  # still photo -> free parallax motion
                    spec = q if isinstance(q, dict) else {"photo": q.split(":", 1)[1].strip()}
                    credits[f] = fetch_photo(spec, os.path.join(ep, f), i, log)
                else:
                    credits[f] = fetch_clip(q, os.path.join(ep, f))
        if credits:
            json.dump(credits, open(os.path.join(ep, "clip_credits.json"), "w"), indent=1)
        out["usd"] = round(sum(float(c.get("usd") or 0) for c in credits.values()), 3)
        out["ai"] = sum(1 for c in credits.values() if str(c.get("kind", "")).startswith("ai"))
        out["fallbacks"] = [c["fallback"] for c in credits.values() if c.get("fallback")]
        st = "voice"
        if not os.path.exists(os.path.join(ep, "words.json")):
            run(["python3", os.path.join(HERE, "tts.py"), ep, "--voice", VOICE], log)
        st = "fit"
        out.update(fit_length(ep))
        st = "render"
        run(["python3", os.path.join(HERE, "thumbnail.py"), ep], log)
        if not os.path.exists(os.path.join(ep, "short.mp4")):
            run(["python3", os.path.join(HERE, "render.py"), ep], log)
        out["seconds"] = round(float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(ep, "short.mp4")],
            capture_output=True, text=True).stdout or 0), 1)
        if UPLOAD and not os.path.exists(os.path.join(ep, "uploaded.json")):
            st = "upload"
            out["at"] = publish_time(slug, k)
            run(["python3", os.path.join(HERE, "youtube_upload.py"), ep, "--publish-at", out["at"]], log)
        if os.path.exists(os.path.join(ep, "uploaded.json")):
            out["url"] = json.load(open(os.path.join(ep, "uploaded.json")))["url"]
        out["at"] = out.get("at", day["schedule"][slug])
        out["ok"] = True
        if UPLOAD and out.get("url"):  # keep an Instagram copy; ig_daily.py posts it the day after YouTube
            try:
                import ig_daily
                with IG_LOCK:
                    ig_daily.stash(ep, out["url"].rstrip("/").split("/")[-1], out["at"])
                out["ig"] = True
            except Exception as e:  # noqa: BLE001 - Instagram is a bonus; never fail the Short over it
                out["ig_error"] = str(e)[:120]
                open(log, "a").write(f"instagram stash failed: {e}\n")
    except Exception as e:
        out.update(ok=False, step=st, error=str(e)[:200])
        open(log, "a").write(traceback.format_exc())
    print(slug, "OK" if out["ok"] else f"FAILED at {out['step']}: {out['error']}", flush=True)
    return out


def link_series():
    names = {}
    for slug in day["order"]:
        st = json.load(open(os.path.join(DAY, slug, "story.json")))
        if st.get("series") and os.path.exists(os.path.join(DAY, slug, "uploaded.json")):
            names.setdefault(st["series"]["name"], []).append(slug)
    res = {}
    for name, parts in names.items():
        d = os.path.join(DAY, "series", name.lower().replace(" ", "-"))
        os.makedirs(d, exist_ok=True)
        for p in parts:
            if not os.path.exists(os.path.join(d, p)):
                os.symlink(os.path.join("..", "..", p), os.path.join(d, p))
        r = subprocess.run(["python3", os.path.join(HERE, "series_link.py"), d], capture_output=True, text=True)
        res[name] = r.returncode == 0
    return res


def channel_stats():
    """Today's channel totals and the change since the last run (state/channel_stats.json)."""
    try:
        sys.path.insert(0, HERE)
        from youtube_upload import credentials
        from googleapiclient.discovery import build
        s = build("youtube", "v3", credentials=credentials()).channels().list(part="statistics", mine=True).execute()["items"][0]["statistics"]
        now = {"views": int(s["viewCount"]), "subs": int(s.get("subscriberCount", 0)), "videos": int(s["videoCount"])}
        p = os.path.join(ROOT, "state", "channel_stats.json")
        last = json.load(open(p)) if os.path.exists(p) else None
        json.dump({**now, "date": day["date"]}, open(p, "w"), indent=1)
        return now, last
    except Exception:
        return None, None


def tg(text):
    tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not tok or not chat:
        print(text)
        return
    data = urllib.parse.urlencode({"chat_id": chat, "text": text, "parse_mode": "HTML",
                                   "disable_web_page_preview": "true"}).encode()
    urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage", data=data), timeout=30)


def k_fmt(n):
    return f"{n / 1000:.1f}K" if n >= 1000 else str(n)


def report(results, series_ok, stats):
    d = datetime.date.fromisoformat(day["date"])
    ok = [r for r in results if r["ok"]]
    head = "✅" if len(ok) == len(results) else ("⚠️" if ok else "❌")
    lines = [f"{head} <b>UNREAD · {d.strftime('%a %d %b')}</b>", f"<b>{len(ok)}/{len(results)} Shorts scheduled</b>"]
    if day.get("moved_from"):
        lines.append(f"<i>📅 {day['moved_from']} already had posts, so this batch moved to {d.strftime('%a %d %b')}</i>")
    lines.append("━━━━━━━━━━━━━━━")
    for r in results:
        title = html.escape(r["title"])
        if r["ok"]:
            t = datetime.datetime.fromisoformat(r["at"]).astimezone(IST).strftime("%H:%M")
            link = f'<a href="{r["url"]}">{title}</a>' if r.get("url") else title
            long = " ⚠️ over 30 s, write shorter" if (r.get("seconds") or 0) > 30.5 else ""
            lines.append(f"🕒 <b>{t}</b>  {link}  <i>{r.get('seconds', '')}s</i>{long}")
        else:
            lines.append(f"❌ {title}\n      <i>failed at {r['step']}: {html.escape(r['error'][:120])}</i>")
    usd, ai = sum(r.get("usd", 0) for r in results), sum(r.get("ai", 0) for r in results)
    fb = [f for r in results for f in r.get("fallbacks", [])]
    if usd or ai or fb:
        import falgen
        lines += ["━━━━━━━━━━━━━━━", f"🎨 AI visuals: <b>{ai}</b> · fal spend <b>${usd:.2f}</b> "
                  f"(today ${falgen.spent_today():.2f} of ${falgen.cap():.2f} cap)"]
        if fb:
            lines.append(f"<i>↩️ {len(fb)} fell back to free footage: {html.escape(fb[0][:90])}</i>")
    ig = sum(1 for r in results if r.get("ig"))
    ige = [r["ig_error"] for r in results if r.get("ig_error")]
    if ig or ige:
        lines.append(f"📸 {ig} saved for Instagram (posted the day after YouTube)"
                     + (f" · <i>{len(ige)} failed: {html.escape(ige[0][:80])}</i>" if ige else ""))
    if series_ok:
        lines += ["━━━━━━━━━━━━━━━"] + [f"🔗 Series <b>{html.escape(n)}</b> {'linked' if v else 'link failed'}"
                                         for n, v in series_ok.items()]
    now, last = stats
    if now:
        lines.append("━━━━━━━━━━━━━━━")
        if last:
            lines.append(f"📈 Since last run: <b>+{k_fmt(now['views'] - last['views'])}</b> views · "
                         f"<b>{now['subs'] - last['subs']:+d}</b> subs")
        lines.append(f"👥 {k_fmt(now['subs'])} subscribers · {k_fmt(now['views'])} total views")
    tg("\n".join(lines))


if __name__ == "__main__":
    try:
        if UPLOAD:
            move_to_free_day()
        results = list(ThreadPoolExecutor(3).map(produce, enumerate(day["order"])))
        series_ok = link_series() if UPLOAD else {}
        idx_p = os.path.join(ROOT, "stories_index.json")
        idx = json.load(open(idx_p))
        idx["titles"] += [r["title"] for r in results if r["ok"] and r["title"] not in idx["titles"]]
        json.dump(idx, open(idx_p, "w"), indent=1, ensure_ascii=False)
        json.dump(sorted(used_clips, key=lambda x: (isinstance(x, str), str(x).zfill(12))), open(USED_P, "w"))
        json.dump(results, open(os.path.join(DAY, "results.json"), "w"), indent=1, ensure_ascii=False)
        report(results, series_ok, channel_stats() if UPLOAD else (None, None))
        sys.exit(0 if all(r["ok"] for r in results) else 1)
    except Exception as e:
        tg(f"❌ <b>UNREAD autopilot crashed</b>\n{html.escape(day.get('date', ''))}\n<code>{html.escape(str(e)[:300])}</code>")
        raise
