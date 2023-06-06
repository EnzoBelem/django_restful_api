from django.urls import path
from itens.views import ItemDetail, ItemGeneral

urlpatterns = [
    path('', ItemGeneral.as_view()),
    path('<str:codigo_item>/', ItemDetail.as_view())
]
