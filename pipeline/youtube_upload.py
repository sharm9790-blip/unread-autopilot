"""Upload an episode's short.mp4 to YouTube with its title/description/tags/thumbnail.

Usage:
  python3 youtube_upload.py <episode_dir> --dry-run          # proof: print exactly what will be sent
  python3 youtube_upload.py <episode_dir> [--privacy private|unlisted|public] [--publish-at 2026-10-31T21:00:00+05:30]

One-time setup (the user does this, never the agent):
  1. Google Cloud console -> new project -> enable "YouTube Data API v3".
  2. OAuth consent screen (External, add yourself as a test user).
  3. Credentials -> OAuth client ID -> "Desktop app" -> download JSON to
     ~/.config/scary-short/client_secret.json
  4. First upload opens a browser for the user to sign in and click Allow; the token is
     cached at ~/.config/scary-short/youtube_token.json for later runs.
Writes <episode_dir>/uploaded.json with the video id and URL.

Shorts thumbnails: YouTube only shows a custom Shorts thumbnail for Partner Program channels (desktop
Studio, rolled out July 2026). Everyone else gets a frame from the video. So render.py puts the
thumbnail in the first 0.5 s of every video ("cover") and this script still calls thumbnails.set.
"""
import json
import os
import sys

CFG = os.path.expanduser("~/.config/scary-short")
SECRET = os.path.join(CFG, "client_secret.json")
TOKEN = os.path.join(CFG, "youtube_token.json")
# youtube.upload to upload; youtube.force-ssl for captions; youtube to set thumbnails, edit descriptions and manage playlists (series links)
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl"]  # force-ssl: upload caption tracks


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def build_body(ep):
    story = json.load(open(os.path.join(ep, "story.json")))
    up = story.get("upload", {})
    title = up.get("title", story.get("title", "Scary story"))[:100]
    desc = up.get("description", "")
    if up.get("shorts", True) and "#shorts" not in desc.lower():
        desc += "\n\n#shorts"
    tags = [t.strip() for t in up.get("tags", "").split(",") if t.strip()]
    privacy = arg("--privacy", up.get("privacy", "private"))
    status = {"privacyStatus": privacy, "selfDeclaredMadeForKids": bool(up.get("made_for_kids", False)),
              "containsSyntheticMedia": bool(up.get("synthetic", True))}
    publish_at = arg("--publish-at")
    if publish_at:  # scheduled publish requires private until then
        status.update(privacyStatus="private", publishAt=publish_at)
    return {"snippet": {"title": title, "description": desc[:5000], "tags": tags,
                        "categoryId": str(up.get("category", "24"))},
            "status": status}


def credentials():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    creds = Credentials.from_authorized_user_file(TOKEN) if os.path.exists(TOKEN) else None
    if creds and not set(SCOPES) <= set(creds.scopes or []):
        creds = None  # token was granted fewer permissions; ask the user to approve again
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception as e:  # refresh token expired/revoked (testing-mode apps: 7 days); approve again
            print(f"token refresh failed ({str(e)[:80]}); opening Google sign-in in the browser", flush=True)
            creds = None
    if not creds or not creds.valid:
        if os.environ.get("CI"):  # no browser in the cloud: the refresh token in YT_TOKEN_JSON must be renewed
            raise SystemExit("YOUTUBE_REAUTH_NEEDED: run youtube_upload.py once on the Mac and update the YT_TOKEN_JSON secret")
        if not os.path.exists(SECRET):
            raise SystemExit(f"NO_CLIENT_SECRET: put your OAuth Desktop client JSON at {SECRET}")
        creds = InstalledAppFlow.from_client_secrets_file(SECRET, SCOPES).run_local_server(port=0)
        os.makedirs(CFG, exist_ok=True)
        with open(TOKEN, "w") as f:
            f.write(creds.to_json())
        os.chmod(TOKEN, 0o600)
    return creds


def main():
    ep = sys.argv[1].rstrip("/")
    up = json.load(open(os.path.join(ep, "story.json"))).get("upload", {})
    video = os.path.join(ep, up.get("video", "short.mp4"))  # long videos set "video" and "shorts": false
    thumb = os.path.join(ep, "thumbnail.jpg")  # vertical 720x1280, under 2 MB
    body = build_body(ep)
    if "--dry-run" in sys.argv:
        print(json.dumps(body, indent=2, ensure_ascii=False))
        print(f"\nvideo: {video} ({os.path.getsize(video) / 1e6:.0f} MB)")
        print(f"thumbnail: {thumb if os.path.exists(thumb) else 'none'}")
        print(f"auth: {'client secret found' if os.path.exists(SECRET) else 'MISSING ' + SECRET}"
              f", token {'cached' if os.path.exists(TOKEN) else 'not yet created'}")
        return
    if os.path.exists(os.path.join(ep, "uploaded.json")) and "--force" not in sys.argv:
        raise SystemExit("ALREADY_UPLOADED: see uploaded.json (pass --force to upload again)")
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    yt = build("youtube", "v3", credentials=credentials())
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(video, chunksize=8 * 1024 * 1024, resumable=True))
    resp = None
    while resp is None:
        st, resp = req.next_chunk()
        if st:
            print(f"uploading {int(st.progress() * 100)}%", flush=True)
    vid = resp["id"]
    result = {"id": vid, "url": f"https://youtube.com/shorts/{vid}" if up.get("shorts", True) else f"https://youtu.be/{vid}", "privacy": body["status"]["privacyStatus"],
              "title": body["snippet"]["title"]}
    if os.path.exists(thumb):
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(thumb)).execute()
            result["thumbnail"] = "set"
        except Exception as e:  # custom thumbnails need a phone-verified channel
            result["thumbnail"] = f"not set: {str(e)[:160]}"
    json.dump(result, open(os.path.join(ep, "uploaded.json"), "w"), indent=1)  # add_episode reads the id from here
    try:  # file it under Scary / Bedtime / Did You Know? (see channel_playlists.py)
        from channel_playlists import add_episode
        result["playlist"] = add_episode(yt, ep) or "none (no category)"
    except Exception as e:
        result["playlist"] = f"not added: {str(e)[:160]}"
    json.dump(result, open(os.path.join(ep, "uploaded.json"), "w"), indent=1)
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
