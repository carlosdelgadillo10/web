# Dockerfile para Flask
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo
RUN mkdir /app
WORKDIR /app

# Copiar requisitos
COPY /requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --upgrade pipenv\
    && apt-get clean \
    && apt-get update \
    && apt install -y build-essential \
    && apt install -y libmariadb3 libmariadb-dev \
    && pip install --upgrade -r /opt/microservices/requirements.txt

# Copiar el código de la aplicación Antes era web/ .
COPY / .


EXPOSE 8080

CMD ["python", "app.py", "8080"]

