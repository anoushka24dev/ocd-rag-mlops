import re

# ── Subtype keyword maps ───────────────────────────────────────────────────────

SUBTYPE_KEYWORDS = {
    "contamination": [
        "wash", "washing", "hands", "clean", "cleaning", "dirty", "germs",
        "contaminated", "contamination", "sanitize", "bacteria", "virus",
        "touched", "filthy", "soap", "shower", "scrub"
    ],
    "checking": [
        "check", "checking", "lock", "locked", "door", "stove", "oven",
        "unplugged", "turned off", "left on", "make sure", "verify",
        "go back", "did i", "forgot to"
    ],
    "counting": [
        "count", "counting", "arrange", "arranging", "symmetry", "even",
        "order", "ordering", "tap", "tapping", "repeat", "repeating",
        "number", "pattern", "straight", "align"
    ],
    "intrusive": [
        "intrusive", "thought", "thoughts", "harm", "hurt", "violent",
        "inappropriate", "horrible", "disgusting", "terrible", "bad person",
        "what if i", "i might", "i could", "urge to"
    ],
    "reassurance": [
        "am i okay", "am i normal", "am i safe", "is it okay",
        "does this mean", "are you sure", "can you confirm",
        "tell me", "reassure", "i need to know", "please confirm"
    ]
}

# ── Subtype responses ─────────────────────────────────────────────────────────

RESPONSES = {
    "contamination": (
        "I can see you're struggling with contamination-related urges.\n\n"
        "This is a very common OCD pattern. The urge to wash or clean feels overwhelming, "
        "but each time you act on it, the urge becomes stronger over time.\n\n"
        "Try this instead:\n"
        "• Acknowledge the thought: 'I notice I have the urge to wash'\n"
        "• Don't act on it for the next 2 minutes\n"
        "• Remind yourself: the discomfort will pass even without washing\n\n"
        "You are not in danger. The urge is OCD, not reality."
    ),

    "checking": (
        "I notice you're experiencing a checking urge.\n\n"
        "Checking provides temporary relief but reinforces the OCD cycle. "
        "Each check tells your brain the threat was real — making the next urge stronger.\n\n"
        "Try this instead:\n"
        "• Resist going back to check for the next 5 minutes\n"
        "• Say to yourself: 'I may have locked it. I can tolerate not knowing for certain'\n"
        "• Sit with the uncertainty — this is how OCD loses its power\n\n"
        "Uncertainty is uncomfortable but not dangerous."
    ),

    "counting": (
        "It sounds like you're dealing with counting, ordering, or symmetry compulsions.\n\n"
        "These rituals can feel like they prevent something bad from happening — "
        "but that connection isn't real. It's OCD creating a false sense of control.\n\n"
        "Try this instead:\n"
        "• Deliberately leave something slightly out of order\n"
        "• Resist the urge to fix or complete the pattern\n"
        "• Stay with the discomfort for 1 minute without acting\n\n"
        "The anxiety will peak and then fade — even without the ritual."
    ),

    "intrusive": (
        "Intrusive thoughts can feel very frightening, but having a thought "
        "does not mean you want it or will act on it.\n\n"
        "These thoughts are a hallmark of OCD — your brain is generating "
        "unwanted content, not reflecting who you are as a person.\n\n"
        "Try this instead:\n"
        "• Don't try to push the thought away — that makes it stronger\n"
        "• Say: 'I notice I'm having an intrusive thought. It's just OCD.'\n"
        "• Let the thought exist without engaging with it\n\n"
        "You are not your thoughts. They do not define you."
    ),

    "reassurance": (
        "I understand you're looking for certainty right now.\n\n"
        "However, seeking reassurance is itself a compulsion in OCD. "
        "Each time reassurance is given, it provides brief relief "
        "but makes the need for reassurance stronger next time.\n\n"
        "Try this instead:\n"
        "• Notice the urge to seek reassurance\n"
        "• Do not ask the question or seek the answer\n"
        "• Sit with the uncertainty for 30 seconds\n\n"
        "You are training your mind to tolerate not knowing — and that is the path forward."
    ),

    "general": (
        "I understand the urge to act on this.\n\n"
        "What you're experiencing is a common OCD pattern — "
        "the urge feels urgent and real, but acting on it only strengthens it over time.\n\n"
        "Try this instead:\n"
        "• Pause and name what you're feeling: 'This is OCD'\n"
        "• Delay your response by 2 minutes\n"
        "• Remind yourself: discomfort is temporary, but resisting builds strength\n\n"
        "You don't need to eliminate the urge — just delay your response to it."
    )
}

# ── Subtype detector ──────────────────────────────────────────────────────────

def detect_subtype(query):
    q = query.lower()
    q = re.sub(r"[^\w\s]", "", q)

    scores = {subtype: 0 for subtype in SUBTYPE_KEYWORDS}

    for subtype, keywords in SUBTYPE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in q:
                scores[subtype] += 1

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "general"

    return best

# ── Main response function ────────────────────────────────────────────────────

def get_specific_response(query):
    subtype = detect_subtype(query)
    print(f"SUBTYPE: {subtype}")
    return RESPONSES[subtype]