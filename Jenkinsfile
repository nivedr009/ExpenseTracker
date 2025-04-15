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
                echo "Building the project..."
                
                // Start the Django server in the background
                sh 'nohup python3 manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &'
                
                // Wait for the server to start
                sleep 15
                
                // Check if the server is running
                sh '''
                if ! pgrep -f "manage.py runserver"; then
                    echo "Django server failed to start."
                    cat server.log
                    exit 1
                fi
                '''
                
                // Print logs to check for startup errors
                sh 'cat server.log'
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
