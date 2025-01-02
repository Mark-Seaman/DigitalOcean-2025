from pathlib import Path
from random import choice

from django.forms import model_to_dict
from publish.days import is_old
from publish.files import write_json
from publish.import_export import get_pub_contents, pub_json_path
from publish.shell import banner

from .document import document_body, document_html, document_title
from .files import read_csv_file, read_file, read_json
from .import_export import create_pub, pub_json_path, save_pub_data
from .models import Content, Pub
from .text import line_count, text_join
from .toc import create_pub_index


def all_blogs():
    return all_pubs('blog')


def all_books():
    return all_pubs('book')


def all_courses():
    return all_pubs('course')


def all_privates():
    return all_pubs('private')


def all_pubs(pub_type=None):
    if pub_type:
        return list(Pub.objects.filter(pub_type=pub_type))
    else:
        return list(Pub.objects.all())


def bouncer_redirect(bouncer_id):
    if bouncer_id:
        bounce_table = read_csv_file(
            'Documents/Shrinking-World-Pubs/_bouncer.csv')
        for x in bounce_table:
            if x[1:] and int(x[0]) == bouncer_id:
                # print(f"Bounce to {x[1]}")
                return x[1]


def build_pubs(**kwargs):

    def build_pub_index(pub, verbose):
        if pub.auto_index:
            if verbose:
                print(f"CREATE Index - {pub.name}")
            create_pub_index(pub, get_pub_contents(pub))

    def delete_pubs():
        if delete:
            if verbose:
                print("Delete pubs\n")
            Pub.objects.all().delete()
            assert len(Pub.objects.all()) == 0

    def verify_all_pubs():
        if is_old("config/publish.json"):
            if verbose:
                print("Save pubs JSON\n")
            save_pub_data()
        return verify_pubs(verbose)

    verbose = kwargs.get('verbose', False)
    delete = kwargs.get('delete', False)
    delete_pubs()
    if verbose:
        print("Build pubs:\n")
    for pub in list_publications():
        p = create_pub(pub[0], pub[1], verbose)
        get_pub(p.name)
        build_pub_index(p, verbose)

    return verify_all_pubs()


def doc_view_context(**kwargs):
    path = kwargs.get('path', 'Documents/shrinking-world.com/blog/Index.md')
    json = kwargs.get('json', 'Documents/shrinking-world.com/blog.json')
    kwargs = read_json(json)
    markdown = document_body(read_file(path))
    kwargs['title'] = document_title(path)
    kwargs['html'] = document_html(markdown)
    return kwargs


def get_pub(name):
    return Pub.objects.get(name=name)


def get_pub_info(pub_name=None):
    if pub_name:
        pubs = [get_pub(pub_name)]
    else:
        pubs = all_pubs()
    text = ''
    for pub in pubs:
        text += f'{banner(pub.name)}\n\n{pub}\n\n'
        text += f'Title: {pub.title}\n\n'
        text += f'Tag Line: {pub.subtitle}\n\n'
        text += f'Document Path: {pub.doc_path}\n\n'
        text += f'Summary: \n{show_pub_content(pub)}\n\n'
    return text


def is_local(host):
    return '127.0.0.1' in host or 'localhost' in host


def list_publications():
    return read_csv_file('Documents/publications.csv')


def list_content(pub):
    return list(Content.objects.filter(blog=pub))


def pub_redirect(host, pub, doc):
    if host == "shrinking-world.com" and not pub:
        return f"/after"
    if host == "seamanslog.com" and not pub:
        return f"/after"
    if host == "seamansguide.com" and not pub:
        return f"/pubs/book"
    if host == "seamanfamily.org" and not pub:
        return f"/after"
    if host == "spiritual-things.org" and not pub:
        return f"/spiritual"
    if host == "markseaman.org" and not pub:
        return f"/marks"
    if host == "markseaman.info" and not pub:
        return f"/private"
    if ("localhost" in host or "127.0.0.1" in host) and not pub:
        return f"/pubs/book"
    if not doc:
        return f"/{pub}"
    return f"/{pub}/{doc}"


def random_doc(directory):
    return choice([p for p in Path(directory).iterdir()])


def random_doc_page(path):
    x = choice([str(f.name)
               for f in Path(path).iterdir() if str(f).endswith(".md")])
    return x.replace(".md", "")


def save_pub_info():
    for pub in all_pubs():
        text = get_pub_info(pub.name)
        Path(f'probe/pubs/{pub.name}').write_text(text)


