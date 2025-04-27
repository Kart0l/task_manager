from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Profile
from core.mixins import BootstrapFormMixin
from core.standard_values import ROLE_CHOICES


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
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={"role": self.cleaned_data["role"]}
            )
            if not created:
                profile.role = self.cleaned_data["role"]
                profile.save()
        return user 