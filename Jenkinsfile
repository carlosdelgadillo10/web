node {
    def app

    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
        script {
            app = docker.build("carlosdelgadillo/web")
        }
    }

    stage('Deploy for Testing') {
        script {
            try {
                sh '''
                    # Detener y eliminar cualquier contenedor existente con el mismo nombre
                    docker stop test-app || true
                    docker rm test-app || true

                    # Ejecutar el contenedor de la aplicación
                    docker run -d --name test-app -p 9000:9000 carlosdelgadillo/web

                    # Verificar que el contenedor esté en ejecución
                    docker ps
                '''
            } catch (Exception e) {
                error "Failed to deploy the application for testing: ${e.message}"
            }
        }
    }



    stage('Push image') {
        script {
            docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                app.push("${env.BUILD_NUMBER}")
            }
        }
    }

    stage('Trigger ManifestUpdate') {
        echo "hola erdnando"
    }
}
