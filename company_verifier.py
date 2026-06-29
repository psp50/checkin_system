"""
company_verifier.py
Verifies whether a given company name is related to the denim/textile
industry by doing a LIVE web lookup (no API key needed) and checking
the result snippets for relevant industry keywords.

Used by app.py for the "Verify Exhibitor/Visitor Company" feature.
"""

import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://html.duckduckgo.com/html/"

# Keywords that indicate a company is connected to the denim / textile /
# apparel supply chain. Checked against the live search result snippets.
DENIM_KEYWORDS = [
    "denim", "jeans", "jean", "textile", "fabric", "garment",
    "apparel", "clothing", "fashion brand", "fashion retailer",
    "spinning mill", "weaving", "yarn", "cotton mill",
    "sourcing", "buying house", "dyeing", "washing plant",
    "indigo dye", "trims", "manufacturer of clothing",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
    )
}


def fetch_search_snippets(query: str, timeout: int = 6) -> dict:
    """
    Runs a live web search for the query and returns the result snippets
    plus a flag for whether any real results came back at all.
    """
    try:
        resp = requests.post(
            SEARCH_URL,
            data={"q": query},
            headers=HEADERS,
            timeout=timeout,
        )
        resp.raise_for_status()
    except requests.RequestException:
        return {"text": "", "result_count": 0}

    soup = BeautifulSoup(resp.text, "html.parser")
    snippet_tags = soup.select(".result__snippet")
    title_tags = soup.select(".result__a")

    snippet_text = " ".join(s.get_text(" ", strip=True) for s in snippet_tags)
    title_text = " ".join(t.get_text(" ", strip=True) for t in title_tags)

    return {
        "text": (snippet_text + " " + title_text).strip(),
        "result_count": len(snippet_tags),
    }


def verify_company_denim_relation(company_name: str) -> dict:
    """
    Looks up a company name live and decides whether it's denim/textile
    industry related.

    IMPORTANT: the search query intentionally does NOT contain words like
    "denim" or "textile" — only the company name itself plus a neutral
    qualifier. If we searched for "{company} denim textile", a page with
    zero real results (or an unrelated page that merely echoes the query
    text) could falsely "match" on words we ourselves typed. Keeping the
    query neutral means a match only happens if the company's *own*
    real-world description mentions the industry.

    Returns a dict:
      {
        "accepted": bool,
        "company_name": str,
        "matched_keywords": [...],
        "snippet": "...",      # short excerpt used for the decision
        "lookup_failed": bool  # True if the live search itself failed
      }
    """
    company_name = company_name.strip()
    query = f'"{company_name}" company profile business'
    search_result = fetch_search_snippets(query)

    # Treat "no real results" the same as "lookup failed" -- we can't make
    # a confident decision either way, so we don't grant access.
    if search_result["result_count"] == 0 or not search_result["text"]:
        return {
            "accepted": False,
            "company_name": company_name,
            "matched_keywords": [],
            "snippet": "",
            "lookup_failed": True,
        }

    lowered = search_result["text"].lower()
    matched = [kw for kw in DENIM_KEYWORDS if kw in lowered]

    return {
        "accepted": bool(matched),
        "company_name": company_name,
        "matched_keywords": matched,
        "snippet": search_result["text"][:300],
        "lookup_failed": False,
    }
