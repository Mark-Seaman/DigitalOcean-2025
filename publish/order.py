from pathlib import Path
from publish.pdf import build_pdf
from publish.epub import build_epub
import json


def build_pub(pub, writer=None):
    json_file = json_path(pub)
    data = read_json(json_file)
    if not data or "contents" not in data:
        writer.stdout.write(writer.style.ERROR(
            f"Invalid JSON structure in: {json_file}"))
        return
    pub_dir = Path(data["pub-path"])
    if not pub_dir.exists():
        writer.stdout.write(writer.style.ERROR(
            f"Publication path does not exist: {pub_dir}"))
        return
    build_pdf(pub_dir)
    build_epub(pub_dir)


def count_words(pub):
    json_file = json_path(pub)
    data = read_json(json_file)
    if not data or "contents" not in data:
        return None, None, json_file
    pub_dir = Path(data["pub-path"])
    total_words = 0
    file_word_counts = []
    for rel_path in data["contents"]:
        md_path = pub_dir / rel_path
        if md_path.exists():
            with open(md_path, 'r', encoding='utf-8') as f:
                text = f.read()
                word_count = len(text.split())
                total_words += word_count
                file_word_counts.append((rel_path, word_count))
        else:
            file_word_counts.append((rel_path, None))
    pages = total_words // 250 + (1 if total_words % 250 else 0)
    return total_words, pages, file_word_counts


def create_json(file_path):
    pub_dir = file_path.parent.parent
    pub = pub_dir.name
    data = {
        "pub-path": str(pub_dir),
        "book": str(pub_dir.parent.parent / "books" / pub),
        "title": str(pub_dir.name),
        "subtitle": str(pub_dir.parent.name),
        "author": "Mark Seaman"
    }
    rel_md_files = list_contents(pub_dir)
    save_contents(pub, rel_md_files)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def json_path(pub):
    return pub_path(pub) / "dev" / f"{pub}.json"


def pub_path(pub):
    # if the guides directory does not exist, then try playbooks
    if (Path("Obsidian/forge/guides") / pub).exists():
        return Path("Obsidian/forge/guides") / pub
    return Path("Obsidian/forge/playbooks") / pub


def read_json(file_path):
    file_path = Path(file_path)
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return None


def list_contents(pub_dir):
    md_files = []
    for f in sorted(pub_dir.rglob("*.md")):
        if "dev" in f.parts or 'Cover.md' in f.parts or 'Title.md' in f.parts:
            continue
        md_files.append(f)
    return [str(f.relative_to(pub_dir)) for f in md_files]


def save_contents(pub, rel_md_files):
    json_file = json_path(pub)
    json_file.parent.mkdir(parents=True, exist_ok=True)
    data = read_json(json_file) or {}
    data["contents"] = rel_md_files
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)


def show_contents(pub):
    json_file = json_path(pub)
    data = read_json(json_file)
    if not data or "contents" not in data:
        return None, None, json_file
    return data["contents"]


def show_words(pub, writer=None):
    total_words, pages, file_word_counts = count_words(pub)
    output = []
    if total_words is None:
        if file_word_counts:
            msg = f"No contents found in {file_word_counts}. Run the build action first."
        else:
            msg = "No contents found. Run the build action first."
        if writer:
            writer(msg, error=True)
        else:
            print(msg)
        return
    for rel_path, word_count in file_word_counts:
        if word_count is not None:
            line = f"{rel_path}: {word_count} words"
        else:
            line = f"{rel_path}: File not found"
        if writer:
            writer(line)
        else:
            output.append(line)
    summary = f"Total words in {pub}: {total_words} (about {pages} pages)"
    if writer:
        writer(summary, success=True)
    else:
        output.append(summary)
        return output
