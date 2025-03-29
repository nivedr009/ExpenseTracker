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
                service postgresql start
                service postgresql status
                sh 'python3 manage.py migrate'
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
                echo "Starting Django application..."
                sh 'nohup python3 manage.py runserver 0.0.0.0:8000 &'
            }
        }
    }
}
