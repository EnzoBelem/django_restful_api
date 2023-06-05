from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from usuarios.permissions import IsClient
from usuarios.serializers import (UserCreateSerializer, UserSerializer,
                                  UserUpdateSerializer)
from usuarios.utils import UserGroupVerify


class UserAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=usuario)
        return Response({'token': token.key})


class UserGeneral(APIView):
    """
    API Endpoint - listagem e criacao de usuarios.\n
    Cliente sem permissao: listagem completa e criacao de usuarios.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if UserGroupVerify.is_cliente(request.user):
            serializer = UserSerializer(request.user)
        else:
            query_set = User.objects.all()
            serializer = UserSerializer(query_set, many=True)
        return Response(serializer.data)

    def post(self, request):
        if UserGroupVerify.is_cliente(request.user):
            return Response("Não possui permissão.", status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    API Endpoint - GET/PUT/DELETE usuario especifico.\n
    Cliente sem permissao: manipulacao de outros usuarios.
    """
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def _get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username):
        usuario = self._get_user(username)
        serializer = UserSerializer(usuario)
        return Response(serializer.data)

    def patch(self, request, username):
        usuario = self._get_user(username)
        serializer = UserUpdateSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        usuario = self._get_user(username)
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
