from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import admin

from task_manager.models import Worker, Position, TaskType, Task


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123&*("
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="test position")
        self.worker = get_user_model().objects.create_user(
            first_name="test_first",
            last_name="test_last",
            username="test_username",
            password="test123*!",
            email="test_email@email.com",
            position=self.position,
        )


    def test_worker_position_in_list_display(self):
        worker_admin = admin.site._registry[Worker]
        self.assertIn("position", worker_admin.list_display)

    def test_worker_position_in_fieldsets(self):
        url = reverse("admin:task_manager_worker_change", args=[self.worker.id])
        response = self.client.get(url)
        self.assertContains(response, "Position:")

    def test_worker_position_in_add_fieldsets(self):
        url = reverse("admin:task_manager_worker_add")
        response = self.client.get(url)
        self.assertContains(response, "Position:")

    def test_worker_position_in_list_filter(self):
        url = reverse("admin:task_manager_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, "By position")

    def test_worker_first_name_in_search_fields(self):
        worker_admin = admin.site._registry[Worker]
        self.assertIn("first_name", worker_admin.search_fields)

    def test_worker_last_name_in_search_fields(self):
        worker_admin = admin.site._registry[Worker]
        self.assertIn("last_name", worker_admin.search_fields)

    def test_worker_username_in_search_fields(self):
        worker_admin = admin.site._registry[Worker]
        self.assertIn("username", worker_admin.search_fields)

    def test_task_type_name_in_list_display(self):
        task_type_admin = admin.site._registry[TaskType]
        self.assertIn("name", task_type_admin.list_display)

    def test_task_type_name_in_search_fields(self):
        task_type_admin = admin.site._registry[TaskType]
        self.assertIn("name", task_type_admin.search_fields)

    def test_position_name_in_list_display(self):
        position_admin = admin.site._registry[Position]
        self.assertIn("name", position_admin.list_display)

    def test_position_name_in_search_fields(self):
        position_admin = admin.site._registry[Position]
        self.assertIn("name", position_admin.search_fields)

    def test_task_list_display(self):
        task_admin = admin.site._registry[Task]
        self.assertEqual([
            "name",
            "description",
            "deadline",
            "status",
            "priority",
            "task_type"
        ]
            , task_admin.list_display)

    def test_task_status_in_list_filter(self):
        task_admin = admin.site._registry[Task]
        self.assertIn("status", task_admin.list_filter)

    def test_task_priority_in_list_filter(self):
        task_admin = admin.site._registry[Task]
        self.assertIn("priority", task_admin.list_filter)

    def test_task_task_type_in_list_filter(self):
        task_admin = admin.site._registry[Task]
        self.assertIn("task_type", task_admin.list_filter)

    def test_task_name_in_search_fields(self):
        task_admin = admin.site._registry[Task]
        self.assertIn("name", task_admin.search_fields)

    def test_task_description_in_search_fields(self):
        task_admin = admin.site._registry[Task]
        self.assertIn("description", task_admin.search_fields)
