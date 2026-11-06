"""Keep the channel's three category playlists (Scary / Bedtime / Did You Know?) up to date.

Usage (run from anywhere; paths are relative to the YouTube project root):
  python3 channel_playlists.py --dry-run             # show which video goes in which playlist
  python3 channel_playlists.py [--privacy private]   # create missing playlists, add missing videos

Category of an episode: story.json "upload": {"playlist": "scary" | "bedtime" | "facts" | "stoic" | "space"} if set,
otherwise by top folder: shorts/ longform/ -> scary, kids/ soothing/ -> bedtime, facts/ -> facts, stoic/ -> stoic.
Playlist ids are kept in branding/playlists.json. Re-runnable: videos already in a playlist are skipped.
youtube_upload.py calls add_episode() after each upload so new videos land in their playlist.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from youtube_upload import credentials  # noqa: E402
from series_link import retry  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, ".."))  # repo root (unread-autopilot)
STORE = os.path.join(ROOT, "branding", "playlists.json")
PLAYLISTS = {
    "scary": ("😱 Scary Stories",
              "Short horror stories from UNREAD: creepy texts, unexplained calls and things that knock at 3 AM. "
              "Best watched alone, in the dark."),
    "bedtime": ("🌙 Bedtime Stories",
                "Gentle, calm stories for kids and grown-ups from UNREAD. Kind characters, soft voices and cozy "
                "sounds for story time, quiet time or falling asleep."),
    "facts": ("💡 Did You Know?",
              "Short, surprising facts and true stories about the world, science and history from UNREAD."),
    "stoic": ("🏛️ Stoic Mindset",
              "One idea a day from Stoic and modern philosophy: Marcus Aurelius, Seneca, Epictetus, Nietzsche and "
              "Camus. Calm, deep and under a minute, from UNREAD."),
    "space": ("🌌 Space Mysteries",
              "Documentaries about the strangest real mysteries of the universe: the Great Attractor, dark flow, "
              "black holes and the edge of everything we can see. Real science, from UNREAD."),
}
FOLDERS = {"daily": "scary", "shorts": "scary", "longform": "scary", "kids": "bedtime", "soothing": "bedtime", "facts": "facts", "stoic": "stoic", "space": "space"}


def category(ep):
    try:
        up = json.load(open(os.path.join(ep, "story.json"))).get("upload", {})
    except (OSError, ValueError):
        up = {}
    if up.get("playlist") in PLAYLISTS:
        return up["playlist"]
    return FOLDERS.get(os.path.relpath(ep, ROOT).split(os.sep)[0])


def episodes():
    """(category, video_id, title, episode_dir) for every uploaded video, oldest upload first."""
    out = []
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("clips", "tmp", "node_modules")]
        if "uploaded.json" in files:
            up = json.load(open(os.path.join(dirpath, "uploaded.json")))
            out.append((os.path.getmtime(os.path.join(dirpath, "uploaded.json")), category(dirpath),
                        up["id"], up.get("title", ""), dirpath))
    return [e[1:] for e in sorted(out)]


def ensure_playlist(yt, store, key, privacy):
    if key not in store:
        title, desc = PLAYLISTS[key]
        pl = yt.playlists().insert(part="snippet,status", body={
            "snippet": {"title": title, "description": desc}, "status": {"privacyStatus": privacy}}).execute()
        store[key] = {"id": pl["id"], "title": title, "url": f"https://www.youtube.com/playlist?list={pl['id']}"}
        json.dump(store, open(STORE, "w"), indent=1, ensure_ascii=False)
        print(f"created playlist {title}: {store[key]['url']}")
    return store[key]["id"]


def playlist_videos(yt, pl_id):
    have, req = set(), yt.playlistItems().list(part="snippet", playlistId=pl_id, maxResults=50)
    while req:
        r = retry(req.execute)
        have |= {i["snippet"]["resourceId"]["videoId"] for i in r.get("items", [])}
        req = yt.playlistItems().list_next(req, r)
    return have


def add(yt, pl_id, vid):
    retry(yt.playlistItems().insert(part="snippet", body={"snippet": {
        "playlistId": pl_id, "resourceId": {"kind": "youtube#video", "videoId": vid}}}).execute)


def add_episode(yt, ep, privacy="private"):
    """Called by youtube_upload.py right after an upload."""
    key = category(os.path.abspath(ep))
    if not key:
        return None
    store = json.load(open(STORE)) if os.path.exists(STORE) else {}
    vid = json.load(open(os.path.join(ep, "uploaded.json")))["id"]
    pl_id = ensure_playlist(yt, store, key, privacy)
    add(yt, pl_id, vid)
    return PLAYLISTS[key][0]


def main():
    privacy = sys.argv[sys.argv.index("--privacy") + 1] if "--privacy" in sys.argv else "private"
    eps = episodes()
    if "--dry-run" in sys.argv:
        for key, (title, _) in PLAYLISTS.items():
            rows = [e for e in eps if e[0] == key]
            print(f"\n{title}  ({len(rows)} videos)")
            for _, vid, t, _ in rows:
                print(f"  {vid}  {t}")
        skipped = [e for e in eps if e[0] is None]
        if skipped:
            print("\nno category (set upload.playlist in story.json):")
            for _, vid, t, ep in skipped:
                print(f"  {vid}  {t}  [{os.path.relpath(ep, ROOT)}]")
        return
    from googleapiclient.discovery import build
    yt = build("youtube", "v3", credentials=credentials())
    store = json.load(open(STORE)) if os.path.exists(STORE) else {}
    for key in PLAYLISTS:
        rows = [e for e in eps if e[0] == key]
        if not rows:
            continue
        pl_id = ensure_playlist(yt, store, key, privacy)
        have = playlist_videos(yt, pl_id)
        new = [e for e in rows if e[1] not in have]
        for _, vid, t, _ in new:
            add(yt, pl_id, vid)
        print(f"{PLAYLISTS[key][0]}: added {len(new)}, already had {len(rows) - len(new)}  {store[key]['url']}")


if __name__ == "__main__":
    main()
