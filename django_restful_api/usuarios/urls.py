from django.urls import path
from usuarios.views import UserList

urlpatterns = [
    path('', UserList.as_view()),
]
