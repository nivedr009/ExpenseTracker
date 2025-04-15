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
            echo 'Building Docker image...'
            bat 'docker build -t expense-tracker .'
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
