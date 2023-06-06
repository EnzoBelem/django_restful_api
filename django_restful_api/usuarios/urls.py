from django.urls import path
from usuarios.views import UserAuthToken, UserDetail, UserGeneral

urlpatterns = [
    path('', UserGeneral.as_view()),
    path('<str:username>/', UserDetail.as_view()),
]
