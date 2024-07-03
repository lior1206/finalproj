pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the Git repository
                checkout scm

                // Example: List files in the Jenkins workspace
                sh 'ls -l'
            }
        }

        // Add more stages as needed for build, test, deploy, etc.
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
