from django.http import Http404
from itens.models import Item
from itens.serializers import (ItemResumeSerializer, ItemSerializer,
                               ItemUpdateSerializer)
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from usuarios.permissions import GroupsPermissionForItemManipulation


class ItemGeneral(APIView):
    """
    API Endpoint - Listagem/criação de itens.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, 
                          GroupsPermissionForItemManipulation]

    def get(self, request):
        query_set = Item.objects.all()
        if request.user and not request.user.groups.filter(name='Cliente').exists():
            serializer = ItemSerializer(query_set, many=True)
        else:
            # Usuarios nao autenticados ou com baixa permissao nao tem acesso a informacoes internas do item
            serializer = ItemResumeSerializer(query_set, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ItemDetail(APIView):
    """
    API Endpoint - GET/PATCH/DELETE item especifio via <str:codigo_item>.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          GroupsPermissionForItemManipulation]

    def _get_item(self, codigo):
        try:
            return Item.objects.get(codigo_item= codigo)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, codigo_item):
        item = self._get_item(codigo_item)
        if request.user and not request.user.groups.filter(name='Cliente').exists():
            serializer = ItemSerializer(item)
        else:
            serializer = ItemResumeSerializer(item)
        return Response(serializer.data)
    
    def patch(self, request, codigo_item):
        item = self._get_item(codigo_item)
        serializer = ItemUpdateSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, codigo_item):
        item = self._get_item(codigo_item)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

