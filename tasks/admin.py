from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "assignee", "task_type", "status", "priority", "deadline", "created_at")
    list_filter = ("status", "task_type", "priority", "author", "assignee", "created_at", "deadline")
    search_fields = ("title", "description")
    date_hierarchy = "created_at"
    list_select_related = ("author", "assignee")
    list_editable = ("status", "priority", "assignee")
    ordering = ("-created_at",)
    actions = ["mark_as_done"]

    def task_type_colored(self, obj):
        color = obj.get_task_type_color()
        return f'<span style="color: {color};">{obj.get_task_type_display()}</span>'
    task_type_colored.short_description = "Task Type"
    task_type_colored.allow_tags = True

    def mark_as_done(self, request, queryset):
        queryset.update(status="done")
    mark_as_done.short_description = "Mark as done"

