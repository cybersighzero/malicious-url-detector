# Malicious URL Detector

A rule-based cybersecurity tool that analyzes URLs and flags potentially malicious patterns using common threat indicators and redirect analysis.

---

## Features

- Detects IP-based URLs
- Flags excessive subdomains
- Identifies suspicious TLDs
- Detects URL redirection tricks
- Resolves redirect chains
- Weighted risk scoring system
- Risk classification:
  - Safe
  - Suspicious
  - High Risk

---

## Setup

Create and activate a virtual environment, then install dependencies.

### Create Virtual Environment

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

Install Dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage
Run the Detector:
```bash
python detector.py
```
Then enter a URL when prompted.

---

## Example Risk Levels

| Score | Risk Level |
|---|---|
| 0–29 | Safe |
| 30–59 | Suspicious |
| 60+ | High Risk |

---

## Disclaimer
For education purposes only.

---

## Created By

**Pratima Narang**  
[@cybersighzero](https://github.com/cybersighzero)

Feedback or ideas? Drop an [issue](https://github.com/cybersighzero/WeakSauce/issues) or submit a pull request!
