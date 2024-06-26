pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub'  // Credentials ID for Docker Hub
        DOCKER_IMAGE = 'abhifarhan42/healthapp'  // Docker Hub username and image name
    }
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/abdulhaseebs/Healthapp.git'  // GitHub repository URL
            }
        }
        
        stage('Build and Push Docker Image') {
            steps {
                script {
                    def dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        dockerImage.push('latest')
                        dockerImage.push("${env.BUILD_ID}")
                    }
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                script {
                    sh '''
                    #!/bin/bash
                    docker rmi ${DOCKER_IMAGE}:${env.BUILD_ID}
                    '''
                }
            }
        }
    }
}
