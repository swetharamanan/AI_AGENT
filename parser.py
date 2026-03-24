def extract_elements(page):
    elements = page.query_selector_all(
    "input, textarea, button"
)

    data = []

    for i, el in enumerate(elements):
        try:
            data.append({
    "index": i,
    "tag": el.evaluate("e => e.tagName"),
    "text": (el.inner_text() or "")[:50],
    "placeholder": el.get_attribute("placeholder"),
    "type": el.get_attribute("type")
})
        except:
            continue

    return data