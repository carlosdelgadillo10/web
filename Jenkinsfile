pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "carlosdelgadillo/web"
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/carlosdelgadillo10/web.git', branch: 'main'
            }
        }
        stage('Build') {
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
                        sh 'npm test'
                    }
                }
            }
        }
        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub') {
                        dockerImage.push("${env.BUILD_ID}")
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    sh 'docker run -d -p 5000:5000 ${DOCKER_IMAGE}:${env.BUILD_ID}'
                }
            }
        }
    }
}

