# Demo video and diagrams

This folder is a [videowright](https://github.com/scosman/videowright) project. It makes `docs/demo/keepvoice-demo.mp4` and converts the diagrams to PNG.

```bash
npm install
npx playwright install chromium
```

## Diagrams

The diagrams follow the [diagram-design](https://github.com/cathrynlavery/diagram-design) style. The source of each diagram is `docs/diagrams/<name>.html`. To export:

```bash
# 1. HTML to SVG, with the script from a diagram-design checkout
python3 <diagram-design>/skills/diagram-design/scripts/export_svg.py ../docs/diagrams/pipeline.html ../docs/diagrams/pipeline.svg

# 2. SVG to PNG at 2x
node scripts/svg-to-png.mjs
```

## Video

- Segments: `segments/kv-*/index.ts`
- Timeline, plan, script and audio: `videos/keepvoice_demo/`
- Style: `styles/editorial-mono/`

```bash
npx videowright dev                      # preview
npx videowright render keepvoice_demo --output ../docs/demo/keepvoice-demo.mp4
```

**Known problem:** videowright 0.1.0 and 0.1.1 from npm cannot start the preview or the render. The package does not contain `src/index.ts`, which its own pages import. Until a corrected version is published, use a source checkout:

```bash
git clone https://github.com/scosman/videowright && cd videowright
npm install && npm run build --workspace=packages/lib
cd <this folder>
node <videowright>/packages/lib/dist/cli/bin.js render keepvoice_demo --output ../docs/demo/keepvoice-demo.mp4
```

## Voice-over

The narration is generated with ElevenLabs (voice "Alice", British English). To generate it again, set `ELEVENLABS_API_KEY` and run `videos/keepvoice_demo/audio/originals/voiceovers/v1/generate.sh`. Then build the track with the command in `videos/keepvoice_demo/audio/audio_plan.md`. If the audio changes, update the times in `audio/tracks/v1/track.ts` from the new `timing.json`.
