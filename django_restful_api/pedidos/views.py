from django.shortcuts import render
from pedidos.models import Pedido
from pedidos.serializers import PedidoCreateSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class PedidoGeneral(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        pedidos = Pedido.objects.all()
        serializer = PedidoCreateSerializer(pedidos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PedidoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)