# Import/Export games

from pathlib import Path

import chess
import chess.pgn

from reassess.models import FullMove, GameRecord, Ply


def import_game_from_pgn(path: Path) -> chess.pgn.Game:
    """Load the first game from a UTF-8 encoded PGN file

    Args:
        ""path: Path to the source file.
        If the file contains multiple games, only the first game will be loaded"
    Returns:
          Parsed game tree from 'python-chess'.
    Raises:
          ValueError: If the file is empty or contains no valid PGN games.
          OSError: If the file cannot be opened or read.
    """
    with path.open(encoding="utf-8") as f:
        game = chess.pgn.read_game(f)
    if game is None:
        raise ValueError(f"There is no games in file {path}")
    return game


def to_record_game(game: chess.pgn.Game) -> GameRecord:
    """Convert a game tree into an immutable GameRecord.

    Args:
          game: Source game tree to convert.
    Returns:
          Normilized 'GameRecord' containing PGN headers and sequential plies.
    """
    headers = game.headers
    board = game.board()
    plies: list[Ply] = []

    for node in game.mainline():
        move = node.move
        piece = board.piece_at(move.from_square)
        assert piece is not None
        fen_before = board.fen()
        san = board.san(move)
        board.push(move)
        fen_after = board.fen()
        plies.append(Ply(len(plies) + 1, piece.symbol(), san, move.uci(), fen_before, fen_after))

    full_moves: list[FullMove] = []

    game_record = GameRecord(headers=dict(headers), plies=tuple(plies), moves=tuple(full_moves))
    return game_record
