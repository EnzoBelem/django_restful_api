from django.urls import path
from pedidos.views import PedidoDetail, PedidoGeneral

urlpatterns = [
    path('', PedidoGeneral.as_view()),
    path('<slug:codigo_pedido>/', PedidoDetail.as_view()),
]
