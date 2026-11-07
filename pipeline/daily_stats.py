"""Daily UNREAD stats → Telegram (runs every morning in GitHub Actions; also works on the Mac).

Usage: python3 pipeline/daily_stats.py [--print] [--weekly]
Every day: the short high-level message below. Mondays (or --weekly): also the detailed 28-day deep-dive.
- Last 7 days vs the 7 before (YouTube Analytics API; its data runs ~2-3 days behind, the message says up to when)
- Yesterday's Shorts with LIVE view counts (Data API, real time)
- Best and weakest Short of the last 7 days (live)
Token: ~/.config/scary-short/analytics_token.json (read-only scopes; secret YT_ANALYTICS_TOKEN_JSON in the cloud).
"""
import datetime
import html
import json
import os
import sys
import urllib.parse
import urllib.request

TOKEN = os.path.expanduser("~/.config/scary-short/analytics_token.json")
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


def creds():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    c = Credentials.from_authorized_user_file(TOKEN)
    if not c.valid:
        c.refresh(Request())
    return c


def k(n):
    return f"{n / 1000:.1f}K" if n >= 1000 else str(n)


def pct(new, old):
    if not old:
        return ""
    ch = 100 * (new - old) / old
    return f" ({'▲' if ch >= 0 else '▼'}{abs(ch):.0f}% vs prev 7d)"


def totals(ya, start, end):
    m = "views,subscribersGained,subscribersLost,shares,likes,comments,averageViewPercentage"
    r = ya.reports().query(ids="channel==MINE", startDate=start.isoformat(), endDate=end.isoformat(), metrics=m).execute()
    row = (r.get("rows") or [[0] * 7])[0]
    return dict(zip(m.split(","), row))


def last_data_day(ya, today):
    """Newest day the Analytics API has numbers for (it lags 2-3 days)."""
    r = ya.reports().query(ids="channel==MINE", startDate=(today - datetime.timedelta(days=6)).isoformat(),
                           endDate=today.isoformat(), metrics="views", dimensions="day", sort="-day").execute()
    days = [datetime.date.fromisoformat(x[0]) for x in r.get("rows", []) if x[1]]
    return days[0] if days else today - datetime.timedelta(days=3)


def recent_shorts(yt, since):
    """Public videos published since `since` with live statistics."""
    up = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, tok = [], None
    for _ in range(3):
        r = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50, pageToken=tok).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        tok = r.get("nextPageToken")
        if not tok:
            break
    out = []
    for i in range(0, len(ids), 50):
        for v in yt.videos().list(part="snippet,statistics,status", id=",".join(ids[i:i + 50])).execute()["items"]:
            if v["status"]["privacyStatus"] != "public":
                continue
            t = datetime.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00")).astimezone(IST)
            if t >= since:
                s = v["statistics"]
                out.append({"id": v["id"], "title": v["snippet"]["title"].split(" #")[0], "at": t,
                            "views": int(s.get("viewCount", 0)), "likes": int(s.get("likeCount", 0)),
                            "comments": int(s.get("commentCount", 0))})
    return out


