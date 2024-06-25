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
                    dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
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
