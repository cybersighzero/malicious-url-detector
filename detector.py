from urllib.parse import urlparse

from resolver import resolve_redirects
from rules import analyze_url, risk_from_score, score_from_reasons


def _print_result(label, result):
    print(f"\n{label}")
    print(f"Score: {result['score']} | Risk: {result['risk']}")
    if result["reasons"]:
        print("Reasons:")
        for reason in result["reasons"]:
            print(f"- {reason}")
    else:
        print("Reasons: none")


def _merge_reasons(*reason_lists):
    merged = []
    seen = set()
    for reasons in reason_lists:
        for reason in reasons:
            if reason not in seen:
                seen.add(reason)
                merged.append(reason)
    return merged

def main():
    url = input("Enter URL to analyze: ").strip()
    parsed_input = urlparse(url)
    normalized_url = url if parsed_input.scheme else f"https://{url}"

    redirect_result = resolve_redirects(normalized_url)
    if "error" in redirect_result:
        print(f"Redirect resolution failed: {redirect_result['error']}")
        return

    if "warning" in redirect_result:
        print(f"Warning: {redirect_result['warning']}")

    hops = redirect_result.get("hops", [])
    final_url = redirect_result.get("final_url", normalized_url)

    if len(hops) > 1:
        print("\nRedirect chain:")
        for index, hop in enumerate(hops, start=1):
            print(f"{index}. {hop}")
    else:
        print("No redirects found")

    input_host = urlparse(normalized_url).hostname or ""
    final_host = urlparse(final_url).hostname or ""
    if input_host and final_host and input_host.lower() != final_host.lower():
        print("Destination differs from input")

    original_result = analyze_url(normalized_url)

    if len(hops) > 1:
        final_result = analyze_url(final_url)
        combined_reasons = _merge_reasons(
            original_result["reasons"],
            final_result["reasons"],
        )
        combined_score = score_from_reasons(combined_reasons)
        combined_result = {
            "score": combined_score,
            "risk": risk_from_score(combined_score),
            "reasons": combined_reasons,
        }
        _print_result("URL analysis", combined_result)
    else:
        _print_result("URL analysis", original_result)

if __name__ == "__main__":
    main()
