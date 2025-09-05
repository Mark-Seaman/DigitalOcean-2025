import os
from datetime import datetime


DATE = datetime.now().strftime("%Y-%m-%d")
CSS_FILE = "../../epub.css"


def build_epub(pub_path):
    from publish.management.commands.order import read_json

    script_dir = pub_path / 'dev'
    script_dir.mkdir(parents=True, exist_ok=True)
    script_path = script_dir / 'build-epub.sh'
    json_path = script_dir / f'{pub_path.name}.json'

    # Try to get CONTENT_FILES from JSON if available
    json_data = read_json(json_path)
    if json_data:
        content_files = json_data.get('contents', 'CONTENTS not found')
        author = json_data.get('author', 'AUTHOR not found')
        title = json_data.get('title', 'TITLE not found')
        subtitle = json_data.get('subtitle', 'SUBTITLE not found')
        cover_image = json_data.get('cover-image', 'COVER_IMAGE not found')
        book = json_data.get('book', 'BOOK not found') + '.epub'

    def quote(arg):
        if ' ' in str(arg) or any(c in str(arg) for c in '"\''):
            return f'"{arg}"'
        return str(arg)

    epub_cmd = [
        'pandoc',
        '--strip-comments',
        '--standalone',
        '--epub-cover-image', quote(cover_image),
        '--css', quote(CSS_FILE),
        '--metadata', f'author={quote(author)}',
        '--metadata', f'title={quote(title)}',
        '--metadata', f'subtitle={quote(subtitle)}',
        '--metadata', f'date={quote(DATE)}',
        '-o', quote(book),
        'Contents.md'
    ] + [quote(f) for f in content_files]

    with open(script_path, 'w') as f:
        f.write('#!/bin/bash\n')
        f.write(f'# Build EPUB for {pub_path.name} using Pandoc\n\n')
        f.write(f'cd {pub_path}\n\n')
        f.write('pandoc \\\n')
        for arg in epub_cmd[1:-len(content_files)]:
            f.write(f'  {arg} \\\n')
        for i, mdfile in enumerate(epub_cmd[-len(content_files):]):
            if i == len(content_files) - 1:
                f.write(f'  {mdfile}\n')
            else:
                f.write(f'  {mdfile} \\\n')
        success = f'''

# Check for errors and report
if [ $? -eq 0 ]; then
    echo "EPUB built successfully:"
    echo open {book}
    # open {book}
else
    echo "Error building EPUB."
fi

        '''
        f.write(f'\n{success}\n')
    os.chmod(script_path, 0o755)
    print(f"\nWrote build script: \n{script_path}\n")
