import chess
import chess.pgn
import pytest

from reassess.games import group_into_full_moves, import_game_from_pgn_file, to_record_game
from reassess.models import Ply


class TestImportGames:
    def test_missing_file(self, tmp_path):
        missing_pgn = tmp_path / "missing.pgn"

        with pytest.raises(FileNotFoundError):
            import_game_from_pgn_file(missing_pgn)

    def test_empty_pgn_file(self, tmp_path):
        empty_pgn = tmp_path / "empty.pgn"
        empty_pgn.write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match="There is no games in file"):
            import_game_from_pgn_file(empty_pgn)

    def test_game_in_pgn_file(self, tmp_path):
        pgn_content = (
            '[Event "Casual Game"]\n'
            '[White "Player1"]\n'
            '[Black "Player2"]\n'
            '[Result "1-0"]\n\n'
            "1. e4 e5 2. Nf3 Nc6 1-0\n"
        )
        pgn_file = tmp_path / "game.pgn"
        pgn_file.write_text(pgn_content, encoding="utf-8")

        game = import_game_from_pgn_file(pgn_file)

        assert game.headers["White"] == "Player1"
        assert game.headers["Black"] == "Player2"
        assert game.headers["Result"] == "1-0"
        assert [move.uci() for move in game.mainline_moves()] == ["e2e4", "e7e5", "g1f3", "b8c6"]


class TestGroupIntoFullMoves:
    @staticmethod
    def make_ply(number: int, piece: str = "P", san: str = "e4", uci: str = "e2e4") -> Ply:
        return Ply(number, piece, san, uci, "fen_before", "fen_after")

    def test_missing_moves_game(self):
        plies: list[Ply] = []
        full_moves = group_into_full_moves(plies)
        assert len(full_moves) == 0

    def test_unfinished_last_move(self):
        plies: list[Ply] = []
        plies.append(self.make_ply(1))
        full_moves = group_into_full_moves(plies)
        assert len(full_moves) == 1
        assert full_moves[0].number == 1
        assert full_moves[0].black_ply is None

    def test_black_moves_first(self):
        plies: list[Ply] = [
            (self.make_ply(1, "p", "e5", "e7e5")),
            (self.make_ply(2, "P", "Nf3", "g1f3")),
            (self.make_ply(3, "p", "Nc6", "b8c6")),
        ]
        full_moves = group_into_full_moves(plies)

        assert full_moves[0].number == 1
        assert full_moves[0].white_ply is None
        assert full_moves[0].black_ply == plies[0]

        assert full_moves[1].number == 2
        assert full_moves[1].white_ply == plies[1]
        assert full_moves[1].black_ply == plies[2]


class TestRecordGames:
    def test_black_starts_game(self):
        board = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
        game = chess.pgn.Game()
        game.setup(board)
        game.add_variation(chess.Move.from_uci("e7e5"))

        record = to_record_game(game)

        assert len(record.plies) == 1
        assert record.plies[0].uci == "e7e5"
        assert record.plies[0].san == "e5"
        assert record.plies[0].piece == "p"

        assert len(record.moves) == 1
        assert record.moves[0].number == 1
        assert record.moves[0].white_ply is None
        assert record.moves[0].black_ply == record.plies[0]
