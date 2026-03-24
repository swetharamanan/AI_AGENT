from playwright.sync_api import sync_playwright


def start_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    context = browser.new_context(
    permissions=["geolocation"]
    )
    return page, browser, p