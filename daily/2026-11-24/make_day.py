import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM
import langs as L

day = Day(__file__)
ST = lambda p, e: series("Sleep Talk", p, 2, e)

day.ep("no-face", "second-person",
   "[whispering] My daughter drew Dad with no face. [quietly] Tonight his shoes stood by the door. His keys jingled. "
   "Dad is abroad for work. [long pause] She whispered, \"Mama, he's colouring his face in.\" Then the pencil in her hand moved by itself. "
   "[whispering] Subscribe... before Dad gets his face.",
   [clip(),
    clip("shoes-0.2", file="clip2.mp4"), clip("keys-0.2", file="clip3.mp4"),
    clip("abroad-0.2", file="clip4.mp4"), clip("whispered-0.2", file="clip5.mp4"),
    clip("pencil-0.2", file="clip6.mp4"),
    title3("pencil-0.1", "HE WAS", "COLOURING", "HIS FACE.", "Would you look up?", ("subscribe", 0.4))],
   [("sting", "my", 0), ("heartbeat", "shoes", 0), ("sting", "abroad", 0), ("sting", "pencil", 0)],
   ["pencil"], ["abroad", "pencil"],
   {"scene": 0, "lines": ["DAD HAS", "NO FACE"], "sub": "my daughter drew him last night"},
   "My Daughter Drew Dad With No Face. Dad Is Abroad.",
   "My daughter drew Dad with no face. Tonight his shoes stood by the door and his keys jingled. Dad is abroad.",
   "Would you look at the drawing?",
   clips=[{"ai": "A child's crayon drawing of a tall father figure with a blank white oval for a face, taped to a dark wall, lamp light, close-up", "key": True, "move": "dolly-in", "fallback": "child drawing dark"},
          {"ai": "A pair of men's black shoes standing by a front door in a dark Indian home hallway, a faint light under the door", "move": "pan-left", "fallback": "shoes by door night"},
          {"ai": "A bunch of house keys swinging on a hook beside a dark front door, motion blur, night", "move": "rise", "fallback": "keys door dark"},
          {"ai": "A phone on a bedside table showing a world map and an airplane icon, dim room at night", "move": "dolly-out", "fallback": "phone night room"},
          {"ai": "Riya sitting up in bed holding crayons, Mama's shoulder in the foreground, dark bedroom, one lamp", "move": "orbit", "fallback": "child bedroom night"},
          {"ai": "A tall dark father figure with a smooth blank face standing behind Riya's bed, a crayon drawing beside her lit by lamp light, hand on her shoulder", "key": True, "move": "fall", "fallback": "dark figure bedroom"}],
   look="2d", characters="Mama: Indian woman, 32, long black braid, blue cotton nightsuit. Riya: girl, 6, two short braids, yellow nightdress. Dad: tall Indian man, grey shirt, face always in shadow.",
   share="the friend whose husband works abroad",
   langs=L.build(L.E1_T, L.E1_H))

day.ep("sleeptalk-p1", "series",
   "[whispering] My husband talks in his sleep. [quietly] Tonight he spoke in our baby's voice: \"Mama, don't turn on the light.\" "
   "The monitor showed her crib. Empty. [long pause] His eyes stayed shut. He smiled. \"She's with me.\" "
   "[whispering] Part two is on my channel. Subscribe... before your husband talks in his sleep.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("voice-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("empty-0.3", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Sleep Talk continues", ("channel", 0.3))],
   [("sting", "my", 0), ("heartbeat", "voice", 0), ("sting", "empty", 0), ("sting", "shes", 0)],
   ["empty"], ["empty", "shes"],
   {"scene": 0, "lines": ["HE TALKS IN", "OUR BABY'S VOICE"], "sub": "the crib was empty"},
   "Sleep Talk · Pt 1: My Husband Speaks in Our Baby's Voice",
   "My husband talks in his sleep. Last night he spoke in our baby's voice while the monitor showed an empty crib.",
   "Would you turn on the light?",
   clips=["dark bedroom sleeping man",
          {"ai": "A man asleep in a dark bedroom, mouth slightly open, his wife awake beside him in the foreground, blue night light, shot from behind her shoulder", "move": "dolly-in", "fallback": "photo: dark bedroom bed"},
          {"ai": "A baby monitor screen glowing green on a nightstand showing an empty crib, dark room, close-up", "motion": "the monitor screen flickers and a small shadow crosses the crib", "fallback": "baby monitor dark"}],
   series=ST(1, "My Husband Speaks in Our Baby's Voice"), share="the friend whose husband talks in his sleep",
   langs=L.build(L.E2_T, L.E2_H))

day.ep("sleeptalk-p2", "series",
   "[whispering] Never answer a man who talks in his sleep. [quietly] I asked, \"Where is my baby?\" His mouth said, \"Under the bed.\" "
   "She was there, smiling, holding someone's pale hand. [long pause] My husband woke up screaming: "
   "\"Why is my voice coming from the bed?\" [whispering] Subscribe... and never answer a sleeping man.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    clip("under-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("woke-0.3", file="clip3.mp4"),
    title3("subscribe-0.1", "WHOSE VOICE", "WAS UNDER", "THE BED?", "Part 1 is on the channel", ("sleeping", 0.4))],
   [("sting", "never", 0), ("heartbeat", "under", 0), ("sting", "pale", 0), ("sting", "woke", 0)],
   ["under"], ["pale", "woke"],
   {"scene": 0, "lines": ["NEVER ANSWER", "A SLEEPING MAN"], "sub": "his mouth said: under the bed"},
   "Sleep Talk · Pt 2: My Baby Held a Hand Under the Bed",
   "I asked where my baby was. My sleeping husband said: under the bed. She was holding someone's pale hand.",
   "Whose voice was it?",
   clips=["dark under bed",
          {"ai": "A dark gap under a bed with a baby's small hand and a long pale adult hand clasped together in the shadow, flashlight glow from one side", "move": "dolly-in", "fallback": "photo: under bed dark"},
          {"ai": "A man sitting up in bed in a dark room, mouth wide in a scream, his wife kneeling on the floor holding a baby, cold blue light", "motion": "a pale hand slowly withdraws into the dark under the bed", "fallback": "dark bedroom scared"}],
   series=ST(2, "My Baby Held a Hand Under the Bed"), share="the friend who checks under the bed",
   langs=L.build(L.E3_T, L.E3_H))

day.save()
