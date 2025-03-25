from django.forms import ModelForm

from mailing.models import Mailing


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = "__all__"