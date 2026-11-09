"""Lint a day before it is committed (no API keys needed): every anchor word exists in the narration, in scene order;
narration length; subscribe line; clip queries vs clip files; titles not already used (stories_index.json).

Usage: python3 pipeline/check_day.py daily/<YYYY-MM-DD>     -> prints OK or the problems (exit 1)
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANCHOR = re.compile(r"^(?P<tok>[a-z0-9:' ]+?)(?:#(?P<n>\d+))?(?P<off>[+-]\d+(?:\.\d+)?)?$")


def clean_words(text):
    text = re.sub(r"\[[^\]]+\]", " ", text)
    return ["".join(c for c in w.lower() if c.isalnum() or c == ":") for w in text.split()]


def find(words, spec, after):
    """index of the anchor word (prefix match, n-th after `after`), or None"""
    if spec is None or isinstance(spec, (int, float)):
        return after
    m = ANCHOR.match(str(spec).strip().lower())
    if not m:
        return None
    tok, n = m["tok"].strip().replace("'", ""), int(m["n"] or 1)
    for i, w in enumerate(words):
        if i >= after and w and w.startswith(tok):
            n -= 1
            if n == 0:
                return i
    return None


def check(day_dir):
    day = json.load(open(os.path.join(day_dir, "day.json")))
    index = json.load(open(os.path.join(ROOT, "stories_index.json")))
    used = {t.lower() for t in index["titles"]}
    problems = []
    if len(day["order"]) != 4:
        problems.append(f"expected 4 episodes (2 standalones + a 2-part series), got {len(day['order'])}")
    times = sorted(t[11:16] for t in day["schedule"].values())
    if times != ["12:30", "16:30", "18:00", "19:30"]:
        problems.append(f"slots {times}: need 12:30 + 16:30 standalones and the series at 18:00 / 19:30")
    for slug in day["order"]:
        ep = os.path.join(day_dir, slug)
        st = json.load(open(os.path.join(ep, "story.json")))
        words = clean_words(open(os.path.join(ep, "narration.txt")).read())
        p = lambda msg: problems.append(f"{slug}: {msg}")
        if not 36 <= len(words) <= 50:
            p(f"{len(words)} words (keep 40-48: the voice reads ~1.75 words/s, and Shorts over 30 s get a third of the views)")
        if "subscribe" not in words:
            p("narration has no 'Subscribe...' line")
        else:  # loop: the closing tag line echoes the hook so the replay connects
            first = re.split(r"[.!?]", re.sub(r"\[[^\]]+\]", " ", open(os.path.join(ep, "narration.txt")).read()).strip())[0]
            hook_w = {w for w in clean_words(first) if len(w) >= 4}
            tail = words[len(words) - words[::-1].index("subscribe"):]
            if not hook_w & set(tail):
                p(f"closing line after 'Subscribe...' must repeat a word from the hook ({', '.join(sorted(hook_w)) or first!r})")
            if len(clean_words(first)) > 12:
                p(f"hook sentence has {len(clean_words(first))} words (keep it 5-12)")
        for ln in st.get("thumbnail", {}).get("lines", []):
            if len(ln) > 16:
                p(f"thumb/hook card line {ln!r} is {len(ln)} chars (max 16, it is read at frame 1)")
        if st["title"].lower() in used:
            p(f"title already used: {st['title']}")
        prev = 0
        for k, s in enumerate(st["scenes"]):
            if k == 0 and s.get("start"):
                p("first scene must not have a start")
            i = find(words, s.get("start"), prev) if k else 0
            if i is None:
                p(f"scene {k} start {s.get('start')!r} not found after word {prev}")
                continue
            for key in ("note_at", "red_at", "figure_at", "eyes_at"):
                if s.get(key) and find(words, s[key], i) is None:
                    p(f"scene {k} {key} {s[key]!r} not found")
            for ln in (s.get("lines", []) if s["type"] == "title" else []) + ([s["footer"]] if s.get("footer") else []):
                if find(words, ln.get("at"), i) is None:
                    p(f"scene {k} line {ln.get('text')!r} at {ln.get('at')!r} not found")
            if s["type"] == "clip" and not re.fullmatch(r"clip\d*\.mp4", s["file"]):
                p(f"scene {k} clip file must be clip.mp4 / clip2.mp4 ...")
            prev = i
        n_files = {s["file"] for s in st["scenes"] if s["type"] == "clip"}
        if not n_files:
            p("no Pixabay clip scene")
        if len(day["clips"].get(slug, [])) < len(n_files):
            p(f"{len(n_files)} clip files but {len(day['clips'].get(slug, []))} search queries")
        for x in st["sfx"]:
            if find(words, x["at"], 0) is None:
                p(f"sfx anchor {x['at']!r} not found")
        for w in st.get("shake", []) + st.get("glitch", []) + [st["subscribe"]["at"]]:
            if find(words, w, 0) is None:
                p(f"shake/glitch/subscribe anchor {w!r} not found")
    return problems


if __name__ == "__main__":
    probs = check(sys.argv[1].rstrip("/"))
    print("OK" if not probs else "\n".join(probs))
    sys.exit(1 if probs else 0)
