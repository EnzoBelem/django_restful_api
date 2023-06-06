from django.shortcuts import render
from itens.models import Item
from itens.serializers import ItemResumeSerializer, ItemSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from usuarios.permissions import GroupsPermissionForItemManipulation


class ItemGeneral(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, 
                          GroupsPermissionForItemManipulation]

    def get(self, request):
        query_set = Item.objects.all()
        if request.user and not request.user.groups.filter(name='Cliente').exists():
            serializer = ItemSerializer(query_set, many=True)
        else:
            serializer = ItemResumeSerializer(query_set, many=True)
        
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ItemDetail(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          GroupsPermissionForItemManipulation]

    def get(self, request):
        pass
