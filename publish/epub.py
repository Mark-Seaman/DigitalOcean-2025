import os
import subprocess
from datetime import datetime

from publish.pdf import PDF_ARGS

# -------- Config --------
TITLE = "Friendship"
SUBTITLE = "Healthy and Thriving"
AUTHOR = "Mark Seaman"
LANG = "en"
DATE = datetime.now().strftime("%Y-%m-%d")
EPUB = "../books/Friendship.epub"
PDF = "../books/Friendship.pdf"
COVER_IMAGE = "Friendship.500.png"
CSS_FILE = "epub.css"

# -------- Input files (ordered) --------
CONTENT_FILES = [
    "1.md",
    "2.md",
    "3.md",
    "4.md",
    "5.md",
]

# -------- Build EPUB --------
EPUB_ARGS = [
    "pandoc",
    "--strip-comments",
    "--standalone",
    "--epub-cover-image", COVER_IMAGE,
    "--css", CSS_FILE,
    "--metadata", f"author={AUTHOR}",
    "--metadata", f"title={TITLE}",
    "--metadata", f"subtitle={SUBTITLE}",
    "--metadata", f"date={DATE}",
    "-o", EPUB,
] + CONTENT_FILES


def build_epub():

    def has_xelatex():
        from shutil import which
        return which("xelatex") is not None

    if has_xelatex():
        print(f"Building {EPUB} ...")
        print(" ".join(EPUB_ARGS))
        subprocess.run(EPUB_ARGS, check=True)
        subprocess.run(["open", EPUB])
        print(f"Done with {EPUB}")
    else:
        print("Skipping EPUB (xelatex not found).")
