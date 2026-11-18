# Import/Export games

from pathlib import Path

import chess.pgn


def import_game_from_pgn(path: Path) -> chess.pgn.Game:
    with path.open(encoding="utf-8") as f:
        game = chess.pgn.read_game(f)
    if game is None:
        raise ValueError(f"There is no games in file {path}")
    return game
