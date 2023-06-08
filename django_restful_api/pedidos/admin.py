from django.contrib import admin
from pedidos.models import ItemPedido, Pedido


@admin.register(Pedido)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(ItemPedido)
class ItemAdmin(admin.ModelAdmin):
    pass
