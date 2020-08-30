from django.contrib.auth.backends import ModelBackend

from apps.users.models import User


def only_digits(s):
    return "".join([i for i in s if i.isdigit()])


class CPFBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        cpf = only_digits(kwargs["username"])
        password = kwargs["password"]
        try:
            user = User.objects.get(cpf=cpf)

            if user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
