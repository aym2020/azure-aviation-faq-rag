import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
import streamlit as st
from aviationrag.azure_rag_chain import search_chunks, call_openai

load_dotenv()

st.set_page_config(page_title="Azure Aviation RAG Chatbot", layout="wide")
st.title("🛫 Azure Aviation FAQ Chatbot")
st.caption("Ask aviation regulatory questions based on the EASA Air OPS document.")

question = st.text_input("❓ Ask your question", placeholder="e.g. When can a commander extend the flight duty period?")

if st.button("🧠 Get Answer") and question:
    with st.spinner("Retrieving answer..."):
        chunks = search_chunks(question, top_k=5)
        context = "\n\n".join(chunks)
        answer = call_openai(question, context)

        st.markdown("### 💬 Answer")
        st.write(answer)

        st.markdown("### 📄 Pages Used")
        for chunk in chunks:
            lines = chunk.split("\n")
            page_line = lines[0] if lines else "Page N/A"
            st.write(page_line)
