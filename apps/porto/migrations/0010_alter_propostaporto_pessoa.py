# Generated by Django 3.2.10 on 2022-02-18 16:44
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("porto", "0009_auto_20211202_1027")]

    operations = [
        migrations.AlterField(
            model_name="propostaporto",
            name="pessoa",
            field=models.CharField(
                choices=[("", ""), ("pf", "Pessoa Física"), ("pj", "Pessoa Jurídica")],
                default="pf",
                max_length=100,
                verbose_name="Pessoa Física ou Jurídica",
            ),
        )
    ]
