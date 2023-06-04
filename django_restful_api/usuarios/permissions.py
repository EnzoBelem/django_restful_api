from django.contrib.auth.models import User
from rest_framework import permissions


class IsClient(permissions.BasePermission):
    message = 'Você não tem permissão para manipular outros usuários.'

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Cliente').exists():
            username = request.resolver_match.kwargs.get('username', None)
            user = User.objects.filter(username=username).first()
            if user and user != request.user:
                return False

        return True
   
   