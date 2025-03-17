import secrets

from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from mailing.models import EmailStatistics
from users.forms import UserRegisterForm
from users.models import User


class UserCreatorView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"

        try:
            send_mail(
                subject="Подтверждение почты",
                message=f"Привет! Перейди по ссылке для подтверждения регистрации: {url}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            # Увеличиваем счетчик успешных попыток
            self.update_email_statistics(user, successful=True)
        except Exception as e:
            # Увеличиваем счетчик неуспешных попыток
            self.update_email_statistics(user, successful=False)

        return super().form_valid(form)

    @transaction.atomic
    def update_email_statistics(self, user, successful):
        stats, created = EmailStatistics.objects.get_or_create(user=user)

        if successful:
            stats.successful_attempts += 1
        else:
            stats.failed_attempts += 1

        stats.total_sent += 1
        stats.save()


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


