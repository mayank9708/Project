import sys
import time
from zapv2 import ZAPv2

def run_zap_scan(target_url):
    zap = ZAPv2()

    print(f"🛡️ Starting OWASP ZAP scan on: {target_url}")

    # Ensure the URL is correctly formatted
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        print("❌ ERROR: Invalid URL format. Use http:// or https://")
        sys.exit(1)

    # Open the URL
    zap.urlopen(target_url)
    time.sleep(2)

    # Passive scan
    print("🔍 Running passive scan...")
    while int(zap.pscan.records_to_scan) > 0:
        print(f"⏳ Pending records: {zap.pscan.records_to_scan}")
        time.sleep(2)

    # Save the report
    report_path = "/mnt/reports/zap_scan_report.html"
    print(f"📄 Saving report to: {report_path}")
    with open(report_path, "w") as report_file:
        report_file.write(zap.core.htmlreport())

    print("✅ OWASP ZAP scan completed!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ ERROR: Missing URL argument. Usage: python script.py <URL>")
        sys.exit(1)

    target_url = sys.argv[1]
    run_zap_scan(target_url)
