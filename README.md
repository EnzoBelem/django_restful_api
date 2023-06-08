# django_restful_api
Projeto feito para o desafio da Medclub de criar uma API RESTful que gerencie usuários, pedidos e itens.

## Como configurar e executar este projeto em sua máquina
### 1 - Clonar o projeto
Usando o terminal/bash da sua preferência execute o seguinte comando git:
```
git clone https://github.com/EnzoBelem/django_restful_api.git
```
### 2 - Criar e configurar o ambiente virtual
#### 2.1 - Versão do python
Este projeto foi desenvolvido na versão [3.10.11](https://www.python.org/downloads/release/python-31011/) do Python.
#### 2.2 - Criando o ambiente virtual
Dentro da pasta do projeto execute o seguinte comando:
- Windows
```
python -m venv venv
```
- Linux
```
python3.10 -m venv venv
```
#### 2.3 - Dificuldades com a versão do Python no Windows
Caso seu sistema já possua alguma versão do Python instalada alguns problemas podem surgir. Verifique se a versão 3.10.11 é a versão global do Python,
caso não seja aqui vão algumas dicas importantes:
- Verifique e altere as variáveis de ambiente do Python no seu sistema.
- Crie o ambiente usando o caminho direto para a versão 3.10.11:
```
C:\Users\usuario\AppData\Local\Programs\Python\Python310\python.exe -m venv venv
```
#### 2.4 - Configurando o ambiente virtual
Agora precisamos instalar todos os pacotes necessários para executar o projeto de forma correta.<br>
Com seu terminal/bash aberto dentro da pasta do projeto inicie o ambiente virtual com o seguinte comando:
- Windows
```
.\venv\Scripts\activate
```
- Linux
```
source venv/bin/activate
```
Agora precisamos instalar os seguintes pacotes:
```
pip install django
pip install djangorestframework
```
### 3 - Migrações do projeto
Agora que temos nosso ambiente virtual criado e configurado, precisamos realizar as migrações necessárias para configurar o banco de dados.<br>
Com o seu ambiente virtual executando vá para a pasta do projeto Django e execute o seguinte comando:
```
python manage.py migrate
```
### 4 - Executar o projeto
Nessa etapa todas as configurações já foram feitas e basta executar o projeto usando o seguinte comando:
```
python manage.py runserver
```
O projeto será executado na porta padrão 8000.
```
System check identified no issues (0 silenced).
June 08, 2023 - 18:35:38
Django version 4.2.1, using settings 'django_restful_api.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
Agora você pode usar a API como quiser, lembrando que a documentação completa do projeto se encontra no arquivo DOCS.md.
