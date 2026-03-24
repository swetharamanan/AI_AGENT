from browser import start_browser
from parser import extract_elements
from llm import ask_gemini
from executor import execute
from executor import handle_cookies   # 👈 add this
from executor import handle_cookies, open_date_picker, select_date , select_flights_tab,handle_popups

def select_one_way(page):
    print("selecting one way")

    try:
        page.wait_for_timeout(2000)

        page.get_by_label("One-way").click()
        print("✅ Selected One-way (label)")
        return True

    except:
        try:
            # ✅ Try exact visible text
            page.locator("text=One-way").first.click()
            print("✅ Selected One-way (text)")
            return True

        except:
            try:
                # ✅ Last fallback: any radio near "One-way"
                radios = page.locator("input[type='radio']")
                count = radios.count()

                for i in range(count):
                    label = radios.nth(i).evaluate(
                        "el => el.closest('label')?.innerText || ''"
                    )

                    if "one" in label.lower():
                        radios.nth(i).click()
                        print("✅ Selected One-way (radio match)")
                        return True

            except Exception as e:
                print("❌ One-way failed:", e)

    return False

def run_agent(task, url):
    page, browser, p = start_browser()
    page.goto(url)

    # wait for page + cookie popup
    page.wait_for_timeout(3000)

    handle_popups(page)

    task_lower = task.lower()

    if "flight_tab" in task_lower:
        print("selecting tab")
        select_flights_tab(page)

    #  handle cookies (retry few times)
    for _ in range(3):
        if handle_cookies(page):
            break
        page.wait_for_timeout(2000)

    select_one_way(page) 


    history = []

    for step in range(10):
        print(f"\n--- Step {step} ---")

        elements = extract_elements(page)

        decision = ask_gemini(task, elements, history)
        print("decisionssss------------>",decision)

        print("Decision:", decision)

        done = execute(page, decision)

        history.append(decision)

        #  ADD THIS BLOCK HERE (INSIDE LOOP)
        if step == 2:
            print("👉 Selecting date now...")
            page.wait_for_timeout(2000)
            open_date_picker(page)
            select_date(page)

        if done:
            print("Task completed ✅")
            break

    browser.close()
    p.stop()


if __name__ == "__main__":
    run_agent(
    """
    
    Fill flight search form:

    - Select "One-way"
    - Departure airport: LHR (London Heathrow)
    - Arrival airport: DEL (Delhi)
    - Travel date: 30 April

    Then click search/submit
    """,
    "https://in.trip.com/flights/?locale=en-IN&curr=TWD"
)