from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.standard_values import STATUS_CHOICES, PRIORITY_CHOICES, TASK_TYPE_CHOICES, TASK_TYPE_COLORS
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authored_tasks",
        verbose_name=_("Author")
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
        verbose_name=_("Assignee")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="todo",
        verbose_name=_("Status")
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
        verbose_name=_("Priority")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    deadline = models.DateTimeField(verbose_name=_("Deadline"))
    task_type = models.CharField(
        max_length=50,
        choices=TASK_TYPE_CHOICES,
        default="bug",
        blank=True,
        verbose_name=_("Task Type")
    )

    def get_task_type_color(self):
        return TASK_TYPE_COLORS.get(self.task_type, "#000000")

    def __str__(self):
        return self.title

    def is_overdue(self):
        return self.deadline < timezone.now() and self.status != "done"


    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ["-created_at"]


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Task")
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Author")
    )
    text = models.TextField(verbose_name=_("Text"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]
