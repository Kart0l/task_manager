from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from accounts.models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Signal triggered for user profile creation
    if not hasattr(instance, "profile"):
        Profile.objects.get_or_create(user=instance, defaults={"role": "user"})
