from playwright.sync_api import sync_playwright


def render_and_extract(url, wait_selector, extract_fn):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_selector(wait_selector)
        result = extract_fn(page)
        browser.close()
        return result
