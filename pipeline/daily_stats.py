"""Daily UNREAD stats → Telegram (runs every morning in GitHub Actions; also works on the Mac).

Usage: python3 pipeline/daily_stats.py [--print] [--weekly | --pulse | --winners]
--winners: write state/winners.json (top/bottom Shorts of 14 days, live views) for the 06:00 writer.
--pulse: live subs/views + last-24h Shorts, with change since the previous pulse (12:00/16:00/20:00/00:00 IST).
Every day: the short high-level message below. --weekly: the detailed 28-day deep-dive instead (on request only).
- Last 7 days vs the 7 before (YouTube Analytics API; its data runs ~2-3 days behind, the message says up to when)
- Yesterday's Shorts with LIVE view counts (Data API, real time)
- Best and weakest Short of the last 7 days (live)
Token: ~/.config/scary-short/analytics_token.json (read-only scopes; secret YT_ANALYTICS_TOKEN_JSON in the cloud).
"""
import datetime
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.error
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
        for v in yt.videos().list(part="snippet,statistics,status,contentDetails", id=",".join(ids[i:i + 50])).execute()["items"]:
            if v["status"]["privacyStatus"] != "public":
                continue
            t = datetime.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00")).astimezone(IST)
            if t >= since:
                s = v["statistics"]
                out.append({"id": v["id"], "title": v["snippet"]["title"].split(" #")[0], "at": t,
                            "views": int(s.get("viewCount", 0)), "likes": int(s.get("likeCount", 0)),
                            "comments": int(s.get("commentCount", 0)),
                            "long": bool(re.search(r"\d+H|[2-9]M|\d\dM", v["contentDetails"].get("duration", "")))})
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
    c = costs_line()
    if c:
        lines += ["━━━━━━━━━━━━━━━"] + c
    return "\n".join(lines)


def costs_line():
    """ElevenLabs credits left + fal.ai spend: two lines for the morning message (never raises)."""
    out = []
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not key:
        try:
            key = json.load(open(os.path.expanduser("~/.claude/settings.json")))["env"]["ELEVENLABS_API_KEY"]
        except Exception:  # noqa: BLE001
            key = ""
    if key:
        try:
            req = urllib.request.Request("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": key})
            d = json.load(urllib.request.urlopen(req, timeout=20))
            left = int(d["character_limit"]) - int(d["character_count"])
            reset = datetime.datetime.fromtimestamp(int(d.get("next_character_count_reset_unix") or 0), IST)
            days = left // 1050  # ~3 Shorts x ~350 credits a day
            warn = " ⚠️ <b>top up soon</b>" if left < 3000 or reset.date() - datetime.date.today() > datetime.timedelta(days=days) else ""
            out.append(f"🎙 ElevenLabs: <b>{left:,}</b> / {int(d['character_limit']):,} credits left "
                       f"(≈{days} days of Shorts) · resets {reset.strftime('%d %b')}{warn}")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            out.append("🎙 ElevenLabs credits: turn on <b>User → Read</b> for the API key (ElevenLabs → Developers → API Keys) to see them here"
                       if "user_read" in body else f"🎙 ElevenLabs credits: unavailable ({e.code})")
        except Exception as e:  # noqa: BLE001
            out.append(f"🎙 ElevenLabs credits: unavailable ({str(e)[:60]})")
    try:
        led = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "state", "fal_spend.json")))
        y = (datetime.datetime.now(IST) - datetime.timedelta(days=1)).date().isoformat()
        last7 = sum(v["usd"] for d_, v in led.items() if d_ >= (datetime.date.today() - datetime.timedelta(days=7)).isoformat())
        out.append(f"🎨 fal.ai: ${led.get(y, {}).get('usd', 0):.2f} yesterday · ${last7:.2f} last 7 days "
                   f"(cap ${float(os.environ.get('FAL_DAILY_CAP', '0.64')):.2f}/day)")
    except Exception:  # noqa: BLE001
        pass
    return out


