import sys
import time
from zapv2 import ZAPv2

def run_zap_scan(target_url):
    zap = ZAPv2()

    print(f"🛡️ Starting OWASP ZAP scan on: {target_url}")

    # Open the URL
    zap.urlopen(target_url)
    time.sleep(2)  # Wait for ZAP to process

    # Passive scan
    print("🔍 Running passive scan...")
    while int(zap.pscan.records_to_scan) > 0:
        print(f"⏳ Pending records: {zap.pscan.records_to_scan}")
        time.sleep(2)

    # Save the report inside the mounted reports directory
    report_path = "/mnt/reports/zap_scan_report.html"
    print(f"📄 Saving report to: {report_path}")
    with open(report_path, "w") as report_file:
        report_file.write(zap.core.htmlreport())

    print("✅ OWASP ZAP scan completed!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ ERROR: No URL provided. Usage: python script.py <URL>")
        sys.exit(1)

    target_url = sys.argv[1]
    run_zap_scan(target_url)
