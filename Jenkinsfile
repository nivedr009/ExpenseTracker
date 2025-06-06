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
                echo 'Building Docker Compose services...'
                bat 'docker-compose -p expensetracker build'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application using Docker Compose...'
                bat 'docker-compose -p expensetracker up -d'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'
                bat 'docker-compose -p expensetracker run --rm web pytest tests/ --maxfail=5 --disable-warnings --html=reports/test_report.html'
            }
        }
    }

    post {
        always {
            // Archive test report HTML file
            archiveArtifacts artifacts: 'reports/test_report.html', allowEmptyArchive: true
        }
    }
}
