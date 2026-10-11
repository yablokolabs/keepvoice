#!/usr/bin/env bash
# Generate the voice-over and its timing with ElevenLabs.
# Needs ELEVENLABS_API_KEY in the environment. Run from this folder.
set -euo pipefail
VOICE_ID="Xb7hH8MSUJpSbSDYk0k2" # Alice: British female (voices from the library need a paid plan)
TEXT=$(sed '1,/^---$/d' provider_script.md)
RESPONSE=$(mktemp)
curl -sf -X POST "https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}/with-timestamps" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" -H "Content-Type: application/json" \
  -d "$(jq -n --arg text "$TEXT" '{text: $text, model_id: "eleven_multilingual_v2",
        voice_settings: {stability: 0.5, similarity_boost: 0.75}}')" -o "$RESPONSE"
jq -r '.audio_base64' "$RESPONSE" | base64 --decode > audio.mp3
# The API gives one time per character; join the characters into words.
jq '.alignment as $a
    | reduce range(0; $a.characters | length) as $i ({words: [], cur: null};
        ($a.characters[$i]) as $c
        | if ($c | test("\\s")) then
            (if .cur then .words += [.cur] | .cur = null else . end)
          else
            .cur = (if .cur then .cur | .word += $c | .end = $a.character_end_times_seconds[$i]
                    else {word: $c, start: $a.character_start_times_seconds[$i],
                          end: $a.character_end_times_seconds[$i]} end)
          end)
    | {words: (.words + (if .cur then [.cur] else [] end))}' "$RESPONSE" > timing.json
rm -f "$RESPONSE"
