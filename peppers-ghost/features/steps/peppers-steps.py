# features/steps/peppers-steps.py
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

URL = "https://www.instructables.com/Peppers-Ghost-Illusion-in-a-Small-Space/"

# -------------------------
# Navigation / setup
# -------------------------
@given("I open the Pepper's Ghost tutorial")
def step_open_page(context):
    context.browser.get(URL)
    WebDriverWait(context.browser, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

@given("I dismiss any consent banner if asked")
def step_dismiss_consent(context):
    # Try common consent/notice buttons; ignore if not present.
    driver = context.browser
    try:
        # Look for buttons with typical consent text
        candidates = driver.find_elements(By.XPATH,
            "//button[normalize-space()[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'accept')"
            " or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'agree')"
            " or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'consent')]]"
        )
        if candidates:
            try:
                candidates[0].click()
            except Exception:
                pass
    except Exception:
        pass

# -------------------------
# Identity & structure
# -------------------------
@then('the page title should mention "{text}"')
def step_title_contains(context, text):
    WebDriverWait(context.browser, 20).until(lambda d: d.title is not None)
    assert text.lower() in context.browser.title.lower()

@then('the main heading should mention "{text}"')
def step_h1_contains(context, text):
    h1 = WebDriverWait(context.browser, 20).until(
        EC.visibility_of_element_located((By.TAG_NAME, "h1"))
    )
    assert text.lower() in h1.text.lower()

@then('the current URL should start with "{prefix}"')
def step_url_prefix(context, prefix):
    assert context.browser.current_url.startswith(prefix)

@then("the page body should be visible")
def step_body_visible(context):
    WebDriverWait(context.browser, 20).until(
        EC.visibility_of_element_located((By.TAG_NAME, "body"))
    )

@then('I should see the word "{word}" somewhere on the page')
def step_word_in_source(context, word):
    WebDriverWait(context.browser, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    source = context.browser.page_source
    assert word.lower() in source.lower()

# -------------------------
# Images & media
# -------------------------
@then('I should see at least {n:d} images on the page')
def step_at_least_n_images(context, n):
    imgs = WebDriverWait(context.browser, 20).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
    )
    assert len(imgs) >= n

@then("at least 1 image should have a non-empty src")
def step_image_has_src(context):
    imgs = context.browser.find_elements(By.TAG_NAME, "img")
    assert any((img.get_attribute("src") or "").strip() for img in imgs)

# -------------------------
# Lists / links
# -------------------------
@then('I should see at least {n:d} list items on the page')
def step_at_least_n_listitems(context, n):
    items = context.browser.find_elements(By.TAG_NAME, "li")
    assert len(items) >= n

@then('I should see at least {n:d} external links on the page')
def step_at_least_n_external_links(context, n):
    links = context.browser.find_elements(By.XPATH, "//a[starts-with(@href, 'http')]")
    assert len(links) >= n

# -------------------------
# Scrolling & resilience
# -------------------------
@when('I scroll down the page by {pixels:d} pixels')
def step_scroll_by(context, pixels):
    context.browser.execute_script(f"window.scrollBy(0, {pixels});")

@then("the page body should still be present")
def step_body_still_present(context):
    assert context.browser.find_elements(By.TAG_NAME, "body")

@when("I reload the page")
def step_reload(context):
    context.browser.refresh()
    WebDriverWait(context.browser, 20).until(
        EC.visibility_of_element_located((By.TAG_NAME, "body"))
    )

@then('I should find at least {n:d} elements matching "{css_selector}"')
def step_elements_by_css(context, n, css_selector):
    # Allow a small wait, then check count.
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector.split(",")[0].strip()))
    )
    elems = context.browser.find_elements(By.CSS_SELECTOR, css_selector)
    assert len(elems) >= n

