from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from client.forms import ClientForm
from client.models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client/client_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=self.request.user)


@method_decorator(cache_page(60 * 15), name="dispatch")
class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("client:client_list")

    def form_valid(self, form):
        client = form.save()
        client.owner = self.request.user
        return super().form_valid(form)

    # @login_required
    # def create_client(request):
    #     if request.method == "POST":
    #         name = request.POST["name"]
    #         email = request.POST["email"]
    #         Client.objects.create(name=name, email=email, created_by=request.user)
    #         return redirect("client_list")
    #     return render(request, "create_client.html")


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("client:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("client:client_list")
