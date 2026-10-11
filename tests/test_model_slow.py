import numpy as np
import pytest

from keepvoice.separate import DialogueSeparator


@pytest.mark.slow
def test_real_model_returns_a_stem_of_the_same_shape_and_removes_a_pure_tone():
    rate = 44100
    t = np.arange(rate * 5) / rate
    tone = 0.2 * np.sin(2 * np.pi * 440 * t)
    audio = np.stack([tone, tone], axis=1).astype(np.float32)
    speech = DialogueSeparator(fast=True)(audio, rate)
    assert speech.shape == audio.shape
    assert np.mean(speech**2) < 0.01 * np.mean(audio**2)
