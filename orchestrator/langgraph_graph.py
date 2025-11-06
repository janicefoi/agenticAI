# langgraph_graph.py
from langgraph.graph import StateGraph, END
from datetime import datetime
from typing import TypedDict, Any, Dict
from tools.rag_tool import rag_tool
from tools.web_tool import web_tool


# 🧠 1️⃣ Define the state schema
class AgentState(TypedDict, total=False):
    query: str
    plan: Dict[str, Any]
    results: Dict[str, Any]
    observation: str
    reflection: str
    metadata: Dict[str, Any]


# 🧭 2️⃣ PLAN: Decide which tools to use
def plan_node(state: AgentState):
    query = state["query"].lower()
    use_rag = True
    use_web = any(keyword in query for keyword in ["current", "latest", "today", "recent", "remote"])
    plan = {"use_rag": use_rag, "use_web": use_web}

    print(f"[PLAN] {plan}")
    return {"plan": plan}


# ⚙️ 3️⃣ ACT: Execute chosen tools
def act_node(state: AgentState):
    query = state["query"]
    plan = state["plan"]
    results = {}

    if plan.get("use_rag"):
        rag_results = rag_tool(query)
        results["rag"] = rag_results

    if plan.get("use_web"):
        web_results = web_tool(query)
        results["web"] = web_results

    print("[ACT] Results fetched.")
    return {"results": results}


# 🔍 4️⃣ OBSERVE: Summarize results
def observe_node(state: AgentState):
    results = state["results"]

    # RAG summary
    if "rag" in results and results["rag"]:
        rag_summary = f"📘 Found {len(results['rag'])} internal document(s)."
    else:
        rag_summary = "📘 No relevant internal docs found."

    # Web summary
    if "web" in results and results["web"]:
        first_result = results["web"][0]
        web_summary = f"🌐 Top web result: {first_result.get('snippet', '')}\nURL: {first_result.get('url', '')}"
    else:
        web_summary = "🌐 No web info found."

    observation = f"{rag_summary}\n\n{web_summary}"
    print("[OBSERVE] Observation complete.")
    return {"observation": observation}



# 💭 5️⃣ REFLECT: Adjust future behavior
def reflect_node(state: AgentState):
    observation = state["observation"]

    if "No relevant" in observation:
        reflection = "Next time: consider expanding the query or updating local data."
    else:
        reflection = "Query successful. Tools worked as expected."

    metadata = {
        "reflection": reflection,
        "timestamp": datetime.utcnow().isoformat(),
    }

    print("[REFLECT] Reflection complete.")
    return {"reflection": reflection, "metadata": metadata}


# 🧩 6️⃣ Assemble the LangGraph
def build_agent_graph():
    # ✅ Pass the state schema
    graph = StateGraph(AgentState)

    graph.add_node("plan", plan_node)
    graph.add_node("act", act_node)
    graph.add_node("observe", observe_node)
    graph.add_node("reflect", reflect_node)

    graph.add_edge("plan", "act")
    graph.add_edge("act", "observe")
    graph.add_edge("observe", "reflect")
    graph.add_edge("reflect", END)

    graph.set_entry_point("plan")
    return graph.compile()
