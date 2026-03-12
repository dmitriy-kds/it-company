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


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "deadline",
        "status",
        "priority",
        "task_type"
    ]
    list_filter = ["status", "priority", "task_type"]
    search_fields = ["name", "description"]


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "position"
    ]
    list_filter = ["position"]
    search_fields = ["username", "first_name", "last_name"]
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("position", )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("position", )}),
    )
