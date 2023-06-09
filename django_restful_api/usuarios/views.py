from django.contrib.auth.models import User
from django.http import Http404
from pedidos.models import Pedido
from pedidos.serializers import PedidoSerializer
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from usuarios.permissions import GroupsPermissionsForUserManipulation
from usuarios.serializers import (UserCreateSerializer, UserSerializer,
                                  UserSignUpSerializer, UserUpdateSerializer)
from usuarios.utils import UserGroupVerify


class UserAuthToken(ObtainAuthToken):
    """
    API Endpoint - Autenticacao por Token via credenciais validas.
    """
    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=usuario)
        return Response({'token': token.key})


class UserClienteSignUp(APIView):
    """
    API Endpoint - Criacao de clientes.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGeneral(APIView):
    """
    API Endpoint - Acesso a usuarios sem parametro.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        GET - listagem total/parcial de usuarios do sistema
        * Cliente: acesso somente a listagem parcial.
        """
        if UserGroupVerify.is_cliente(request.user):
            serializer = UserSignUpSerializer(request.user)
        else:
            query_set = User.objects.all()
            serializer = UserSerializer(query_set, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        POST - criacao de usuario.
        * Cliente: sem permissao.
        * Funcionário: criar unicamente Clientes.
        """
        if UserGroupVerify.is_cliente(request.user):
            return Response("Não possui permissão.", status=status.HTTP_401_UNAUTHORIZED)
        elif UserGroupVerify.is_funcionario(request.user):
           if not request.data.get('group') == 'Cliente':
            return Response("Não possui permissão.", status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    API Endpoint - GET/PATCH/DELETE usuario especifico via <str:username>.
    """
    permission_classes = [permissions.IsAuthenticated, GroupsPermissionsForUserManipulation]

    def _get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username):
        """
        GET - Listagem de dados de usuario especifico.
        """
        usuario = self._get_user(username)
        if UserGroupVerify.is_cliente(request.user):
            serializer = UserSignUpSerializer(usuario)
        else:
            serializer = UserSerializer(usuario)
        return Response(serializer.data)

    def patch(self, request, username):
        """
        PATCH - Atualizacao total/parcial de dados de usuario especifico.
        """
        usuario = self._get_user(username)
        serializer = UserUpdateSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        """
        DELETE - Remocao de usuario especifico.
        """
        usuario = self._get_user(username)
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UserPedidos(APIView):
    """
    API Endpoint - Listagem dos pedidos de um usuario especifico.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username):
        try:
            usuario = User.objects.get(username=username)
            pedidos = Pedido.objects.filter(usuario= usuario)
            context= {'request': request, 'resume_request': True}
            serializer = PedidoSerializer(pedidos, many=True, context= context)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise Http404

