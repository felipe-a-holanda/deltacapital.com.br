from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .constants import VENDEDOR
from .forms import UserChangeForm
from .forms import UserChangeFormOwner
from .forms import UserCreationForm
from .models import Loja


def get_admin_url(obj):
    content_type = ContentType.objects.get_for_model(obj.__class__)
    return reverse(
        "admin:%s_%s_change" % (content_type.app_label, content_type.model),
        args=(obj.id,),
    )


def get_admin_link(obj):
    admin_url = get_admin_url(obj)
    link = mark_safe("<a href='{}'>{}</a>".format(admin_url, obj))
    return link


User = get_user_model()


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ["name", "operador", "vendedores"]

    readonly_fields = ["vendedores"]

    def vendedores(self, obj):
        return mark_safe(", ".join([get_admin_link(v) for v in obj.vendedores.all()]))


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    form_super = UserChangeForm
    form_owner = UserChangeFormOwner
    add_form = UserCreationForm

    list_display = ["username", "name", "user_type"]
    list_filter = ("is_staff", "user_type", "is_active", "groups")
    search_fields = ["name"]

    readonly_fields = ["date_joined", "last_login"]

    def get_fieldsets(self, request, obj):
        if obj.user_type == VENDEDOR:
            personal = {"fields": ("name", "loja")}
        else:
            personal = {"fields": ("name",)}  # type: ignore

        super_fieldsets = (
            (None, {"fields": ("user_type", "username", "cpf", "email", "password")}),
            (_("Personal info"), personal),
            (
                _("Permissions"),
                {
                    "fields": (
                        "is_active",
                        "is_staff",
                        "is_superuser",
                        "groups",
                        "user_permissions",
                    )
                },
            ),
            (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        )
        owner_fieldsets = (
            (None, {"fields": ("user_type", "username", "cpf", "email", "password")}),
            (_("Personal info"), personal),
            (_("Permissions"), {"fields": ("is_active",)}),
            (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        )

        if request.user.is_superuser:
            return super_fieldsets
        return owner_fieldsets

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.form = self.form_super
        else:
            self.form = self.form_owner

        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                "username",
                "is_superuser",
                "is_staff",
                "groups",
                "user_permissions",
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form
