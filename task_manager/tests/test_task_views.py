from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from task_manager.models import Task, TaskType


def get_future_weekday():
    d = date.today() + timedelta(days=1)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


class PublicTaskTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(
            name="test_task_type",
        )
        self.task = Task.objects.create(
            name="test_task",
            description="test_description",
            deadline=get_future_weekday(),
            status="New",
            priority=1,
            task_type=self.task_type,
        )

    def test_task_list_login_required(self):
        url = reverse("task_manager:task-list")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_task_create_login_required(self):
        url = reverse("task_manager:task-create")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_task_detail_login_required(self):
        url = reverse("task_manager:task-detail", kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_task_update_login_required(self):
        url = reverse("task_manager:task-update", kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_task_delete_login_required(self):
        url = reverse("task_manager:task-delete", kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_task_toggle_status_login_required(self):
        url = reverse("task_manager:task-toggle-status", kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_task_assign_login_required(self):
        url = reverse("task_manager:task-assign", kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)


class PrivateTaskTests(TestCase):
    def setUp(self):
        self.worker = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first",
            last_name="test_last",
            email="test_email",
            password="1234%^&*tyui",
        )
        self.another_worker = get_user_model().objects.create_user(
            username="another_username",
            first_name="another_first",
            last_name="another_last",
            email="another_email",
            password="another_1234%^&*tyui",
        )
        self.task_type = TaskType.objects.create(
            name="test_task_type",
        )
        self.another_task_type = TaskType.objects.create(
            name="another_test_task_type",
        )
        self.task = Task.objects.create(
            name="test_task",
            description="test_description",
            deadline=get_future_weekday(),
            status="New",
            priority=1,
            task_type=self.task_type,
        )
        self.another_task = Task.objects.create(
            name="another_task",
            description="another_description",
            deadline=get_future_weekday() + timedelta(days=1),
            status="Done",
            priority=4,
            task_type=self.another_task_type,
        )
        self.client.force_login(self.worker)

    def test_task_list_returns_200(self):
        url = reverse("task_manager:task-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_list_search_by_name(self):
        url = reverse("task_manager:task-list")
        response = self.client.get(url, data={"name_or_description": self.another_task.name})
        self.assertContains(response, self.another_task.description)
        self.assertNotContains(response, self.task.description)

    def test_task_list_search_by_description(self):
        url = reverse("task_manager:task-list")
        response = self.client.get(url, data={"name_or_description": self.another_task.description})
        self.assertContains(response, self.another_task.description)
        self.assertNotContains(response, self.task.description)

    def test_task_list_sort_by_name(self):
        url = reverse("task_manager:task-list")
        response = self.client.get(url, data={"sort": "-name"})
        self.assertEqual(
            list(response.context["task_list"]),
            list(Task.objects.all().order_by("-name"))
        )

    def test_task_list_sort_by_task_type(self):
        url = reverse("task_manager:task-list")
        response = self.client.get(url, data={"sort": "-task_type__name"})
        self.assertEqual(
            list(response.context["task_list"]),
            list(Task.objects.all().order_by("-task_type__name"))
        )

    def test_task_list_sort_by_deadline(self):
        url = reverse("task_manager:task-list")
        response = self.client.get(url, data={"sort": "deadline"})
        self.assertEqual(
            list(response.context["task_list"]),
            list(Task.objects.all().order_by("deadline"))
        )

    def test_task_list_sort_by_priority(self):
        url = reverse("task_manager:task-list")
        response = self.client.get(url, data={"sort": "-priority"})
        self.assertEqual(
            list(response.context["task_list"]),
            list(Task.objects.all().order_by("-priority"))
        )

    def test_task_list_sort_by_status(self):
        url = reverse("task_manager:task-list")
        response = self.client.get(url, data={"sort": "status"})
        self.assertEqual(
            list(response.context["task_list"]),
            list(Task.objects.all().order_by("status"))
        )

    def test_task_list_pagination(self):
        for i in range(7):
            Task.objects.create(
                name=f"task_{i}",
                description=f"description_{i}",
                deadline=get_future_weekday(),
                status="New",
                priority=4,
                task_type=self.task_type,
            )
        url = reverse("task_manager:task-list")
        response = self.client.get(url)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_list"]), 8)

    def test_task_create_returns_200(self):
        url = reverse("task_manager:task-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_create_post_with_valid_data(self):
        form_data = {
            "name": "valid_name",
            "description": "valid_description",
            "deadline": get_future_weekday(),
            "status": "New",
            "priority": 3,
            "task_type": self.task_type.pk,
        }
        response = self.client.post(reverse("task_manager:task-create"), data=form_data)
        new_task = Task.objects.get(name=form_data["name"])
        self.assertEqual(new_task.name, form_data["name"])
        self.assertEqual(new_task.description, form_data["description"])
        self.assertEqual(new_task.deadline, form_data["deadline"])
        self.assertEqual(new_task.status, form_data["status"])
        self.assertEqual(new_task.priority, form_data["priority"])
        self.assertEqual(new_task.task_type.pk, form_data["task_type"])
        self.assertRedirects(response, expected_url=reverse("task_manager:task-list"))

    def test_task_create_post_with_invalid_data(self):
        form_data = {
            "name": "",
            "description": "valid_description",
            "deadline": get_future_weekday(),
            "status": "New",
            "priority": 3,
            "task_type": "",
        }
        response = self.client.post(reverse("task_manager:task-create"), data=form_data)
        new_task = Task.objects.filter(description=form_data["description"])
        self.assertFalse(new_task.exists())
        self.assertEqual(response.status_code, 200)

    def test_task_update_returns_200(self):
        url = reverse("task_manager:task-update", kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_update_get_is_pre_populated(self):
        url = reverse("task_manager:task-update", kwargs={"pk": self.another_task.pk})
        response = self.client.get(url)
        self.assertContains(response, self.another_task.description)

    def test_task_update_post(self):
        form_data = {
            "name": "updated_name",
            "description": "another_description",
            "deadline": get_future_weekday(),
            "status": "Done",
            "priority": 2,
            "task_type": self.task_type.pk,
        }
        response = self.client.post(reverse("task_manager:task-update", kwargs={"pk": self.another_task.pk}), data=form_data)
        self.another_task.refresh_from_db()
        self.assertEqual(self.another_task.name, form_data["name"])
        self.assertRedirects(response, expected_url=reverse("task_manager:task-list"))

    def test_task_delete_returns_200(self):
        url = reverse("task_manager:task-delete", kwargs={"pk": self.another_task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_delete_post(self):
        response = self.client.post(reverse("task_manager:task-delete", kwargs={"pk": self.another_task.pk}))
        another_task = Task.objects.filter(description="another_description")
        self.assertFalse(another_task.exists())
        self.assertRedirects(response, expected_url=reverse("task_manager:task-list"))

    def test_task_detail_returns_200(self):
        url = reverse("task_manager:task-detail", kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_detail_context(self):
        url = reverse("task_manager:task-detail", kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertIn("today", response.context)

    def test_task_add_assignee(self):
        self.assertNotIn(self.worker, self.task.assignees.all())
        url = reverse("task_manager:task-assign", kwargs={"pk": self.task.pk})
        response = self.client.post(url, data={"assignee": self.worker.pk})
        self.assertIn(self.worker, self.task.assignees.all())
        self.assertRedirects(response, reverse("task_manager:task-detail", kwargs={"pk": self.task.pk}))

    def test_task_remove_assignee(self):
       self.task.assignees.add(self.worker)
       url = reverse("task_manager:task-assign", kwargs={"pk": self.task.pk})
       response = self.client.post(url)
       self.assertNotIn(self.worker, self.task.assignees.all())
       self.assertRedirects(response, reverse("task_manager:task-detail", kwargs={"pk": self.task.pk}))

    def test_task_toggle_status(self):
        url = reverse("task_manager:task-toggle-status", kwargs={"pk": self.another_task.pk})
        response = self.client.post(url)
        self.another_task.refresh_from_db()
        self.assertEqual(self.another_task.status, "New")
        self.assertRedirects(response, reverse("task_manager:task-detail", kwargs={"pk": self.another_task.pk}))
