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

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies from requirements.txt...'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker Compose services...'
                bat 'docker-compose -p expensetracker build'
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Deploying the application using Docker Compose...'
                bat 'docker-compose -p expensetracker up -d'
            }
        }

        stage('Wait for Server to be Ready') {
            steps {
                echo 'Waiting for the server to be fully up and running...'
                // Wait for the server to be available (e.g., 10 seconds)
                sleep 3
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running automated tests...'
                bat 'pytest tests/'
            }
        }
    }
}
