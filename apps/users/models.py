from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .constants import OPERADOR
from .constants import PROPRIETARIO
from .constants import USER_TYPE_CHOICES
from .constants import VENDEDOR
from .constants import WEBMASTER
from .utils import create_groups


class Loja(models.Model):
    name = models.CharField("Nome", max_length=100)
    operador = models.ForeignKey(
        "users.User", related_name="operador", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["operador", "name"]

    def __str__(self):
        return self.name


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Nome do usuário"), blank=True, max_length=255)
    cpf = models.CharField(_("CPF do usuário"), max_length=11)
    user_type = models.PositiveSmallIntegerField(
        "Tipo do usuário", default=VENDEDOR, choices=USER_TYPE_CHOICES
    )
    loja = models.ForeignKey(
        "users.Loja",
        related_name="vendedores",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def change_user_by_type(self):
        if self.is_superuser:
            self.user_type = WEBMASTER

        if self.user_type == PROPRIETARIO:
            self.is_staff = True
        elif self.user_type == OPERADOR:
            self.is_staff = True
        elif self.user_type == VENDEDOR:
            self.is_staff = False

    def save(self, *args, **kwargs):
        create_groups()
        self.change_user_by_type()
        super().save(*args, **kwargs)

    @property
    def is_operador(self):
        return self.user_type == OPERADOR

    @property
    def is_vendedor(self):
        return self.user_type == VENDEDOR

    @property
    def is_proprietario(self):
        return self.user_type == PROPRIETARIO


def save_groups(sender, instance, **kwargs):
    instance.groups.clear()
    instance.groups.add(Group.objects.get(pk=instance.user_type))


post_save.connect(save_groups, sender=User)
