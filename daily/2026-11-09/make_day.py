import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
from batchlib import Day, clip, title3, lines, card, lock, call, series, COOL, WARM

day = Day(__file__)
LIFT = lambda p, e: series("Floor 0", p, 2, e)

day.ep("feet-door", "rules",
   "[whispering] Never sleep with your feet toward the door. [quietly] Grandma said it invites them. I forgot. "
   "Something cold gripped my ankles and pulled, slowly, off the bed. [long pause] I woke in the hallway, dragged past "
   "my own door. [whispering] Through the gap, I saw my body still lying there... feet toward the door. Subscribe... "
   "and never sleep that way.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    clip("through-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("body-0.1", "MY BODY", "WAS STILL", "IN BED.", "Which way do you sleep?", ("lying", 0.3))],
   [("sting", "never", 0), ("heartbeat", "cold", 0), ("sting", "hallway", 0), ("sting", "body", 0)],
   ["gripped"], ["hallway", "body"],
   {"scene": 0, "lines": ["FEET TOWARD", "THE DOOR?"], "sub": "something pulled me out"},
   "Never Sleep With Your Feet Toward the Door. I Did.",
   "Grandma said sleeping with your feet toward the door invites them. Last night something pulled me out by the ankles.",
   "Which way do you sleep?",
   clips=["dark bedroom door night", "photo: dark hallway doorway"])

day.ep("floor0-p1", "series",
   "[whispering] My building has nine floors. Tonight the lift showed a tenth button: zero. [quietly] It glowed red. "
   "I pressed it. The doors opened on my own corridor, but every door had my name on it. [long pause] Behind one, my "
   "mother called, \"You're late.\" She lives in the village. [whispering] Part two is on my channel. Subscribe... "
   "count your building's floors.",
   [clip(grade={"dim": 0.9, "tint": COOL}),
    card("every-0.2", "0", "Lift · Floor 0", ["ALL DOORS: YOUR NAME", "Mom is waiting"]),
    title3("part-0.1", "PART 2", "ON THE", "CHANNEL.", "Floor 0 continues", ("channel", 0.3))],
   [("sting", "zero", 0), ("heartbeat", "pressed", 0), ("sting", "late", 0), ("sting", "village", 0)],
   ["zero"], ["late", "village"],
   {"scene": 0, "lines": ["LIFT BUTTON", "FLOOR ZERO"], "sub": "every door had my name"},
   "Floor 0 · Pt 1: My Lift Grew a Tenth Button",
   "My building has nine floors. Tonight the lift showed a button for zero. Every door had my name.",
   "Would you press it?",
   clips=["elevator interior night", "photo: apartment corridor night"], series=LIFT(1, "My Lift Grew a Tenth Button"))

day.ep("floor0-p2", "series",
   "[whispering] Don't press zero twice. [quietly] I ran back into the lift and pressed nine. It stopped at zero again. "
   "My mother stood outside, smiling too wide. [long pause] \"Come home,\" she said, in my voice. The doors closed. "
   "[whispering] Upstairs, my own flat lights are on. Someone else is living my life. Subscribe... and never press zero.",
   [clip(grade={"dim": 0.8, "desat": 0.3, "tint": COOL}),
    lock("upstairs-0.2", "9:09", "My Flat", "Welcome home. We kept your bed.", "upstairs"),
    title3("someone-0.1", "SOMEONE ELSE", "LIVES MY", "LIFE NOW.", "Part 1 is on the channel", ("life", 0.4))],
   [("sting", "dont", 0), ("sting", "mother", 0), ("heartbeat", "closed", 0), ("sting", "someone", 0)],
   ["mother"], ["voice", "someone"],
   {"scene": 0, "lines": ["I PRESSED NINE.", "IT STOPPED AT 0"], "sub": "floor zero, part 2"},
   "Floor 0 · Pt 2: Someone Else Is Living in My Flat",
   "I pressed nine. The lift stopped at zero. My mother said, in my voice, come home.",
   "Did you guess the twist?",
   clips=["elevator doors opening dark"], series=LIFT(2, "Someone Else Is Living in My Flat"))

day.ep("papa-flight", "voice-call",
   "[whispering] Papa's flight is still in the air. [quietly] The app says 31,000 feet. At 2 AM, he calls. \"Beta, open "
   "the door. I'm outside.\" I checked the app. Still flying. [long pause] I looked through the peephole. Papa waved, "
   "smiling. [whispering] The phone said, \"Papa is calling.\" And Papa's lips were not moving. Subscribe... before his flight lands.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    call("papa-0.2", "Papa"),
    title3("lips-0.1", "HIS LIPS", "WEREN'T", "MOVING.", "Would you open it?", ("moving", 0.4))],
   [("buzz", "papas", 0), ("heartbeat", "app", 0), ("sting", "peephole", 0), ("sting", "lips", 0)],
   ["peephole"], ["waved", "lips"],
   {"scene": 0, "lines": ["PAPA'S FLIGHT", "IS STILL UP"], "sub": "he's knocking anyway"},
   "Papa's Flight Is Still in the Air. He's Knocking.",
   "The app says Papa is at 31,000 feet. At 2 AM he called to say he's outside the door.",
   "Would you open it?",
   clips=["apartment door peephole dark"])

day.ep("cinema-seat", "second-person",
   "[whispering] You bought one ticket. Seat 7. [quietly] The midnight show is empty, except someone in seat 8. They "
   "don't breathe. On screen, the film is just this hall. [long pause] You on screen. And a pale figure leaning close to "
   "your ear. [whispering] You feel cold breath now. It whispers, \"Don't turn. I'm only watching.\" Subscribe... "
   "and never buy one ticket.",
   [clip(grade={"dim": 0.95, "tint": COOL}),
    clip("on-0.2", file="clip2.mp4", grade={"dim": 0.85, "tint": COOL}),
    title3("turn-0.2", "DON'T TURN.", "IT'S ONLY", "WATCHING.", "Would you turn?", ("watching", 0.4))],
   [("sting", "seat", 0), ("heartbeat", "breathe", 0), ("sting", "leaning", 0), ("sting", "turn", 0)],
   ["leaning"], ["leaning", "whispers"],
   {"scene": 0, "lines": ["1 TICKET.", "SEAT 8 TAKEN"], "sub": "the midnight show"},
   "1 Ticket. Seat 7. Someone Is Sitting in Seat 8.",
   "The midnight show is empty, except seat 8. Then the screen shows you, and what leans close.",
   "Would you turn around?",
   clips=["empty cinema theater", "photo: empty cinema seats dark"])

day.save()
