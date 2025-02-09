
pipeline {
    agent any

    environment {
        NMAP_IMAGE = 'my-nmap-scanner'
        ZAP_IMAGE = 'my-zap-scanner'
        NMAP_NETWORK = '192.168.1.1/24'  // Fixed: Correct CIDR notation
        ZAP_URL = 'http://example.com'   // Change this dynamically if needed
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
                        error "❌ ERROR: Dockerfile-nmap is missing!"
                    }
                    if (!fileExists("$WORKSPACE/Dockerfiles/Dockerfile-zap")) {
                        error "❌ ERROR: Dockerfile-zap is missing!"
                    }
                    if (!fileExists("$WORKSPACE/scripts/scan.py")) {
                        error "❌ ERROR: scan.py is missing!"
                    }
                    if (!fileExists("$WORKSPACE/scripts/script.py")) {
                        error "❌ ERROR: script.py is missing!"
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
                        docker run --rm \
                        -v $WORKSPACE/scripts:/mnt/scripts \
                        -v $WORKSPACE/reports:/mnt/reports \
                        ${NMAP_IMAGE} python3 /mnt/scripts/scan.py ${NMAP_NETWORK} \
                        > $WORKSPACE/reports/nmap_scan_report.txt
                    '''
                }
            }
        }

        stage('Run OWASP ZAP Scan') {
            steps {
                script {
                    echo "🛡️ Running OWASP ZAP scan..."
                    
                    // Debugging: Print the URL before using it
                    echo "ZAP_URL is: ${ZAP_URL}"

                   sh '''
                   docker run --rm \
                   -v /var/lib/jenkins/workspace/PTAAS/scripts:/mnt/scripts \
                   -v /var/lib/jenkins/workspace/PTAAS/reports:/mnt/reports \
                   my-zap-scanner "${ZAP_URL}"
                   '''
             

                    echo "📄 Copying ZAP scan report..."
                    sh '''
                        docker cp $(docker create --rm ${ZAP_IMAGE}):/usr/src/app/results.html $WORKSPACE/reports/zap_scan_report.html
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
