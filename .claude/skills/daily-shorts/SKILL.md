---
name: daily-shorts
description: Write today's 5 UNREAD scary Shorts (stories + scenes + Pixabay search queries) into daily/<date>/, lint them, and push so GitHub Actions voices, renders and schedules them on YouTube. Use for the daily cloud routine or "/daily-shorts".
---

# Daily UNREAD Shorts (story writer)

You write the stories. GitHub Actions (`.github/workflows/produce.yml`) does everything else when you push:
Pixabay clips → ElevenLabs voice → render → YouTube upload at 12:30 / 14:30 / 16:30 / 18:00 / 19:30 IST → series links → Telegram report.
You need no API keys. Never upload, never touch secrets.

## Steps

1. Work on branch `claude/daily-shorts` (`git fetch origin && git checkout claude/daily-shorts && git pull`).
   Today's date = the date in **Asia/Kolkata** (`TZ=Asia/Kolkata date +%F`). If `daily/<date>/day.json` already exists, stop: today is done.
2. Read `LEARNINGS.md` (what wins on this channel - follow every rule), `stories_index.json` (titles already used - never reuse
   a title or its premise), and the narrations in the last 7 `daily/*/` folders (don't repeat their twists or settings).
3. Write `daily/<date>/make_day.py` with exactly **5 episodes**, in slot order:
   - slot 1 (12:30): standalone
   - slots 2-3 (14:30, 16:30): **one 2-part series** (Part 1 ends on a cliffhanger: "...Part two is on my channel. Subscribe...";
     Part 2 opens with a new command line, pays it off with a twist, footer "Part 1 is on the channel")
   - slots 4-5 (18:00, 19:30): standalones
   Rotate formats across the day: rules / pick-one (comment 1, 2 or 3) / second-person / text-story / voice-call.
   Use the helpers in `pipeline/batchlib.py` (`Day`, `clip`, `title3`, `lines`, `card`, `lock`, `call`, `series`, `COOL`, `WARM`).
   Copy the structure of the example below.
4. Run `python3 daily/<date>/make_day.py` then `python3 pipeline/check_day.py daily/<date>`. Fix every problem it lists and re-run until it prints `OK`.
5. `git add daily/<date> && git commit -m "day <date>: <5 titles, short>" && git push origin claude/daily-shorts`. That push starts production.
   Reply with the 5 titles and their slots.

## Story rules (from the channel's analytics - see LEARNINGS.md)

- **45-55 words** of narration → 25-30 s. Never over 58 words.
- **First line = the hook: 5-12 words, the scary word in the first 3** ("Don't whistle after dark." / "Thirty desks.
  Thirty-one students."). Never open on setup, a greeting or a neutral notification.
- **Put a number or a name in the hook when it fits** ("after 9 PM", "Bus 0", "Room 214", "seven coins"): concrete beats vague.
- Hook formulas that work for horror (rotate them across the day, name the one you used in `fmt` notes):
  - *Negative command* - "Never answer roll call after lights out." (the channel's proven winner)
  - *Impossible number* - "30 desks. 31 students."
  - *Mid-sentence start* - "...and that's when the second voice answered." (fill in the setup by second 8)
  - *Callout* - "Hostel students: never answer the midnight roll call." (people tag friends → shares)
  - *Verbatim question* - "Why does my dog stare at the corner at 3 AM?" (matches what people search)
  - *Pick one* - "3 doors. Only one is your mom." (comment 1, 2 or 3)
- One clear twist in the last 2 lines, then the comment question in the description, then the spoken `Subscribe... <tag line>`.
- **Loop:** the tag line after "Subscribe..." **repeats a word from the hook** so the replay connects
  ("Don't whistle after dark ... Subscribe... and never whistle after dark."). Part 1s too: "Subscribe... before the last ferry leaves."
  `check_day.py` rejects a day without it.
- ElevenLabs v3 tags allowed: `[whispering]`, `[quietly]`, `[long pause]`, `[slowly]`. Start with `[whispering]`.
- Settings that fit viewers in India / Malaysia / Philippines / Indonesia are welcome (village rules, night buses, hostels,
  exam halls, family homes), but keep names short and the language simple.
- Titles end up as "<title> #creepy #horror": write a curiosity-gap title under 70 characters.

## Scenes

- Every episode needs at least one `clip()` scene (real footage). The **first scene has no start**.
- `clips=[...]`: one Pixabay **video** search query per clip file, in order (clip.mp4, clip2.mp4...). 2-4 plain words that describe
  dark, real footage: "dark hallway door", "hospital corridor night", "rain car window night". Avoid words that return cartoons
  ("baby", "christmas", "cute"). Production picks a dark, unused hit automatically, ranking the nouns first.
  **Better:** if you can open pixabay.com/videos/search/<words>/ (web fetch or browser), look at the results and put the
  chosen video's numeric id instead of the query (e.g. `clips=[20837, "dark bedroom night"]`). Never reuse ids in
  `state/used_clips.json`.
- Anchors are narration words (lowercase, punctuation dropped: "don't" → `dont`, "I'm" → `im`, "Thirty-one" → `thirtyone`),
  matched by prefix, searched forward from the previous scene's start; `word#2` = 2nd match, `word-0.3` = 0.3 s earlier.
  Beware prefixes: `we` also matches "wet" - pick distinctive words.
- End with `title3(...)` on the twist (3 short ALL-CAPS lines + footer question). UI scenes: `lock(...)` notification,
  `card(...)` (avatar letter/●/!, header, 1-2 lines), `call(start, "Mom")`, `lines(...)` for big custom text.
- `sfx`: (type, anchor, delay) with type `sting` / `heartbeat` / `knock` / `buzz`. `shake`/`glitch`: lists of anchor words.
- `thumb`: {"scene": index of a clip scene, "lines": [white line, red line] (≤14 chars each, max 16), "sub": "small line"}.
  **The same two lines are the on-screen hook card for the first 2.8 s** (read before the voice is heard, most viewers
  start muted), so make them the hook in ≤6 words total, e.g. ["DON'T WHISTLE", "AFTER DARK"].
- Change the picture every ~4 s: footage auto-punches in/out every 3.5 s, but still add a 2nd clip, a `card` or a `lock`
  in the middle instead of one clip for 15+ seconds.
- `speed=1.05-1.1` only if a story runs long.

## Example (copy the shape)

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM

day = Day(__file__)

day.ep("whistle", "rules",
   "[whispering] Don't whistle after dark. [quietly] My grandmother said it calls them. Last night, walking home alone, "
   "I forgot. I whistled one song. [long pause] Behind me, something whistled it back. Every note. [whispering] Then it "
   "whistled the next song... the one I was about to pick. Subscribe... and never whistle after dark.",
   [clip(speed=0.5, grade={"dim": 0.95, "tint": COOL}),
    title3("next-0.3", "IT KNEW", "MY NEXT", "SONG.", "Would you turn around?", ("pick", 0.4))],
   [("sting", "dont", 0), ("heartbeat", "behind", 0), ("sting", "every", 0), ("sting", "next", 0)],
   ["behind"], ["every", "next"],
   {"scene": 0, "lines": ["DON'T WHISTLE", "AFTER DARK"], "sub": "something whistles back"},
   "Never Whistle After Dark. Something Whistles Back",
   "My grandmother said whistling after dark calls them. Last night I forgot. Something whistled it back.",
   "Would you turn around?",
   clips=["dark street night walking"])

day.ep("bus-p1", "series",
   "[whispering] Never get on a bus with no number. [quietly] One stopped for me at 2 AM. Empty. Warm. The driver never "
   "looked at me. Every seat had a name tag. [long pause] The last row had mine. And under my name... a stop. Tonight. "
   "[whispering] Part two is on my channel. Subscribe... before the bus with no number stops for you.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    card("last-0.2", "0", "Route 0 · Last row", ["RESERVED: YOU", "Your stop: TONIGHT"]),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Route 0 continues", ("channel", 0.3))],
   [("sting", "never", 0), ("heartbeat", "every", 0), ("sting", "mine", 0), ("sting", "tonight", 0)],
   ["mine"], ["mine", "tonight"],
   {"scene": 0, "lines": ["NEVER BOARD", "BUS NO. 0"], "sub": "every seat has a name tag"},
   "Route 0 · Pt 1: Never Get on a Bus With No Number",
   "A bus with no number stopped for me at 2 AM. Every seat had a name tag. The last row had mine.",
   "Would you get on?",
   clips=["bus night city"], series=series("Route 0", 1, 2, "Never Get on a Bus With No Number"))

# ... bus-p2 (series part 2), then two more standalones ...
day.save()
```

More worked examples (UI scenes, pick-one, second-person, lock screens): see `examples/batch-nov03.py`.
