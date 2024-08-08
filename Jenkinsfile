node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scannerHome = tool 'SonarScanner';
    withSonarQubeEnv('Sonarqubeserver') {
      sh "${scannerHome}/bin/sonar-scanner"
    }
  }
}
