from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    
    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15, blank=True, null=True)

    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    bio = models.TextField(blank=True, null=True)

    is_online = models.BooleanField(default=False)

    last_seen = models.DateTimeField(blank=True, null=True)
     # 🔥 IMPORTANT: login will use email instead of username
    USERNAME_FIELD = "email"

    # Required when USERNAME_FIELD is changed
    REQUIRED_FIELDS = ["username", "first_name"]

    def __str__(self):
        return self.email

    class Meta:
        db_table = "custom_users"