# UNREAD channel learnings (from YouTube Analytics, Oct 2026)

Every daily Short must follow these. Keep this file updated when new analytics come in.

Lessons from YouTube Analytics on 2026-10-26 (pulled with `scripts/yt_analytics.py`; numbers saved in branding/analytics.csv):
- **Length:** Shorts under 30 s had a median of ~1,050 views; 45–60 s had ~190 and over 60 s ~70. Keep scary Shorts 20–30 s and end with a loop back to the start.
- **Hook:** only ~35% of viewers watch past the first seconds (target 50%+). Open on the scariest line or image, with no setup.
- **Topic drift:** Stoic Shorts got ~30 views and space Shorts 0–12 on this horror channel. Horror viewers swipe past them. Keep this channel horror (plus maybe bedtime); other topics belong on their own channels.
- **Spike vs baseline:** Oct 22 was a one-off spike (23.7k views, 107 subs). No horror was posted after Oct 23, and views collapsed.
- **Posting volume:** dumping 29 a day lowered views per video. Use 2–3 a day, scheduled.
- **What works:** series Parts 1–2 (Alder Lane, Mile Marker 13), "family rule" stories, and titles ending in #creepy #horror. Almost no shares or comments, so ask a question at the end and pin a comment.

- **Production rules now in the scary-short skill (2026-10-26):** every Short has Pixabay `clip` footage plus a subscribe end card (spoken "Subscribe..." line + `subscribe` key). Batches rotate the formats rules / pick-one / second-person / text story. Templates: shorts/batch-oct27 (clips) and shorts/batch-oct29 (clips + subscribe + formats). Compare the formats in analytics once they're live.


**Batch Nov 7–21 (made 2026-11-06, shorts/batch-nov07):** the user asked for 15 scary Shorts on a daily schedule, so it's 1/day at 16:30 IST. Each Short has a Pixabay video + a Pixabay vertical photo (photo.mp4 push-in via fetch_media.py), Flash voice, and a "Subscribe..." line plus a come-back end card ("NEW SCARY STORY EVERY DAY" / "PART 2 TOMORROW"). There are three 2-part series where Part 2 airs the next day. The user then asked for **4/day** (12:30, 14:30, 16:30, 18:00 IST), so the batch now runs Nov 7–10. `batch-nov07/reschedule.py` moves already-uploaded Shorts via videos.update. Each Part 1 takes a day's last slot and its Part 2 the next day's first slot. The Pixabay CDN sometimes returns "Rate limit exceeded" as the image body, so check the file size before using it.

**Update 2026-10-29** (data in branding/analytics_oct29.csv and uploads_oct29.json; the Analytics API runs ~3 days behind, so recent videos use lifetime viewCount):
- The new 22–31 s clip+subscribe horror Shorts (Oct 27–29) got 900–1,040 views each within 1–2 days for the best ones. The median is lower: Oct 27 ≈ 905, Oct 28 ≈ 100. The rules above are working.
- Larkspur Day 1 (~50–66 s, character-cutout style) underperformed. Rooms 1–3 got about 200 views each, Rooms 4–10 got 5–52, and only 1 subscriber came from the whole batch. Room 1 average view was 29%, with 32% engaged. 10 at once on one day (Oct 23) went into the collapse.
- Larkspur long video (9:41): 35 views, mostly suggested videos. 73% of viewers left within ~35 s (8 s silent title intro, then a slow Room 1 open). Only 6% stayed past 2 min, and it gained 0 subs. Long videos need a cold-open hook, not a title card.
- The 1-min bedtime story got 1,026 views, so bedtime is the one non-horror format that fits. Stoic, space and kids content stays low (4–250).

