def detect_patterns(memory):
    history = memory.get("history", [])

    # Need at least 3 messages
    if len(history) < 3:
        return None

    # 🔹 Normalize history (important fix)
    cleaned = [q.strip().lower() for q in history]

    last_query = cleaned[-1]

    # Count repetition of cleaned query
    repetition_count = cleaned.count(last_query)

    if repetition_count >= 3:
        return (
            "I notice that this question has come up multiple times. "
            "This might be part of a repeating pattern or compulsion."
        )

    return None


def reflect_progress(memory):
    level = memory.get("erp_level", 1)

    if level >= 3:
        return f"You're making progress. Current ERP level: {level}"

    return None