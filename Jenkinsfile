pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub') // Jenkins credentials ID for Docker Hub
        DOCKER_IMAGE = 'yourdockerhubusername/healthapp-streamlit' // Replace with your Docker Hub username and repository name
        STREAMLIT_PORT = 8501 // Port on which Streamlit app runs
    }
    
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/abdulhaseebs/Healthapp.git', branch: 'main' // Replace with your GitHub repository URL and branch
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                    dockerImage.tag("${DOCKER_IMAGE}:latest") // Tag the image as 'latest'
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    // Push the Docker image to Docker Hub
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        dockerImage.push("${env.BUILD_ID}")
                        dockerImage.push('latest')
                    }
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                sh "docker rmi ${DOCKER_IMAGE}:${env.BUILD_ID}" // Clean up images locally
                sh "docker rmi ${DOCKER_IMAGE}:latest"
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline succeeded! Docker image deployed to Docker Hub.'
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
    }
}
