from django.urls import path
from usuarios.views import (UserClienteSignUp, UserDetail, UserGeneral,
                            UserPedidos)

urlpatterns = [
    path('', UserGeneral.as_view()),
    path('signup/', UserClienteSignUp.as_view()),
    path('<str:username>/', UserDetail.as_view()),
    path('<str:username>/pedidos/', UserPedidos.as_view()),
]
