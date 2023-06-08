from django.http import Http404
from pedidos.models import Pedido
from pedidos.serializers import PedidoSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class PedidoGeneral(APIView):
    """
    API Endpoint - listagem/criação de pedidos.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.groups.filter(name='Cliente').exists():
            pedidos = Pedido.objects.filter(usuario= request.user)
        else:
            pedidos = Pedido.objects.all()
        context={'request': request, 'resume_request': True}
        serializer = PedidoSerializer(pedidos, many=True, context=context)
        return Response(serializer.data)

    def post(self, request):
        serializer = PedidoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PedidoDetail(APIView):
    """
    API Endpoint - requisição de dados completos para um pedido especifico.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, codigo_pedido):
        try:
            pedido = Pedido.objects.get(codigo_pedido=codigo_pedido)
            serializer = PedidoSerializer(pedido, context={'request': request})
            return Response(serializer.data)
        except Pedido.DoesNotExist:
            raise Http404
            
