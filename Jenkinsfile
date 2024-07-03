pipeline {
    agent {
        kubernetes {
            yamlFile 'build-pod.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }

    environment {
        DOCKER_IMAGE = 'liorgerbi/finalproj'
        IMAGE_TAG = 'latest'
        GITHUB_API_URL = 'https://api.github.com'
        GITHUB_REPO = 'lior1206/finalproj'
        GITHUB_TOKEN ='githubcred'
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
                    dockerImage = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}", "--no-cache .")
                }
            }
        }

        stage('Push Docker image') {
            when {
                branch 'master'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-creds') (
                        dockerImage.push("latest")
                    )
                }
            }
        }

        stage('Create merge request') {
            when {
                not {
                    branch 'master'
                }
            }
            steps {
                withCredentials([string(credentialsId: 'githubcred', usernameVariable:'USERNAME' , passwordVariable:'PASSWORD' )]) {
                    script {
                        def branchName = env.BRANCH_NAME
                        def pullRequestTitle = "Merge ${branchName} into master"
                        def pullRequestBody = "Automatically generated merge request for branch ${branchName}"

                        sh """
                            curl -X POST -u ${USERNAME}:${PASSWORD} \
                            -d '{ "title": "${pullRequestTitle}", "body": "${pullRequestBody}", "head": "${branchName}", "base": "master" }' \
                            ${GITHUB_API_URL}/repos/${GITHUB_REPO}/pulls
                        """
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
