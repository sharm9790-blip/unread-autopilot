import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM

day = Day(__file__)
DIARY = lambda p, e: series("The Diary", p, 2, e)

day.ep("terrace-steps", "rules",
   "[whispering] Never count the steps to the terrace. [quietly] Grandpa said there are twelve. Always twelve. Last night, "
   "carrying clothes up, I counted thirteen. [long pause] I turned back. The stairs below me kept going down... into the "
   "dark. [whispering] Then someone whispered, \"Finally. Someone counted.\" Subscribe... and never count the steps.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    clip("turned-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("finally-0.1", "SOMEONE", "FINALLY", "COUNTED.", "Would you go back down?", ("subscribe", 0.4))],
   [("sting", "never", 0), ("heartbeat", "thirteen", 0), ("sting", "dark", 0), ("sting", "finally", 0)],
   ["thirteen"], ["thirteen", "finally"],
   {"scene": 0, "lines": ["NEVER COUNT THE", "STEPS UP"], "sub": "grandpa said there are twelve"},
   "Never Count the Steps to the Terrace. I Counted 13",
   "Grandpa said there are twelve steps to the terrace. Last night I counted thirteen. Then the stairs kept going down.",
   "Would you go back down?",
   clips=["dark staircase night", "photo: old concrete stairs"])

day.ep("diary-p1", "series",
   "[whispering] Never buy a diary after the shop closes. [quietly] The old shopkeeper sold me one at 7:01 PM. Page one was "
   "in my handwriting. It described tonight. My room. My lamp. [long pause] The last line said: \"You'll read this at 9:14.\" "
   "My clock said 9:13. [whispering] Part two is on my channel. Subscribe... before the shop closes.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    card("last-0.2", "!", "Diary · Page 1", ["MY ROOM. MY LAMP.", "You'll read this at 9:14"]),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "The Diary continues", ("channel", 0.3))],
   [("sting", "never", 0), ("heartbeat", "handwriting", 0), ("sting", "clock", 0), ("sting", "channel", 0)],
   ["handwriting"], ["lamp", "clock"],
   {"scene": 0, "lines": ["NEVER BUY", "A DIARY LATE"], "sub": "page one was my handwriting"},
   "The Diary · Pt 1: Never Buy a Diary After the Shop Closes",
   "The shopkeeper sold me a diary at 7:01 PM. Page one described my room, my lamp, and the exact minute I'd read it.",
   "Would you open it?",
   clips=["old notebook dark", "photo: old shop night"], series=DIARY(1, "Never Buy a Diary After the Shop Closes"))

day.ep("diary-p2", "series",
   "[whispering] Don't read the last page. [quietly] I read it anyway. It said: \"Look up.\" The ceiling fan was still. "
   "In the lamp's reflection, the shopkeeper stood behind me. [long pause] \"Every diary needs a writer,\" he said. "
   "[whispering] My hand was already holding the pen... and it was writing his next line. Subscribe... and leave the last page alone.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    card("pen-0.2", "●", "Diary · Last page", ["WRITER: YOU", "Next line: ..."]),
    title3("writing-0.1", "MY HAND", "WROTE HIS", "NEXT LINE.", "Part 1 is on the channel", ("page", 0.4))],
   [("sting", "dont", 0), ("heartbeat", "look", 0), ("sting", "writer", 0), ("sting", "writing", 0)],
   ["shopkeeper"], ["writer", "writing"],
   {"scene": 0, "lines": ["DON'T READ", "THE LAST PAGE"], "sub": "the shopkeeper was behind me"},
   "The Diary · Pt 2: The Shopkeeper Was Standing Behind Me",
   "I read the last page. The shopkeeper stood behind me in the lamp's reflection. Then my hand started writing.",
   "Did you guess the twist?",
   clips=["dark room lamp night", "photo: antique pen paper"], series=DIARY(2, "The Shopkeeper Was Standing Behind Me"))

day.ep("water-tank", "monologue",
   "[whispering] Three knocks on the water tank. Every night at 3. [quietly] Dad said it's just the pipes. Tonight I counted "
   "four. [long pause] I climbed the ladder and opened the lid. The water was dark and still... and the knocking came from "
   "inside. [whispering] Then it whispered, \"Four. Because you're here.\" Subscribe... and count the knocks.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("climbed-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("four-0.1", "FOUR.", "BECAUSE", "YOU'RE HERE.", "Would you open the lid?", ("knocks", 0.4))],
   [("knock", "three", 0), ("heartbeat", "four", 0), ("sting", "inside", 0), ("sting", "here", 0)],
   ["inside"], ["four", "inside"],
   {"scene": 0, "lines": ["3 KNOCKS", "FROM THE TANK"], "sub": "tonight there were four"},
   "Three Knocks Every Night From the Water Tank. Tonight, Four.",
   "Dad said it's just the pipes. Tonight I counted four knocks, opened the lid, and something answered from inside.",
   "Would you open the lid?",
   clips=["dark rooftop night", "photo: rusty water tank"])

day.ep("sister-text", "text-story",
   "[whispering] Your sister texts you: Come downstairs. [quietly] She's asleep beside you. Still breathing. The phone buzzes "
   "again. \"Why aren't you coming?\" [long pause] Footsteps climb the stairs. Slow. [whispering] Then your sister opens her "
   "eyes. \"Don't open the door,\" she whispers. \"That isn't me out there.\" Subscribe... and never go downstairs.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    lock("asleep", "3:07", "Sister", "Come downstairs", "phone"),
    card("why-0.2", "!", "Sister · Message", ["Why aren't you coming?", "Seen 3:07 AM"]),
    title3("isnt-0.1", "THAT ISN'T", "ME OUT", "THERE.", "Would you go down?", ("subscribe", 0.4))],
   [("buzz", "texts", 0), ("buzz", "again", 0), ("sting", "footsteps", 0), ("sting", "isnt", 0)],
   ["footsteps"], ["whispers", "isnt"],
   {"scene": 0, "lines": ["SISTER TEXTS:", "COME DOWNSTAIRS"], "sub": "she's asleep beside you"},
   "Your Sister Texts: Come Downstairs. She's Asleep Beside You",
   "Your sister texts you to come downstairs. She's asleep next to you. Then the footsteps start climbing.",
   "Would you go down?",
   clips=["dark bedroom stairs", "photo: phone glowing dark room"])

day.save()
