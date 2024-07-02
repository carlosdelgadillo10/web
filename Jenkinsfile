pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'https://registry.hub.docker.com'
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials' // ID de tus credenciales de Docker en Jenkins
        ZAP_DOCKER_IMAGE = 'carlosdelgadillo/web'
        ZAP_REPORT = 'zap_report.html'
        APP_CONTAINER_NAME = 'app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script {
                    app = docker.build("carlosdelgadillo/web")
                }
            }
        }

        stage('Deploy for Testing') {
            steps {
                script {
                    try {
                        sh '''

                            # Ejecutar el contenedor de la aplicación
                            docker run -d --name ${APP_CONTAINER_NAME} -p 8080:80 carlosdelgadillo/web

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
                    try {
                        sh '''
                            # Ejecutar OWASP ZAP para analizar la aplicación
                            docker run --network="host" \
                                -v $(pwd):/zap/wrk/ \
                                ${ZAP_DOCKER_IMAGE} zap-baseline.py \
                                -t http://localhost:8080 -r ${ZAP_REPORT}

                            # Verificar si el reporte de ZAP fue generado
                            ls -l ${ZAP_REPORT}
                        '''
                    } catch (Exception e) {
                        error "DAST analysis failed: ${e.message}"
                    }
                }
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: "${ZAP_REPORT}", allowEmptyArchive: true
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

        stage('Clean Up') {
            steps {
                script {
                    try {
                        // Detener y eliminar el contenedor de la aplicación
                        sh '''
                            docker stop ${APP_CONTAINER_NAME}
                            docker rm ${APP_CONTAINER_NAME}
                        '''
                    } catch (Exception e) {
                        error "Cleanup failed: ${e.message}"
                    }
                }
            }
        }
    }

    post {
        always {
            // Opcional: Eliminar la imagen de Docker después de cada build para ahorrar espacio
            sh 'docker rmi mi-aplicacion:latest || true'
        }
    }
}


    

