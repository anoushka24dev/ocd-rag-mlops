import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def detect_intent(query):
    q = clean_text(query)

    reassurance_keywords = [
        "am i safe",
        "is it safe",
        "are you sure",
        "will it be fine",
        "nothing will happen"
    ]

    
    if "safe" in q or any(k in q for k in reassurance_keywords):
        return "reassurance"

    
    compulsion_patterns = [
        r"(wash|check|verify)(\s+\w+)*\s+(again|more|once)",
        r"(again|more|once)(\s+\w+)*\s+(wash|check|verify)",
        r"repeat",
        r"make sure"
    ]

    if any(re.search(p, q) for p in compulsion_patterns):
        return "compulsion"

    return "normal"