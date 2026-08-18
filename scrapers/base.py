from playwright.sync_api import sync_playwright


def render_and_extract(url, wait_selector, extract_fn):
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-blink-features=AutomationControlled"])
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page.on("response", lambda r: print("API:", r.status, r.url) if "halfclub.com" in r.url and ("/api" in r.url or r.url.endswith(".json")) else None)
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
