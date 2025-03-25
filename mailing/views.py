import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from dotenv import load_dotenv

from client.models import Client
from mailing.models import EmailStatistics, Mailing
from users.views import can_disable_mailings, can_view_all_mailings

load_dotenv()


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing_list.html"

    @login_required
    def mailing_list(request):
        if can_view_all_mailings(request.user):
            mailings = Mailing.objects.all()
        else:
            mailings = Mailing.objects.filter(created_by=request.user)
        return render(request, "mailing_list.html", {"mailings": mailings})


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing_detail.html"

    @login_required
    def disable_mailing(request, mailing_id):
        if not can_disable_mailings(request.user):
            return redirect("unauthorized")
        mailing = get_object_or_404(Mailing, id=mailing_id)
        mailing.is_active = False
        mailing.save()
        return redirect("mailing_list")


class MailingCreateView(CreateView):
    model = Mailing
    fields = "__all__"
    success_url = "/"
    template_name = "mailing_form.html"

    @login_required
    def create_mailing(request):
        if request.method == "POST":
            subject = request.POST["subject"]
            message = request.POST["message"]
            Mailing.objects.create(
                subject=subject, message=message, created_by=request.user
            )
            return redirect("mailing_list")
        return render(request, "create_mailing.html")


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = "__all__"
    success_url = "/"
    template_name = "mailing_form.html"


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = "/"
    template_name = "mailing_confirm_delete.html"


class SendMailingView(View):
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


class EmailStatisticsView(ListView):
    model = EmailStatistics
    template_name = "email_statistics.html"

    def get_queryset(self):
        return EmailStatistics.objects.filter(user=self.request.user)
