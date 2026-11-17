import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM
import langs as L

day = Day(__file__)
RC = lambda p, e: series("Rocking Chair", p, 2, e)

day.ep("schoolgate", "rules",
   "[whispering] My sick daughter was waiting at the school gate. [quietly] I hugged her. Cold. She whispered, \"Papa, don't take me home.\" "
   "[long pause] Then my wife texted: \"Why is she calling you from her bed?\" "
   "[whispering] The girl in my arms smiled. Subscribe... and watch the school gate.",
   [clip(),
    clip("hugged-0.2", file="clip2.mp4"), clip("whispered-0.2", file="clip3.mp4"),
    clip("wife-0.2", file="clip4.mp4"), clip("bed-0.2", file="clip5.mp4"),
    clip("girl-0.1", file="clip6.mp4"),
    title3("smiled-0.1", "IT WAS", "NOT MY", "DAUGHTER.", "Would you let go?", ("watch", 0.4))],
   [("sting", "sick", 0), ("heartbeat", "hugged", 0), ("sting", "texted", 0), ("sting", "smiled", 0)],
   ["whispered"], ["girl", "smiled"],
   {"scene": 0, "lines": ["SICK DAUGHTER", "AT THE GATE"], "sub": "she was home in bed"},
   "My Daughter Waited at the School Gate. She Was Home Sick.",
   "My sick daughter was waiting at the school gate. She felt cold. My wife texted that our daughter was still in her bed.",
   "Would you let go of her?",
   clips=[{"ai": "A small girl in a red school uniform stands alone at an empty school gate in grey afternoon light, Papa walking toward her from behind, wide shot", "key": True, "move": "dolly-in", "fallback": "school gate empty"},
          {"ai": "Papa kneels and hugs the small girl at the school gate, shot from behind Papa, the girl's pale hands on his shirt, cold teal light", "move": "pan-left", "fallback": "father hugging child"},
          {"ai": "Close shot of the girl's pale face in shadow beside Papa's ear, she is whispering, school gate blurred behind", "move": "rise", "fallback": "child shadow dusk"},
          {"ai": "Papa standing at the gate reading a phone screen, his worried face lit blue by the phone, dusk", "move": "dolly-out", "fallback": "man phone dusk"},
          {"ai": "Anaya, a sick girl, asleep in her bed at home under a blanket, warm lamp, a thermometer on the nightstand, wide shot", "move": "orbit", "fallback": "sick child bed"},
          {"ai": "Papa holding the girl in his arms at the gate, the girl's head over his shoulder smiling too wide at the camera, her eyes reflecting light, dusk", "key": True, "move": "fall", "fallback": "child smile dark"}],
   look="2d", characters="Papa: Indian man, 38, short black hair, grey shirt, tired face. Anaya: girl, 8, two braids, red school uniform, very pale.",
   share="the friend who picks up their kid from school",
   langs=L.build(L.E1_T, L.E1_H))

day.ep("chair-p1", "series",
   "[whispering] Never sit in Grandpa's chair while he's away. [quietly] It rocks by itself at 3 AM. Grandpa is in the hospital. "
   "Tonight a shape sat in it. [long pause] The hospital called: Grandpa woke screaming, \"Don't let him sit!\" "
   "[whispering] Part two is on my channel. Subscribe... before the chair rocks again.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("tonight-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("hospital-0.4", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Rocking Chair continues", ("channel", 0.3))],
   [("sting", "never", 0), ("heartbeat", "rocks", 0), ("sting", "shape", 0), ("sting", "screaming", 0)],
   ["shape"], ["sit", "screaming"],
   {"scene": 0, "lines": ["NEVER SIT IN", "GRANDPA'S CHAIR"], "sub": "it rocks at 3 AM"},
   "Rocking Chair · Pt 1: Grandpa's Chair Rocks. He's in Hospital.",
   "Grandpa's chair rocks by itself at 3 AM. He is in the hospital. Tonight a shape sat in it. Then the hospital called.",
   "Would you sit in it?",
   clips=["rocking chair dark",
          {"ai": "An old wooden rocking chair in a dark living room at night, a tall thin shadow sitting in it facing the window, wide shot, cold moonlight",
           "move": "dolly-in", "fallback": "photo: rocking chair dark room"},
          {"ai": "A hospital bed at night with an old man sitting up screaming, a phone glowing on the blanket, a nurse rushing in from the corridor, dim green light",
           "motion": "the old man's head turns slowly toward camera", "fallback": "hospital room night"}],
   series=RC(1, "Grandpa's Chair Rocks. He's in Hospital."), share="the friend whose grandparent has an old chair",
   langs=L.build(L.E2_T, L.E2_H))

day.ep("chair-p2", "series",
   "[whispering] Never turn your back on Grandpa's chair. [quietly] Grandpa came home pale and sat in it. "
   "\"Better me than the boy,\" he said. [long pause] The chair rocked twice. A shape smiled behind him. "
   "[whispering] The hospital called: \"He died at 3.\" Subscribe... and never sit in the chair.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    clip("better-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("shape-0.3", file="clip3.mp4"),
    title3("died-0.1", "HE DIED", "AT 3 AM", "IN BED.", "Part 1 is on the channel", ("sit", 0.4))],
   [("sting", "never", 0), ("heartbeat", "pale", 0), ("sting", "rocked", 0), ("sting", "died", 0)],
   ["rocked"], ["shape", "died"],
   {"scene": 0, "lines": ["NEVER TURN", "YOUR BACK"], "sub": "grandpa died at 3"},
   "Rocking Chair · Pt 2: Grandpa Came Home. He Died at 3 AM.",
   "Grandpa came home pale and sat in his chair. Then the hospital called: he had died at 3 AM.",
   "Did you guess the twist?",
   clips=["old man armchair dark",
          {"ai": "A pale old man in a white kurta sitting in a wooden rocking chair in a dark living room, a boy watching from the doorway, seen from behind the boy, warm dim lamp",
           "move": "dolly-in", "fallback": "photo: old man chair dark"},
          {"ai": "Behind a rocking chair in a dark room a tall thin shadow bends over the sitting old man, smiling, moonlight through curtains, wide shot",
           "motion": "the rocking chair slowly rocks and the shadow leans closer", "fallback": "dark figure room"}],
   series=RC(2, "Grandpa Came Home. He Died at 3 AM."), share="the friend who never sits in someone else's chair",
   langs=L.build(L.E3_T, L.E3_H))

day.save()
