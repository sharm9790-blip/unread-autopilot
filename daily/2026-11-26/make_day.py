import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM
import langs as L

day = Day(__file__)
SR = lambda p, e: series("Voice Note", p, 2, e)

day.ep("didi-knock", "second-person",
   "[whispering] Didi is knocking on the front door. [quietly] We buried her this morning. Mom whispered, \"Don't open it. Count the knocks.\" "
   "Three. Then Didi's voice came from behind me, inside the house: [long pause] \"Who are you talking to?\" "
   "[whispering] Subscribe... before Didi knocks.",
   [clip(),
    clip("buried-0.2", file="clip2.mp4"), clip("count-0.2", file="clip3.mp4"),
    clip("three-0.2", file="clip4.mp4"), clip("behind-0.2", file="clip5.mp4"),
    clip("who-0.3", file="clip6.mp4"),
    title3("who-0.1", "DIDI WAS", "INSIDE", "THE HOUSE.", "Would you open the door?", ("subscribe", 0.4))],
   [("knock", "knocking", 0), ("heartbeat", "buried", 0), ("sting", "three", 0), ("sting", "who", 0)],
   ["knocking"], ["three", "who"],
   {"scene": 0, "lines": ["DIDI IS KNOCKING", "WE BURIED HER"], "sub": "count the knocks"},
   "My Sister Is Knocking to Come In. Her Funeral Was Today.",
   "Didi is knocking on the front door. We buried her this morning. Then her voice came from inside the house.",
   "Would you open the door?",
   clips=[{"ai": "A closed wooden front door of an Indian house at night, a thin line of dark light under it, a small girl's silhouette standing far back in the hallway", "key": True, "move": "dolly-in", "fallback": "dark door night"},
          {"ai": "A fresh grave mound with marigold flowers in morning mist, wide shot, muted colors", "move": "pan-left", "fallback": "graveyard morning fog"},
          {"ai": "Mom gripping the wrist of Riya in a dim hallway, finger to her lips, both facing the door", "move": "rise", "fallback": "dark hallway family"},
          {"ai": "The front door shaking slightly with a pale hand shape pressed against the frosted glass beside it, close-up", "move": "dolly-out", "fallback": "door glass night"},
          {"ai": "Riya looking over her shoulder at the dark living room behind her, Mom frozen beside her, lamp light", "move": "orbit", "fallback": "dark living room night"},
          {"ai": "A pale teenage girl in a white salwar standing in the dark hallway behind Riya and Mom, her head tilted, eyes reflecting light", "key": True, "move": "fall", "fallback": "dark figure hallway"}],
   look="2d", characters="Riya: Indian girl, 10, two short braids, yellow nightdress. Mom: Indian woman, 38, long black braid, green cotton saree, face in shadow. Didi: Indian girl, 17, long loose hair, white salwar, face in shadow.",
   share="the friend who always locks the door twice",
   langs=L.build(0))

day.ep("voice-note-p1", "series",
   "[whispering] Mom sent me a voice note. [quietly] Her phone is in my hand. She's asleep beside me. The note says: "
   "\"Beta, stay in bed. Whatever calls you from downstairs isn't me.\" [long pause] Downstairs, Mom called: \"Beta, come eat.\" "
   "[whispering] Part two is on my channel. Subscribe... before Mom's voice note.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("asleep-0.2", file="clip2.mp4"),
    lock("stay-0.3", "3:07", "Mom", "Beta, stay in bed.", "stay"),
    clip("downstairs#2-0.2", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Voice Note continues", ("channel", 0.3))],
   [("sting", "mom", 0), ("heartbeat", "asleep", 0), ("buzz", "stay", 0), ("sting", "eat", 0)],
   ["eat"], ["stay", "eat"],
   {"scene": 0, "lines": ["MOM SENT A NOTE", "SHE'S ASLEEP"], "sub": "her phone is in my hand"},
   "Voice Note · Pt 1: Mom Messaged Me. Her Phone Is in My Hand",
   "Mom sent me a voice note. Her phone is in my hand and she is asleep beside me. The note says stay in bed.",
   "Would you press play?",
   clips=["dark bedroom phone night",
          {"ai": "A sleeping mother's back under a blanket in a dark bedroom, a phone glowing in her son's hand at the edge of frame, cold blue screen light", "move": "dolly-in", "fallback": "photo: phone dark bedroom"},
          {"ai": "A dark staircase leading down into a pitch-black living room, a faint yellow kitchen light at the bottom, shot from the top step", "motion": "the kitchen light flickers and a thin shadow crosses it", "fallback": "dark staircase night"}],
   series=SR(1, "Mom Messaged Me. Her Phone Is in My Hand"), share="the friend who gets voice notes at 3 AM",
   langs=L.build(1))

day.ep("voice-note-p2", "series",
   "[whispering] Never answer the voice from downstairs. [quietly] I played the note to the end. Mom's real voice whispered: "
   "\"The one sleeping beside you came up first.\" [long pause] I looked. The blanket was empty. A warm hand covered my mouth. "
   "[whispering] Subscribe... and never answer the voice from downstairs.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    clip("played-0.2", file="clip2.mp4"),
    clip("looked-0.2", file="clip3.mp4"),
    title3("warm-0.1", "THE BLANKET", "WAS", "EMPTY.", "Part 1 is on the channel", ("subscribe", 0.4))],
   [("sting", "never", 0), ("heartbeat", "played", 0), ("sting", "empty", 0), ("sting", "warm", 0)],
   ["empty"], ["empty", "warm"],
   {"scene": 0, "lines": ["NEVER ANSWER", "FROM DOWNSTAIRS"], "sub": "she came up first"},
   "Voice Note · Pt 2: Mom's Real Voice Said: Don't Look Beside You",
   "I played the voice note to the end. Mom's real voice said the one sleeping beside me came up first.",
   "Would you look beside you?",
   clips=["dark bedroom night bed",
          {"ai": "A phone lit up on a dark bed with a waveform on screen, a pale hand resting on the pillow beside it, cold light", "move": "dolly-in", "fallback": "photo: phone dark bed"},
          {"ai": "A bed with the blanket thrown back showing only a dent in the mattress, a tall dark figure standing at the headboard, dim moonlight", "motion": "the dark figure slowly leans down toward camera", "fallback": "dark figure bedroom"}],
   series=SR(2, "Mom's Real Voice Said: Don't Look Beside You"), share="the friend who sleeps next to their phone",
   langs=L.build(2))

day.save()
