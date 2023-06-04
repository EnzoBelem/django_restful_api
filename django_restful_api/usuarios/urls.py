from django.urls import path
from usuarios.views import UserAuthToken, UserDetail, UserList

urlpatterns = [
    path('', UserList.as_view()),
    path('<str:username>/', UserDetail.as_view()),
    path('auth/', UserAuthToken.as_view()),
]