def jumbotron_json(kwargs):
    writer = dict(title="Writer",
                  description="Books and blogs about life",
                  content='He writes about how to utilize technology to thrive in the modern world.\n' +
                  'He also explores the life stages and how to navigate them.',
                  link='/marks/Write.md')
    teacher = dict(title="Teacher",
                   description="Shrinking World Academy",
                   content='Training students in technology such as AI, Web Development, and Software Engineering.' +
                   'He also teaches at University of Northern Colorado and writes textbooks.' +
                   'He founded Shrinking World Academy to provide online technology courses.',
                   link='/marks/Teach.md')
    innovator = dict(title="Innovator",
                     description="Technical innovation and invention",
                     content='Mark has worked over 44 years as a professional software engineer. He has developed over 100 software apps and has 12 patents.',
                     link='/marks/Innovate.md')
    kwargs['jumbotrons'] = [writer, teacher, innovator]


def select_blog_doc(pub, doc, local_host=False):
    def load_object(pub):
        return Pub.objects.filter(pk=pub.pk).values()[0]

    def load_document(pub):
        path = pub.doc_path
        path = Path(path) / doc.replace("-", "/")
        if not Path(path).exists() and Path(f"{path}.md").exists():
            path = Path(f"{path}.md")
        if not Path(path).exists():
            path = Path(str(path).replace("/Pub", "/Pub/stories"))
        if path.exists():
            markdown = document_body(read_file(path), pub.image_path)
            github = 'https://github.com/Mark-Seaman/SoftwareEngineering'
            server = 'https://seamanslog.com'
            team = 'https://seamanslog.com/sweng/m1-Instructor_1.md'
            markdown = markdown.replace('{{ github }}', github)
            markdown = markdown.replace('{{ server }}', server)
            markdown = markdown.replace('{{ team }}', team)
            title = document_title(path)
            html = document_html(markdown)
        else:
            title = "Missing Document"
            html = f"<h1>Document file not found<h1><h2> {path}</h2>"

        return dict(
            title=title, html=html, site_title=pub.title, site_subtitle=pub.subtitle, path=path
        )

    p = get_pub(pub)
    if p:
        kwargs = model_to_dict(p)
        kwargs.update(load_document(p))
        jpath = Path(str(kwargs['path']).replace(".md", ".json"))
        if jpath.exists():
            kwargs.update(read_json(jpath))
        # if pub == 'marks' and doc == 'Index.md':
        #     jumbotron_json(kwargs)
        kwargs["menu"] = read_menu(kwargs.get("menu"), local_host)
    return kwargs


def read_menu(menu, local_host):

    def allow(items):
        exclude = ['Unpublished', 'Edit Content']
        return [item for item in items if item[0] not in exclude]

    if menu:
        m = read_json(menu)
        if not local_host and "menu" in m and "items" in m["menu"]:
            items = m["menu"]["items"]
            m["menu"]["items"] = allow(items)
        return m["menu"]


def save_pub_json(pub=None):
    if pub:
        pubs = [pub]
    else:
        pubs = all_pubs()

    for pub in pubs:
        json_path = pub_json_path(pub.name, pub.doc_path)
        data = {}
        for field in pub._meta.get_fields():
            if field.concrete:
                field_name = field.name
                data[field_name] = getattr(pub, field_name)
        write_json(json_path, data)
        json_path = pub_json_path(pub.name, pub.doc_path)
        print(f'\n\n{json_path}:\n\n', json_path.read_text())
        json1 = Path(f'static/js/{pub.name}.json')
        if json1.exists():
            json1.unlink()


def show_pub_content(pub):
    text = f"PUB CONTENT - {pub.title}\n\n"
    folders = get_pub_contents(pub)
    for f in folders:
        text += f"\nFOLDER {f.get('path')}\n"
        for d in f.get("documents"):
            text += f"     {d.get('path')}\n"
    return text


def show_pub_json(pub=None):
    if pub:
        pubs = [get_pub(pub)]
    else:
        pubs = all_pubs()
    return text_join([read_file(pub_json_path(pub.name, pub.doc_path)) for pub in pubs])


def verify_pubs(verbose):
    pubs = list_publications()
    for p in pubs:
        if p:
            pub = Pub.objects.filter(doc_path=p[1], name=p[0])
            if pub:
                pub = pub[0]
            else:
                print("NO OBJECT", p)
                assert False
        assert Path(pub.doc_path).exists()
        json = pub_json_path(pub.name, pub.doc_path)
        assert json.exists()

    pubs = list(Pub.objects.all())
    info = line_count(get_pub_info())
    contents = len(Content.objects.all())
    min_lines, max_lines = 3600, 6400
    if min_lines < info and info < max_lines:
        text = f'Rebuild Pubs:  {text_join([str(p) for p in  pubs])}\n'
        text += f'\nPub Info: {info}\n'
        text += f'\nPub Contents: {contents}\n'
        if verbose:
            print(text)
        else:
            return text


def work_pending():
    output = 'AI DOCS:\n\n'
    for pub in all_pubs():
        output += list_ai_docs(pub)
    path = Path('Documents/markseaman.info/words/AI-Docs')
    path.write_text(output)