**Update 2026-10-29 evening (live viewCount; the Analytics API only reaches Oct 26):** the Oct 27–28 batch is bimodal. 4 Shorts got ~900–1,040 views (Dead Mom Called, Daughter/Lady in Room, Two of Me, Selfie) and 6 got 60–424. By slot: 16:30 IST 2/2 winners (967, 1,043); 21:00 0/2 (136, 60). The only Short with no clip (Group Chat) got 136. The winners open on a command or a child's voice ("Don't answer the call", "Never take a selfie", "Mommy… who's the lady"); the losers open on a neutral notification. Subscribers went 100 → 113 between Oct 27 and Oct 29, right as the first subscribe-card Short (s01 Bed 13: 540 views, 13 likes in 8 h, 2.4% like rate) went live. That's not proven yet; re-check once the per-video analytics arrive.

## Nov 2026 additions
- 2-part series (Part 1 cliffhanger "Part two is on my channel", Part 2 one slot later the same day) send viewers to the next video; series parts earned the most views historically (Alder Lane, Mile Marker 13).
- Slots (from 2026-11-10): 12:30 / 16:30 standalones, 18:00 Part 1, 19:30 Part 2 (4/day; 14:30 dropped for volume, not proven weak). 21:00+ is the worst.
- From 2026-11-08 (ideas from the Instagram agent skill's Reel rules, not yet proven on UNREAD - compare engagedPct and
  outlier before/after with yt_analytics.py): on-screen hook card for the first 2.8 s, captions inside the safe zone
  (y 230-1440), picture changes every ~3.5 s, closing line echoes the hook (loop), number/name in the hook when it fits.

## Update 2026-11-09 (live views of the 23 Shorts posted Nov 3-7, each 2+ days old)
- **Length:** ≤30 s median 599 views vs 222 over 30 s (month: 25-30 s 599, 31-44 s 144, 45 s+ 42). The autopilot drifted to
  32-41 s because the voice reads ~1.75 words/s + 3 s end card. Now: 40-48 words, and produce.py speeds the voice up to
  1.15x so the Short lands at ≤30 s; the Telegram report flags anything still longer.
- **Slot:** 14:30 got 79/125/139/264, but two were Part 1s and one a weak title, and "The School Said Dad Picked Him Up"
  got 905 at 14:30 on Nov 8. So 14:30 is NOT proven bad; it was dropped to post 4/day (fewer posts per day did better
  in October) and to free the evening for the series. Re-test it with a strong standalone before ruling it out.
- **Series:** Part 1s got 44/125/139 (three at 14:30) vs 959 for the one at 18:00; Part 2s 473-613. Series now 18:00 + 19:30.
- **Titles:** winners = a threat inside home/family + a short contradicting sentence ("The School Said Dad Picked Him Up.
  I'm His Dad." 905, "A Man Whispered on My Baby Monitor. I Live Alone." 880). Losers = number puzzles, transit,
  objects ("30 Desks. 31 Students." 190, "3 Elevators Open at 3 AM" 154, "My Cleaner Cleaned 4 Rooms" 79).
- **Engagement:** ~15 likes per 1K views is fine, but only 3 comments across 23 Shorts and ~15 shares a month.
- Compare Shorts from the first batch with these rules against Nov 3-7 before treating them as proven.

## Update 2026-11-15 (Analytics to Nov 12 + live views; and a "break the 1K cap" Shorts-growth video)
- Views/Short fell after Nov 8: Nov 8 releases ~1,000 each; Nov 9-11 ~100-500; Nov 12-14 ~25-200. 7-day views -32%.
  "Stayed vs swiped" (engagedPct) dropped from 30-44% (Nov 8) to 15-25% (Nov 9-10), the same days photo-parallax clips
  started replacing real footage and posting rose to 4-5/day. Likely causes, not proven.
- Changes from Nov 16: **3 Shorts/day** (12:30 standalone, 18:00 Part 1, 19:30 Part 2); the **first clip is always real
  moving footage**; each standalone copies the *shape* of a `state/winners.json` top Short (refreshed daily from live
  views); a tailored "📤 Send this to ..." share line in every description.
- Not used from the video: trending music and custom Shorts thumbnails need the YouTube phone app (no API) and music
  under narration hurts horror; channel warm-up only matters for brand-new channels.
- Re-check ~Nov 20: engagedPct and median views of Nov 16+ Shorts vs Nov 9-14.
