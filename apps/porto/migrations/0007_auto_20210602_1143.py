# Generated by Django 3.2.3 on 2021-06-02 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('porto', '0006_auto_20210414_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='propostaporto',
            name='cnpj',
            field=models.CharField(blank=True, help_text='<h2>Cliente</h2><h3>Preencha com o CNPJ da Empresa</h3>', max_length=20, verbose_name='CNPJ'),
        ),
        migrations.AddField(
            model_name='propostaporto',
            name='pessoa',
            field=models.CharField(choices=[('pf', 'pf'), ('pj', 'pj')], default='pf', max_length=100),
        ),
    ]