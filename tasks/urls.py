from django.urls import path
from . import views
from .views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListByTypeView,
    UpdateTaskStatusView,
    CompleteTaskView,
    CreateCommentView,
)

app_name = "tasks"

urlpatterns = [
    path("", TaskListView.as_view(), name="dashboard"),
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:pk>/update_status/", UpdateTaskStatusView.as_view(), name='update_task_status'),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/<int:pk>/complete/", CompleteTaskView.as_view(), name="complete_task"),
    path("tasks/<int:task_id>/comment/create/", CreateCommentView.as_view(), name="create_comment"),
] 