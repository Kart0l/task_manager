from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from .forms import UserRegisterForm
from .models import Profile
from tasks.service import TaskService


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("tasks:dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend="django.contrib.auth.backends.ModelBackend")
        return response


class ProfileView(LoginRequiredMixin, View):
    template_name = "accounts/profile.html"

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        
        # Get statistics for the user
        stats = TaskService.get_task_statistics(user)
        
        context = {
            "user": user,
            "profile": profile,
            "total_tasks": stats["total_tasks"],
            "completed_tasks": stats["completed_tasks"],
            "in_progress_tasks": stats["in_progress_tasks"],
            "overdue_tasks": stats["overdue_tasks"],
            "priority_stats": stats.get("priority_stats", {}),
            "status_stats": stats.get("status_stats", {}),
        }

        return render(request, self.template_name, context)
