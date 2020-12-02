from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from .constants import OPERADOR
from .constants import PROPRIETARIO
from .constants import USER_TYPE_CHOICES
from .constants import VENDEDOR
from .constants import WEBMASTER


def webmaster_perms():
    owner = Group.objects.get(pk=WEBMASTER)
    owner.permissions.add(*Permission.objects.all())


def owner_perms():
    owner = Group.objects.get(pk=PROPRIETARIO)
    owner.permissions.add(*Permission.objects.all())

    owner.permissions.remove(*Permission.objects.filter(content_type__app_label="auth"))
    owner.permissions.remove(
        *Permission.objects.filter(content_type__app_label="sites")
    )
    owner.permissions.remove(
        *Permission.objects.filter(content_type__app_label="account")
    )
    owner.permissions.remove(
        *Permission.objects.filter(content_type__app_label="socialaccount")
    )


def operator_perms():
    owner = Group.objects.get(pk=OPERADOR)
    owner.permissions.set([])
    owner.permissions.add(*Permission.objects.filter(codename="view_propostaporto"))


def seller_perms():
    owner = Group.objects.get(pk=VENDEDOR)
    owner.permissions.set([])


def create_groups():
    for pk, name in USER_TYPE_CHOICES:
        Group.objects.update_or_create(pk=pk, defaults={"name": name})

    webmaster_perms()
    owner_perms()
    operator_perms()
    seller_perms()
