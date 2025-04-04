# src/ingest_to_azure.py

import os
import uuid
import requests
import json
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from unstructured.partition.pdf import partition_pdf
from uuid import uuid4
import logging

logging.getLogger("unstructured").setLevel(logging.ERROR)
logging.getLogger("pdfminer").setLevel(logging.ERROR)
logging.getLogger("pdfminer.layout").setLevel(logging.ERROR)
logging.getLogger("pdfminer.converter").setLevel(logging.ERROR)

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

def prepare_payload(chunks):
    print("🔹 Preparing documents for Azure Search upload...")
    payload = {
        "value": [
            {
                "id": str(uuid4()),
                "content": doc.page_content,
                "page_number": doc.metadata.get("page_number", 0)
            }
            for doc in chunks
        ]
    }
    return payload

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

def upload_to_azure(docs, batch_size=1000):
    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX}/docs/index?api-version=2023-07-01-Preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": SEARCH_KEY
    }

    total = len(docs)
    print(f"Uploading {total} documents in batches of {batch_size}...")

    for i in range(0, total, batch_size):
        batch = docs[i:i + batch_size]
        payload = {"value": batch}

        print(f"Uploading batch {i // batch_size + 1} ({len(batch)} docs)...")
        res = requests.post(url, headers=headers, json=payload)

        if res.status_code >= 400:
            print(f"Error in batch {i // batch_size + 1}: {res.status_code} - {res.text}")
            res.raise_for_status()

    print("All batches uploaded successfully.")

if __name__ == "__main__":
    print("🔹 Loading and chunking PDF...")
    docs = load_pdf(PDF_PATH)
    chunks = chunk_documents(docs)
    payload = prepare_for_upload(chunks)
    upload_to_azure(payload)
