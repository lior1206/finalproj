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
        ARGOCD_SERVER = 'argocd-server.argocd.svc.cluster.local:80' 
        HELM_REPO_URL = 'https://raw.githubusercontent.com/lior1206/finalproj/master/final-helm'
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
                    echo "Triggering ArgoCD sync with webhook URL: ${webhookURL}"
                    sh "curl -X POST '${webhookURL}' -H 'Content-Type: application/json' -d '{}'"
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
        }
        failure {
            echo 'Pipeline failed! Sending notifications...'
        }
    }
}
