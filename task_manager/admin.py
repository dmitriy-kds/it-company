from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from task_manager.models import TaskType, Position, Task, Worker


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
