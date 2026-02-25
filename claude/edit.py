#!/usr/bin/env python3
"""Automated text editor using Claude.

Reads a file, applies a named transform, shows a diff, and rewrites
the file only after user confirmation.

Usage:
    python edit.py <file_path> <transform_name> [--direct]

Transforms are defined as markdown files in the ./transforms/ directory.

Flags:
    --direct    Unsets CLAUDECODE so the subprocess can run from inside a
                Claude Code session (safe for non-interactive claude -p calls).

Examples:
    python edit.py ~/Obsidian/notes/draft.md grammar
    python edit.py ~/Obsidian/notes/draft.md grammar --direct
    python edit.py ~/Obsidian/notes/draft.md friendly
"""

import os
import subprocess
import sys
import difflib
from pathlib import Path

TRANSFORMS_DIR = Path(__file__).parent / "transforms"


def load_transform(name: str) -> str:
    transform_file = TRANSFORMS_DIR / f"{name}.md"
    if not transform_file.exists():
        available = sorted(p.stem for p in TRANSFORMS_DIR.glob("*.md"))
        print(f"Error: Transform '{name}' not found.")
        print(f"Available transforms: {', '.join(available)}")
        sys.exit(1)
    return transform_file.read_text().strip()


def strip_fences(text: str) -> str:
    """Remove markdown code fences if Claude wrapped the output."""
    lines = text.strip().splitlines()
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1] == "```":
        return "\n".join(lines[1:-1])
    return text.strip()


def apply_transform(content: str, instructions: str, direct: bool = False) -> str:
    prompt = (
        f"{instructions}\n\n"
        "Apply these instructions to the following text. "
        "Return ONLY the transformed text — no preamble, explanation, or commentary.\n\n"
        f"---\n{content}\n---"
    )

    env = os.environ.copy()
    if direct:
        env.pop("CLAUDECODE", None)

    print("Applying transform...")
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)

    return strip_fences(result.stdout)


def show_diff(original: str, revised: str, filename: str) -> bool:
    """Print a unified diff. Returns True if there are changes."""
    original_lines = original.splitlines(keepends=True)
    revised_lines = revised.splitlines(keepends=True)

    diff = list(difflib.unified_diff(
        original_lines,
        revised_lines,
        fromfile=f"{filename} (original)",
        tofile=f"{filename} (revised)",
        lineterm="",
    ))

    if not diff:
        print("No changes detected.")
        return False

    print("\n--- DIFF ---")
    for line in diff:
        print(line)
    print("--- END DIFF ---\n")
    return True


def confirm_apply() -> bool:
    while True:
        response = input("Apply changes? [y/N] ").strip().lower()
        if response in ("y", "yes"):
            return True
        if response in ("", "n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    direct = "--direct" in sys.argv

    if len(args) < 2:
        print("Usage: python edit.py <file_path> <transform_name> [--direct]\n")
        if TRANSFORMS_DIR.exists():
            available = sorted(p.stem for p in TRANSFORMS_DIR.glob("*.md"))
            print(f"Available transforms: {', '.join(available)}")
        sys.exit(1)

    file_path = Path(args[0]).expanduser().resolve()
    transform_name = args[1]

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    original_content = file_path.read_text()
    instructions = load_transform(transform_name)

    revised_content = apply_transform(original_content, instructions, direct=direct)

    has_changes = show_diff(original_content, revised_content, file_path.name)

    if not has_changes:
        return

    if confirm_apply():
        file_path.write_text(revised_content)
        print(f"Changes applied to: {file_path}")
    else:
        print("Changes discarded.")


if __name__ == "__main__":
    main()
