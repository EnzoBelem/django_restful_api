from django.urls import path
from pedidos.views import PedidoGeneral

urlpatterns = [
    path('', PedidoGeneral.as_view()),
]
