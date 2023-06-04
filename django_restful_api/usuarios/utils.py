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