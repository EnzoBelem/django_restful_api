# Generated by Django 4.2.1 on 2023-06-06 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itens', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='quantidade',
            new_name='quantidade_estoque',
        ),
    ]
