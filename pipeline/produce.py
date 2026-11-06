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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
VOICE = os.environ.get("VOICE_ID", "BycOlIr9Aytiubl0LIIY")  # Gxl
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
DAY = sys.argv[1].rstrip("/")
UPLOAD = "--no-upload" not in sys.argv
day = json.load(open(os.path.join(DAY, "day.json")))
USED_P = os.path.join(ROOT, "state", "used_clips.json")
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


def fetch_clip(query, dest):
    """Best Pixabay hit: the query's nouns in its tags first (searching the full query and the nouns alone), then mood
    words; long enough, not reused, not cartoon, not black/blown-out."""
    key = os.environ["PIXABAY_API_KEY"]
    if isinstance(query, int) or str(query).isdigit():  # the writer pinned an exact Pixabay video id
        h = get(f"https://pixabay.com/api/videos/?key={key}&id={int(query)}")["hits"][0]
        v = h["videos"]["medium"] if h["videos"]["medium"].get("url") else h["videos"]["large"]
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
    score = lambda h: 3 * sum(has(h, w) for w in nouns) + sum(has(h, w) for w in words if w in MOOD)
    ok = [h for h in hits if h["id"] not in used_clips and h["duration"] >= 4 and not any(n in h.get("tags", "").lower() for n in NO)]
    ranked = sorted(ok, key=lambda h: -score(h))
    vid = lambda h: h["videos"]["medium"] if h["videos"]["medium"].get("url") else h["videos"]["large"]
    pick = next((h for h in ranked[:8] if 30 <= brightness(vid(h)["thumbnail"]) <= 165), ranked[0] if ranked else None)
    if not pick:
        raise RuntimeError(f"no Pixabay video for {query!r}")
    open(dest, "wb").write(get(vid(pick)["url"], True))
    used_clips.add(pick["id"])
    return {"id": pick["id"], "user": pick["user"], "query": query, "tags": pick.get("tags", "")}


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
                credits[f] = fetch_clip(q, os.path.join(ep, f))
        if credits:
            json.dump(credits, open(os.path.join(ep, "clip_credits.json"), "w"), indent=1)
        st = "voice"
        if not os.path.exists(os.path.join(ep, "words.json")):
            run(["python3", os.path.join(HERE, "tts.py"), ep, "--voice", VOICE], log)
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
            lines.append(f"🕒 <b>{t}</b>  {link}  <i>{r.get('seconds', '')}s</i>")
        else:
            lines.append(f"❌ {title}\n      <i>failed at {r['step']}: {html.escape(r['error'][:120])}</i>")
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
        json.dump(sorted(used_clips), open(USED_P, "w"))
        json.dump(results, open(os.path.join(DAY, "results.json"), "w"), indent=1, ensure_ascii=False)
        report(results, series_ok, channel_stats() if UPLOAD else (None, None))
        sys.exit(0 if all(r["ok"] for r in results) else 1)
    except Exception as e:
        tg(f"❌ <b>UNREAD autopilot crashed</b>\n{html.escape(day.get('date', ''))}\n<code>{html.escape(str(e)[:300])}</code>")
        raise
