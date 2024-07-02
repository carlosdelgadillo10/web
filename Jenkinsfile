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
                    docker run -d --name test-app -p 5000:5000 carlosdelgadillo/web

                    # Verificar que el contenedor esté en ejecución
                    docker ps
                '''
            } catch (Exception e) {
                error "Failed to deploy the application for testing: ${e.message}"
            }
        }
    }

    stage('DAST Analysis') {
        script {
            try {
                sh '''
                    # Usando OWASP ZAP Docker container para ejecutar el análisis
                    docker run --network host -v $(pwd):/zap/wrk/ owasp/zap2docker-stable zap-baseline.py \
                    -t http://localhost:5000 -r zap_report.html

                    # Verificar si el reporte de ZAP fue generado
                    ls -l zap_report.html
                '''
            } catch (Exception e) {
                error "DAST analysis failed: ${e.message}"
            }
        }
    }

    stage('Archive Results') {
        archiveArtifacts artifacts: 'zap_report.html', allowEmptyArchive: true
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
