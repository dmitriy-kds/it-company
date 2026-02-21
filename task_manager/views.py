from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import generic

from .models import Task, Worker, Position


def index(request: HttpRequest) -> HttpResponse:
    counter = request.session.get("counter", 0)
    counter += 1
    request.session["counter"] = counter
    context = {
        "num_employees": Worker.objects.count(),
        "num_positions": Position.objects.count(),
        "num_tasks": Task.objects.count(),
        "num_new_tasks": Task.objects.filter(status="New").count(),
        "num_completed_tasks": Task.objects.filter(status="Done").count(),
        "num_in_progress_tasks": Task.objects.filter(status="Done").count(),
        "counter": counter,
    }
    return render(request, template_name="task_manager/index.html", context=context)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "task_manager/worker_list.html"
    paginate_by = 8


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "task_manager/worker_detail.html"
    queryset = Worker.objects.all().select_related("position").prefetch_related("tasks")


class TaskListView(LoginRequiredMixin, generic.ListView):
    pass


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    pass


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    pass


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    pass

class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    template_name = "task_manager/position_list.html"
    paginate_by = 8

class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    template_name = "task_manager/position_detail.html"
    queryset = Position.objects.all().prefetch_related("workers")
