from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import permissions


class GroupsPermissionsForUserManipulation(permissions.BasePermission):
    """
    Permite acesso dado o grupo do usuario.\n
    * Cliente: permissao de acesso/manipulacao a seus proprios dados.\n
    * Funcionário: acesso livre, manipulacao somente a dados de Clientes.\n
    * Gerência: acesso/manipulacao livre.
    """
    message = 'Você não possui permissão.'

    def _get_user_by_kwargs(self, request):
        username = request.resolver_match.kwargs.get('username', None)
        return User.objects.filter(username=username).first()

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Cliente').exists():
            user = self._get_user_by_kwargs(request)

            if user and user == request.user:
                return True
            
        elif request.user.groups.filter(name='Funcionário').exists():

            if request.method in permissions.SAFE_METHODS:
                return True
            
            user = self._get_user_by_kwargs(request)

            if user and user.groups.filter(name='Cliente').exists():
                return True
            
        elif request.user.groups.filter(name='Gerência').exists():
            return True
        
        return False
   

class GroupsPermissionForItemManipulation(permissions.BasePermission):

    message = 'Essa operação não é permitida.'

    def has_permission(self, request, view):
        if  request.method in permissions.SAFE_METHODS or \
            not request.user.groups.filter(name= 'Cliente'):
            return True
        return False

