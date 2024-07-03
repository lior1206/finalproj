pipeline {
   agent{
        kubernetes{
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
        stage('build docker image') {     
             steps{

                script{
                  def dockerImage = docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}", "-f Dockerfile .")
                    
                    // Example of commands to execute inside the Docker container
                    dockerImage.inside {
                        sh 'echo "Running inside the Docker container"'
                        // Add more commands as needed
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
