pipeline {
    agent {
        kubernetes {
            yamlFile 'build-pod.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }

    environment {
        DOCKER_REGISTRY = 'liorgerbi'
        IMAGE_NAME = 'finalproj'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}", "-f Dockerfile .")
                }
            }
        }

        stage('Merge Request Checks') {
            when {
                expression {
                    return env.BRANCH_NAME != 'master'
                }
            }
            steps {
                script {
                    echo "Running merge request checks for branch ${env.BRANCH_NAME}..."
                    // Example: Run tests, validate code, etc.
                }
            }
        }

        stage('Merge to Master') {
            when {
                expression {
                    return env.BRANCH_NAME != 'master'
                }
            }
            steps {
                script {
                    echo "Merging branch ${env.BRANCH_NAME} to 'master'..."
                    sh """
                        git config user.name "jenkins"
                        git config user.email "jenkins@example.com"
                        git checkout master
                        git pull origin master
                        git merge --no-ff origin/${env.BRANCH_NAME} -m "Merge ${env.BRANCH_NAME} branch"
                        git push origin master
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', 'docker-credentials-id') {
                        docker.image("${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}").push()
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Triggering further actions...'
            // Add post-build actions here, such as notifications or triggering downstream jobs
        }
        failure {
            echo 'Pipeline failed! Sending notifications...'
            // Add actions to handle pipeline failures
        }
    }
}
