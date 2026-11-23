import pytest

pytest.importorskip("modal")

from keepvoice.modal_app import cli_args  # noqa: E402


def test_no_options():
    assert cli_args(False, "") == []


def test_fast_and_mute_ranges():
    assert cli_args(True, "0-17, 3:07-3:13.4") == [
        "--fast",
        "--mute",
        "0-17",
        "--mute",
        "3:07-3:13.4",
    ]


def test_bad_range_fails_before_upload():
    with pytest.raises(ValueError):
        cli_args(False, "17-5")
