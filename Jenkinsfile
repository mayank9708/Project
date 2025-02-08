pipeline {
    agent any

    environment {
        NMAP_IMAGE = 'my-nmap-scanner'
        ZAP_IMAGE = 'my-zap-scanner'
        NMAP_NETWORK = '192.168.37.128' // Define the network to scan
        ZAP_URL = 'http://google.com' // Define the target URL for ZAP scan
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
                    def missingFiles = []
                    def requiredFiles = [
                        "Dockerfiles/Dockerfile-nmap",
                        "Dockerfiles/Dockerfile-zap",
                        "scripts/scan.py",
                        "scripts/script.py"
                    ]
                    
                    requiredFiles.each { file ->
                        if (!fileExists("$WORKSPACE/${file}")) {
                            missingFiles.add(file)
                        }
                    }

                    if (missingFiles.size() > 0) {
                        error "❌ ERROR: Missing files: ${missingFiles.join(', ')}"
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
                        ls -l $WORKSPACE/Dockerfiles/
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
                        docker run --rm -v $WORKSPACE/scripts:/mnt/scripts -v $WORKSPACE/reports:/mnt/reports ${NMAP_IMAGE} python3 /mnt/scripts/scan.py ${NMAP_NETWORK} | tee $WORKSPACE/reports/nmap_scan_report.txt
                    '''
                }
            }
        }

        stage('Run OWASP ZAP Scan') {
            steps {
                script {
                    echo "🛡️ Running OWASP ZAP scan..."
                    sh '''
                        docker run --rm -v $WORKSPACE/scripts:/mnt/scripts -v $WORKSPACE/reports:/mnt/reports ${ZAP_IMAGE} python3 /mnt/scripts/script.py ${ZAP_URL} | tee $WORKSPACE/reports/zap_scan_output.txt
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
