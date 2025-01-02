import csv
from pathlib import Path

from publish.document import document_body, document_html, document_title
from publish.files import read_csv_file, read_file
from publish.publication import read_menu


def select_content(**kwargs):

    def site_context(pub):
        return dict(site_title='Seaman Family Yearbook',
                    site_subtitle='Photo Stories',
                    pub=pub,
                    albums=['2023', '2022'])

    def read_content(pub, album, page):
        csv = Path(
            f'Documents/Shrinking-World-Pubs/{pub}/{album}/_content.csv')
        if csv.exists():
            content = {}
            for row in read_csv_file(csv):
                if row[1:]:
                    page = row[1].split('.')[0]
                    content[page] = story_content(pub, album, page, row[1:])
            return content
        return []

    def story_content(pub, album, page, images):
        path = Path(
            f'Documents/Shrinking-World-Pubs/{pub}/{album}/{page}.md')
        markdown = document_body(read_file(path))
        return dict(page=page,
                    path=path,
                    images=images,
                    title=document_title(path),
                    html=document_html(markdown))

    pub = kwargs.get("pub", "yearbook")
    album = kwargs.get("album")
    page = kwargs.get("page")
    kwargs.update(site_context(pub))

    csv = Path(
        f'Documents/Shrinking-World-Pubs/{pub}/{album}/_content.csv')
    image_path = Path(
        '/static/images/Shrinking-World-Pubs/yearbook')
    if csv.exists():
        stories = read_content(pub, album, page)
        kwargs['content'] = stories
        kwargs['image_path'] = image_path
        if page:
            kwargs['story'] = stories[page]

    kwargs["menu"] = read_menu("static/js/nav_yearbook.json", False)

    # kwargs['pub'] = pub
    # kwargs['albums'] = ['2023', '2022']
    return kwargs
