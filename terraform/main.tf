provider "local" {}

# Define the path to the Nmap scan report
variable "nmap_report" {
  description = "Path to the Nmap scan report"
  type        = string
}

# Define the path to the ZAP scan report
variable "zap_report" {
  description = "Path to the ZAP scan report"
  type        = string
}

# Resource to process the Nmap scan report
resource "null_resource" "nmap_vulnerability_check" {
  provisioner "local-exec" {
    command = "python3 parse_nmap_report.py ${var.nmap_report}"
  }
}

# Resource to process the ZAP scan report
resource "null_resource" "zap_vulnerability_check" {
  provisioner "local-exec" {
    command = "python3 parse_zap_report.py ${var.zap_report}"
  }
}

# Example of handling output
output "nmap_report_result" {
  value = null_resource.nmap_vulnerability_check.id
}

output "zap_report_result" {
  value = null_resource.zap_vulnerability_check.id
}
