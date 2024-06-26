
node {
    def app

    stage('Clone repository') {

        checkout scm
    }

    stage('Build image') {
       app = docker.build("carlosdelgadillo/web")
    }

    stage('Push image') {
        
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            app.push("${env.BUILD_NUMBER}")
        }
    }
    
    stage('Trigger ManifestUpdate') {
                echo "hola como estas"

        }
}
