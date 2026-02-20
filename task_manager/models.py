from django.contrib.auth.models import AbstractUser
from django.db import models

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
        verbose_name_plural = "task types"

    def __str__(self):
        return self.name
