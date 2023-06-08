from django.contrib import admin
from itens.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass

