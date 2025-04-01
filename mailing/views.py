import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from dotenv import load_dotenv

from client.models import Client
from mailing.forms import MailingForm
from mailing.models import Mailing

load_dotenv()


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=self.request.user)


@method_decorator(cache_page(60 * 15), name="dispatch")
class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing_detail.html"

    # @login_required
    # def disable_mailing(request, mailing_id):
    #     if not can_disable_mailings(request.user):
    #         return redirect("unauthorized")
    #     mailing = get_object_or_404(Mailing, id=mailing_id)
    #     mailing.is_active = False
    #     mailing.save()
    #     return redirect("mailing_list")


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = "/"
    template_name = "mailing_form.html"

    def form_valid(self, form):
        mailing = form.save()
        mailing.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = "/"
    template_name = "mailing_form.html"


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = "/"
    template_name = "mailing_confirm_delete.html"


class SendMailingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        clients = Client.objects.all()
        client_emails = [client.email for client in clients]

        try:
            send_mail(
                subject=mailing.communication.topic,
                message=mailing.communication.links,
                from_email=os.getenv("EMAIL_HOST_USER"),
                recipient_list=client_emails,
                fail_silently=False,
            )
            messages.success(request, "Рассылка успешно отправлена!")
        except Exception as e:
            messages.error(request, f"Ошибка при отправке рассылки: {str(e)}")

        return render(
            request, "result.html", {"message": "Рассылка успешно отправлена!"}
        )


class HomeView(View):
    def get(self, request):
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status="Запущена").count()
        unique_recipients = Client.objects.values("email").distinct().count()

        context = {
            "total_mailings": total_mailings,
            "active_mailings": active_mailings,
            "unique_recipients": unique_recipients,
        }

        return render(request, "home.html", context)


# class EmailStatisticsView(LoginRequiredMixin, ListView):
#     model = EmailStatistics
#     template_name = "email_statistics.html"
#
#     def get_queryset(self):
#         return EmailStatistics.objects.filter(user=self.request.user)
