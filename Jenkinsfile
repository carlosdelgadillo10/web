
node {
    def app

    stage('Clone repository') {

        checkout scm
    }

    stage('Build image') {
       app = docker.build("carlosdelgadillo/web")
    }
    stage('Deploy for Testing') {
            steps {
                script {
                    try {
                        sh '''
                            # Ejecutar el contenedor de la aplicación
                            docker run -d -p 5000:5000 carlosdelgadillo/web

                            # Verificar que el contenedor esté en ejecución
                            docker ps
                        '''
                    } catch (Exception e) {
                        error "Failed to deploy the application for testing: ${e.message}"
                    }
                }
            }
        }
    stage('DAST Analysis') {
            steps {
                script {
                    // Usando OWASP ZAP Docker container para ejecutar el análisis
                    sh '''
                        docker run -t --network host  zap-baseline.py \
                        -t http://localhost:5000 -r zap_report.html
                    '''
                }
            }
        }
    stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'zap_report.html', allowEmptyArchive: true
            }
        }

    stage('Push image') {
        
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            app.push("${env.BUILD_NUMBER}")
        }
    }
    
    stage('Trigger ManifestUpdate') {
                echo "hola erdnando"

        }
}
