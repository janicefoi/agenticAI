from orchestrator.langgraph_graph import build_agent_graph

if __name__ == "__main__":
    agent = build_agent_graph()

    print("🤖 Welcome to your Agentic AI Research Assistant!")
    print("Type your query (or 'exit' to quit):")

    while True:
        user_query = input("\nYour query: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        result = agent.invoke({"query": user_query})

        print("\n=== FINAL ANSWER ===")
        print(result["observation"])
        print("\n=== REFLECTION ===")
        print(result["reflection"])
        print("\n=== METADATA ===")
        print(result["metadata"])
