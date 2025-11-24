from __future__ import annotations

import argparse
import sys
from typing import Sequence

from .load import read_file, read_gcs, read_stdin
from .parse import parse_stream
from .types import StreamLike


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="parser",
    )

    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        "-f",
        "--file",
        metavar="PATH",
        help="Read XML from a local file path.",
    )
    source_group.add_argument(
        "-u",
        "--url",
        metavar="URL",
        help="Read XML from a public URL (http/s only, no gs://).",
    )
    source_group.add_argument(
        "-s",
        "--stdin",
        action="store_true",
        help="Explicitly read XML from stdin (default when no other source is provided).",
    )

    return parser


def _resolve_source(args: argparse.Namespace) -> StreamLike:
    if args.file:
        return read_file(args.file)
    if args.url:
        return read_gcs(args.url)
    return read_stdin()


def _print_result(doc_numbers: list[str]) -> None:
    print(doc_numbers)


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        source = _resolve_source(args)
        doc_numbers = parse_stream(source)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    _print_result(doc_numbers)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
