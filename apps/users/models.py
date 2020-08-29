from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Loja(models.Model):
    name = models.CharField("Nome", max_length=100)
    operador = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        ordering = ["operador", "name"]


class UserProfile(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)


class VendedorProfile(UserProfile):
    loja = models.ForeignKey("users.Loja", on_delete=models.CASCADE)


WEBMASTER = 1
PROPRIETARIO = 2
OPERADOR = 3
VENDEDOR = 4


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (WEBMASTER, "Webmaster"),
        (PROPRIETARIO, "Proprietario"),
        (OPERADOR, "Operador"),
        (VENDEDOR, "Vendedor"),
    )

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Nome do usuário"), blank=True, max_length=255)
    cpf = models.CharField(_("CPF do usuário"), unique=True, max_length=11)
    user_type = models.PositiveSmallIntegerField(
        "Tipo do usuário", default=VENDEDOR, choices=USER_TYPE_CHOICES
    )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
