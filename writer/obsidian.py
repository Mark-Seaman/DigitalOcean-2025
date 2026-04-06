from pathlib import Path
from shutil import copy
from publish.files import read_json


# Use template to render HTML cover
def render_cover_html(pub):
    # Copy artwork to static images
    pub_cover = pub_path(pub) / 'dev' / 'cover' / f'{pub}.png'
    static_file = "static/images/Cover.png"
    if pub_cover.exists():
        copy(pub_cover, static_file)
        print(f"Copied cover image from {pub_cover} to {static_file}")
    else:
        print(f"Cover image not found at {pub_cover}, using default.")


def obsidian_cover():
    # Read the JSON data for the publication
    pub = 'becoming'
    json = pub_path(pub) / 'dev' / f'{pub}.json'
    data = read_json(json)
    if not data:
        print(f"Invalid JSON structure in: {json}")
        return
    # print(f"Publication Data: {data}")
    print(f"Title: {data.get('title', 'Untitled')}")
    print(f"Subtitle: {data.get('subtitle', '')}")
    print(f"Author: {data.get('author', 'Mark Seaman')}")
    print(f"Cover Image: {data.get('cover-image', '')}")
    print(f"Publication Path: {data.get('pub-path', '')}")
    render_cover_html(pub)
    print(f"https://localhost:8000/cover/{pub}")


def pub_path(pub):
    forge_dir = Path("Obsidian/forge")
    if not forge_dir.exists():
        return None

    # Look through all series directories in forge
    for series_dir in forge_dir.iterdir():
        if series_dir.is_dir():
            pub_path = series_dir / pub
            # Check if the publication has the required JSON file
            json_file = pub_path / "dev" / f"{pub}.json"
            if json_file.exists():
                return pub_path
    return None
