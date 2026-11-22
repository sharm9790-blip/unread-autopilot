import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM
import langs as L

day = Day(__file__)
TR = lambda p, e: series("Terrace", p, 2, e)

day.ep("bhaiya-bus", "rules",
   "[whispering] Bhaiya's bus crashed an hour ago. [quietly] Now he's ringing our doorbell. Ma ran to open it, crying. "
   "Through the peephole, he smiled, unscratched. [long pause] The police called: \"Bhaiya is still on the bus.\" "
   "Ma had already unlocked the door. [whispering] Subscribe... before Bhaiya's bus stops at your door.",
   [clip(),
    clip("ringing-0.2", file="clip2.mp4"), clip("peephole-0.2", file="clip3.mp4"),
    clip("police-0.2", file="clip4.mp4"), clip("ma-0.1", file="clip5.mp4"),
    clip("already-0.1", file="clip6.mp4"),
    title3("unlocked-0.1", "THAT WASN'T", "BHAIYA AT", "THE DOOR.", "Would you open it?", ("subscribe", 0.4))],
   [("sting", "bhaiyas", 0), ("heartbeat", "ringing", 0), ("sting", "police", 0), ("sting", "unlocked", 0)],
   ["unlocked"], ["police", "unlocked"],
   {"scene": 0, "lines": ["BHAIYA'S BUS", "CRASHED. RINGS"], "sub": "Ma is opening the door"},
   "Bhaiya's Bus Crashed an Hour Ago. He's Ringing the Bell.",
   "Bhaiya's bus crashed an hour ago. Now he's ringing our doorbell, not a scratch on him. The police say he's still on the bus.",
   "Would you open the door?",
   clips=[{"ai": "A dark Indian apartment corridor at night, a closed front door with a doorbell glowing, a mother in a saree seen from behind reaching for the latch, her son's silhouette visible through the door's peephole light", "key": True, "move": "dolly-in", "fallback": "dark apartment door night"},
          {"ai": "Close-up of a doorbell button being pressed by a pale hand in the dark, wet sleeve, warm light from inside", "move": "rise", "fallback": "doorbell dark night"},
          {"ai": "A fisheye view through a door peephole of a young man smiling in a stairwell, clean clothes, no marks, face half in shadow", "move": "pan-left", "fallback": "peephole door dark"},
          {"ai": "A phone glowing on a kitchen table at night, a police officer's name on the screen, a daughter's hand beside it", "move": "dolly-out", "fallback": "phone ringing dark"},
          {"ai": "The mother's hand turning the lock of the front door, steel chain hanging loose, hallway dark", "move": "orbit", "fallback": "door lock dark"},
          {"ai": "The front door open an inch, a smiling young man standing in the dark stairwell with wet hair, eyes reflecting light, the mother silhouetted in the doorway", "key": True, "move": "fall", "fallback": "dark figure doorway"}],
   look="2d", characters="Ma: Indian woman, 55, grey-streaked bun, faded blue saree. Bhaiya: Indian man, 26, white shirt, short hair, face always in shadow. Riya: girl, 17, ponytail, green kurta.",
   share="the friend whose brother travels by night bus",
   langs=L.build(L.E1_T, L.E1_H))

day.ep("terrace-p1", "series",
   "[whispering] Dadi locked the terrace before she died. [quietly] Every dawn, wet clothes hang up there. "
   "Today I found my daughter's frock, dripping. [long pause] She was asleep in bed, her hair wet. The key hung around her neck. "
   "[whispering] Part two is on my channel. Subscribe... before the terrace door opens.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("frock-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("asleep-0.3", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "The terrace continues", ("channel", 0.3))],
   [("sting", "dadi", 0), ("heartbeat", "wet", 0), ("sting", "frock", 0), ("sting", "key", 0)],
   ["asleep"], ["frock", "key"],
   {"scene": 0, "lines": ["DADI LOCKED", "THE TERRACE"], "sub": "wet clothes hang there at dawn"},
   "Terrace · Pt 1: Dadi Locked It. Wet Clothes Hang There.",
   "Dadi locked the terrace before she died. Every dawn, wet clothes hang up there. Today it was my daughter's frock, and her hair was wet in bed.",
   "Would you unlock the terrace?",
   clips=["dark rooftop dawn clothesline",
          {"ai": "A small child's school frock dripping on a rooftop clothesline at grey dawn, an old locked terrace door behind it, water pooling on concrete",
           "move": "dolly-in", "fallback": "photo: clothesline dawn rooftop"},
          {"ai": "A little girl asleep in bed with wet hair soaking the pillow, a brass key on a thread around her neck, dim bedside lamp, mother's silhouette in the doorway",
           "motion": "the key on her neck slowly sways as if something breathes", "fallback": "child sleeping dark room"}],
   series=TR(1, "Dadi Locked It. Wet Clothes Hang There."), share="the friend whose grandmother's room is still locked",
   langs=L.build(L.E2_T, L.E2_H))

day.ep("terrace-p2", "series",
   "[whispering] Never hang clothes on Dadi's terrace. [quietly] I took the key and went up at dawn. "
   "A woman was hanging my husband's shirt, soaking. She turned. Dadi, smiling. [long pause] \"Whoever it dries on, beta, I keep.\" "
   "Downstairs, my husband was coughing water. [whispering] Subscribe... and never hang clothes on the terrace.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    clip("woman-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("coughing-0.3", file="clip3.mp4"),
    title3("subscribe-0.1", "SHE WASHES", "THE ONES", "SHE TAKES.", "Part 1 is on the channel", ("terrace", 0.4))],
   [("sting", "never", 0), ("heartbeat", "soaking", 0), ("sting", "dadi", 0), ("sting", "coughing", 0)],
   ["turned"], ["dadi", "coughing"],
   {"scene": 0, "lines": ["NEVER HANG", "CLOTHES UP THERE"], "sub": "she keeps who they dry on"},
   "Terrace · Pt 2: Dadi Hung My Husband's Shirt. It Was Dripping.",
   "I went up to Dadi's terrace at dawn. She was hanging my husband's shirt, soaking wet. Downstairs, he was coughing water.",
   "Did you guess the twist?",
   clips=["old woman rooftop dawn",
          {"ai": "An old woman in a white saree seen from behind on a grey dawn rooftop hanging a soaking man's shirt on a line, a daughter-in-law at the stairwell door",
           "move": "dolly-in", "fallback": "photo: rooftop clothesline woman"},
          {"ai": "A man doubled over in a dim bedroom, water dripping from his mouth and hair onto the floor, wife's silhouette in the doorway, cold light",
           "motion": "water slowly drips from his hair as his head lifts toward camera", "fallback": "dark figure bedroom"}],
   series=TR(2, "Dadi Hung My Husband's Shirt. It Was Dripping."), share="the friend who dries clothes on the terrace",
   langs=L.build(L.E3_T, L.E3_H))

day.save()
