# src/ingest_to_azure.py
import os
import uuid
import requests
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from unstructured.partition.pdf import partition_pdf

load_dotenv()

SEARCH_ENDPOINT = os.getenv("AZURE_COG_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_COG_SEARCH_KEY")
SEARCH_INDEX = os.getenv("AZURE_COG_SEARCH_INDEX")

PDF_PATH = "data/easa_air_ops.pdf"

def load_pdf(path):
    elements = partition_pdf(path, strategy="fast")
    docs = []
    for el in elements:
        if el.text.strip():
            docs.append(Document(
                page_content=el.text.strip(),
                metadata={"page_number": el.metadata.page_number}
            ))
    return docs

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    return splitter.split_documents(docs)

def prepare_for_upload(chunks):
    return [
        {
            "@search.action": "upload",
            "id": str(uuid.uuid4()),
            "content": chunk.page_content,
            "page_number": chunk.metadata.get("page_number", -1)
        }
        for chunk in chunks
    ]

def upload_to_azure(docs):
    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX}/docs/index?api-version=2023-07-01-Preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": SEARCH_KEY
    }
    payload = {"value": docs}
    res = requests.post(url, headers=headers, json=payload)
    res.raise_for_status()
    print(f"✅ Uploaded {len(docs)} documents to Azure Search.")

if __name__ == "__main__":
    print("🔹 Loading and chunking PDF...")
    docs = load_pdf(PDF_PATH)
    chunks = chunk_documents(docs)
    payload = prepare_for_upload(chunks)
    upload_to_azure(payload)
