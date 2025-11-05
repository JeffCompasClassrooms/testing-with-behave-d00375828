# features/environment.py
# Create a Chrome driver on context.browser.
# Try behave-webdriver first; if that import fails, fall back to plain Selenium.

def _make_driver():
    # Try behave-webdriver lazily (avoids import-time crashes)
    try:
        from behave_webdriver import webdriver as bwd
        return bwd.Chrome()
    except Exception:
        # Fallback: plain Selenium WebDriver
        from selenium import webdriver
        # Minimal, straightforward Chrome (assumes chromedriver on PATH)
        return webdriver.Chrome()

def before_all(context):
    context.browser = _make_driver()

def before_scenario(context, scenario):
    # Safety net if something closed the driver
    if not hasattr(context, "browser") or context.browser is None:
        context.browser = _make_driver()

def after_all(context):
    try:
        context.browser.quit()
    except Exception:
        pass
