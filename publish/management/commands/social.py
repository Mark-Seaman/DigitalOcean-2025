from django.core.management.base import BaseCommand

from brainchild.social import add_blog_pages, list_publications, scan_for_blog_content, show_blog_pages, show_pubs


class Command(BaseCommand):
    help = 'Custom command to process orders.'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Action to perform')
        parser.add_argument('pub', type=str, nargs='?',
                            help='Publication name or ID')

    def handle(self, *args, **options):
        action = options['action']
        pub = options['pub']

        if action == 'pubs':
            list_publications(pub)
            show_pubs(pub)
        elif action == 'scan':
            scan_for_blog_content()
        elif action == 'build':
            pass
            # build_pub(pub, self)
        elif action == 'add':
            add_blog_pages()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown action: {action}"))

    # def handle_build(self, pub):
    #     from pathlib import Path
    #     pub_dir = Path("Obsidian/public/guides") / pub
    #     if not pub_dir.exists():
    #         self.stdout.write(self.style.ERROR(
    #             f"Publication path does not exist: {pub_dir}"))
    #         return
    #     build_pdf(pub_dir)
    #     build_epub(pub_dir)
