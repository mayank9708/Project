import os
import sys
import subprocess

def run_nmap_scan(target_network):
    """Run an Nmap scan on the provided network and print the output."""
    print(f"Starting Nmap scan on network: {target_network}")
    
    # Build the Nmap command
    nmap_command = ["nmap", "-v", "-A", target_network]  # Fixed to use list format

    try:
        # Run the command using subprocess
        result = subprocess.run(nmap_command, text=True, capture_output=True, check=True)
        print("Scan results:\n", result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error executing Nmap scan: {e.stderr}")

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
