"""Nov 3 - Nov 6 batch (18 Shorts: 3 tonight, then 5/day). Lessons from memory (channel-performance-learnings):
20-30 s; the FIRST LINE is a command / threat / impossible fact; real Pixabay footage in every Short; twist + comment
question; spoken "Subscribe..." + subscribe end card; #creepy #horror titles; new stories only.
New here: three 2-part series (Route 0, The 4th Bedroom, Dashcam). Part 1 ends on a cliffhanger that sends viewers
to Part 2 on the channel (end card says so); Part 2 airs in the next slot the same day. Link with series_link.py."""
import json, os, re
COOL, WARM = [0.82, 0.88, 1.12], [1.05, 0.92, 0.82]
TAGS = "#shorts #scarystories #horror #creepy #horrorstory #scary"
TAG_LIST = ("scary stories, horror shorts, creepy story, short horror story, scary, ghost story, paranormal, "
            "creepy, unread, horror rules, 3am")
HERE = os.path.dirname(os.path.abspath(__file__))
# slot order: (slug, ISO publish time, lock-screen date)
D = {3: "Tuesday, November 3", 4: "Wednesday, November 4", 5: "Thursday, November 5", 6: "Friday, November 6"}
SLOTS = [(3, "21:00"), (3, "21:45"), (3, "22:30")] + [(d, t) for d in (4, 5, 6) for t in ("12:30", "14:30", "16:30", "18:00", "19:30")]
ORDER, SCHEDULE = [], {}
FAST = {"n06-your-stop": 1.1, "n12-ceiling": 1.08, "n05-thirty-one": 1.05}  # keep spoken length near 30 s


def ep(slug, fmt, narration, scenes, sfx, shake, glitch, thumb, title, hook, question, series=None, extra_tags=""):
    d = os.path.join(HERE, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "narration.txt"), "w").write(narration.strip() + "\n")
    day, hhmm = SLOTS[len(ORDER)]
    ORDER.append(slug)
    SCHEDULE[slug] = f"2026-11-{day:02d}T{hhmm}:00+05:30"
    for s in scenes:
        if s["type"] == "lock":
            s["date"] = D[day]
    end_text = "PART 2 ON THE CHANNEL" if series and series["part"] == 1 else "NEW SCARY STORY EVERY NIGHT"
    more = ("Part 2 is already on the channel. Watch it next 👉 UNREAD" if series and series["part"] == 1 else
            "Missed Part 1? It's on the channel." if series else "More scary stories every night on UNREAD.")
    story = {"title": title, "format": fmt, "speed": FAST.get(slug, 1.0), "tail": 3.0, "transitions": "fade",
             "shake": shake, "glitch": glitch, "silence_from": "subscribe",
             "sfx": [dict(type=t, at=a, **({"delay": dl} if dl else {})) for t, a, dl in sfx]
                    + [{"type": "buzz", "at": "subscribe", "delay": 1.6}],
             "subscribe": {"at": "subscribe", "text": end_text},
             "scenes": scenes, "thumbnail": thumb,
             "upload": {"title": f"{title} #creepy #horror"[:100],
                        "description": f"{hook}\n\n{question} Tell me in the comments 👇\n{more}\n"
                                       f"Subscribe to UNREAD for a new scary story every night.\n\n"
                                       f"Footage: Pixabay · Voice: AI narration\n\n{TAGS}{extra_tags}",
                        "tags": TAG_LIST}}
    if series:
        story["series"] = series
    json.dump(story, open(os.path.join(d, "story.json"), "w"), indent=1, ensure_ascii=False)


def title3(start, a, b, c, footer, fat, captions=True, delays=(0, 0.5, 1.0)):
    return {"type": "title", "start": start, "captions": captions,
            "lines": [{"text": t, "at": start, "delay": dl} for t, dl in zip((a, b, c), delays) if t],
            "footer": {"text": footer, "at": fat[0], "delay": fat[1]}}


