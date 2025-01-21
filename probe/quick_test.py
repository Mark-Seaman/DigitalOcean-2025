from datetime import datetime
from distutils.file_util import copy_file
from pathlib import Path
from django.contrib.auth.models import User
from csv import DictReader, reader, writer

import webbrowser

from course.course import initialize_course_data
from course.import_export import import_all_courses
from course.models import Team
from course.team import setup_team_pages, setup_teams
from publish.days import days_ago, to_date, today
from publish.files import read_json, write_json
from publish.publication import build_pubs, jumbotron_json
from publish.text import text_join, text_lines
from task.task import activity_summary, fix_tasks, task_command
from task.todo import edit_todo_list
from writer.cover import create_cover_image, create_cover_thumbnails, scale_image
from writer.outline import create_outlines
from writer.pub_script import pub_path, pub_script
from writer.words import measure_pub_words
from publish.note import create_moderators

from .data import load_json_data, save_json_data
import csv


def quick_test():
    # print("No quick test defined")
    # hours_to_seta()
    # course()
    # create_moderators()
    # pub()
    # tasks()
    # tests()
    # gwriter()
    fix_tasks()
    # subscribers()
    # yearbook()
    return 'Running quick test'


def yearbook():
    print("Build YEARBOOK")
    path = Path(
        '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/yearbook/2023')
    static_path = Path(
        '/Users/seaman/Hammer/static/images/Shrinking-World-Pubs/yearbook/2023')
    static_path.mkdir(exist_ok=True, parents=True)

    print("# 2023 Photos")

    # Read CSV File Path(path)/'_content.csv'
    csv_file = path / '_content.csv'
    with open(csv_file, 'r') as file:
        for row in csv.reader(file):
            for f in row[1:]:
                copy_file(path/f, static_path/f)
                print(f'\n![](img/{f})')
            # copy_file(path/row[1], static_path/row[1])
            print(f'\n![](img/{row[1]})')
            print(f'\n[{row[0]}](img/{row[0]})')


def subscribers():
    d = Path(
        '/Users/seaman/Library/Mobile Documents/com~apple~CloudDocs/Documents/Stacie/GuestBook')
    print("SUBSCRIBERS")
    # path1 = d/'Email-Table.csv'
    # path2 = d/'email.csv'
    path3 = d/'subscribers.csv'

    # name_map = {}
    # for row in reader(open(path1)):
    #     name_map[row[1]] = row[0]
    # data = [(r[0], name_map.get(r[0], '**'))
    #         for r in reader(open(path2)) if r]
    # def read_csv_file(file_path):
    # with open(path3, 'w', newline='') as f:
    #     w = writer(f)
    #     for row in data:
    #         w.writerow(row)

    with open(path3, 'r') as csvfile:
        reader = DictReader(csvfile)
        names = []
        for row in reader:
            name = row['Name'].split(' ')
            name = name[-1] + ',' + ' '.join(name[0:-1]) + ',' + row['Email']
            names.append(name)
        names.sort()
        for name in names:
            print(name)


def course():
    # Team.objects.all().delete()
    initialize_course_data(delete=True, verbose=True, sales=False)
    # setup_teams()
    # setup_team_pages()
    import_all_courses(verbose=True, delete=True)


def pub():
    # kwargs = {}
    # jumbotron_json(kwargs)
    path = Path(
        '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/marks/Index.json')
    # write_json(path, kwargs)
    if path.exists():
        kwargs = read_json(path)
    print(kwargs)
    # Build Pubs
    # build_pubs(verbose=False, delete=True)
    # text = measure_pub_words()
    # print(text)


def gwriter():
    print("WRITER")
    print("Create Cover Images")
    # text = pub_script(
    #         'outline', ['ghost', 'Micropublishing', 'C-Outline.md'])
    # print(text)
    # create_outlines(pub_path('sweng', 'Milestone-6'))

    # print(f'Words {pub.name}: {pub.words}')

    # pub = get_pub(x)
    # # pub.delete()
    # # create_pub(x, f'Documents/Shrinking-World-Pubs/{x}/Pub', False)
    # # create_pub_index(pub, get_pub_contents(pub))
    #
    # print(show_pub_details(pub))

    # Create Cover Images
    path = '/Users/seaman/Hammer/Documents/Shrinking-World-Pubs/footsteps/Images/Plaka.png'
    scale_image(path, 800, 500)
    create_cover_image(path)
    # create_cover_thumbnails(path, True)


def tasks():
    print("TASKS")
    activity_summary()
    print(task_command(['x', '120']))


def execute_pub_script(text):
    return text_join([pub_script(line.strip().split(' ')) for line in text_lines(text) if line.strip()])


def todo():
    print("TODO")
    edit_todo_list()


def write_webapps_contents():
    csv = ""
    x = 1
    for i, row in enumerate(range(14)):
        chapter = i + 1
        csv += f"chapter/{i+1:02}.md,{chapter}\n"
        x += 1
        csv += f"skill/{i*3+1:02}.md,{chapter},{x}\n"
        x += 1
        csv += f"skill/{i*3+2:02}.md,{chapter},{x}\n"
        x += 1
        csv += f"skill/{i*3+3:02}.md,{chapter},{x}\n"
        x += 1
        csv += f"demo/{i+1:02}.md,{chapter},{x}\n"
        x += 1
        csv += f"project/{i+1:02}.md,{chapter},{x}\n"
        x += 1
    Path("Documents/seamansguide.com/webapps/_content.csv").write_text(csv)


def execute_command(args):
    if not args:
        return (f'NO COMMAND GIVEN: {args}')
    elif args[0] == 'save':
        save_json_data('config/data.json')
    elif args[0] == 'load':
        load_json_data('config/data.json')
    elif args[0] == 'web':
        url = args[1] if args[1:] else None
        web_browser(url)
    else:
        return (f'NO COMMAND FOUND: {args}')


def web_browser(url=None):
    if not url:
        url = 'http://localhost:8000/writer/author/'
    print(url)
    browser = webbrowser.get('firefox')
    browser.open(url)


def hours_to_seta():
    now = datetime.now()
    target_time = datetime(now.year, 10, 16, 12, 0, 0)
    time_difference = target_time - now
    hours_until_target = time_difference.total_seconds() / 3600
    print(f"Hours until 12:00 PM on 10-16: {hours_until_target:.2f} hours")
