# Generated by Django 3.2 on 2021-04-21 11:26

import apps.gestao.upload
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('porto', '0006_auto_20210414_1452'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0005_auto_20210405_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aprovada_em', models.DateField(null=True)),
                ('cliente', models.CharField(max_length=255)),
                ('cpf_cnpj', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('aguardando', 'Aguardando Análise'), ('analista', 'Com Analista'), ('recusado', 'Recusado'), ('reanalise', 'Em Reanálise'), ('aprovado', 'Aprovado'), ('efetivada', 'Proposta Efetivada')], default='aguardando', max_length=100)),
                ('telefone', models.CharField(blank=True, max_length=255)),
                ('origem', models.CharField(blank=True, max_length=255, verbose_name='Origem/Lead')),
                ('valor_veiculo', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True)),
                ('valor_entrada', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True)),
                ('valor_financiado', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True)),
                ('veiculo', models.CharField(blank=True, max_length=255, null=True)),
                ('parcelas', models.IntegerField(blank=True, null=True)),
                ('valor_parcela', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True)),
                ('taxa', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('n_contrato', models.CharField(blank=True, max_length=255, null=True)),
                ('comissao', models.DecimalField(decimal_places=1, default=6.0, max_digits=3)),
                ('comissao_operador', models.DecimalField(decimal_places=2, default=2.0, max_digits=3)),
                ('comissao_campanha', models.DecimalField(decimal_places=2, default=2.0, max_digits=3)),
                ('valor_comissao', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True)),
                ('valor_comissao_operador', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True)),
                ('valor_comissao_campanha', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True)),
                ('valor_comissao_liquido', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True)),
                ('arquivo_cnh', models.FileField(blank=True, null=True, upload_to=apps.gestao.upload.UploadToPath('cnh'), verbose_name='Arquivo da CNH')),
                ('arquivo_nf', models.FileField(blank=True, null=True, upload_to=apps.gestao.upload.UploadToPath('nf'), verbose_name='Dut ou NF')),
                ('arquivo_rg', models.FileField(blank=True, null=True, upload_to=apps.gestao.upload.UploadToPath('rg'), verbose_name='Arquivo do RG')),
                ('arquivo_cpf', models.FileField(blank=True, null=True, upload_to=apps.gestao.upload.UploadToPath('cpf'), verbose_name='Arquivo do CPF')),
                ('arquivo_endereco', models.FileField(blank=True, null=True, upload_to=apps.gestao.upload.UploadToPath('endereco'), verbose_name='Arquivo do Comprovante de Endereço')),
                ('arquivo_renda', models.FileField(blank=True, null=True, upload_to=apps.gestao.upload.UploadToPath('renda'), verbose_name='Arquivo do Comprovante de Renda')),
                ('arquivo_contrato_social', models.FileField(blank=True, null=True, upload_to=apps.gestao.upload.UploadToPath('contrato_social'), verbose_name='Arquivo do Contrato Social')),
                ('criada_em', models.DateTimeField(auto_now_add=True)),
                ('loja', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.loja')),
                ('proposta_porto', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='porto.propostaporto')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
