from pathlib import Path
import random
from re import split
from tokenize import group
from brainchild.models import BlogPage, BlogPost, PubCategory, Pub

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


def show_pubs(category=None):
    if not category:
        for group in PubCategory.objects.all():
            show_pubs(group.name)
        return

    group = PubCategory.objects.get(name=category)
    print(f'\n{"="*60}\nCategory: {category}\n{"="*60}\n')

    for p in Pub.objects.filter(category=group):
        print(f'\n{"-"*40}\n{p.pub_path}\n{"-"*40}\n')
        print(p.pub_path)
        print(p.blog_content_path)
        for bp in p.blog_posts.all():
            print(f'    {bp.id} - {bp.title}')


def list_publications(group=None):
    setup_pub_categories()
    if not group:
        for group in PubCategory.objects.all():
            list_publications(group.name)
        return

    for blog_dir in Path('Obsidian/forge/').glob(f'{group}/*/dev/'):
        pub = blog_dir.parent.name
        Pub.add_pub(
            title=blog_dir.parent.name.replace('-', ' ').title(),
            pub_path=str(blog_dir.parent),
            category=group
        )

# ------------------ Blog Pages ------------------#


def add_blog_pages(post='all', pages=3):
    print(f'Adding {pages} blog pages for post: {post}')
    for page in range(pages):
        posts = BlogPost.objects.all()
        # random selection of a blog post
        x = random.choice(posts)
        add_blog_page(x)
    show_blog_pages()


def add_blog_page(post, order=1):
    return BlogPage.objects.get_or_create(
        post=post,
        title=post.title,
        content=post.content,
        order=order
    )


def show_blog_pages():
    print("Blog Pages:\n\n")
    for category in PubCategory.objects.all():
        print(f'\n\n{category.name}:\n')
        for p in Pub.objects.filter(category=category):
            print(f'   {p.title}')
            for post in BlogPage.objects.filter(post__pub=p):
                print(f'        {post.pk} - {post.title}')


def setup_pub_categories():
    # PubCategory.objects.all().delete()
    if not PubCategory.objects.all():
        print("Setting up publication categories...")
        PubCategory.objects.get_or_create(name="growth")
        PubCategory.objects.get_or_create(name="playbooks")
        PubCategory.objects.get_or_create(name="home")
        PubCategory.objects.get_or_create(name="spirituality")
