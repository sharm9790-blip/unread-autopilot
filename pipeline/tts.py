"""Voiceover + word timestamps in ONE ElevenLabs API call (no transcription step).

Usage: python3 tts.py <episode_dir> [--voice VOICE_ID] [--model MODEL_ID]
  reads  <episode_dir>/narration.txt  (audio tags like [whispering] allowed)
  writes <episode_dir>/voice.mp3 and words.json
Needs ELEVENLABS_API_KEY in the environment (or in ~/.elevenlabs_key).
"""
import base64
import json
import os
import sys
import urllib.request

DEFAULT_VOICE = "BycOlIr9Aytiubl0LIIY"  # Gxl - bold, deep cinematic narrator
DEFAULT_MODEL = "eleven_v3"


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    path = os.path.expanduser("~/.elevenlabs_key")
    if not key and os.path.exists(path):
        key = open(path).read().strip()
    if not key:
        raise SystemExit("NO_API_KEY: set ELEVENLABS_API_KEY or use the connector path in SKILL.md")
    return key


def words_from_alignment(al):
    """Character timings -> word timings, dropping [audio tags]."""
    chars = al["characters"]
    st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
    out, cur, cs, ce, in_tag = [], "", None, None, False
    for ch, a, b in zip(chars, st, en):
        if ch == "[":
            in_tag = True
            continue
        if in_tag:
            in_tag = ch != "]"
            continue
        if ch.isspace():
            if cur:
                out.append({"text": cur, "start": cs, "end": ce})
            cur, cs = "", None
            continue
        if cs is None:
            cs = a
        cur += ch
        ce = b
    if cur:
        out.append({"text": cur, "start": cs, "end": ce})
    # drop stray punctuation-only tokens (e.g. "..." on its own)
    return [w for w in out if any(c.isalnum() for c in w["text"])]


def main():
    ep = sys.argv[1]
    voice, model = arg("--voice", DEFAULT_VOICE), arg("--model", DEFAULT_MODEL)
    text = open(os.path.join(ep, "narration.txt")).read().strip()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps({"text": text, "model_id": model}).encode(),
        headers={"xi-api-key": api_key(), "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        res = json.load(r)
    open(os.path.join(ep, "voice.mp3"), "wb").write(base64.b64decode(res["audio_base64"]))
    al = res.get("alignment") or res["normalized_alignment"]  # raw text keeps "3:17" as typed
    words = words_from_alignment(al)
    json.dump(words, open(os.path.join(ep, "words.json"), "w"))
    print(f"voice.mp3 + words.json  words={len(words)}  spoken={words[-1]['end']:.1f}s")


if __name__ == "__main__":
    main()
