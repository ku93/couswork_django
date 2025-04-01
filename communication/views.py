from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from communication.forms import CommunicationForm
from communication.models import Communication


class CommunicationListView(LoginRequiredMixin, ListView):
    model = Communication
    template_name = "communication_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=self.request.user)


@method_decorator(cache_page(60 * 15), name="dispatch")
class CommunicationDetailView(LoginRequiredMixin, DetailView):
    model = Communication
    template_name = "communication_detail.html"


class CommunicationCreateView(LoginRequiredMixin, CreateView):
    model = Communication
    form_class = CommunicationForm
    template_name = "communication_form.html"
    success_url = reverse_lazy("communication:communication_list")

    def form_valid(self, form):
        communication = form.save()
        communication.owner = self.request.user
        return super().form_valid(form)


class CommunicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Communication
    form_class = CommunicationForm
    template_name = "communication_form.html"
    success_url = reverse_lazy("communication:communication_list")


class CommunicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Communication
    template_name = "communication_confirm_delete.html"
    success_url = reverse_lazy("communication:communication_list")
