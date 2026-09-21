pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    docker run -d \
                    --name payflow-test-redis \
                    --network devops-net \
                    redis:7-alpine

                    sleep 3

                    . .venv/bin/activate

                    DATABASE_URL=sqlite:// \
                    REDIS_URL=redis://payflow-test-redis:6379/0 \
                    pytest
                '''
            }

            post {
                always {
                    sh '''
                        docker rm -f payflow-test-redis || true
                    '''
                }
            }
        }
    }
}