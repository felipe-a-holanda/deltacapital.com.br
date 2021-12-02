from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


def only_digits(s):
    return "".join([i for i in s if i.isdigit()])


class UserChangeFormSuper(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

    def clean_username(self):
        return self.cleaned_data["username"].lower()

    def clean_cpf(self):
        return only_digits(self.cleaned_data["cpf"])


class UserChangeFormOwner(UserChangeFormSuper):
    def __init__(self, *args, **kwargs):
        super(UserChangeFormSuper, self).__init__(*args, **kwargs)
        self.fields["user_type"].choices = self.fields["user_type"]._choices[1:]

    def validate(self):
        return False


class UserCreationFormDelta(UserCreationForm):

    error_message = auth.forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(auth.forms.UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "cpf")

    def clean_cpf(self):
        return only_digits(self.cleaned_data["cpf"])

    def clean_username(self):
        username = self.cleaned_data["username"].lower()

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])
