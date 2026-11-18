# Import/Export games

from pathlib import Path

import chess
import chess.pgn

from reassess.models import FullMove, GameRecord, Ply


def import_game_from_pgn(path: Path) -> chess.pgn.Game:
    with path.open(encoding="utf-8") as f:
        game = chess.pgn.read_game(f)
    if game is None:
        raise ValueError(f"There is no games in file {path}")
    return game


def to_record_game(game: chess.pgn.Game) -> GameRecord:
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
        plies.append(Ply(len(plies) + 1, piece, san, move.uci(), fen_before, fen_after))

    full_moves: list[FullMove] = []

    game_record = GameRecord(headers=dict(headers), plies=tuple(plies), moves=tuple(full_moves))
    return game_record
