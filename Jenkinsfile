pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "hamzay123/jenkin-hms:latest"
        DOCKER_CREDENTIALS = "docker-hub-credentials" // Jenkins DockerHub credentials ID
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', 
                    credentialsId: 'github-credentials', 
                    url: 'https://github.com/Humzay123/hms.git'
            }
        }

        // NEW STEP: Generate Dockerfile
        stage('Generate Dockerfile') {
            steps {
                script {
                    sh """
                    cat << EOF > Dockerfile
                    FROM ubuntu:latest
                    RUN apt-get update && apt-get install -y curl
                    CMD ["echo", "Hello from Docker"]
                    EOF
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE ."
                }
            }
        }

        stage('Login to DockerHub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                    }
                }
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                script {
                    sh "docker push $DOCKER_IMAGE"
                }
            }
        }
    }
}
