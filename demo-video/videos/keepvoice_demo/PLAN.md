# Plan: keepvoice demo

## Purpose
- Audience: people who make videos and get copyright claims for background music.
- Takeaway: keepvoice removes songs, including the singers, and keeps the speech.
- Constraints / hard guidelines: no footage from real videos, no music (the tool removes music), less than 45 seconds.

## Style
- Active style: editorial-mono
- Notes: mono labels are 22px, larger than the style default, so that they can be read in a README preview.

## Audio intent
- Voiceover: yes
- Sound effects: no
- Background music: no
- Notes: British female voice (ElevenLabs "Alice"). Voices from the ElevenLabs library need a paid plan.

## Segment outline
1. kv-problem — the video has a copyrighted song in the background.
2. kv-vocals — a vocal remover keeps the singers.
3. kv-model — the dialogue model splits speech, music and effects; only speech is kept.
4. kv-result — measured result (−39 dB to below −81 dB) and the picture copy.
5. kv-cta — the command and the repository.

## Script
See voiceover_script/script.md

---

## Log

### 2026-10-11 — Initial scaffold
- Created segments: kv-problem, kv-vocals, kv-model, kv-result, kv-cta
- Timeline: 5 segments, style: editorial-mono
- Voiceover: drafted, generated with ElevenLabs, synced from word timing
