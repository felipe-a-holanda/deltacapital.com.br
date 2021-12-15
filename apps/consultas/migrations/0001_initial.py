# Generated by Django 3.2.3 on 2021-12-14 17:16
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Consulta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "entrada",
                    models.CharField(
                        max_length=18,
                        validators=[django.core.validators.MinLengthValidator(11)],
                    ),
                ),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("PessoaFisica", "Pessoa Física"),
                            ("PessoaJuridica", "Pessoa Jurídica"),
                            ("VinculosEmpresariais", "Vínculos Empresariais"),
                            ("ParticipacaoEmpresarial", "Participação Empresarial"),
                        ],
                        max_length=100,
                    ),
                ),
                ("resultado", models.JSONField(blank=True, null=True)),
                (
                    "criado_em",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "modificado_em",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        )
    ]
