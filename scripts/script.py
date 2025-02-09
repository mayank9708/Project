import sys
import time
from zapv2 import ZAPv2

# Extract the last argument as the URL (ignoring extra args)
target_url = sys.argv[-1].strip()

# Validate the URL format
if not target_url.startswith(("http://", "https://")):
    print(f"❌ ERROR: Invalid URL '{target_url}'. Ensure it starts with 'http://' or 'https://'.")
    sys.exit(1)

print(f"🛡️ Starting OWASP ZAP scan on: {target_url}")

# Initialize ZAP API client
zap = ZAPv2(proxies={'http': 'http://localhost:8080', 'https': 'http://localhost:8080'})

# Open the target URL
print(f"📡 Accessing {target_url} via ZAP proxy...")
zap.urlopen(target_url)
time.sleep(2)  # Allow time for the request to process

# Start active scan
print(f"🚀 Starting Active Scan on {target_url}...")
scan_id = zap.ascan.scan(target_url)

if scan_id.isdigit():
    while int(zap.ascan.status(scan_id)) < 100:
        print(f"⏳ Scan progress: {zap.ascan.status(scan_id)}%")
        time.sleep(5)
else:
    print("❌ ERROR: Failed to start ZAP scan.")
    sys.exit(1)

print("✅ Scan completed!")

# Save the report
with open("/usr/src/app/results.html", "w") as report_file:
    report_file.write(zap.core.htmlreport())

print("📄 Report saved as results.html")
