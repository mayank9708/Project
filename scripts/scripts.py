import subprocess
import sys
import time

def start_zap_container(url):
    print(f"Starting OWASP ZAP scan for {url}...")

    container = subprocess.run([
        'docker', 'run', '-d', '-p', '8080:8080', 'zaproxy/zap-stable',
        'zap-baseline.py', '-t', url, '-r', '/zap/wrk/output/results.html', '-l', 'INFO'
    ], capture_output=True, text=True)

    if container.returncode == 0:
        container_id = container.stdout.strip()
        print(f"Container ID: {container_id}")

        # Wait for scan completion
        time.sleep(30)

        # Copy the report
        subprocess.run(['docker', 'cp', f'{container_id}:/zap/wrk/output/results.html', './zap_scan_report.html'])
        print("Scan completed. Report saved as zap_scan_report.html.")

        # Stop the container
        subprocess.run(['docker', 'stop', container_id])
        subprocess.run(['docker', 'rm', container_id])
    else:
        print("Error starting the ZAP container:", container.stderr)

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    start_zap_container(url)

if __name__ == "__main__":
    main()
