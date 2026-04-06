import os
import subprocess
from datetime import datetime
from pathlib import Path

DATE = datetime.now().strftime("%Y-%m-%d")
CSS_FILE = "epub.css"


def build_pdf(pub_path):
    from publish.management.commands.order import read_json

    script_dir = pub_path / 'dev'
    script_dir.mkdir(parents=True, exist_ok=True)
    script_path = script_dir / 'build-pdf.sh'
    json_path = script_dir / f'{pub_path.name}.json'

    # Try to get CONTENT_FILES from JSON if available
    json_data = read_json(json_path)
    if json_data:
        content_files = json_data.get('contents', 'CONTENTS not found')
        book_path = json_data.get('book', 'BOOK not found') + '.pdf'

        # Convert to absolute paths to avoid directory change issues
        hammer_root = Path.cwd()
        abs_book_path = hammer_root / book_path
        abs_pub_path = hammer_root / pub_path

    def quote(arg):
        if ' ' in str(arg) or any(c in str(arg) for c in '"\''):
            return f'"{arg}"'
        return str(arg)

    pdf_cmd = [
        'pandoc',
        '--pdf-engine=xelatex',
        '-o', str(abs_book_path),
        str(abs_pub_path / 'Cover.md'),
        str(abs_pub_path / 'Contents.md'),
    ]

    # Add content files with page breaks
    for f in content_files:
        pdf_cmd.append(str(abs_pub_path / f))
        pdf_cmd.append(str(hammer_root / 'Obsidian/forge/page.md'))

    # Remove the last page break
    pdf_cmd.pop()

    with open(script_path, 'w') as f:
        f.write('#!/bin/bash\n')
        f.write(f'# Build PDF for {pub_path.name} using Pandoc\n\n')
        f.write('# Using absolute paths to avoid directory change issues\n')
        f.write(' '.join(quote(arg) for arg in pdf_cmd))
        f.write('\n\n')

        success = f'''
# Check for errors and report
if [ $? -eq 0 ]; then
    echo "PDF built successfully:"
    echo "open {abs_book_path}"
    open "{abs_book_path}"
else
    echo "Error building PDF."
fi
'''
        f.write(success)
    os.chmod(script_path, 0o755)
    print(f"\nWrote build script: \n{script_path}\n")
