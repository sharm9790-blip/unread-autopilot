import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM

day = Day(__file__)
GR = lambda p, e: series("Guest Room", p, 2, e)

day.ep("mom-text", "text-story",
   "[whispering] Mom texted me: come home now. [quietly] She was driving the car. Right beside me, humming. I showed "
   "her the phone. The humming stopped. [long pause] Another text arrived: Don't get out with her. [whispering] "
   "Through the windshield, Mom stood in our doorway... waving. Subscribe... before Mom says come home.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    lock("another-0.2", "11:48", "Mom", "Don't get out with her.", "another"),
    title3("doorway-0.1", "MOM WAS", "WAVING FROM", "THE DOOR.", "Would you get out?", ("waving", 0.4))],
   [("buzz", "texted", 0), ("heartbeat", "humming", 0), ("sting", "another", 0), ("sting", "doorway", 0)],
   ["stopped"], ["doorway", "waving"],
   {"scene": 0, "lines": ["MOM TEXTED:", "COME HOME NOW"], "sub": "she was driving beside me"},
   "Mom Texted Me to Come Home. She Was Driving Me Home.",
   "Mom texted: come home now. She was in the driver's seat next to me. Then a second text said not to get out with her.",
   "Would you get out of the car?",
   clips=["car night road passenger", "photo: house doorway night"])

day.ep("cat-tooth", "second-person",
   "[whispering] My cat left a baby tooth on my pillow. [quietly] I have no kids. Tonight I stayed awake. "
   "She dropped another and stared at the wall. [long pause] Behind it, a small voice giggled, \"Thank you, kitty.\" "
   "[whispering] Then, \"One more... for his smile.\" Subscribe... and check your pillow.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    clip("behind-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("smile-0.1", "ONE MORE", "TOOTH FOR", "HIS SMILE.", "Would you check your pillow?", ("smile", 0.4))],
   [("sting", "tooth", 0), ("heartbeat", "stayed", 0), ("sting", "giggled", 0), ("sting", "smile", 0)],
   ["wall"], ["giggled", "smile"],
   {"scene": 0, "lines": ["BABY TOOTH", "ON MY PILLOW"], "sub": "I have no kids"},
   "My Cat Left a Baby Tooth on My Pillow. I Have No Kids.",
   "Every night my cat leaves a baby tooth on my pillow. Last night I heard who she's been giving them to.",
   "Would you check your pillow?",
   clips=["cat dark bedroom night", "photo: dark wall bedroom night"])

day.ep("guest-p1", "series",
   "[whispering] Never sleep in the guest room. [quietly] Mom makes its bed daily. Nobody visits. I slept there once. "
   "At 2 AM, a cold hand tucked me in. [long pause] \"Good boy.\" A framed boy "
   "had my face. [whispering] Part two is on my channel. Subscribe... before the guest room.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    card("framed-0.2", "!", "Guest Room · Nightstand", ["A BOY WITH MY FACE", "Dated 1994"]),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Guest Room continues", ("channel", 0.3))],
   [("sting", "never", 0), ("heartbeat", "cold", 0), ("sting", "good", 0), ("sting", "face", 0)],
   ["cold"], ["good", "face"],
   {"scene": 0, "lines": ["NEVER SLEEP IN", "THE GUEST ROOM"], "sub": "mom makes the bed daily"},
   "Guest Room · Pt 1: Mom Makes the Bed Daily. Nobody Visits.",
   "Mom makes the guest room bed every morning. Nobody visits. I slept there once, and something tucked me in.",
   "Would you sleep there?",
   clips=["bedroom door dark night", "photo: old bedroom bed dark"], series=GR(1, "Mom Makes the Bed Daily. Nobody Visits."))

day.ep("guest-p2", "series",
   "[whispering] Don't tell Mom you saw the photo. [quietly] She sobbed. \"That's your brother. "
   "He died in 1994.\" She makes his bed daily. [long pause] \"You slept in it. Now he's home.\" "
   "[whispering] Tonight, in my flat, a cold hand tucked me in. Subscribe... and don't tell Mom.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    lock("tonight-0.2", "2:07", "Mom", "Did he follow you? Don't answer him.", "tonight"),
    title3("tucked-0.1", "HE FOLLOWED", "ME HOME.", "GOOD BOY.", "Part 1 is on the channel", ("tucked", 0.4))],
   [("sting", "dont", 0), ("sting", "brother", 0), ("heartbeat", "home", 0), ("sting", "tucked", 0)],
   ["brother"], ["died", "tucked"],
   {"scene": 0, "lines": ["HE FOLLOWED ME", "HOME TONIGHT"], "sub": "guest room, part 2"},
   "Guest Room · Pt 2: He Followed Me Home. Mom Warned Me.",
   "Mom told me who the boy in the photo was. Then I felt the same cold hand tuck me in, in my own flat.",
   "Did you guess the twist?",
   clips=["dark bedroom hallway night"], series=GR(2, "He Followed Me Home. Mom Warned Me."))

day.save()
