import os

from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from django.contrib import messages


from client.models import Client
from mailing.models import Mailing, EmailStatistics
from dotenv import load_dotenv

load_dotenv()

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_list.html'

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'

class MailingCreateView(CreateView):
    model = Mailing
    fields = '__all__'
    success_url = '/'
    template_name = 'mailing_form.html'

class MailingUpdateView(UpdateView):
    model = Mailing
    fields = '__all__'
    success_url = '/'
    template_name = 'mailing_form.html'

class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = '/'
    template_name = 'mailing_confirm_delete.html'

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
            messages.success(request, 'Рассылка успешно отправлена!')
        except Exception as e:
            messages.error(request, f'Ошибка при отправке рассылки: {str(e)}')

        return render(request, 'result.html', {'message': 'Рассылка успешно отправлена!'})


class HomeView(View):
    def get(self, request):
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status='Запущена').count()
        unique_recipients = Client.objects.values('email').distinct().count()

        context = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_recipients': unique_recipients,
        }

        return render(request, 'home.html', context)

class EmailStatisticsView(ListView):
    model = EmailStatistics
    template_name = "email_statistics.html"

    def get_queryset(self):
        return EmailStatistics.objects.filter(user=self.request.user)
