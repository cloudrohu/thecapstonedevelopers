from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    username = None

    ROLE_CHOICES = [
        ("super_admin", "Super Admin"),
        ("company_admin", "Company Admin"),
        ("sales_manager", "Sales Manager"),
        ("sales_executive", "Sales Executive"),
        ("marketing", "Marketing"),
        ("accounts", "Accounts"),
        ("support", "Support"),
        ("employee", "Employee"),
    ]

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default="employee",
    )

    profile_photo = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True,
    )

    is_email_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["-id"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()