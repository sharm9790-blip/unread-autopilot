import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM
import langs as L

day = Day(__file__)
DW = lambda p, e: series("Dog Warning", p, 2, e)

day.ep("goodnight", "rules",
   "[whispering] If Mom says goodnight twice, lock your door. [quietly] Tonight she said it, then kissed my forehead. "
   "Ten minutes later, from the hallway, she said it again. [long pause] Mom was asleep beside me. "
   "[whispering] The doorknob turned slowly. Subscribe... and lock your door.",
   [clip(),
    clip("tonight-0.2", file="clip2.mp4"), clip("ten-0.2", file="clip3.mp4"),
    clip("hallway-0.2", file="clip4.mp4"), clip("again-0.1", file="clip5.mp4"),
    clip("asleep-0.4", file="clip6.mp4"),
    title3("turned-0.1", "SHE WAS", "ASLEEP", "BESIDE ME.", "Would you open it?", ("lock", 0.4))],
   [("sting", "if", 0), ("heartbeat", "tonight", 0), ("sting", "again", 0), ("sting", "asleep", 0)],
   ["hallway"], ["asleep", "doorknob"],
   {"scene": 0, "lines": ["SAID IT TWICE", "LOCK THE DOOR"], "sub": "she was asleep beside me"},
   "Mom Said Goodnight Twice. Mom Was Asleep Beside Me.",
   "Mom said goodnight and kissed my forehead. Ten minutes later she said it again from the hallway. She was asleep beside me.",
   "Would you open the door?",
   clips=[{"ai": "Mom stands in a dark bedroom doorway at night, hand on the door, backlit by warm hallway light, Riya in bed under a blanket, medium shot", "key": True, "move": "dolly-in", "fallback": "dark hallway door"},
          {"ai": "Mom bends to kiss sleepy Riya's forehead in bed, soft amber lamp light, shot from behind Mom", "move": "pan-left", "fallback": "child bedroom night"},
          {"ai": "A wall clock showing ten past ten in a quiet dark bedroom, moonlight through the window, Riya's eyes open in bed", "move": "rise", "fallback": "clock night bedroom"},
          {"ai": "A long dark hallway with a thin line of warm light under a closed bedroom door, a tall shadow standing in the hallway, wide shot", "move": "dolly-out", "fallback": "dark hallway night"},
          {"ai": "Riya sits up in bed hearing a sound, her face in shadow, the closed door in front of her, teal moonlight", "move": "orbit", "fallback": "girl bed dark"},
          {"ai": "Mom asleep in bed beside Riya, calm, eyes closed, while the bedroom doorknob turns slowly in the dark behind them, shot over Mom's shoulder", "key": True, "move": "fall", "fallback": "door handle dark"}],
   look="2d", characters="Mom: Indian woman, 35, long black braid, green cotton saree. Riya: girl, 8, two short braids, yellow nightdress.",
   share="the friend who sleeps with the door unlocked",
   langs=L.build(L.E1_T, L.E1_H))

day.ep("dog-p1", "series",
   "[whispering] Never tell your dog to stop growling at your wife. [quietly] Since she came back, he sleeps against our bedroom door. "
   "Tonight he stopped growling. [long pause] My wife stood over me, smiling. Her hand was full of fur. "
   "[whispering] Part two is on my channel. Subscribe... before your wife comes home.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("tonight-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("hand-0.4", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Dog Warning continues", ("channel", 0.3))],
   [("sting", "never", 0), ("heartbeat", "since", 0), ("sting", "stood", 0), ("sting", "fur", 0)],
   ["stood"], ["hand", "fur"],
   {"scene": 0, "lines": ["DOG STOPPED", "GROWLING"], "sub": "at my wife"},
   "Dog Warning · Pt 1: My Dog Stopped Growling at My Wife",
   "My dog growled at my wife every night since she came back. Tonight he went quiet. She stood over me smiling, her hand full of fur.",
   "Would you check on the dog?",
   clips=["dog dark room night",
          {"ai": "A dog's empty bed beside a bedroom door at night, dark room, a faint silhouette of a woman standing at the foot of a bed, wide shot, cold light",
           "move": "dolly-in", "fallback": "photo: dark bedroom door night"},
          {"ai": "A woman's silhouette standing over a bed in the dark, smiling, one hand hanging down holding clumps of brown fur, shot from the pillow",
           "motion": "the woman's head slowly tilts and her hand tightens", "fallback": "dark figure bedroom"}],
   series=DW(1, "My Dog Stopped Growling at My Wife"), share="the friend whose dog hates a certain person",
   langs=L.build(L.E2_T, L.E2_H))

day.ep("dog-p2", "series",
   "[whispering] Never call the dog when she's home. [quietly] He was under the bed, shaking. "
   "The thing in my wife's shape knelt and called his name. [long pause] He started to crawl out. "
   "[whispering] Then my real wife shouted from the street, \"Why is our light on?\" Subscribe... and never call the dog.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    clip("thing-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("crawl-0.3", file="clip3.mp4"),
    title3("real-0.1", "MY REAL", "WIFE WAS", "OUTSIDE.", "Part 1 is on the channel", ("light", 0.4))],
   [("sting", "never", 0), ("heartbeat", "shaking", 0), ("sting", "crawl", 0), ("sting", "real", 0)],
   ["thing"], ["crawl", "real"],
   {"scene": 0, "lines": ["NEVER CALL", "THE DOG"], "sub": "my real wife was outside"},
   "Dog Warning · Pt 2: My Real Wife Shouted From the Street",
   "Something in my wife's shape called my dog out from under the bed. Then my real wife shouted from the street.",
   "Did you guess the twist?",
   clips=["under bed dark",
          {"ai": "A dark bedroom, a woman kneeling on the floor beside a bed with one hand held out toward the gap beneath it, seen from behind, cold teal light",
           "move": "dolly-in", "fallback": "photo: dark bedroom floor shadow"},
          {"ai": "Under a dark bed, a frightened dog's eyes catching the light as it slowly creeps forward toward an outstretched pale hand, low angle",
           "motion": "the dog slowly creeps forward and the light flickers", "fallback": "dog under bed dark"}],
   series=DW(2, "My Real Wife Shouted From the Street"), share="the friend who talks to their dog at night",
   langs=L.build(L.E3_T, L.E3_H))

day.save()
