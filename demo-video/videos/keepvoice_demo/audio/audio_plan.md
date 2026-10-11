# Audio Plan

## Plan

VO-only track. Single full-file voiceover placed at 0s, set to a constant loudness, with 1.6 s of silence added at the end for the last frame.

### Cue 1 -- voiceover
- **Source:** audio/originals/voiceovers/v1/audio.mp3
- **Slice:** full file
- **Place at:** 0s

### Final mix command

```bash
ffmpeg -y \
  -i audio/originals/voiceovers/v1/audio.mp3 \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11,apad=pad_dur=1.6" -ar 44100 \
  -c:a libmp3lame -q:a 2 \
  {TRACK_OUT}
```

## Log

## 2026-10-11 -- Initial build (v1)
**Change:** initial build
