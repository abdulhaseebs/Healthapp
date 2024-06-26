pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('abhifarhan42')  // Credentials ID for Docker Hub
        DOCKER_IMAGE = 'abhifarhan42/healthapp'  // Replace with your Docker Hub username and image name
    }
    
    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-pat', url: 'https://github.com/abdulhaseebs/Healthapp.git'  // Replace with your GitHub repository URL and credentials ID
            }
        }
        
        stage('Build and Push Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        dockerImage.push('latest')
                        dockerImage.push("${env.BUILD_ID}")
                    }
                }
            }
        }
        
        stage('Deploy to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        dockerImage.push('latest')
                        dockerImage.push("${env.BUILD_ID}")
                    }
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                sh 'docker rmi ${DOCKER_IMAGE}:${env.BUILD_ID}'
            }
        }
    }
}