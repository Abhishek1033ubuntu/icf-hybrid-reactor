# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0.0 | :x:                |

## Reporting Vulnerabilities or Numerical Anomalies

Because this repository contains scientific simulation software, security and integrity issues include:
1. **Numerical Divergence or Instability:** Unhandled NaN/Inf floating-point crashes in hydrodynamics or neutronics solvers.
2. **Data & Dependency Security:** Vulnerabilities in third-party Python dependencies (`NumPy`, `Numba`, `ReportLab`).
3. **Data Privacy:** Accidental exposure of private credentials, keys, or non-public personal data.

### How to Report
Please **do not** open public GitHub issues for security vulnerabilities. Instead, report them directly to the Project Lead:

* **Lead Investigator:** Abhishek Singh
* **Email:** `abhishek1033@gmail.com` | 'abhishek.singh.941491229013@proton.me'
* **Response Time:** Acknowledgment within 48 hours; resolution or mitigation within 14 days.
