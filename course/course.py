from django.contrib.auth import get_user_model
from pathlib import Path
from course.import_export import bacs350_options, create_course, cs350_options, import_all_courses
from course.student import create_student, export_students, import_sales, import_students, students
from course.workspace import workspace_path

from publish.document import document_body, document_html, document_title
from publish.files import read_file, read_json
from .models import Student, Team
from .models import Content, Course


def accordion_data(course, week):

    def card_data(title="Random Card", data=None, color='bg-primary text-light', width='col-lg-12', link=None):
        return dict(title=title, data=data, color=color, width=width)

    def card_content(i, active, data):
        card = card_data(f'Week {i+2}',  data)
        if i == active:
            card.update(dict(id=i, collapsed='', show='show', aria='true'))
        else:
            card.update(
                dict(id=i, collapsed='collapsed', show='', aria='false'))
        return card

    weeks = weekly_content(course)
    return [card_content(i, week-1, c) for i, c in enumerate(weeks)]


def course_settings(**kwargs):
    def read_course_settings(course):
        return read_json(
            Path("Documents") / "shrinking-world.com" /
            course.name / "course.json"
        )

    course = get_course(kwargs["course"])
    settings = read_course_settings(course)
    course.week = settings["week"]
    course.save()
    settings["course_name"] = course.name
    settings["course_object"] = course
    kwargs.update(**settings)
    return kwargs


def create_courses():
    course1 = create_course(**cs350_options())
    course2 = create_course(**bacs350_options())


def find_artifacts(course):
    def list_files(c, doc_type):
        results = []
        d = Path(c.doc_path)/doc_type
        if d.exists():
            # print(doc_type, 'files:')
            for a in sorted(d.iterdir()):
                results.append(str(a))
        return results

    c = get_course(course)
    # print(c.name, c.title, c.doc_path)
    lessons = list_files(c, 'lesson')
    projects = list_files(c, 'project')
    docs = list_files(c, 'docs')
    # list_files(c, '.')
    # videos = list_files(c, 'video')
    return lessons+projects+docs


def get_course(course_name):
    return Course.objects.get(name=course_name)


def get_course_content(user, **kwargs):
    kwargs = course_settings(**kwargs)
    course = kwargs["course_object"]
    week = kwargs["week"]
    doctype = kwargs.get('doctype')

    # if doctype:
    #     html = read_document(course, kwargs)
    #     kwargs.update(dict(title=course.title, html=html))
    # else:
    #     kwargs['accordion'] = accordion_data(course, week)[:week]

    # if user.is_anonymous:
    #     kwargs['doctype'] = 'docs'
    #     kwargs['doc'] = 'StudentWorkspace.md'
    #     html = read_document(course, kwargs)
    #     kwargs.update(dict(title=course.title, html=html))
    # else:
    # student = Student.objects.filter(course=course, user=user)
    # if student:
    #     student = student.first()
    student = None
    if doctype:
        html = read_document(course, kwargs)
        kwargs.update(dict(title=course.title, html=html, student=student))
    else:
        kwargs['accordion'] = accordion_data(course, week)[:(week+1)]
        kwargs['student'] = student

    return kwargs


def get_content(course):
    weeks = []
    for week in Content.objects.filter(course=course, doctype="week").order_by('order'):
        contents = []
        for content in Content.objects.filter(course=course, folder=week):
            if (
                content.doctype == "lesson"
                or content.doctype == "project"
                or content.doctype == "demo"
            ):
                contents.append(content)
        weeks.append(dict(week=week, contents=contents))
    return weeks


def initialize_course_data(**kwargs):
    verbose = kwargs.get('verbose')
    delete = kwargs.get('delete')
    sales = kwargs.get('sales')
    if delete:
        get_user_model().objects.all().delete()
    create_courses()
    import_all_courses()
    if sales:
        sales_to_students()
    import_students(workspace_path(course='bacs350', project='_students.csv'))
    students(verbose=verbose)


def sales_to_students():
    import_sales(workspace_path(course='bacs350', project='_sales.csv'))
    create_student(name='Mark Seaman',
                   email='mark.seaman@shrinking-world.com', course='cs350')
    create_student(name='Mark Seaman',
                   email='mark.seaman@shrinking-world.com', course='bacs350')
    export_students(workspace_path(
        course='bacs350', project='_students.csv'))
    import_students(workspace_path(course='bacs350', project='_students.csv'))


def show_content(course):
    content = ""
    weeks = get_content(course)
    for w in weeks:
        content += f'{w["week"]}\n'
        for c in w["contents"]:
            content += f"    {c}\n"
    return content


def resource_title(x):
    return document_title(x.document)


def document_path(course, doctype, doc):
    return f"Documents/shrinking-world.com/{course.name}/{doctype}/{doc}"


def read_document(course, kwargs):
    doctype = kwargs.get("doctype")
    order = kwargs.get("order")
    doc = kwargs.get("doc", "StudentWorkspace.md")

    if doctype == "chapter" or doctype == "skill":
        path = document_path(course, 'docs', 'Purchase.md')
    elif doctype == "docs" and doc:
        path = document_path(course, 'docs', doc)
    elif doctype and order:
        path = document_path(course, doctype, f"{order:02}.md")
    else:
        path = document_path(course, 'docs', "StudentWorkspace.md")
    markdown = document_body(read_file(path))
    html = document_html(markdown)
    return html


def weekly_content(course, full_agenda=False):
    def lesson(x):
        slides_url = x.url.replace("lesson", "slides")
        video_doc = Path(x.document.replace("lesson", "video"))
        video_url = x.url.replace("lesson", "video")
        if video_doc.exists():
            video_url = video_url
            return dict(title=f'Lesson {x.order}', notes=x.url, slides=slides_url, video=video_url)
        return dict(title=x.title, notes=x.url, slides=slides_url)

    def weekly_agenda(week):
        lessons = []
        practice = []
        book = []

        for x in week["contents"]:
            if x.doctype == "lesson":
                lessons.append(lesson(x))
            elif x.doctype == "chapter" or x.doctype == "skill":
                if full_agenda:
                    book.append(x)
            elif x.doctype == "project":
                practice.append(x)

        return dict(week=week, practice=practice, lessons=lessons, book=book)

    return [weekly_agenda(week) for week in get_content(course)]
