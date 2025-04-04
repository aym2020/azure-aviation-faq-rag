from setuptools import setup, find_packages

setup(
    name="aviationrag",
    version="0.1",
    packages=find_packages(include=["aviationrag", "aviationrag.*"]),
    install_requires=[
        "azure-search-documents",
        "langchain",
        "langchain-openai",
        "faiss-cpu",
        "openai",
        "pypdf",
        "python-dotenv",
        "langchain-community",
        "tiktoken",
        "rank_bm25",
        "sentence-transformers",
        "unstructured[pdf]",
        "pdfminer.six",
        "pi-heif",
        "streamlit",
    ],
)
