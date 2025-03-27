from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from client.models import Client


class ClientListView(ListView):
    model = Client
    template_name = "client/client_list.html"

    def get_queryset(self):
        clients = cache.get("client_list")
        if not clients:
            clients = list(Client.objects.all())
            cache.set("client_list", clients, timeout=60 * 15)
        return clients


class ClientDetailView(DetailView):
    model = Client

    def get_object(self, queryset=None):
        client_id = self.kwargs.get("pk")
        client = cache.get(f"client_{client_id}")
        if not client:
            client = Client.objects.get(id=client_id)
            cache.set(f"client_{client_id}", client, timeout=60 * 15)
        return client
      
class ClientCreateView(CreateView):
    model = Client
    fields = "__all__"
    success_url = reverse_lazy("client:client_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete("client_list")
        return response

    @login_required
    def create_client(request):
        if request.method == "POST":
            name = request.POST["name"]
            email = request.POST["email"]
            Client.objects.create(name=name, email=email, created_by=request.user)
            return redirect("client_list")
        return render(request, "create_client.html")

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete('client_list')
        return response

    @login_required
    def create_client(request):
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            Client.objects.create(name=name, email=email, created_by=request.user)
            return redirect('client_list')
        return render(request, 'create_client.html')


class ClientUpdateView(UpdateView):
    model = Client
    fields = "__all__"
    success_url = reverse_lazy("client:client_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        client_id = self.object.id
        cache.delete(f"client_{client_id}")
        cache.delete("client_list")
        return response


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("client:client_list")

    def delete(self, request, *args, **kwargs):
        client_id = self.get_object().id
        response = super().delete(request, *args, **kwargs)
        cache.delete(f'client_{client_id}')
        cache.delete('client_list')
        return response


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("client:client_list")

    def delete(self, request, *args, **kwargs):
        client_id = self.get_object().id
        response = super().delete(request, *args, **kwargs)
        cache.delete(f"client_{client_id}")
        cache.delete("client_list")
        return response
