from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
from django.views.decorators.http import require_http_methods
from .models import (
    CalculoNotaFiscalPadrao, CalculoNotaFiscalDetalhado,
    FuncionarioContaVinculada, CalculoContaVinculada, ItemContaVinculada,
    CalculoVigilante
)

def index(request):
    """Renderiza a página inicial."""
    return render(request, 'index.html')

@require_http_methods(["GET", "POST"])
def calcular_nota_fiscal_padrao(request):
    """
    Calculadora de Nota Fiscal - Padrão (G&E - Interativa e Real)
    
    Cálculo de impostos:
    - INSS: 11% do valor bruto
    - IRRF: 4,8% do valor bruto
    - ISSQN: 5% do valor bruto
    """
    context = {
        'valor_bruto': None,
        'inss': None,
        'irrf': None,
        'issqn': None,
        'outras_deducoes': None,
        'valor_liquido': None,
    }
    
    if request.method == 'POST':
        try:
            valor_bruto_str = request.POST.get('valor_bruto', '0').replace(',', '.')
            outras_deducoes_str = request.POST.get('outras_deducoes', '0').replace(',', '.')
            
            valor_bruto = Decimal(valor_bruto_str)
            outras_deducoes = Decimal(outras_deducoes_str)
            
            if valor_bruto <= 0:
                messages.error(request, "O valor bruto deve ser maior que zero.")
                return render(request, 'calcular_nota_fiscal_padrao.html', context)
            
            # Cálculo dos impostos
            inss = valor_bruto * Decimal('0.11')
            irrf = valor_bruto * Decimal('0.048')
            issqn = valor_bruto * Decimal('0.05')
            
            # Valor líquido
            valor_liquido = valor_bruto - (inss + irrf + issqn + outras_deducoes)
            
            # Salvar o cálculo
            calculo = CalculoNotaFiscalPadrao(
                valor_bruto=valor_bruto,
                inss=inss,
                irrf=irrf,
                issqn=issqn,
                outras_deducoes=outras_deducoes,
                valor_liquido=valor_liquido
            )
            calculo.save()
            
            context.update({
                'valor_bruto': valor_bruto,
                'inss': inss,
                'irrf': irrf,
                'issqn': issqn,
                'outras_deducoes': outras_deducoes,
                'valor_liquido': valor_liquido,
            })
            
        except (InvalidOperation, ValueError) as e:
            messages.error(request, f"Erro no cálculo: {str(e)}")
    
    return render(request, 'calcular_nota_fiscal_padrao.html', context)

@require_http_methods(["GET", "POST"])
def calcular_nota_fiscal_detalhado(request):
    """
    Calculadora de Nota Fiscal - Detalhada (Juiz de Fora)
    
    Cálculos:
    - Valor Deduzido = Valor Bruto - (Vale Transporte + Vale Alimentação)
    - INSS = 11% do Valor Deduzido
    - IRRF = 4,8% do Valor Bruto (da Nota)
    - ISSQN = 5% do Valor Bruto (da Nota)
    """
    context = {
        'valor_bruto': None,
        'valor_vale_transporte': None,
        'valor_vale_alimentacao': None,
        'valor_deduzido': None,
        'valor_nota_deduzida': None,
        'inss_valor': None,
        'irrf_valor': None,
        'issqn_valor': None,
        'outras_deducoes': None,
        'valor_liquido': None,
    }
    
    if request.method == 'POST':
        try:
            valor_bruto = Decimal(request.POST.get('valor_bruto', '0').replace(',', '.'))
            valor_vale_transporte = Decimal(request.POST.get('valor_vale_transporte', '0').replace(',', '.'))
            valor_vale_alimentacao = Decimal(request.POST.get('valor_vale_alimentacao', '0').replace(',', '.'))
            outras_deducoes = Decimal(request.POST.get('outras_deducoes', '0').replace(',', '.'))
            
            if valor_bruto <= 0:
                messages.error(request, "O valor bruto deve ser maior que zero.")
                return render(request, 'calcular_nota_fiscal_detalhado.html', context)
            
            # Cálculos conforme planilha
            valor_deduzido = valor_vale_transporte + valor_vale_alimentacao
            valor_nota_deduzida = valor_bruto - valor_deduzido
            
            # Impostos
            inss_valor = valor_nota_deduzida * Decimal('0.11')
            irrf_valor = valor_bruto * Decimal('0.048')
            issqn_valor = valor_bruto * Decimal('0.05')
            
            # Valor líquido
            valor_liquido = valor_bruto - (inss_valor + irrf_valor + issqn_valor + outras_deducoes)
            
            # Salvar o cálculo
            calculo = CalculoNotaFiscalDetalhado(
                valor_bruto=valor_bruto,
                valor_vale_transporte=valor_vale_transporte,
                valor_vale_alimentacao=valor_vale_alimentacao,
                valor_deduzido=valor_deduzido,
                valor_nota_deduzida=valor_nota_deduzida,
                inss_valor=inss_valor,
                irrf_valor=irrf_valor,
                issqn_valor=issqn_valor,
                outras_deducoes=outras_deducoes,
                valor_liquido=valor_liquido
            )
            calculo.save()
            
            context.update({
                'valor_bruto': valor_bruto,
                'valor_vale_transporte': valor_vale_transporte,
                'valor_vale_alimentacao': valor_vale_alimentacao,
                'valor_deduzido': valor_deduzido,
                'valor_nota_deduzida': valor_nota_deduzida,
                'inss_valor': inss_valor,
                'irrf_valor': irrf_valor,
                'issqn_valor': issqn_valor,
                'outras_deducoes': outras_deducoes,
                'valor_liquido': valor_liquido,
            })
            
        except (InvalidOperation, ValueError) as e:
            messages.error(request, f"Erro no cálculo: {str(e)}")
    
    return render(request, 'calcular_nota_fiscal_detalhado.html', context)

