from django.db import models

from client.models import Client
from communication.models import Communication


class Mailing(models.Model):
    status_choise  = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]
    first_send_time = models.DateTimeField(null=True, blank=True, verbose_name='Начало рассылки')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='Окончание рассылки')
    status = models.CharField(max_length=20, choices=status_choise, default='Создана', verbose_name='Статус')
    communication = models.ForeignKey(Communication, on_delete=models.CASCADE, verbose_name='Сообщение')
    client = models.ManyToManyField(Client, verbose_name='Клиенты')
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

    class Metta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'Рассылка: {self.communication.subject} - {self.status}'


class MailingAttempt(models.Model):
    status_choise = [
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=20, choices=status_choise, verbose_name='Статус ')
    server_response = models.TextField(verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts', verbose_name='Рассылка')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        return f'{self.timestamp} - {self.status}'
