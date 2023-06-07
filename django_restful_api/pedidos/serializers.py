from django.contrib.auth.models import User
from itens.models import Item
from pedidos.models import ItemPedido, Pedido
from rest_framework import serializers


class ItemCreatePedidoSerializer(serializers.ModelSerializer):
    item = serializers.SlugRelatedField(slug_field='codigo_item', queryset=Item.objects.all())
    class Meta:
        model = ItemPedido
        fields = ['id', 'item', 'quantidade']


class PedidoCreateSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField()
    itens = ItemCreatePedidoSerializer(many=True, source='itenspedido')

    class Meta:
        model = Pedido
        fields = ['usuario', 'data_criacao', 'itens']

    def validate_usuario(self, usuario):
        try:
            return User.objects.get(username=usuario)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não encontrado.")

    def create(self, validated_data):
        itens_data = validated_data.pop('itenspedido')

        try:
            usuario = validated_data['usuario']
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)

        pedido = Pedido.objects.create(usuario=usuario)
        
        for item_data in itens_data:
            item = item_data.pop('item')
            quantidade = item_data.pop('quantidade')
            ItemPedido.objects.create(pedido=pedido, item=item, quantidade=quantidade)
        
        return pedido
