from django.contrib.auth.models import User
from itens.models import Item
from pedidos.models import ItemPedido, Pedido
from rest_framework import serializers


class ItemPedidoSerializer(serializers.ModelSerializer):
    item = serializers.SlugRelatedField(slug_field='codigo_item', queryset=Item.objects.all())
    descricao = serializers.CharField(source = 'item.descricao', read_only=True)

    class Meta:
        model = ItemPedido
        fields = ['id', 'item', 'descricao', 'quantidade']

    def to_representation(self, instance):
        user = self.context.get('request').user
        fields = super().to_representation(instance)
        if user.groups.filter(name='Cliente').exists():
            fields.pop('id')

        return fields


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, source='itenspedido')
    usuario = serializers.CharField(required= False)

    class Meta:
        model = Pedido
        fields = ['id', 'codigo_pedido', 'usuario', 'data_criacao', 'itens']

    def validate_usuario(self, usuario):
        try:
            user = self.context.get('request').user
            if user.groups.filter(name='Cliente').exists() and user.username != usuario:
                raise Exception()
            return User.objects.get(username=usuario)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não encontrado.")
        except Exception as exception:
            raise serializers.ValidationError("Esta operação não é permitida para Clientes.")

    def create(self, validated_data):
        user = self.context.get('request').user
        itens_data = validated_data.pop('itenspedido')

        try:
            usuario = validated_data.get('usuario', user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)

        pedido = Pedido.objects.create(usuario=usuario)
        
        for item_data in itens_data:
            item = item_data.pop('item')
            quantidade = item_data.pop('quantidade')
            ItemPedido.objects.create(pedido=pedido, item=item, quantidade=quantidade)
        
        return pedido
    
    def to_representation(self, instance):
        user = self.context.get('request').user
        fields = super().to_representation(instance)
        if user.groups.filter(name='Cliente').exists():
            fields.pop('id')

        return fields
    