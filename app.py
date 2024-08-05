#Pagina web
from flask import Flask, render_template, request, jsonify
import requests
import os
from prometheus_client import start_http_server, Summary, Counter, generate_latest

app = Flask(__name__)

# Obtener las IPs de los microservicios desde las variables de entorno sin valores por defecto
URL_SUMA = os.getenv('URL_SUMAR')
URL_RESTA = os.getenv('URL_RESTAR')
URL_MULTI = os.getenv('URL_MULTIPLICAR')
URL_DIVIDIR = os.getenv('URL_DIVIDIR')
# Obtener el puerto desde la variable de entorno
PUERTO = int(os.getenv('PUERTO'))

# Crear métricas de Prometheus
REQUEST_COUNT = Counter('web_requests_total', 'Total number of requests made')
REQUEST_LATENCY = Summary('web_request_latency_seconds', 'Latency of requests in seconds')


@app.route('/')
def index():
    return render_template('index.html', resultado='')

@app.route('/calcular', methods=['POST'])
@REQUEST_LATENCY.time()
def calcular():
    REQUEST_COUNT.inc()
    expression = request.form['expression']

    # Verificar que todas las URLs necesarias estén definidas
    #if not all([SUMAR_SERVICE_URL, RESTAR_SERVICE_URL, MULTIPLICAR_SERVICE_URL, DIVIDIR_SERVICE_URL]):
        #return render_template('index.html', resultado='Error: Las variables de entorno de los microservicios no están configuradas')

    # Realiza la solicitud al microservicio correspondiente
    if '+' in expression:
        num1, num2 = map(float, expression.split('+'))
        response = requests.post(URL_SUMA , json={'num1': num1, 'num2': num2})
    elif '-' in expression:
        num1, num2 = map(float, expression.split('-'))
        response = requests.post(URL_RESTA, json={'num1': num1, 'num2': num2})
    elif '*' in expression:
        num1, num2 = map(float, expression.split('*'))
        response = requests.post(URL_MULTI, json={'num1': num1, 'num2': num2})
    elif '/' in expression:
        num1, num2 = map(float, expression.split('/'))
        response = requests.post(URL_DIVIDIR, json={'num1': num1, 'num2': num2})
    else:
        return render_template('index.html', resultado='Error: Operación no válida')

    if response.status_code == 200:
        resultado = response.json()
        return render_template('index.html', resultado=resultado)
    else:
        return render_template('index.html', resultado='Error en la solicitud al microservicio')

@app.route('/metrics')
def metrics():
    return generate_latest(), 200

if __name__ == '__main__':
    start_http_server(8000)  # Exponer las métricas en el puerto 8000
    app.run(host='0.0.0.0', port=PUERTO) #host='0.0.0.0' hace que la aplicación esté accesible desde cualquier dirección IP de la máquina.
