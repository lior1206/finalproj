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
        GITHUB_TOKEN = 'githubcred' 
        HELM_CHART_DIR = 'final-helm' 
        ARGOCD_APP_NAME = 'finalcd' 
        ARGOCD_SERVER = 'localhost:8080' 
        HELM_REPO_URL = 'https://lior1206.github.io/finalproj/final-helm/' // Update with your GitHub Pages URL
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare') {
            steps {
                script {
                    // Add the safe directory configuration if needed
                    def safeDirectory = "/home/jenkins/agent/workspace/finalproj_${env.BRANCH_NAME}"
                    sh "git config --global --add safe.directory ${safeDirectory}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}", "--no-cache .")
                }
            }
        }

        stage('Push Docker Image') {
            when {
                branch 'master'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-creds') {
                        dockerImage.push("latest")
                    }
                }
            }
        }

        stage('Update Helm Chart') {
            when {
                branch 'master'
            }
            steps {
                script {
                    sh "helm repo add myrepo ${HELM_REPO_URL}"
                    sh "helm repo update"
                    sh "helm package ${HELM_CHART_DIR}"
                    sh "helm repo index --url ${HELM_REPO_URL} --merge index.yaml ."
                    sh "helm repo update"
                }
            }
        }

        stage('Trigger ArgoCD Sync') {
            when {
                branch 'master'
            }
            steps {
                script {
                    def webhookURL = "http://${ARGOCD_SERVER}/api/webhook?project=default&application=${ARGOCD_APP_NAME}"
                    sh "curl -X POST $webhookURL"
                }
            }
        }

        stage('Create Merge Request') {
            when {
                not {
                    branch 'master'
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'githubcred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    script {
                        def branchName = env.BRANCH_NAME
                        def pullRequestTitle = "Merge ${branchName} into master"
                        def pullRequestBody = "Automatically generated merge request for branch ${branchName}"

                        sh """
                            curl -X POST -u ${USERNAME}:${PASSWORD} \\
                            -d '{ "title": "${pullRequestTitle}", "body": "${pullRequestBody}", "head": "${branchName}", "base": "master" }' \\
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
