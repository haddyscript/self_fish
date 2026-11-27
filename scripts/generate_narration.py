#!/usr/bin/env python3
"""
Generate the Female and Male story narration for the SELF + FISH landing page
using ElevenLabs (natural, human-sounding AI voices).

It writes, for each voice:
  assets/audio/story-<voice>.mp3   the narration audio
  assets/audio/story-<voice>.json  the start time of every word, so the page
                                   highlights words exactly in sync

Usage (from the project folder):
  export ELEVENLABS_API_KEY="your key"         # never commit this key
  python3 scripts/generate_narration.py         # both voices
  python3 scripts/generate_narration.py female  # just one
  python3 scripts/generate_narration.py --list  # list voices on your account

Pick different voices with environment variables (voice IDs from your
ElevenLabs Voice Library):
  ELEVENLABS_FEMALE_VOICE_ID   default: Sarah  (soft, warm, American)
  ELEVENLABS_MALE_VOICE_ID     default: Brian  (deep, calm narrator, American)
  ELEVENLABS_MODEL_ID          default: eleven_multilingual_v2

Only the Python 3 standard library is needed.
"""
import base64
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index.html")
OUT_DIR = os.path.join(ROOT, "assets", "audio")
API = "https://api.elevenlabs.io/v1"

VOICES = {
    "female": os.environ.get("ELEVENLABS_FEMALE_VOICE_ID", "EXAVITQu4vr4xnSDxMaL"),  # Sarah
    "male": os.environ.get("ELEVENLABS_MALE_VOICE_ID", "nPczCjzI2devNBz1zQrb"),      # Brian
}
MODEL = os.environ.get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")

# Settings tuned for warm, unhurried storytelling rather than an announcer tone
VOICE_SETTINGS = {
    "stability": 0.45,
    "similarity_boost": 0.8,
    "style": 0.25,
    "use_speaker_boost": True,
    "speed": 0.94,
}


def story_text():
    """Read the founder story straight from index.html so audio and page always match."""
    src = open(PAGE, encoding="utf-8").read()
    m = re.search(r'<div class="story" id="story">(.*?)</div>', src, re.S)
    if not m:
        sys.exit("Could not find the founder story (div#story) in index.html")
    paras = re.findall(r"<p[^>]*>(.*?)</p>", m.group(1), re.S)
    clean = [html.unescape(re.sub(r"<[^>]+>", "", p)).strip() for p in paras]
    return [re.sub(r"\s+", " ", p) for p in clean if p]


def request(method, path, body=None, key=None):
    req = urllib.request.Request(API + path, method=method)
    req.add_header("xi-api-key", key)
    req.add_header("Accept", "application/json")
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data=data, timeout=120) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        sys.exit("ElevenLabs error %s: %s" % (e.code, detail[:500]))


def word_start_times(text, chars, starts):
    """Start time (seconds) of each whitespace-separated word, matching the page's word split."""
    # Map each character of our text to the returned characters (normally identical;
    # tolerate small normalisation differences such as dropped whitespace or quote styles)
    pos, j = [], 0
    for ch in text:
        k = j
        while k < len(chars) and k < j + 8 and chars[k] != ch:
            k += 1
        if k < len(chars) and chars[k] == ch:
            j = k
            pos.append(j)
            j += 1
        else:
            pos.append(max(0, min(j, len(chars) - 1)))
    return [round(starts[pos[m.start()]], 3) for m in re.finditer(r"\S+", text)]


def generate(voice, key, paragraphs):
    # A blank line between paragraphs gives a natural, longer pause
    text = "\n\n".join(paragraphs)
    print("Generating %s narration (voice %s, model %s)..." % (voice, VOICES[voice], MODEL))
    res = request(
        "POST",
        "/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128" % VOICES[voice],
        {"text": text, "model_id": MODEL, "voice_settings": VOICE_SETTINGS},
        key,
    )
    align = res.get("alignment") or {}
    times = word_start_times(text, align.get("characters", []), align.get("character_start_times_seconds", []))
    expected = len(re.findall(r"\S+", " ".join(paragraphs)))
    if len(times) != expected:
        sys.exit("Got %d word timings, expected %d." % (len(times), expected))

    os.makedirs(OUT_DIR, exist_ok=True)
    mp3 = os.path.join(OUT_DIR, "story-%s.mp3" % voice)
    with open(mp3, "wb") as f:
        f.write(base64.b64decode(res["audio_base64"]))
    with open(os.path.join(OUT_DIR, "story-%s.json" % voice), "w") as f:
        json.dump({"voice_id": VOICES[voice], "model_id": MODEL, "words": times}, f)
    print("  wrote %s (%d KB, %d words timed)" % (os.path.relpath(mp3, ROOT), os.path.getsize(mp3) // 1024, len(times)))


def main():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("Set ELEVENLABS_API_KEY first (export ELEVENLABS_API_KEY=\"...\").")
    args = sys.argv[1:]
    if "--list" in args:
        for v in request("GET", "/voices", key=key).get("voices", []):
            labels = v.get("labels") or {}
            print("%-24s %s  %s %s %s" % (v["voice_id"], v["name"], labels.get("gender", ""), labels.get("accent", ""), labels.get("description", "")))
        return
    which = [a for a in args if a in VOICES] or list(VOICES)
    paragraphs = story_text()
    for voice in which:
        generate(voice, key, paragraphs)
    print("Done. Open the page and press \"Listen to Santesha's Story\".")


if __name__ == "__main__":
    main()
