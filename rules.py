from urllib.parse import urlparse
import re

SUSPICIOUS_TLDS = [".ru", ".tk", ".cn", ".xyz"]
MAX_URL_LENGTH = 75
MAX_SUBDOMAINS = 3
SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "secure",
    "update",
    "account",
    "bank",
    "confirm",
    "password",
    "signin",
    "webscr",
]

WEIGHTS = {
    "IP address as domain": 40,
    "Suspicious TLD": 30,
    "@ symbol": 30,
    "Keyword in domain": 25,
    "Excessive subdomains": 15,
    "Hyphen in domain": 10,
    "High digit ratio in domain": 20,
    "Long URL": 10,
}


def risk_from_score(score):
    if score < 30:
        return "safe"
    if score < 60:
        return "suspicious"
    return "high risk"


def score_from_reasons(reasons):
    return sum(WEIGHTS.get(reason, 0) for reason in reasons)


def analyze_url(url):
    reasons = []
    score = 0

    parsed = urlparse(url)
    host = parsed.hostname or ""

    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host):
        reasons.append("IP address as domain")
        score += WEIGHTS["IP address as domain"]

    if len(url) > MAX_URL_LENGTH:
        reasons.append("Long URL")
        score += WEIGHTS["Long URL"]

    domain_parts = host.split(".") if host else []
    if host and len(domain_parts) - 2 > MAX_SUBDOMAINS:
        reasons.append("Excessive subdomains")
        score += WEIGHTS["Excessive subdomains"]

    for tld in SUSPICIOUS_TLDS:
        if host.endswith(tld):
            reasons.append("Suspicious TLD")
            score += WEIGHTS["Suspicious TLD"]
            break

    if "@" in url:
        reasons.append("@ symbol")
        score += WEIGHTS["@ symbol"]

    if host:
        base_domain = host.rsplit(".", 1)[0]
    else:
        base_domain = ""
    lower_domain = base_domain.lower()
    if any(keyword in lower_domain for keyword in SUSPICIOUS_KEYWORDS):
        reasons.append("Keyword in domain")
        score += WEIGHTS["Keyword in domain"]

    if "-" in host:
        reasons.append("Hyphen in domain")
        score += WEIGHTS["Hyphen in domain"]

    if host:
        compact = host.replace(".", "")
        digit_count = sum(1 for ch in compact if ch.isdigit())
        if compact and (digit_count / len(compact)) > 0.3:
            reasons.append("High digit ratio in domain")
            score += WEIGHTS["High digit ratio in domain"]

    return {
        "score": score,
        "risk": risk_from_score(score),
        "reasons": reasons,
    }
