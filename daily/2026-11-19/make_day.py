import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM
import langs as L

day = Day(__file__)
W9 = lambda p, e: series("Ward 9", p, 2, e)

day.ep("fan", "rules",
   "[whispering] Papa is fixing our ceiling fan at midnight. [quietly] His back to me, humming. Then my phone lit up: Papa. "
   "\"Beta, I'm on night shift. Don't look up.\" [long pause] The man on the ladder turned his head all the way around. "
   "[whispering] Subscribe... before Papa fixes your fan.",
   [clip(),
    clip("humming-0.2", file="clip2.mp4"), clip("phone-0.2", file="clip3.mp4"),
    clip("shift-0.3", file="clip4.mp4"), clip("ladder-0.2", file="clip5.mp4"),
    clip("turned-0.1", file="clip6.mp4"),
    title3("around-0.1", "IT WAS", "NOT MY", "PAPA.", "Would you look up?", ("subscribe", 0.4))],
   [("sting", "papa", 0), ("heartbeat", "humming", 0), ("sting", "shift", 0), ("sting", "turned", 0)],
   ["shift"], ["ladder", "turned"],
   {"scene": 0, "lines": ["PAPA FIXES", "THE FAN AT 12"], "sub": "Papa is on night shift"},
   "Papa Is Fixing Our Fan at Midnight. Papa Is on Night Shift.",
   "Papa is fixing our ceiling fan at midnight. Then Papa called: he is on night shift. Don't look up.",
   "Would you look up?",
   clips=[{"ai": "A man in a grey shirt on a ladder under a ceiling fan in a dark Indian bedroom at midnight, seen from behind, a girl in bed watching, dim lamp light, wide shot", "key": True, "move": "dolly-in", "fallback": "ceiling fan night"},
          {"ai": "The man on the ladder from behind, arms raised to the ceiling fan, a thin beam of light from the doorway, dark room", "move": "pan-left", "fallback": "man ladder dark"},
          {"ai": "Riya's phone on the bed glowing in the dark, a caller named Papa on the screen, close-up", "move": "rise", "fallback": "phone ringing dark"},
          {"ai": "Papa in a security guard uniform sitting in a small night-shift booth under a tube light, far away, wide shot", "move": "dolly-out", "fallback": "security booth night"},
          {"ai": "Riya from behind sitting rigid in bed, the ladder and the man silhouetted ahead of her, ceiling fan still", "move": "orbit", "fallback": "dark bedroom fan"},
          {"ai": "The man on the ladder with his head turned all the way around toward the camera, face in deep shadow, eyes reflecting light, dark bedroom", "key": True, "move": "fall", "fallback": "dark figure ceiling"}],
   look="2d", characters="Riya: girl, 15, long braid, blue nightdress. Papa: Indian man, 45, grey shirt, moustache, face always in shadow. Security guard Papa: same man in khaki guard uniform.",
   share="the friend whose papa works night shifts",
   langs=L.build(L.E1_T, L.E1_H))

day.ep("ward-p1", "series",
   "[whispering] My mom is in a coma. [quietly] I whispered goodnight. Her lips never moved. A voice answered: "
   "\"Goodnight, beta.\" It came from the empty bed. [long pause] The nurse paled. Bed 10 has been empty since Sunday. "
   "[whispering] Part two is on my channel. Subscribe... before your mom is in a coma.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("whispered-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("nurse-0.2", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Ward 9 continues", ("channel", 0.3))],
   [("sting", "my", 0), ("heartbeat", "whispered", 0), ("sting", "empty", 0), ("sting", "sunday", 0)],
   ["goodnight#2"], ["bed", "sunday"],
   {"scene": 0, "lines": ["MOM IS IN A COMA", "SOMEONE ANSWERS"], "sub": "from the empty bed"},
   "Ward 9 · Pt 1: Mom Is in a Coma. Someone Answers When I Talk.",
   "My mom is in a coma. When I whispered goodnight, a voice answered from the empty bed beside hers.",
   "Would you say goodnight?",
   clips=["hospital ward night",
          {"ai": "A dim hospital ward at night, a mother lying in bed with monitors, an empty made bed beside her, daughter seen from behind at the bedside, cold green light",
           "move": "dolly-in", "fallback": "photo: hospital ward dark"},
          {"ai": "An empty hospital bed with a crumpled sheet in a dark ward, a nurse far away in the doorway with a torch, faint shape under the sheet",
           "motion": "the sheet slowly rises as if someone is breathing under it", "fallback": "hospital corridor night"}],
   series=W9(1, "Mom Is in a Coma. Someone Answers When I Talk."), share="the friend who sits with a parent in hospital",
   langs=L.build(L.E2_T, L.E2_H))

day.ep("ward-p2", "series",
   "[whispering] Never say goodnight in Ward 9. [quietly] I forgot. The empty bed whispered back. Mom's monitor went flat. "
   "The nurse stopped. Mom was sitting up, smiling. [long pause] \"Thank you, beta,\" it said in Mom's voice. "
   "\"Nobody ever says goodnight to me.\" [whispering] Subscribe... and never say goodnight in Ward 9.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    clip("flat-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("thank-0.3", file="clip3.mp4"),
    title3("subscribe-0.1", "IT WORE", "MOM'S", "VOICE.", "Part 1 is on the channel", ("ward", 0.4))],
   [("sting", "never", 0), ("heartbeat", "whispered", 0), ("sting", "flat", 0), ("sting", "thank", 0)],
   ["flat"], ["smiling", "thank"],
   {"scene": 0, "lines": ["NEVER SAY", "GOODNIGHT"], "sub": "Ward 9 at night"},
   "Ward 9 · Pt 2: Mom's Voice Said Goodnight. She Was Already Gone.",
   "I said goodnight in Ward 9. The empty bed answered, and Mom's monitor went flat. Then Mom sat up smiling.",
   "Did you guess the twist?",
   clips=["hospital room dark",
          {"ai": "A hospital monitor showing a flat green line in a dark ward, a daughter at the bedside seen from behind, a nurse frozen in the doorway, cold light",
           "move": "dolly-in", "fallback": "photo: hospital monitor dark"},
          {"ai": "A woman sitting upright in a hospital bed in a dark ward, smiling too wide, face half in shadow, her daughter in the foreground from behind",
           "motion": "the woman's head slowly tilts toward camera", "fallback": "dark figure hospital"}],
   series=W9(2, "Mom's Voice Said Goodnight. She Was Already Gone."), share="the friend who never skips goodnight",
   langs=L.build(L.E3_T, L.E3_H))

day.save()
