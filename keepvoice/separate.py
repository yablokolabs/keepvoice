"""Speech / music / effects separation with the CDX23 dialogue model.

The checkpoints are from https://github.com/ZFTurbo/MVSEP-CDX23-Cinematic-Sound-Demixing
(MIT). They are Demucs v4 models trained on the Divide and Remaster dataset.
"""

from pathlib import Path

import numpy as np

RELEASE_URL = (
    "https://github.com/ZFTurbo/MVSEP-CDX23-Cinematic-Sound-Demixing/releases/download/v.1.0.0/"
)
CHECKPOINTS = ("97d170e1-dbb4db15.th", "97d170e1-a778de4a.th", "97d170e1-e41a5468.th")
DIALOG_STEM = 2  # model output order is music, effect, dialog


class DialogueSeparator:
    """Callable that returns the speech stem of a (samples, 2) float array."""

    def __init__(self, fast: bool = False, cache_dir: Path | None = None):
        self.names = CHECKPOINTS[:1] if fast else CHECKPOINTS
        self.cache_dir = cache_dir or Path.home() / ".cache" / "keepvoice"
        self._models = None

    def _load(self):
        import torch
        from demucs.states import load_model

        self.cache_dir.mkdir(parents=True, exist_ok=True)
        models = []
        for name in self.names:
            path = self.cache_dir / name
            if not path.is_file():
                torch.hub.download_url_to_file(RELEASE_URL + name, str(path))
            models.append(load_model(str(path)))
        return models

    def __call__(self, audio: np.ndarray, rate: int) -> np.ndarray:
        import torch
        from demucs.apply import apply_model

        if self._models is None:
            self._models = self._load()
        mix = torch.from_numpy(np.ascontiguousarray(audio.T, dtype=np.float32))[None]
        device = "cuda" if torch.cuda.is_available() else "cpu"
        stems = [
            apply_model(model, mix, shifts=1, overlap=0.8, device=device)[0, DIALOG_STEM]
            for model in self._models
        ]
        return torch.stack(stems).mean(dim=0).cpu().numpy().T
