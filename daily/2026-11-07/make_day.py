import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM

day = Day(__file__)
WELL = lambda p, e: series("The Well", p, 2, e)

day.ep("exam-hall", "second-person",
   "[whispering] Thirty minutes into the exam, you hear a pen scratching. [quietly] Not yours. You look up. The hall "
   "is empty. Every desk is bare, except one. Your name is on it. [long pause] The paper is already finished. "
   "[whispering] The handwriting is yours... and the date is next year. Subscribe... and leave the hall before time.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    clip("empty-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("date-0.3", "THE DATE", "WAS NEXT", "YEAR.", "Would you read it?", ("subscribe", 0.4))],
   [("sting", "thirty", 0), ("heartbeat", "scratching", 0), ("sting", "finished", 0), ("sting", "year", 0)],
   ["finished"], ["finished", "next"],
   {"scene": 0, "lines": ["EMPTY HALL.", "PEN SCRATCHING"], "sub": "your paper is already done"},
   "Something Finished Your Exam Paper in an Empty Hall",
   "Thirty minutes into the exam, a pen scratches. The hall is empty. Your name is on one desk.",
   "Would you read it?",
   clips=["empty classroom dark", "school desk dark"])

day.ep("well-p1", "series",
   "[whispering] Never drop a coin in the village well. [quietly] Everyone knows. My cousin dared me anyway. I "
   "dropped one. It never splashed. [long pause] Instead, from far below, a child whispered, \"Thank you.\" Then "
   "the rope in my hands pulled tight. [whispering] Something was climbing. Part two is on my channel. Subscribe... "
   "and stay away from wells.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    title3("climbing-0.3", "SOMETHING", "WAS", "CLIMBING.", "Part 2 on the channel", ("part", 0.3))],
   [("sting", "never", 0), ("heartbeat", "splashed", 0), ("sting", "thank", 0), ("sting", "climbing", 0)],
   ["rope"], ["thank", "climbing"],
   {"scene": 0, "lines": ["NEVER DROP A", "COIN IN THE WELL"], "sub": "something thanked me"},
   "The Well · Pt 1: Never Drop a Coin in the Village Well",
   "My cousin dared me to drop a coin in the village well. It never splashed. A child whispered, thank you.",
   "Would you have dropped it?",
   clips=["old stone well", "village night fog"], series=WELL(1, "Never Drop a Coin in the Village Well"))

day.ep("well-p2", "series",
   "[whispering] Don't pull the rope. [quietly] I pulled it. A small wet hand came over the edge. A girl. She "
   "smiled. \"You gave me a coin. Now I can leave.\" [long pause] The villagers ran. My cousin screamed. [whispering] "
   "Because she wasn't looking at me. She was looking at him. \"Your turn to go down.\" Subscribe... and keep your coins.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    card("coin-0.2", "!", "Village well · Midnight", ["PAID: 1 COIN", "Debt: 1 LIFE"]),
    title3("your-0.1", "YOUR TURN", "TO GO", "DOWN.", "Part 1 is on the channel", ("turn", 0.4))],
   [("sting", "dont", 0), ("heartbeat", "hand", 0), ("sting", "girl", 0), ("sting", "turn", 0)],
   ["hand"], ["screamed", "turn"],
   {"scene": 0, "lines": ["SHE CLIMBED OUT", "OF THE WELL"], "sub": "the well, part 2"},
   "The Well · Pt 2: The Girl Climbed Out. She Wanted My Cousin.",
   "I pulled the rope. A small wet hand came over the edge. She was looking at my cousin.",
   "Did you guess the twist?",
   clips=["dark water well", "wet hand dark"], series=WELL(2, "The Girl Climbed Out. She Wanted My Cousin."))

day.ep("night-bus-seat", "rules",
   "[whispering] Never sit in the seat behind the driver on the night bus. [quietly] The conductor warned me. I "
   "sat there anyway, it was the only one free. The driver never blinked. [long pause] At my stop, he whispered, "
   "\"Thank you for keeping me company.\" [whispering] The conductor looked at me, pale. \"We have no driver "
   "tonight.\" Subscribe... and check who's driving.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("conductor-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("we-0.1", "THERE WAS", "NO DRIVER", "TONIGHT.", "Would you get off?", ("tonight", 0.4))],
   [("sting", "never", 0), ("heartbeat", "blinked", 0), ("sting", "company", 0), ("sting", "driver#3", 0)],
   ["blinked"], ["company", "driver#3"],
   {"scene": 0, "lines": ["NEVER SIT BEHIND", "THE DRIVER"], "sub": "the night bus had no driver"},
   "Never Sit Behind the Driver on the Night Bus",
   "The conductor warned me not to sit behind the driver. I did. At my stop, he thanked me for the company.",
   "Would you get off?",
   clips=["night bus interior", "bus driver night"])

day.ep("mom-voicecall", "voice-call",
   "[whispering] Mom called me at midnight. [quietly] She said, \"Beta, lock your door and don't open it for me.\" "
   "I laughed, she was in the next room. [long pause] Then someone knocked. Softly. \"Beta, open the door, "
   "it's Mom.\" [whispering] The phone was still ringing in my hand. Mom was calling from outside. Subscribe... "
   "and don't open it.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    call("then-0.2", "Mom"),
    title3("phone-0.2", "THE PHONE", "WAS STILL", "RINGING.", "Would you open it?", ("open", 0.4))],
   [("buzz", "mom", 0), ("heartbeat", "laughed", 0), ("sting", "knocked", 0), ("sting", "ringing", 0)],
   ["knocked"], ["knocked", "ringing"],
   {"scene": 0, "lines": ["MOM CALLED.", "SHE WAS INSIDE."], "sub": "don't open the door"},
   "Mom Called at Midnight: Lock the Door, Don't Open It",
   "Mom called at midnight and told me not to open the door. She was in the next room. Then someone knocked.",
   "Would you open it?",
   clips=["dark door handle night"])

day.save()
