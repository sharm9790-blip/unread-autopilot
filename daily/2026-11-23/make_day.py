import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM
import langs as L

day = Day(__file__)
MR = lambda p, e: series("Mirror Rule", p, 2, e)

day.ep("mom-tea", "rules",
   "[whispering] Mom is still in surgery. [quietly] The kitchen light just turned on. Tea boiling, her bangles jingling, her lullaby humming. "
   "[long pause] The hospital called: \"Surgery's over. We're so sorry.\" Mom set a cup beside me. \"Drink, beta.\" "
   "[whispering] Subscribe... before Mom's surgery ends.",
   [clip(),
    clip("tea-0.2", file="clip2.mp4"), clip("bangles-0.2", file="clip3.mp4"),
    clip("hospital-0.2", file="clip4.mp4"), clip("cup-0.2", file="clip5.mp4"),
    clip("drink-0.1", file="clip6.mp4"),
    title3("drink-0.1", "MOM DIED", "AT 2 AM.", "SHE SERVED TEA.", "Would you drink it?", ("subscribe", 0.4))],
   [("sting", "mom", 0), ("heartbeat", "tea", 0), ("sting", "hospital", 0), ("sting", "drink", 0)],
   ["drink"], ["hospital", "drink"],
   {"scene": 0, "lines": ["MOM IS STILL", "IN SURGERY"], "sub": "the kitchen light just turned on"},
   "Mom's Surgery Isn't Over. She's Making Tea in Our Kitchen.",
   "Mom is still in surgery, but the kitchen light just turned on. Tea boiling, her bangles jingling. Then the hospital called.",
   "Would you drink the tea?",
   clips=[{"ai": "A dark Indian home kitchen at night, a single light on over the stove, a steaming tea pot, a woman's silhouette in a faded saree standing with her back to camera", "key": True, "move": "dolly-in", "fallback": "dark kitchen night"},
          {"ai": "A steel pot of milk tea boiling on a gas stove, steam rising in warm light, dark kitchen", "move": "rise", "fallback": "tea boiling kitchen"},
          {"ai": "A woman's wrist with glass bangles and a hand stirring a pot, only the arm lit, dark kitchen", "move": "pan-left", "fallback": "bangles hand dark"},
          {"ai": "A phone glowing on a dining table at night showing a hospital name, a son's hand beside it, dark room", "move": "dolly-out", "fallback": "phone ringing dark"},
          {"ai": "A steel cup of tea placed on a bedside table beside a young man's hand, warm steam in the dark", "move": "orbit", "fallback": "tea cup dark night"},
          {"ai": "Mom standing close beside a seated young man in a dark kitchen, hospital band on her wrist, smiling too wide, eyes reflecting light, holding out a cup", "key": True, "move": "fall", "fallback": "dark figure kitchen"}],
   look="2d", characters="Mom: Indian woman, 52, grey-streaked bun, faded green saree, glass bangles, hospital wristband. Aman: Indian man, 24, grey t-shirt, short hair, face in shadow.",
   share="the friend whose mom is always in the kitchen at night",
   langs=L.build(L.E1_T, L.E1_H))

day.ep("mirror-p1", "series",
   "[whispering] Grandma's rule: never blink back at the mirror. [quietly] Tonight, my reflection blinked first. "
   "Behind it, my daughter's reflection smiled and waved. [long pause] She was asleep in my arms, eyes shut. "
   "Her reflection stepped closer. [whispering] Part two is on my channel. Subscribe... before your mirror blinks first.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("blinked-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("asleep-0.3", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "The mirror continues", ("channel", 0.3))],
   [("sting", "grandmas", 0), ("heartbeat", "blinked", 0), ("sting", "waved", 0), ("sting", "closer", 0)],
   ["asleep"], ["waved", "closer"],
   {"scene": 0, "lines": ["NEVER BLINK", "BACK AT IT"], "sub": "my daughter's reflection waved"},
   "Mirror Rule · Pt 1: My Daughter's Reflection Waved. She Was Asleep.",
   "Grandma's rule: never blink back at the mirror. Tonight my reflection blinked first, and my sleeping daughter's reflection waved.",
   "Would you blink back?",
   clips=["dark mirror bedroom night",
          {"ai": "A dark bedroom mirror showing a woman's reflection with eyes closed while the real woman stands with eyes open, a faint amber lamp, close framing from behind",
           "move": "dolly-in", "fallback": "photo: dark bedroom mirror"},
          {"ai": "A mother seen from behind holding a sleeping little girl in front of a tall dim mirror, in the mirror the girl's reflection is awake and smiling, hand raised in a wave",
           "motion": "the reflection's raised hand slowly waves as the figure steps forward", "fallback": "dark mirror figure"}],
   series=MR(1, "My Daughter's Reflection Waved. She Was Asleep."), share="the friend who keeps a mirror in the bedroom",
   langs=L.build(L.E2_T, L.E2_H))

day.ep("mirror-p2", "series",
   "[whispering] Never wave back at the mirror. [quietly] I waved. My reflection stepped out, calm, smiling, my face. "
   "My daughter's eyes opened in my arms. [long pause] \"Mama, who is holding me?\" "
   "The other me touched her hair. \"I'm taking care of her now.\" [whispering] Subscribe... and never wave at the mirror.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    clip("stepped-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("mama-0.3", file="clip3.mp4"),
    title3("subscribe-0.1", "WHICH ONE", "IS REALLY", "HER MAMA?", "Part 1 is on the channel", ("mirror", 0.4))],
   [("sting", "never", 0), ("heartbeat", "stepped", 0), ("sting", "mama", 0), ("sting", "taking", 0)],
   ["stepped"], ["mama", "taking"],
   {"scene": 0, "lines": ["NEVER WAVE", "AT THE MIRROR"], "sub": "she stepped out smiling"},
   "Mirror Rule · Pt 2: My Reflection Said: I'm Taking Care of Her.",
   "I waved back at the mirror. My reflection stepped out wearing my face. My daughter woke up and asked who was holding her.",
   "Which one is her mama?",
   clips=["dark mirror hallway",
          {"ai": "A woman's reflection stepping out of a tall dim bedroom mirror, calm smile, identical to the real woman holding a child, cold blue light, shot from behind",
           "move": "dolly-in", "fallback": "photo: mirror dark room"},
          {"ai": "Two identical women in a dark bedroom, one holding a little girl with wide open eyes, the other touching the girl's hair, faces half in shadow",
           "motion": "the second woman's hand slowly strokes the child's hair and her head tilts toward camera", "fallback": "dark figure bedroom"}],
   series=MR(2, "My Reflection Said: I'm Taking Care of Her."), share="the friend who never covers the mirror at night",
   langs=L.build(L.E3_T, L.E3_H))

day.save()
