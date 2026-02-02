from pathlib import Path
from re import split
from tokenize import group
from brainchild.models import BlogPost, PubCategory, Pub

# --------------------- Scan for blog content --------------------- #


def scan_for_blog_content():

    def extract_blog_posts(p):            # read blog content
        blog_content_path = Path(p.blog_content_path)
        if blog_content_path.exists():
            text = blog_content_path.read_text(
                encoding='utf-8')
            sections = markdown_sections(blog_content_path)
            for section in sections:
                title = section.splitlines()[0].replace('#', '').strip()
                print({
                    "title": title,
                    "pub": p.title
                })
                BlogPost.objects.get_or_create(
                    pub=p,
                    title=title,
                    content=section
                )
        else:
            print(f'Blog content path does not exist: {blog_content_path}')

    for category in PubCategory.objects.all():
        print(f'\n{"="*60}\nCategory: {category.name}\n{"="*60}\n')

        for p in Pub.objects.filter(category=category):
            print(f'\n{"-"*40}\n{p.pub_path}\n{"-"*40}\n')
            print(p.pub_path)
            print(p.blog_content_path)
            extract_blog_posts(p)


def markdown_sections(path):
    """
    Reads a markdown file and prints each section one at a time.
    A section is defined by a heading line starting with #.
    """

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split on headings but keep the headings
    parts = split(r"(?m)(^#+\s.*$)", text)

    sections = []
    current = ""

    for part in parts:
        if part.startswith("#"):
            if current.strip():
                sections.append(current.strip())
            current = part + "\n"
        else:
            current += part

    if current.strip():
        sections.append(current.strip())

    return sections

# --------------------- Show publications --------------------- #


def show_pubs(category='all'):
    if category == 'all':
        for group in ['spirituality', 'growth', 'playbooks', 'home']:
            show_pubs(group)
        return

    for category in PubCategory.objects.filter(name=category):
        print(f'\n{"="*60}\nCategory: {category.name}\n{"="*60}\n')

        for p in Pub.objects.filter(category=category):
            print(f'\n{"-"*40}\n{p.pub_path}\n{"-"*40}\n')
            print(p.pub_path)
            print(p.blog_content_path)
            for bp in p.blog_posts.all():
                print(f'    {bp.id} - {bp.title}')


def list_publications(group='all'):
    if group == 'all':
        for group in ['spirituality', 'growth', 'playbooks', 'home']:
            list_publications(group)
        return

    for blog_dir in Path('Obsidian/forge/').glob(f'{group}/*/dev/'):
        pub = blog_dir.parent.name
        Pub.add_pub(
            title=blog_dir.parent.name.replace('-', ' ').title(),
            pub_path=str(blog_dir.parent),
            category=group
        )


# PubCategory.objects.all().delete()
# PubCategory.objects.get_or_create(name="growth")
# PubCategory.objects.get_or_create(name="playbooks")
# PubCategory.objects.get_or_create(name="home")
# PubCategory.objects.get_or_create(name="spirituality")
