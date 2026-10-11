import argparse
import sys
from pathlib import Path

from .pipeline import KeepVoiceError, parse_ranges, remove_music
from .separate import DialogueSeparator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="keepvoice",
        description="Remove music from a video, including songs with singing, and keep the speech.",
    )
    parser.add_argument("input", type=Path, help="video file")
    parser.add_argument(
        "-o", "--output", type=Path, help="output file (default: <input>_voice_only.mp4)"
    )
    parser.add_argument(
        "--mute",
        action="append",
        default=[],
        metavar="START-END",
        help="make this time range fully silent, for example 0-17 or 3:07-3:13.4; "
        "can be given more than one time",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="use 1 model checkpoint instead of 3: 3 times faster, lower quality",
    )
    args = parser.parse_args(argv)

    output = args.output or args.input.with_name(args.input.stem + "_voice_only.mp4")
    try:
        mute = parse_ranges(args.mute)
        remove_music(args.input, output, DialogueSeparator(fast=args.fast), mute)
    except (KeepVoiceError, ValueError) as error:
        print(f"keepvoice: {error}", file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