def lines(start, items, footer=None, captions=True):
    s = {"type": "title", "start": start, "captions": captions,
         "lines": [{"text": t, "at": a, "delay": dl} for t, a, dl in items]}
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


ROUTE0 = lambda p, e: {"name": "Route 0", "part": p, "of": 2, "episode": e}
ROOM4 = lambda p, e: {"name": "The 4th Bedroom", "part": p, "of": 2, "episode": e}
DASH = lambda p, e: {"name": "Dashcam", "part": p, "of": 2, "episode": e}

# ---------------- Tonight: Tuesday Nov 3 ----------------
ep("n01-whistle", "rules",
   "[whispering] Don't whistle after dark. [quietly] My grandmother said it calls them. Last night, walking home alone, "
   "I forgot. I whistled one song. [long pause] Behind me, something whistled it back. Every note. [whispering] Then it "
   "whistled the next song... the one I was about to pick. Subscribe... and keep quiet tonight.",
   [clip(speed=0.5, grade={"dim": 0.95, "tint": COOL}),
    title3("next-0.3", "IT KNEW", "MY NEXT", "SONG.", "Would you turn around?", ("pick", 0.4))],
   [("sting", "dont", 0), ("heartbeat", "behind", 0), ("sting", "every", 0), ("sting", "next", 0)],
   ["behind"], ["every", "next"],
   {"scene": 0, "lines": ["DON'T WHISTLE", "AFTER DARK"], "sub": "something whistles back"},
   "Never Whistle After Dark. Something Whistles Back",
   "My grandmother said whistling after dark calls them. 🎶 Last night I forgot. Something whistled it back.",
   "Would you turn around?")

ep("s1-p1-bus", "series",
   "[whispering] Never get on a bus with no number. [quietly] One stopped for me at 2 AM. Empty. Warm. The driver never "
   "looked at me. Every seat had a name tag. [long pause] The last row had mine. And under my name... a stop. Tonight. "
   "[whispering] Part two is on my channel. Subscribe... before it stops for you.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    card("last-0.2", "0", "Route 0 · Last row", ["RESERVED: YOU", "Your stop: TONIGHT"]),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Route 0 continues", ("channel", 0.3))],
   [("sting", "never", 0), ("heartbeat", "every", 0), ("sting", "mine", 0), ("sting", "tonight", 0)],
   ["mine"], ["mine", "tonight"],
   {"scene": 0, "lines": ["NEVER BOARD", "BUS NO. 0"], "sub": "every seat has a name tag"},
   "Route 0 · Pt 1: Never Get on a Bus With No Number",
   "A bus with no number stopped for me at 2 AM. 🚌 Every seat had a name tag. The last row had mine.",
   "Would you get on?", ROUTE0(1, "Never Get on a Bus With No Number"))

ep("s1-p2-bus", "series",
   "[whispering] Don't read the other name tags. [quietly] I did. They were all people from my street. Each one had a "
   "stop. My neighbor's stop was yesterday. He never came home. [long pause] I begged the driver to let me off. He "
   "finally turned around. [whispering] It was my neighbor. Smiling. Subscribe... and check your street tonight.",
   [clip(grade={"dim": 0.6, "desat": 0.5, "tint": COOL}),
    card("my-0.2", "!", "Seat 9 · Mr. Davis", ["Next door neighbor", "Stop: YESTERDAY"]),
    title3("smiling-0.9", "IT WAS", "MY", "NEIGHBOR.", "Part 1 is on the channel", ("smiling", 0.5))],
   [("sting", "dont", 0), ("heartbeat", "begged", 0), ("sting", "smiling", 0)],
   ["turned"], ["yesterday", "smiling"],
   {"scene": 0, "lines": ["THE DRIVER", "WAS MY NEIGHBOR"], "sub": "he went missing yesterday"},
   "Route 0 · Pt 2: My Missing Neighbor Was Driving the Bus",
   "Every seat on Route 0 had a name from my street. 🚌 My neighbor's stop was yesterday. He never came home.",
   "Who do you think is next?", ROUTE0(2, "My Missing Neighbor Was Driving the Bus"))

