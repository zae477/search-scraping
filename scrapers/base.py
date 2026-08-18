from playwright.sync_api import sync_playwright


def render_and_extract(url, wait_selector, extract_fn):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page.on("console", lambda m: print("CONSOLE:", m.type, m.text))
        page.on("requestfailed", lambda r: print("REQFAIL:", r.url, r.failure))
        page.on("response", lambda r: print("RESP:", r.status, r.url) if r.status >= 400 or "rank" in r.url.lower() or "keyword" in r.url.lower() else None)
        page.goto(url, wait_until="domcontentloaded")
        for _ in range(20):
            if page.locator(wait_selector).count() > 0:
                break
            page.mouse.wheel(0, 800)
            page.wait_for_timeout(300)
        page.wait_for_selector(wait_selector, timeout=5000)
        result = extract_fn(page)
        browser.close()
        return result
