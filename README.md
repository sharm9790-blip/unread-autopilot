# UNREAD autopilot

Daily scary Shorts for the UNREAD YouTube channel, fully in the cloud.

1. **06:00 IST** - claude.ai cloud routine runs the `daily-shorts` skill: writes 5 new stories (one 2-part series) into
   `daily/<date>/`, lints them with `pipeline/check_day.py`, pushes to `claude/daily-shorts`.
2. **GitHub Actions** (`produce.yml`) - Pixabay clips, ElevenLabs voice, render, upload scheduled at
   12:30 / 14:30 / 16:30 / 18:00 / 19:30 IST, series links, then a Telegram report (@sharmi_yt_upload_status_bot).
3. **08:00 IST** - if no stories were written, Telegram warns.

Secrets (repo settings): `PIXABAY_API_KEY`, `ELEVENLABS_API_KEY`, `YT_CLIENT_SECRET_JSON`, `YT_TOKEN_JSON`,
`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

If the Telegram report says `YOUTUBE_REAUTH_NEEDED`: on the Mac run any upload once (browser sign-in), then
`gh secret set YT_TOKEN_JSON < ~/.config/scary-short/youtube_token.json`.

Run a day by hand: Actions → produce-daily-shorts → Run workflow (date), or locally
`python3 pipeline/produce.py daily/<date> --no-upload`.

## Free photo motion (parallax)

`pipeline/parallax.py` turns one still into a 2.5D camera-move clip with no AI video credits. A depth model
separates near from far, then a virtual camera moves so the foreground shifts more than the background.

    python3 pipeline/parallax.py photo.jpg daily/<date>/s3.mp4 --move dolly-in --dur 5 --fog 0.3 --dust 50

Then use it as a normal scene: `{"type": "clip", "file": "s3.mp4", ...}`. Moves: dolly-in, dolly-out,
pan-left, pan-right, rise, fall, orbit, sway (loops). `--strength` 0.03 subtle / 0.06 normal / 0.10 dramatic.
Depth comes from `<photo>.depth.png` if present, else Depth Anything V2 Small (Mac: ~10 s, needs
`transformers<5` with the installed torch 2.4), else a weak bottom-is-near guess. Compute depth on the Mac
(`--depth-only`) and commit the PNG so the runner needs only numpy + Pillow. A 5 s clip renders in ~15 s
on the M1 with OpenCV, ~90 s without it.
In the daily pipeline, write `"photo: <words>"` or `{"photo": "<words>", "move": "orbit"}` in a clip list: produce.py
takes a vertical Pixabay photo (skipping cut-outs, preferring dark, on-topic hits) and renders a 10 s parallax clip.
A video query with no usable hit falls back to a photo the same way. Photo ids go into used_clips.json as `img:<id>`.
