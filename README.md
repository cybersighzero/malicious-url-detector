# Malicious URL Detector

A rule-based cybersecurity tool that analyzes URLs and flags potentially malicious patterns using common threat indicators.

## Features
- Detects IP-based URLs
- Flags excessive subdomains
- Identifies suspicious TLDs
- Detects URL redirection tricks
- Resolves redirect chains and compares destinations
- Weighted scoring with risk levels (safe/suspicious/high risk)

---

## Setup
Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
```

---

## Usage
```bash
python detector.py
```

---

## Disclaimer
For education purposes only.

---

## After you finish
1. Test with multiple URLs  
2. Commit with:
```bash
git commit -m "Add rule-based malicious URL detection tool"
```

---


## Created By

**Pratima Narang**  
[@cybersighzero](https://github.com/cybersighzero)

Feedback or ideas? Drop an [issue](https://github.com/cybersighzero/WeakSauce/issues) or submit a pull request!
