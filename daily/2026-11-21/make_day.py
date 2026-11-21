import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM
import langs as L

day = Day(__file__)
LU = lambda p, e: series("Lullaby", p, 2, e)

day.ep("upstairs", "rules",
   "[whispering] My husband is calling me from upstairs. [quietly] He's standing beside me in the kitchen, phone in his pocket. "
   "The caller whispers: \"Keep him there. I'm the real one.\" [long pause] Upstairs, footsteps reached the stairs. "
   "My husband smiled. \"Don't answer, jaan.\" [whispering] Subscribe... before your husband calls from upstairs.",
   [clip(),
    clip("standing-0.2", file="clip2.mp4"), clip("caller-0.2", file="clip3.mp4"),
    clip("real-0.2", file="clip4.mp4"), clip("footsteps-0.2", file="clip5.mp4"),
    clip("smiled-0.1", file="clip6.mp4"),
    title3("dont-0.1", "THAT WAS", "NOT MY", "HUSBAND.", "Would you answer?", ("subscribe", 0.4))],
   [("sting", "my", 0), ("heartbeat", "standing", 0), ("sting", "real", 0), ("sting", "smiled", 0)],
   ["footsteps"], ["caller", "smiled"],
   {"scene": 0, "lines": ["HUSBAND CALLS", "FROM UPSTAIRS"], "sub": "he's standing next to me"},
   "My Husband Is Calling From Upstairs. He's Next to Me.",
   "My husband is calling me from upstairs. He is standing next to me in the kitchen. The caller says: keep him there.",
   "Would you answer?",
   clips=[{"ai": "A dark Indian kitchen at night, a woman seen from behind with her phone glowing in her hand, a husband in a grey shirt standing close beside her facing the ceiling, a staircase in the background", "key": True, "move": "dolly-in", "fallback": "dark kitchen night"},
          {"ai": "The husband standing very still beside the wife in the kitchen, phone in his pocket, face in shadow, cold light from the fridge", "move": "pan-left", "fallback": "man standing kitchen dark"},
          {"ai": "Close-up of a phone screen glowing in the dark, caller named Husband, a hand holding it", "move": "rise", "fallback": "phone ringing dark"},
          {"ai": "A dark staircase seen from the kitchen, the upstairs landing black, a faint light under a bedroom door", "move": "dolly-out", "fallback": "dark staircase night"},
          {"ai": "Bare feet in shadow at the top of a dark staircase, mid-step toward the stairs, wide shot", "move": "orbit", "fallback": "dark stairs feet"},
          {"ai": "The husband in the kitchen turned toward the wife, smiling too wide, face half in shadow, eyes reflecting light, her phone glowing in the foreground", "key": True, "move": "fall", "fallback": "dark figure smiling"}],
   look="2d", characters="Meera: Indian woman, 32, long black braid, orange cotton kurta. Husband: Indian man, 36, grey shirt, short beard, face always in shadow.",
   share="the friend whose husband works late and calls from the other room",
   langs=L.build(L.E1_T, L.E1_H))

day.ep("lullaby-p1", "series",
   "[whispering] Someone sings to my baby. Mom has no voice. [quietly] She lost it in surgery. A lullaby drifted from the nursery. "
   "Mom stood silent beside me, crying. [long pause] It was her old voice... singing from inside the crib. "
   "[whispering] Part two is on my channel. Subscribe... before someone sings to your baby.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("lullaby-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("old-0.3", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Lullaby continues", ("channel", 0.3))],
   [("sting", "someone", 0), ("heartbeat", "lullaby", 0), ("sting", "old", 0), ("sting", "singing", 0)],
   ["silent"], ["old", "singing"],
   {"scene": 0, "lines": ["SOMEONE SINGS", "MOM HAS NO VOICE"], "sub": "to my baby, at night"},
   "Lullaby · Pt 1: Someone Sings to My Baby. Mom Has No Voice.",
   "Someone sings to my baby every night. Mom lost her voice in surgery. The singing was her old voice, from inside the crib.",
   "Would you open the nursery door?",
   clips=["dark nursery night",
          {"ai": "A dim nursery at night with a crib, a mother in a cotton nightdress standing silent beside her daughter, both seen from behind, tears on her cheek in the lamp glow",
           "move": "dolly-in", "fallback": "photo: dark nursery crib"},
          {"ai": "A wooden crib in a dark nursery with a pale glow inside it, mouth-shaped shadow on the mattress, two figures far away at the door",
           "motion": "the glow inside the crib slowly pulses as if something is singing", "fallback": "crib dark room"}],
   series=LU(1, "Someone Sings to My Baby. Mom Has No Voice."), share="the friend who has a newborn",
   langs=L.build(L.E2_T, L.E2_H))

day.ep("lullaby-p2", "series",
   "[whispering] Never hum back to the lullaby. [quietly] I hummed. The singing stopped. By morning, Mom was speaking, her old voice perfect. "
   "[long pause] My baby lay beside her, lips moving with every word. Mom smiled. \"Thank you for lending me yours.\" "
   "[whispering] Subscribe... and never hum back to the lullaby.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    clip("morning-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("lips-0.3", file="clip3.mp4"),
    title3("subscribe-0.1", "SHE TOOK", "MY BABY'S", "VOICE.", "Part 1 is on the channel", ("lullaby", 0.4))],
   [("sting", "never", 0), ("heartbeat", "hummed", 0), ("sting", "lips", 0), ("sting", "thank", 0)],
   ["stopped"], ["lips", "thank"],
   {"scene": 0, "lines": ["NEVER HUM BACK", "TO THE LULLABY"], "sub": "Mom's voice came back"},
   "Lullaby · Pt 2: Mom's Voice Came Back. My Baby's Lips Moved.",
   "I hummed back to the lullaby. By morning Mom's voice was back, and my baby's lips moved with every word she said.",
   "Did you guess the twist?",
   clips=["baby nursery dark",
          {"ai": "A grandmother sitting on a bed in soft morning light speaking, a baby lying on the quilt beside her, mother in the doorway from behind, muted colours",
           "move": "dolly-in", "fallback": "photo: old woman bed morning"},
          {"ai": "A baby lying on a quilt in a dim room, tiny mouth moving, a grandmother smiling above her with face in shadow",
           "motion": "the grandmother's head slowly turns toward camera, smiling", "fallback": "dark figure bedroom"}],
   series=LU(2, "Mom's Voice Came Back. My Baby's Lips Moved."), share="the friend who hums to their baby",
   langs=L.build(L.E3_T, L.E3_H))

day.save()
