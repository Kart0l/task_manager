from django.db.models import Q, Count
from django.utils import timezone
from .models import Task
from core.standard_values import STATUS_CHOICES
from accounts.models import Profile

class TaskService:

    @staticmethod
    def get_user_tasks(user, filters=None, tab=None, sort=None, prefetch=None):
        filters = filters or {}
        prefetch = prefetch or []

        queryset = Task.objects.filter(
            Q(author=user) | Q(assignee=user)
        ).distinct()


        if tab == "created":
            queryset = queryset.filter(author=user)
        elif tab == "assigned":
            queryset = queryset.filter(assignee=user)

        if filters.get("status"):
            queryset = queryset.filter(status=filters["status"])
        if filters.get("assignee"):
            queryset = queryset.filter(assignee=filters["assignee"])
        if filters.get("priority"):
            queryset = queryset.filter(priority=filters["priority"])
        if filters.get("task_type"):
            queryset = queryset.filter(task_type=filters["task_type"])
        if filters.get("date_from"):
            queryset = queryset.filter(deadline__gte=filters["date_from"])
        if filters.get("date_to"):
            queryset = queryset.filter(deadline__lte=filters["date_to"])
        if filters.get("search"):
            queryset = queryset.filter(
                Q(title__icontains=filters["search"]) |
                Q(description__icontains=filters["search"])
            )

        if sort:
            queryset = queryset.order_by(sort)

        if prefetch:
            queryset = queryset.prefetch_related(*prefetch)

        return queryset


    @staticmethod
    def has_task_permission(task, user, permission_type):
        print(
            f"Checking permission for user {user.username}, task {task.title}, type {permission_type}")  # Діагностика
        try:
            if permission_type == "delete":
                return user == task.author or user.profile.role == "pm"
            elif permission_type == "update_status":
                return user == task.assignee or user.profile.role == "pm"
            elif permission_type == "edit":
                return user == task.author or user == task.assignee or user.profile.role == "pm"
        except Profile.DoesNotExist:
            print(f"User {user.username} has no profile")
            return False
        return False


    @staticmethod
    def update_task_status(task, new_status, user):
        if not TaskService.has_task_permission(task, user, "update_status"):
            raise PermissionError("Insufficient rights to change task status")
        if new_status not in dict(STATUS_CHOICES):
            raise ValueError("Invalid task status")
        task.status = new_status
        task.save()

    @staticmethod
    def get_task_statistics(user, filter_by="author"):
        base_filter = {filter_by: user}
        tasks = Task.objects.filter(**base_filter)

        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status="done").count()
        in_progress_tasks = tasks.filter(status="in_progress").count()
        overdue_tasks = tasks.filter(
            status__in=["todo", "in_progress"],
            deadline__lt=timezone.now()
        ).count()

        priority_stats = tasks.values("priority").annotate(count=Count("priority"))
        priority_stats = {item["priority"]: item["count"] for item in priority_stats}

        status_stats = tasks.values("status").annotate(count=Count("status"))
        status_stats = {item["status"]: item["count"] for item in status_stats}

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "overdue_tasks": overdue_tasks,
            "priority_stats": priority_stats,
            "status_stats": status_stats,
        }