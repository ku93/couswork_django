from django.contrib.auth.forms import UserCreationForm

from catalog.forms import StyledFormMixin
from users.models import User


class UserRegisterForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")
