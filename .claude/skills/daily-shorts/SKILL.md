---
name: daily-shorts
description: Write today's 4 UNREAD scary Shorts (stories + scenes + Pixabay search queries) into daily/<date>/, lint them, and push so GitHub Actions voices, renders and schedules them on YouTube. Use for the daily cloud routine or "/daily-shorts".
---

# Daily UNREAD Shorts (story writer)

You write the stories. GitHub Actions (`.github/workflows/produce.yml`) does everything else when you push:
Pixabay clips → ElevenLabs voice → render → YouTube upload at 12:30 / 18:00 / 19:30 IST → series links → Telegram report.
You need no API keys. Never upload, never touch secrets.

## Steps

1. Work on branch `claude/daily-shorts` (`git fetch origin && git checkout claude/daily-shorts && git pull`).
   Today's date = the date in **Asia/Kolkata** (`TZ=Asia/Kolkata date +%F`). If `daily/<date>/day.json` already exists, stop: today is done.
2. Read `LEARNINGS.md` (what wins on this channel - follow every rule), `stories_index.json` (titles already used - never reuse
   a title or its premise), and the narrations in the last 7 `daily/*/` folders (don't repeat their twists or settings).
   Also read `state/winners.json` (refreshed 08:00 daily from live views): `top` = Shorts that passed ~1K, `bottom` = flops.
   **Double down:** the standalone must reuse the *shape* of a `top` entry (same kind of threat, same title pattern,
   e.g. "<family member> did X. <contradiction>.") with a brand-new premise. Never echo a `bottom` entry's setting or pattern.
   Also read `state/viral.json`: scary Shorts from OTHER channels that went viral in the last 14 days, ranked by
   `outlier` (views ÷ channel subscribers: high = the idea and hook did the work, not the channel's size). Learn the
   **title and hook patterns** (e.g. "If your cat ever hisses at you when you come home... DON'T GO INSIDE",
   "My mom texted me at 3:17... but she was asleep next to my hospital bed", "6 rules for the night shift at ..."),
   then write your own new story. **Never copy** a viral video's story, title, twist or lines.
   And `state/social_viral.json`: the same for **TikTok and Instagram** (hook = first line of the caption). Borrow
   their *patterns* ("Grandma's rule: if she calls my name after midnight, don't answer", "Dad's outside, but Mom says
   it's not him. Who do you trust?", "Our door says 4... we're only 3"). Their videos run 60-180 s; **ours stay
   25-30 s** because that's what wins on YouTube Shorts for UNREAD.
   And `state/vidiq_research.md` (vidIQ outlier research across YouTube/Instagram/TikTok): pick one of its 6 patterns
   for at least one episode a day (e.g. a pet that warns a family member is an impostor; "Mom does X twice";
   "In <place>, if ... at night" for Indian/Filipino settings; Grandma's one warning).
   **Vary the idea:** don't repeat yesterday's opening word, setting or twist type (repetitive ideas get skipped).
3. Write `daily/<date>/make_day.py` with exactly **3 episodes** (batchlib assigns the slots):
   - 1 standalone → 12:30. Make it the strongest story of the day.
   - **one 2-part series** → Part 1 at 18:00, Part 2 at 19:30 (Part 1 ends on a cliffhanger: "...Part two is on my channel.
     Subscribe..."; Part 2 opens with a new command line, pays it off with a twist, footer "Part 1 is on the channel").
     Part 1 must work as a complete scare on its own: viewers who never see Part 2 still need a payoff.
   (3/day from Nov 15: views per Short fell when we posted 4-5/day on Nov 11-14; fewer, stronger posts did better in October.)
   Rotate formats across the day: rules / pick-one (comment 1, 2 or 3) / second-person / text-story / voice-call.
   Use the helpers in `pipeline/batchlib.py` (`Day`, `clip`, `title3`, `lines`, `card`, `lock`, `call`, `series`, `COOL`, `WARM`).
   Copy the structure of the example below.
4. Run `python3 daily/<date>/make_day.py` then `python3 pipeline/check_day.py daily/<date>`. Fix every problem it lists and re-run until it prints `OK`.
5. `git add daily/<date> && git commit -m "day <date>: <3 titles, short>" && git push origin claude/daily-shorts`. That push starts production.
   Reply with the 3 titles and their slots.

## Languages (translated title + first description line; the voice stays English)
- Every `day.ep(...)` gets `langs={...}` with **all 26 codes** in `pipeline/check_day.py` LANGS:
  hi ta te bn mr ur · fil id ms my th vi · es pt fr de it nl sv pl ru tr · ar ja ko zh-CN.
  UNREAD's viewers are India 26%, US 21%, Philippines 16%, UK 7%, Malaysia 7%, Indonesia 6%, then Sweden, Germany,
  Italy, Myanmar...; the rest are YouTube's biggest language markets. Viewers whose YouTube is set to a language see
  that title and hook. `check_day.py` rejects a day with any code missing.
  ```python
  langs={"hi": {"title": "अंधेरे के बाद कभी सीटी मत बजाना", "hook": "दादी कहती थीं कि सीटी उन्हें बुलाती है।"},
         "es": {"title": "Nunca Silbes Después del Anochecer", "hook": "Mi abuela decía que silbar los llama."},
         # ... all 26 codes
         }
  ```
  Tip: build it once per episode as a dict literal; keep each hook to one short sentence.
- Translate the *meaning* naturally, the way a native speaker would title it (keep the threat and the contradiction);
  under 70 characters; keep names, numbers and "Pt 1"/"Pt 2". Don't add hashtags (they're appended automatically).

## First 3 seconds (decide whether YouTube keeps pushing the Short)
- Frame 1 = **real moving footage** (first entry in `clips=[...]` is a Pixabay query or pinned id, never `photo:` or AI;
  `check_day.py` enforces it), the on-screen hook card, and a `("sting", <first hook word>, 0)` so it starts loud.
- The scariest line is the first line. No setup, no "So last night...".
- **Line 2 (seconds 3-8) escalates at once** with a second impossible detail: retention falls from ~100% to ~60%
  there on every UNREAD Short. Never spend line 2 on explanation. Put one more turn ~75% of the way in.
- **Write for UNREAD's real audience: adults 25-44 (65% of viewers), many of them parents.** Threats to a child,
  baby, partner or parent at home beat teen/school-life settings.
- Pass `share="<the friend who ...>"` to `day.ep(...)`, fitted to the story ("the friend who sleeps with the door open",
  "your sister"): it becomes "📤 Send this to ... 👀" in the description. Shares are the channel's weakest signal (≈0).

## Story rules (from the channel's analytics - see LEARNINGS.md)

- **40-48 words** of narration (lint allows 36-50). The voice reads ~1.75 words/s, plus a 3 s end card: 48 words ≈ 30 s.
  Production speeds the voice up to 1.15x to land at ≤30 s, and the Telegram report flags any Short still over 30 s.
  ≤30 s Shorts get ~3x the views of 31-44 s ones (median 599 vs 144), so cut setup words, never the twist.
- **First line = the hook: 5-12 words, the scary word in the first 3** ("Don't whistle after dark." / "My baby
  laughs at the corner every night."). Never open on setup, a greeting or a neutral notification.
- **Put a number or a name in the hook when it fits** ("after 9 PM", "Bus 0", "Room 214", "seven coins"): concrete beats vague.
- Hook formulas that work for horror (rotate them across the day, name the one you used in `fmt` notes):
  - *Negative command* - "Never answer roll call after lights out." (the channel's proven winner)
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
- **Title formula that wins here** (Nov 3-7: these got 730-1,050 views): *a threat inside the home or family* + *a short
  second sentence that contradicts it*. "The School Said Dad Picked Him Up. I'm His Dad." / "A Man Whispered on My Baby
  Monitor. I Live Alone." / "Something Held My Foot in Bed. My Wife Was at Work." / "Since My Wife Came Home, Our Dog Won't
  Stop Staring at Her". Use baby, child, spouse, parent, pet, your own bed / room / phone.
- **Avoid** (79-190 views): number puzzles and abstract setups ("30 Desks. 31 Students.", "3 Elevators Open at 3 AM"),
  transit and public places with no one you love in them ("The Train Said: Passenger in Car 4"), chores or objects
  ("My Cleaner Cleaned 4 Rooms"). Each day, at least 2 of the 3 titles use the winning formula.

## Scenes

- Every episode needs at least one `clip()` scene (real footage). The **first scene has no start**.
- `clips=[...]`: one Pixabay **video** search query per clip file, in order (clip.mp4, clip2.mp4...). 2-4 plain words that describe
  dark, real footage: "dark hallway door", "hospital corridor night", "rain car window night". Avoid words that return cartoons
  ("baby", "christmas", "cute"). Production picks a dark, unused hit automatically, ranking the nouns first.
  **Better:** if you can open pixabay.com/videos/search/<words>/ (web fetch or browser), look at the results and put the
  chosen video's numeric id instead of the query (e.g. `clips=[20837, "dark bedroom night"]`). Never reuse ids in
  `state/used_clips.json`.
- **Photo clips (free motion):** when no footage fits (a specific room, object, old photo, place), use a still instead:
  `"photo: abandoned motel room"` or `{"photo": "abandoned motel room", "move": "dolly-in"}` in `clips=[...]`. Production
  takes a vertical Pixabay photo and animates it into a 10 s 2.5D camera move with fog and dust (`pipeline/parallax.py`).
  Moves: dolly-in, dolly-out, orbit, pan-left, pan-right, rise, fall (default rotates per clip); optional `dur`,
  `strength` (0.07), `fog` (0.2), `dust` (40). Mix them: about 1 photo clip per episode alongside real footage.
  A video query with no usable hit falls back to a photo clip automatically.
- **AI clips (paid, fal.ai, ~$0.40/day budget):** story-specific shots that stock footage can't give. Per episode use
  **exactly 2 AI entries**: one hero clip on the scare beat and one AI still; any other clip stays a free Pixabay query.
  - Hero: `{"ai": "<shot>", "motion": "<what moves>", "fallback": "<2-4 pixabay words>"}` → AI still animated into a
    6 s AI video. Motion must be small and slow: "the figure's head turns toward camera", "the door opens an inch",
    "the monitor screen flickers and a face appears". No fast action, no talking, no text on screen.
  - Still: `{"ai": "<shot>", "fallback": "<words>", "move": "dolly-in"}` → AI still with the free parallax camera move.
  - `<shot>` is one concrete sentence a cinematographer could shoot: subject, place, light, framing, e.g.
    "A green-lit baby monitor on a dark nightstand, its screen showing a crib with a tall thin figure beside it,
    close-up, 3 AM". The house horror style (dark, film grain, realistic, no text) is added automatically.
    Keep people at a distance, in shadow or from behind (faces in AI stills look fake up close). No gore, no
    children in danger shown on screen (suggest it: an empty crib, a small shoe), no real brands or famous people.
  - Put the hero clip where the twist lands (its scene starts on the twist anchor), the still earlier.
  - If fal has no key, hits the daily cap or fails, production uses the `fallback` words as a free Pixabay photo clip,
    so always give a good `fallback`.
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
    clip("every-0.2", file="clip2.mp4"),   # AI still (clips[1])
    card("last-0.2", "0", "Route 0 · Last row", ["RESERVED: YOU", "Your stop: TONIGHT"]),
    clip("mine-0.2", file="clip3.mp4"),    # AI hero clip on the twist (clips[2])
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Route 0 continues", ("channel", 0.3))],
   [("sting", "never", 0), ("heartbeat", "every", 0), ("sting", "mine", 0), ("sting", "tonight", 0)],
   ["mine"], ["mine", "tonight"],
   {"scene": 0, "lines": ["NEVER BOARD", "BUS NO. 0"], "sub": "every seat has a name tag"},
   "Route 0 · Pt 1: Never Get on a Bus With No Number",
   "A bus with no number stopped for me at 2 AM. Every seat had a name tag. The last row had mine.",
   "Would you get on?",
   clips=["bus night city",
          {"ai": "Rows of empty seats inside a dim night bus, each seat with a small paper name tag, shot down the aisle, "
                 "cold fluorescent light", "move": "dolly-in", "fallback": "empty bus seats night"},
          {"ai": "The last row of an empty night bus, one paper name tag lit by a flickering tube light, the driver a "
                 "dark shape far away in the mirror", "motion": "the light flickers and the driver's head slowly turns "
                 "toward camera", "fallback": "bus interior dark"}],
   series=series("Route 0", 1, 2, "Never Get on a Bus With No Number"))

# Every episode needs exactly these 2 AI entries (check_day.py rejects the day otherwise); the whistle example above
# predates them - add one AI still + one AI hero clip to it the same way.

# ... bus-p2 (series part 2) (3 total; batchlib sets the slots) ...
day.save()
```

More worked examples (UI scenes, pick-one, second-person, lock screens): see `examples/batch-nov03.py`.
