stage('Build Docker Images') {
    steps {
        script {
            echo "Building Docker images..."
            sh 'docker build -t my-nmap-scanner -f Dockerfiles/Dockerfile-nmap .'
            sh 'docker build -t my-zap-scanner -f Dockerfiles/Dockerfile-zap .'
        }
    }
}
stage('Run Nmap Scan') {
    steps {
        script {
            echo "Running Nmap scan..."
            sh 'docker run --rm -v $PWD/scripts:/scripts my-nmap-scanner python3 /scripts/run_nmap_scan.py 192.168.1.1 > reports/nmap_scan_report.txt'
        }
    }
}

stage('Run OWASP ZAP Scan') {
    steps {
        script {
            echo "Running OWASP ZAP scan..."
            sh 'docker run --rm -v $PWD/scripts:/scripts my-zap-scanner python3 /scripts/run_zap_scan.py http://example.com'
            
            // Wait for scan completion
            sleep(time: 30, unit: "SECONDS")

            // Copy the ZAP scan report from the container
            sh 'docker ps -q --filter "ancestor=my-zap-scanner" | xargs -I {} docker cp {}:/usr/src/app/zap_scan_report.html reports/zap_scan_report.html'
        }
    }
}
