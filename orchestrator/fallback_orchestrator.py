# orchestrator/fallback_orchestrator.py
from tools.rag_tool import RAGTool
from tools.web_tool import WebToolStub
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class Agent:
    def __init__(self):
        self.rag = RAGTool()
        self.web = WebToolStub()

    def plan(self, user_query):
        q = user_query.lower()
        need_rag = any(k in q for k in ["policy","our company","our", "document", "policy"])
        need_web = any(k in q for k in ["current","average salary","salary","market","today","how much","rate","price"])
        # fallback: if ambiguous, use both
        return {"use_rag": need_rag or not need_web, "use_web": need_web or not need_rag}

    def act(self, user_query, plan):
        results = {}
        if plan["use_rag"]:
            results["rag"] = self.rag.query(user_query)
        if plan["use_web"]:
            results["web"] = self.web.search(user_query)
        return results

    def observe(self, raw_results):
        # normalize outputs into structured dict
        obs = {"tools": {}, "timestamp": datetime.utcnow().isoformat()+"Z"}
        if "rag" in raw_results:
            obs["tools"]["rag"] = raw_results["rag"]  # list of matches
        if "web" in raw_results:
            obs["tools"]["web"] = raw_results["web"]
        return obs

    def reflect(self, user_query, obs):
        parts = []
        if "rag" in obs["tools"]:
            if obs["tools"]["rag"]:
                top = obs["tools"]["rag"][0]
                parts.append(f"[RAG] Found in {top['source']}:\n{top['text'][:400]}...")
            else:
                parts.append("[RAG] No relevant internal doc found.")
        if "web" in obs["tools"]:
            web = obs["tools"]["web"]
            snippet = web["results"][0]["snippet"]
            parts.append(f"[Web] {snippet} (source: {web['results'][0]['url']})")
        # combine
        answer = "\n\n".join(parts)
        return {"answer": answer, "metadata": obs}

    def run(self, user_query):
        plan = self.plan(user_query)
        logging.info(f"Plan: {plan}")
        raw = self.act(user_query, plan)
        obs = self.observe(raw)
        final = self.reflect(user_query, obs)
        return final
