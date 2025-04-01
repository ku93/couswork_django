from django.forms import ModelForm

from client.models import Client


class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = ("owner",)
