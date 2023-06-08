import random
import string

from django.contrib.auth.models import User
from django.db import models
from itens.models import Item


def _generate_random_code():
    len = 8
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(len))


class Pedido(models.Model):
    codigo_pedido = models.CharField(max_length= 8, unique=True, editable=False, default= _generate_random_code())
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itenspedido')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()

    class Meta:
        unique_together = ['pedido', 'item']

