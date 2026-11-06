"""Helpers for daily/<YYYY-MM-DD>/make_day.py (written by the daily routine, see .claude/skills/daily-shorts).

    from batchlib import Day, clip, title3, lines, card, lock, call, COOL, WARM
    day = Day(__file__)                      # date comes from the folder name
    day.ep("whistle", "rules", narration, scenes, sfx, shake, glitch, thumb, title, hook, question,
           clips=["dark street night walking", "foggy alley night"])
    day.save()

Each ep gets the next slot (12:30, 14:30, 16:30, 18:00, 19:30 IST). `clips` are Pixabay video search queries, in order:
clip("...") scenes use clip.mp4, clip2.mp4 ... matching them. produce.py downloads the best hit for each.
Series: pass series=series("Route 0", part, 2, "Episode title"); Part 1 must end "Part two is on my channel. Subscribe...".
"""
import datetime
import json
import os
import re

COOL, WARM, CCTV = [0.82, 0.88, 1.12], [1.05, 0.92, 0.82], [0.78, 1.05, 0.82]
SLOTS = ["12:30", "14:30", "16:30", "18:00", "19:30"]
TAGS = "#shorts #scarystories #horror #creepy #horrorstory #scary"
TAG_LIST = ("scary stories, horror shorts, creepy story, short horror story, scary, ghost story, paranormal, "
            "creepy, unread, horror rules, 3am")


def title3(start, a, b, c, footer, fat, captions=True, delays=(0, 0.5, 1.0)):
    return {"type": "title", "start": start, "captions": captions,
            "lines": [{"text": t, "at": start, "delay": dl} for t, dl in zip((a, b, c), delays) if t],
            "footer": {"text": footer, "at": fat[0], "delay": fat[1]}}


def lines(start, items, footer=None, captions=True):
    s = {"type": "title", "start": start, "captions": captions,
         "lines": [{"text": t, "at": a, "delay": dl} for t, a, dl in items]}
    if start is None:
        s.pop("start")
    if footer:
        s["footer"] = {"text": footer[0], "at": footer[1], "delay": footer[2]}
    return s


def clip(start=None, file="clip.mp4", **kw):
    s = {"type": "clip", "file": file, "loop": True, "grade": kw.pop("grade", {"dim": 0.85, "tint": COOL})}
    if start:
        s["start"] = start
    s.update(kw)
    return s


def card(start, avatar, head, body):
    return {"type": "card", "start": start, "avatar": avatar, "title": head, "lines": body}


def lock(start, clock, sender, body, note_at, red_at=None):
    s = {"type": "lock", "clock": clock, "note_from": sender, "note_body": body, "note_at": note_at}
    if start:
        s["start"] = start
    if red_at:
        s["red_at"] = red_at
    return s


def call(start, contact):
    return {"type": "call", "start": start, "contact": contact}


def series(name, part, of, episode):
    return {"name": name, "part": part, "of": of, "episode": episode}


class Day:
    def __init__(self, file):
        self.dir = os.path.dirname(os.path.abspath(file))
        self.date = datetime.date.fromisoformat(os.path.basename(self.dir))
        self.order, self.schedule, self.clips = [], {}, {}

    def ep(self, slug, fmt, narration, scenes, sfx, shake, glitch, thumb, title, hook, question,
           clips, series=None, speed=1.0, extra_tags=""):
        d = os.path.join(self.dir, slug)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "narration.txt"), "w").write(narration.strip() + "\n")
        hhmm = SLOTS[len(self.order)]
        self.order.append(slug)
        self.schedule[slug] = f"{self.date.isoformat()}T{hhmm}:00+05:30"
        self.clips[slug] = clips
        for s in scenes:
            if s["type"] == "lock":
                s["date"] = self.date.strftime("%A, %B ") + str(self.date.day)
        p1 = series and series["part"] < series["of"]
        end_text = f"PART {series['part'] + 1} ON THE CHANNEL" if p1 else "NEW SCARY STORY EVERY NIGHT"
        more = ("The next part is already on the channel. Watch it next 👉 UNREAD" if p1 else
                "Missed the earlier part? It's on the channel." if series else "More scary stories every night on UNREAD.")
        story = {"title": title, "format": fmt, "speed": speed, "tail": 3.0, "transitions": "fade",
                 "shake": shake, "glitch": glitch, "silence_from": "subscribe",
                 "sfx": [dict(type=t, at=a, **({"delay": dl} if dl else {})) for t, a, dl in sfx]
                        + [{"type": "buzz", "at": "subscribe", "delay": 1.6}],
                 "subscribe": {"at": "subscribe", "text": end_text},
                 "scenes": scenes, "thumbnail": thumb,
                 "upload": {"title": f"{title} #creepy #horror"[:100], "playlist": "scary",
                            "description": f"{hook}\n\n{question} Tell me in the comments 👇\n{more}\n"
                                           f"Subscribe to UNREAD for a new scary story every night.\n\n"
                                           f"Footage: Pixabay · Voice: AI narration\n\n{TAGS}{extra_tags}",
                            "tags": TAG_LIST}}
        if series:
            story["series"] = series
        json.dump(story, open(os.path.join(d, "story.json"), "w"), indent=1, ensure_ascii=False)

    def save(self):
        json.dump({"date": self.date.isoformat(), "order": self.order, "schedule": self.schedule, "clips": self.clips},
                  open(os.path.join(self.dir, "day.json"), "w"), indent=1)
        for slug in self.order:
            w = len(re.sub(r"\[[^\]]+\]", "", open(os.path.join(self.dir, slug, "narration.txt")).read()).split())
            print(slug, w, "words", self.schedule[slug])