@require_http_methods(["GET", "POST"])
def calcular_conta_vinculada(request):
    """
    Calculadora de Conta Vinculada
    
    Permite calcular a provisão (30,83%) sobre o valor total dos salários
    de acordo com a quantidade de funcionários por função.
    """
    # Carrega informações dos salários de cada função
    salarios_base = {
        'SERVENTE': Decimal('1743.69'),
        'ENCARREGADO': Decimal('3383.59'),
        'OPERADOR_ROCADEIRA': Decimal('1802.16'),
        'COZINHEIRA': Decimal('2726.91'),
    }
    
    # Prepara contexto inicial
    context = {
        'salarios_base': salarios_base,
        'itens': [],
        'total': Decimal('0'),
        'total_provisao': Decimal('0'),
    }
    
    if request.method == 'POST':
        try:
            # Cria um objeto de cálculo
            calculo = CalculoContaVinculada(
                total=Decimal('0'),
                total_provisao=Decimal('0')
            )
            calculo.save()
            
            total_geral = Decimal('0')
            itens_calculo = []
            
            # Processa cada função
            for funcao, salario_base in salarios_base.items():
                qtd_str = request.POST.get(f'qtd_{funcao.lower()}', '0')
                quantidade = int(qtd_str) if qtd_str.isdigit() else 0
                
                if quantidade > 0:
                    # Cria ou obtém o modelo de funcionário
                    funcionario, _ = FuncionarioContaVinculada.objects.get_or_create(
                        funcao=funcao,
                        defaults={'salario_base': salario_base}
                    )
                    
                    # Calcula o total para este tipo de funcionário
                    total_funcao = salario_base * quantidade
                    total_geral += total_funcao
                    
                    # Cria item de cálculo
                    item = ItemContaVinculada(
                        calculo=calculo,
                        funcionario=funcionario,
                        quantidade=quantidade,
                        total=total_funcao
                    )
                    item.save()
                    
                    # Adiciona ao contexto
                    itens_calculo.append({
                        'funcao': funcionario.get_funcao_display(),
                        'salario_base': salario_base,
                        'quantidade': quantidade,
                        'total': total_funcao,
                    })
            
            # Calcula provisão (30,83%)
            total_provisao = total_geral * Decimal('0.3083')
            
            # Atualiza o cálculo
            calculo.total = total_geral
            calculo.total_provisao = total_provisao
            calculo.save()
            
            # Atualiza o contexto
            context.update({
                'itens': itens_calculo,
                'total': total_geral,
                'total_provisao': total_provisao,
            })
            
        except (InvalidOperation, ValueError) as e:
            messages.error(request, f"Erro no cálculo: {str(e)}")
    
    return render(request, 'calcular_conta_vinculada.html', context)

