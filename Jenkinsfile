pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub') // Update 'dockerhub' to match your credentials ID
        DOCKER_IMAGE = 'abhifarhan42/healthappjenkins'    // Update to match your Docker Hub repository name
    }

    stages {
        stage('Clone repository') {
            steps {
                git url: 'https://github.com/abdulhaseebs/Healthapp.git', branch: 'master'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                    // Optionally, you can tag the image with 'latest' for the latest build
                    dockerImage.tag("${DOCKER_IMAGE}:latest")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        dockerImage.push("${env.BUILD_ID}")
                        dockerImage.push('latest') // Push 'latest' tag to Docker Hub
                    }
                }
            }
        }

        stage('Clean up') {
            steps {
                sh "docker rmi ${DOCKER_IMAGE}:${env.BUILD_ID}"
                sh "docker rmi ${DOCKER_IMAGE}:latest" // Clean up 'latest' tag as well
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
