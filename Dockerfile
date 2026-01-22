# Usa uma imagem oficial do Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os ficheiros do repositório para o container
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta (opcional, o Discord não precisa de porta)
EXPOSE 8080

# Comando para iniciar o bot
CMD ["python", "main.py"]
