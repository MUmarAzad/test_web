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
            sh 'docker-compose -p $PROJECT_NAME -f docker-compose.yml down -v --remove-orphans || true'
            sh 'docker system prune -af || true'
            sh 'docker volume prune -f || true'
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
                sh 'docker run --rm selenium-tests || (echo "❌ Selenium tests failed!" && exit 1)'
                
                echo '✅ Selenium tests completed.'
            }
            }
        }
    }
  }

  post {
    always {
      emailext(
        subject: "Jenkins Build: ${currentBuild.fullDisplayName}",
        body: "Build ${currentBuild.currentResult}: Check console output at ${env.BUILD_URL}",
        to: "umar.azad.work@gmail.com"
      )
    }
  }
}
