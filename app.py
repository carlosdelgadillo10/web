#Pagina web
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Obtener las IPs de los microservicios desde las variables de entorno sin valores por defecto
URL_SUMA = os.getenv('URL_SUMA')
URL_RESTA = os.getenv('RESTAR_END')
MULTIPLICAR_END = os.getenv('MULTIPLICAR_END')
DIVIDIR_END = os.getenv('DIVIDIR_END')
# Obtener el puerto desde la variable de entorno
PUERTO = int(os.getenv('PUERTO'))

@app.route('/')
def index():
    return render_template('index.html', resultado='')

@app.route('/calcular', methods=['POST'])
def calcular():
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
        response = requests.post(MULTIPLICAR_END, json={'num1': num1, 'num2': num2})
    elif '/' in expression:
        num1, num2 = map(float, expression.split('/'))
        response = requests.post(DIVIDIR_END, json={'num1': num1, 'num2': num2})
    else:
        return render_template('index.html', resultado='Error: Operación no válida')

    if response.status_code == 200:
        resultado = response.json()
        return render_template('index.html', resultado=resultado)
    else:
        return render_template('index.html', resultado='Error en la solicitud al microservicio')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PUERTO) #host='0.0.0.0' hace que la aplicación esté accesible desde cualquier dirección IP de la máquina.
