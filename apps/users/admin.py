from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .constants import OPERADOR
from .constants import VENDEDOR
from .forms import UserChangeFormOwner
from .forms import UserChangeFormSuper
from .forms import UserCreationForm
from .models import Loja
from .models import Operador
from .models import User
from .models import Vendedor


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


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ["name", "cadastrada", "operador", "vendedores"]

    readonly_fields = ["vendedores"]

    def vendedores(self, obj):
        return mark_safe(", ".join([get_admin_link(v) for v in obj.vendedores.all()]))


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeFormSuper
    form_change_super = UserChangeFormSuper
    form_change_owner = UserChangeFormOwner
    add_form = UserCreationForm
    ordering = ["user_type", "username"]

    list_display = ["username", "cpf", "name", "user_type", "date_joined"]
    list_filter = ("is_staff", "user_type", "is_active", "groups")
    search_fields = ["name"]

    readonly_fields = ["date_joined", "last_login"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "user_type", "password1", "password2"),
            },
        ),
    )

    class Media:
        # this path may be any you want,
        # just put it in your static folder
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery
            'src/admin/js/inputmask.js',
           # 'src/admin/js/jquery.inputmask.min.js',
            'src/admin/js/masks_admin.js',
        )

    def get_fieldsets(self, request, obj):
        if obj:
            personal = {"fields": ("name",)}
            if obj.user_type == VENDEDOR:
                personal = {"fields": ("name", "loja")}  # type: ignore

            super_fieldsets = (
                (
                    None,
                    {"fields": ("user_type", "username", "cpf", "email", "password")},
                ),
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
                (
                    None,
                    {"fields": ("user_type", "username", "cpf", "email", "password")},
                ),
                (_("Personal info"), personal),
                (_("Permissions"), {"fields": ("is_active",)}),
                (_("Important dates"), {"fields": ("last_login", "date_joined")}),
            )

            if request.user.is_superuser:
                return super_fieldsets
            return owner_fieldsets
        else:
            return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        if obj is not None:
            if request.user.is_superuser:
                self.form = self.form_change_super
            else:
                self.form = self.form_change_owner

        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                "is_superuser",
                "is_staff",
                "groups",
                "user_permissions",
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


@admin.register(Operador)
class UserOperadorAdmin(UserAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(user_type=OPERADOR)

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserOperadorAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["user_type"].initial = OPERADOR

        return form


@admin.register(Vendedor)
class UserVendedorAdmin(UserAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(user_type=VENDEDOR)

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserVendedorAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["user_type"].initial = VENDEDOR
        form.base_fields["loja"].required = True

        return form
