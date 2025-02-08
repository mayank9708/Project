import sys
import time
from zapv2 import ZAPv2

# Ensure the script receives a URL argument
if len(sys.argv) < 2:
    print("❌ ERROR: Missing URL argument. Usage: python script.py <URL>")
    sys.exit(1)

# Read target URL from command line argument
target_url = sys.argv[1]
print(f"🛡️ Starting OWASP ZAP scan on: {target_url}")

# Initialize ZAP API client
zap = ZAPv2()

# Open the target URL
print(f"📡 Accessing {target_url} via ZAP proxy...")
zap.urlopen(target_url)
time.sleep(2)

# Start active scan
print(f"🚀 Starting Active Scan on {target_url}...")
scan_id = zap.ascan.scan(target_url)
while int(zap.ascan.status(scan_id)) < 100:
    print(f"⏳ Scan progress: {zap.ascan.status(scan_id)}%")
    time.sleep(5)

print("✅ Scan completed!")

# Save the report
with open("/usr/src/app/results.html", "w") as report_file:
    report_file.write(zap.core.htmlreport())

print("📄 Report saved as results.html")
