from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from task_manager.models import (
    TaskType,
    Position,
    Task,
    validate_task_deadline
)


class ModelsTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="test")
        self.position = Position.objects.create(name="test")
        self.worker = get_user_model().objects.create_user(
            first_name="test_first",
            last_name="test_last",
            username="test_username",
            password="test123*!",
            email="test_email@email.com",
            position=self.position
        )
        self.task = Task.objects.create(
            name="test_task",
            description="test_description",
            deadline=date.today() + timedelta(days=1),
            status="New",
            priority=2,
            task_type=self.task_type
        )

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), self.task_type.name)

    def test_position_str(self):
        self.assertEqual(str(self.position), self.position.name)

    def test_create_worker_with_position(self):
        self.assertEqual(self.worker.first_name, "test_first")
        self.assertEqual(self.worker.last_name, "test_last")
        self.assertEqual(self.worker.username, "test_username")
        self.assertTrue(self.worker.check_password("test123*!"))
        self.assertEqual(self.worker.email, "test_email@email.com")
        self.assertEqual(self.worker.position, self.position)

    def test_worker_str_with_position(self):
        self.assertEqual(
            str(self.worker),
            f"{self.worker.first_name} "
            f"{self.worker.last_name}, "
            f"{self.worker.position}"
        )

    def test_worker_str_without_position(self):
        self.worker.position = None
        self.assertEqual(
            str(self.worker),
            f"{self.worker.first_name} "
            f"{self.worker.last_name}, "
            f"No position"
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), "test_task")

    def test_validate_task_deadline_raises_with_message_1(self):
        deadline = date.today() - timedelta(days=1)
        expected_message = "Deadline can't be in the past!"
        with self.assertRaises(ValidationError) as context:
            validate_task_deadline(deadline)
        self.assertEqual(context.exception.message, expected_message)

    def test_validate_task_deadline_raises_with_message_2(self):
        deadline = date(2100, 1, 2)
        expected_message = "Can't set deadline beyond 2100-01-01!"
        with self.assertRaises(ValidationError) as context:
            validate_task_deadline(deadline)
        self.assertEqual(context.exception.message, expected_message)

    def test_task_next_status_new(self):
        self.task.status = "New"
        self.assertEqual(self.task.next_status, "In Progress")

    def test_task_next_status_in_progress(self):
        self.task.status = "In Progress"
        self.assertEqual(self.task.next_status, "Done")

    def test_task_next_status_done(self):
        self.task.status = "Done"
        self.assertEqual(self.task.next_status, "New")
