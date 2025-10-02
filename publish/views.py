from pathlib import Path
from django.views.generic import RedirectView, TemplateView

from publish.document import document_body, document_html, document_title
from publish.yearbook import select_content

from .files import read_file, read_json
from .import_export import refresh_pub_from_git
from .models import Pub
from .publication import bouncer_redirect, is_local, pub_redirect, read_menu, select_blog_doc


class BouncerRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        x = bouncer_redirect(kwargs.get('id'))
        if x:
            return x
        host = self.request.get_host()
        pub = kwargs.get("pub")
        doc = kwargs.get("doc", 'Index.md')
        return pub_redirect(host, pub, doc)


class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        pub = 'marks'
        doc = kwargs.get("doc", "contact")
        kwargs = select_blog_doc(pub, doc)
        return kwargs


class PubCoverView(TemplateView):
    template_name = "pub/cover.html"

    def get_context_data(self, **kwargs):
        pub = kwargs.get("pub", "cover")
        kwargs = obsidian_json(pub)
        image_file = f"/static/images/CoverArtwork.png"
        kwargs['image'] = image_file
        return kwargs

#  http://127.0.0.1:8000/cover/becoming


def obsidian_json(pub):
    # Read the JSON data for the publication
    json = pub_path(pub) / 'dev' / f'{pub}.json'
    data = read_json(json)
    if not data:
        print(f"Invalid JSON structure in: {json}")
        return
    # print(f"Publication Data: {data}")
    print(f"Title: {data.get('title', 'Untitled')}")
    print(f"Subtitle: {data.get('subtitle', '')}")
    print(f"Author: {data.get('author', 'Mark Seaman')}")
    print(f"Cover Image: {data.get('cover-image', '')}")
    print(f"Publication Path: {data.get('pub-path', '')}")
    return data


def pub_path(pub):
    for base_dir in ["growth", "playbooks", "spirituality", "guides"]:
        path = Path("Obsidian/forge") / base_dir / pub
        if path.exists():
            return path


class PubRedirectView(RedirectView):
    url = 'https://publish.obsidian.md/seaman'


class PubRampView(TemplateView):
    template_name = "pub/blog.html"

    def get_context_data(self, **kwargs):
        month = kwargs.get("month", "08")
        day = kwargs.get("day", "15")
        doc = kwargs.get("type", "Index")
        path = f"Documents/Shrinking-World-Pubs/log/{month:02}/{day:02}/{doc}.md"
        markdown = document_body(read_file(path))
        # title = document_title(path)
        html = document_html(markdown)
        kwargs.update({
            'title': "Seaman's Log",
            'html': html,
            'no_navbar': True,
            'no_header': True
        })
        return kwargs


class PubView(TemplateView):
    template_name = "pub/blog.html"

    def get_context_data(self, **kwargs):
        pub = kwargs.get("pub", "marks")
        doc = kwargs.get("doc", "Index.md")
        local_host = is_local(self.request.get_host())
        kwargs = select_blog_doc(pub, doc, local_host)
        return kwargs


class PubLibraryView(TemplateView):
    template_name = "pub/library.html"

    def get_context_data(self, **kwargs):
        collections = [
            get_collection('course', 'Courses'),
            get_collection('book', 'Books about Life'),
            get_collection('blog', 'Blogs'),
            get_collection('private', 'Private Blogs'),
        ]
        local_host = is_local(self.request.get_host())
        menu = read_menu("static/js/nav_blog.json", local_host)
        kwargs = dict(collections=collections, menu=menu,
                      site_title="Shrinking Word Publication Library", site_subtitle="All Publications")
        return kwargs


def get_collection(pub_type, title):
    return {'type': title, 'pubs': Pub.objects.filter(pub_type=pub_type)}


class PubListView(TemplateView):

    template_name = "pub/list.html"
    model = Pub
    context_object_name = "pubs"

    def get_context_data(self, **kwargs):
        pub_type = self.kwargs.get('pub_type')
        pubs = Pub.objects.filter(pub_type=pub_type)
        local_host = is_local(self.request.get_host())
        menu = read_menu("static/js/nav_blog.json", local_host)
        kwargs = dict(pubs=pubs, menu=menu, site_title="Shrinking Word Publication Library",
                      site_subtitle="A Seaman's Guides")
        return kwargs


class PubDetailView(TemplateView):
    template_name = "pub_script/cover.html"

    def get_context_data(self, **kwargs):
        refresh_pub_from_git()
        pub = kwargs.get("pub")
        doc = kwargs.get("doc", "Index.md")
        local_host = is_local(self.request.get_host())
        kwargs = select_blog_doc(pub, doc, local_host)
        return kwargs


class GalleryView(TemplateView):
    template_name = "gallery/gallery.html"

    def get_context_data(self, **kwargs):
        kwargs = select_content(**kwargs)
        return kwargs
