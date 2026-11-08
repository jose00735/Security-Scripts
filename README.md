# security-scripts

Small tools and lab builds from my offensive-security and Fortinet study between August 2023 and May 2024, while preparing for OSCP, PNPT, CRTP and CRTE and working as a FortiGate support engineer.

They are study and lab tools, published as written with light clean-up: hard-coded lab URLs and session tokens removed, help text fixed, and one unfinished mode completed. Nothing here contains exam material, lab flags, credentials or customer data.

**Use them only against systems you own or are explicitly authorised to test.**

## Contents

| Path | What it does |
|---|---|
| `web/blind-sqli/blind_sqli_conditional_response.py` | Boolean-based blind SQL injection. Extracts a password character by character by checking for a "true" marker in the response. |
| `web/blind-sqli/blind_sqli_conditional_error.py` | Error-based blind SQLi. Forces a divide-by-zero in a `CASE` expression to learn the password length, then each character. |
| `web/blind-sqli/blind_sqli_timer.py` | Time-based blind SQLi on PostgreSQL (`pg_sleep`). It can resume from a given position when the target is slow. |
| `recon/nmapx.sh` | Two-stage nmap wrapper. A full TCP sweep saves grepable output, then `-sCV` runs only on the open ports it found. |
| `linux/ps_eye.sh` | Process-diff monitor for privilege escalation. Prints every new command line that appears (cron jobs, scripts run by other users) without needing root. |
| `ftp/ftp_downloader.py` | FTP load generator. Downloads one file over N parallel sessions to push traffic through a firewall under test. |
| `fortinet/policy-sync/sync_fortigate.sh` | Compares the firewall policies of two FortiGate configurations by policy ID and checksum. Prints a `config firewall policy` CLI block with only the policies that differ, without their UUIDs, ready to paste into the other unit. |
| `fortinet/ssl-inbound-inspection-lab/` | Lab for FortiGate inbound SSL inspection (server-certificate protection). It has a private CA, a CSR with SANs, and an nginx HTTPS server in Docker that presents the CA-signed certificate. |
| `fortinet/gui-certificate-lab/` | OpenSSL-in-Docker environment for issuing a FortiGate admin GUI certificate from a private CA, with IP SANs for each management interface. |

## Notes

- The SQLi scripts were written against the PortSwigger Web Security Academy blind SQL injection labs. They depend on `pwntools` and `requests`.
- The lab folders hold configuration only. Generate your own keys and certificates. No private keys are included.
- The policy-sync script expects two files listing `<policy-id>: <checksum>` and the full config the policies are taken from. Run it on configurations you are authorised to handle.

## Author

Jose Acosta Hernandez: OSCP, CRTE, CRTP, PNPT, NSE 7, CCNA.
[LinkedIn](https://www.linkedin.com/in/jose-acosta-hernandez)
