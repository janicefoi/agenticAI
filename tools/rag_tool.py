def rag_tool(query: str):
    # Simulated offline RAG lookup
    if "policy" in query.lower():
        return [{"doc": "Company remote work policy: 3 days in-office minimum."}]
    return []
