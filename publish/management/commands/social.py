from django.core.management.base import BaseCommand

from brainchild.social import add_blog_pages, build_blog_files, construct_blog, list_publications, scan_for_blog_content, show_blog_pages, show_pubs, reset_blog_data


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
        elif action == 'pages':
            show_blog_pages()
        elif action == 'construct':
            construct_blog()
        elif action == 'scan':
            scan_for_blog_content()
        elif action == 'build':
            build_blog_files()
        elif action == 'add':
            add_blog_pages(pub)
        elif action == 'initialize':
            reset_blog_data()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown action: {action}"))
