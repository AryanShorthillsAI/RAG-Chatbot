import streamlit as st
import requests
import json

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/query"

st.title("🎬 Nolan Script Query System")
st.write("Ask anything about Christopher Nolan's movie scripts!")

# User input
query = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if query:
        response = requests.post(API_URL, json={"query": query})
        data = response.json()
        
        if "response" in data:
            st.write("**🤖 Answer:**", data["response"])
        else:
            st.write("⚠️ Error:", data.get("error", "Unknown error occurred"))

# Display query logs
# st.subheader("📜 Query Logs")
# try:
#     with open("../logs/query_logs.json", "r", encoding="utf-8") as file:
#         logs = json.load(file)
#         for log in reversed(logs[-3:]):  # Show last  logs
#             st.write(f"🕒 {log['timestamp']}")
#             st.write(f"**🔍 Query:** {log['query']}")
#             st.write(f"**💡 Answer:** {log['response']}")
#             st.write("---")
# except FileNotFoundError:
#     st.write("No logs found.")