@require_http_methods(["GET", "POST"])
def calcular_vigilante(request):
    """
    Calculadora para Vigilantes
    
    Permite calcular o custo de vigilantes considerando:
    - Diferentes tipos (armado/não-armado, diurno/noturno)
    - Adicional de periculosidade (30% do salário base)
    - Adicional noturno (para turnos noturnos)
    - Vale transporte e alimentação
    """
    context = {
        'tipos_vigilante': [
            {'codigo': 'AD', 'nome': 'Armado Diurno'},
            {'codigo': 'AN', 'nome': 'Armado Noturno'},
            {'codigo': 'ND', 'nome': 'Não-Armado Diurno'},
            {'codigo': 'NN', 'nome': 'Não-Armado Noturno'},
        ],
        'resultado': None,
    }
    
    if request.method == 'POST':
        try:
            tipo_vigilante = request.POST.get('tipo_vigilante')
            salario_base = Decimal(request.POST.get('salario_base', '0').replace(',', '.'))
            quantidade = int(request.POST.get('quantidade', '0'))
            vale_transporte = Decimal(request.POST.get('vale_transporte', '0').replace(',', '.'))
            vale_alimentacao = Decimal(request.POST.get('vale_alimentacao', '0').replace(',', '.'))
            
            if salario_base <= 0 or quantidade <= 0:
                messages.error(request, "O salário base e a quantidade devem ser maiores que zero.")
                return render(request, 'calcular_vigilante.html', context)
            
            # Cálculo do adicional de periculosidade (30% do salário base)
            adicional_periculosidade = salario_base * Decimal('0.30')
            
            # Cálculo do adicional noturno (se aplicável)
            adicional_noturno = Decimal('0')
            if tipo_vigilante in ['AN', 'NN']:
                # 20% sobre as horas noturnas (considerando 8h diárias)
                adicional_noturno = (salario_base / 30 / 8) * 8 * Decimal('0.20') * 30
            
            # Calcula valor por funcionário
            valor_por_funcionario = salario_base + adicional_periculosidade + adicional_noturno + vale_transporte + vale_alimentacao
            
            # Calcula total bruto
            total_bruto = valor_por_funcionario * quantidade
            
            # Salvar o cálculo
            calculo = CalculoVigilante(
                tipo_vigilante=tipo_vigilante,
                salario_base=salario_base,
                quantidade=quantidade,
                adicional_periculosidade=adicional_periculosidade,
                adicional_noturno=adicional_noturno,
                vale_transporte=vale_transporte,
                vale_alimentacao=vale_alimentacao,
                total_bruto=total_bruto
            )
            calculo.save()
            
            context.update({
                'tipo_vigilante': tipo_vigilante,
                'tipo_vigilante_nome': dict(CalculoVigilante.TIPO_CHOICES)[tipo_vigilante],
                'salario_base': salario_base,
                'quantidade': quantidade,
                'adicional_periculosidade': adicional_periculosidade,
                'adicional_noturno': adicional_noturno,
                'vale_transporte': vale_transporte,
                'vale_alimentacao': vale_alimentacao,
                'valor_por_funcionario': valor_por_funcionario,
                'total_bruto': total_bruto,
            })
            
        except (InvalidOperation, ValueError) as e:
            messages.error(request, f"Erro no cálculo: {str(e)}")
    
    return render(request, 'calcular_vigilante.html', context)

# API para cálculos dinâmicos via AJAX (opcional)
def api_calcular_vigilante(request):
    """API para cálculo dinâmico de vigilantes via AJAX"""
    if request.method == 'GET':
        try:
            tipo_vigilante = request.GET.get('tipo_vigilante')
            salario_base = Decimal(request.GET.get('salario_base', '0').replace(',', '.'))
            
            # Cálculo do adicional de periculosidade
            adicional_periculosidade = salario_base * Decimal('0.30')
            
            # Cálculo do adicional noturno
            adicional_noturno = Decimal('0')
            if tipo_vigilante in ['AN', 'NN']:
                adicional_noturno = (salario_base / 30 / 8) * 8 * Decimal('0.20') * 30
            
            return JsonResponse({
                'adicional_periculosidade': float(adicional_periculosidade),
                'adicional_noturno': float(adicional_noturno),
                'total_salario': float(salario_base + adicional_periculosidade + adicional_noturno)
            })
            
        except (InvalidOperation, ValueError) as e:
            return JsonResponse({'erro': str(e)}, status=400)
    
    return JsonResponse({'erro': 'Método não permitido'}, status=405)