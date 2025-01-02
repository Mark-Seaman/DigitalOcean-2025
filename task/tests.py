from pathlib import Path
from django.test import TestCase

from publish.days import day_str, days_ago, to_date
from task.models import Task
from task.task import task_command, task_import_files


class TaskDataTest(TestCase):

    def setUp(self):
        self.task1 = dict(name='Work')
        self.task2 = dict(name='Play', hours=10)

    def test_add_book(self):
        self.assertEqual(len(Task.objects.all()), 0)
        Task.objects.create(**self.task1)
        Task.objects.create(**self.task2)
        x = Task.objects.get(pk=2)
        # self.assertEqual(str(x), '')
        self.assertEqual(x.name, 'Play')
        self.assertEqual(x.hours, 10)
        self.assertEqual(len(Task.objects.all()), 2)

    def test_goals(self):
        goals = Path("Documents/markseaman.info/history/Today.md").read_text()
        self.assertTrue(goals.startswith('# Aspirations'))

    def test_activities(self):
        today = to_date('2024-04-20')
        activities = [days_ago(today, -w*7) for w in range(16)]
        for a in activities:
            print(task_command(['day', a]))
        # print(activities)

    # def test_tasks(self):
    #     task_import_files(100)
    #     tasks = Task.objects.all()
    #     # print('Tasks:', len(tasks))
    #     self.assertGreater(len(tasks), 400)
