from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import permissions


class GroupsPermissionsForUserManipulation(permissions.BasePermission):
    """
    Permite acesso dado o grupo do usuario.\n
    * Clientes: permissao de acesso/manipulacao a seus proprios dados.\n
    * Funcionários: acesso livre, manipulacao somente a dados de Clientes.\n
    * Gerência: acesso/manipulacao livre.
    """
    message = 'Você não possui permissão.'

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Cliente').exists():
            username = request.resolver_match.kwargs.get('username', None)
            user = User.objects.filter(username=username).first()

            if user and user == request.user:
                return True
            
        elif request.user.groups.filter(Q(name='Funcionário')).exists():

            if request.method in permissions.SAFE_METHODS:
                return True
            
            username = request.resolver_match.kwargs.get('username', None)
            user = User.objects.filter(username=username).first()

            if user and user.groups.filter(name='Cliente').exists():
                return True
            
        elif request.user.groups.filter(Q(name='Gerência')).exists():
            return True
        
        return False
   
   