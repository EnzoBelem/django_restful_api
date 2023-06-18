# imagem base do conteiner
FROM python:3.10.11-slim

# diretorio de trabalho dentro do conteiner
WORKDIR /django_restful_api

# copia o arquivo requirements.txt para a pasta do projeto dentro do container
COPY requirements.txt .

# instala as dependencias do projeto
RUN pip install -r requirements.txt 

# copia o restante do projeto para a pasta do projeto dentro do container
COPY . .

# executa as migracoes do projeto
RUN python django_restful_api/manage.py migrate

# comando a ser executado quando o conteiner for iniciado
CMD ["python", "django_restful_api/manage.py", "runserver", "0.0.0.0:8000"]

