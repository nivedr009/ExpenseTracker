pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/YOUR_GITHUB_USERNAME/ExpenseTracker.git'
            }
        }

        stage('Build') {
            steps {
                sh 'echo "Building the Expense Tracker App..."'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'echo "Running Tests (No tests yet, skipping...)"'
            }
        }

        stage('Deploy') {
            steps {
                sh 'echo "Deployment - Will be configured later"'
            }
        }
    }
}
