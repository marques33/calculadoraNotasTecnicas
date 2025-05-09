from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calcular-nota-fiscal-padrao/', views.calcular_nota_fiscal_padrao, name='calcular_nota_fiscal_padrao'),
    path('calcular-nota-fiscal-detalhado/', views.calcular_nota_fiscal_detalhado, name='calcular_nota_fiscal_detalhado'),
    path('calcular-conta-vinculada/', views.calcular_conta_vinculada, name='calcular_conta_vinculada'),
    path('calcular-vigilante/', views.calcular_vigilante, name='calcular_vigilante'),
    path('api/calcular-vigilante/', views.api_calcular_vigilante, name='api_calcular_vigilante'),
]