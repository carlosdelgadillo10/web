#Pagina web
#nuevo cambio 5
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', resultado='')

@app.route('/calcular', methods=['POST'])
def calcular():
    expression = request.form['expression']

    # Realiza la solicitud al microservicio correspondiente
    if '+' in expression:
        num1, num2 = map(float, expression.split('+'))
        response = requests.post('127.0.0.1:8001/sumar', json={'num1': num1, 'num2': num2})
    elif '-' in expression:
        num1, num2 = map(float, expression.split('-'))
        response = requests.post('http://192.168.56.1:8004/restar', json={'num1': num1, 'num2': num2})
    elif '*' in expression:
        num1, num2 = map(float, expression.split('*'))
        response = requests.post('http://192.168.56.1:8003/multiplicar', json={'num1': num1, 'num2': num2})
    elif '/' in expression:
        num1, num2 = map(float, expression.split('/'))
        response = requests.post('http://192.168.56.1:8002/dividir', json={'num1': num1, 'num2': num2})
    else:
        return render_template('index.html', resultado='Error: Operación no válida')

    if response.status_code == 200:
        resultado = response.json()
        return render_template('index.html', resultado=resultado)
    else:
        return render_template('index.html', resultado='Error en la solicitud al microservicio')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
