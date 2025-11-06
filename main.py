# main.py
import os

# 1. Load documents
docs = {}
for fname in os.listdir("knowledge_docs"):
    if fname.endswith(".txt"):
        with open(os.path.join("knowledge_docs", fname)) as f:
            docs[fname] = f.read()

# 2. Query function
def query_documents(query):
    for name, text in docs.items():
        if query.lower() in text.lower():
            return f"Found in {name}:\n{text}"
    return "No match found."

# 3. Run query
response = query_documents("AI engineer")
print(response)
