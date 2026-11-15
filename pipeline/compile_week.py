"""Weekly long-form compilation: the week's best UNREAD Shorts joined into one 16:9 video ("N Scary Stories ...").

Why: long videos earn watch hours (Partner Program: 4,000 h) and show up in search / as night-time listening, while
Shorts alone grow slowly toward monetization. Costs nothing new: it reuses rendered Shorts (no voice, no footage).

  python3 pipeline/compile_week.py stash <episode_dir> <youtube_id> <publish_at>   # produce.py, after each upload
  python3 pipeline/compile_week.py build [--publish-at ISO] [--no-upload] [--local DIR ...] [--max-min 12]

stash: keeps a 1080p copy of the Short (6 Mbps) as an asset of the private repo's release "compilation-queue"
       + state/comp_queue.json {id: {title, publish_at, end, asset}}; `end` = where the story ends (the spoken
       "Subscribe..." starts), so the compilation plays stories back to back without 20 subscribe pitches.
build: Shorts public for 48 h+, ranked by live YouTube views, best first, a series' Part 1 kept right before its
       Part 2; up to --max-min minutes. Each Short sits on a blurred 16:9 copy of itself with its title on the side.
       Ends on one subscribe card. Uploads as a normal (long) video with chapters, a thumbnail and the Scary playlist.
       --local DIR: also use Shorts rendered on this Mac (folders with short.mp4 + uploaded.json + words.json).
"""
import datetime
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
QUEUE = os.path.join(ROOT, "state", "comp_queue.json")
DONE = os.path.join(ROOT, "state", "compiled.json")
RELEASE = "compilation-queue"
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
W, H, FPS = 1920, 1080, 30
RED = (200, 28, 28)


def load(p, default):
    return json.load(open(p)) if os.path.exists(p) else default


def gh(*args, check=True):
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def story_end(ep):
    """Seconds into short.mp4 where the story ends (the 'Subscribe...' line starts); None = use the whole Short."""
    try:
        st = json.load(open(os.path.join(ep, "story.json")))
        words = json.load(open(os.path.join(ep, "words.json")))
    except (OSError, ValueError):
        return None
    if isinstance(words, dict):
        words = words.get("words") or words.get("alignment") or []
    speed = float(st.get("speed", 1.0))
    anchor = (st.get("silence_from") or "subscribe").lower()
    for w in words:
        if not isinstance(w, dict):
            return None
        if re.sub(r"[^a-z0-9]", "", str(w.get("text", w.get("word", ""))).lower()).startswith(anchor):
            return round(float(w["start"]) / speed, 2)
    return None


def clean_title(t):
    return re.sub(r"\s*#\S+", "", t).strip()


# ---------------------------------------------------------------- stash (called by produce.py after each upload)
def stash(ep, yt_id, publish_at):
    src = os.path.join(ep, "short.mp4")
    if not os.path.exists(src):
        return
    q = load(QUEUE, {})
    tmp = os.path.join(tempfile.gettempdir(), f"{yt_id}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", "scale=1080:1920", "-c:v", "libx264",
                    "-b:v", "6M", "-maxrate", "6M", "-bufsize", "12M", "-preset", "veryfast", "-c:a", "aac",
                    "-b:a", "160k", "-movflags", "+faststart", tmp], check=True)
    if gh("release", "view", RELEASE, check=False).returncode:
        gh("release", "create", RELEASE, "--title", "Weekly compilation queue (automatic)", "--prerelease",
           "--notes", "Rendered Shorts kept for the Sunday compilation (pipeline/compile_week.py). Deleted after use.")
    gh("release", "upload", RELEASE, tmp, "--clobber")
    st = json.load(open(os.path.join(ep, "story.json")))
    q[yt_id] = {"title": clean_title(st.get("upload", {}).get("title", st.get("title", ""))), "publish_at": publish_at,
                "end": story_end(ep), "asset": f"{yt_id}.mp4", "series": st.get("series")}
    json.dump(q, open(QUEUE, "w"), indent=1, ensure_ascii=False)
    os.remove(tmp)


