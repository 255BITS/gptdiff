#!/usr/bin/env python3
"""
Generate *planprompt.txt* that tells an LLM to run **gptdiff** on only the files
that matter.

Workflow
--------
1. Accept the natural‑language command you would normally give *plan*.
2. Use **ripgrep** (`rg`) to locate files whose **paths** *or* **contents**
   match keywords from the command.
3. Always include any file whose path contains “schema”.
4. Build a `gptdiff` command pre‑populated with those files.
5. Write a ready‑to‑paste prompt to **planprompt.txt** –
   just like `gptdiff` does with *prompt.txt*.
"""

from __future__ import annotations

import argparse
import os
import re
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import List, Set
from gptdiff.gptdiff import load_gitignore_patterns, is_ignored

# LLM helpers
import json
from gptdiff.gptdiff import call_llm, domain_for_url


# --------------------------------------------------------------------------- #
# Keyword extraction via LLM                                                  #
# --------------------------------------------------------------------------- #

def _unique(seq: List[str]) -> List[str]:
    """Preserve order while removing duplicates."""
    seen: Set[str] = set()
    out: List[str] = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _parse_keywords(requirement: str) -> List[str]:
    """
    Ask the configured **GPTDIFF_MODEL** LLM to emit the most relevant, UNIQUE
    search terms for *ripgrep*.

    Fallback: returns simple heuristics if no API key is configured or the call
    fails.
    """
    api_key = os.getenv("GPTDIFF_LLM_API_KEY")
    model = os.getenv("GPTDIFF_MODEL", "deepseek-reasoner")
    base_url = os.getenv("GPTDIFF_LLM_BASE_URL", "https://nano-gpt.com/api/v1/")

    # Heuristic fallback when no key available
    if not api_key:
        return _unique(
            [w.lower() for w in re.findall(r"[A-Za-z_]{4,}", requirement)]
        )

    system_prompt = (
        "You are an expert software search assistant.\n"
        "Given a natural‑language coding requirement, output **only** a JSON "
        "array of 3‑10 UNIQUE, lowercase keywords that will best locate the "
        "relevant source files. Exclude common stop‑words and keep each keyword "
        "to a single token if possible."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": requirement},
    ]

    try:
        response = call_llm(
            api_key=api_key,
            base_url=base_url,
            model=model,
            messages=messages,
            max_tokens=128,
            temperature=0.0,
        )
        content = response.choices[0].message.content.strip()

        # In case the model adds commentary, grab the first JSON array found.
        json_start = content.find("[")
        json_end = content.rfind("]")
        if json_start == -1 or json_end == -1:
            raise ValueError("No JSON array detected.")

        keywords = json.loads(content[json_start : json_end + 1])
        if not isinstance(keywords, list):
            raise ValueError("Expected a JSON list of keywords.")

        return _unique([str(k).lower() for k in keywords])

    except Exception as e:  # noqa: BLE001
        # Print a hint and fall back to heuristic extraction.
        print(
            f"\033[33m⚠️  Keyword LLM extraction failed ({e}); "
            "falling back to simple parsing.\033[0m"
        )
        return _unique(
            [w.lower() for w in re.findall(r"[A-Za-z_]{4,}", requirement)]
        )


def _rg(arguments: List[str]) -> Set[str]:
    """Thin wrapper around ripgrep – returns an *empty* set if rg isn’t present."""
    if not shutil.which("rg"):
        return set()

    completed = subprocess.run(
        ["rg", "--follow", "--no-config", "--color", "never"] + arguments,
        check=False,
        capture_output=True,
        text=True,
    )
    return {p for p in completed.stdout.splitlines() if p}


def find_relevant_files(keywords: List[str], include_schema: bool = True) -> List[str]:
    """Locate files worth passing to gptdiff."""
    files: Set[str] = set()

    # 1. Path matches
    for kw in keywords:
        files |= _rg(["-i", "-g", f"*{kw}*"])

    # 2. Content matches
    for kw in keywords:
        files |= _rg(["-i", "--files-with-matches", kw])

    # 3. Anything with “schema” in the path
    if include_schema:
        files |= _rg(["-i", "-g", "*schema*"])

    return sorted(files)


def build_gptdiff_command(cmd: str, files: List[str], apply: bool) -> str:
    pieces = ["gptdiff", shlex.quote(cmd)]
    if files:
        pieces.append("--files " + " ".join(shlex.quote(f) for f in files))
    if apply:
        pieces.append("--apply")
    return " ".join(pieces)


# --------------------------------------------------------------------------- #
# CLI                                                                         #
# --------------------------------------------------------------------------- #


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="plangptdiff",
        description="Create planprompt.txt that invokes gptdiff on relevant files.",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="The natural‑language instruction you would normally give plan.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Add --apply to the generated gptdiff command.",
    )
    args = parser.parse_args()

    if not args.command:
        parser.error("You must provide a command, e.g.  plangptdiff 'add logging'")

    original_cmd = " ".join(args.command).strip()
    keywords = _parse_keywords(original_cmd)
    files = find_relevant_files(keywords)

    # Exclude prompt.txt and any files listed in .gitignore or .gptignore
    ignore_patterns: List[str] = []
    cwd = Path.cwd()
    gitignore_path = cwd / ".gitignore"
    gptignore_path = cwd / ".gptignore"
    if gitignore_path.exists():
        ignore_patterns.extend(load_gitignore_patterns(str(gitignore_path)))
    if gptignore_path.exists():
        ignore_patterns.extend(load_gitignore_patterns(str(gptignore_path)))
    # Always ignore prompt.txt explicitly
    ignore_patterns.append("prompt.txt")
    # Filter out ignored files
    files = [f for f in files if not is_ignored(f, ignore_patterns)]

    gptdiff_cmd = build_gptdiff_command(original_cmd, files, args.apply)

    prompt = f"""You are working in a repository where **gptdiff** is installed.
Run the command below to implement the requested change:

```bash
{gptdiff_cmd}
```"""

    Path("planprompt.txt").write_text(prompt, encoding="utf8")
    print(f"📝  planprompt.txt written – {len(files)} file(s) included.")


if __name__ == "__main__":
    main()