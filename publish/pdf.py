import os
import subprocess
from datetime import datetime

# -------- Config --------
TITLE = "Friendship"
SUBTITLE = "Healthy and Thriving"
AUTHOR = "Mark Seaman"
LANG = "en"
DATE = datetime.now().strftime("%Y-%m-%d")
EPUB = "../../books/Friendship.epub"
PDF = "../../books/Friendship.pdf"
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

# -------- Build PDF --------
PDF_ARGS = [
    "pandoc",
    "--pdf-engine=xelatex",
    "-o", PDF,
    "Cover.md",
] + CONTENT_FILES


def build_pdf():
    def has_xelatex():
        from shutil import which
        return which("xelatex") is not None

    if has_xelatex():
        print(f"Building {PDF} ...")
        print(" ".join(PDF_ARGS))
        subprocess.run(PDF_ARGS, check=True)
        subprocess.run(["open", PDF])
        print(f"Done with {PDF}")
    else:
        print("Skipping PDF (xelatex not found).")
