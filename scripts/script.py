import subprocess
import shutil
import sys

# Check if Docker is installed and available
docker_path = shutil.which("docker")
if not docker_path:
    print("Error: Docker is not installed or not found in PATH")
    sys.exit(1)

# Function to run a ZAP scan using Docker
def run_zap_scan(target_url):
    try:
        # Running ZAP scan inside Docker
        zap_command = [
            docker_path, "run", "--rm",
            "-v", "/var/lib/jenkins/workspace/PTAAS/reports:/zap/reports",
            "owasp/zap2docker-stable",
            "zap-baseline.py", "-t", target_url, "-r", "/zap/reports/report.html"
        ]
        print(f"Running command: {' '.join(zap_command)}")
        result = subprocess.run(zap_command, capture_output=True, text=True, check=True)
        
        print("ZAP Scan Completed. Report saved in /zap/reports")
        print(result.stdout)
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing ZAP scan: {e}")
    except FileNotFoundError:
        print("Error: Docker command not found. Ensure Docker is installed inside the container.")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py <target_url>")
        sys.exit(1)

    target_url = sys.argv[1]
    run_zap_scan(target_url)
