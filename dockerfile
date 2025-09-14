# Use Python 3.11 slim
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (para cache do Docker)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Definir variáveis de ambiente para EasyPanel
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Configurações do banco EasyPanel
ENV DB_HOST=easypanel.pontocomdesconto.com.br
ENV DB_PORT=33070
ENV DB_USER=erp_admin
ENV DB_PASSWORD=8de3405e496812d04fc7
ENV DB_NAME=erp

# Porta padrão
ENV PORT=8000

# Expor porta
EXPOSE $PORT

# Comando para iniciar a aplicação
CMD ["python", "run.py"]