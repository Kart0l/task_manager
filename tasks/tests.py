from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Task, Profile, Comment
from .forms import TaskForm
from .standart_value import STATUS_CHOICES, PRIORITY_CHOICES, TASK_TYPE_CHOICES
import datetime


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        if not hasattr(self.user, "profile"):
            self.profile = Profile.objects.create(
                user=self.user,
                role="developer"
            )
        else:
            self.profile = self.user.profile
        self.client = Client()
        self.client.login(username="testuser", password="testpass123")

    def tearDown(self):
        self.user.delete()


class TaskModelTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            author=self.user,
            status="todo",
            priority="medium",
            deadline=timezone.now() + datetime.timedelta(days=1),
            task_type="bug"
        )

    def tearDown(self):
        self.task.delete()
        super().tearDown()

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.status, "todo")
        self.assertEqual(self.task.author, self.user)

    def test_task_is_overdue(self):
        self.assertFalse(self.task.is_overdue())
        self.task.deadline = timezone.now() - datetime.timedelta(days=1)
        self.assertTrue(self.task.is_overdue())


class ProfileModelTest(BaseTestCase):
    def test_profile_creation(self):
        self.profile.role = "developer"
        self.profile.save()
        self.assertEqual(self.profile.role, "developer")
        self.assertEqual(self.profile.user.username, "testuser")


class ViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            author=self.user,
            status="todo",
            priority="medium",
            deadline=timezone.now() + datetime.timedelta(days=1),
            task_type="bug"
        )

    def tearDown(self):
        self.task.delete()
        super().tearDown()

    def test_dashboard_view(self):
        response = self.client.get(reverse("tasks:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/dashboard.html")

    def test_task_detail_view(self):
        self.task.assignee = self.user
        self.task.save()
        response = self.client.get(reverse("tasks:task_detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_detail.html")

    def test_complete_task_view(self):
        self.task.assignee = self.user
        self.task.save()
        response = self.client.get(reverse("tasks:complete_task", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect status
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "done")
