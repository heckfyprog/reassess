# Import/Export games

from collections.abc import Sequence
from pathlib import Path

import chess
import chess.pgn

from reassess.models import FullMove, GameRecord, Ply


def import_game_from_pgn_file(path: Path) -> chess.pgn.Game:
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


def group_into_full_moves(plies: Sequence[Ply], start_number: int = 1) -> tuple[FullMove, ...]:
    """Group plies into full moves (white + black pair).

    Handles games started with Black's move and an unfinished last move.
    """
    full_moves: list[FullMove] = []
    number = start_number
    i = 0

    if plies and not plies[0].is_white:
        full_moves.append(FullMove(number, None, plies[0]))
        number += 1
        i = 1

    while i < len(plies):
        black = plies[i + 1] if i + 1 < len(plies) else None
        full_moves.append(FullMove(number, plies[i], black))
        number += 1
        i += 2

    return tuple(full_moves)


def to_record_game(game: chess.pgn.Game) -> GameRecord:
    """Convert a game tree into an immutable GameRecord.

    Args:
          game: Source game tree to convert.
    Returns:
          Normilized 'GameRecord' containing PGN headers and sequential plies.
    """
    headers = game.headers
    board = game.board()
    start_number = board.fullmove_number
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

    moves = group_into_full_moves(plies, start_number)
    return GameRecord(headers=dict(headers), plies=tuple(plies), moves=moves)
