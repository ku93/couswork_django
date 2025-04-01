from django.db import models

from users.models import User


class Communication(models.Model):
    topic = models.CharField(
        max_length=100,
        verbose_name="Тема сообщения",
        help_text="Укажите тему сообщения",
    )
    links = models.TextField(
        verbose_name="Текст сообщения", help_text="Добавьте текст сообщения"
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
        related_name="communications",
        verbose_name="Владелец",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщенния"

    def __str__(self):
        return self.topic
