import shlex
from os import environ

from django.core.management.base import BaseCommand
from os.path import exists, isdir, join
from traceback import format_exc

from publish.shell import shell


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("files", nargs="*", type=str)

    def handle(self, *args, **options):
        try:
            # print(options['files'])
            edit_file(options["files"])
        except:
            self.stdout.write("** edit Exception (%s) **" %
                              " ".join(options["files"]))
            self.stdout.write(format_exc())


def edit_file(args):
    exe_path = "subl"
    # create command string as f-string. with exe_path and str(args)

    # normalize args into a string and safely quote
    if isinstance(args, (list, tuple)):
        arg_str = " ".join(shlex.quote(str(a)) for a in args)
    elif args is None:
        arg_str = ""
    else:
        arg_str = shlex.quote(str(args))

    command = f"{exe_path} {arg_str}".strip()
    # print(command)
    shell(command)
