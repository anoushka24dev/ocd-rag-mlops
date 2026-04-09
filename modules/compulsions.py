def handle_compulsion(query, memory):
    # Get current ERP level (default = 1)
    level = memory.get("erp_level", 1)

    # Decide action based on level
    if level == 1:
        step = "delay the action for 30 seconds"
    elif level == 2:
        step = "delay the action for 2 minutes"
    else:
        step = "try skipping the action once"

    # Increase level for next time (max = 3)
    memory["erp_level"] = min(level + 1, 3)

    return (
        "I understand the urge to act.\n\n"
        f"Instead, try to {step}.\n\n"
        "This helps weaken the compulsion over time.\n"
        "You don't need to eliminate the urge—just delay your response."
    )