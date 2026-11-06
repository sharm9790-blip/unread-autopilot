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
