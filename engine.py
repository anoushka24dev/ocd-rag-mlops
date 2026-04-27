from modules.intentM1 import detect_intent
from modules.reassurance import handle_reassurance
from modules.compulsions import handle_compulsion
from modules.risk import detect_risk, crisis_response
from modules.patterns import detect_patterns, reflect_progress
from modules.responses import get_specific_response


def process_query(query, memory, qa_chain):
    print("ENGINE RUNNING")

    #  Save history
    memory["history"] = memory.get("history", []) + [query]
    

    cleaned = [q.strip().lower() for q in memory["history"]]

    pattern = detect_patterns(memory)
    print("PATTERN RESULT:", pattern)

    # Step 1: Risk check
    risk = detect_risk(query)
    print("RISK:", risk)

    if risk == "high":
        return crisis_response()

    # 🔹 Step 2: Intent detection
    intent = detect_intent(query)
    print("INTENT:", intent)
    if intent == "Reassurance":
        cleaned = [" ".join(q.lower().split()) for q in memory["history"]]

        

        last = cleaned[-1]
        count = cleaned.count(last)

        print("LAST QUERY:", last)
        print("COUNT:", count)

        if count >= 3:
            print("SWITCHING TO COMPULSION")
            response = handle_compulsion(query, memory)
        else:
            print("STILL REASSURANCE")
            response = handle_reassurance(query)

        pattern = detect_patterns(memory)
        if pattern:
            response += f"\n\n{pattern}"

        return response

      # COMPULSION FLOW
    if intent == "Compulsion":
        response = get_specific_response(query)
        pattern = detect_patterns(memory)
        progress = reflect_progress(memory)

        if pattern:
            response += f"\n\n{pattern}"

        if progress:
            response += f"\n\n{progress}"

        return response

    #  NORMAL → RAG
    result = qa_chain.invoke({"query": query})

    answer = result["result"]
    sources = result["source_documents"]

    response = f"\n{answer}\n"

    #  Add pattern insight
    pattern = detect_patterns(memory)
    progress = reflect_progress(memory)

    if pattern:
        response += f"\n\n{pattern}"

    if progress:
        response += f"\n\n{progress}"

    #  Add sources (remove duplicates)
    seen = set()
    response += "\n\nSources:\n"

    for doc in sources:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")

        key = (source, page)
        if key not in seen:
            response += f"- {source} (page {page})\n"
            seen.add(key)

    return response