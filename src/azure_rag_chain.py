# src/azure_rag_chain.py

import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import openai
from openai import AzureOpenAI

load_dotenv()

# Azure Cognitive Search
AZURE_COG_SEARCH_ENDPOINT = os.getenv("AZURE_COG_SEARCH_ENDPOINT")
AZURE_COG_SEARCH_KEY = os.getenv("AZURE_COG_SEARCH_KEY")
AZURE_COG_SEARCH_INDEX = os.getenv("AZURE_COG_SEARCH_INDEX")

# Azure OpenAI
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Setup clients
openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_type = "azure"
openai.api_version = AZURE_OPENAI_API_VERSION

def search_chunks(query, top_k=5):
    search_client = SearchClient(
        endpoint=AZURE_COG_SEARCH_ENDPOINT,
        index_name=AZURE_COG_SEARCH_INDEX,
        credential=AzureKeyCredential(AZURE_COG_SEARCH_KEY)
    )

    results = search_client.search(search_text=query, top=top_k)

    docs = []
    for result in results:
        content = result["content"]
        page = result.get("page_number", "N/A")
        docs.append(f"[Page {page}]\n{content}")
    return docs

def call_openai(question, context):
    messages = [
        {"role": "system", "content": """You are an expert in EASA aviation regulations. You answer questions using ONLY the provided context.

Instructions:
- Provide a detailed and structured explanation, as if training a new pilot or compliance officer.
- Reference the source page(s) (e.g., "As stated on Page 102").
- If the answer is only partially in the context, summarize it.
- Only say "I don’t know" if the context clearly doesn’t mention it at all.
- Use bullet points or paragraph form.
- Answer length should be 3–6 sentences.

Context:
""" + context},
        {"role": "user", "content": question}
    ]

    response = openai_client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=messages,
        temperature=0.1
    )

    return response.choices[0].message.content

def ask(question):
    context_chunks = search_chunks(question, top_k=5)
    combined_context = "\n\n".join(context_chunks)
    answer = call_openai(question, combined_context)

    print("\nQuestion:")
    print(question)
    print("\nAnswer:")
    print(answer)

# CLI
if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or type 'exit'): ")
        if q.lower() == "exit":
            break
        ask(q)
