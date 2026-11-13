import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM

day = Day(__file__)
GP = lambda p, e: series("Grandma's Plate", p, 2, e)

day.ep("dog-greet", "rules",
   "[whispering] Never let the dog greet Dad. [quietly] Bruno wags at the door at 8:05. Tonight Dad was "
   "home, asleep beside me. [long pause] The key turned. Bruno wagged at a hand I couldn't see. "
   "[whispering] Then something said, \"Good boy.\" In Dad's voice. Subscribe... and never let the dog greet Dad.",
   [clip(grade={"dim": 0.95, "tint": WARM}),
    clip("key-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("something-0.2", file="clip3.mp4"),
    title3("good-0.1", "IT SAID", "GOOD BOY.", "IN DAD'S VOICE.", "Would you open the door?", ("voice", 0.4))],
   [("sting", "never", 0), ("heartbeat", "key", 0), ("sting", "something", 0), ("sting", "good", 0)],
   ["key"], ["something", "good"],
   {"scene": 0, "lines": ["DON'T LET THE", "DOG GREET DAD"], "sub": "dad is asleep beside me"},
   "My Dog Greets Dad at the Door. Dad Is Asleep Beside Me.",
   "Our dog greets Dad at the door every night. Tonight Dad was already home, asleep beside me. Then the key turned.",
   "Would you open the door?",
   clips=["dark front door night",
          {"ai": "A dim apartment entrance at night, a golden retriever sitting wagging its tail facing the closed front door, wide shot, one lamp",
           "move": "dolly-in", "fallback": "photo: dog waiting at door"},
          {"ai": "A dog at a dark front door looking up at empty air as if someone stands there, seen from behind the sofa in shadow",
           "motion": "the dog's tail wags and its head tilts up slowly", "fallback": "dog door night dark"}])

day.ep("door-draw", "second-person",
   "[whispering] Never let your child draw a door. [quietly] My son drew a small brown one on his wall. Last night it "
   "was open. [long pause] Inside, a woman waved at him. [whispering] \"Mama says come in,\" he whispered. I was "
   "standing right behind him. Subscribe... and never let him draw a door.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    clip("open-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("mama-0.2", file="clip3.mp4"),
    title3("behind-0.1", "I WAS", "STANDING", "BEHIND HIM.", "Would you let him go in?", ("draw", 0.4))],
   [("sting", "never", 0), ("heartbeat", "open", 0), ("sting", "mama", 0), ("sting", "standing", 0)],
   ["waved"], ["mama", "standing"],
   {"scene": 0, "lines": ["HE DREW A DOOR", "NOW IT'S OPEN"], "sub": "'Mama says come in'"},
   "My Son Drew a Door on His Wall. Last Night It Was Open.",
   "My son drew a small door on his bedroom wall. Last night it was open, a woman waved from inside, and he called her Mama.",
   "Would you let him go in?",
   clips=["child bedroom dark night",
          {"ai": "A child's bedroom wall at night with a small crayon-drawn brown door, a toy on the floor, nightlight glow, close-up",
           "move": "dolly-in", "fallback": "photo: child crayon drawing wall"},
          {"ai": "A small crayon-drawn door on a dark bedroom wall standing open to blackness, a faint pale hand inside the dark, a small boy seen from behind",
           "motion": "the pale hand inside the doorway slowly waves", "fallback": "dark doorway bedroom"}])

day.ep("plate-p1", "series",
   "[whispering] Never eat the fifth plate. [quietly] Grandma sets five. We are four. I ate it anyway. She went white. "
   "\"Now it knows your taste.\" [long pause] Tonight a plate waited outside my door. [whispering] Still warm. Part two "
   "is on my channel. Subscribe... before the fifth plate is yours.",
   [clip(grade={"dim": 0.9, "tint": WARM}),
    card("grandma-0.2", "G", "Grandma · Dinner", ["Plates on table: 5", "Family members: 4"]),
    clip("tonight-0.2", file="clip3.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Grandma's Plate continues", ("channel", 0.3))],
   [("sting", "never", 0), ("heartbeat", "grandma", 0), ("sting", "knows", 0), ("sting", "warm", 0)],
   ["knows"], ["knows", "warm"],
   {"scene": 0, "lines": ["NEVER EAT THE", "FIFTH PLATE"], "sub": "grandma sets five. we are four"},
   "Grandma's Plate · Pt 1: Grandma Sets a Fifth Plate. We Are Four.",
   "Grandma sets a fifth plate every night, though we are four. I ate it once. Tonight a warm plate waited outside my door.",
   "Would you eat it?",
   clips=["dinner table dark home",
          {"ai": "A dim family dining table set with five steel plates, one at an empty chair with steam rising, warm lamp, close-up",
           "move": "dolly-in", "fallback": "photo: dinner table plates dark"},
          {"ai": "A single steel plate of food on the floor outside a dark bedroom door at night, steam rising, a thin shadow under the door",
           "motion": "the steam curls and the shadow under the door shifts", "fallback": "dark hallway door night"}],
   series=GP(1, "Grandma Sets a Fifth Plate. We Are Four."))

day.ep("plate-p2", "series",
   "[whispering] Don't thank Grandma for dinner. [quietly] Mom wept. \"Grandma died in March.\" [long pause] The fifth "
   "plate kept something fed. I ate its dinner. [whispering] Tonight the table had five plates again... and the fifth "
   "had my name. Subscribe... and don't thank Grandma.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    card("march-0.2", "!", "Mom · Kitchen", ["Grandma died in March", "Who has been cooking?"]),
    title3("fifth-0.1", "THE FIFTH", "PLATE HAD", "MY NAME.", "Part 1 is on the channel", ("name", 0.4))],
   [("sting", "dont", 0), ("heartbeat", "march", 0), ("sting", "fifth", 0), ("sting", "name", 0)],
   ["wept"], ["fifth", "name"],
   {"scene": 0, "lines": ["GRANDMA DIED", "IN MARCH"], "sub": "so who cooks dinner?"},
   "Grandma's Plate · Pt 2: Grandma Died in March. Dinner Is Still Served.",
   "Mom said Grandma died in March. Something has cooked since. Tonight the fifth plate had my name on it.",
   "Did you guess the twist?",
   clips=["kitchen dark night stove",
          {"ai": "A woman crying at a dim kitchen table seen from behind, a stove glowing in the background, an old woman's faint silhouette at the stove far away",
           "move": "dolly-in", "fallback": "photo: dark kitchen night"},
          {"ai": "A dining table with five plates at night, the fifth plate at one chair with a small paper name card, warm dim lamp, close-up",
           "motion": "the steam from the fifth plate curls and the lamp flickers", "fallback": "dinner table dark"}],
   series=GP(2, "Grandma Died in March. Dinner Is Still Served."))

day.save()
