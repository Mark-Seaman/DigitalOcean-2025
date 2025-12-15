#!/usr/bin/env python3
"""
list_newest_files.py
Lists the 50 newest files in a directory tree, excluding anything
inside a .git subtree.
"""

import os
from pathlib import Path


def list_newest_files(root_dir=".", limit=50):
    root = Path(root_dir)
    files = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip .git directories
        if ".git" in dirnames:
            dirnames.remove(".git")

        for fname in filenames:
            fpath = Path(dirpath) / fname
            try:
                mtime = fpath.stat().st_mtime
                files.append((mtime, fpath))
            except FileNotFoundError:
                continue

    # Sort newest first
    files.sort(reverse=True, key=lambda x: x[0])

    # Take top N
    for _, f in files[:limit]:
        print(f)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        list_newest_files(sys.argv[1])
    else:
        list_newest_files(".")
