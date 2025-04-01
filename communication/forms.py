from django.forms import ModelForm

from communication.models import Communication


class CommunicationForm(ModelForm):
    class Meta:
        model = Communication
        exclude = ("owner",)
