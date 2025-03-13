from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from communication.models import Communication


class CommunicationListView(ListView):
    model = Communication
    template_name = 'communication_list.html'

class CommunicationDetailView(DetailView):
    model = Communication
    template_name = 'communication_detail.html'

class CommunicationCreateView(CreateView):
    model = Communication
    fields = '__all__'
    template_name = 'communication_form.html'
    success_url = reverse_lazy('communication:communication_list')


class CommunicationUpdateView(UpdateView):
    model = Communication
    fields = '__all__'
    template_name = 'communication_form.html'
    success_url = reverse_lazy('communication:communication_list')

class CommunicationDeleteView(DeleteView):
    model = Communication
    template_name = 'communication_confirm_delete.html'
    success_url = reverse_lazy('communication:communication_list')



