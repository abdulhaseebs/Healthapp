pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKER_IMAGE = 'abhifarhan42/healthappjenkins'
    }

    stages {
        
        stage('Build Docker Image') {
            steps {
                script {
                    def dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                    dockerImage.tag("${DOCKER_IMAGE}:latest")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        dockerImage.push("${env.BUILD_ID}")
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Clean up') {
            steps {
                sh "docker rmi ${DOCKER_IMAGE}:${env.BUILD_ID}"
                sh "docker rmi ${DOCKER_IMAGE}:latest"
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Any additional success criteria can be added here.'
        }
        failure {
            echo 'Pipeline failed! Any additional failure handling can be added here.'
        }
    }
}
