from os import chdir, system
from os.path import exists
from pathlib import Path, PurePath

from publish.shell import shell


def vc_command(options):
    if options:
        cmd = options[0]
        args = options[1:]
        if cmd == "commit":
            vc_commit(args)
        elif cmd == "diff":
            vc_diff()
        elif cmd == "dirs":
            for d in vc_dirs():
                print(PurePath(d))
        # elif cmd == 'log':
        #     vc_log(args)
        elif cmd == "pull":
            vc_pull(args)
        elif cmd == "push":
            vc_push()
        elif cmd == "status":
            vc_status()
        else:
            vc_help()
    else:
        vc_help()


def vc_help():
    print(
        """
        vc Command

        usage: x vc COMMAND [ARGS]

        COMMAND:

            commit  - update all local changes in git
            diff    - show uncommitted changes
            dirs    - show the version directories
            log     - show the log on the production server
            pull    - pull all changes from repo
            push    - push all changes to repo
            status  - show git status

        """
    )


# ------------------------------
# Functions


def git_cmd(label, cmd, dirs=None):
    # print(label)
    if not dirs:
        dirs = vc_dirs()
    for d in dirs:
        # print(d)
        chdir(d)
        text = git_filter(shell(cmd))
        if text and text != "\n":
            print(f"cd {d}")
            print(text)


def git_filter(text):
    def ok(line):
        filters = [
            "up to date",
            "up-to-date",
            "nothing",
            "no changes",
            "branch main",
            "origin/main",
            "git add",
            "git checkout",
            "publish your local",
            "insertions(+)",
            "ing objects:",
        ]
        for f in filters:
            if f in line:
                return False
        return True

    text = text.split("\n")
    text = [line for line in text if ok(line)]
    return "\n".join(text)


def vc_commit(args):
    comment = " ".join(args)
    git_cmd("git add:", "git add -A .")
    git_cmd("git commit:", 'git commit -m "%s"' % comment)
    git_cmd("git push:", 'git push')


def vc_diff():
    git_cmd("git diff:", "git diff --color")


def vc_dirs():

    # Macs
    hammer = Path.home() / "Hammer"
    if exists(hammer):
        pubs = hammer / "Documents/Shrinking-World-Pubs"
        github = Path.home() / "Github"
        prometa = github / "ProMETA"
        dirs = [hammer, pubs]
        return [PurePath(d) for d in dirs if d.exists()]


def vc_pull(args):
    vc_commit(['Auto Commit'])

    for d in vc_dirs():
        chdir(d)
        git_cmd("git pull:", "git pull")
    path = Path.home() / "Hammer"
    chdir(path)
    git_cmd("git checkout production:", "git checkout production", [path])
    git_cmd("git pull:", "git pull", [path])
    git_cmd("git checkout main:", "git checkout main", [path])
    git_cmd("git merge:", "git merge production", [path])


def vc_push():
    cmd = """
        cd ~/Hammer &&
        git checkout production &&
        git pull &&
        git merge main -m "Main Merge" &&
        git push &&
        git checkout main &&
        
        cd ~/Hammer/Documents/Shrinking-World-Pubs &&
        git push &&
        
        # Show deployment status
        open https://cloud.digitalocean.com/apps/260d8b80-b11f-4e57-a38d-dea84b9c2396/overview
    """
    system(cmd)


def vc_status():
    git_cmd("git status:", "git status")
