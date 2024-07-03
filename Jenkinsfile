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
                    def dockerImage = docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}", "-f Dockerfile .")
                }
            }
        }
        stage('Merge Request Checks') {
            when {
                expression {
                    // Only merge if the branch is not 'master'
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
                    // Only merge into 'master' if the branch is not 'master'
                    return env.BRANCH_NAME != 'master'
                }
            }
            steps {
                script {
                    echo "Merging branch ${env.BRANCH_NAME} to 'master'..."
                    sh "git checkout master"
                    sh "git merge origin/${env.BRANCH_NAME} --no-ff -m \"Merge ${env.BRANCH_NAME} branch\""
                    sh "git push origin master"
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
