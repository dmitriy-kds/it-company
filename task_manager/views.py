from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from task_manager.models import Task


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_tasks": Task.objects.count(),
        "num_new_tasks": Task.objects.filter(status="New").count(),
        "num_completed_tasks": Task.objects.filter(status="Done").count(),
        "num_in_progress_tasks": Task.objects.filter(status="Done").count(),
    }
    return render(request, template_name="task_manager/index.html", context=context)
