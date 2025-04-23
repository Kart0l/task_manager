from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Task


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name_plural = "Profile"
    fk_name = "user"


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "get_role", "is_staff")
    list_filter = ("profile__role", "is_staff")
    list_select_related = ("profile",)

    def get_role(self, instance):
        return instance.profile.get_role_display() if hasattr(instance, "profile") else "No Profile"
    get_role.short_description = "Role"

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


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

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

