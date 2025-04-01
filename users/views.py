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
    subject_template_name = "password_reset_subject.txt"
    success_url = reverse_lazy("users:password_reset_done")

    def form_valid(self, form):
        print("Form is valid")  # Check if this prints
        email = form.cleaned_data["email"]
        print(f"Processing email: {email}")  # Verify the email
        # return super().form_valid(form)

        active_users = User.objects.filter(email__iexact=email, is_active=True)
        response = super().form_valid(form)
        for user in active_users:
            try:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f"{settings.BASE_URL}/password-reset/{uid}/{token}/"

                # Send email using your custom format
                send_mail(
                    subject="Восстановление пароля",
                    message=f"Привет! Для сброса пароля перейди по ссылке: {reset_url}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )

                print(f"Password reset email sent to {user.email}")  # Debug print
                self.update_email_statistics(user, successful=True)

            except Exception as e:
                print(f"Failed to send email to {user.email}: {str(e)}")  # Debug print
                self.update_email_statistics(user, successful=False)

        # Still return the original response to maintain the flow
        return super().form_valid(form)

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        print(subject_template_name, email_template_name, context, from_email, to_email)
        """
        Override the default send_mail to use our custom implementation
        """
        subject = self.render_subject(subject_template_name, context)
        message = self.render_email_body(email_template_name, context)

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[to_email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Failed to send password reset email: {e}")
            return False

    def render_subject(self, template_name, context):
        from django.template.loader import render_to_string

        return render_to_string(template_name, context).strip()

    def render_email_body(self, template_name, context):
        from django.template.loader import render_to_string

        return render_to_string(template_name, context)
