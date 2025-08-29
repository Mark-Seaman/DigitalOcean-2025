from django.core.management.base import BaseCommand
from publish.epub import build_epub


class Command(BaseCommand):
    help = 'Custom command to process orders.'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Action to perform')
        parser.add_argument('pub', type=str, help='Publication name or ID')

    def handle(self, *args, **options):
        action = options['action']
        pub = options['pub']

        if action == 'json':
            self.handle_json(pub)
        elif action == 'build':
            self.handle_build(pub)
        elif action == 'cover':
            self.handle_cover(pub)
        elif action == 'words':
            self.handle_words(pub)
        elif action == 'content':
            self.handle_content(pub)
        else:
            self.stdout.write(self.style.ERROR(f"Unknown action: {action}"))

    def handle_json(self, pub):
        json_file = self.json_path(pub)
        json_file.parent.mkdir(parents=True, exist_ok=True)
        if not json_file.exists():
            self.create_json(json_file)
            self.stdout.write(self.style.SUCCESS(
                f"Created JSON file: {json_file}"))
        else:
            data = self.read_json(json_file)
            self.stdout.write(self.style.SUCCESS(
                f"JSON file already exists: {json_file}\nContents: {data}"))

    def json_path(self, pub):
        from pathlib import Path
        pub_dir = Path("Obsidian/public/guides") / pub
        return pub_dir / ".dev" / f"{pub}.json"

    def create_json(self, file_path):
        import json
        pub_dir = file_path.parent.parent
        pub = pub_dir.name
        data = {
            "pub-path": str(pub_dir),
            "book": str(pub_dir.parent.parent / "books" / pub),
            "title": str(pub_dir.name),
            "subtitle": str(pub_dir.parent.name),
            "author": "Mark Seaman"
        }
        rel_md_files = self.list_contents(pub_dir)
        if rel_md_files:
            self.stdout.write(self.style.SUCCESS(
                f"Markdown files in {pub_dir}:"))
            for rel_path in rel_md_files:
                self.stdout.write(f"- {rel_path}")
        else:
            self.stdout.write(self.style.WARNING(
                f"No markdown files found in {pub_dir}"))
        # Update JSON file with contents
        self.save_contents(pub, rel_md_files)
        self.stdout.write(self.style.SUCCESS(
            f"Updated {self.json_path(pub)} with contents list."))
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def read_json(self, file_path):
        import json
        from pathlib import Path
        file_path = Path(file_path)
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return None

    def handle_build(self, pub):
        from pathlib import Path
        pub_dir = Path("Obsidian/public/guides") / pub
        if not pub_dir.exists():
            self.stdout.write(self.style.ERROR(
                f"Publication path does not exist: {pub_dir}"))
            return

        build_epub(pub_dir)

    def list_contents(self, pub_dir):
        md_files = []
        for f in sorted(pub_dir.rglob("*.md")):
            # Skip files in any .dev directory
            if ".dev" in f.parts or 'Cover.md' in f.parts or 'Title.md' in f.parts:
                continue
            md_files.append(f)
        return [str(f.relative_to(pub_dir)) for f in md_files]

    def save_contents(self, pub, rel_md_files):
        import json
        json_file = self.json_path(pub)
        json_file.parent.mkdir(parents=True, exist_ok=True)
        data = self.read_json(json_file) or {}
        data["contents"] = rel_md_files
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)

    def handle_cover(self, pub):
        # Placeholder for cover action logic
        self.stdout.write(self.style.SUCCESS(f"Cover action for pub: {pub}"))

    def handle_words(self, pub):
        from pathlib import Path
        json_file = self.json_path(pub)
        data = self.read_json(json_file)
        if not data or "contents" not in data:
            self.stdout.write(self.style.ERROR(
                f"No contents found in {json_file}. Run the build action first."))
            return
        # Count words in each markdown file
        pub_dir = Path(data["pub-path"])
        total_words = 0
        for rel_path in data["contents"]:
            md_path = pub_dir / rel_path
            if md_path.exists():
                with open(md_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    word_count = len(text.split())
                    total_words += word_count
            else:
                self.stdout.write(self.style.WARNING(
                    f"File not found: {md_path}"))
        pages = total_words // 250 + (1 if total_words % 250 else 0)
        self.stdout.write(self.style.SUCCESS(
            f"Total words in {pub}: {total_words} (about {pages} pages)"))

    def handle_content(self, pub):
        # Placeholder for content action logic
        self.stdout.write(self.style.SUCCESS(f"Content action for pub: {pub}"))
