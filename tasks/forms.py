from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Task, Profile, Comment
from .mixins import BootstrapFormMixin
from .standart_value import ROLE_CHOICES, STATUS_CHOICES, PRIORITY_CHOICES, TASK_TYPE_CHOICES


class UserRegisterForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(label=_("E-mail"))
    role = forms.ChoiceField(choices=ROLE_CHOICES, label=_("Role"))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("This email is already in use."))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(user=user, role=self.cleaned_data["role"])
        return user


class TaskForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "assignee", "status", "priority", "deadline", "task_type"]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["assignee"].queryset = User.objects.filter(profile__isnull=False)
        self.fields["assignee"].required = False
        if user and not self.instance.pk:
            self.fields["assignee"].initial = user

    def clean_assignee(self):
        assignee = self.cleaned_data.get("assignee")
        user = self.initial.get("user")
        if user and user.profile.role != "pm" and assignee != user:
            raise forms.ValidationError(_("Only a manager can assign other performers."))
        return assignee


class TaskFilterForm(BootstrapFormMixin, forms.Form):
    status = forms.ChoiceField(choices=[("", _("All"))] + STATUS_CHOICES, required=False)
    priority = forms.ChoiceField(choices=[("", _("All"))] + PRIORITY_CHOICES, required=False)
    task_type = forms.ChoiceField(choices=[("", _("All"))] + TASK_TYPE_CHOICES, required=False)
    assignee = forms.ModelChoiceField(queryset=User.objects.all(), required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }