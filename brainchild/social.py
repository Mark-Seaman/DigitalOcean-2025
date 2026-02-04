from pprint import pprint
from django.template import Engine, Context
from pathlib import Path
import random
from re import split
from tokenize import group

from requests import post
from brainchild.models import BlogPage, BlogPost, PubCategory, Pub

# --------------------- Scan for blog content --------------------- #


def reset_blog_data():
    BlogPost.objects.all().delete()
    Pub.objects.all().delete()
    PubCategory.objects.all().delete()
    PubCategory.objects.get_or_create(name="growth")
    PubCategory.objects.get_or_create(name="playbooks")
    PubCategory.objects.get_or_create(name="home")
    PubCategory.objects.get_or_create(name="spirituality")
    scan_for_blog_content()


def scan_for_blog_content():

    def extract_blog_posts(p):            # read blog content
        blog_content_path = Path(p.blog_content_path)
        public_path = Path(f"Obsidian/public/{p.category.name}/{p.title}")
        # if not public_path.exists():
        #     print(
        #         f'Public Blog path does not exist: {public_path}')
        if blog_content_path.exists() and public_path.exists():
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


def add_blog_pages(group):
    print(f'Adding blog pages to {group} blog')
    # set_initial_blog_pages()
    add_round_robin_pages(group, 1)
    show_blog_pages()


def set_initial_blog_pages():
    print('Setting initial blog pages')
    BlogPage.objects.all().delete()
    posts = BlogPost.objects.all()
    for x in range(3):
        post = random.choice(posts)
        add_blog_page(post)


def add_round_robin_pages(group, pages=1):
    print(f'Adding {pages} blog pages for post: {group}')
    pubs = Pub.objects.filter(category__name=group)
    for pub in pubs:
        posts = BlogPost.objects.filter(pub=pub)
        post = random.choice(posts)
        # Explain this logic
        page, created = add_blog_page(post)
        if created:
            print(
                f'Added blog page: {post.title} for publication: {pub.title}')
        else:
            print(
                f'Blog page already exists: {post.title} for publication: {pub.title}')


def add_random_blog_pages(post='all', pages=3):
    print(f'Adding {pages} blog pages for post: {post}')
    for page in range(pages):
        posts = BlogPost.objects.all()
        x = random.choice(posts)
        add_blog_page(x)


def add_blog_page(post):
    order = BlogPage.objects.filter(
        post__pub__category=post.pub.category).count() + 1
    print('ID:', post.id, 'Title:', post.title, 'Publication:', post.pub.title,
          'Order:', order)
    page, created = BlogPage.objects.get_or_create(
        post=post,
        defaults={
            "title": post.title,
            "content": post.content,
            "order": order
        }
    )

    if not created:
        # Optional: keep page in sync with post
        page.title = post.title
        page.content = post.content
        page.save()

    return page, created


def show_blog_pages():
    print("Blog Pages:\n\n")
    for category in PubCategory.objects.all():
        print(f'\n\n{category.name}:\n')
        for p in Pub.objects.filter(category=category):
            print(f'   {p.title}')
            for post in BlogPage.objects.filter(post__pub=p):
                print(f'        {post.pk} - {post.title}')


# --------------------- Website Files --------------------- #

# Define the template as a Django template string
BLOG_TEMPLATE = """{{ title }}

{{ text }}

Prev: [[{{ prev }}]].  Go Deeper [[{{ more }}]]. Next [[{{ next }}]]
"""


def write_blog_post(entry: dict):
    """
    Takes a JSON entry and writes a markdown blog post file
    using a Django template.

    Expected keys in entry:
      - title
      - text
      - file
      - prev
      - next
      - more
    """

    file_path = Path(entry["file"])

    # Build template context
    context = {
        "title": entry.get("title", "").strip(),
        "text": entry.get("text", "").strip(),
        "prev": entry.get("prev", ""),
        "next": entry.get("next", ""),
        "more": entry.get("more", ""),
    }

    # Render template
    engine = Engine.get_default()
    template = engine.from_string(BLOG_TEMPLATE)
    content = template.render(Context(context))

    print('\n\n', file_path)
    print(content)

    # # Ensure directories exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # # Write file
    file_path.write_text(content, encoding="utf-8")

    return file_path


def build_blog_files():
    for page in BlogPage.objects.filter(post__pub__category__name='growth').order_by('post__pub', 'order'):
        cat_name = page.post.pub.category.name
        pub_name = page.post.pub
        entry = {
            "title": page.title,
            "text": page.content,
            "file": f'Obsidian/public/{cat_name}/blog/{page.order:02d}.md',
            "prev": f'{page.order - 1:02d}' if page.order > 1 else '00',
            "next": f'{page.order + 1:02d}',
            "more": f'public/{cat_name}/{pub_name}/{pub_name}',
        }
        # pprint(entry, indent=4)
        write_blog_post(entry)
