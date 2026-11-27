# SELF + FISH Landing Page

**Woman to Woman. Human to Human.**

Landing page for SELF + FISH by founder Santesha Johnson: a guided wellness journal to heal, reflect, and grow.

This is a static, single-page website (HTML and CSS, with a little JavaScript). It has no backend, database, or build step. Purchases and contact messages go to the existing Shopify store at [selfandfish.com](https://selfandfish.com).

## Page sections

1. **Hero:** full-screen moving beach video with the headline "A Gentle Return to You"
2. **Meet the Founder:** Santesha's photo and story, with a "Listen to Santesha's Story" button that reads the story aloud (browser text-to-speech, Female or Male voice) and highlights each word as it is spoken
3. **The Wellness Journal:** journal introduction, Heal / Reflect / Grow / You themes, details, price, and order button
4. **Make Room for You:** journal benefits
5. **Coming Soon:** Signature Keychain and Tote
6. **Call to action:** "Get Your Journal Now"
7. **Contact:** link to the store's contact page

## Project structure

```
index.html        The whole page (markup, styles, and scripts)
assets/
  logo.png        Original SELF + FISH logo (source file)
  logo-web.png    Web-sized copy of the logo used on the page
  founder.png     Original founder photo (unmodified source file)
  founder-cutout.png  Founder photo with the background removed (used on the page; face not altered)
  founder-alt.png Second original founder photo (not used on the page yet)
  journal-2.png   Journal cover
  keychain.jpg    Signature Keychain product image
  tote.jpg        Tote product image
  hero-poster.jpg Still frame shown while the hero video loads
```

## Run locally

Serve the folder with any static server so the images and video load correctly:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Hero video

The page plays `assets/hero-beach.mp4` (or `assets/hero-beach.webm`) first. Add the approved clip, with bright white sand and clear blue water, under that name. Until that file exists, the hero falls back to the video currently hosted on selfandfish.com.

Keep the clip short, loop-friendly, and compressed (ideally under 5 MB at 1080p). The video is muted, autoplays, and pauses for visitors who have reduced motion turned on.

## Story narration (Female / Male)

The "Listen to Santesha's Story" button reads the founder story aloud and highlights each word as it is spoken.

**Generate natural voices with ElevenLabs (recommended):**

1. Create an ElevenLabs account. A paid plan (Starter or above) is needed for commercial use on a business website.
2. Copy your API key from your ElevenLabs profile settings.
3. From this folder, run:

   ```bash
   export ELEVENLABS_API_KEY="paste-your-key-here"
   python3 scripts/generate_narration.py
   ```

   This creates `assets/audio/story-female.mp3`, `story-male.mp3` and their `.json` word timings. Default voices are Sarah (female) and Brian (male). To try others, run `python3 scripts/generate_narration.py --list` and set `ELEVENLABS_FEMALE_VOICE_ID` / `ELEVENLABS_MALE_VOICE_ID`.
4. Commit and push the files in `assets/audio/`. Never commit the API key.

If you change the story text in `index.html`, run the script again so the audio matches.

**Or use your own recordings:** add them to `assets/audio/`:

```
assets/audio/story-female.mp3   (or .m4a)
assets/audio/story-male.mp3     (or .m4a)
```

When a file is present, the page plays it for that voice for every visitor. When it is missing, that voice falls back to the device's own speech voice. Each recording must read exactly this text:

> I created SELF + FISH from a personal journey of healing, self-discovery, and growth. This journal is a collection of the lessons I've learned, the challenges I've faced, and the tools that helped me keep going. My heart is to encourage you, remind you that you're not alone, and give you a safe space to heal, reflect, and grow into the next version of yourself.

Word highlighting follows the recording automatically. For exact timing, add `assets/audio/story-female.json` (and `story-male.json`) containing `{ "words": [ ... ] }`, with the start time in seconds of each of the 65 words.

**Device voice fallback:** the page picks the most natural voice the visitor's device offers (Microsoft "Natural" voices in Edge, Apple Premium/Enhanced voices, then standard voices) and skips novelty voices. If a device has no voice for one option, that option is disabled.

## Links

| Button | Destination |
| --- | --- |
| Order the Journal / Order Your Journal / Get Your Journal Now | https://selfandfish.com/products/self-fish-journal |
| Signature Keychain | https://selfandfish.com/products/self-fish-signature-keychain |
| Tote | https://selfandfish.com/products/self-fish-accessories |
| Contact / Send a Message | https://selfandfish.com/pages/contact |
| Privacy Policy | https://selfandfish.com/policies/privacy-policy |

Check that every link works before launch.

## Brand guidelines

- **Colors:** olive green, gold accents, and premium white/ivory only. The blue water in the hero video is part of the footage, not a brand color.
- **Logo:** use the existing SELF + FISH logo as supplied; do not redesign it.
- **Founder photo:** use the original photo; do not retouch, regenerate, or alter Santesha's features.
- **Fonts:** Cormorant Garamond (headings) and Jost (body), both from Google Fonts.

Design or color changes need client approval.

## Deploy

Any static host works. For GitHub Pages, open **Settings → Pages** in this repository, choose the `main` branch, and save.
