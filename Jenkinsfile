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
                sh 'nohup python3 manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &'
                sleep 10 // Give the server some time to start
                sh 'ps aux | grep manage.py' // Verify if the process is running
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
