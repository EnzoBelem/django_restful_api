from django.urls import path
from usuarios.views import UserDetail, UserList

urlpatterns = [
    path('', UserList.as_view()),
    path('<str:username>/', UserDetail.as_view()),
]
