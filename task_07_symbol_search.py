import argparse
import ssl
import urllib.parse
import urllib.request


_ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query/"


def search_symbols(keywords, apikey="demo"):
    """Search Alpha Vantage symbols and return the raw CSV response."""
    query = urllib.parse.urlencode({
        "function": "SYMBOL_SEARCH",
        "keywords": keywords,
        "datatype": "csv",
        "apikey": apikey,
    })
    url = _ALPHA_VANTAGE_URL + "?" + query

    context = ssl.create_default_context()
    with urllib.request.urlopen(url, timeout=10, context=context) as response:
        return response.read().decode("utf-8", errors="ignore")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Search Alpha Vantage symbols and print the raw CSV result."
    )
    parser.add_argument("keywords", help="Search text, for example RWE, IBM, NVIDIA or Apple")
    parser.add_argument("-k", "--apikey", default="demo", help="Alpha Vantage API key")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = search_symbols(args.keywords, args.apikey)
    except Exception as exc:
        print(f"Fehler beim Abrufen der Symbole: {exc}")
        return 1

    print(result, end="" if result.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
