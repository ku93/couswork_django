from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from communication.models import Communication


class CommunicationListView(ListView):
    model = Communication
    template_name = "communication_list.html"

    def get_queryset(self):
        communications = cache.get("communication_list")
        if not communications:
            communications = list(Communication.objects.all())
            cache.set("communication_list", communications, timeout=60 * 15)
        return communications


class CommunicationDetailView(DetailView):
    model = Communication
    template_name = "communication_detail.html"

    def get_object(self, queryset=None):
        communication_id = self.kwargs.get("pk")
        communication = cache.get(f"communication_{communication_id}")
        if not communication:
            communication = Communication.objects.get(id=communication_id)
            cache.set(
                f"communication_{communication_id}", communication, timeout=60 * 15
            )
        return communication


class CommunicationCreateView(CreateView):
    model = Communication
    fields = "__all__"
    template_name = "communication_form.html"
    success_url = reverse_lazy("communication:communication_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete("communication_list")
        return response


class CommunicationUpdateView(UpdateView):
    model = Communication
    fields = "__all__"
    template_name = "communication_form.html"
    success_url = reverse_lazy("communication:communication_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        communication_id = self.object.id
        cache.delete(f"communication_{communication_id}")
        cache.delete("communication_list")
        return response


class CommunicationDeleteView(DeleteView):
    model = Communication
    template_name = "communication_confirm_delete.html"
    success_url = reverse_lazy("communication:communication_list")

    def delete(self, request, *args, **kwargs):
        communication_id = self.get_object().id
        response = super().delete(request, *args, **kwargs)
        cache.delete(f"communication_{communication_id}")
        cache.delete("communication_list")
        return response
