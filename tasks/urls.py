from django.urls import path
from . import views
from .views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListByTypeView,
    register,
    profile,
    update_task_status,
    complete_task,
    create_comment,
)

app_name = "tasks"

urlpatterns = [
    path("", TaskListView.as_view(), name="dashboard"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),

    path("task/create/", views.TaskCreateView.as_view(), name="task_create"),
    path("task/<int:pk>/update/", views.TaskUpdateView.as_view(), name="task_update"),
    path("task/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:pk>/update_status/", views.update_task_status, name='update_task_status'),
    path("task/<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("task/<int:pk>/complete/", views.complete_task, name="complete_task"),
    path("task/<int:task_id>/comment/create/", views.create_comment, name="create_comment"),
] 