from django.test import TestCase

from task_manager.models import TaskType, Position
from task_manager.tests.utils import get_future_weekday, get_future_sunday
from task_manager.forms import (
    WorkerCreationForm,
    TaskCreateForm,
    WorkerUpdateForm,
    TaskNameDescriptionSearchForm,
    WorkerFirstLastNameSearchForm
)


class FormTests(TestCase):
    def setUp(self):
        self.worker_form_data = {
            "username": "test_username",
            "first_name": "test_first",
            "last_name": "test_last",
            "position": None,
            "email": "email@email.com",
            "password1": "123413458ijnnl0*",
            "password2": "123413458ijnnl0*",
        }
        self.task_type = TaskType.objects.create(name="test_task_type")
        self.task_form_data = {
            "name": "test_name",
            "description": "test_description",
            "deadline": get_future_weekday(),
            "status": "New",
            "priority": 1,
            "task_type": self.task_type.pk,
        }

    def test_worker_creation_form_has_position_field(self):
        form = WorkerCreationForm(data=self.worker_form_data)
        self.assertIn("position", form.fields)

    def test_worker_creation_form_with_valid_data(self):
        form = WorkerCreationForm(data=self.worker_form_data)
        self.assertTrue(form.is_valid())

    def test_task_create_form_with_valid_data(self):
        form = TaskCreateForm(data=self.task_form_data)
        self.assertTrue(form.is_valid())

    def test_task_create_form_with_sunday_deadline(self):
        self.task_form_data.update(deadline=get_future_sunday())
        form = TaskCreateForm(data=self.task_form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)

    def test_worker_update_form_with_valid_data(self):
        updated_position = Position.objects.create(name="updated_ position")
        self.worker_form_data.update(position=updated_position.pk)
        form = WorkerUpdateForm(data=self.worker_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(updated_position, form.cleaned_data["position"])

    def test_worker_update_form_with_invalid_data(self):
        self.worker_form_data.update(username="")
        form = WorkerUpdateForm(data=self.worker_form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_task_search_form_is_valid(self):
        form = TaskNameDescriptionSearchForm(
            data={"name_or_description": "test_name"}
        )
        self.assertTrue(form.is_valid())

    def test_worker_search_form_is_valid(self):
        form = WorkerFirstLastNameSearchForm(
            data={"first_or_last_name": "test_last"}
        )
        self.assertTrue(form.is_valid())
