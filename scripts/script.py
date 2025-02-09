import subprocess
import time
from zapv2 import ZAPv2

# Target URL for scanning
target_url = "http://example.com"
ZAP_PORT = "8080"
ZAP_API_URL = f"http://127.0.0.1:{ZAP_PORT}"

# Start OWASP ZAP in daemon mode
print("🛡️ Starting OWASP ZAP...")
zap_process = subprocess.Popen(
    ["zap.sh", "-daemon", "-port", ZAP_PORT],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

# Wait for ZAP to start
print("⏳ Waiting for ZAP to become ready...")
zap = ZAPv2()
while True:
    try:
        version = zap.core.version
        print(f"✅ ZAP is ready! Version: {version}")
        break
    except:
        time.sleep(5)

# Start Spider Scan
print(f"🕷️ Starting Spider Scan on {target_url}...")
scan_id = zap.spider.scan(target_url)
while int(zap.spider.status(scan_id)) < 100:
    print(f"⏳ Spider Scan progress: {zap.spider.status(scan_id)}%")
    time.sleep(5)
print("✅ Spider Scan completed!")

# Start Active Scan
print("🚀 Starting Active Scan...")
scan_id = zap.ascan.scan(target_url)
while int(zap.ascan.status(scan_id)) < 100:
    print(f"⏳ Active Scan progress: {zap.ascan.status(scan_id)}%")
    time.sleep(5)
print("✅ Active Scan completed!")

# Generate Report
print("📄 Generating ZAP Report...")
report = zap.core.htmlreport()
with open("zap_report.html", "w") as f:
    f.write(report)

print("✅ Scan completed! Report saved as zap_report.html")

# Stop OWASP ZAP
zap.core.shutdown()
print("🛑 OWASP ZAP stopped.")
