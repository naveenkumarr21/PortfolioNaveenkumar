pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh 'docker build -t my-static-app:latest .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Stop and remove any existing container with the same name
                    sh 'docker stop my-static-app-container || true'
                    sh 'docker rm my-static-app-container || true'

                    // Run the Docker container on localhost:3000
                    sh 'docker run -d -p 3000:80 --name my-static-app-container my-static-app:latest'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Application is running on http://localhost:3000'
        }
        failure {
            echo 'Pipeline failed! Check the logs for errors.'
        }
    }
}