# ---------------- Wednesday Nov 4 ----------------
ep("n02-two-nurses", "pick-one",
   "[whispering] Two nurses walk into your hospital room at 3 AM. [quietly] Both say, \"Time for your medicine.\" One "
   "whispers, \"Don't let her touch you. She died here in 1996.\" [long pause] [whispering] Then the other one whispers "
   "the exact same thing. Which nurse do you trust? Comment one or two. Subscribe... before your next dose.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    clip("then-0.2", file="clip2.mp4", grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    title3("which", "NURSE 1", "OR", "NURSE 2?", "Comment 1 or 2", ("comment", 0.3))],
   [("heartbeat", "two", 0), ("sting", "died", 0), ("sting", "exact", 0), ("sting", "which", 0)],
   ["died"], ["died", "exact"],
   {"scene": 0, "lines": ["2 NURSES.", "ONE IS DEAD."], "sub": "3 AM, hospital room"},
   "2 Nurses Walk In at 3 AM. One Died Here in 1996",
   "Two nurses walk into your hospital room at 3 AM. 🏥 Both say one of them died here in 1996.",
   "Which nurse do you trust, 1 or 2?")

ep("s2-p1-fourth-door", "series",
   "[whispering] Don't use the fourth bedroom. [quietly] That's what my landlord texted on my first night. My apartment "
   "has three. I laughed... then counted the doors in the hallway. Four. [long pause] The fourth one was locked from the "
   "inside. [whispering] And under it, a light just turned on. Part two is on my channel. Subscribe... and count your doors.",
   [{"type": "lock", "clock": "11:48", "note_from": "Landlord", "note_body": "Please don't use the fourth bedroom.",
     "note_at": "dont"},
    clip("counted-0.2", grade={"dim": 1.05, "tint": WARM}),
    title3("light-0.2", "A LIGHT", "JUST", "TURNED ON.", "Part 2 on the channel", ("part", 0.3))],
   [("buzz", "dont", 0), ("heartbeat", "counted", 0), ("sting", "four", 0), ("sting", "light", 0)],
   ["four"], ["four", "light"],
   {"scene": 0, "lines": ["DON'T USE THE", "4TH BEDROOM"], "sub": "my apartment has three"},
   "The 4th Bedroom · Pt 1: My Apartment Only Has Three",
   "My landlord texted: \"Please don't use the fourth bedroom.\" 🚪 My apartment has three.",
   "Would you open it?", ROOM4(1, "My Apartment Only Has Three"))

ep("s2-p2-fourth-door", "series",
   "[whispering] Never knock on a door that isn't yours. [quietly] I knocked on the fourth door. Something knocked back. "
   "Then my landlord texted: \"You knocked. Now it knows you're home.\" [long pause] This morning, there are three doors "
   "again. [whispering] And my landlord just texted a new tenant... \"Don't use the fourth bedroom.\" I'm in it. "
   "Subscribe... and never knock back.",
   [clip(grade={"dim": 0.9}),
    {"type": "lock", "start": "then-0.2", "clock": "3:12", "note_from": "Landlord",
     "note_body": "You knocked. Now it knows you're home.", "note_at": "landlord"},
    title3("im-0.1", "I'M", "IN", "IT.", "Part 1 is on the channel", ("subscribe", -0.6))],
   [("knock", "knocked", 0), ("knock", "back", 0), ("knock", "back", 0.45), ("buzz", "then", 0), ("sting", "three", 0),
    ("sting", "im", 0)],
   ["back"], ["three", "im"],
   {"scene": 0, "lines": ["SOMETHING", "KNOCKED BACK"], "sub": "the 4th bedroom, part 2"},
   "The 4th Bedroom · Pt 2: Something Knocked Back",
   "I knocked on the fourth door. 🚪 Something knocked back. Then my landlord texted: \"Now it knows you're home.\"",
   "Would you have knocked?", ROOM4(2, "Something Knocked Back"))

