from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

class PublicWorkerTests(TestCase):
    def setUp(self):
       self.worker = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first",
            last_name="test_last",
            email="test_email",
        )

    def test_worker_list_login_required(self):
        url = reverse("task_manager:worker-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_worker_create_login_required(self):
        url = reverse("task_manager:worker-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_worker_detail_login_required(self):
        url = reverse("task_manager:worker-detail", kwargs={"pk": self.worker.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_worker_update_login_required(self):
        url = reverse("task_manager:worker-update", kwargs={"pk": self.worker.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_worker_delete_login_required(self):
        url = reverse("task_manager:worker-delete", kwargs={"pk": self.worker.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class PrivateWorkerTests(TestCase):
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
        self.client.force_login(self.worker)

    def test_worker_list_returns_200(self):
        url = reverse("task_manager:worker-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_worker_list_search_by_first_name(self):
        url = reverse("task_manager:worker-list")
        response = self.client.get(url, data={"first_or_last_name": self.another_worker.first_name})
        self.assertContains(response, self.another_worker.last_name)
        self.assertNotContains(response, self.worker.last_name)

    def test_worker_list_search_by_last_name(self):
        url = reverse("task_manager:worker-list")
        response = self.client.get(url, data={"first_or_last_name": self.another_worker.last_name})
        self.assertContains(response, self.another_worker.first_name)
        self.assertNotContains(response, self.worker.first_name)

    def test_worker_create_returns_200(self):
        url = reverse("task_manager:worker-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_worker_create_post_with_valid_data(self):
        form_data = {
            "username": "john_doe",
            "first_name": "john",
            "last_name": "doe",
            "email": "email@email.com",
            "password1": "123413458ijnnl0*",
            "password2": "123413458ijnnl0*",
        }
        response = self.client.post(reverse("task_manager:worker-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.username, form_data["username"])
        self.assertEqual(new_user.email, form_data["email"])
        self.assertRedirects(response, expected_url=reverse("task_manager:worker-list"))

    def test_worker_create_post_with_invalid_data(self):
        form_data = {
            "username": "john_doe",
            "first_name": "john",
            "last_name": "doe",
            "email": "email@email.com",
            "password1": "1234",
            "password2": "1234",
        }
        response = self.client.post(reverse("task_manager:worker-create"), data=form_data)
        new_user = get_user_model().objects.filter(username=form_data["username"])
        self.assertFalse(new_user.exists())
        self.assertEqual(response.status_code, 200)

    def test_worker_update_returns_200(self):
        url = reverse("task_manager:worker-update", kwargs={"pk": self.another_worker.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_worker_update_get_is_pre_populated(self):
        url = reverse("task_manager:worker-update", kwargs={"pk": self.another_worker.pk})
        response = self.client.get(url)
        self.assertContains(response, self.another_worker.last_name)

    def test_worker_update_post(self):
        form_data = {
            "username": "updated",
        }
        response = self.client.post(reverse("task_manager:worker-update", kwargs={"pk": self.another_worker.pk}), data=form_data)
        self.another_worker.refresh_from_db()
        self.assertEqual(self.another_worker.username, form_data["username"])
        self.assertRedirects(response, expected_url=reverse("task_manager:worker-list"))

    def test_worker_delete_returns_200(self):
        url = reverse("task_manager:worker-delete", kwargs={"pk": self.another_worker.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_worker_delete_post(self):
        response = self.client.post(reverse("task_manager:worker-delete", kwargs={"pk": self.another_worker.pk}))
        another_worker = get_user_model().objects.filter(username="another_username")
        self.assertFalse(another_worker.exists())
        self.assertRedirects(response, expected_url=reverse("task_manager:worker-list"))

    def test_worker_detail_returns_200(self):
        url = reverse("task_manager:worker-detail", kwargs={"pk": self.worker.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_worker_detail_context(self):
        url = reverse("task_manager:worker-detail", kwargs={"pk": self.worker.pk})
        response = self.client.get(url)
        self.assertIn("today", response.context)
        self.assertIn("new", response.context)
        self.assertIn("in_progress", response.context)
        self.assertIn("done", response.context)
