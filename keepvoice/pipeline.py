"""Audio extraction, mute ranges and remux. The separation model is passed in."""

import subprocess
import tempfile
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path

import numpy as np
import soundfile as sf

SAMPLE_RATE = 44100

Separator = Callable[[np.ndarray, int], np.ndarray]
Range = tuple[float, float]


class KeepVoiceError(Exception):
    """A problem the user can correct: bad input file, bad option."""


def _seconds(clock: str) -> float:
    parts = clock.split(":")
    if not 1 <= len(parts) <= 3 or any(p.strip() == "" for p in parts):
        raise ValueError(clock)
    total = 0.0
    for part in parts:
        value = float(part)
        if value < 0:
            raise ValueError(clock)
        total = total * 60 + value
    return total


def parse_ranges(texts: Iterable[str]) -> list[Range]:
    """Turn 'START-END' texts into seconds. Times are seconds or [H:]MM:SS[.s]."""
    ranges = []
    for text in texts:
        try:
            start_text, end_text = text.split("-")
            start, end = _seconds(start_text), _seconds(end_text)
        except ValueError:
            raise ValueError(f"invalid time range '{text}', expected START-END") from None
        if start >= end:
            raise ValueError(f"invalid time range '{text}', START must be before END")
        ranges.append((start, end))
    return ranges


def _ffmpeg(*args: str) -> None:
    result = subprocess.run(["ffmpeg", "-v", "error", "-y", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise KeepVoiceError(f"ffmpeg failed: {result.stderr.strip()}")


def _audio_channels(src: Path) -> int:
    """Channel count of the first audio stream, 0 if there is none."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=channels",
            "-of",
            "csv=p=0",
            str(src),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise KeepVoiceError(f"cannot read {src}: {result.stderr.strip()}")
    return int(result.stdout.strip() or 0)


def remove_music(src: Path, dst: Path, separator: Separator, mute: Sequence[Range] = ()) -> None:
    """Write dst with the picture of src and only the speech that separator returns."""
    src, dst = Path(src), Path(dst)
    if not src.is_file():
        raise KeepVoiceError(f"input file not found: {src}")
    if dst.exists() and dst.samefile(src):
        raise KeepVoiceError("output and input are the same file; give a different output path")
    channels = _audio_channels(src)
    if channels == 0:
        raise KeepVoiceError(f"{src} has no audio stream")
    # -ac 2 lowers a mono source by 3 dB, so copy the one channel to left and right instead
    to_stereo = ["-af", "pan=stereo|c0=c0|c1=c0"] if channels == 1 else ["-ac", "2"]

    with tempfile.TemporaryDirectory() as tmp:
        mixed, speech = Path(tmp) / "mixed.wav", Path(tmp) / "speech.wav"
        _ffmpeg(
            "-i",
            str(src),
            "-vn",
            *to_stereo,
            "-ar",
            str(SAMPLE_RATE),
            "-c:a",
            "pcm_f32le",
            str(mixed),
        )
        audio, rate = sf.read(mixed, dtype="float32", always_2d=True)
        sf.write(speech, separator(audio, rate), rate, subtype="FLOAT")

        filters = []
        if mute:
            enabled = "+".join(f"between(t,{start},{end})" for start, end in mute)
            filters = ["-af", f"volume=0:enable='{enabled}'"]
        _ffmpeg(
            "-i",
            str(src),
            "-i",
            str(speech),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            *filters,
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(dst),
        )
