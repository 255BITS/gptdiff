#!/usr/bin/env python3
"""
Command line tool to apply a unified diff directly to a file system.

Usage:
    gptapply --diff "<diff text>"
    or
    gptapply path/to/diff.patch

This tool uses the same patch-application logic as gptdiff.
"""

import sys
import argparse
from pathlib import Path
from gptdiff.gptdiff import apply_diff


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Apply a unified diff to the file system using GPTDiff's patch logic."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--diff",
        type=str,
        help="Unified diff text to apply (provide as a string)."
    )
    group.add_argument(
        "diff_file",
        nargs="?",
        help="Path to a file containing the unified diff."
    )
    parser.add_argument(
        "--project-dir",
        type=str,
        default=".",
        help="Project directory where the diff should be applied (default: current directory)."
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.diff:
        diff_text = args.diff
    else:
        diff_path = Path(args.diff_file)
        if not diff_path.exists():
            print(f"Error: Diff file '{args.diff_file}' does not exist.")
            sys.exit(1)
        diff_text = diff_path.read_text(encoding="utf8")

    project_dir = args.project_dir
    success = apply_diff(project_dir, diff_text)
    if success:
        print("✅ Diff applied successfully.")
    else:
        print("❌ Failed to apply diff.")


if __name__ == "__main__":
    main()
