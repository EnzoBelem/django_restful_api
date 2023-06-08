from django.contrib.auth.models import Group


def create_groups():
    group_names = ['Cliente', 'Funcionário', 'Gerência']
    
    if Group.objects.count() == len(group_names):
        return

    for group_name in group_names:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f'Grupo {group_name} criado com sucesso!')
        else:
            print(f'Grupo {group_name} já existe.')
    

class UserGroupVerify():
    @staticmethod
    def is_cliente(user):
       return user.groups.filter(name='Cliente').exists()
    
    @staticmethod
    def is_funcionario(user):
       return user.groups.filter(name='Funcionário').exists()
    
    @staticmethod
    def is_gerencia(user):
       return user.groups.filter(name='Gerência').exists()