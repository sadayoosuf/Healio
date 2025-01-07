from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model for authentication with roles
class CustomUser(AbstractUser):
    address = models.TextField(default="")
    phone = models.IntegerField(default=0)

    is_admin = models.BooleanField(default=False)  # For Admin
    is_doctor = models.BooleanField(default=False)  # For Doctor
    is_patient = models.BooleanField(default=False)  # For Patient

    # Resolving reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True
    )

    def __str__(self):
        return self.username
