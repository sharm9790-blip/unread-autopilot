import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM
import langs as L

day = Day(__file__)
SR = lambda p, e: series("Night Bell", p, 2, e)

day.ep("dadi-landline", "text-story",
   "[whispering] Dadi answered our landline at midnight. [quietly] Dadi died last year. Mom grabbed the receiver: \"Who is this?\" "
   "[long pause] Dadi's voice said: \"Tell Riya to stop sleeping in my bed.\" Riya sleeps in Dadi's old bed. "
   "[whispering] The line clicked. Subscribe... before the landline rings.",
   [clip(),
    clip("died-0.2", file="clip2.mp4"), clip("grabbed-0.2", file="clip3.mp4"),
    clip("voice-0.2", file="clip4.mp4"), clip("riya#2-0.2", file="clip5.mp4"),
    clip("clicked-0.3", file="clip6.mp4"),
    title3("clicked-0.1", "DADI SAID:", "GET OUT OF", "MY BED.", "Would you look at Riya's bed?", ("subscribe", 0.4))],
   [("sting", "dadi", 0), ("heartbeat", "died", 0), ("sting", "voice", 0), ("sting", "clicked", 0)],
   ["answered"], ["voice", "clicked"],
   {"scene": 0, "lines": ["DADI ANSWERED", "THE LANDLINE"], "sub": "dadi died last year"},
   "Dadi Answered the Landline at Midnight. Dadi Died Last Year.",
   "Our landline rang at midnight and Dadi answered it. Dadi died last year. Then she asked about Riya's bed.",
   "Would you pick up the receiver?",
   clips=[{"ai": "An old black landline phone on a dark hallway table at night, the receiver lifted off the cradle and hanging by its cord, a faint warm lamp glow", "key": True, "move": "dolly-in", "fallback": "old telephone dark"},
          {"ai": "A framed photo of an elderly Indian grandmother in a white saree on a wall, garland on the frame, dim room", "move": "pan-left", "fallback": "old photo frame dark"},
          {"ai": "Mom gripping a landline receiver in a dim hallway, back to camera, night, small hall lamp", "move": "rise", "fallback": "woman phone dark hallway"},
          {"ai": "The old landline receiver close up, cord swinging slightly, shadows on the wall", "move": "dolly-out", "fallback": "telephone cord dark"},
          {"ai": "Riya asleep in an old wooden bed with a faded quilt, a thin dark shape standing at the foot of the bed, moonlight through a window", "move": "orbit", "fallback": "child bed dark room"},
          {"ai": "An old grandmother silhouette in a white saree standing in a dark doorway beside the landline table, face in shadow, hand resting on the phone", "key": True, "move": "fall", "fallback": "dark figure doorway"}],
   look="2d", characters="Riya: Indian girl, 10, two short braids, yellow nightdress. Mom: Indian woman, 38, long black braid, green cotton saree, face in shadow. Dadi: elderly Indian woman, white saree, grey hair in a bun, face in shadow.",
   share="the friend who still has a landline at home",
   langs=L.build(0))

day.ep("night-bell-p1", "series",
   "[whispering] Never answer the doorbell at 2 AM. [quietly] Ours rang. The camera showed my husband outside, smiling. "
   "But he was in the shower, humming. [long pause] The doorbell rang again. In the bathroom, the humming stopped. "
   "[whispering] Part two is on my channel. Subscribe... before your doorbell rings at 2 AM.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    clip("showed-0.2", file="clip2.mp4"),
    card("shower-0.3", "!", "Doorbell Camera · 2:00 AM", ["VISITOR: your husband", "Your husband: in the shower"]),
    clip("stopped-0.2", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Night Bell continues", ("channel", 0.3))],
   [("sting", "never", 0), ("heartbeat", "showed", 0), ("buzz", "shower", 0), ("sting", "stopped", 0)],
   ["stopped"], ["shower", "stopped"],
   {"scene": 0, "lines": ["NEVER ANSWER", "THE 2 AM BELL"], "sub": "my husband is outside. and in the shower"},
   "Night Bell · Pt 1: My Husband Rang Our Bell. He Was in the Shower",
   "The doorbell camera showed my husband outside, smiling. But he was in the shower, humming. Then the humming stopped.",
   "Would you open the door?",
   clips=["doorbell night rain",
          {"ai": "A doorbell camera view at night of a man standing on a porch in heavy rain, drenched, head slightly tilted, fisheye wide angle, cold light", "move": "dolly-in", "fallback": "photo: front door rain night"},
          {"ai": "A dark bathroom door with steam under it and a thin line of light, the hallway empty, a small camera screen glowing at the edge of frame", "motion": "the bathroom door slowly opens an inch", "fallback": "bathroom door dark"}],
   series=SR(1, "My Husband Rang Our Bell. He Was in the Shower"), share="the friend who lives alone with a doorbell camera",
   langs=L.build(1))

day.ep("night-bell-p2", "series",
   "[whispering] Never let your husband in twice. [quietly] The shower stopped. He stepped out whispering: \"Don't open the door. That's not me.\" "
   "The doorbell rang. On the camera, the drenched one smiled: \"Neither is he.\" [long pause] Water dripped from our bedroom ceiling. "
   "[whispering] Subscribe... and never answer the doorbell at 2 AM.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    clip("stopped-0.2", file="clip2.mp4"),
    clip("neither-0.2", file="clip3.mp4"),
    title3("ceiling-0.1", "NEITHER", "WAS MY", "HUSBAND.", "Part 1 is on the channel", ("subscribe", 0.4))],
   [("sting", "never", 0), ("heartbeat", "stopped", 0), ("sting", "neither", 0), ("sting", "ceiling", 0)],
   ["neither"], ["neither", "ceiling"],
   {"scene": 0, "lines": ["TWO HUSBANDS.", "ONE LIED."], "sub": "that's not me"},
   "Night Bell · Pt 2: Two Husbands. One Whispered: That's Not Me.",
   "Two husbands, one doorbell. One whispered: that's not me. The other smiled on the camera. Then the ceiling started dripping.",
   "Which husband would you trust?",
   clips=["dark bathroom door",
          {"ai": "A husband in a towel standing in a dim bedroom doorway, dry, face in shadow, one finger raised to his lips, a doorbell camera screen glowing on the bed behind", "move": "dolly-in", "fallback": "photo: dark bedroom doorway"},
          {"ai": "A dark bedroom ceiling with a dark wet stain spreading, water dripping onto a bed below, a pale hand pressed against the plaster from above", "motion": "a drop of water falls and the pale hand slowly slides across the ceiling", "fallback": "ceiling water stain dark"}],
   series=SR(2, "Two Husbands. One Whispered: That's Not Me."), share="the friend who showers at night while home alone",
   langs=L.build(2))

day.save()
