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
        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner'

                    withSonarQubeEnv('sonar-server') {
                        sh """
                            . .venv/bin/activate

                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=payflow \
                            -Dsonar.projectName=PayFlow \
                            -Dsonar.sources=app \
                            -Dsonar.tests=tests \
                            -Dsonar.python.version=3.13
                        """
                    }
                }
            }
        }
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }


        stage('OWASP Dependency Check') {
            steps {
                sh '''
                    mkdir -p reports/dependency-check

                    dependency-check.sh \
                    --project "PayFlow" \
                    --scan requirements.txt \
                    --scan requirements-dev.txt \
                    --format HTML \
                    --out reports/dependency-check
                '''
            }

            post {
                always {
                    archiveArtifacts artifacts: 'reports/dependency-check/**',
                                    allowEmptyArchive: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                    -t payflow-api:${BUILD_NUMBER} .
                '''
            }
        }


        stage('Trivy Image Scan') {
            steps {
                sh '''
                    trivy image \
                    --severity HIGH,CRITICAL \
                    --ignore-unfixed \
                    --exit-code 1 \
                    payflow-api:${BUILD_NUMBER}
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'rithuraj6-dockerhub',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin

                        docker tag \
                            payflow-api:${BUILD_NUMBER} \
                            ${DOCKER_USERNAME}/payflow-api:${BUILD_NUMBER}

                        docker push \
                            ${DOCKER_USERNAME}/payflow-api:${BUILD_NUMBER}

                        docker logout
                    '''
                }
            }
        }

        

        
    }
}