pipeline {
    agent any

    environment {
        NMAP_IMAGE = 'my-nmap-scanner'
        ZAP_IMAGE = 'my-zap-scanner'
        NMAP_NETWORK = '192.168.1.1' // Define the network to scan
        ZAP_URL = 'http://example.com' // Define the target URL for ZAP scan
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

        stage('Validate Dockerfiles') {
            steps {
                script {
                    if (!fileExists("$WORKSPACE/Dockerfiles/Dockerfile-nmap")) {
                        error "Dockerfile-nmap is missing in $WORKSPACE/Dockerfiles"
                    }
                    if (!fileExists("$WORKSPACE/Dockerfiles/Dockerfile-zap")) {
                        error "Dockerfile-zap is missing in $WORKSPACE/Dockerfiles"
                    }
                }
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
                    sh '''
                        docker run --rm -v $WORKSPACE:/mnt ${NMAP_IMAGE} python3 /mnt/scripts/scan.py ${NMAP_NETWORK} > $WORKSPACE/reports/nmap_scan_report.txt
                    '''
                }
            }
        }

        stage('Run OWASP ZAP Scan') {
            steps {
                script {
                    echo "Running OWASP ZAP scan..."
                    sh '''
                        docker run --rm -v $WORKSPACE:/mnt ${ZAP_IMAGE} python3 /mnt/scripts/script.py ${ZAP_URL}
                    '''
                    
                    sleep(time: 30, unit: 'SECONDS')

                    echo "Copying ZAP scan report..."
                    sh '''
                        docker run --rm -v $WORKSPACE/reports:/mnt/reports ${ZAP_IMAGE} cp /usr/src/app/results.html /mnt/reports/zap_scan_report.html
                    '''
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
