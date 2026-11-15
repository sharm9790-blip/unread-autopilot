"""Find scary-story Shorts that went viral recently on OTHER channels -> state/viral.json (for the 06:00 writer).

Usage: python3 pipeline/viral_scan.py [--days 14] [--print]
YouTube Data API search (Shorts = videoDuration short), last N days, most viewed, for a few horror queries.
Each hit gets views, channel subscribers and an outlier score (views / subscribers): a 2K-sub channel with 2M views
means the idea/hook did the work, not the channel's size. The writer studies titles and hook patterns only - it never
copies a story. Quota: ~100 units per query + a few for stats (daily limit 10,000).
Token: ~/.config/scary-short/analytics_token.json (youtube.readonly; secret YT_ANALYTICS_TOKEN_JSON in the cloud).
"""
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "state", "viral.json")
QUERIES = ["scary story shorts", "horror story shorts", "creepy story", "true scary story", "scary text story",
           "horror rules", "creepy things that happened", "scary story narration"]
OWN = "UCmhYphTjjaZ-Z88VRApYycw"  # UNREAD itself
# not story Shorts (or not English): skip so the writer learns from narrated horror stories like ours
SKIP = re.compile(r"cartoon|roblox|minecraft|meme|funny|edit\b|game|prank|react|trailer|bhoot|animation|asmr|😂|🤣", re.I)


def english(t):
    letters = [c for c in t if c.isalpha()]
    return letters and sum(c.isascii() for c in letters) / len(letters) > 0.9


def main():
    sys.path.insert(0, HERE)
    from daily_stats import creds
    from googleapiclient.discovery import build
    yt = build("youtube", "v3", credentials=creds())
    days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 14
    since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ids = []
    for q in QUERIES:
        r = yt.search().list(part="id", q=q, type="video", videoDuration="short", order="viewCount",
                             publishedAfter=since, maxResults=25, relevanceLanguage="en").execute()
        ids += [i["id"]["videoId"] for i in r.get("items", [])]
    ids = list(dict.fromkeys(ids))
    vids = []
    for i in range(0, len(ids), 50):
        vids += yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50])).execute()["items"]
    chans = {v["snippet"]["channelId"] for v in vids}
    subs = {}
    cl = list(chans)
    for i in range(0, len(cl), 50):
        for c in yt.channels().list(part="statistics", id=",".join(cl[i:i + 50])).execute()["items"]:
            subs[c["id"]] = int(c["statistics"].get("subscriberCount", 0) or 0)
    rows = []
    for v in vids:
        d = v["contentDetails"].get("duration", "")
        m = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?$", d)
        secs = (int(m.group(1) or 0) * 60 + int(m.group(2) or 0)) if m else 999
        if secs > 90 or v["snippet"]["channelId"] == OWN or SKIP.search(v["snippet"]["title"]) or not english(v["snippet"]["title"]):
            continue
        views = int(v["statistics"].get("viewCount", 0))
        s = subs.get(v["snippet"]["channelId"], 0)
        rows.append({"title": v["snippet"]["title"], "views": views, "likes": int(v["statistics"].get("likeCount", 0)),
                     "comments": int(v["statistics"].get("commentCount", 0)), "seconds": secs,
                     "channel": v["snippet"]["channelTitle"], "channel_subs": s,
                     "outlier": round(views / max(s, 1000), 1), "published": v["snippet"]["publishedAt"][:10],
                     "url": f"https://youtube.com/shorts/{v['id']}"})
    rows.sort(key=lambda r: -r["outlier"])
    out = {"updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "days": days, "n": len(rows),
           "note": "Study title + hook patterns only. Never copy a story, title or line.", "top": rows[:20]}
    json.dump(out, open(OUT, "w"), indent=1, ensure_ascii=False)
    if "--print" in sys.argv:
        for r in rows[:20]:
            print(f"{r['views']:>10,} {r['outlier']:>7}x {r['seconds']:>3}s  {r['title'][:70]}  ({r['channel'][:20]}, {r['channel_subs']:,} subs)")
    print(f"viral.json: {len(rows)} Shorts from the last {days} days")


if __name__ == "__main__":
    main()