ep("n03-corner", "text-story",
   "[whispering] Never let your baby sleep facing the corner. [quietly] Every night, my son laughs at it. Giggles. "
   "Reaches up. Last night, I filmed him on my phone. [long pause] On the video, the corner leans down... and laughs "
   "with him. [whispering] Then it looks straight into the camera. Subscribe... and turn the crib around.",
   [clip(grade={"dim": 1.0, "tint": WARM}),
    card("filmed-0.2", "●", "REC · Nursery", ["00:03:14", "2 faces detected"]),
    title3("then-0.2", "THEN IT", "LOOKED AT", "THE CAMERA.", "Would you keep filming?", ("camera", 0.4))],
   [("heartbeat", "every", 0), ("sting", "leans", 0), ("sting", "looks", 0)],
   ["leans"], ["leans", "looks"],
   {"scene": 0, "lines": ["MY BABY LAUGHS", "AT THE CORNER"], "sub": "so I filmed it"},
   "My Baby Laughs at the Corner Every Night. I Filmed It.",
   "Every night my son laughs at the corner of his room. 👶 Last night I filmed it.",
   "Would you turn the crib around?")

ep("n04-seven-coins", "rules",
   "[whispering] Never pick up money from the road at night. [quietly] I found seven coins outside my gate. I kept them. "
   "At midnight, someone knocked. Seven times. [long pause] A voice said, \"You took my fare. Now you take my place.\" "
   "[whispering] This morning, there are seven coins outside my gate again. And I can't go back inside. Subscribe... "
   "and leave the coins.",
   [clip(grade={"dim": 0.9, "tint": WARM}),
    title3("cant-0.2", "I CAN'T", "GO BACK", "INSIDE.", "Would you pick them up?", ("inside", 0.4))],
   [("knock", "seven#2", 0), ("knock", "seven#2", 0.35), ("knock", "seven#2", 0.7), ("knock", "seven#2", 1.05),
    ("sting", "fare", 0), ("sting", "cant", 0)],
   ["fare"], ["fare", "cant"],
   {"scene": 0, "lines": ["NEVER PICK UP", "ROAD MONEY"], "sub": "it's someone's fare"},
   "Never Pick Up Coins From the Road at Night",
   "I found seven coins outside my gate and kept them. 🪙 At midnight, someone knocked. Seven times.",
   "Would you pick them up?")

# ---------------- Thursday Nov 5 ----------------
ep("n05-thirty-one", "text-story",
   "[whispering] Thirty desks. Thirty-one students. [quietly] The examiner counted us three times during our final "
   "exam. Always thirty-one. Nobody moved. [long pause] At the end, he collected thirty-one papers. One had no name. "
   "[whispering] Just one line, in my handwriting: \"Thank you for letting me sit with you.\" Subscribe... and count "
   "your class.",
   [lines(None, [("30 DESKS.", "thirty", 0), ("31 STUDENTS.", "thirtyone", 0)], captions=False),
    clip("examiner-0.2", grade={"dim": 0.85, "desat": 0.3, "tint": COOL}),
    title3("thank-0.1", "THANK YOU", "FOR LETTING", "ME SIT.", "Who wrote it?", ("sit", 0.4))],
   [("sting", "thirtyone", 0), ("heartbeat", "always", 0), ("sting", "name", 0), ("sting", "handwriting", 0)],
   ["name"], ["name", "handwriting"],
   {"scene": 1, "lines": ["30 DESKS.", "31 STUDENTS."], "sub": "one paper had no name"},
   "30 Desks. 31 Students. One Exam Paper Had No Name.",
   "Thirty desks. Thirty-one students. 📝 One exam paper had no name, just a line in my handwriting.",
   "Who do you think wrote it?")

