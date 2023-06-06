from django.db import models


class Item(models.Model):
    codigo_item = models.CharField(max_length=9, unique=True)
    nome = models.CharField(max_length=75)
    descricao = models.TextField()
    preco = models.FloatField()
    quantidade_estoque = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.nome
    
    def __str_descricao__(self):
        return f'{self.nome} - {self.descricao}'
