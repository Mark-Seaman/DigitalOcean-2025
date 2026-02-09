from django.template import Engine, Context
from pathlib import Path
import random
from re import split
from json import loads
from brainchild.models import BlogPage, BlogPost, PubCategory, Pub

# --------------------- Scan for blog content --------------------- #


def construct_blog():
    print(f'Constructing blog for all groups')
    # reset_blog_data()
    # Pub.objects.all().delete()
    list_publications()
    scan_for_blog_content()
    show_pubs()
    add_blog_pages()
    build_blog_files()
    show_blog_pages()


def reset_blog_data():
    # BlogPost.objects.all().delete()
    Pub.objects.all().delete()
    PubCategory.objects.all().delete()
    PubCategory.objects.get_or_create(name="growth", title="Personal Growth")
    PubCategory.objects.get_or_create(
        name="playbooks", title="Creative Playbooks")
    PubCategory.objects.get_or_create(
        name="spirituality", title="Spiritual Guides")
    # scan_for_blog_content()


def scan_for_blog_content():
    BlogPost.objects.all().delete()

    def extract_blog_posts(p):
        blog_content_path = Path(p.blog_content_path)
        if not blog_content_path.exists():
            print(
                f'Blog content path does not exist: {blog_content_path}')
            p.delete()
            return

        public_path = Path(
            f"Obsidian/public/{p.category.name}/{p.name}/{p.name}.md")
        if not public_path.exists():
            print(
                f'Public Blog path does not exist: {public_path}')
            p.delete()
            return
        scan_for_blog_content(blog_content_path)

    def scan_for_blog_content(path):
        sections = markdown_sections(path)
        for section in sections:
            title = section.splitlines()[0].replace('#', '').strip()
            BlogPost.objects.get_or_create(
                pub=p,
                title=title,
                content=section
            )

    def markdown_sections(path):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
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

    for category in PubCategory.objects.all():
        for p in Pub.objects.filter(category=category):
            extract_blog_posts(p)


# --------------------- Show publications --------------------- #


def show_pubs(category=None):
    if not category:
        text = "# Blog Articles Available\n"

        for group in PubCategory.objects.all():
            t = show_pubs(group.name)
            text += f"\n## {group.name}\n\n{t}"
        write_file_path = Path('Obsidian/forge/mcp/blog.md')
        write_file_path.write_text(text, encoding='utf-8')
        return text

    text = ""
    for p in Pub.objects.filter(category__name=category):
        text += f"- [{p.name}]({Path(p.blog_content_path).name})\n"
        for bp in p.blog_posts.all():
            text += f'    - {bp.id} - {bp.title}\n'
    return text


def list_publications(group=None):

    def pub_title(pub, blog_dir):
        json_path = blog_dir / f'{pub}.json'
        if json_path.exists():
            json_data = loads(json_path.read_text(encoding='utf-8'))
            return json_data.get("title", None)

    if not group:
        for group in PubCategory.objects.all():
            list_publications(group.name)
        return

    print(f'Articles: {group}')
    for blog_dir in Path('Obsidian/forge/').glob(f'{group}/*/dev/'):
        pub_name = blog_dir.parent.name
        title = pub_title(pub_name, blog_dir)
        print(f'    - {pub_name} - {title}')
        path = str(blog_dir.parent)
        Pub.add_pub(pub_name, title, path, group)


def show_blog_pages():
    text = "\n\n---\n\n# Published Blog Pages\n\n"
    for category in PubCategory.objects.all():
        text += f"\n## {category.name}\n"
        for p in Pub.objects.filter(category=category):
            for page in BlogPage.objects.filter(post__pub=p):
                path = f'{category.name}/blog/{page.order:02d}.md'
                text += f'- [[{path}]] - {page.post.pk} - {page.post.title}\n'
    write_file_path = Path('Obsidian/forge/mcp/blog.md')
    with open(write_file_path, "a", encoding="utf-8") as f:
        f.write(text)
    return text

# ------------------ Blog Pages ------------------#


def add_blog_pages(group=None):
    add_initial_pages(group)
    # add_round_robin_pages(group, 1)


def add_initial_pages(group=None):
    if not group:
        for category in PubCategory.objects.all():
            add_initial_pages(category.name)
        return
    print(f'Adding blog pages to {group}')
    category = PubCategory.objects.get(name=group)
    for pub in Pub.objects.filter(category=category):
        post = BlogPost.objects.filter(pub=pub).order_by('id')[0]
        add_blog_page(post)


def add_round_robin_pages(group, pages=1):
    print(f'Adding {pages} blog pages for post: {group}')
    pubs = Pub.objects.filter(category__name=group)
    for pub in pubs:
        posts = BlogPost.objects.filter(pub=pub)
        post = random.choice(posts)
        add_blog_page(post)


def add_random_blog_pages(post='all', pages=1):
    print(f'Adding {pages} blog pages for post: {post}')
    for page in range(pages):
        posts = BlogPost.objects.all()
        x = random.choice(posts)
        add_blog_page(x)


def add_blog_page(post):
    order = BlogPage.objects.filter(
        post__pub__category=post.pub.category).count() + 1
    page, created = BlogPage.objects.get_or_create(
        post=post,
        defaults={
            "order": order
        }
    )
    return page, created


# --------------------- Website Files --------------------- #

BLOG_TEMPLATE = """### {{ blog}}

{{ text|safe }}

---

Prev: [{{ prev_title }}]({{ prev }}) -- Go Deeper [{{ more_title }}]({{ more }})  --  Next: [{{ next_title }}]({{ next }})

"""


def write_blog_post(entry):
    file_path = Path(entry["file"])
    engine = Engine.get_default()
    template = engine.from_string(BLOG_TEMPLATE)
    content = template.render(Context(entry))
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return file_path


def page_title(group, page_order):
    return BlogPage.objects.get(
        post__pub__category__name=group, order=page_order).post.title


def build_blog_files(group=None):
    if not group:
        for category in PubCategory.objects.all():
            build_blog_files(category.name)
        return

    print(f'Building blog files for {group}')
    for page in BlogPage.objects.filter(post__pub__category__name=group).order_by('post__pub', 'order'):
        cat_name = page.post.pub.category.name
        pub_name = page.post.pub
        num_posts = BlogPage.objects.filter(
            post__pub__category__name=group).count()
        prev = page.order - 1 if page.order > 1 else num_posts
        next = page.order + 1 if page.order < num_posts else 1
        more = f'{pub_name}/{pub_name}'
        more_title = page.post.pub.title
        prev_title = page_title(group, prev)
        next_title = page_title(group, next)
        entry = {
            "blog": page.post.pub.category.title,
            "title": page.post.title,
            "text": page.post.content,
            "file": f'Obsidian/public/{cat_name}/blog/{page.order:02d}.md',
            "prev": f'{prev:02d}',
            "next": f'{next:02d}',
            "prev_title": prev_title,
            "next_title": next_title,
            "more": f'{more}',
            "more_title": more_title,
        }
        write_blog_post(entry)
