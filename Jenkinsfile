node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scannerHome = tool 'sonarqubeserver'
    withSonarQubeEnv('Sonarqubeserver') {
      sh "${scannerHome}/bin/sonar-scanner"
    }
  }
}
