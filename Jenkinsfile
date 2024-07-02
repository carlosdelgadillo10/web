
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
                    docker.run("carlosdelgadillo/web", "-d -p 5000:80")
                }
            }
        }
    stage('DAST Analysis') {
            steps {
                script {
                    // Usando OWASP ZAP Docker container para ejecutar el análisis
                    sh '''
                        docker run -t --network host owasp/zap2docker-stable zap-baseline.py \
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
