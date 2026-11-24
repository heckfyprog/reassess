# Main CLI

import argparse
import sys
from pathlib import Path

from reassess.engine import to_analyze_game
from reassess.games import import_game_from_pgn_file, to_record_game


def build_parser() -> argparse.ArgumentParser:
    """Create and configure the CLI argument parser"""
    parser = argparse.ArgumentParser(prog="reassess", description="Chess game analyzer")
    parser.add_argument("pgn", type=Path, help="Path to the PGN-file with game")
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=10,
        help="Stockfish analysis depth (default is %(default)s)",
    )
    parser.add_argument(
        "-f", "--format", choices=["text", "pgn", "json"], default="text", help="The output format"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.pgn.is_file():
        print(f"File not found: {args.pgn}", file=sys.stderr)
        return 1
    try:
        game = import_game_from_pgn_file(args.pgn)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    game_record = to_record_game(game)
    game_analysis = to_analyze_game(game_record)

    print(game_analysis)

    return 0
