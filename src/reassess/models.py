from dataclasses import dataclass


@dataclass(frozen=True)
class Ply:
    number: int
    piece: str  # Standart chess notation
    san: str
    uci: str
    fen_before: str
    fen_after: str

    @property
    def is_white(self) -> bool:
        return self.piece.isupper()


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
