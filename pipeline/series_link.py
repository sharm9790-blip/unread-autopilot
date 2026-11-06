"""Link an uploaded series: playlist in part order + 'all parts' block in every description.

Usage: python3 series_link.py <series_dir> [--privacy private]
  <series_dir> holds one folder per part; each has story.json ("series": {"part": n}) and uploaded.json.
Re-runnable: it replaces the block between the markers instead of appending twice.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from youtube_upload import credentials  # noqa: E402

START, END = "━━ ALL PARTS ━━", "━━━━━━━━━━━━"


def retry(fn, tries=6):
    """New playlists take a few seconds to become readable/writable; retry 404s with backoff."""
    from googleapiclient.errors import HttpError
    for k in range(tries):
        try:
            return fn()
        except HttpError as e:
            if e.resp.status != 404 or k == tries - 1:
                raise
            time.sleep(3 * (k + 1))


def main():
    root = sys.argv[1].rstrip("/")
    privacy = sys.argv[sys.argv.index("--privacy") + 1] if "--privacy" in sys.argv else "private"
    eps = []
    for d in sorted(os.listdir(root)):
        p = os.path.join(root, d)
        if os.path.exists(os.path.join(p, "uploaded.json")):
            st = json.load(open(os.path.join(p, "story.json")))
            eps.append((st["series"]["part"], st, json.load(open(os.path.join(p, "uploaded.json"))), p))
    eps.sort(key=lambda e: e[0])
    if not eps:
        raise SystemExit("no uploaded parts found")
    name = eps[0][1]["series"]["name"]
    from googleapiclient.discovery import build
    yt = build("youtube", "v3", credentials=credentials())

    pl_file = os.path.join(root, "playlist.json")
    if os.path.exists(pl_file):
        pl_id = json.load(open(pl_file))["id"]
    else:
        pl = yt.playlists().insert(part="snippet,status", body={
            "snippet": {"title": f"{name} (Scary Series)",
                        "description": f"{name}: a {len(eps)}-part horror story. Watch in order."},
            "status": {"privacyStatus": privacy}}).execute()
        pl_id = pl["id"]
        json.dump({"id": pl_id, "url": f"https://www.youtube.com/playlist?list={pl_id}"}, open(pl_file, "w"))
    have = set()
    req = yt.playlistItems().list(part="snippet", playlistId=pl_id, maxResults=50)
    while req:
        r = retry(req.execute)
        have |= {i["snippet"]["resourceId"]["videoId"] for i in r.get("items", [])}
        req = yt.playlistItems().list_next(req, r)
    for pos, (_, _, up, _) in enumerate(eps):
        if up["id"] not in have:
            retry(yt.playlistItems().insert(part="snippet", body={"snippet": {
                "playlistId": pl_id, "position": pos,
                "resourceId": {"kind": "youtube#video", "videoId": up["id"]}}}).execute)

    pl_url = f"https://www.youtube.com/playlist?list={pl_id}"
    for i, (n, st, up, _) in enumerate(eps):
        lines = [START, f"▶ Full series playlist: {pl_url}"]
        if i > 0:
            lines.append(f"◀ Previous (Part {eps[i - 1][0]}): {eps[i - 1][2]['url']}")
        if i + 1 < len(eps):
            lines.append(f"▶ Next (Part {eps[i + 1][0]}): {eps[i + 1][2]['url']}")
        lines += [f"Part {m}: {e['url']}" + ("  ← you are here" if m == n else "") for m, _, e, _ in eps]
        lines.append(END)
        block = "\n".join(lines)
        v = yt.videos().list(part="snippet", id=up["id"]).execute()["items"][0]
        sn = v["snippet"]
        desc = sn.get("description", "")
        if START in desc:
            desc = desc[:desc.index(START)].rstrip()
        sn["description"] = (desc + "\n\n" + block)[:5000]
        yt.videos().update(part="snippet", body={"id": up["id"], "snippet": {
            "title": sn["title"], "description": sn["description"], "tags": sn.get("tags", []),
            "categoryId": sn["categoryId"]}}).execute()
        print(f"Part {n}: linked  {up['url']}")
    print("playlist:", pl_url)


if __name__ == "__main__":
    main()