ep("s3-p1-dashcam", "series",
   "[whispering] Don't watch last night's dashcam. [quietly] I did. It shows me driving home at 1 AM. Then I pull over "
   "on a road I've never seen. I get out. I walk into the trees. [long pause] I don't remember any of it. [whispering] "
   "Forty minutes later... someone walks back out and drives my car home. Part two is on my channel. Subscribe.",
   [clip(grade={"dim": 1.1, "tint": COOL}),
    card("pull-0.2", "●", "DASHCAM · 01:12 AM", ["Vehicle stopped", "Driver exited"]),
    title3("someone-0.1", "SOMEONE", "WALKED", "BACK OUT.", "Part 2 on the channel", ("part", 0.3))],
   [("sting", "dont", 0), ("heartbeat", "trees", 0), ("sting", "someone", 0)],
   ["someone"], ["trees", "someone"],
   {"scene": 0, "lines": ["DON'T WATCH", "MY DASHCAM"], "sub": "I walked into the trees"},
   "Dashcam · Pt 1: My Dashcam Shows Me Walking Into the Woods",
   "My dashcam shows me pulling over at 1 AM and walking into the trees. 🚗 I don't remember any of it.",
   "Who drove the car home?", DASH(1, "My Dashcam Shows Me Walking Into the Woods"))

ep("s3-p2-dashcam", "series",
   "[whispering] Never watch the rest of the footage. [quietly] The thing that drove my car home sat in the driveway and "
   "stared into the dashcam for an hour. Not blinking. Then it whispered, \"Tomorrow, you drive.\" [long pause] Tonight, "
   "my car started by itself. [whispering] The GPS already has a destination. The trees. Subscribe... and never check "
   "your dashcam.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    title3("tomorrow-0.1", "TOMORROW,", "YOU", "DRIVE.", "Part 1 is on the channel", ("drive", 0.4)),
    card("tonight-0.2", "G", "GPS · Route set", ["Destination: THE TREES", "Arriving in 40 min"])],
   [("sting", "never", 0), ("heartbeat", "stared", 0), ("sting", "tomorrow", 0), ("buzz", "started", 0), ("sting", "trees", 0)],
   ["tomorrow"], ["tomorrow", "trees"],
   {"scene": 1, "lines": ["TOMORROW,", "YOU DRIVE"], "sub": "dashcam, part 2"},
   "Dashcam · Pt 2: It Stared Into the Camera and Said: You Drive",
   "The thing that drove my car home stared into the dashcam for an hour. 🚗 Then it whispered: \"Tomorrow, you drive.\"",
   "Would you get in the car?", DASH(2, "It Stared Into the Camera and Said: You Drive"))

ep("n06-your-stop", "rules",
   "[whispering] If the train calls your stop, get off. [quietly] Last night, the speaker said: \"Next stop, Harmon "
   "Street. Passenger in car four, this is your stop.\" There is no Harmon Street. I was the only one in car four. "
   "[long pause] The doors opened onto a platform full of people. [whispering] All staring at me. All wearing my face. "
   "Subscribe... and stay on the train.",
   [clip(speed=0.5, grade={"dim": 0.9, "tint": COOL}),
    card("next-0.2", "M", "Metro · Car 4", ["Next: HARMON STREET", "This is your stop."]),
    title3("wearing-0.4", "ALL", "WEARING", "MY FACE.", "Would you get off?", ("face", 0.4))],
   [("buzz", "next", 0), ("sting", "only", 0), ("heartbeat", "doors", 0), ("sting", "wearing", 0)],
   ["staring"], ["only", "wearing"],
   {"scene": 0, "lines": ["CAR 4,", "THIS IS YOUR STOP"], "sub": "there is no Harmon Street"},
   "The Train Said: Passenger in Car 4, This Is Your Stop",
   "\"Passenger in car four, this is your stop.\" 🚇 I was the only one in car four. There is no Harmon Street.",
   "Would you get off?")

