from keepvoice.cli import main


def test_missing_input_gives_exit_code_1_and_a_clear_message(tmp_path, capsys):
    code = main([str(tmp_path / "nope.mp4")])
    assert code == 1
    assert "not found" in capsys.readouterr().err


def test_invalid_mute_range_gives_exit_code_1_and_names_the_range(video, capsys):
    code = main([str(video), "--mute", "9-3"])
    assert code == 1
    assert "9-3" in capsys.readouterr().err
