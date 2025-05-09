# Generated by Django 5.2.1 on 2025-05-09 13:27

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CalculoContaVinculada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_calculo', models.DateTimeField(default=django.utils.timezone.now)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_provisao', models.DecimalField(decimal_places=2, help_text='Total x 30,83%', max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='CalculoNotaFiscalDetalhado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_calculo', models.DateTimeField(default=django.utils.timezone.now)),
                ('valor_bruto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valor_vale_transporte', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('valor_vale_alimentacao', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('valor_deduzido', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valor_nota_deduzida', models.DecimalField(decimal_places=2, max_digits=10)),
                ('inss_valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('irrf_valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('issqn_valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('outras_deducoes', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('valor_liquido', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='CalculoNotaFiscalPadrao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_calculo', models.DateTimeField(default=django.utils.timezone.now)),
                ('valor_bruto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('inss', models.DecimalField(decimal_places=2, max_digits=10)),
                ('irrf', models.DecimalField(decimal_places=2, max_digits=10)),
                ('issqn', models.DecimalField(decimal_places=2, max_digits=10)),
                ('outras_deducoes', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('valor_liquido', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='CalculoVigilante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_calculo', models.DateTimeField(default=django.utils.timezone.now)),
                ('tipo_vigilante', models.CharField(choices=[('AD', 'Armado Diurno'), ('AN', 'Armado Noturno'), ('ND', 'Não-Armado Diurno'), ('NN', 'Não-Armado Noturno')], max_length=2)),
                ('salario_base', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantidade', models.PositiveIntegerField()),
                ('adicional_periculosidade', models.DecimalField(decimal_places=2, max_digits=10)),
                ('adicional_noturno', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('vale_transporte', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('vale_alimentacao', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_bruto', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='FuncionarioContaVinculada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funcao', models.CharField(choices=[('SERVENTE', 'Servente'), ('ENCARREGADO', 'Encarregado'), ('OPERADOR_ROCADEIRA', 'Operador de Roçadeira'), ('COZINHEIRA', 'Cozinheira'), ('OUTRO', 'Outro')], max_length=20)),
                ('salario_base', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ItemContaVinculada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=0)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('calculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculo.calculocontavinculada')),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculo.funcionariocontavinculada')),
            ],
        ),
        migrations.AddField(
            model_name='calculocontavinculada',
            name='funcionarios',
            field=models.ManyToManyField(through='calculo.ItemContaVinculada', to='calculo.funcionariocontavinculada'),
        ),
    ]
