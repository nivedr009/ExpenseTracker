pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-token', 
                    url: 'https://github.com/nivedr009/ExpenseTracker.git'
            }
        }

        stage('Build') {
            steps {
                echo "Building the project..."
                // Add build commands here (e.g., mvn package, npm install, etc.)
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
                echo "Deploying application..."
                // Add deployment commands here
            }
        }
    }
}
