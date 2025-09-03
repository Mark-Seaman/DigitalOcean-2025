from django.core.management.base import BaseCommand

from publish.epub import build_epub
from publish.pdf import build_pdf
from publish.order import build_pub, json_path, pub_path, read_json, create_json, list_contents, save_contents, count_words, show_contents


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
            build_pub(pub, self)
        elif action == 'cover':
            self.handle_cover(pub)
        elif action == 'words':
            self.handle_words(pub)
        elif action == 'content':
            self.handle_content(pub)
        else:
            self.stdout.write(self.style.ERROR(f"Unknown action: {action}"))

    def handle_json(self, pub):
        json_file = json_path(pub)
        json_file.parent.mkdir(parents=True, exist_ok=True)
        if not json_file.exists():
            create_json(json_file)
            self.stdout.write(self.style.SUCCESS(
                f"Created JSON file: {json_file}"))
        else:
            data = read_json(json_file)
            self.stdout.write(self.style.SUCCESS(
                f"JSON file already exists: {json_file}\nContents: {data}"))

    # def handle_build(self, pub):
    #     from pathlib import Path
    #     pub_dir = Path("Obsidian/public/guides") / pub
    #     if not pub_dir.exists():
    #         self.stdout.write(self.style.ERROR(
    #             f"Publication path does not exist: {pub_dir}"))
    #         return
    #     build_pdf(pub_dir)
    #     build_epub(pub_dir)

    def handle_cover(self, pub):
        # Placeholder for cover action logic
        self.stdout.write(self.style.SUCCESS(f"Cover action for pub: {pub}"))

    def handle_words(self, pub):
        def writer(msg, error=False, success=False):
            if error:
                self.stdout.write(self.style.ERROR(msg))
            elif success:
                self.stdout.write(self.style.SUCCESS(msg))
            else:
                self.stdout.write(msg)
        from publish.order import show_words
        show_words(pub, writer=writer)

    def handle_content(self, pub):
        content = show_contents(pub)
        self.stdout.write(self.style.SUCCESS(
            f"Pub Content: {pub}\n{content}"))
