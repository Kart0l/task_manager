from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Task, Comment
from .forms import TaskForm, TaskFilterForm, CommentForm
from django.utils.translation import gettext_lazy as _
from .mixins import AjaxFormMixin, AjaxListMixin, AjaxActionMixin
from .service import TaskService
from django.http import JsonResponse
from core.standard_values import STATUS_CHOICES


class UpdateTaskStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if TaskService.has_task_permission(task, request.user, "update_status"):
            new_status = request.POST.get("status")
            if new_status in dict(STATUS_CHOICES):
                task.status = new_status
                task.save()
                return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error"}, status=400)


class CompleteTaskView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.assignee == request.user or request.user.profile.role == "pm":
            task.status = "done"
            task.save()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error"}, status=400)


class CreateCommentView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return JsonResponse({
                "status": "success",
                "comment": {
                    "text": comment.text,
                    "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
                    "user": comment.author.username
                }
            })
        return JsonResponse({"status": "error"}, status=400)


class TaskListView(LoginRequiredMixin, AjaxListMixin, ListView):
    model = Task
    template_name = "tasks/dashboard.html"  
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



class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context["can_edit"] = TaskService.has_task_permission(task, self.request.user, "update_status")
        return context
