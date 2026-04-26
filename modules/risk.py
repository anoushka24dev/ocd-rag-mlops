import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def detect_risk(query):
    q = clean_text(query)

    # High risk (flexible matching)
    if (
        "harm" in q
        or "hurt" in q
        or "kill" in q
    ):
        return "high"

    #  Distress detection
    distress_keywords = [
        "i cant take this",
        "i feel trapped",
        "hopeless",
        "overwhelmed",
        "scared",
        "afraid",
        "terrified"
    ]

    if any(k in q for k in distress_keywords):
        return "medium"

    return "low"


def crisis_response():
    return (
        "I'm really sorry you're going through this.\n\n"
        "Having these thoughts can feel very distressing, but they do not define you.\n\n"
        "It might really help to talk to someone you trust or a mental health professional.\n"
        "If you feel like you might act on these thoughts, please seek immediate help or contact a helpline in your area.\n\n"
        "You’re not alone in this."
    )