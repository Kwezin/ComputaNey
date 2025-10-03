pipeline {
    agent any

    environment {
        VENV = 'venv'
    }

    stages {
        stage('Clonar repositório') {
            steps {
                git 'https://github.com/Kwezin/ComputaNey.git'
            }
        }

        stage('Criar ambiente virtual') {
            steps {
                sh 'python3 -m venv $VENV'
            }
        }

        stage('Instalar dependências') {
            steps {
                sh '. $VENV/bin/activate && pip install -r app/requirements.txt'
            }
        }

        stage('Executar testes') {
            steps {
                sh '. $VENV/bin/activate && python -m unittest app/tests/tests.py'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finalizada.'
        }
        success {
            echo 'Todos os testes passaram!'
        }
        failure {
            echo 'Algum teste falhou.'
        }
    }
}
