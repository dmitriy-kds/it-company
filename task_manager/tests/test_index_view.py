from django.test import TestCase
from django.urls import reverse

from task_manager.models import Worker, Position, Task


class IndexTests(TestCase):
    def test_index_returns_200(self):
        response = self.client.get(reverse("task_manager:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_visit_counter(self):
        self.client.get(reverse("task_manager:index"))
        self.assertEqual(self.client.session["counter"], 1)
        self.client.get(reverse("task_manager:index"))
        self.assertEqual(self.client.session["counter"], 2)

    def test_index_context(self):
        response = self.client.get(reverse("task_manager:index"))
        self.assertEqual(response.context["num_employees"], Worker.objects.count())
        self.assertEqual(response.context["num_positions"], Position.objects.count())
        self.assertEqual(response.context["num_tasks"], Task.objects.count())
        self.assertEqual(response.context["num_new_tasks"], Task.objects.filter(status="New").count())
        self.assertEqual(response.context["num_completed_tasks"], Task.objects.filter(status="Done").count())
        self.assertEqual(response.context["num_in_progress_tasks"], Task.objects.filter(status="In Progress").count())
