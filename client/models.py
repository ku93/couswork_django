from django.db import models

from users.models import User


class Client(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Адрес электронной почты",
        help_text="Укажите адрес электронной почты для связи",
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Имя клиента",
        help_text="Укажите имя клиента",
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий клиента",
        help_text="Добавьте любые дополнительные комментарии к клиенту",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата создания продукта",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
        help_text="Дата последнего изменения продукта",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name="Владелец",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.email
