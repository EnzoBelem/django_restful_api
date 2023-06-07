from django.contrib.auth.models import User
from django.db import models
from itens.models import Item


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itenspedido')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()

    class Meta:
        unique_together = ['pedido', 'item']

