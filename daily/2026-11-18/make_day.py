import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM
import langs as L

day = Day(__file__)
CH = lambda p, e: series("Crib Hand", p, 2, e)

day.ep("brother", "rules",
   "[whispering] My brother came home from the army tonight. [quietly] He hugged Ma and ate two rotis. Then his captain called: \"Why is he still at the border?\" "
   "[long pause] Ma was serving him a third roti. He smiled at me. "
   "[whispering] Subscribe... before your brother comes home.",
   [clip(),
    clip("hugged-0.2", file="clip2.mp4"), clip("captain-0.2", file="clip3.mp4"),
    clip("border-0.3", file="clip4.mp4"), clip("serving-0.2", file="clip5.mp4"),
    clip("smiled-0.1", file="clip6.mp4"),
    title3("subscribe-0.1", "IT WAS", "NOT MY", "BROTHER.", "Would you open the door?", ("before", 0.4))],
   [("sting", "brother", 0), ("heartbeat", "hugged", 0), ("sting", "captain", 0), ("sting", "smiled", 0)],
   ["captain"], ["third", "smiled"],
   {"scene": 0, "lines": ["BROTHER'S HOME", "BUT HE'S AWAY"], "sub": "his captain called"},
   "My Brother Came Home From the Army. He's Still at the Border.",
   "My brother came home from the army tonight. His captain called: he is still at the border.",
   "Would you open the door for him?",
   clips=[{"ai": "A tall soldier in olive uniform stands in the doorway of an Indian home at night, his face in shadow, Ma smiling at him from inside, warm lamp, wide shot", "key": True, "move": "dolly-in", "fallback": "soldier doorway night"},
          {"ai": "Ma hugging the soldier brother in a small living room, shot from behind the soldier, warm dim light", "move": "pan-left", "fallback": "mother hugging son"},
          {"ai": "Riya's phone on a table glowing in a dark room, a caller named Captain on the screen, close-up", "move": "rise", "fallback": "phone ringing dark"},
          {"ai": "A lonely army border post at night, barbed wire and a watchtower under cold moonlight, wide shot", "move": "dolly-out", "fallback": "border fence night"},
          {"ai": "Ma serving rotis to the soldier brother at a low dining table, the brother seen from behind, a third roti on the plate, warm kitchen light", "move": "orbit", "fallback": "indian kitchen night"},
          {"ai": "The soldier brother at the dinner table turning his head to smile too wide at the camera, eyes reflecting light, Riya in the foreground from behind, dark room", "key": True, "move": "fall", "fallback": "dark smile figure"}],
   look="2d", characters="Brother: Indian man, 28, olive army uniform, short hair, face always half in shadow. Ma: Indian woman, 55, grey-streaked bun, orange saree. Riya: girl, 16, long braid, blue kurta.",
   share="the friend whose brother is far from home",
   langs=L.build(L.E1_T, L.E1_H))

day.ep("crib-p1", "series",
   "[whispering] Someone holds my baby's hand every night. [quietly] The crib camera shows her tiny hand lifted around nothing. "
   "Last night, fingers were there. Long. Grey. Under the crib. [long pause] My husband whispered, \"Don't move.\" He was asleep. "
   "[whispering] Part two is on my channel. Subscribe... before someone holds your hand.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("last-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("husband-0.2", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Crib Hand continues", ("channel", 0.3))],
   [("sting", "someone", 0), ("heartbeat", "tiny", 0), ("sting", "grey", 0), ("sting", "asleep", 0)],
   ["fingers"], ["under", "asleep"],
   {"scene": 0, "lines": ["SOMEONE HOLDS", "MY BABY'S HAND"], "sub": "every night at 3 AM"},
   "Crib Hand · Pt 1: Someone Holds My Baby's Hand. My Husband Is Asleep.",
   "Every night someone holds my baby's hand through the crib bars. Last night I saw the fingers. Then my husband whispered.",
   "Would you check under the crib?",
   clips=["baby crib dark room",
          {"ai": "A dark nursery at night, a crib with a tiny hand lifted between the bars and long grey fingers curled around it from beneath, green night-camera light, close-up",
           "move": "dolly-in", "fallback": "photo: crib dark nursery"},
          {"ai": "A couple's bed in a dark bedroom, the husband lying asleep with his eyes closed, the wife sitting up rigid in the foreground from behind, a crib dimly visible at the far end",
           "motion": "the husband's lips slowly move in his sleep", "fallback": "bedroom night dark"}],
   series=CH(1, "Someone Holds My Baby's Hand. My Husband Is Asleep."), share="the friend with a new baby",
   langs=L.build(L.E2_T, L.E2_H))

day.ep("crib-p2", "series",
   "[whispering] Never pull your baby's hand away. [quietly] I pulled. Something under the crib pulled back. "
   "My husband woke calmly: \"Let it hold. It keeps her breathing.\" [long pause] He fed it her hand every night. "
   "[whispering] Tonight it let go... and held mine. Subscribe... and never let go of her hand.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    clip("husband-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("tonight-0.3", file="clip3.mp4"),
    title3("subscribe-0.1", "IT HELD", "MY HAND", "INSTEAD.", "Part 1 is on the channel", ("never", 0.4))],
   [("sting", "never", 0), ("heartbeat", "pulled", 0), ("sting", "breathing", 0), ("sting", "tonight", 0)],
   ["pulled#2"], ["fed", "tonight"],
   {"scene": 0, "lines": ["NEVER PULL", "HER HAND AWAY"], "sub": "my husband knew"},
   "Crib Hand · Pt 2: My Husband Knew. He Feeds It Her Hand.",
   "Something under the crib pulled my baby's hand. My husband said to let it. He had fed it her hand every night.",
   "Did you guess the twist?",
   clips=["father baby crib night",
          {"ai": "A calm husband in a dark nursery standing beside a crib, hand resting on the rail, wife seen from behind in the doorway, thin warm lamp light",
           "move": "dolly-in", "fallback": "photo: father nursery dark"},
          {"ai": "A woman's hand held tightly by long grey fingers reaching from under a crib in a dark nursery, close-up, cold blue night light",
           "motion": "the grey fingers slowly tighten around the hand", "fallback": "hand reaching dark"}],
   series=CH(2, "My Husband Knew. He Feeds It Her Hand."), share="the friend who checks on her baby every night",
   langs=L.build(L.E3_T, L.E3_H))

day.save()
