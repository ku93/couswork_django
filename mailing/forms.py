from django.forms import ModelForm

from mailing.models import Mailing


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        exclude = ("owner",)
