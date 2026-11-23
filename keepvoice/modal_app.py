"""Run keepvoice on a Modal GPU.

modal run -m keepvoice.modal_app --video VIDEO.mp4 [--fast]
    [--mute 0-17,3:07-3:13.4] [--out PATH]
"""

import tempfile
from pathlib import Path

import modal

from .pipeline import parse_ranges

CACHE_DIR = "/root/.cache/keepvoice"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg")
    .pip_install("demucs>=4.0.1", "numpy", "soundfile", "torch>=2.0", "torchaudio>=2.0")
    .add_local_python_source("keepvoice")
)
cache = modal.Volume.from_name("keepvoice-cache", create_if_missing=True)
app = modal.App("keepvoice", image=image)


def cli_args(fast: bool, mute: str) -> list[str]:
    """Convert the entrypoint options to keepvoice CLI arguments."""
    ranges = [r.strip() for r in mute.split(",") if r.strip()]
    parse_ranges(ranges)
    args = ["--fast"] if fast else []
    for r in ranges:
        args += ["--mute", r]
    return args


@app.function(gpu="A10G", timeout=3600, volumes={CACHE_DIR: cache})
def separate(data: bytes, name: str, args: list[str]) -> bytes:
    from .cli import main

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / name
        src.write_bytes(data)
        out = Path(tmp) / "out.mp4"
        if main([str(src), "-o", str(out), *args]) != 0:
            raise RuntimeError("keepvoice failed")
        cache.commit()
        return out.read_bytes()


@app.local_entrypoint()
def run(video: str, fast: bool = False, mute: str = "", out: str = ""):
    src = Path(video)
    args = cli_args(fast, mute)
    dst = Path(out) if out else src.with_name(src.stem + "_voice_only.mp4")
    dst.write_bytes(separate.remote(src.read_bytes(), src.name, args))
    print(dst)
