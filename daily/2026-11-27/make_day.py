import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM
import langs as L

day = Day(__file__)
SR = lambda p, e: series("Second Baby", p, 2, e)

day.ep("papa-scooter", "text-story",
   "[whispering] Papa's scooter honked outside our gate. [quietly] Papa was already home, asleep on the sofa. Mom gripped my arm: \"Don't open it.\" "
   "The honking stopped. Then the front door opened by itself. [long pause] Papa's voice came from the sofa: \"Who just came in?\" "
   "[whispering] Subscribe... before Papa's scooter honks.",
   [clip(),
    clip("already-0.2", file="clip2.mp4"), clip("gripped-0.2", file="clip3.mp4"),
    clip("honking-0.2", file="clip4.mp4"), clip("opened-0.2", file="clip5.mp4"),
    clip("voice-0.3", file="clip6.mp4"),
    title3("who-0.1", "PAPA WAS", "ALREADY", "INSIDE.", "Would you look at the door?", ("subscribe", 0.4))],
   [("sting", "papas", 0), ("heartbeat", "already", 0), ("knock", "opened", 0), ("sting", "who", 0)],
   ["honked"], ["opened", "who"],
   {"scene": 0, "lines": ["PAPA'S SCOOTER", "HONKED OUTSIDE"], "sub": "papa is asleep on the sofa"},
   "Papa's Scooter Is Outside Our Gate. Papa Is Asleep on the Sofa.",
   "Papa's scooter honked outside our gate. Papa was already home, asleep on the sofa. Then the front door opened by itself.",
   "Would you open the door?",
   clips=[{"ai": "An Indian family gate at night with a parked scooter behind it, its headlight glowing in the dark lane, a closed house door in the foreground", "key": True, "move": "dolly-in", "fallback": "scooter night street"},
          {"ai": "Papa asleep on a living room sofa under a thin blanket, lamp light, seen from the doorway", "move": "pan-left", "fallback": "sofa dark living room"},
          {"ai": "Mom gripping the wrist of Riya in a dim hallway, finger to her lips, both facing the front door", "move": "rise", "fallback": "dark hallway family"},
          {"ai": "A scooter headlight shining through the frosted glass of a front door, long shadows on the floor", "move": "dolly-out", "fallback": "car headlights window night"},
          {"ai": "The front door open an inch with darkness behind it, Riya and Mom frozen in the hallway, lamp light", "move": "orbit", "fallback": "open door dark night"},
          {"ai": "Papa sitting up on the sofa in the dark, his face in shadow turned toward a tall dark figure standing in the open doorway", "key": True, "move": "fall", "fallback": "dark figure doorway"}],
   look="2d", characters="Riya: Indian girl, 10, two short braids, yellow nightdress. Mom: Indian woman, 38, long black braid, green cotton saree, face in shadow. Papa: Indian man, 42, mustache, grey checked shirt, face in shadow.",
   share="the friend who waits up for their dad",
   langs=L.build(0))

day.ep("second-baby-p1", "series",
   "[whispering] Never take the second baby. [quietly] A nurse handed me a newborn at 3 AM. Mine slept beside me. "
   "She smiled: \"Both are yours.\" [long pause] Both babies opened their eyes... and looked at the door. "
   "[whispering] Part two is on my channel. Subscribe... before a nurse hands you a second baby.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("slept-0.2", file="clip2.mp4"),
    card("both-0.3", "!", "Nurse · Ward 4", ["BABY A: in your arms", "BABY A: in the crib"]),
    clip("opened-0.2", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Second Baby continues", ("channel", 0.3))],
   [("sting", "never", 0), ("heartbeat", "slept", 0), ("buzz", "both", 0), ("sting", "opened", 0)],
   ["opened"], ["both", "opened"],
   {"scene": 0, "lines": ["NEVER TAKE THE", "SECOND BABY"], "sub": "both are yours"},
   "Second Baby · Pt 1: A Nurse Gave Me a Baby. Mine Was Asleep",
   "A nurse placed a newborn in my arms at 3 AM. My own baby was asleep in the crib. She said both are mine.",
   "Would you take the baby?",
   clips=["hospital corridor night",
          {"ai": "A hospital crib with a sleeping newborn under a dim night light, a tired mother's arm holding a second small blanket bundle at the edge of frame", "move": "dolly-in", "fallback": "photo: hospital room night"},
          {"ai": "A dark hospital maternity room at 3 AM, a nurse silhouette standing at the door, two newborn bundles on the bed lit by a thin cold light", "motion": "the nurse's head slowly turns toward camera", "fallback": "hospital room dark night"}],
   series=SR(1, "A Nurse Gave Me a Baby. Mine Was Asleep"), share="the friend who just had a baby",
   langs=L.build(1))

day.ep("second-baby-p2", "series",
   "[whispering] Never let the nurse hold both babies. [quietly] I checked the wristbands. Mine said Baby A. The second baby's said Baby A too. "
   "The nurse whispered: \"Only one can go home.\" [long pause] The lights went out. Both babies whispered: \"Mama, choose.\" "
   "[whispering] Subscribe... and never take the second baby.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    clip("checked-0.2", file="clip2.mp4"),
    clip("lights-0.2", file="clip3.mp4"),
    title3("choose-0.1", "MAMA,", "CHOOSE.", "", "Part 1 is on the channel", ("subscribe", 0.4))],
   [("sting", "never", 0), ("heartbeat", "wristbands", 0), ("sting", "lights", 0), ("sting", "choose", 0)],
   ["lights"], ["lights", "choose"],
   {"scene": 0, "lines": ["NEVER LET HER", "HOLD BOTH"], "sub": "only one can go home"},
   "Second Baby · Pt 2: Both Wristbands Said Baby A. 'Mama, Choose.'",
   "Both wristbands said Baby A. The nurse said only one can go home. Then the lights went out.",
   "Which baby would you hold?",
   clips=["hospital room dark night",
          {"ai": "Two small hospital wristbands lying side by side on a blanket, both printed with the same label, cold light, close-up", "move": "dolly-in", "fallback": "photo: hospital bracelet"},
          {"ai": "A pitch dark hospital room, two small cribs side by side, two pale newborn faces turned toward camera, a nurse's shadow on the wall", "motion": "both small heads slowly turn toward camera", "fallback": "dark nursery night"}],
   series=SR(2, "Both Wristbands Said Baby A. 'Mama, Choose.'"), share="the friend who never sleeps in hospital rooms",
   langs=L.build(2))

day.save()
