"""Run any portfolio application from the command line."""
import argparse
import json
from pathlib import Path
from portfolio.registry import SLUGS, load, execute


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", choices=SLUGS)
    parser.add_argument("--live", action="store_true", help="Use your configured Foundry deployment; incurs usage charges")
    parser.add_argument("--text", help="Override demo input")
    parser.add_argument("--input", type=Path, help="Read editable input from a UTF-8 text file")
    parser.add_argument("--as-of", help="Reference date for date-based workflows (YYYY-MM-DD)")
    args = parser.parse_args()
    if args.text is not None and args.input:
        parser.error("Choose --text or --input")
    try:
        text = args.input.read_text() if args.input else args.text
        payload = {"text": text if text is not None else load(args.project).SPEC["example_input"]}
        if args.as_of:
            payload["as_of"] = args.as_of
        print(json.dumps(execute(args.project, payload, args.live), indent=2, ensure_ascii=False))
    except Exception as exc:
        from portfolio.ai import AIError
        if isinstance(exc, (AIError, ValueError, OSError)):
            parser.exit(1, f"Unable to complete: {exc}\n")
        raise


if __name__ == "__main__":
    main()
