from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegisterForm
from core.standard_values import ROLE_CHOICES


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        # Get or create profile instead of always creating
        self.profile, created = Profile.objects.get_or_create(
            user=self.user,
            defaults={"role": "developer"}
        )
        if not created and self.profile.role != "developer":
            self.profile.role = "developer"
            self.profile.save()

    def tearDown(self):
        self.user.delete()

    def test_profile_creation(self):
        self.assertEqual(self.profile.role, "developer")
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertTrue(hasattr(self.user, "profile"))
    
    def test_profile_str_method(self):
        expected_str = f"{self.user.username} - {self.profile.get_role_display()}"
        self.assertEqual(str(self.profile), expected_str)


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("accounts:register")
    
    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertIsInstance(response.context['form'], UserRegisterForm)
    
    def test_register_view_post_valid(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "complex_password123",
            "password2": "complex_password123",
            "role": "developer"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        
        # Verify user and profile were created correctly
        user = User.objects.first()
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertEqual(user.profile.role, "developer")
    
    def test_register_view_post_invalid(self):
        data = {
            "username": "newuser",
            "email": "invalid_email",  # Invalid email
            "password1": "pass",       # Too short
            "password2": "different",  # Doesn't match
            "role": "developer"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)  # Form is displayed again with errors
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)
        self.assertFalse(response.context['form'].is_valid())


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        # Get or create profile instead of always creating
        self.profile, created = Profile.objects.get_or_create(
            user=self.user,
            defaults={"role": "developer"}
        )
        if not created and self.profile.role != "developer":
            self.profile.role = "developer"
            self.profile.save()
            
        self.profile_url = reverse("accounts:profile")
        self.client.login(username="testuser", password="testpass123")
    
    def test_profile_view_authenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['profile'], self.profile)
    
    def test_profile_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
