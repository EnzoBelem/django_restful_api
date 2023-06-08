from django.contrib import admin
from django.urls import include, path
from usuarios.views import UserAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', UserAuthToken.as_view()),
    path('usuarios/', include('usuarios.urls')),
    path('itens/', include('itens.urls')),
    path('pedidos/', include('pedidos.urls')),
]
