"""CLI for the File Integrity Monitor."""

import argparse
from pathlib import Path
from integrity_monitor import build_baseline, compare, load_baseline, save_baseline


def print_report(report):
    labels = [("ADDED", "added"), ("MODIFIED", "modified"), ("DELETED", "deleted")]
    changed = False
    for heading, key in labels:
        values = report[key]
        if values:
            changed = True
            print(f"\n{heading} ({len(values)}):")
            for name in values:
                print(f"  - {name}")
    print(f"\nUNCHANGED: {len(report['unchanged'])}")
    if not changed:
        print("No integrity changes detected.")


def main():
    parser = argparse.ArgumentParser(description="Defensive SHA-256 file-integrity monitor")
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="Create a new baseline")
    init_parser.add_argument("directory", help="Directory to monitor")
    init_parser.add_argument("-b", "--baseline", default="baseline.json")

    check_parser = sub.add_parser("check", help="Compare files with a baseline")
    check_parser.add_argument("directory", help="Directory to monitor")
    check_parser.add_argument("-b", "--baseline", default="baseline.json")

    args = parser.parse_args()
    directory = str(Path(args.directory).resolve())

    if args.command == "init":
        baseline = build_baseline(directory)
        save_baseline(baseline, args.baseline)
        print(f"Baseline created: {args.baseline}")
        print(f"Files recorded: {len(baseline)}")
    else:
        baseline = load_baseline(args.baseline)
        print_report(compare(directory, baseline))


if __name__ == "__main__":
    main()
