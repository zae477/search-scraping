from playwright.sync_api import sync_playwright


def render_and_extract(url, wait_selector, extract_fn):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page.goto(url, wait_until="networkidle")
        try:
            page.wait_for_selector(wait_selector)
        except Exception:
            html = page.content()
            print("URL:", page.url)
            print("horizontal-area count:", html.count("horizontal-area"))
            print("rank-list count:", html.count("rank-list"))
            idx = html.find("인기 검색어")
            print("인기 검색어 idx:", idx)
            if idx != -1:
                print("CONTEXT:", html[max(0, idx - 300):idx + 500])
            raise
        result = extract_fn(page)
        browser.close()
        return result