# ---------------------------------------------------------------- build
def font(size, bold=True):
    from PIL import ImageFont
    for p in [os.path.join(HERE, "fonts", "Anton-Regular.ttf") if bold else "",
              "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if p and os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, f, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + ([cur] if cur else [])


def side_panel(path, n, total, title):
    """Transparent 1920x1080 overlay: story number + title on the left, channel name on the right."""
    from PIL import Image, ImageDraw
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fg_w = H * 9 // 16  # the vertical Short in the middle; darken both sides so the text reads on bright footage
    d.rectangle([0, 0, (W - fg_w) // 2, H], fill=(0, 0, 0, 110))
    d.rectangle([(W + fg_w) // 2, 0, W, H], fill=(0, 0, 0, 110))
    left = 64
    d.text((left, 300), f"STORY {n}/{total}", font=font(46), fill=RED)
    y = 370
    for line in wrap(d, title.upper(), font(64), 560)[:6]:
        d.text((left, y), line, font=font(64), fill=(240, 240, 240))
        y += 78
    d.text((W - 64 - d.textlength("UNREAD", font=font(80)), 470), "UNREAD", font=font(80), fill=(235, 235, 235))
    sub = "a new scary story every night"
    d.text((W - 64 - d.textlength(sub, font=font(30, False)), 570), sub, font=font(30, False), fill=(170, 170, 170))
    im.save(path)


def segment(src, end, panel, out):
    """One Short -> 16:9 segment: blurred, darkened copy behind, the vertical Short centred, panel on top."""
    t = ["-t", f"{end + 0.4:.2f}"] if end else []
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", *t, "-i", src, "-i", panel, "-filter_complex",
        f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,"
        f"eq=brightness=-0.28[bg];[b]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:0[v];[v][1:v]overlay=0:0,"
        f"fps={FPS},format=yuv420p[vo];[0:a]aresample=48000,afade=t=out:st={max(0.1, (end or 30) + 0.05):.2f}:d=0.35[ao]",
        "-map", "[vo]", "-map", "[ao]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac",
        "-b:a", "192k", "-ar", "48000", "-ac", "2", out], check=True)


def outro(out, thumb_bg):
    from PIL import Image, ImageDraw, ImageFilter
    bg = Image.open(thumb_bg).convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(24))
    bg = Image.eval(bg, lambda v: int(v * 0.35))
    d = ImageDraw.Draw(bg)
    for txt, f, y, c in [("SUBSCRIBE", font(150), 330, RED), ("A NEW SCARY STORY EVERY NIGHT", font(64), 540, (240,) * 3),
                         ("UNREAD", font(56), 660, (190,) * 3)]:
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=c)
    png = out + ".png"
    bg.save(png)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", "6", "-i", png, "-f", "lavfi", "-t", "6",
                    "-i", "anullsrc=r=48000:cl=stereo", "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)


def thumbnail(path, frame, n):
    from PIL import Image, ImageDraw, ImageFilter
    fr = Image.open(frame).convert("RGB")
    bg = fr.resize((1280, 720)).filter(ImageFilter.GaussianBlur(18))
    bg = Image.eval(bg, lambda v: int(v * 0.45))
    fg = fr.resize((int(720 * fr.width / fr.height), 720))
    bg.paste(fg, (1280 - fg.width - 40, 0))
    d = ImageDraw.Draw(bg)
    d.text((48, 120), str(n), font=font(260), fill=RED)
    d.text((48, 400), "SCARY", font=font(120), fill=(245,) * 3)
    d.text((48, 530), "STORIES", font=font(120), fill=(245,) * 3)
    bg.save(path, quality=90)


def live_views(ids):
    sys.path.insert(0, HERE)
    from googleapiclient.discovery import build
    from youtube_upload import credentials
    yt = build("youtube", "v3", credentials=credentials())
    out = {}
    for i in range(0, len(ids), 50):
        for v in yt.videos().list(part="statistics,status", id=",".join(ids[i:i + 50])).execute()["items"]:
            out[v["id"]] = (v["status"]["privacyStatus"] == "public", int(v["statistics"].get("viewCount", 0)))
    return out


def candidates(local_dirs):
    """{yt_id: {title, end, src or asset, series, publish_at}} from the cloud queue and/or local folders."""
    c = {}
    for yid, v in load(QUEUE, {}).items():
        c[yid] = dict(v)
    for base in local_dirs:
        for up in glob.glob(os.path.join(base, "**", "uploaded.json"), recursive=True):
            ep = os.path.dirname(up)
            if not os.path.exists(os.path.join(ep, "short.mp4")):
                continue
            u = json.load(open(up))
            if u.get("id") in c:
                continue
            st = json.load(open(os.path.join(ep, "story.json")))
            if st.get("upload", {}).get("playlist", "scary") not in ("scary", None) or st.get("upload", {}).get("shorts") is False:
                continue
            c[u["id"]] = {"title": clean_title(u.get("title") or st.get("title", "")), "end": story_end(ep),
                          "src": os.path.join(ep, "short.mp4"), "series": st.get("series")}
    done = set(load(DONE, {}).get("used", []))
    return {k: v for k, v in c.items() if k not in done}


def pick(c, views, max_s):
    now = datetime.datetime.now(datetime.timezone.utc)
    ok = []
    for yid, v in c.items():
        pub, n = views.get(yid, (False, 0))
        if not pub:
            continue
        if v.get("publish_at"):
            t = datetime.datetime.fromisoformat(v["publish_at"])
            if now - t < datetime.timedelta(hours=48):
                continue
        ok.append((n, yid))
    ok.sort(reverse=True)
    order, total = [], 0.0
    by_series = {}
    for yid, v in c.items():
        s = v.get("series")
        if s:
            by_series[(s["name"], s["part"])] = yid
    for n, yid in ok:
        if yid in order:
            continue
        v = c[yid]
        group = [yid]
        s = v.get("series")
        if s and s.get("of", 2) > 3:  # long series (6-10 parts) would swamp the week; they get their own video
            continue
        if s:  # keep a 2-3 part series together, in part order
            group = [by_series[(s["name"], p)] for p in range(1, s["of"] + 1) if (s["name"], p) in by_series]
            group = [g for g in group if views.get(g, (False, 0))[0]] or [yid]
        dur = sum((c[g].get("end") or 30) + 0.4 for g in group if g not in order)
        if total + dur > max_s:
            continue
        order += [g for g in group if g not in order]
        total += dur
    return order, total


def main_build():
    args = sys.argv
    local = [args[i + 1] for i, a in enumerate(args) if a == "--local"]
    max_s = 60 * float(args[args.index("--max-min") + 1]) if "--max-min" in args else 12 * 60
    c = candidates(local)
    if not c:
        print("compilation: nothing queued")
        return
    views = live_views(list(c))
    order, total = pick(c, views, max_s)
    if len(order) < 8:
        print(f"compilation: only {len(order)} eligible Shorts (need 8); skipping this week")
        return
    work = tempfile.mkdtemp(prefix="comp-")
    segs, chapters, t = [], [], 0.0
    for i, yid in enumerate(order, 1):
        v = c[yid]
        src = v.get("src")
        if not src:
            gh("release", "download", RELEASE, "-p", v["asset"], "-D", work, "--clobber")
            src = os.path.join(work, v["asset"])
        panel = os.path.join(work, f"p{i}.png")
        side_panel(panel, i, len(order), v["title"])
        seg = os.path.join(work, f"s{i:02d}.mp4")
        segment(src, v.get("end"), panel, seg)
        segs.append(seg)
        chapters.append(f"{int(t // 60):02d}:{int(t % 60):02d} {v['title']}")
        t += float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", seg],
                                  capture_output=True, text=True).stdout)
        if i == 1:
            frame = os.path.join(work, "frame.jpg")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.2", "-i", src, "-frames:v", "1", frame], check=True)
    out_dir = os.path.join(ROOT, "compilations", datetime.datetime.now(IST).strftime("%Y-%m-%d"))
    os.makedirs(out_dir, exist_ok=True)
    end_card = os.path.join(work, "outro.mp4")
    outro(end_card, frame)
    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in segs + [end_card]))
    video = os.path.join(out_dir, "compilation.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    "-movflags", "+faststart", video], check=True)
    thumbnail(os.path.join(out_dir, "thumbnail.jpg"), frame, len(order))
    n, top = len(order), c[order[0]]["title"]
    title = f"{n} Scary Stories to Keep You Up Tonight | {top}"
    if len(title) > 100:
        title = f"{n} Scary Stories to Keep You Up Tonight | UNREAD"
    desc = (f"{n} short scary stories from UNREAD, back to back. Lights off, headphones on.\n\n"
            "Which one got you? Tell me the number in the comments 👇\n"
            "📤 Send this to the friend who says nothing scares them.\n\n" + "\n".join(chapters) +
            "\n\nSubscribe to UNREAD for a new scary story every night.\n\nFootage: Pixabay · Voice: AI narration\n\n"
            "#scarystories #horrorstories #creepy #horror #scarystoriescompilation")
    story = {"title": title, "upload": {"title": title, "description": desc, "shorts": False, "video": "compilation.mp4",
                                        "playlist": "scary", "category": "24",
                                        "tags": "scary stories, horror stories compilation, creepy stories, scary stories to fall asleep to, short horror stories, unread"}}
    json.dump(story, open(os.path.join(out_dir, "story.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(order, open(os.path.join(out_dir, "order.json"), "w"))
    print(f"compilation: {n} stories, {t / 60:.1f} min -> {video}")
    if "--no-upload" in args:
        return
    pa = args[args.index("--publish-at") + 1] if "--publish-at" in args else None
    cmd = ["python3", os.path.join(HERE, "youtube_upload.py"), out_dir] + (["--publish-at", pa] if pa else [])
    subprocess.run(cmd, check=True)
    d = load(DONE, {"used": [], "videos": []})
    d["used"] += order
    d["videos"].append({"date": os.path.basename(out_dir), "stories": n,
                        "id": json.load(open(os.path.join(out_dir, "uploaded.json")))["id"]})
    json.dump(d, open(DONE, "w"), indent=1)
    q = load(QUEUE, {})
    for yid in order:  # free the release space
        if yid in q:
            gh("release", "delete-asset", RELEASE, q[yid]["asset"], "-y", check=False)
            q.pop(yid)
    json.dump(q, open(QUEUE, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stash":
        stash(sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) > 1 and sys.argv[1] == "build":
        main_build()
    else:
        print(__doc__)
