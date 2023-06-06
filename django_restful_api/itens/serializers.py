from itens.models import Item
from rest_framework import serializers
from rest_framework.fields import empty


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'codigo_item', 'nome', 'descricao', 'preco', 'quantidade_estoque']


class ItemResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['codigo_item', 'nome', 'descricao', 'preco']