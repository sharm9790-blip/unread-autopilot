import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM

day = Day(__file__)
PA = lambda p, e: series("Photo Album", p, 2, e)

day.ep("tiffin", "text-story",
   "[whispering] Never eat the second tiffin. [quietly] Mom packs two every morning. I'm an only child. Today I asked "
   "who it's for. She smiled. \"The girl behind you.\" [long pause] I turned. Nobody. [whispering] Then a tiny voice "
   "said, \"Thanks, didi.\" Subscribe... and never eat the second tiffin.",
   [clip(grade={"dim": 0.95, "tint": WARM}),
    card("mom-0.2", "M", "Mom · Morning", ["Two tiffins packed", "The second one is not for you"]),
    clip("turned-0.2", file="clip3.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("thanks-0.1", "SOMETHING", "THANKED ME.", "FROM BEHIND.", "Would you turn around?", ("didi", 0.2))],
   [("sting", "never", 0), ("heartbeat", "only", 0), ("sting", "turned", 0), ("sting", "thanks", 0)],
   ["turned"], ["tiny", "thanks"],
   {"scene": 0, "lines": ["NEVER EAT THE", "SECOND TIFFIN"], "sub": "mom packs two. I'm an only child"},
   "Mom Packs Two Tiffins. I'm an Only Child.",
   "Mom packs two tiffins every morning, but I have no siblings. When I asked who the second one was for, she said the girl behind me.",
   "Would you turn around?",
   clips=["kitchen morning dark",
          {"ai": "Two steel tiffin boxes on a dim kitchen counter at dawn, one lid slightly open, a faint small shadow behind them, close-up",
           "move": "dolly-in", "fallback": "photo: steel tiffin box kitchen"},
          {"ai": "An empty school classroom bench seen from behind in dim light, a small steel tiffin box on the desk behind it",
           "motion": "the tiffin lid slowly lifts open on its own", "fallback": "empty classroom dark"}])

day.ep("window-wave", "second-person",
   "[whispering] Don't wave back at the window. [quietly] My son waves goodnight to it every night. We live on the "
   "fifth floor. Tonight I looked. [long pause] A pale hand waved from outside the glass. [whispering] Then my wife, "
   "fast asleep beside me, waved back. Subscribe... and don't wave at the window.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    clip("looked-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("hand-0.2", file="clip3.mp4"),
    title3("wife-0.1", "MY WIFE", "WAVED BACK.", "ASLEEP.", "Would you wake her?", ("back", 0.4))],
   [("sting", "dont", 0), ("heartbeat", "fifth", 0), ("sting", "hand", 0), ("sting", "wife", 0)],
   ["pale"], ["hand", "wife"],
   {"scene": 0, "lines": ["DON'T WAVE BACK", "AT THE WINDOW"], "sub": "we live on the fifth floor"},
   "My Son Waves Goodnight to the Window. We're on the Fifth Floor.",
   "My son waves goodnight to our window every night. We live on the fifth floor. Tonight something waved back, and so did my sleeping wife.",
   "Would you wake her?",
   clips=["dark bedroom window night",
          {"ai": "A dark apartment bedroom window at night, curtain half open, city lights far below, a faint pale smear on the glass, wide shot",
           "move": "dolly-in", "fallback": "photo: dark window night"},
          {"ai": "A bedroom window at night seen from the bed in shadow, a pale thin hand pressed against the outside of the glass",
           "motion": "the pale hand slowly waves outside the glass", "fallback": "window rain night dark"}])

day.ep("album-p1", "series",
   "[whispering] Never ask Dad about the cut photos. [quietly] In every family album, one person is cut out. Always "
   "beside me. Last night Dad took a Diwali photo. I checked the screen. [long pause] [whispering] "
   "A tall gap stood beside me. Part two is on my channel. Subscribe... never ask Dad about the photos.",
   [clip(grade={"dim": 0.9, "tint": WARM}),
    card("diwali-0.2", "D", "Dad · Diwali Photo", ["1 photo taken", "Someone is missing beside you"]),
    clip("screen-0.2", file="clip3.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Photo Album continues", ("channel", 0.3))],
   [("sting", "never", 0), ("heartbeat", "album", 0), ("sting", "gap", 0), ("sting", "tall", 0)],
   ["gap"], ["tall", "gap"],
   {"scene": 0, "lines": ["DAD CUTS ONE", "PERSON OUT"], "sub": "of every family photo"},
   "Photo Album · Pt 1: Dad Cuts Someone Out of Every Family Photo",
   "In every family album Dad cuts one person out. Always the same height, always beside me. Last night his new photo had a gap too.",
   "Would you ask Dad?",
   clips=["old photo album dark",
          {"ai": "An old family photo album open on a table, one tall figure cut out of a group photo leaving a dark gap beside a child, warm lamp, close-up",
           "move": "dolly-in", "fallback": "photo: old family photo album"},
          {"ai": "A camera screen glowing in a dim living room showing a family photo with a tall black gap beside a girl, close-up",
           "motion": "the screen flickers and the black gap slowly widens", "fallback": "camera screen dark room"}],
   series=PA(1, "Dad Cuts Someone Out of Every Family Photo"))

day.ep("album-p2", "series",
   "[whispering] Don't ask Dad who was cut out. [quietly] I did. He wept. \"Your twin. She never left the house.\" "
   "[long pause] He opened the album. [whispering] Every photo of me was cut out. He couldn't see me. "
   "Subscribe... and don't ask Dad about the photos.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    card("twin-0.2", "!", "Album · Page 1", ["PHOTOS OF YOU: 0", "Every one was cut out"]),
    title3("couldnt-0.1", "DAD COULD", "NOT SEE", "ME.", "Part 1 is on the channel", ("see", 0.4))],
   [("sting", "dont", 0), ("heartbeat", "twin", 0), ("sting", "every", 0), ("sting", "couldnt", 0)],
   ["wept"], ["every", "couldnt"],
   {"scene": 0, "lines": ["EVERY PHOTO OF", "ME IS CUT OUT"], "sub": "photo album, part 2"},
   "Photo Album · Pt 2: Dad Can't See Me in Any Photo",
   "Dad said the one cut from every photo was my twin. Then he opened the album and every photo of me was cut out too.",
   "Did you guess the twist?",
   clips=["dark living room old photos",
          {"ai": "A crying man sitting in a dim living room holding an old photo album, seen from behind, a girl faint at the doorway far away",
           "move": "dolly-in", "fallback": "photo: dark living room old"},
          {"ai": "An old photo album open under a lamp, every photo of a girl cut into a clean empty outline, close-up, dim room",
           "motion": "the lamp flickers and a faint pale shape appears in one empty outline", "fallback": "old album dark"}],
   series=PA(2, "Dad Can't See Me in Any Photo"))

day.save()
