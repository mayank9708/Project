pipeline {
    agent any

    environment {
        NMAP_IMAGE = 'my-nmap-scanner'
        ZAP_IMAGE = 'my-zap-scanner'
        NMAP_NETWORK = '192.168.37.128' // Define the network to scan
        ZAP_URL = 'http://google.com' // Define the target URL for ZAP scan
        ANSIBLE_PLAYBOOK = 'security_config.yml' // Ansible playbook for security automation
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
                    // Check if Dockerfiles and Scripts exist
                    if (!fileExists("$WORKSPACE/Dockerfiles/Dockerfile-nmap")) {
                        error "ERROR: Dockerfile-nmap is missing at $WORKSPACE/Dockerfiles/"
                    }
                    if (!fileExists("$WORKSPACE/Dockerfiles/Dockerfile-zap")) {
                        error "ERROR: Dockerfile-zap is missing at $WORKSPACE/Dockerfiles/"
                    }
                    if (!fileExists("$WORKSPACE/scripts/scan.py")) {
                        error "ERROR: scan.py is missing at $WORKSPACE/scripts/"
                    }
                    if (!fileExists("$WORKSPACE/scripts/script.py")) {
                        error "ERROR: script.py is missing at $WORKSPACE/scripts/"
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Build the Docker images for Nmap and ZAP
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
                    // Run Nmap scan using the generated Docker image
                    sh '''
                        docker run --rm -v $WORKSPACE/scripts:/mnt/scripts -v $WORKSPACE/reports:/mnt/reports ${NMAP_IMAGE} python3 /mnt/scripts/scan.py ${NMAP_NETWORK} > $WORKSPACE/reports/nmap_scan_report.txt
                    '''
                }
            }
        }

        stage('Run OWASP ZAP Scan') {
            steps {
                script {
                    // Run ZAP scan using the generated Docker image
                    sh '''
                        docker run --rm -v $WORKSPACE/scripts:/mnt/scripts -v $WORKSPACE/reports:/mnt/reports ${ZAP_IMAGE} python3 /mnt/scripts/script.py ${ZAP_URL} > $WORKSPACE/reports/zap_scan_output.txt
                    '''
                    
                    sleep(time: 30, unit: 'SECONDS')

                    sh '''
                        docker run --rm -v $WORKSPACE/reports:/mnt/reports ${ZAP_IMAGE} cp /usr/src/app/results.html /mnt/reports/zap_scan_report.html
                    '''
                }
            }
        }

        stage('Run Terraform') {
            steps {
                script {
                    // Initialize Terraform and apply configuration
                    echo "Initializing Terraform..."
                    sh 'terraform init'

                    echo "Applying Terraform configuration..."
                    sh 'terraform apply -auto-approve'
                }
            }
        }

        stage('Run Ansible Playbook for Security Hardening') {
            steps {
                script {
                    sh '''
                        echo "Checking if Ansible is installed..."
                        if ! command -v ansible &> /dev/null
                        then
                            echo "Installing Ansible..."
                            sudo apt update && sudo apt install -y ansible
                        fi

                        echo "Running Ansible Playbook for security hardening..."
                        ansible-playbook -i hosts.ini $ANSIBLE_PLAYBOOK
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline execution completed!"
        }

        success {
            echo "The pipeline was successful!"

            emailext subject: "Security Scan & Hardening Completed Successfully",
                     body: """<p>The security scan and hardening process have been completed successfully.</p>
                              <p>Reports:</p>
                              <ul>
                                  <li><a href="${BUILD_URL}artifact/reports/nmap_scan_report.txt">Nmap Scan Report</a></li>
                                  <li><a href="${BUILD_URL}artifact/reports/zap_scan_report.html">ZAP Scan Report</a></li>
                              </ul>
                              <p>Security configurations have been applied automatically.</p>""",
                     to: 'redminote6pro12999@gmail.com',
                     mimeType: 'text/html'
        }

        failure {
            echo "The pipeline failed. Please check the logs."

            emailext subject: "Security Scan & Hardening Failed",
                     body: """<p>The security scan or hardening process has failed. Please check the Jenkins logs for details.</p>
                              <p>Jenkins Build: <a href="${BUILD_URL}">${BUILD_URL}</a></p>""",
                     to: 'security-team@example.com',
                     mimeType: 'text/html'
        }
    }
}
