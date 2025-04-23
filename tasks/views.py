from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Task, Comment
from .forms import TaskForm, TaskFilterForm, UserRegisterForm, CommentForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _
from .mixins import AjaxFormMixin, AjaxListMixin, AjaxActionMixin
from .service import TaskService
from django.http import JsonResponse


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "tasks/register.html", {"form": form})


class TaskListView(LoginRequiredMixin, AjaxListMixin, ListView):
    model = Task
    template_name = "tasks/dashboard.html"  #
    context_object_name = "tasks"
    paginate_by = 10
    ajax_template_name = "tasks/task_list_partial.html"

    def get_queryset(self):
        filter_form = TaskFilterForm(self.request.GET)
        return TaskService.get_user_tasks(
            user=self.request.user,
            filters=filter_form.cleaned_data if filter_form.is_valid() else {},
            tab=self.request.GET.get("tab"),
            sort=self.request.GET.get("sort"),
            prefetch=["author", "assignee"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = TaskFilterForm(self.request.GET)
        return context


class TaskCreateView(LoginRequiredMixin, AjaxFormMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:dashboard")
    action_type = "created"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskUpdateView(LoginRequiredMixin, AjaxFormMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:dashboard")
    template_name = "tasks/task_form.html"
    action_type = "updated"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not TaskService.has_task_permission(self.object, request.user, "edit"):
            return self.handle_no_permission()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not TaskService.has_task_permission(self.object, request.user, "edit"):
            return self.handle_no_permission()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.object
        return context


class TaskDeleteView(LoginRequiredMixin, AjaxActionMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:dashboard")

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        if TaskService.has_task_permission(task, request.user, "delete"):
            return super().delete(request, *args, **kwargs)
        return self.error_response(_("Insufficient rights to delete task"), status=403)


@login_required
def profile(request):
    stats = TaskService.get_task_statistics(user=request.user, filter_by="author")
    recent_completed = TaskService.get_user_tasks(
        user=request.user,
        filters={"status": "done"},
        sort="-created_at",
        prefetch=["author", "assignee"]
    )[:5]
    upcoming_deadlines = TaskService.get_user_tasks(
        user=request.user,
        filters={"status__in": ["todo", "in_progress"], "deadline__gte": timezone.now()},
        sort="deadline",
        prefetch=["author", "assignee"]
    )[:5]

    context = {
        "profile": request.user.profile,
        "total_tasks": stats["total_tasks"],
        "completed_tasks": stats["completed_tasks"],
        "in_progress_tasks": stats["in_progress_tasks"],
        "overdue_tasks": stats["overdue_tasks"],
        "priority_stats": stats["priority_stats"],
        "status_stats": stats["status_stats"],
        "recent_completed": recent_completed,
        "upcoming_deadlines": upcoming_deadlines,
    }
    return render(request, "tasks/profile.html", context)


class TaskListByTypeView(LoginRequiredMixin, AjaxListMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10
    ajax_template_name = "tasks/task_list_partial.html"

    def get_queryset(self):
        task_type = self.kwargs["task_type"]
        return TaskService.get_user_tasks(
            user=self.request.user,
            filters={"task_type": task_type},
            prefetch=["tasks", "comments"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_type"] = self.kwargs["task_type"]
        return context


@require_http_methods(["POST"])
@login_required
@csrf_exempt
def update_task_status(request, pk):
    mixin = AjaxActionMixin()
    try:
        task = Task.objects.get(id=pk)
        new_status = request.POST.get("status")
        TaskService.update_task_status(task, new_status, request.user)
        return mixin.success_response(_("Task status updated"))
    except Task.DoesNotExist:
        return mixin.error_response(_("Task not found"), status=404)
    except PermissionError as e:
        return mixin.error_response(e, status=403)
    except ValueError as e:
        return mixin.error_response(e, status=400)
    except Exception as e:
        return mixin.error_response(e, status=500)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context["can_edit"] = TaskService.has_task_permission(task, self.request.user, "update_status")
        return context


@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if TaskService.has_task_permission(task, request.user, "update_status"):
        task.status = "done"
        task.save()
        return redirect("tasks:dashboard")
    return redirect("tasks:dashboard")


@login_required
@require_http_methods(["POST"])
def create_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.task = task
        comment.author = request.user
        comment.save()
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'text': comment.text,
                'author': comment.author.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    
    return JsonResponse({
        'success': False,
        'errors': form.errors
    }, status=400)