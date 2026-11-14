import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM

day = Day(__file__)
VN = lambda p, e: series("Voice Note", p, 2, e)

day.ep("parrot", "rules",
   "[whispering] Never ignore the parrot after midnight. [quietly] Ours only copies Mom's voice. Last night it whispered, "
   "\"That isn't me.\" Mom was asleep right beside me. [long pause] Downstairs, someone called \"Coming!\" in her voice. "
   "[whispering] The parrot screamed. Subscribe... and never ignore the parrot.",
   [clip(grade={"dim": 0.95, "tint": WARM}),
    clip("downstairs-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("screamed-0.5", file="clip3.mp4"),
    title3("screamed-0.1", "IT WASN'T", "MOM", "DOWNSTAIRS.", "Would you go down?", ("parrot", 0.4))],
   [("sting", "never", 0), ("heartbeat", "downstairs", 0), ("sting", "coming", 0), ("sting", "screamed", 0)],
   ["screamed"], ["coming", "screamed"],
   {"scene": 0, "lines": ["NEVER IGNORE", "THE PARROT"], "sub": "'that isn't me'"},
   "The Parrot Whispered: That Isn't Me. Mom Was Asleep Beside Me.",
   "Our parrot only copies Mom. Last night it whispered, 'That isn't me,' while Mom slept beside me. Then someone downstairs answered in her voice.",
   "Would you go downstairs?",
   clips=["dark living room night",
          {"ai": "A grey parrot in a cage in a dim living room at night, staring toward a dark staircase, lit by a faint streetlight, wide shot",
           "move": "dolly-in", "fallback": "photo: parrot cage dark room"},
          {"ai": "A dark staircase at night seen from the top, a pale shape faintly visible at the bottom near the front door, a parrot cage in the foreground",
           "motion": "the pale shape at the bottom of the stairs slowly turns its head upward", "fallback": "dark staircase night"}])

day.ep("tuck-in", "second-person",
   "[whispering] Someone tucked me in last night. [quietly] Blanket to my chin. Warm hands. My husband is abroad. "
   "[long pause] I texted him. He replied: \"Did it fix the blanket? It does that for me too.\" "
   "[whispering] Then the blanket pulled tighter. Subscribe... because someone tucked me in.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    clip("texted-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    card("did-0.2", "H", "Husband · Abroad", ["Did it fix the blanket?", "It does that for me too."]),
    clip("tighter-0.3", file="clip3.mp4"),
    title3("tighter-0.1", "IT PULLED", "THE BLANKET", "TIGHTER.", "Would you look under it?", ("tucked", 0.4))],
   [("sting", "someone", 0), ("heartbeat", "texted", 0), ("sting", "did", 0), ("sting", "tighter", 0)],
   ["tighter"], ["tighter"],
   {"scene": 0, "lines": ["SOMEONE TUCKED", "ME IN"], "sub": "my husband is abroad"},
   "Someone Tucked Me In at 2 AM. My Husband Is Abroad.",
   "Someone tucked me in last night, warm hands, blanket to my chin. My husband is abroad. His reply made it worse.",
   "Would you look under the blanket?",
   clips=["dark bedroom bed night",
          {"ai": "A made bed at night with the blanket pulled neatly to the pillow, a phone glowing on the nightstand, a dark bedroom door behind, close-up",
           "move": "dolly-in", "fallback": "photo: bed blanket dark bedroom"},
          {"ai": "A dark bedroom bed seen from the foot, the blanket slightly raised by an unseen shape beside the sleeping woman, dim moonlight",
           "motion": "the blanket slowly pulls tight and a faint pale hand shows at its edge", "fallback": "bedroom dark blanket"}])

day.ep("vn-p1", "series",
   "[whispering] Don't play Mom's voice note. She can't speak. [quietly] At 3 AM, a voice note: her breathing. Then her "
   "voice: \"Don't come home.\" [long pause] I was already outside her door. Inside, she was whispering to someone. "
   "[whispering] Part two is on my channel. Subscribe... before Mom's voice note reaches you.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    card("voice-0.2", "M", "Mom · Voice note 0:07", ["Mom hasn't spoken in 2 years", "\"Don't come home.\""]),
    clip("outside-0.2", file="clip3.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Voice Note continues", ("channel", 0.3))],
   [("sting", "dont", 0), ("heartbeat", "voice", 0), ("sting", "inside", 0), ("sting", "someone", 0)],
   ["inside"], ["outside", "inside"],
   {"scene": 0, "lines": ["MOM CAN'T SPEAK", "SHE SENT A VOICE"], "sub": "'Don't come home.'"},
   "Voice Note · Pt 1: Mom Hasn't Spoken Since Her Stroke. She Sent Me a Voice Note.",
   "Mom hasn't spoken since her stroke. At 3 AM she sent a voice note: Don't come home. I was already outside her door.",
   "Would you open the door?",
   clips=["dark house door night",
          {"ai": "A phone on a dark nightstand showing a voice note waveform, glowing in a dim hallway, close-up, 3 AM",
           "move": "dolly-in", "fallback": "photo: phone glowing dark hallway"},
          {"ai": "A narrow dark hallway ending at a closed bedroom door with a thin line of light underneath, a shadow moving behind the gap",
           "motion": "the shadow under the door slowly shifts and the light flickers", "fallback": "dark hallway door night"}],
   series=VN(1, "Mom Hasn't Spoken Since Her Stroke. She Sent Me a Voice Note."))

day.ep("vn-p2", "series",
   "[whispering] Don't answer a voice that sounds like Mom. [quietly] Through the door, Mom's lips weren't moving. The "
   "whisper came from under her bed. \"Is he gone?\" [long pause] Mom met my eyes. She mouthed one word: run. "
   "[whispering] The voice said, \"Come in, beta.\" Subscribe... and don't answer Mom's voice.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    card("whisper-0.2", "!", "Mom · Bedroom", ["Her lips are not moving", "The voice is under the bed"]),
    title3("come-0.1", "COME IN,", "BETA.", "IT HAD HER VOICE.", "Part 1 is on the channel", ("voice", 0.4))],
   [("sting", "dont", 0), ("heartbeat", "whisper", 0), ("sting", "mouthed", 0), ("sting", "come", 0)],
   ["whisper"], ["mouthed", "come"],
   {"scene": 0, "lines": ["HER LIPS", "DIDN'T MOVE"], "sub": "the voice was under her bed"},
   "Voice Note · Pt 2: Mom's Lips Never Moved. The Voice Was Under Her Bed.",
   "Mom's lips weren't moving. The whisper came from under her bed, in her voice. She mouthed one word: run.",
   "Did you guess the twist?",
   clips=["dark bedroom door night",
          {"ai": "An elderly woman sitting upright in a dim bedroom seen from the doorway, her hands gripping the blanket, a dark gap under the bed",
           "move": "dolly-in", "fallback": "photo: old woman bed dark room"},
          {"ai": "The dark gap under a bed in a dim bedroom, two pale fingers curling out from the shadow along the floor, close-up",
           "motion": "the pale fingers slowly curl and withdraw into the dark", "fallback": "dark under bed"}],
   series=VN(2, "Mom's Lips Never Moved. The Voice Was Under Her Bed."))

day.save()
