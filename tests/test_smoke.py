import shutil

import chess
import chess.engine
import pytest


def test_python_chess_works() -> None:
    assert len(list(chess.Board().legal_moves)) == 20


@pytest.mark.skipif(shutil.which("stockfish") is None, reason="stockfish not installed")
def test_stockfish_answers() -> None:
    with chess.engine.SimpleEngine.popen_uci("stockfish") as engine:
        info = engine.analyse(chess.Board(), chess.engine.Limit(depth=8))
        assert "score" in info
