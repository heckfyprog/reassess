from dataclasses import dataclass

import chess
import chess.pgn


@dataclass(frozen=True)
class Ply:
    number: int
    piece: chess.Piece
    san: str
    uci: str
    fen_before: str
    fen_after: str


@dataclass(frozen=True)
class FullMove:
    number: int
    white_ply: Ply | None
    black_ply: Ply | None


@dataclass(frozen=True)
class GameRecord:
    headers: dict[str, str]
    plies: tuple[Ply, ...]
    moves: tuple[FullMove, ...]
