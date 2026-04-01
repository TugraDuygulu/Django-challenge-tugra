from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render

from .forms import TaskForm
from .models import Task

SAMPLE_TASKS = [
    {
        "id": 1,
        "title": "Read Django docs",
        "description": "Understand models, views, and templates",
        "is_completed": False,
    },
    {
        "id": 2,
        "title": "Practice CRUD",
        "description": "Implement create, edit, delete, and list",
        "is_completed": True,
    },
]


def _get_sample_task(task_id: int) -> dict[str, object]:
    for task in SAMPLE_TASKS:
        if task["id"] == task_id:
            return task
    raise Http404("Task not found")


def task_list(request: HttpRequest) -> HttpResponse:
    return render(request, "tasks/task_list.html", {"tasks": Task.objects.all()})


def task_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(
        request,
        "tasks/task_form.html",
        {"form": form, "page_title": "Create Task", "submit_label": "Create"},
    )


def task_edit(request: HttpRequest, task_id: int) -> HttpResponse:
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404("Task not found")

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "tasks/task_form.html",
        {"form": form, "page_title": "Edit Task", "submit_label": "Save"},
    )


def task_delete(request: HttpRequest, task_id: int) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404("Task not found")

    task.delete()
    return redirect("task_list")
