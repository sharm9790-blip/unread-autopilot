import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM
import langs as L

day = Day(__file__)
SR = lambda p, e: series("Fourth Chair", p, 2, e)

day.ep("imaginary-bed", "second-person",
   "[whispering] My son made a bed for his imaginary friend. [quietly] Tonight the blanket was warm. A dent in the pillow. "
   "Long black hairs. [long pause] My son whispered, \"Shh, he's sleeping. He says your bed is softer.\" "
   "[whispering] Subscribe... before your child makes a bed for a friend.",
   [clip(),
    clip("blanket-0.2", file="clip2.mp4"), clip("dent-0.2", file="clip3.mp4"),
    clip("hairs-0.2", file="clip4.mp4"), clip("shh-0.2", file="clip5.mp4"),
    clip("softer-0.3", file="clip6.mp4"),
    title3("softer-0.1", "HE SLEPT", "IN THE", "BED.", "Would you check yours?", ("subscribe", 0.4))],
   [("sting", "my", 0), ("heartbeat", "blanket", 0), ("sting", "hairs", 0), ("sting", "softer", 0)],
   ["softer"], ["hairs", "softer"],
   {"scene": 0, "lines": ["IMAGINARY FRIEND", "SLEPT HERE"], "sub": "the blanket was warm"},
   "My Son Made a Bed for His Imaginary Friend. It Was Slept In.",
   "My son made a bed for his imaginary friend. Tonight the blanket was warm, the pillow dented, long black hairs on it.",
   "Would you check your child's bed?",
   clips=[{"ai": "A small child's bed made up neatly with a blanket and pillow on a dark bedroom floor, a toy lamp glowing beside it, close-up", "key": True, "move": "dolly-in", "fallback": "child bed dark room"},
          {"ai": "A wrinkled blanket on the little bed with a faint wisp of warm steam rising from it, dark room, lamp light", "move": "pan-left", "fallback": "blanket bed night"},
          {"ai": "A pillow with a deep head-shaped dent in it, dim lamp light, close-up", "move": "rise", "fallback": "pillow bed dark"},
          {"ai": "Long black hairs lying across a white pillow, close-up, cold light", "move": "dolly-out", "fallback": "dark hair pillow"},
          {"ai": "Aman, a small boy in pyjamas, kneeling beside the little bed with a finger to his lips, Mama watching from the doorway, dark bedroom", "move": "orbit", "fallback": "child bedroom night"},
          {"ai": "A tall thin dark figure lying curled under the blanket of the little bed, its long black hair spilling over the pillow, Aman standing beside it smiling, lamp light", "key": True, "move": "fall", "fallback": "dark figure bedroom"}],
   look="2d", characters="Aman: Indian boy, 6, short black hair, blue striped pyjamas. Mama: Indian woman, 32, long black braid, green nightsuit, face in shadow.",
   share="the friend whose child talks to an imaginary friend",
   langs=L.build(L.E1_T, L.E1_H))

day.ep("fourth-chair-p1", "series",
   "[whispering] My son counts four at dinner. [quietly] We are three. He points at the empty chair: \"Mama, she says she sat here first.\" "
   "The chair slid back by itself. [long pause] My husband went white. \"Don't answer her.\" "
   "[whispering] Part two is on my channel. Subscribe... before you count four at dinner.",
   [clip(grade={"dim": 0.9, "tint": WARM}),
    clip("chair-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("white-0.3", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Fourth Chair continues", ("channel", 0.3))],
   [("sting", "my", 0), ("heartbeat", "empty", 0), ("sting", "slid", 0), ("sting", "white", 0)],
   ["slid"], ["slid", "white"],
   {"scene": 0, "lines": ["HE COUNTS FOUR", "WE ARE THREE"], "sub": "the empty chair slid back"},
   "Fourth Chair · Pt 1: My Son Counts Four at Dinner. We're Three",
   "My son counts four at dinner. We are three. He says someone sat in the empty chair first.",
   "Would you answer her?",
   clips=["family dinner table dark",
          {"ai": "A dim family dining table with three plates and one empty wooden chair pulled slightly back, warm yellow lamp, shot low", "move": "dolly-in", "fallback": "photo: dining table dark"},
          {"ai": "An Indian man at a dinner table staring at an empty chair, his face pale in shadow, his wife and small son beside him", "motion": "the empty chair slowly slides backward", "fallback": "dark dining room"}],
   series=SR(1, "My Son Counts Four at Dinner. We're Three"), share="the friend with a child who talks to empty chairs",
   langs=L.build(L.E2_T, L.E2_H))

day.ep("fourth-chair-p2", "series",
   "[whispering] Never answer the fourth chair. [quietly] My husband finally spoke: \"Her name was Meera. She died in this house before you.\" "
   "A fourth plate appeared on our table, steaming. [long pause] My son smiled. \"Mama, she says you're in her seat.\" "
   "[whispering] Subscribe... and never answer the fourth chair.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    clip("plate-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": WARM}),
    clip("smiled-0.3", file="clip3.mp4"),
    title3("subscribe-0.1", "SHE WANTS", "THE SEAT", "I'M IN.", "Part 1 is on the channel", ("fourth", 0.4))],
   [("sting", "never", 0), ("heartbeat", "meera", 0), ("sting", "plate", 0), ("sting", "seat", 0)],
   ["plate"], ["plate", "seat"],
   {"scene": 0, "lines": ["NEVER ANSWER", "THE 4TH CHAIR"], "sub": "her name was Meera"},
   "Fourth Chair · Pt 2: Her Plate Was Set. She Wants My Seat",
   "My husband finally told me who sits in the fourth chair. Then a fourth plate appeared, steaming.",
   "Whose seat are you sitting in?",
   clips=["dark dining room chair",
          {"ai": "A fourth plate of steaming food set by itself on a dark dining table in front of an empty chair, a family of three frozen in the background", "move": "dolly-in", "fallback": "photo: dinner plate dark"},
          {"ai": "A small boy smiling at the dining table in warm lamp light while behind his mother a pale woman in a white saree stands in the dark", "motion": "the pale figure behind the mother slowly leans closer", "fallback": "dark figure dining room"}],
   series=SR(2, "Her Plate Was Set. She Wants My Seat"), share="the friend who always sits in the same seat",
   langs=L.build(L.E3_T, L.E3_H))

day.save()
