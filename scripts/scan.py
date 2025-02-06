import os
import sys
import subprocess

def run_nmap_scan(target_network):
    """Run an Nmap scan on the provided network and print the output."""
    print(f"Starting Nmap scan on network: {target_network}")
    
    # Build the Nmap command
    nmap_command = f"nmap -v -A {target_network}"
    
    try:
        # Run the command using subprocess and capture the output
        result = subprocess.run(nmap_command, shell=True, text=True, capture_output=True)
        
        # Check for errors
        if result.returncode != 0:
            print(f"Error executing Nmap scan: {result.stderr}")
        else:
            print("Scan results:\n")
            print(result.stdout)
    
    except Exception as e:
        print(f"An error occurred while running the scan: {e}")

def main():
    """Main function to get the network from the user and run the scan."""
    if len(sys.argv) < 2:
        print("Usage: python scan.py <network>")
        sys.exit(1)
    
    # Get the target network from the command-line argument
    target_network = sys.argv[1]
    
    # Run the scan
    run_nmap_scan(target_network)

if __name__ == "__main__":
    main()