ep("n07-red-light", "text-story",
   "[whispering] Don't roll your window down at a red light. [quietly] At 2 AM, a little boy knocked on my car window. "
   "Barefoot. Soaking wet. \"Can you take me home? I live in your house.\" [long pause] I drove off. [whispering] When I "
   "got home, my wife opened the door and said, \"There you are, sweetheart.\" We don't have kids. Subscribe.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    title3("kids-0.9", "WE DON'T", "HAVE", "KIDS.", "Who did she let in?", ("kids", 0.4))],
   [("knock", "knocked", 0), ("knock", "knocked", 0.4), ("sting", "house", 0), ("heartbeat", "drove", 0), ("sting", "kids", 0)],
   ["house"], ["house", "kids"],
   {"scene": 0, "lines": ["\"I LIVE IN", "YOUR HOUSE\""], "sub": "a barefoot boy at a red light"},
   "A Barefoot Boy Knocked on My Car Window: I Live in Your House",
   "At 2 AM, a barefoot boy knocked on my car window at a red light. 🚦 \"Can you take me home? I live in your house.\"",
   "Who did she let in?")

# ---------------- Friday Nov 6 ----------------
ep("n08-dog-stares", "text-story",
   "[whispering] Trust your dog. [quietly] Since my wife came home from the hospital, our dog won't stop staring at her. "
   "He growls when she walks by. He won't sleep in our room. Last night, he finally barked at her. [long pause] "
   "[whispering] She looked at him... and barked back. Exactly like him. Subscribe... and watch your dog tonight.",
   [clip(grade={"dim": 0.95, "tint": WARM}),
    title3("looked-0.3", "SHE", "BARKED", "BACK.", "Would you trust her?", ("exactly", 0.3))],
   [("heartbeat", "staring", 0), ("sting", "barked", 0), ("sting", "back", 0)],
   ["back"], ["barked", "back"],
   {"scene": 0, "lines": ["MY DOG WON'T", "STOP STARING"], "sub": "at my wife"},
   "Since My Wife Came Home, Our Dog Won't Stop Staring at Her",
   "Since my wife came home from the hospital, our dog won't stop staring at her. 🐕 Last night he barked. She barked back.",
   "Would you trust her?")

ep("n09-cleaner", "text-story",
   "[whispering] Don't take the mirror down. [quietly] I live in a studio. One room. But my cleaning app said: four "
   "rooms cleaned. The cleaner left a note. \"The room behind your mirror was filthy. Please feed him less.\" [long pause] "
   "I took the mirror down. Just a wall. [whispering] But the wall is warm... and something just knocked. Subscribe.",
   [clip(grade={"dim": 1.0, "tint": WARM}),
    {"type": "lock", "start": "app-0.3", "clock": "6:05", "note_from": "SparkleClean",
     "note_body": "Job complete: 4 rooms cleaned. Rate your cleaner!", "note_at": "app"},
    card("note-0.2", "!", "Note from your cleaner", ["The room behind your mirror", "was filthy. Please feed him less."]),
    title3("warm-0.3", "THE WALL", "IS", "WARM.", "Would you take it down?", ("knocked", 0.3))],
   [("buzz", "app", 0), ("sting", "feed", 0), ("heartbeat", "wall", 0), ("knock", "knocked", 0), ("knock", "knocked", 0.4)],
   ["knocked"], ["feed", "warm"],
   {"scene": 0, "lines": ["I HAVE 1 ROOM.", "SHE CLEANED 4."], "sub": "the room behind the mirror"},
   "I Live in a Studio. My Cleaner Cleaned 4 Rooms.",
   "I live in a one-room studio. 🧹 My cleaner's note: \"The room behind your mirror was filthy. Please feed him less.\"",
   "Would you take the mirror down?")

