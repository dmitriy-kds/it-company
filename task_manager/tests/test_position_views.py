from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from task_manager.models import Position

class PublicPositionTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="test_position",
        )

    def test_position_list_login_required(self):
        url = reverse("task_manager:position-list")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_position_create_login_required(self):
        url = reverse("task_manager:position-create")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_position_update_login_required(self):
        url = reverse("task_manager:position-update", kwargs={"pk": self.position.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_position_delete_login_required(self):
        url = reverse("task_manager:position-delete", kwargs={"pk": self.position.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)


class PrivatePositionTests(TestCase):
    def setUp(self):
        self.worker = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first",
            last_name="test_last",
            email="test_email",
            password="1234%^&*tyui",
        )
        self.position = Position.objects.create(
            name="test_position",
        )
        self.client.force_login(self.worker)

    def test_position_list_returns_200(self):
        url = reverse("task_manager:position-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_position_list_pagination(self):
        for i in range(8):
            Position.objects.create(
                name=f"position_{i}",
            )
        url = reverse("task_manager:position-list")
        response = self.client.get(url)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["position_list"]), 8)

    def test_position_create_returns_200(self):
        url = reverse("task_manager:position-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_position_create_post_with_valid_data(self):
        form_data = {
            "name": "valid_name"
        }
        response = self.client.post(reverse("task_manager:position-create"), data=form_data)
        new_position = Position.objects.get(name=form_data["name"])
        self.assertEqual(new_position.name, form_data["name"])
        self.assertRedirects(response, expected_url=reverse("task_manager:position-list"))

    def test_position_create_post_with_invalid_data(self):
        form_data = {
            "name": ""
        }
        response = self.client.post(reverse("task_manager:position-create"), data=form_data)
        new_position = Position.objects.filter(name=form_data["name"])
        self.assertFalse(new_position.exists())
        self.assertEqual(response.status_code, 200)

    def test_position_update_returns_200(self):
        url = reverse("task_manager:position-update", kwargs={"pk": self.position.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_position_update_get_is_pre_populated(self):
        url = reverse("task_manager:position-update", kwargs={"pk": self.position.pk})
        response = self.client.get(url)
        self.assertContains(response, self.position.name)

    def test_position_update_post(self):
        form_data = {
            "name": "updated_name"
        }
        response = self.client.post(reverse("task_manager:position-update", kwargs={"pk": self.position.pk}), data=form_data)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, form_data["name"])
        self.assertRedirects(response, expected_url=reverse("task_manager:position-list"))

    def test_position_delete_returns_200(self):
        url = reverse("task_manager:position-delete", kwargs={"pk": self.position.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_position_delete_post(self):
        response = self.client.post(reverse("task_manager:position-delete", kwargs={"pk": self.position.pk}))
        position = Position.objects.filter(name=self.position.name)
        self.assertFalse(position.exists())
        self.assertRedirects(response, expected_url=reverse("task_manager:position-list"))
