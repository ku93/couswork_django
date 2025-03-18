from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('manager', 'Менеджер'),
    ]
    username = None
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Номер телефона")
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар")
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="Страна")
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email