def renewals():
    """Alerts for the next 36 h (sent at 08:00, so 'tomorrow' is always caught): ElevenLabs renewal (from its API),
    Claude renewal (state/renewals.json, by hand), fal.ai prepaid credit running low. Returns alert lines (may be [])."""
    now = datetime.datetime.now(IST)
    soon = lambda t: t > now and (t.date() - now.date()).days <= 1  # due tomorrow (the day-before alert) or later today
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    cfg = json.load(open(os.path.join(root, "state", "renewals.json")))
    out = []
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not key:
        try:
            key = json.load(open(os.path.expanduser("~/.claude/settings.json")))["env"]["ELEVENLABS_API_KEY"]
        except Exception:  # noqa: BLE001
            key = ""
    if key:
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(
                "https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": key}), timeout=20))
            inv = d.get("next_invoice") or {}
            pay = datetime.datetime.fromtimestamp(int(inv.get("next_payment_attempt_unix") or 0), IST)
            reset = datetime.datetime.fromtimestamp(int(d.get("next_character_count_reset_unix") or 0), IST)
            amt = f"{(inv.get('amount_due_cents') or 0) / 100:,.0f} {str(d.get('currency', '')).upper()}"
            if d.get("status") != "active" or not inv:
                if soon(reset):
                    out.append(f"🎙 <b>ElevenLabs</b> {d.get('tier')} plan ends <b>{reset.strftime('%a %d %b, %H:%M')}</b> "
                               "with no renewal: subscribe (Starter) or the daily voice-overs stop.")
            elif soon(pay):
                out.append(f"🎙 <b>ElevenLabs</b> renews <b>{pay.strftime('%a %d %b, %H:%M')}</b> · {amt} · "
                           f"credits refill {reset.strftime('%d %b %H:%M')}")
        except Exception as e:  # noqa: BLE001
            out.append(f"🎙 ElevenLabs renewal: couldn't check ({str(e)[:60]})")
    c = cfg.get("claude", {})
    if c.get("ends"):  # subscription cancelled: the cloud routines (06:00 story writer) stop with it
        e = datetime.datetime.fromisoformat(c["ends"]).replace(hour=23, minute=59, tzinfo=IST)
        if e > now and (e.date() - now.date()).days <= 1:
            out.append(f"🤖 <b>Claude subscription ends {e.strftime('%a %d %b')}</b>: the 06:00 story writer "
                       "(and other Claude routines) stop after that, so no new Shorts get written. "
                       "Resubscribe at claude.ai → Settings → Billing to keep the autopilot running.")
    elif c.get("next_renewal"):
        r = datetime.datetime.fromisoformat(c["next_renewal"]).replace(hour=9, tzinfo=IST)
        while c.get("monthly", True) and r < now - datetime.timedelta(hours=12):  # roll forward month by month
            m = r.month % 12 + 1
            r = r.replace(year=r.year + (r.month == 12), month=m)
        if soon(r):
            out.append(f"🤖 <b>Claude</b> {c.get('plan', '')} renews <b>{r.strftime('%a %d %b')}</b> "
                       "(the 06:00 story writer runs on it)")
    try:
        led = json.load(open(os.path.join(root, "state", "fal_spend.json")))
        paid = sum(t["usd"] for t in cfg.get("fal", {}).get("topups", []))
        first = min(t["date"] for t in cfg["fal"]["topups"])
        spent = sum(v["usd"] for d_, v in led.items() if d_ >= first)
        week = [v["usd"] for d_, v in led.items() if d_ >= (now.date() - datetime.timedelta(days=7)).isoformat()]
        per_day = max(sum(week) / max(len(week), 1), 0.01)
        left = paid - spent
        days = left / per_day
        if days <= 4 or left < 2:
            out.append(f"🎨 <b>fal.ai</b> credit low: <b>${left:.2f}</b> left ≈ {days:.0f} days at ${per_day:.2f}/day. "
                       "Top up at fal.ai → Billing, then add it to state/renewals.json (or tell Claude).")
    except Exception:  # noqa: BLE001
        pass
    return out


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


PULSE_STATE = os.path.expanduser("~/.cache/unread-pulse.json")  # kept between runs by actions/cache


