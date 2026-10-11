# How keepvoice works

## The problem

A video recorded in a public place can contain music that is protected by copyright. A platform can detect that music and block the video or remove its income. The usual solution is to remove the music and keep the speech.

## First attempt: a vocals model

The first attempt used `htdemucs_ft` from Demucs with the `--two-stems vocals` option. This model was trained on songs. It gives two stems:

- `vocals`: all human voice
- `no_vocals`: all other sound

The instrumental music went to `no_vocals`, which is correct. But the songs had singers, and a singer is a human voice. The singers went to `vocals` together with the speaker. In a section with no speech (1:31 to 1:45 in the test video), the song could be heard in the output at up to −39 dB.

This is not an error of the model. The model did its task. The task was the wrong one.

## Final method: a dialogue model

The correct task is known in film sound as cinematic sound demixing: separate a film soundtrack into dialogue, music and effects. A model for this task learns that speech is dialogue and that a song, with or without a singer, is music.

keepvoice uses the checkpoints from [MVSEP-CDX23-Cinematic-Sound-Demixing](https://github.com/ZFTurbo/MVSEP-CDX23-Cinematic-Sound-Demixing). They are Demucs v4 (hybrid transformer) models trained on the Divide and Remaster (DnR) dataset. The output has three stems in this order: music, effect, dialog.

keepvoice runs three checkpoints and uses the mean of their dialog stems. One checkpoint is used with `--fast`.

![Stems of a vocals model and of a dialogue model](diagrams/stems.png)

In the same section of the test video, the dialog stem is below −81 dB. That level cannot be heard.

## The pipeline

![Pipeline](diagrams/pipeline.png)

| Step | Tool | Detail |
|---|---|---|
| Extract audio | ffmpeg | 44.1 kHz, stereo, 32-bit float. A mono source is copied to left and right. ffmpeg `-ac 2` is not used for mono because it lowers the level by 3 dB. |
| Separate | PyTorch, Demucs | `apply_model` with `shifts=1`, `overlap=0.8`. A GPU is used if one is available. |
| Mute ranges | ffmpeg | `volume=0` in each range given with `--mute`. |
| Remux | ffmpeg | Picture stream copied (`-c:v copy`). Audio encoded as AAC, 192 kbit/s. |

## Why there are mute ranges

The model removes most of the music, but a very quiet residue (approximately −60 dB) can stay where the music is loud, for example in an intro that an editing app added. If you know that you do not speak in a section, `--mute` makes that section fully silent. This is the safest result for automatic music detection.

keepvoice does not select these ranges automatically. A wrong automatic selection would remove speech, and only you know where you speak.

## How the result was checked

The results in the README come from measurements, not from listening:

- The level of each stem was calculated for each second of the video.
- Spectrograms of the two methods were compared in the sections where the levels were different. Singing shows as flat, steady lines with reverberation. Speech shows as lines that move quickly, with sharp starts.
- The picture stream of the input and of the output were compared with a checksum.

A person then listened to the full output and confirmed the result.

## Code

| File | Function |
|---|---|
| `keepvoice/pipeline.py` | Audio extraction, time ranges, remux. The separator is a parameter, so the tests can run this code with real ffmpeg and without the model. |
| `keepvoice/separate.py` | Downloads the checkpoints and runs the model. |
| `keepvoice/cli.py` | Command-line options. |
