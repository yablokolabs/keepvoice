import pytest

from keepvoice.pipeline import KeepVoiceError, remove_music

from .conftest import audio_db, duration, make_video, passthrough, video_md5


def test_picture_is_copied_bit_for_bit_and_length_is_kept(video, tmp_path):
    out = tmp_path / "out.mp4"
    remove_music(video, out, passthrough)
    assert video_md5(out) == video_md5(video)
    assert duration(out) == pytest.approx(duration(video), abs=0.15)


def test_output_audio_is_what_the_separator_returned(video, tmp_path):
    out = tmp_path / "out.mp4"
    remove_music(video, out, lambda audio, rate: audio * 0.1)
    before = audio_db(video, 1, 5, tmp_path)
    after = audio_db(out, 1, 5, tmp_path)
    assert after == pytest.approx(before - 20, abs=1.5)


def test_muted_ranges_are_silent_and_the_rest_keeps_its_level(video, tmp_path):
    out = tmp_path / "out.mp4"
    remove_music(video, out, passthrough, mute=[(1.0, 2.0), (4.0, 5.0)])
    reference = audio_db(video, 2.3, 3.7, tmp_path)
    assert audio_db(out, 1.15, 1.85, tmp_path) < -80
    assert audio_db(out, 4.15, 4.85, tmp_path) < -80
    assert audio_db(out, 2.3, 3.7, tmp_path) == pytest.approx(reference, abs=1.5)


def test_mute_range_past_the_end_of_the_video_is_accepted(video, tmp_path):
    out = tmp_path / "out.mp4"
    remove_music(video, out, passthrough, mute=[(5.0, 99.0)])
    assert audio_db(out, 5.2, 5.8, tmp_path) < -80
    assert duration(out) == pytest.approx(duration(video), abs=0.15)


def test_mono_input_is_processed(tmp_path):
    src = make_video(tmp_path / "mono.mp4", channels=1)
    out = tmp_path / "out.mp4"
    remove_music(src, out, passthrough)
    assert audio_db(out, 1, 5, tmp_path) == pytest.approx(audio_db(src, 1, 5, tmp_path), abs=1.5)


def test_video_without_audio_is_refused(tmp_path):
    src = make_video(tmp_path / "silent.mp4", audio=False)
    with pytest.raises(KeepVoiceError, match="no audio"):
        remove_music(src, tmp_path / "out.mp4", passthrough)


def test_output_path_equal_to_input_is_refused_and_input_is_untouched(video):
    size = video.stat().st_size
    with pytest.raises(KeepVoiceError, match="same file"):
        remove_music(video, video, passthrough)
    assert video.stat().st_size == size


def test_missing_input_is_refused(tmp_path):
    with pytest.raises(KeepVoiceError, match="not found"):
        remove_music(tmp_path / "nope.mp4", tmp_path / "out.mp4", passthrough)
