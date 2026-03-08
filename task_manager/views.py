from datetime import date
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST

from .forms import WorkerCreationForm, WorkerUpdateForm, TaskNameDescriptionSearchForm, WorkerFirstLastNameSearchForm, \
    TaskCreateForm
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

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        first_or_last_name = self.request.GET.get("first_or_last_name", "")
        context["search_form"] = WorkerFirstLastNameSearchForm(initial={"first_or_last_name": first_or_last_name})
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Worker.objects.all().select_related("position").prefetch_related("tasks")
        form = WorkerFirstLastNameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                Q(first_name__icontains=form.cleaned_data["first_or_last_name"]) | Q(last_name__icontains=form.cleaned_data["first_or_last_name"])
            )
        return queryset

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
    model = Task
    context_object_name = "task_list"
    template_name = "task_manager/task_list.html"
    queryset = Task.objects.all().select_related("task_type").prefetch_related("assignees")
    paginate_by = 8

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskListView, self).get_context_data(**kwargs)
        context["today"] = date.today()
        name_or_description = self.request.GET.get("name_or_description", "")
        context["search_form"] = TaskNameDescriptionSearchForm(initial={"name_or_description": name_or_description})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get("sort", "deadline")
        form = TaskNameDescriptionSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                Q(name__icontains=form.cleaned_data["name_or_description"]) | Q(description__icontains=form.cleaned_data["name_or_description"]),
            )

        allowed_sorts = [
            "name", "-name",
            "task_type__name", "-task_type__name",
            "deadline", "-deadline",
            "priority", "-priority",
            "status", "-status"
        ]
        if sort_by in allowed_sorts:
            return queryset.order_by(sort_by)

        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    template_name = "task_manager/task_form.html"
    success_url = reverse_lazy("task_manager:task-list")
    form_class = TaskCreateForm


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["today"] = date.today()
        return context

class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    template_name = "task_manager/task_form.html"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/task_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-list")


@login_required
@require_POST
def task_assign_view(request: HttpRequest, pk: int):
    user = request.user
    task = Task.objects.get(pk=pk)
    if user in task.assignees.all():
        task.assignees.remove(user)
    else:
        task.assignees.add(user)
    return redirect("task_manager:task-detail", pk=pk)


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    template_name = "task_manager/position_list.html"
    queryset = Position.objects.all()
    paginate_by = 8


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    template_name = "task_manager/position_form.html"
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    template_name = "task_manager/position_form.html"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "task_manager/position_confirm_delete.html"
    success_url = reverse_lazy("task_manager:position-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "task_manager/task_type_list.html"
    queryset = TaskType.objects.all()
    paginate_by = 8


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-type-list")


@login_required
@require_POST
def task_toggle_status_view(request: HttpRequest, pk: int) -> HttpResponse:
    task = Task.objects.get(pk=pk)
    task.status = task.next_status
    task.save(update_fields=["status"])
    return redirect("task_manager:task-detail", pk=pk)


@login_required
def profile_redirect(request: HttpRequest) -> HttpResponse:
    return redirect("task_manager:worker-detail", pk=request.user.pk)