def build_message():
    from googleapiclient.discovery import build
    c = creds()
    ya, yt = build("youtubeAnalytics", "v2", credentials=c), build("youtube", "v3", credentials=c)
    now = datetime.datetime.now(IST)
    today = now.date()
    end = last_data_day(ya, today)
    cur = totals(ya, end - datetime.timedelta(days=6), end)
    prev = totals(ya, end - datetime.timedelta(days=13), end - datetime.timedelta(days=7))
    lines = [f"📊 <b>UNREAD · daily stats · {now.strftime('%a %d %b')}</b>", "━━━━━━━━━━━━━━━",
             f"<b>Last 7 days</b> <i>(YouTube data up to {end.strftime('%d %b')})</i>",
             f"👁 <b>{k(int(cur['views']))}</b> views{pct(cur['views'], prev['views'])}",
             f"👥 <b>+{int(cur['subscribersGained'])}</b> subs · −{int(cur['subscribersLost'])} lost",
             f"⏱ {cur['averageViewPercentage']:.0f}% avg watched · 🔁 {int(cur['shares'])} shares · 💬 {int(cur['comments'])}"]
    week = recent_shorts(yt, now - datetime.timedelta(days=7))
    yday = sorted([v for v in week if v["at"].date() == today - datetime.timedelta(days=1)], key=lambda v: v["at"])
    if yday:
        lines += ["━━━━━━━━━━━━━━━", f"🎬 <b>Yesterday's Shorts</b> <i>(live)</i>"]
        for v in yday:
            lines.append(f"<b>{k(v['views'])}</b> · {v['at'].strftime('%H:%M')} · "
                         f"<a href=\"https://youtube.com/shorts/{v['id']}\">{html.escape(v['title'][:48])}</a>")
    older = [v for v in week if (now - v["at"]).total_seconds() > 20 * 3600]  # give each Short ~a day before judging
    if len(older) >= 3:
        best, worst = max(older, key=lambda v: v["views"]), min(older, key=lambda v: v["views"])
        med = sorted(v["views"] for v in older)[len(older) // 2]
        lines += ["━━━━━━━━━━━━━━━",
                  f"🏆 Best this week: <b>{k(best['views'])}</b> ({best['views'] / max(med, 1):.1f}× median) · "
                  f"{html.escape(best['title'][:44])}",
                  f"💤 Weakest: <b>{k(worst['views'])}</b> · {html.escape(worst['title'][:44])}",
                  f"📈 Median Short this week: <b>{k(med)}</b> views ({len(older)} Shorts)"]
    return "\n".join(lines)


def weekly_detail():
    """Monday deep-dive, same shape as the manual analysis: last 28 days of Shorts by length, series vs standalone,
    top outliers, best subscriber converters, shares and how many stayed to watch."""
    import re
    import statistics as st
    from googleapiclient.discovery import build
    c = creds()
    ya, yt = build("youtubeAnalytics", "v2", credentials=c), build("youtube", "v3", credentials=c)
    end = last_data_day(ya, datetime.datetime.now(IST).date())
    start = end - datetime.timedelta(days=27)
    m = "views,averageViewPercentage,shares,subscribersGained,engagedViews"
    r = ya.reports().query(ids="channel==MINE", startDate=start.isoformat(), endDate=end.isoformat(), dimensions="video",
                           metrics=m, sort="-views", maxResults=200).execute()
    rows = [dict(zip(["video"] + m.split(","), x)) for x in r.get("rows", [])]
    meta = {}
    for i in range(0, len(rows), 50):
        for v in yt.videos().list(part="snippet,contentDetails", id=",".join(x["video"] for x in rows[i:i + 50])).execute()["items"]:
            d = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", v["contentDetails"]["duration"])
            meta[v["id"]] = (v["snippet"]["title"].split(" #")[0], int(d[1] or 0) * 60 + int(d[2] or 0) if d else 0)
    sh = []
    for x in rows:
        x["title"], x["secs"] = meta.get(x["video"], ("?", 0))
        if 0 < x["secs"] <= 61 and x["views"]:
            sh.append(x)
    if len(sh) < 5:
        return None
    med = st.median(x["views"] for x in sh)
    L = [f"🔎 <b>UNREAD · weekly deep-dive</b>", f"<i>Shorts from {start.strftime('%d %b')} to {end.strftime('%d %b')} · {len(sh)} Shorts</i>",
         "━━━━━━━━━━━━━━━",
         f"👁 {k(sum(x['views'] for x in sh))} views · 👥 +{sum(x['subscribersGained'] for x in sh)} subs · "
         f"🔁 {sum(x['shares'] for x in sh)} shares",
         f"⏱ stayed to watch: <b>{st.mean(100 * x['engagedViews'] / x['views'] for x in sh):.0f}%</b> (target 50%+)",
         "━━━━━━━━━━━━━━━", "<b>Length → median views</b>"]
    for lo, hi in [(0, 25), (25, 31), (31, 45), (45, 62)]:
        v = [x["views"] for x in sh if lo <= x["secs"] < hi]
        if v:
            L.append(f"{lo}-{hi - 1}s: <b>{k(int(st.median(v)))}</b> ({len(v)})")
    ser = [x["views"] for x in sh if re.search(r"Pt\.? ?\d", x["title"])]
    non = [x["views"] for x in sh if not re.search(r"Pt\.? ?\d", x["title"])]
    if ser and non:
        L.append(f"Series vs single: <b>{k(int(st.median(ser)))}</b> vs <b>{k(int(st.median(non)))}</b> median")
    L += ["━━━━━━━━━━━━━━━", "🏆 <b>Top outliers</b> (views ÷ median)"]
    for x in sorted(sh, key=lambda x: -x["views"])[:3]:
        L.append(f"{x['views'] / med:.1f}× · {k(x['views'])} · {html.escape(x['title'][:42])}")
    conv = sorted((x for x in sh if x["views"] >= 100), key=lambda x: -x["subscribersGained"] / x["views"])[:2]
    if conv:
        L += ["━━━━━━━━━━━━━━━", "👥 <b>Best subscriber converters</b>"]
        L += [f"{1000 * x['subscribersGained'] / x['views']:.1f}/1K · +{x['subscribersGained']} · {html.escape(x['title'][:40])}"
              for x in conv]
    return "\n".join(L)


def tg(text):
    tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    data = urllib.parse.urlencode({"chat_id": chat, "text": text, "parse_mode": "HTML",
                                   "disable_web_page_preview": "true"}).encode()
    urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage", data=data), timeout=30)


if __name__ == "__main__":
    if "--weekly" in sys.argv or (datetime.datetime.now(IST).weekday() == 0 and "--daily" not in sys.argv):
        try:
            w = weekly_detail()
            if w:
                print(w) if "--print" in sys.argv or not os.environ.get("TELEGRAM_BOT_TOKEN") else tg(w)
        except Exception as e:
            print("weekly detail failed:", e)
        if "--weekly" in sys.argv:
            sys.exit(0)
    try:
        msg = build_message()
    except Exception as e:
        msg = (f"📊 <b>UNREAD daily stats</b>\n❌ couldn't read YouTube Analytics:\n<code>{html.escape(str(e)[:250])}</code>\n"
               "If it says invalid_grant: run yt_analytics.py once on the Mac, then\n"
               "<code>gh secret set YT_ANALYTICS_TOKEN_JSON &lt; ~/.config/scary-short/analytics_token.json</code>")
    print(msg) if "--print" in sys.argv or not os.environ.get("TELEGRAM_BOT_TOKEN") else tg(msg)
