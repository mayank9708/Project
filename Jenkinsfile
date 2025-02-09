pipeline {
    agent any

    environment {
        ZAP_URL = "http://example.com"  // Replace with your target URL
        TARGET_NETWORK = "192.168.1.1/24" // Replace with your network target
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "📥 Checking out code from Git..."
                checkout scm
                sh 'mkdir -p reports'
            }
        }

        stage('Validate Dockerfiles and Scripts') {
            steps {
                script {
                    def files = ['Dockerfiles/Dockerfile-nmap', 'Dockerfiles/Dockerfile-zap', 'scripts/scan.py', 'scripts/script.py']
                    files.each { file ->
                        if (!fileExists(file)) {
                            error "🚨 ERROR: ${file} is missing!"
                        }
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo "⚙️ Building Docker images..."

                    // Build Nmap Image
                    sh '''
                    echo "Building Nmap image..."
                    docker build -t my-nmap-scanner -f Dockerfiles/Dockerfile-nmap .
                    '''

                    // Build OWASP ZAP Image
                    sh '''
                    echo "Building ZAP image..."
                    docker build -t my-zap-scanner -f Dockerfiles/Dockerfile-zap .
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
                    my-nmap-scanner python3 /mnt/scripts/scan.py $TARGET_NETWORK
                    '''
                }
            }
        }

        stage('Run OWASP ZAP') {
            steps {
                script {
                    echo "🛡️ Starting OWASP ZAP in background..."
                    sh '''
                    docker run -d --name zap-scanner \
                    -p 8080:8080 \
                    -v $WORKSPACE/reports:/mnt/reports \
                    my-zap-scanner -daemon -port 8080
                    '''
                }
            }
        }

        stage('Run Python Script for ZAP') {
            steps {
                script {
                    echo "🚀 Running ZAP script..."
                    sh '''
                    docker exec zap-scanner python3 /usr/src/app/script.py $ZAP_URL
                    '''
                }
            }
        }

        stage('Stop OWASP ZAP') {
            steps {
                script {
                    echo "🛑 Stopping and cleaning up OWASP ZAP..."
                    sh '''
                    docker stop zap-scanner
                    docker rm zap-scanner
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "📄 Archiving reports..."
            archiveArtifacts artifacts: 'reports/*', fingerprint: true
        }
        success {
            echo "✅ Scan completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs for details."
        }
    }
}
