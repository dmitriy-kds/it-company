from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.decorators.http import require_POST

from .forms import WorkerCreationForm, WorkerUpdateForm
from .models import Task, Worker, Position, TaskType


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


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "task_manager/worker_detail.html"
    queryset = Worker.objects.all().select_related("position").prefetch_related("tasks")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        worker = Worker.objects.get(pk=self.kwargs["pk"])
        context["today"] = date.today()
        context["new"] = worker.tasks.filter(status="New")
        context["in_progress"] = worker.tasks.filter(status="In Progress")
        context["done"] = worker.tasks.filter(status="Done")
        return context


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "task_manager/worker_confirm_delete.html"
    success_url = reverse_lazy("task_manager:worker-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    pass


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    pass


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    pass


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    pass


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    pass


@login_required
@require_POST
def task_assign_view(request: HttpRequest) -> HttpResponse:
    pass


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    pass


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    pass


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    pass


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-list")


@login_required
@require_POST
def task_toggle_status_view(request: HttpRequest) -> HttpResponse:
    pass

@login_required
def profile_redirect(request: HttpRequest) -> HttpResponse:
    return redirect("task_manager:worker-detail", pk=request.user.pk)
