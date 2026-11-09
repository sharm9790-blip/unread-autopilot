#!/usr/bin/env python3
"""Cross-post UNREAD Shorts to Instagram (@unread1111) 2 days after they go public on YouTube (IG_LAG_DAYS),
the 2 with the most YouTube views per day (IG_PER_DAY); the rest of that day's Shorts are skipped.

Storage: rendered Shorts are kept as assets of the GitHub release "ig-queue" (release assets have no storage quota,
unlike Actions artifacts) and listed in state/ig_queue.json; posted ones move to state/ig_posted.json and their asset
is deleted.

    python3 pipeline/ig_daily.py stash <episode_dir> <youtube_id> <publish_at>   # produce.py calls this after upload
    python3 pipeline/ig_daily.py post [--dry-run]    # daily 05:15 IST: post every Short public on YouTube since
                                                     # yesterday or earlier that isn't on Instagram yet; Telegram report
Env: IG_TOKEN_JSON ({"mode": "fb", "access_token": Page token, "ig_user_id": "1784..."}), TELEGRAM_BOT_TOKEN,
TELEGRAM_CHAT_ID, GH_TOKEN (Actions) + YouTube token files (to confirm the Short is public).
"""
import datetime
import html
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
QUEUE = os.path.join(ROOT, "state", "ig_queue.json")
POSTED = os.path.join(ROOT, "state", "ig_posted.json")
REPO = os.environ.get("GITHUB_REPOSITORY", "sharm9790-blip/unread-autopilot")
RELEASE = "ig-queue"
FB = "https://graph.facebook.com/v26.0"
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
TAGS = "#scarystories #horrorstories #creepy #horror #shortstory #scary #reels"
MAX_TRIES = 3
PER_DAY = int(os.environ.get("IG_PER_DAY", "2"))  # Reels per day; the rest of that day's Shorts are skipped
LAG_DAYS = int(os.environ.get("IG_LAG_DAYS", "2"))  # Instagram posts a Short this many days after YouTube


def load(p, default):
    try:
        return json.load(open(p))
    except Exception:  # noqa: BLE001
        return default


