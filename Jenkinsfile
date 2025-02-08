pipeline {
    agent any

    environment {
        NMAP_IMAGE = 'my-nmap-scanner'
        ZAP_IMAGE = 'my-zap-scanner'
        NMAP_NETWORK = '192.168.1.1' // Define the network you want to scan
        ZAP_URL = 'http://example.com' // Define the URL for ZAP scan
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                sh 'mkdir -p reports'
            }
        }

        stage('Check Workspace') {
            steps {
                sh 'pwd && ls -R'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo "Building Docker images..."
                    sh 'docker build -t ${NMAP_IMAGE} -f $WORKSPACE/Dockerfiles/Dockerfile-nmap $WORKSPACE'
                    sh 'docker build -t ${ZAP_IMAGE} -f $WORKSPACE/Dockerfiles/Dockerfile-zap $WORKSPACE'
                }
            }
        }

        stage('Run Nmap Scan') {
            steps {
                script {
                    echo "Running Nmap scan..."
                    sh 'docker run --rm -v $WORKSPACE/scripts:/scripts ${NMAP_IMAGE} python3 /scripts/scan.py ${NMAP_NETWORK} > $WORKSPACE/reports/nmap_scan_report.txt'
                }
            }
        }

        stage('Run OWASP ZAP Scan') {
            steps {
                script {
                    echo "Running OWASP ZAP scan..."
                    sh 'docker run --rm -v $WORKSPACE/scripts:/scripts ${ZAP_IMAGE} python3 /scripts/script.py ${ZAP_URL}'

                    sleep(time: 30, unit: 'SECONDS')

                    sh 'docker ps -q --filter "ancestor=${ZAP_IMAGE}" | xargs -I {} docker cp {}:/usr/src/app/results.html $WORKSPACE/reports/zap_scan_report.html'
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished!"
        }

        success {
            echo "The pipeline was successful!"
        }

        failure {
            echo "The pipeline failed. Check the logs."
        }
    }
}
