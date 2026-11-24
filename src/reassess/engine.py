import chess
import chess.engine

from reassess.models import GameAnalysis, GameRecord, PlyAnalysis


def evaluate_accuracy(plies: tuple[PlyAnalysis, ...], ) -> float:
    result = 0.0
    return result


def analyze_game(record: GameRecord) -> GameAnalysis:

    ply_analysis: list[PlyAnalysis] = []

    for ply in record.plies:
        ply_analysis.append(PlyAnalysis(ply, "0", "0", 0, "!"))

    white_accuracy = evaluate_accuracy(tuple(ply_analysis))
    black_accuracy = evaluate_accuracy(tuple(ply_analysis))

    game_analysis = GameAnalysis(
        mainline=record,
        ply_analyses=tuple(ply_analysis),
        white_accuracy=white_accuracy,
        black_accuracy=black_accuracy
    )

    return game_analysis
