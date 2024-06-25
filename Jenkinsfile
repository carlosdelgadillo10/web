node {
    def application = "web"
    def dockerhubaccountid = "carlosdelgadillo"
    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
        app = docker.build("${dockerhubaccountid}/${application}:${BUILD_NUMBER}")
    }

    stage('Push image') {
        withCredentials([usernamePassword( credentialsId: 'dockerHub', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
            def registry_url = "registry.hub.docker.com/"
            sh "docker login -u $USER -p $PASSWORD ${registry_url}"
            withDockerRegistry([ credentialsId: "dockerHub", url: "registry.hub.docker.com/" ]) {
                // Push your image now
                        app.push()
                        app.push("latest")
            }
        }
    }

    stage('Deploy') {
        sh ("docker run -d -p 3333:3333 ${dockerhubaccountid}/${application}:${BUILD_NUMBER}")
    }

    stage('Remove old images') {
        // remove old docker images
        sh("docker rmi ${dockerhubaccountid}/${application}:latest -f")
   }
}