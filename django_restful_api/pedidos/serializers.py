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
            user = validated_data.get('usuario', user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)

        pedido = Pedido.objects.create(usuario=user)
        flag_error = False
        list_itens = []

        for item_data in itens_data:
            item = item_data.pop('item')
            quantidade = item_data.pop('quantidade')
            if item.quantidade_estoque >= quantidade:
                item.quantidade_estoque -= quantidade
                item.save()
                ItemPedido.objects.create(pedido=pedido, item=item, quantidade=quantidade)
            else:
                flag_error = True
                list_itens.append(item.nome)

        if flag_error:
            pedido.delete()
            raise serializers.ValidationError(f"Item/Itens: {', '.join(list_itens)} sem unidades suficientes em estoque.")
    
        return pedido
       
            
    def to_representation(self, instance):
        user = self.context.get('request').user
        resume_request = self.context.get('resume_request', False)
        fields = super().to_representation(instance)

        if user.groups.filter(name='Cliente').exists():
            fields.pop('id')
            fields.pop('usuario')
        
        if resume_request:
            fields.pop('itens')
            
        return fields
    