def pulse():
    """Live 4-hourly check (Data API, real time): subs + total views with the change since the last pulse,
    and how the last 24 h of Shorts are doing right now."""
    from googleapiclient.discovery import build
    yt = build("youtube", "v3", credentials=creds())
    now = datetime.datetime.now(IST)
    st_ = yt.channels().list(part="statistics", mine=True).execute()["items"][0]["statistics"]
    cur = {"subs": int(st_.get("subscriberCount", 0)), "views": int(st_["viewCount"]), "at": now.isoformat()}
    last = json.load(open(PULSE_STATE)) if os.path.exists(PULSE_STATE) else None
    os.makedirs(os.path.dirname(PULSE_STATE), exist_ok=True)
    json.dump(cur, open(PULSE_STATE, "w"))
    since = ""
    if last:
        since = f" since {datetime.datetime.fromisoformat(last['at']).astimezone(IST).strftime('%H:%M')}"
    d = lambda key: f" ({'+' if cur[key] - last[key] >= 0 else ''}{k(cur[key] - last[key])}{since})" if last else ""
    L = [f"⚡ <b>UNREAD pulse · {now.strftime('%a %H:%M')}</b>",
         f"👥 <b>{k(cur['subs'])}</b> subs{d('subs')}",
         f"👁 <b>{k(cur['views'])}</b> total views{d('views')}"]
    day = sorted(recent_shorts(yt, now - datetime.timedelta(hours=24)), key=lambda v: -v["views"])
    if day:
        L += ["━━━━━━━━━━━━━━━", "🎬 <b>Last 24 h</b> <i>(live)</i>"]
        for v in day[:5]:
            L.append(f"<b>{k(v['views'])}</b> · {v['at'].strftime('%H:%M')} · {html.escape(v['title'][:44])}")
    return "\n".join(L)


def winners(path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "state", "winners.json")):
    """Top and bottom Shorts of the last 14 days by live views (each at least 48 h old) -> state/winners.json.
    The 06:00 writer reads it to double down on what passed ~1K and avoid what flopped."""
    from googleapiclient.discovery import build
    yt = build("youtube", "v3", credentials=creds())
    now = datetime.datetime.now(IST)
    rows = [r for r in recent_shorts(yt, now - datetime.timedelta(days=14)) if now - r["at"] >= datetime.timedelta(hours=48) and not r["long"]]
    rows.sort(key=lambda r: -r["views"])
    med = sorted(r["views"] for r in rows)[len(rows) // 2] if rows else 0
    pick = lambda rs: [{"title": r["title"], "views": r["views"], "x_median": round(r["views"] / med, 1) if med else None,
                        "published": r["at"].strftime("%Y-%m-%d %H:%M")} for r in rs]
    out = {"updated": now.strftime("%Y-%m-%d %H:%M IST"), "median_views": med, "n": len(rows),
           "top": pick(rows[:6]), "bottom": pick(rows[-6:][::-1] if len(rows) > 6 else [])}
    json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
    return out


def tg(text):
    tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    data = urllib.parse.urlencode({"chat_id": chat, "text": text, "parse_mode": "HTML",
                                   "disable_web_page_preview": "true"}).encode()
    urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage", data=data), timeout=30)


if __name__ == "__main__":
    if "--pulse" in sys.argv:
        try:
            msg = pulse()
        except Exception as e:
            msg = f"⚡ <b>UNREAD pulse</b>\n❌ <code>{html.escape(str(e)[:200])}</code>"
        print(msg) if "--print" in sys.argv or not os.environ.get("TELEGRAM_BOT_TOKEN") else tg(msg)
        sys.exit(0)
    if "--renewals" in sys.argv:  # one alert message only when something renews/runs out within ~a day
        al = renewals()
        if al:
            msg = "⏰ <b>UNREAD · renewal reminder</b>\n" + "\n".join(al)
            print(msg) if "--print" in sys.argv or not os.environ.get("TELEGRAM_BOT_TOKEN") else tg(msg)
        else:
            print("renewals: nothing due today or tomorrow")
        sys.exit(0)
    if "--winners" in sys.argv:
        w = winners()
        print(f"winners.json: median {w['median_views']} over {w['n']} Shorts; top {w['top'][0]['title'] if w['top'] else '-'}")
        sys.exit(0)
    if "--weekly" in sys.argv:  # detailed deep-dive only on request; the daily message stays high level
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
