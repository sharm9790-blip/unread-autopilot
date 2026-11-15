"""Small machine-translation helper for titles/descriptions (Google Translate's public web endpoint, no key).

Used where the daily writer doesn't hand-translate (the Sunday compilation, one-off fixes). Series names before
": " are kept in English ("Night Feed · Pt 2: ..."), since literal translations of names read oddly.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_day import LANGS  # noqa: E402  the same 26 languages as the Shorts

GT = {"fil": "tl"}  # YouTube code -> Google Translate code


def tr(text, lang):
    q = urllib.parse.urlencode({"client": "gtx", "sl": "en", "tl": GT.get(lang, lang), "dt": "t", "q": text})
    for i in range(4):
        try:
            d = json.load(urllib.request.urlopen("https://translate.googleapis.com/translate_a/single?" + q, timeout=30))
            return "".join(p[0] for p in d[0] if p[0]).strip()
        except Exception:  # noqa: BLE001 - rate limits: back off and retry
            time.sleep(2 + 3 * i)
    raise RuntimeError(f"translate failed ({lang})")


def title(text, lang):
    pre, body = (text.split(": ", 1) if " · " in text and ": " in text else ("", text))
    return (pre + ": " if pre else "") + tr(body, lang)


def localizations(title_en, lead_en, rest, suffix=""):
    """{lang: {title, description}}: translated title + translated lead paragraph, the rest (chapters, links) English."""
    out = {}
    for L in LANGS:
        try:
            out[L] = {"title": (title(title_en, L) + suffix)[:100], "description": (tr(lead_en, L) + "\n\n" + rest)[:5000]}
        except RuntimeError:
            continue  # a missing language is fine; never block the upload
    return out
