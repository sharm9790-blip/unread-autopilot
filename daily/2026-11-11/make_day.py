import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM

day = Day(__file__)
UT = lambda p, e: series("Upstairs Tenant", p, 2, e)

day.ep("dad-call", "voice-call",
   "[whispering] Don't pick up. Dad is calling from the office. [quietly] He's sitting right across from me, "
   "eating dinner. The phone keeps ringing. I answer anyway. [long pause] A breathing voice says, \"Don't look at "
   "him, beta.\" [whispering] Dad stops chewing. Subscribe... and don't pick up.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    call("answer-0.2", "Dad (Office)"),
    clip("stops-0.3", file="clip3.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("stops-0.1", "DAD STOPPED", "CHEWING.", "AND SMILED.", "Would you look up?", ("chewing", 0.4))],
   [("buzz", "calling", 0), ("heartbeat", "answer", 0), ("sting", "dont#2", 0), ("sting", "stops", 0)],
   ["breathing"], ["stops", "chewing"],
   {"scene": 0, "lines": ["DON'T PICK UP.", "DAD IS CALLING"], "sub": "he's sitting across from me"},
   "Dad Called From the Office. Dad Was Eating Dinner Beside Me.",
   "Dad called from the office while Dad sat eating dinner across from me. The voice on the phone told me not to look at him.",
   "Would you look up?",
   clips=["family dinner table dark",
          {"ai": "A ringing phone face-up on a dim dinner table, a man's blurred silhouette sitting across, warm dim lamp, close-up, night",
           "move": "dolly-in", "fallback": "dinner table dark night"},
          {"ai": "A man seated at a dim dinner table seen from behind in shadow, a lit phone screen in the foreground",
           "motion": "the man's head slowly turns toward the camera", "fallback": "dark dining room night"}])

day.ep("nursery", "second-person",
   "[whispering] Don't go into the nursery tonight. [quietly] My wife is humming in there. She's asleep "
   "beside me. [long pause] The humming matches the lullaby our baby cries for. I opened the door. "
   "[whispering] The crib was rocking, and a voice sang, \"Shh, Mama's here.\" Subscribe... and never enter the nursery.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    clip("matches-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    card("crib-0.2", "!", "Nursery · 3:02 AM", ["THE CRIB IS ROCKING", "Mama is asleep next to you"]),
    clip("shh-0.3", file="clip3.mp4"),
    title3("mama-0.1", "MAMA'S", "ASLEEP NEXT", "TO ME.", "Would you open the door?", ("here", 0.4))],
   [("sting", "dont", 0), ("heartbeat", "humming", 0), ("sting", "crib", 0), ("sting", "mama", 0)],
   ["humming"], ["crib", "mama"],
   {"scene": 0, "lines": ["DON'T ENTER", "THE NURSERY"], "sub": "my wife is asleep beside me"},
   "Someone Hummed in Our Nursery. My Wife Was Asleep Beside Me.",
   "A lullaby hummed from the nursery at 3 AM. My wife was asleep next to me. The crib was rocking.",
   "Would you open the door?",
   clips=["dark hallway door night",
          {"ai": "A dark nursery with a wooden crib rocking gently, a faint pale shape bending over it, moonlight through curtains, wide shot",
           "move": "dolly-in", "fallback": "photo: dark nursery crib"},
          {"ai": "A wooden crib in a dark room, a small night-light glowing, a tall pale shadow on the wall above it",
           "motion": "the crib rocks slowly and the shadow on the wall leans over it", "fallback": "dark room night"}])

day.ep("tenant-p1", "series",
   "[whispering] Never answer the knock from upstairs. [quietly] Our house has one floor. Every night at 11, "
   "someone knocks on the ceiling. Mom says it's the tenant. [long pause] Last night, I knocked back. "
   "[whispering] Footsteps ran toward our stairs... that don't exist. Part two is on my channel. Subscribe... before the knock.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    card("ceiling-0.2", "!", "Ceiling · 11:00 PM", ["KNOCK. KNOCK. KNOCK.", "Our house has one floor"]),
    clip("footsteps-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("stairs-0.3", file="clip3.mp4"),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Upstairs Tenant continues", ("channel", 0.3))],
   [("knock", "knock", 0), ("heartbeat", "tenant", 0), ("sting", "footsteps", 0), ("sting", "stairs", 0)],
   ["knocked"], ["footsteps", "stairs"],
   {"scene": 0, "lines": ["NEVER ANSWER", "THE KNOCK ABOVE"], "sub": "our house has one floor"},
   "Upstairs Tenant · Pt 1: Our House Has One Floor. Something Knocks.",
   "Every night at 11 something knocks on our ceiling. Our house has one floor. Mom says it's the tenant. Last night I knocked back.",
   "Would you knock back?",
   clips=["ceiling dark room night",
          {"ai": "A bare ceiling of a dim old Indian house bedroom with a single bulb, faint dust in the air, shot looking up",
           "move": "dolly-in", "fallback": "photo: old ceiling dark room"},
          {"ai": "A plain ceiling in a dark room with a small hatch-like seam, a thin line of light leaking from it",
           "motion": "the seam in the ceiling opens a crack and the light flickers", "fallback": "dark ceiling light"}],
   series=UT(1, "Our House Has One Floor. Something Knocks."))

day.ep("tenant-p2", "series",
   "[whispering] Don't ask Mom who the tenant is. [quietly] I did. She went pale. \"We never had one. "
   "He came with the house.\" [long pause] A hatch opened above my bed. [whispering] A hand lowered a rent "
   "book. My name was written inside. Subscribe... and don't ask who lives upstairs.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    card("hatch-0.2", "!", "Rent Book · Ceiling", ["TENANT: UNKNOWN", "Next tenant: YOU"]),
    title3("name-0.1", "MY NAME", "WAS THE", "NEXT TENANT.", "Part 1 is on the channel", ("written", 0.4))],
   [("sting", "dont", 0), ("sting", "pale", 0), ("heartbeat", "hatch", 0), ("sting", "name", 0)],
   ["pale"], ["hatch", "name"],
   {"scene": 0, "lines": ["MY NAME IS IN", "THE RENT BOOK"], "sub": "upstairs tenant, part 2"},
   "Upstairs Tenant · Pt 2: A Hand Lowered a Rent Book With My Name",
   "Mom told me the tenant came with the house. Then a hatch opened above my bed and something handed down a rent book with my name.",
   "Did you guess the twist?",
   clips=["dark ceiling hatch night",
          {"ai": "A dim bedroom seen from the bed, a small square hatch open in the ceiling with darkness inside, wide shot",
           "move": "dolly-in", "fallback": "photo: dark ceiling room"},
          {"ai": "A small open hatch in a dark ceiling, a pale thin hand lowering an old notebook on a string into the room",
           "motion": "the pale hand slowly lowers the notebook", "fallback": "dark attic hatch"}],
   series=UT(2, "A Hand Lowered a Rent Book With My Name"))

day.save()
