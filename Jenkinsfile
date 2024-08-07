pipeline {
    agent any
    
    environment {
        SONAR_PROJECT_KEY = 'heeddata'
    }
    
    tools {
        sonarScanner 'SonarScanner'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'integration', 
                    credentialsId: '171313d1-2912-4653-bcaf-eb48b5954e4d', 
                    url: 'https://github.com/cloudtrio/optscale.git'
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(credentialsId: 'sonar-jenkins-cloudtrio') {
                    sh """
                    sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=${SONAR_HOST_URL}
                    """
                }
            }
        }
        
        stage('Download SonarQube Report') {
            steps {
                script {
                    def reportUrl = "${SONAR_HOST_URL}/api/issues/search?projectKeys=${SONAR_PROJECT_KEY}&resolved=false&format=csv"
                    
                    withCredentials([string(credentialsId: 'sonar-jenkins-cloudtrio', variable: 'SONAR_TOKEN')]) {
                        sh """
                        curl -o sonarqube_report.csv -H "Authorization: Bearer ${SONAR_TOKEN}" "${reportUrl}"
                        """
                    }
                    
                    archiveArtifacts artifacts: 'sonarqube_report.csv', allowEmptyArchive: true
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
