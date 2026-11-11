import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM

day = Day(__file__)
FERRY = lambda p, e: series("The Last Ferry", p, 2, e)

day.ep("roll-call", "rules",
   "[whispering] Never answer roll call after lights out. [quietly] In my hostel, a voice calls names at midnight. "
   "Last night, it called mine. I said, \"Present.\" [long pause] This morning, my roommate said, \"You walked out at "
   "midnight. Where did you go?\" [whispering] I never left my bed. So who walked out wearing my clothes? Subscribe... "
   "and never answer.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    clip("this-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("who-0.1", "WHO LEFT", "WEARING", "MY CLOTHES?", "Would you answer?", ("clothes", 0.4))],
   [("sting", "never", 0), ("heartbeat", "mine", 0), ("sting", "present", 0), ("sting", "who", 0)],
   ["present"], ["present", "who"],
   {"scene": 0, "lines": ["NEVER ANSWER", "ROLL CALL"], "sub": "after lights out"},
   "Never Answer the Hostel Roll Call After Lights Out",
   "In my hostel, a voice calls names at midnight. 🛏️ Last night it called mine, and I answered.",
   "Would you answer?",
   clips=[20837, 226811])

day.ep("ferry-p1", "series",
   "[whispering] Never take the last ferry home. [quietly] It left at midnight with twelve passengers. I counted. "
   "Halfway across the river, the engine stopped. The lights went out. [long pause] When they came back on, there were "
   "thirteen of us. [whispering] And everyone was staring at me. Part two is on my channel. Subscribe.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    title3("thirteen-0.3", "THERE WERE", "THIRTEEN", "OF US.", "Part 2 on the channel", ("part", 0.3))],
   [("sting", "never", 0), ("heartbeat", "engine", 0), ("sting", "thirteen", 0), ("sting", "staring", 0)],
   ["thirteen"], ["thirteen", "staring"],
   {"scene": 0, "lines": ["12 PASSENGERS.", "THEN 13."], "sub": "the last ferry home"},
   "The Last Ferry · Pt 1: 12 Passengers Left. 13 Were Counted.",
   "The last ferry left at midnight with twelve passengers. ⛴️ When the lights came back on, there were thirteen.",
   "Who do you think the 13th was?",
   clips=[380033], series=FERRY(1, "12 Passengers Left. 13 Were Counted."))

day.ep("ferry-p2", "series",
   "[whispering] Don't let them count you. [quietly] On the ferry, an old woman pointed at me. \"He wasn't here "
   "before.\" Everyone agreed. I showed them my ticket. It was dated 1979. [long pause] That ferry sank in 1979. "
   "Twelve survivors. [whispering] I've been riding it every night since... looking for a way off. Subscribe... and "
   "count the passengers.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    card("ticket-0.2", "T", "Ferry ticket · Last crossing", ["00:00 · Pier 4", "Date: 14 NOV 1979"]),
    title3("ive-0.1", "I'VE BEEN", "RIDING IT", "EVER SINCE.", "Part 1 is on the channel", ("way", 0.4))],
   [("sting", "dont", 0), ("sting", "pointed", 0), ("heartbeat", "ticket", 0), ("sting", "sank", 0), ("sting", "ive", 0)],
   ["sank"], ["sank", "ive"],
   {"scene": 0, "lines": ["MY TICKET", "SAID 1979"], "sub": "the last ferry, part 2"},
   "The Last Ferry · Pt 2: My Ticket Was From 1979",
   "\"He wasn't here before.\" ⛴️ I showed them my ferry ticket. It was dated 1979, the night the ferry sank.",
   "Did you guess the twist?",
   clips=[186545], series=FERRY(2, "My Ticket Was From 1979"))

day.ep("three-voices", "pick-one",
   "[whispering] Your name, three times, at 3 AM. [quietly] Once from the kitchen. Once from the closet. Once from "
   "under your bed. Only one of them is your mother. She's been dead for two years. [long pause] [whispering] The other "
   "two know that. Which one do you answer? Comment kitchen, closet or bed. Subscribe... before they call again.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    lines("once-0.2", [("KITCHEN", "kitchen", 0), ("CLOSET", "closet", 0), ("UNDER THE BED", "under", 0)],
          ("only one is your mother", "mother", 0)),
    clip("other-0.2", file="clip2.mp4", grade={"dim": 0.8, "tint": COOL}),
    title3("which-0.1", "KITCHEN,", "CLOSET", "OR BED?", "Comment your answer", ("comment", 0.3))],
   [("heartbeat", "three", 0), ("sting", "kitchen", 0), ("sting", "closet", 0), ("sting", "under", 0), ("sting", "dead", 0)],
   ["dead"], ["dead", "which"],
   {"scene": 0, "lines": ["3 VOICES.", "ONE IS MOM."], "sub": "she died two years ago"},
   "3 Voices Call Your Name at 3 AM. Only One Is Your Mom.",
   "Your name, three times, at 3 AM: kitchen, closet, under your bed. 🛏️ Only one is your mother. She died two years ago.",
   "Kitchen, closet or bed?",
   clips=[254651, "dark closet door"])

day.ep("old-phone", "text-story",
   "[whispering] Don't give your kid your old phone. [quietly] I gave my son mine. No SIM. No wifi. Last night, it "
   "buzzed. A text from a contact called \"Friend\": \"He's asleep. Can I come in now?\" [long pause] I typed, \"Who is "
   "this?\" [whispering] It answered: \"Look up. I already did.\" Subscribe... and check your kid's room.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    lock("buzzed-0.2", "3:07", "Friend", "He's asleep. Can I come in now?", "buzzed"),
    title3("look-0.1", "LOOK UP.", "I ALREADY", "DID.", "Would you look up?", ("did", 0.4))],
   [("buzz", "buzzed", 0), ("sting", "asleep", 0), ("heartbeat", "typed", 0), ("sting", "look", 0)],
   ["look"], ["asleep", "look"],
   {"scene": 0, "lines": ["NO SIM. NO WIFI.", "IT GOT A TEXT"], "sub": "my son's old phone"},
   "My Son's Old Phone Has No SIM. Last Night It Got a Text.",
   "My son's old phone has no SIM and no wifi. 📱 Last night it got a text: \"He's asleep. Can I come in now?\"",
   "Would you look up?",
   clips=[169445])

day.save()
