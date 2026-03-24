import json


def execute(page, action_json):

    try:
        action = json.loads(action_json)
    except:
        print("Invalid JSON:", action_json)
        return False

    if action["action"] == "done":
        return True

    elements = page.query_selector_all(
    "input, textarea, button"
    )

    try:

        el = elements[action["index"]]

    except:

        print("Invalid index")

        return False

    try:

        if action["action"] == "type":

            value = action.get("value", "")

            el.click()

            placeholder = (el.get_attribute("placeholder") or "").lower()

            if "date" in placeholder or "depart" in placeholder:

                print(" Skipping date typing")

                return False

            el.fill(value)

            if value.upper() in ["LHR", "DEL"]:

                select_airport(page, value.upper())

        elif action["action"] == "click":
            el.click()
        elif action["action"] == "click_text":
            text = action.get("text", "").lower()

            for el in elements:
                try:
                    t = (el.inner_text() or "").lower()
                    if text in t:
                        el.click()
                        print(f"✅ Clicked text: {text}")
                        return False
                except:
                    continue

    except Exception as e:
        print("Action failed:", e)

    return False

def select_flights_tab(page):
    try:
        page.wait_for_timeout(3000)

        # click Flights tab (by text)
        page.click("text=Flights", timeout=5000)

        print("✅ Switched to Flights tab")
        return True

    except Exception as e:
        print("❌ Flights tab not found:", e)
        return False
# =========================
# ✅ AIRPORT SELECTION
# =========================
def select_airport(page, code):
    try:
        page.wait_for_timeout(2000)

        options = page.query_selector_all("li, div")

        for opt in options:
            text = (opt.inner_text() or "").upper()

            # match exact airport code
            if code in text:
                if opt.is_visible():
                    opt.click()
                    print(f"✅ Selected airport: {code}")
                    return True

        print(f"❌ Airport not found: {code}")

    except Exception as e:
        print("Airport selection error:", e)

    return False

# def select_airport(page, code):
#     try:
#         page.wait_for_timeout(1500)

#         # click option containing code like (LHR)
#         page.locator(f"text={code}").first.click()

#         print(f"✅ Selected airport: {code}")
#         return True

#     except Exception as e:
#         print("❌ Airport select failed:", e)
#         return False

# =========================
# ✅ DATE PICKER
# =========================
def open_date_picker(page):
    try:
        page.click("input[placeholder*='Depart']", timeout=5000)
        print("✅ Date picker opened")
        return True
    except:
        print("❌ Date field not found")
        return False


def select_date(page):
    try:
        page.wait_for_timeout(2000)

        # move to next month (April if needed)
        try:
            page.click("button[aria-label='Next month']", timeout=2000)
        except:
            pass

        # force click date
        page.evaluate("""
        [...document.querySelectorAll('button')]
        .find(b => b.innerText.trim() === '30')?.click()
        """)

        print("✅ Date selected")
        return True

    except Exception as e:
        print("❌ Date selection failed:", e)
        return False


# =========================
# ✅ COOKIE HANDLER
# =========================

def handle_popups(page):
    """Automatically detect and dismiss location popups."""
    try:
        # look for common modal/dialog selectors
        popup = page.query_selector('div[role="dialog"], .location-popup, .modal')
        if popup:
            # look for deny or close button
            deny_btn = popup.query_selector('button.reject, button.no, button.deny, .close-btn')
            if deny_btn:
                deny_btn.click()
                page.wait_for_timeout(300)  # wait for animation
                return True
    except Exception as e:
        print("No location popup found:", e)
    return False
def handle_cookies(page):
    try:
        texts = ["accept", "agree", "got it", "allow", "yes"]

        buttons = page.query_selector_all("button")

        for btn in buttons:
            try:
                text = (btn.inner_text() or "").lower()

                if any(t in text for t in texts):
                    btn.click()
                    print("✅ Cookie accepted")
                    return True
            except:
                continue

    except Exception as e:
        print("Cookie handling error:", e)

    return False