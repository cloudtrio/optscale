node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scannerHome = tool 'Sonarqubeserver';
    withSonarQubeEnv('Sonarqubeserver') {
      sh "${scannerHome}/bin/sonar-scanner"
    }
  }
}
