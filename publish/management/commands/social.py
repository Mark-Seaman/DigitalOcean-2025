from django.core.management.base import BaseCommand

from brainchild.social import list_publications, scan_for_blog_content, show_pubs


class Command(BaseCommand):
    help = 'Custom command to process orders.'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Action to perform')
        parser.add_argument('pub', type=str, help='Publication name or ID')

    def handle(self, *args, **options):
        action = options['action']
        pub = options['pub']

        if action == 'pubs':
            show_pubs(pub)
            # list_publications()
        elif action == 'scan':
            scan_for_blog_content()
        elif action == 'build':
            pass
            # build_pub(pub, self)
        elif action == 'add':
            pass
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