def save(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(d, open(p, "w"), indent=1, ensure_ascii=False)


def gh(*args, check=True):
    r = subprocess.run(["gh", *args, "-R", REPO], capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"gh {args[0]} {args[1] if len(args) > 1 else ''}: {(r.stderr or r.stdout).strip()[:200]}")
    return r


# ---------- stash (after a Short is rendered + scheduled on YouTube) ----------

def caption(story):
    up = story.get("upload", {})
    desc = [l.strip() for l in up.get("description", "").split("\n") if l.strip()]
    hook = desc[0] if desc else story.get("title", "")
    q = next((l.replace("Tell me in the comments 👇", "").strip() for l in desc if "comments" in l), "")
    s = story.get("series")
    more = ("▶️ Part {} is on YouTube, link in bio".format(s["part"] + 1) if s and s["part"] < s["of"]
            else "▶️ More stories on YouTube, link in bio")
    return f"{hook}\n\n{(q + ' 👇') if q else 'Would you have looked? 👇'}\n\n{more}\n.\n{TAGS}"[:2200]


def ig_copy(src, dst):
    """Instagram rejects Reels above ~25 Mbps; 8 Mbps H.264 + AAC, faststart (~30 MB for 30 s)."""
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-c:v", "libx264", "-preset", "medium",
                    "-b:v", "8M", "-maxrate", "10M", "-bufsize", "20M", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", dst], check=True)


def stash(ep, yt_id, publish_at):
    story = json.load(open(os.path.join(ep, "story.json")))
    q = load(QUEUE, {})
    if yt_id in q or yt_id in load(POSTED, {}):
        return q.get(yt_id)
    if gh("release", "view", RELEASE, check=False).returncode:
        gh("release", "create", RELEASE, "--title", "Instagram queue (automatic)", "--prerelease",
           "--notes", "Rendered Shorts waiting to be cross-posted to Instagram by pipeline/ig_daily.py. Do not edit.")
    with tempfile.TemporaryDirectory() as tmp:
        f = os.path.join(tmp, f"{yt_id}.mp4")
        ig_copy(os.path.join(ep, "short.mp4"), f)
        gh("release", "upload", RELEASE, f, "--clobber")
    q[yt_id] = {"title": story.get("title", ""), "publish_at": publish_at, "caption": caption(story),
                "asset": f"{yt_id}.mp4", "episode": os.path.relpath(ep, ROOT)}
    save(QUEUE, q)
    return q[yt_id]


# ---------- post (daily) ----------

def curl(args):
    r = subprocess.run(["curl", "-sS", *args], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except ValueError:
        raise RuntimeError(f"bad response: {r.stdout[:200]} {r.stderr[:200]}") from None
    if "error" in d:
        e = d["error"]
        raise RuntimeError(f"IG_TOKEN_EXPIRED: {e.get('message', '')[:150]}" if e.get("code") == 190
                           else f"API error {e.get('code')}: {e.get('message', '')[:200]}")
    return d


def ig_post(tok, video, cap):
    at, uid = tok["access_token"], tok["ig_user_id"]
    c = curl(["-X", "POST", f"{FB}/{uid}/media", "--data-urlencode", "media_type=REELS",
              "--data-urlencode", "upload_type=resumable", "--data-urlencode", f"caption={cap}",
              "--data-urlencode", "share_to_feed=true", "--data-urlencode", f"access_token={at}"])
    cid = c["id"]
    up = curl(["-X", "POST", f"https://rupload.facebook.com/ig-api-upload/v26.0/{cid}",
               "-H", f"Authorization: OAuth {at}", "-H", "offset: 0", "-H", f"file_size: {os.path.getsize(video)}",
               "--data-binary", f"@{video}"])
    if not up.get("success", True):
        raise RuntimeError(f"upload failed: {up}")
    st = {}
    for _ in range(90):  # Instagram transcodes, usually < 2 min
        st = curl(["-G", f"{FB}/{cid}", "--data-urlencode", "fields=status_code,status",
                   "--data-urlencode", f"access_token={at}"])
        if st.get("status_code") == "FINISHED":
            break
        if st.get("status_code") in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"processing failed: {st.get('status', '')[:150]}")
        time.sleep(10)
    else:
        raise RuntimeError(f"processing timed out ({st.get('status_code')})")
    pub = curl(["-X", "POST", f"{FB}/{uid}/media_publish", "--data-urlencode", f"creation_id={cid}",
                "--data-urlencode", f"access_token={at}"])
    link = curl(["-G", f"{FB}/{pub['id']}", "--data-urlencode", "fields=permalink",
                 "--data-urlencode", f"access_token={at}"]).get("permalink", "")
    return pub["id"], link


def youtube_public(ids):
    """{id: (is_public, views)} live from YouTube; {} if YouTube can't be reached (then trust publish_at)."""
    try:
        sys.path.insert(0, HERE)
        from youtube_upload import credentials
        from googleapiclient.discovery import build
        yt = build("youtube", "v3", credentials=credentials())
        out = {}
        for k in range(0, len(ids), 50):
            for v in yt.videos().list(part="status,statistics", id=",".join(ids[k:k + 50])).execute()["items"]:
                out[v["id"]] = (v["status"]["privacyStatus"] == "public", int(v["statistics"].get("viewCount", 0)))
        return out
    except Exception as e:  # noqa: BLE001
        print("youtube check skipped:", e)
        return {}


def tg(text):
    t, c = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not (t and c):
        print(text)
        return
    data = urllib.parse.urlencode({"chat_id": c, "text": text, "parse_mode": "HTML",
                                   "disable_web_page_preview": "true"}).encode()
    try:
        urllib.request.urlopen(f"https://api.telegram.org/bot{t}/sendMessage", data, timeout=30)
    except Exception as e:  # noqa: BLE001
        print("telegram failed:", e, "\n", text)


STATS = os.path.join(ROOT, "state", "ig_stats.json")


def ig_stats(tok):
    """Daily Instagram summary like the YouTube one: followers (+change), likes/comments on the last 7 days of
    Reels, best Reel. Views/reach are added when the token has instagram_manage_insights (else skipped)."""
    at, uid = tok["access_token"], tok["ig_user_id"]
    me = curl(["-G", f"{FB}/{uid}", "--data-urlencode", "fields=followers_count,media_count",
               "--data-urlencode", f"access_token={at}"])
    media = curl(["-G", f"{FB}/{uid}/media", "--data-urlencode",
                  "fields=id,caption,timestamp,like_count,comments_count,permalink", "--data-urlencode", "limit=40",
                  "--data-urlencode", f"access_token={at}"]).get("data", [])
    since = datetime.datetime.now(IST) - datetime.timedelta(days=7)
    week = [m for m in media if datetime.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z") >= since]
    views = {}
    for m in week[:25]:
        try:
            ins = curl(["-G", f"{FB}/{m['id']}/insights", "--data-urlencode", "metric=views",
                        "--data-urlencode", f"access_token={at}"])
            views[m["id"]] = int(ins["data"][0]["values"][0]["value"])
        except Exception:  # noqa: BLE001 - no insights permission on this token
            break
    hist = load(STATS, {})
    today = datetime.datetime.now(IST).date().isoformat()
    prev = [v for d, v in sorted(hist.items()) if d < today]
    f = me.get("followers_count", 0)
    hist[today] = f
    save(STATS, dict(sorted(hist.items())[-90:]))
    delta = f" ({f - prev[-1]:+d} since yesterday)" if prev else ""
    likes, comm = sum(m.get("like_count", 0) for m in week), sum(m.get("comments_count", 0) for m in week)
    out = ["━━━━━━━━━━━━━━━", f"👥 <b>{f}</b> followers{delta} · {me.get('media_count', 0)} posts",
           f"📅 Last 7 days: <b>{len(week)}</b> Reels · ❤️ {likes} · 💬 {comm}"
           + (f" · 👁 <b>{sum(views.values())}</b> views" if views else "")]
    if week:
        key = (lambda m: views.get(m["id"], 0)) if views else (lambda m: m.get("like_count", 0) * 3 + m.get("comments_count", 0))
        b = max(week, key=key)
        name = html.escape((b.get("caption") or "").split("\n")[0][:55])
        out.append(f'🏆 Best: <a href="{b["permalink"]}">{name}</a> ({views.get(b["id"], b.get("like_count", 0))}'
                   f'{" views" if views else " likes"})')
    return out


def stats_lines(tok):
    try:
        return ig_stats(tok)
    except Exception as e:  # noqa: BLE001 - stats are a bonus
        return [f"<i>Instagram stats unavailable: {html.escape(str(e)[:100])}</i>"]


def post_due(dry=False):
    q, posted = load(QUEUE, {}), load(POSTED, {})
    today = datetime.datetime.now(IST).date()
    due = sorted(((k, v) for k, v in q.items() if k not in posted
                  and datetime.datetime.fromisoformat(v["publish_at"]).astimezone(IST).date()
                  <= today - datetime.timedelta(days=LAG_DAYS)),
                 key=lambda kv: kv[1]["publish_at"])
    head = f"📸 <b>UNREAD · Instagram · {today.strftime('%a %d %b')}</b>"
    tok = json.loads(os.environ.get("IG_TOKEN_JSON") or open(os.path.expanduser("~/.config/unread-instagram/token.json")).read())
    if not due:
        waiting = len([k for k in q if k not in posted])
        tg("\n".join([head, f"Nothing due today. {waiting} Short(s) waiting ({LAG_DAYS} days after YouTube)."]
                      + stats_lines(tok)))
        return 0
    live = youtube_public([k for k, _ in due])
    lines, ok, fail = [head], 0, 0
    if live:  # only Shorts already public; post the PER_DAY with the most YouTube views, skip the rest
        waiting = [(k, v) for k, v in due if not live.get(k, (False, 0))[0]]
        ready = sorted(((k, v) for k, v in due if live.get(k, (False, 0))[0]), key=lambda kv: -live[kv[0]][1])
        pick, skip = ready[:PER_DAY], ready[PER_DAY:]
        for k, v in waiting:
            lines.append(f"⏸ {html.escape(v['title'])}  <i>not public on YouTube yet, retry tomorrow</i>")
        for k, v in skip:
            q.pop(k, None)
            if not dry:
                gh("release", "delete-asset", RELEASE, v["asset"], "-y", check=False)
        if skip:
            save(QUEUE, q) if not dry else None
            lines.append(f"<i>⏭ skipped {len(skip)} with fewer YouTube views: "
                         + ", ".join(f"{html.escape(v['title'][:30])} ({live[k][1]})" for k, v in skip) + "</i>")
        pick.sort(key=lambda kv: kv[1]["publish_at"])  # keep series order (Part 1 before Part 2)
    else:  # YouTube unreachable: oldest first, nothing skipped
        pick = due[:PER_DAY]
    for k, v in pick:
        title = html.escape(v["title"])
        if dry:
            lines.append(f"🧪 would post: {title}")
            continue
        try:
            with tempfile.TemporaryDirectory() as tmp:
                gh("release", "download", RELEASE, "-p", v["asset"], "-D", tmp)
                mid, link = ig_post(tok, os.path.join(tmp, v["asset"]), v["caption"])
            posted[k] = {"media_id": mid, "permalink": link, "title": v["title"],
                         "at": datetime.datetime.now(IST).strftime("%Y-%m-%d %H:%M")}
            q.pop(k, None)
            save(POSTED, posted), save(QUEUE, q)
            gh("release", "delete-asset", RELEASE, v["asset"], "-y", check=False)
            lines.append(f'✅ <a href="{link}">{title}</a>' + (f"  <i>({live[k][1]} YouTube views)</i>" if live else ""))
            ok += 1
            time.sleep(60)  # don't fire Reels back-to-back
        except Exception as e:  # noqa: BLE001
            fail += 1
            v["tries"] = v.get("tries", 0) + 1
            msg = str(e)
            if v["tries"] >= MAX_TRIES and "IG_TOKEN_EXPIRED" not in msg:
                q.pop(k, None)
                gh("release", "delete-asset", RELEASE, v["asset"], "-y", check=False)
                lines.append(f"❌ {title}  <i>gave up after {MAX_TRIES} tries: {html.escape(msg[:100])}</i>")
            else:
                q[k] = v
                lines.append(f"⚠️ {title}  <i>{html.escape(msg[:120])} (retry tomorrow)</i>")
            save(QUEUE, q)
            if "IG_TOKEN_EXPIRED" in msg:
                lines.append("🔑 <b>Instagram token expired.</b> Make a new long-lived token, run "
                             "<code>python3 instagram/unread/ig_post.py --save-token</code> on the Mac, then "
                             "<code>gh secret set IG_TOKEN_JSON &lt; ~/.config/unread-instagram/token.json</code>")
                break
    lines.insert(1, f"<b>{ok}</b> Reel(s) posted" + (f" · {fail} failed" if fail else ""))
    tg("\n".join(lines + stats_lines(tok)))
    return 1 if fail and not ok else 0


if __name__ == "__main__":
    if len(sys.argv) >= 5 and sys.argv[1] == "stash":
        print(stash(sys.argv[2], sys.argv[3], sys.argv[4]))
    elif len(sys.argv) >= 2 and sys.argv[1] == "post":
        try:
            sys.exit(post_due(dry="--dry-run" in sys.argv))
        except Exception as e:  # noqa: BLE001 - always tell Telegram, even if the run dies early
            tg(f"❌ <b>UNREAD · Instagram run crashed</b>\n<code>{html.escape(str(e)[:300])}</code>\n"
               f"Nothing was posted; it retries tomorrow at 05:15 IST.")
            raise
    else:
        print(__doc__)
