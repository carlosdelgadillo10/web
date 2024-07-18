# Dockerfile para Flask
FROM python:3.11-slim

#FROM ubuntu:16.04
#RUN apt-get update && apt-get install -y --no-install-recommends \
##    python3.5 \
#    python3-pip \
#    && \
#apt-get clean && \
#rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
RUN mkdir /app
WORKDIR /app

# Copiar requisitos
COPY /requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt 

# Copiar el código de la aplicación Antes era web/ .
COPY . .

ENV PUERTO=5000

EXPOSE $PUERTO

CMD ["python", "app.py"]

