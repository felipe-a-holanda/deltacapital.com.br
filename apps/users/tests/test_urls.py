import pytest
from django.urls import resolve
from django.urls import reverse

from apps.users.models import User

pytestmark = pytest.mark.django_db


def test_detail(user: User):
    assert (
        reverse("users:detail", kwargs={"username": user.username})
        == f"/usuarios/{user.username}/"
    )
    assert resolve(f"/usuarios/{user.username}/").view_name == "users:detail"


def test_update():
    assert reverse("users:update") == "/usuarios/~update/"
    assert resolve("/usuarios/~update/").view_name == "users:update"


def test_redirect():
    assert reverse("users:redirect") == "/usuarios/~redirect/"
    assert resolve("/usuarios/~redirect/").view_name == "users:redirect"
