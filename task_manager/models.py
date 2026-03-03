from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from it_company import settings


def validate_task_deadline(date):
    latest_deadline = datetime.strptime(
        "2100-01-01", "%Y-%m-%d"
    ).date()
    today = date.today()
    yesterday = today - timedelta(days=1)
    if yesterday > date:
        raise ValidationError(
            f"Deadline can't be in the past!"
        )
    elif date > latest_deadline:
        raise ValidationError(
            f"Can't set deadline beyond {latest_deadline}!"
        )

class TaskType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "task types"

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "positions"

    def __str__(self):
        return self.name

class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name="workers")

    class Meta:
        ordering = ["last_name"]
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        pos = self.position.name if self.position else "No position"
        return f"{self.first_name} {self.last_name}, {pos}"

class Task(models.Model):
    PRIORITY_CHOICES = (
        (4, "Urgent"),
        (3, "High Priority"),
        (2, "Medium Priority"),
        (1, "Low Priority"),
    )
    STATUS_CHOICES = (
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Done", "Done"),
    )


    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    deadline = models.DateField(validators=[validate_task_deadline])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="New")
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="tasks")

    class Meta:
        ordering = ["deadline", "-priority"]
        verbose_name = "task"
        verbose_name_plural = "tasks"

    def __str__(self):
        return self.name

    @property
    def next_status(self) -> str:
        status_map = {
            "New": "In Progress",
            "In Progress": "Done",
            "Done": "New",
        }
        return status_map[self.status]
