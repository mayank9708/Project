import sys
import time
from zapv2 import ZAPv2

# Debug: Print received arguments
print(f"🔍 Received arguments: {sys.argv}")

# Ensure exactly one argument is passed
if len(sys.argv) != 2:
    print(f"❌ ERROR: Expected 1 argument, got {len(sys.argv)-1}. Usage: python script.py <URL>")
    sys.exit(1)

# Read and validate the target URL
target_url = sys.argv[1].strip()
if not target_url.startswith(("http://", "https://")):
    print(f"❌ ERROR: Invalid URL '{target_url}'. Ensure it starts with 'http://' or 'https://'.")
    sys.exit(1)

print(f"🛡️ Running OWASP ZAP scan on: {target_url}")

# Initialize ZAP API client (Without Proxy)
zap = ZAPv2()

# Spider the target URL
print(f"🕷️ Starting Spider Scan on {target_url}...")
scan_id = zap.spider.scan(target_url)

while int(zap.spider.status(scan_id)) < 100:
    print(f"⏳ Spider progress: {zap.spider.status(scan_id)}%")
    time.sleep(5)

print("✅ Spider Scan completed!")

# Start active scan
print(f"🚀 Starting Active Scan on {target_url}...")
scan_id = zap.ascan.scan(target_url)

while int(zap.ascan.status(scan_id)) < 100:
    print(f"⏳ Scan progress: {zap.ascan.status(scan_id)}%")
    time.sleep(5)

print("✅ Active Scan completed!")

# Save the scan report
report_path = "/mnt/reports/results.html"
with open(report_path, "w") as report_file:
    report_file.write(zap.core.htmlreport())

print(f"📄 Report saved at {report_path}")
