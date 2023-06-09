from itens.models import Item
from rest_framework import serializers
from rest_framework.fields import empty


class ItemResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['codigo_item', 'nome', 'descricao', 'preco']


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'codigo_item', 'nome', 'descricao', 'preco', 'quantidade_estoque']


class ItemUpdateSerializer(serializers.ModelSerializer):
    descricao = serializers.CharField(required=False)
    codigo_item = serializers.CharField(required=False)
    nome = serializers.CharField(required=False)
    preco = serializers.FloatField(required=False)

    class Meta:
        model = Item
        fields = ['id', 'codigo_item', 'nome', 'descricao', 'preco', 'quantidade_estoque']

    def validate_codigo_item(self, codigo_item):
        if not self.instance.codigo_item == codigo_item:
            if Item.objects.filter(codigo_item=codigo_item).exists():
                raise serializers.ValidationError("Este código de item não está disponivel.")
        return codigo_item
    
    def validate_quantidade_estoque(self, quant):
        if not isinstance(quant, int) or quant < 0:
            raise serializers.ValidationError("Valor fornecido para quantidade é inválido.")
        return quant

    def update(self, instance, validated_data):
        try:
            codigo_item = validated_data.get('codigo_item', instance.codigo_item)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        
        instance.codigo_item = codigo_item
        instance.nome = validated_data.get('nome', instance.nome)
        instance.descricao = validated_data.get('descricao', instance.descricao)
        instance.preco = validated_data.get('preco', instance.preco)
        instance.quantidade_estoque = validated_data.get('quantidade_estoque', instance.quantidade_estoque)
        instance.save()
        return instance