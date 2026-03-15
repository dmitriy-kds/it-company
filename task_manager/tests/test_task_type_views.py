from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import TaskType


class PublicTaskTypeTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(
            name="test_task_type",
        )

    def test_task_type_list_login_required(self):
        url = reverse("task_manager:task-type-list")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_task_type_create_login_required(self):
        url = reverse("task_manager:task-type-create")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_task_type_update_login_required(self):
        url = reverse(
            "task_manager:task-type-update",
            kwargs={"pk": self.task_type.pk}
        )
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_task_type_delete_login_required(self):
        url = reverse(
            "task_manager:task-type-delete",
            kwargs={"pk": self.task_type.pk}
        )
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)


class PrivateTaskTypeTests(TestCase):
    def setUp(self):
        self.worker = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first",
            last_name="test_last",
            email="test_email",
            password="1234%^&*tyui",
        )
        self.task_type = TaskType.objects.create(
            name="test_task_type",
        )
        self.client.force_login(self.worker)

    def test_task_type_list_returns_200(self):
        url = reverse("task_manager:task-type-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_type_list_pagination(self):
        for i in range(8):
            TaskType.objects.create(
                name=f"task_type_{i}",
            )
        url = reverse("task_manager:task-type-list")
        response = self.client.get(url)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_type_list"]), 8)

    def test_task_type_create_returns_200(self):
        url = reverse("task_manager:task-type-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_type_create_post_with_valid_data(self):
        form_data = {
            "name": "valid_name"
        }
        response = self.client.post(
            reverse("task_manager:task-type-create"),
            data=form_data
        )
        new_task_type = TaskType.objects.get(name=form_data["name"])
        self.assertEqual(new_task_type.name, form_data["name"])
        self.assertRedirects(
            response,
            expected_url=reverse("task_manager:task-type-list")
        )

    def test_task_type_create_post_with_invalid_data(self):
        form_data = {
            "name": ""
        }
        response = self.client.post(
            reverse("task_manager:task-type-create"),
            data=form_data
        )
        new_task_type = TaskType.objects.filter(name=form_data["name"])
        self.assertFalse(new_task_type.exists())
        self.assertEqual(response.status_code, 200)

    def test_task_type_update_returns_200(self):
        url = reverse(
            "task_manager:task-type-update",
            kwargs={"pk": self.task_type.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_type_update_get_is_pre_populated(self):
        url = reverse(
            "task_manager:task-type-update",
            kwargs={"pk": self.task_type.pk}
        )
        response = self.client.get(url)
        self.assertContains(response, self.task_type.name)

    def test_task_type_update_post(self):
        form_data = {
            "name": "updated_name"
        }
        response = self.client.post(
            reverse(
                "task_manager:task-type-update",
                kwargs={"pk": self.task_type.pk}
            ),
            data=form_data
        )
        self.task_type.refresh_from_db()
        self.assertEqual(self.task_type.name, form_data["name"])
        self.assertRedirects(
            response,
            expected_url=reverse("task_manager:task-type-list")
        )

    def test_task_type_delete_returns_200(self):
        url = reverse(
            "task_manager:task-type-delete",
            kwargs={"pk": self.task_type.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_type_delete_post(self):
        response = self.client.post(
            reverse(
                "task_manager:task-type-delete",
                kwargs={"pk": self.task_type.pk}
            )
        )
        task_type = TaskType.objects.filter(name=self.task_type.name)
        self.assertFalse(task_type.exists())
        self.assertRedirects(
            response,
            expected_url=reverse("task_manager:task-type-list")
        )
