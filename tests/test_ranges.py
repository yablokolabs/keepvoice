import pytest

from keepvoice.pipeline import parse_ranges


def test_seconds_and_clock_times_become_seconds():
    assert parse_ranges(["0-17", "3:07-3:13.4", "1:00:00-1:00:01.5"]) == [
        (0.0, 17.0),
        (187.0, 193.4),
        (3600.0, 3601.5),
    ]


@pytest.mark.parametrize("text", ["17", "5-2", "3-3", "a-b", "1:xx-2", "-5"])
def test_invalid_range_is_rejected_with_the_bad_text_in_the_message(text):
    with pytest.raises(ValueError, match=text):
        parse_ranges([text])
