"""Viral scary videos on TikTok + Instagram (Apify scrapers) -> state/social_viral.json for the 06:00 writer.

Usage: APIFY_TOKEN=... python3 pipeline/social_scan.py [--print]
TikTok: clockworks/tiktok-scraper on 2 hashtags (~$0.075/day). Instagram: apify/instagram-hashtag-scraper, Reels on
3 hashtags (~$0.04/day). ~$3.5/month, inside Apify's free $5 monthly credit. Only posts from the last 60 days, ranked
by views and by outlier (views / followers where known). The writer studies hook and title patterns; never copies.
"""
import datetime
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "state", "social_viral.json")
DAYS = 60


def token():
    t = os.environ.get("APIFY_TOKEN") or open(os.path.expanduser("~/.config/apify/token")).read()
    return t.strip()


def actor(name, body):
    req = urllib.request.Request(
        f"https://api.apify.com/v2/acts/{name}/run-sync-get-dataset-items?timeout=280",
        data=json.dumps(body).encode(), headers={"Authorization": f"Bearer {token()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.load(r)
    if isinstance(d, dict):
        raise RuntimeError(str(d)[:200])
    return d


def recent(iso):
    try:
        t = datetime.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        return datetime.datetime.now(datetime.timezone.utc) - t <= datetime.timedelta(days=DAYS)
    except ValueError:
        return False


def first_line(text, n=140):
    t = " ".join(str(text or "").split())
    return t[:n]


def tiktok():
    rows = actor("clockworks~tiktok-scraper", {"hashtags": ["scarystories", "horrorstory"], "resultsPerPage": 10,
                                               "shouldDownloadVideos": False, "shouldDownloadCovers": False,
                                               "shouldDownloadSubtitles": False})
    out, seen = [], set()
    for x in rows:
        if x.get("id") in seen or not recent(x.get("createTimeISO")) or x.get("isAd"):
            continue
        seen.add(x.get("id"))
        fans = (x.get("authorMeta") or {}).get("fans") or 0
        views = x.get("playCount") or 0
        out.append({"platform": "tiktok", "hook": first_line(x.get("text")), "views": views,
                    "likes": x.get("diggCount"), "shares": x.get("shareCount"), "comments": x.get("commentCount"),
                    "seconds": (x.get("videoMeta") or {}).get("duration"), "followers": fans,
                    "outlier": round(views / max(fans, 1000), 1), "date": str(x.get("createTimeISO"))[:10],
                    "lang": x.get("textLanguage"), "url": x.get("webVideoUrl")})
    return out


def instagram():
    rows = actor("apify~instagram-hashtag-scraper", {"hashtags": ["scarystories", "horrorstory", "creepystories"],
                                                     "resultsLimit": 10, "resultsType": "reels"})
    out, seen = [], set()
    for x in rows:
        if x.get("id") in seen or not recent(x.get("timestamp")):
            continue
        seen.add(x.get("id"))
        out.append({"platform": "instagram", "hook": first_line(x.get("caption")),
                    "views": x.get("videoPlayCount") or x.get("igPlayCount") or 0,
                    "likes": x.get("likesCount"), "comments": x.get("commentsCount"), "shares": x.get("sharesCount"),
                    "seconds": round(x.get("videoDuration") or 0), "date": str(x.get("timestamp"))[:10],
                    "url": x.get("url")})
    return out


def main():
    res, errors = [], []
    for name, fn in (("tiktok", tiktok), ("instagram", instagram)):
        try:
            res += fn()
        except Exception as e:  # noqa: BLE001 - one platform failing must not lose the other
            errors.append(f"{name}: {str(e)[:150]}")
    res.sort(key=lambda r: -(r["views"] or 0))
    out = {"updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "days": DAYS, "errors": errors,
           "note": "Study hook/title patterns, formats and lengths only. Never copy a story, title or line.",
           "tiktok": [r for r in res if r["platform"] == "tiktok"][:12],
           "instagram": [r for r in res if r["platform"] == "instagram"][:12]}
    json.dump(out, open(OUT, "w"), indent=1, ensure_ascii=False)
    if "--print" in sys.argv:
        for r in out["tiktok"] + out["instagram"]:
            print(f"{r['platform'][:2]} {r['views']:>11,} {r['seconds']}s {r['date']}  {r['hook'][:80]}")
    print(f"social_viral.json: {len(out['tiktok'])} TikTok + {len(out['instagram'])} Instagram"
          + (f"; errors: {errors}" if errors else ""))


if __name__ == "__main__":
    main()
