from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TaskForm
from .models import Task


def task_list(request):
    """タスクの一覧表示と新規登録を担当する。"""
    tasks = Task.objects.all()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks:list")
    else:
        form = TaskForm()

    return render(request, "tasks/task_list.html", {"tasks": tasks, "form": form})


@require_POST
def task_toggle(request, pk):
    """指定されたタスクの完了状態を反転する。"""
    task = get_object_or_404(Task, pk=pk)
    task.is_done = not task.is_done
    task.save(update_fields=["is_done"])
    return redirect("tasks:list")


@require_POST
def task_delete(request, pk):
    """指定されたタスクを削除する。"""
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect("tasks:list")
