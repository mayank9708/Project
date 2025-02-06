import subprocess
import os
import time

def start_zap_container(url):
    print("Starting OWASP ZAP container...")
    container = subprocess.run([
        'docker', 'run', '-d', '-p', '8080:8080', 'zaproxy/zap-stable', 
        'zap-baseline.py', '-t', url, '-r', '/zap/wrk/output/results.html', '-l', 'INFO'
    ], capture_output=True, text=True)
    
    if container.returncode == 0:
        print("OWASP ZAP container started.")
        container_id = container.stdout.strip()
        print(f"Container ID: {container_id}")
        
        # Wait for a bit to let the scan complete
        print("Starting scan for", url)
        time.sleep(10)  # Adjust the sleep time based on the scan duration

        # Copy the results to the local machine
        print("Fetching the results...")
        subprocess.run(['docker', 'cp', f'{container_id}:/zap/wrk/output/results.html', './results.html'])

        # Print out the result file path
        print("Scan completed. The results are saved in ./results.html.")
        
        # Optionally, open the results in the default web browser (Linux)
        try:
            subprocess.run(['xdg-open', 'results.html'])
        except Exception as e:
            print(f"Could not open the HTML report: {e}")
        
        # Stop the container
        print("Stopping OWASP ZAP container...")
        subprocess.run(['docker', 'stop', container_id])
        subprocess.run(['docker', 'rm', container_id])
    else:
        print("Error starting the ZAP container:", container.stderr)

def main():
    url = input("Enter the URL to scan: ")
    start_zap_container(url)

if __name__ == "__main__":
    main()

