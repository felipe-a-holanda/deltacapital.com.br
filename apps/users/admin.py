from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from .forms import UserChangeForm
from .forms import UserCreationForm
from .models import Loja


User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        ("User", {"fields": ("name", "cpf", "user_type")}),
    ) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "user_type"]
    list_filter = ("is_staff", "user_type", "is_active", "groups")
    search_fields = ["name"]


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ["name", "operador"]
