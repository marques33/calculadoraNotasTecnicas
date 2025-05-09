from django.db import models
from django.utils import timezone

# Modelo para cálculo padrão (G&E - Interativa e Real)
class CalculoNotaFiscalPadrao(models.Model):
    data_calculo = models.DateTimeField(default=timezone.now)
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    inss = models.DecimalField(max_digits=10, decimal_places=2)
    irrf = models.DecimalField(max_digits=10, decimal_places=2)
    issqn = models.DecimalField(max_digits=10, decimal_places=2)
    outras_deducoes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Cálculo Padrão em {self.data_calculo.strftime('%d/%m/%Y %H:%M')}: R$ {self.valor_liquido}"

# Modelo para cálculo detalhado (Juiz de Fora)
class CalculoNotaFiscalDetalhado(models.Model):
    data_calculo = models.DateTimeField(default=timezone.now)
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    valor_vale_transporte = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_vale_alimentacao = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_deduzido = models.DecimalField(max_digits=10, decimal_places=2)
    valor_nota_deduzida = models.DecimalField(max_digits=10, decimal_places=2)
    inss_valor = models.DecimalField(max_digits=10, decimal_places=2)
    irrf_valor = models.DecimalField(max_digits=10, decimal_places=2)
    issqn_valor = models.DecimalField(max_digits=10, decimal_places=2)
    outras_deducoes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Cálculo Detalhado em {self.data_calculo.strftime('%d/%m/%Y %H:%M')}: R$ {self.valor_liquido}"

# Modelo para Conta Vinculada com Funcionários
class FuncionarioContaVinculada(models.Model):
    FUNCAO_CHOICES = [
        ('SERVENTE', 'Servente'),
        ('ENCARREGADO', 'Encarregado'),
        ('OPERADOR_ROCADEIRA', 'Operador de Roçadeira'),
        ('COZINHEIRA', 'Cozinheira'),
        ('OUTRO', 'Outro'),
    ]
    
    funcao = models.CharField(max_length=20, choices=FUNCAO_CHOICES)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.get_funcao_display()}: R$ {self.salario_base}"

class CalculoContaVinculada(models.Model):
    data_calculo = models.DateTimeField(default=timezone.now)
    funcionarios = models.ManyToManyField(FuncionarioContaVinculada, through='ItemContaVinculada')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    total_provisao = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total x 30,83%")
    
    def __str__(self):
        return f"Cálculo Conta Vinculada em {self.data_calculo.strftime('%d/%m/%Y %H:%M')}: R$ {self.total_provisao}"

class ItemContaVinculada(models.Model):
    calculo = models.ForeignKey(CalculoContaVinculada, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(FuncionarioContaVinculada, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.funcionario.get_funcao_display()} ({self.quantidade})"

# Modelo para cálculo de vigilantes
class CalculoVigilante(models.Model):
    TIPO_CHOICES = [
        ('AD', 'Armado Diurno'),
        ('AN', 'Armado Noturno'),
        ('ND', 'Não-Armado Diurno'),
        ('NN', 'Não-Armado Noturno'),
    ]
    
    data_calculo = models.DateTimeField(default=timezone.now)
    tipo_vigilante = models.CharField(max_length=2, choices=TIPO_CHOICES)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()
    adicional_periculosidade = models.DecimalField(max_digits=10, decimal_places=2)
    adicional_noturno = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vale_transporte = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vale_alimentacao = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Cálculo Vigilante {self.get_tipo_vigilante_display()} em {self.data_calculo.strftime('%d/%m/%Y %H:%M')}: R$ {self.total_bruto}"