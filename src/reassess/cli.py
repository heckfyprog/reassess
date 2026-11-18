# Main CLI

import argparse
import sys
from pathlib import Path

from reassess.games import import_game_from_pgn


def built_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reassess", description="Chess game analyzer")
    parser.add_argument("pgn", type=Path, help="Path to the PGN-file with game")
    parser.add_argument("--depth", type=int, default=10, help="Stockfish analysis depth")
    return parser


def get_position():
    return 0


def count_material():
    return 0


def main(argv: list[str] | None = None) -> int:
    args = built_parser().parse_args(argv)
    if not args.pgn.is_file():
        print(f"File not found: {args.pgn}", file=sys.stderr)
        return 1
    try:
        game = import_game_from_pgn(args.pgn)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    print(f"{game.headers.get('White', '?')} - {game.headers.get('Black', '?')}")
    return 0