@then('I should see one of the words "{csv}" somewhere on the page')
def step_any_word_in_source(context, csv):
    words = [w.strip() for w in csv.split(",")]
    WebDriverWait(context.browser, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    source = context.browser.page_source.lower()
    assert any(w.lower() in source for w in words), f"None of {words} found in page"

@then('I should see at least 1 nav link among "{csv}"')
def step_nav_links(context, csv):
    words = [w.strip().lower() for w in csv.split(",")]
    # Grab all visible links and check their text
    links = context.browser.find_elements(By.XPATH, "//a[normalize-space(string())!='']")
    visible_texts = [l.text.strip().lower() for l in links if l.is_displayed()]
    assert any(any(w in t for w in words) for t in visible_texts), f"No visible nav link matched any of {words}"

@when('I use the site search for "{query}"')
def step_use_site_search(context, query):
    d = context.browser
    # Try a few generic selectors; use the first one that exists.
    inputs = d.find_elements(By.XPATH,
        "//input[@type='search'] | "
        "//input[@name='q'] | "
        "//input[contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'search')]"
    )
    assert inputs, "No search input found"
    inp = inputs[0]
    inp.clear()
    inp.send_keys(query)
    inp.send_keys(Keys.RETURN)

@then("I should land on a search results page")
def step_on_search_results(context):
    WebDriverWait(context.browser, 20).until(
        lambda dr: "search" in dr.current_url.lower()
    )

# ---------- TAGS / CATEGORIES ----------
@then("I should see at least 1 tag or category link")
def step_has_tag_or_category(context):
    d = context.browser
    # Look for typical category/tag links in hrefs
    links = d.find_elements(
        By.XPATH,
        "//a[contains(@href,'/tag/') or "
        "     contains(@href,'/categories/') or "
        "     contains(@href,'/category/') or "
        "     contains(@href,'/class/') or "
        "     contains(@href,'/circuits/') or "
        "     contains(@href,'/workshop/') or "
        "     contains(@href,'/craft/') or "
        "     contains(@href,'/living/') or "
        "     contains(@href,'/outside/') or "
        "     contains(@href,'/teachers/')]"
    )

    # Fallback: tags in meta (many articles expose tags here)
    meta_tags = d.find_elements(
        By.XPATH,
        "//meta[@property='article:tag' or @name='keywords' or @name='parsely-tags']"
    )

    assert links or meta_tags, "No tags/categories links or metadata found"


# ---------- RICH MEDIA ----------
@then("I should see an embedded video or player")
def step_has_video_or_player(context):
    d = context.browser
    # Native <video> or common iframe providers.
    vids = d.find_elements(By.TAG_NAME, "video")
    frames = d.find_elements(By.XPATH,
        "//iframe[contains(translate(@src,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'youtube') or "
        "        contains(translate(@src,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'vimeo')]"
    )
    assert vids or frames, "No <video> or YouTube/Vimeo iframe found"

# ---------- DOWNLOAD / PRINT ----------
@then("I should find a download or print option")
def step_has_download_or_print(context):
    d = context.browser

    # Visible download links or files
    dl_links = d.find_elements(
        By.XPATH,
        "//a[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'download') or "
        "    contains(@href,'.pdf') or "
        "    contains(@href,'.zip') or "
        "    @download]"
    )

    # Visible print buttons/links
    print_controls = d.find_elements(
        By.XPATH,
        "//a[contains(.,'Print') or contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'print')] | "
        "//button[contains(.,'Print') or contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'print')]"
    )

    # Fallback: wording appears somewhere on the page (e.g., gated behind login)
    has_text_hint = any(
        word in d.page_source.lower() for word in ("download", "print")
    )

    assert dl_links or print_controls or has_text_hint, "No download or print option found"

# ---------- COMMENTS / DISCUSSION ----------
@when("I scroll to the comments section")
def step_scroll_comments(context):
    d = context.browser
    d.execute_script("window.scrollTo(0, document.body.scrollHeight);")

@then("I should see a comments heading")
def step_comments_visible(context):
    d = context.browser
    # Look for headings containing 'Comment'
    WebDriverWait(d, 10).until(
        lambda dr: any(el.is_displayed() for el in dr.find_elements(
            By.XPATH, "//h2[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'comment')] | "
                      "//h3[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'comment')]"
        ))
    )

# ---------- STEP-BY-STEP ----------
@then("I should see at least 1 step heading")
def step_has_step_heading(context):
    d = context.browser
    # Headings like "Step 1:", "Step 2", etc.
    steps = d.find_elements(By.XPATH,
        "//h2[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'step')] | "
        "//h3[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'step')]"
    )
    assert len(steps) >= 1

    