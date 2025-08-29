import os
from pathlib import Path
from publish.pdf import PDF_ARGS
from datetime import datetime
import subprocess


def read_json(file_path):
    import json
    from pathlib import Path
    file_path = Path(file_path)
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return None


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


def build_epub(pub_path):

    script_dir = pub_path / '.dev'
    script_dir.mkdir(parents=True, exist_ok=True)
    script_path = script_dir / 'build-epub.sh'
    json_path = script_dir / 'friendship.json'

    # Try to get CONTENT_FILES from JSON if available
    json_data = read_json(json_path)
    if json_data and 'contents' in json_data:
        content_files = json_data['contents']
    else:
        content_files = CONTENT_FILES

    def quote(arg):
        if ' ' in str(arg) or any(c in str(arg) for c in '"\''):
            return f'"{arg}"'
        return str(arg)

    epub_cmd = [
        'pandoc',
        '--strip-comments',
        '--standalone',
        '--epub-cover-image', quote(COVER_IMAGE),
        '--css', quote(CSS_FILE),
        '--metadata', f'author={quote(AUTHOR)}',
        '--metadata', f'title={quote(TITLE)}',
        '--metadata', f'subtitle={quote(SUBTITLE)}',
        '--metadata', f'date={quote(DATE)}',
        '-o', quote(EPUB)
    ] + [quote(f) for f in content_files]
    with open(script_path, 'w') as f:
        f.write('#!/bin/bash\n')
        f.write('# Build EPUB for Friendship using Pandoc\n\n')
        f.write(f'cd {pub_path}\n\n')
        f.write('pandoc \\\n')
        for arg in epub_cmd[1:-len(content_files)]:
            f.write(f'  {arg} \\\n')
        for i, mdfile in enumerate(epub_cmd[-len(content_files):]):
            if i == len(content_files) - 1:
                f.write(f'  {mdfile}\n')
            else:
                f.write(f'  {mdfile} \\\n')
        f.write(f'open {quote(EPUB)}\n')
    os.chmod(script_path, 0o755)
    print(f"Wrote build script: {script_path}")
