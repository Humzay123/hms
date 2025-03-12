pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Humzay123/hms.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t hamzay123/hms-django:latest .'
            }
        }

        stage('Login to DockerHub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                    sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push hamzay123/hms-django:latest'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                // Add Kubernetes deployment or Docker run command here
            }
        }
    }
}
