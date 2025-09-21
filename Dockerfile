# 1. Usar uma imagem oficial do Python como base
FROM python:3.11-slim

# 2. Definir o diretório de trabalho dentro do container
WORKDIR /code

# 3. Copiar o arquivo de dependências e instalar
COPY ./app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 4. Copiar todo o código da aplicação para dentro do container
COPY ./app /code/app

# 5. Expor a porta que a aplicação vai rodar
EXPOSE 8000

# 6. Comando para iniciar a aplicação quando o container rodar
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]