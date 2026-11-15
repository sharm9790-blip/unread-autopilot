import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM

day = Day(__file__)
NF = lambda p, e: series("Night Feed", p, 2, e)

day.ep("dada", "second-person",
   "[whispering] My baby said Dada to the empty chair. [quietly] Her father died before she was born. "
   "I've never said his name near her. [long pause] She giggled and held up her arms. "
   "[whispering] The chair creaked as it lifted her. Subscribe... because my baby said Dada.",
   [clip(grade={"dim": 0.95, "tint": WARM}),
    clip("giggled-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("lifted-0.5", file="clip3.mp4"),
    title3("lifted-0.1", "THE CHAIR", "LIFTED", "HER UP.", "Would you take her back?", ("dada", 0.4))],
   [("sting", "dada", 0), ("heartbeat", "never", 0), ("sting", "giggled", 0), ("sting", "lifted", 0)],
   ["lifted"], ["giggled", "lifted"],
   {"scene": 0, "lines": ["BABY SAID DADA", "AT EMPTY CHAIR"], "sub": "her father is dead"},
   "My Baby Said Dada to the Empty Chair. He Died Before She Was Born.",
   "My baby said Dada to the empty chair. Her father died before she was born. Then the chair creaked and lifted her.",
   "Would you take her back?",
   clips=["dark living room night",
          {"ai": "An empty wooden dining chair beside a baby high chair in a dim kitchen at night, soft lamp light, wide shot",
           "move": "dolly-in", "fallback": "photo: empty chair dark kitchen"},
          {"ai": "A dim kitchen at night, a wooden chair pulled slightly out from the table, a pale faint shape leaning over it toward a baby seat",
           "motion": "the chair slowly slides back an inch and the pale shape leans forward", "fallback": "dark kitchen night"}])

day.ep("tank-p", "rules",
   "[whispering] Never answer when your son calls from the cupboard. [quietly] My son is asleep in my arms. "
   "Still, \"Mummy, open it,\" came from the cupboard. In his voice. [long pause] I looked down. "
   "[whispering] His mouth was shut. The cupboard knocked twice. Subscribe... and never open the cupboard.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    clip("looked-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    clip("knocked-0.4", file="clip3.mp4"),
    title3("knocked-0.1", "HIS VOICE", "CAME FROM", "THE CUPBOARD.", "Would you open it?", ("cupboard", 0.4))],
   [("sting", "never", 0), ("heartbeat", "still", 0), ("sting", "looked", 0), ("sting", "knocked", 0)],
   ["knocked"], ["looked", "knocked"],
   {"scene": 0, "lines": ["NEVER ANSWER", "THE CUPBOARD"], "sub": "it had my son's voice"},
   "My Son Called Mummy From the Cupboard. He Was Asleep in My Arms.",
   "My son was asleep in my arms when he called 'Mummy, open it' from the cupboard. His mouth was shut.",
   "Would you open the cupboard?",
   clips=["dark bedroom closet night",
          {"ai": "A wooden bedroom cupboard door slightly ajar in a dark room, a thin line of light, a mother's silhouette holding a child in the foreground",
           "move": "dolly-in", "fallback": "photo: wooden cupboard dark room"},
          {"ai": "A closed dark wooden cupboard in a dim bedroom, a faint pale small handprint on the inside of a gap at the door edge, close-up",
           "motion": "the door trembles and opens one inch", "fallback": "dark closet door"}])

day.ep("nf-p1", "series",
   "[whispering] Don't feed the baby when your husband does. [quietly] At 3 AM, I heard him in the nursery. "
   "Singing. A bottle clinking. [long pause] I walked in. The baby was in my arms. "
   "[whispering] Then who was feeding the crib? Part two is on my channel. Subscribe... before the 3 AM feed.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    card("singing-0.2", "H", "Husband · Working night shift", ["Home at 6 AM", "Don't wake the baby"]),
    clip("who-0.2", file="clip3.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Night Feed continues", ("channel", 0.3))],
   [("sting", "dont", 0), ("heartbeat", "singing", 0), ("sting", "baby#2", 0), ("sting", "who", 0)],
   ["walked"], ["baby#2", "who"],
   {"scene": 0, "lines": ["DON'T FEED", "THE BABY"], "sub": "he feeds her at 3 AM"},
   "Night Feed · Pt 1: My Husband Feeds the Baby at 3 AM. I'm Holding the Baby.",
   "At 3 AM I heard my husband feeding the baby in the nursery. I walked in. The baby was already in my arms.",
   "Would you open the nursery door?",
   clips=["dark nursery night",
          {"ai": "A dark nursery at night with an empty crib, a baby bottle on the rail, faint blue night-light, a tall shadow on the wall, wide shot",
           "move": "dolly-in", "fallback": "photo: empty crib dark nursery"},
          {"ai": "A dim nursery crib seen from the doorway, a tall thin silhouette bent over it in the dark, a mother's shoulder in the foreground",
           "motion": "the silhouette's head slowly turns toward camera", "fallback": "dark nursery crib"}],
   series=NF(1, "My Husband Feeds the Baby at 3 AM. I'm Holding the Baby."))

day.ep("nf-p2", "series",
   "[whispering] Don't hand the baby to him. [quietly] My husband was on night shift, miles away. "
   "The figure held out its arms for her. [long pause] The baby reached for it. "
   "[whispering] Then she looked at me and said, \"Mama, he feeds me every night.\" Subscribe... and don't hand the baby over.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    card("figure-0.2", "!", "Nursery · 3:00 AM", ["He held out his arms", "She reached for him"]),
    title3("every-0.1", "HE FEEDS", "HER EVERY", "NIGHT.", "Part 1 is on the channel", ("baby", 0.4))],
   [("sting", "dont", 0), ("heartbeat", "figure", 0), ("sting", "reached", 0), ("sting", "every", 0)],
   ["figure"], ["reached", "every"],
   {"scene": 0, "lines": ["HE HELD OUT", "HIS ARMS"], "sub": "my husband was miles away"},
   "Night Feed · Pt 2: My Baby Said: He Feeds Me Every Night.",
   "My husband was miles away. The figure held out its arms and my baby reached for it. Then she said he feeds her every night.",
   "Did you guess the twist?",
   clips=["dark nursery door night",
          {"ai": "A tall thin dark figure standing beside a crib in a dim nursery with its arms held out, seen from behind the mother, faint blue light",
           "move": "dolly-in", "fallback": "photo: dark nursery shadow figure"},
          {"ai": "A baby's small hand reaching out of a mother's arms toward a dark shape in a dim nursery, close-up, blue night-light",
           "motion": "the baby's hand slowly stretches toward the dark and the light flickers", "fallback": "dark nursery night"}],
   series=NF(2, "My Baby Said: He Feeds Me Every Night."))

day.save()
