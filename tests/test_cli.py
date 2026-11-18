from pathlib import Path

from reassess.cli import main


def test_missing_file_returns_error(tmp_path: Path) -> None:
    assert main([str(tmp_path / "no.pgn")]) == 1
