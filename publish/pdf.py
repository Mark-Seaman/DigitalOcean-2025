import os
import subprocess
from datetime import datetime

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
        book = json_data.get('book', 'BOOK not found') + '.pdf'

    def quote(arg):
        if ' ' in str(arg) or any(c in str(arg) for c in '"\''):
            return f'"{arg}"'
        return str(arg)

    pdf_cmd = [
        'pandoc',
        '--pdf-engine=xelatex',
        '-o', quote(book),
        'Cover.md',
        'Contents.md',
    ] + [quote(f) for f in content_files]

    with open(script_path, 'w') as f:
        f.write('#!/bin/bash\n')
        f.write(f'# Build PDF for {pub_path.name} using Pandoc\n\n')
        f.write(f'cd {pub_path}\n\n')
        f.write('pandoc \\\n')
        for arg in pdf_cmd[1:-len(content_files)]:
            f.write(f'  {arg} \\\n')
        for i, mdfile in enumerate(pdf_cmd[-len(content_files):]):
            if i == len(content_files) - 1:
                f.write(f'  {mdfile}\n')
            else:
                f.write(f'  {mdfile} \\\n')
                f.write(f'  ../../page.md \\\n')
        success = f'''

# Check for errors and report
if [ $? -eq 0 ]; then
    echo "PDF built successfully:"
    echo open {book}
    open {book}
else
    echo "Error building PDF."
fi

        '''
        f.write(f'\n{success}\n')
    os.chmod(script_path, 0o755)
    print(f"\nWrote build script: \n{script_path}\n")
