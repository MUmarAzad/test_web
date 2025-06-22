pipeline {
  agent any

  environment {
    PROJECT_NAME = "mern-store"
  }

  stages {
    stage('Clone Repository') {
      steps {
        dir('part2') {
          git branch: 'main', url: 'https://github.com/MUmarAzad/mern-ecommerce-1.git'
        }
        dir('tests') {
          git branch: 'main', url: 'https://github.com/MUmarAzad/test_web.git'  // Separate repo for tests
        }
      }
    }

    stage('Build and Deploy') {
      steps {
        dir('part2') {
          script {
            echo "🧹 Cleaning up previous containers..."
            sh 'docker-compose -p $PROJECT_NAME -f docker-compose.yml down -v --remove-orphans || true'
            sh 'docker rm -f $(docker ps -aq --filter name=client) || true'
            sh 'docker rm -f $(docker ps -aq --filter name=mongodb) || true'
            sh 'docker system prune -af || true'
            sh 'docker volume prune -f || true'

            echo "🚀 Building and deploying containers..."
            sh 'docker-compose -p $PROJECT_NAME -f docker-compose.yml up -d --build'
          }
        }
      }
    }

    stage('Run Selenium Tests') {
      steps {
        dir('tests') {
          script {
            echo '🔧 Building Selenium test container...'
            sh 'docker build -t selenium-tests .'

            echo '🚀 Running Selenium tests in container...'
            // Redirect output to log file
            def status = sh(script: 'docker run --rm selenium-tests > selenium_test_output.log 2>&1', returnStatus: true)

            // Show test log in Jenkins console
            sh 'echo "--- Selenium Test Log ---"'
            sh 'cat selenium_test_output.log'

            // Fail the build if tests failed
            if (status != 0) {
              error("❌ Selenium tests failed! Check selenium_test_output.log for details.")
            } else {
              echo '✅ Selenium tests completed successfully.'
            }
          }
        }
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: '**/selenium_test_output.log', allowEmptyArchive: true

      emailext(
        subject: "Jenkins Build: ${currentBuild.fullDisplayName}",
        body: "Build ${currentBuild.currentResult}: Check console output at ${env.BUILD_URL}",
        to: "umar.azad.work@gmail.com"
      )
    }
  }
}
