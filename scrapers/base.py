from playwright.sync_api import sync_playwright


def render_and_extract(url, wait_selector, extract_fn):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page.goto(url, wait_until="domcontentloaded")
        try:
            page.wait_for_selector(wait_selector, timeout=20000)
        except Exception:
            html = page.content()
            print("BODY LEN:", len(html))
            print("rank-list count:", html.count("rank-list"))
            print("horizontal-area count:", html.count("horizontal-area"))
            print("BODY SNIPPET:", html[html.find("<body"):html.find("<body") + 2000])
            raise
        result = extract_fn(page)
        browser.close()
        return result
