import secrets

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView

from config import settings
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User


class UserCreatorView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
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
            self.update_email_statistics(user, successful=True)
        except Exception:
            self.update_email_statistics(user, successful=False)
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = ""
    user.save()
    return redirect(reverse("users:login"))


class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = "password_reset.html"
    email_template_name = "password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        
        if not active_users.exists():
            return super().form_valid(form)

        # Create custom connection
        from django.core.mail import get_connection, EmailMessage
        connection = get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=False,
            use_ssl=True
        )

        for user in active_users:
            try:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f"{settings.BASE_URL}/users/reset/{uid}/{token}/"

                email = EmailMessage(
                    "Password Reset",
                    f"Hello! To reset your password, please click the link: {reset_url}",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    connection=connection
                )
                email.send()
                
                # self.update_email_statistics(user, successful=True)

            except Exception as e:
                print(f"Failed to send to {user.email}: {str(e)}")
                self.update_email_statistics(user, successful=False)

        connection.close()
        return super().form_valid(form)