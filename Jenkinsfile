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
                        credentialsId: 'github-token'
                    ]]
                ])
            }
        }

        stage('Build') {
            steps {
                echo "Building the project..."
                sh 'nohup python3 manage.py runserver 0.0.0.0:8000 &'
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
                echo "Deploy"
            }
        }
    }
}
