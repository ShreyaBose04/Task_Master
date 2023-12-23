from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    new_user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", null=True, blank=True
    )
    auth_token = models.CharField(max_length=1000, default="")
    username = models.CharField(max_length=1000, default="")
    password = models.CharField(max_length=1000, default="")
    email = models.EmailField(default="")
    is_verified = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.new_user:
            return self.new_user.username
        else:
            return "nom"
