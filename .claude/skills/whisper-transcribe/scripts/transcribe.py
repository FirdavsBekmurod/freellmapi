#!/usr/bin/env python3
"""Transcribe or translate an audio/video file with OpenAI Whisper.

Usage:
    python transcribe.py INPUT [--model base] [--language ru] [--task transcribe|translate]
                         [--format txt|srt|vtt|json|all] [--out-dir DIR]

Writes INPUT-stem.<format> into --out-dir (default: next to the input file)
and prints the plain text to stdout.
"""
import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="audio or video file (anything ffmpeg can read)")
    p.add_argument("--model", default="base",
                   help="tiny, base, small, medium, large-v3, turbo (default: base)")
    p.add_argument("--language", default=None,
                   help="language code like ru, en, uz; omit to auto-detect")
    p.add_argument("--task", choices=["transcribe", "translate"], default="transcribe",
                   help="translate = output English text")
    p.add_argument("--format", choices=["txt", "srt", "vtt", "json", "all"], default="txt")
    p.add_argument("--out-dir", default=None)
    args = p.parse_args()

    src = Path(args.input)
    if not src.is_file():
        print(f"error: file not found: {src}", file=sys.stderr)
        return 2

    try:
        import whisper
        from whisper.utils import get_writer
    except ImportError:
        print("error: whisper is not installed. Run: pip install -U openai-whisper "
              "(ffmpeg must also be installed)", file=sys.stderr)
        return 3

    out_dir = Path(args.out_dir) if args.out_dir else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    model = whisper.load_model(args.model)
    result = model.transcribe(str(src), language=args.language, task=args.task, verbose=False)

    formats = ["txt", "srt", "vtt", "json"] if args.format == "all" else [args.format]
    for fmt in formats:
        get_writer(fmt, str(out_dir))(result, str(src), {
            "max_line_width": None, "max_line_count": None, "highlight_words": False,
        })
        print(f"wrote {out_dir / (src.stem + '.' + fmt)}", file=sys.stderr)

    print(result["text"].strip())
    print(json.dumps({"language": result.get("language")}), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