ep("n10-wedding-photo", "text-story",
   "[whispering] Don't look at my parents' wedding photo. [quietly] There's a woman in white behind them. Nobody knows "
   "who she is. And every year, she stands a little closer. [long pause] Last night, Mom called me, crying. [whispering] "
   "The woman is in front of them now. And Mom is gone from the picture. Subscribe... and check your old photos.",
   [clip(grade={"dim": 0.9, "desat": 0.2, "tint": WARM}),
    {"type": "call", "start": "mom-0.2", "contact": "Mom"},
    title3("gone-0.6", "MOM IS", "GONE FROM", "THE PHOTO.", "Check your old photos.", ("picture", 0.3))],
   [("heartbeat", "every", 0), ("buzz", "called", 0), ("sting", "front", 0), ("sting", "gone", 0)],
   ["front"], ["closer", "gone"],
   {"scene": 0, "lines": ["SHE GETS CLOSER", "EVERY YEAR"], "sub": "my parents' wedding photo"},
   "Every Year, the Woman in My Parents' Wedding Photo Gets Closer",
   "There's a woman in white behind my parents in their wedding photo. 📷 Every year, she stands a little closer.",
   "Would you burn the photo?")

ep("n11-thirteen-percent", "second-person",
   "[whispering] Don't let your phone die tonight. [quietly] It's the only light in your room. It's at thirteen percent. "
   "And you can hear breathing in the dark... just past the glow. [long pause] It's been waiting every night for your "
   "screen to go black. Look how close it's gotten. [whispering] Twelve percent. Subscribe... and plug it in.",
   [clip(grade={"dim": 0.85, "tint": COOL}),
    lines("thirteen-0.2", [("13%", "thirteen", 0)], ("something is waiting", "breathing", 0.2)),
    clip("waiting-0.3", **{"from": 6, "grade": {"dim": 0.6, "tint": COOL}}),
    title3("twelve-0.1", "12%", "AND", "FALLING.", "Plug it in.", ("plug", 0))],
   [("heartbeat", "breathing", 0), ("sting", "close", 0), ("sting", "twelve", 0)],
   ["twelve"], ["close", "twelve"],
   {"scene": 0, "lines": ["DON'T LET YOUR", "PHONE DIE"], "sub": "it's at 13%"},
   "Don't Let Your Phone Die Tonight. It's at 13%.",
   "Your phone is the only light in your room. 🔋 It's at 13%. Something is waiting for the screen to go black.",
   "What's your battery at right now?")

ep("n12-ceiling", "rules",
   "[whispering] If someone calls your name from the ceiling... don't look up. [quietly] My little sister told me that, "
   "the week before she went missing. Last night in bed, I heard her voice. Right above me. \"Look at me. Please. I'm so "
   "tired.\" [long pause] I didn't look. [whispering] Then her hand touched my face. Upside down. Subscribe... and don't "
   "look up.",
   [clip(grade={"dim": 1.0, "tint": COOL}),
    title3("upside-0.3", "HER HAND", "WAS", "UPSIDE DOWN.", "Would you look up?", ("down", 0.4))],
   [("heartbeat", "above", 0), ("sting", "tired", 0), ("sting", "hand", 0), ("sting", "upside", 0)],
   ["hand"], ["hand", "upside"],
   {"scene": 0, "lines": ["DON'T", "LOOK UP"], "sub": "if it calls your name"},
   "If Someone Calls Your Name From the Ceiling, Don't Look Up",
   "If someone calls your name from the ceiling, don't look up. 👀 My missing sister's voice called me last night.",
   "Would you look up?")

json.dump({"order": ORDER, "schedule": SCHEDULE}, open(os.path.join(HERE, "schedule.json"), "w"), indent=1)
if __name__ == "__main__":
    for d in ORDER:
        w = len(re.sub(r"\[[^\]]+\]", "", open(os.path.join(HERE, d, "narration.txt")).read()).split())
        print(d, w, "words", SCHEDULE[d])
