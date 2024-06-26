pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKER_IMAGE = 'abhifarhan42/healthappjenkins'
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
                    dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        dockerImage.push('latest')
                        dockerImage.push("${env.BUILD_ID}")
                    }
                }
            }
        }

        stage('Clean up') {
            steps {
                sh 'docker rmi ${DOCKER_IMAGE}:${env.BUILD_ID}'
            }
        }
    }
}
