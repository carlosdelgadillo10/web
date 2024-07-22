Página Web con Flask y Microservicios

Esta aplicación web está construida con Flask y se comunica con varios microservicios para realizar operaciones matemáticas (suma, resta, multiplicación y división). La aplicación obtiene las direcciones de los microservicios a través de variables de entorno.

Configuración de Variables de Entorno

Asegúrate de configurar las siguientes variables de entorno antes de ejecutar la aplicación:

- `URL_SUMAR`: URL del microservicio de suma.
- `URL_RESTAR`: URL del microservicio de resta.
- `URL_MULTIPLICAR`: URL del microservicio de multiplicación.
- `URL_DIVIDIR`: URL del microservicio de división.
- `PUERTO`: Puerto en el que se ejecutará la aplicación Flask (por defecto, 5000).

Uso con Docker

Construir la Imagen Docker

Para construir la imagen Docker de la aplicación, utiliza el siguiente comando en el directorio donde se encuentra el `Dockerfile`:

```sh
docker build -t nombre_imagen:tag .

Ejecutar el Contenedor Docker

Para ejecutar la imagen Docker, utiliza el siguiente comando. Asegúrate de reemplazar las URLs y el puerto con los valores correctos:

docker run -d -p 5000:5000 \
  -e URL_SUMAR=http://localhost:8001/sumar \
  -e URL_RESTAR=http://localhost:8002/restar \
  -e URL_MULTIPLICAR=http://localhost:8003/multiplicar \
  -e URL_DIVIDIR=http://localhost:8004/dividir \
  -e PUERTO=5000 \
  nombre_imagen:tag

