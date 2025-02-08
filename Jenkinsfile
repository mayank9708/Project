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

        stage('Validate Dockerfiles and Scripts') {
            steps {
                script {
                    if (!fileExists("$WORKSPACE/Dockerfiles/Dockerfile-nmap")) {
                        error "❌ ERROR: Dockerfile-nmap is missing at $WORKSPACE/Dockerfiles/"
                    }
                    if (!fileExists("$WORKSPACE/Dockerfiles/Dockerfile-zap")) {
                        error "❌ ERROR: Dockerfile-zap is missing at $WORKSPACE/Dockerfiles/"
                    }
                    if (!fileExists("$WORKSPACE/scripts/scan.py")) {
                        error "❌ ERROR: scan.py is missing at $WORKSPACE/scripts/"
                    }
                    if (!fileExists("$WORKSPACE/scripts/script.py")) {
                        error "❌ ERROR: script.py is missing at $WORKSPACE/scripts/"
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo "⚙️ Building Docker images..."
                    sh '''
                        echo "Building Nmap image..."
                        docker build -t ${NMAP_IMAGE} -f $WORKSPACE/Dockerfiles/Dockerfile-nmap $WORKSPACE
                        
                        echo "Building ZAP image..."
                        docker build -t ${ZAP_IMAGE} -f $WORKSPACE/Dockerfiles/Dockerfile-zap $WORKSPACE
                    '''
                }
            }
        }

        stage('Run Nmap Scan') {
            steps {
                script {
                    echo "🔍 Running Nmap scan..."
                    sh '''
                        docker run --rm -v $WORKSPACE/scripts:/mnt/scripts -v $WORKSPACE/reports:/mnt/reports ${NMAP_IMAGE} python3 /mnt/scripts/scan.py ${NMAP_NETWORK} > $WORKSPACE/reports/nmap_scan_report.txt
                    '''
                }
            }
        }

        stage('Run OWASP ZAP Scan') {
            steps {
                script {
                    echo "🛡️ Running OWASP ZAP scan..."
                    
                    // Check if ZAP_URL is being correctly read
                    echo "ZAP_URL is: ${ZAP_URL}"

                    sh '''
                        docker run --rm -v $WORKSPACE/scripts:/mnt/scripts -v $WORKSPACE/reports:/mnt/reports ${ZAP_IMAGE} python3 /mnt/scripts/script.py "${ZAP_URL}"
                    '''
                    
                    sleep(time: 30, unit: 'SECONDS')

                    echo "📄 Copying ZAP scan report..."
                    sh '''
                        docker run --rm -v $WORKSPACE/reports:/mnt/reports ${ZAP_IMAGE} cp /usr/src/app/results.html /mnt/reports/zap_scan_report.html
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "✅ Pipeline execution completed!"
        }

        success {
            echo "🎉 The pipeline was successful!"
        }

        failure {
            echo "❌ The pipeline failed. Please check the logs."
        }
    }
}
