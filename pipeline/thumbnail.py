"""Thumbnail + upload pack for an episode.

Usage: python3 thumbnail.py <episode_dir>
  reads story.json "thumbnail": {"scene": i, "lines": [white, red], "sub": "small text"}
  and   story.json "upload": {"title", "description", "tags"}
  writes thumbnail.png (1080x1920), thumbnail.jpg (smaller) and upload.md
"""
import os
import runpy
import sys

from PIL import Image, ImageDraw

EP = sys.argv[1]
g = runpy.run_path(os.path.join(os.path.dirname(__file__), "render.py"), run_name="lib")
story, scenes = g["STORY"], g["SCENES"]
th = story.get("thumbnail", {})
s = dict(scenes[th.get("scene", 0)])
s["title_lines"] = []  # the thumbnail draws its own big text; don't double it with the scene's title
s.pop("subtitle", None)
t = min(s["_end"], g["DUR"]) - 0.15  # scene fully built
img = g["SCENE_FN"][s["type"]](s, t)
d = ImageDraw.Draw(img)
colors = [(255, 255, 255), (230, 25, 25)]
for i, txt in enumerate(th.get("lines", [])[:2]):
    size = 230
    while True:
        f = g["font"](g["F_CAP"], size)
        w = d.textlength(txt, font=f)
        if w <= 940:
            break
        size -= 6
    d.text(((1080 - w) / 2, 1180 + i * 250), txt, font=f, fill=colors[i],
           stroke_width=12, stroke_fill=(0, 0, 0))
if th.get("sub"):
    f = g["font"](g["F_BOLD"], 64)
    d.text(((1080 - d.textlength(th["sub"], font=f)) / 2, 1720), th["sub"], font=f, fill=(200, 200, 200))
out = Image.fromarray(g["post"](img, 0.0, 0))
out.save(os.path.join(EP, "thumbnail.png"))
out.resize((720, 1280)).save(os.path.join(EP, "thumbnail.jpg"), quality=90)

up = story.get("upload", {})
with open(os.path.join(EP, "upload.md"), "w") as fh:
    fh.write(f"# {up.get('title', story.get('title', ''))}\n\n## Description\n```\n{up.get('description', '')}\n```\n\n"
             f"## Tags\n```\n{up.get('tags', '')}\n```\n\nThumbnail: thumbnail.png (or pick the frame from scene {th.get('scene', 0) + 1})\n")
print("thumbnail.png + upload.md")
