from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicProfileTests(TestCase):
    def test_profile_login_required(self):
        self.worker = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first",
            last_name="test_last",
            email="test_email",
            password="1234%^&*tyui",
        )
        url = reverse("profile")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

class PrivateProfileTests(TestCase):
    def test_profile_redirect(self):
        self.worker = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first",
            last_name="test_last",
            email="test_email",
            password="1234%^&*tyui",
        )
        self.client.force_login(self.worker)
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, reverse("task_manager:worker-detail", kwargs={"pk": self.worker.pk}))
