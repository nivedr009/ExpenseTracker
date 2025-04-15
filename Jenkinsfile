pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout([ 
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    extensions: [], 
                    userRemoteConfigs: [[ 
                        url: 'https://github.com/nivedr009/ExpenseTracker.git', 
                        credentialsId: 'expenseid' 
                    ]] 
                ])
            }
        }

        stage('Build') {
            steps {
                echo "Building Docker image..."
                script {
                    // Build the Docker image with the application code
                    def imageName = 'expense-tracker-image'
                    def dockerfilePath = '.' // Path to Dockerfile (default is current directory)
                    
                    // Build the Docker image
                    sh "docker build -t ${imageName} ${dockerfilePath}"
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running tests..."
                // Add test commands here
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying the application..."
                // Add deployment commands here
            }
        }
    }
}
