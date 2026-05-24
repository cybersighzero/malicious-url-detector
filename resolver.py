from urllib.parse import urlparse

import requests
import urllib3
from requests.exceptions import (
    ConnectionError,
    InvalidURL,
    MissingSchema,
    RequestException,
    SSLError,
    Timeout,
    TooManyRedirects,
)

DEFAULT_TIMEOUT = 8
MAX_REDIRECTS = 10


def _normalize_url(url):
    url = url.strip()
    if not url:
        return url
    parsed = urlparse(url)
    if not parsed.scheme:
        return f"https://{url}"
    return url


def resolve_redirects(url):
    normalized_url = _normalize_url(url)
    if not normalized_url:
        return {"error": "Empty URL", "hops": [], "final_url": ""}

    with requests.Session() as session:
         session.max_redirects = MAX_REDIRECTS
         ssl_warning = ""
         verify = True

        while True:
                 try:
                     with session.get(
                         normalized_url,
                         allow_redirects=True,
                         timeout=DEFAULT_TIMEOUT,
                         verify=verify,
                     ) as response:
                         hops = [item.url for item in response.history]
                         hops.append(response.url)
                         
                         result = {"hops": hops, "final_url": response.url}
                         if ssl_warning:
                             result["warning"] = ssl_warning
                         return result
                 except SSLError:
                     if verify:
                         urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                         verify = False
                         ssl_warning = "SSL verification failed; proceeding without verification"
                         continue
                     return {"error": "SSL error", "hops": [], "final_url": ""}
                 except (MissingSchema, InvalidURL):
                     return {"error": "Invalid URL", "hops": [], "final_url": ""}
                 except Timeout:
                     return {"error": "Request timed out", "hops": [], "final_url": ""}
                 except TooManyRedirects:
                     return {
                         "error": f"Too many redirects (>{MAX_REDIRECTS})",
                         "hops": [],
                         "final_url": "",
                     }
                 except ConnectionError:
                     return {"error": "Connection error", "hops": [], "final_url": ""}
                 except RequestException as exc:
                     return {"error": f"Request failed: {exc}", "hops": [], "final_url": ""}
