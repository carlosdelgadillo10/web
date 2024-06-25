pipeline {
    agent any
    
    environment {
        GITHUB_CREDENTIALS = credentials('github-token') // ID configurado en Jenkins para el token de GitHub
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credential') // ID configurado en Jenkins para DockerHub
        DOCKER_IMAGE = "carlosdelgadillo/web" // Reemplaza "tu_usuario/tu_microservicio" con tu nombre de usuario e imagen
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    git url: 'https://github.com/carlosdelgadillo10/web.git', credentialsId: 'github-token'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Construir la imagen Docker
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}", "-t ${DOCKER_IMAGE} .")
                    
                    // Detener y eliminar el contenedor si ya está en ejecución (opcional)
                    sh '''
                    if [ "$(docker ps -q -f name=${DOCKER_IMAGE}_container)" ]; then
                        docker stop ${DOCKER_IMAGE}_container
                        docker rm ${DOCKER_IMAGE}_container
                    fi
                    '''

                    // Ejecutar el contenedor en segundo plano
                    sh 'docker run -d -p 5000:5000 --name ${DOCKER_IMAGE}_container ${DOCKER_IMAGE}'
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    dockerImage.inside {
                        // Agrega aquí los comandos necesarios para realizar pruebas.
                        sh 'npm test' // Ejemplo para Node.js; ajusta según tu stack tecnológico.
                    }
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credential') {
                        dockerImage.push("${env.BUILD_ID}")
                        dockerImage.push('latest')
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    // Detener y eliminar contenedores existentes que usan la misma imagen
                    sh '''
                    if [ "$(docker ps -q -f name=web)" ]; then
                        docker stop web
                        docker rm web
                    fi
                    '''

                    // Ejecutar el nuevo contenedor con la nueva imagen
                    sh """
                    docker run -d --name web -p 5000:5000 ${DOCKER_IMAGE}:${env.BUILD_ID}
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs() // Limpia el espacio de trabajo después de cada ejecución.
        }
        success {
            echo 'Build y despliegue exitoso.'
        }
        failure {
            echo 'Build o despliegue fallido.'
        }
    }
}
