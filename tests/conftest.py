import hashlib
import subprocess
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf


def _run(*args: str) -> bytes:
    return subprocess.run(args, check=True, capture_output=True).stdout


def make_video(path: Path, seconds: float = 6.0, audio: bool = True, channels: int = 2) -> Path:
    cmd = [
        "ffmpeg",
        "-v",
        "error",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"testsrc=size=160x120:rate=10:duration={seconds}",
    ]
    if audio:
        cmd += [
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=440:duration={seconds}",
            "-ac",
            str(channels),
            "-c:a",
            "aac",
        ]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)]
    _run(*cmd)
    return path


def video_md5(path: Path) -> str:
    packets = _run(
        "ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v", "-c", "copy", "-f", "h264", "-"
    )
    return hashlib.md5(packets).hexdigest()


def duration(path: Path) -> float:
    out = _run(
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)
    )
    return float(out)


def audio_db(path: Path, start: float, end: float, tmp: Path) -> float:
    wav = tmp / f"measure_{start}_{end}.wav"
    _run("ffmpeg", "-v", "error", "-y", "-i", str(path), "-vn", "-ac", "1", str(wav))
    samples, rate = sf.read(wav)
    part = samples[int(start * rate) : int(end * rate)]
    return float(10 * np.log10(np.mean(part**2) + 1e-12))


def passthrough(audio: np.ndarray, rate: int) -> np.ndarray:
    return audio


@pytest.fixture
def video(tmp_path: Path) -> Path:
    return make_video(tmp_path / "in.mp4")
