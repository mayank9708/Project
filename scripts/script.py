import requests

ZAP_URL = "http://localhost:8080"
TARGET_URL = "http://example.com"  # Change this to your target

# Start scan
requests.get(f"{ZAP_URL}/JSON/spider/action/scan/", params={"url": TARGET_URL})

# Get report
report = requests.get(f"{ZAP_URL}/OTHER/core/other/htmlreport/").text

# Save report
with open("zap_report.html", "w", encoding="utf-8") as f:
    f.write(report)

print("[+] Scan complete! Report saved as zap_report.html")
