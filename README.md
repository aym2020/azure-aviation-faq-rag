
# Azure Aviation FAQ Chatbot

## Overview

The **Azure Aviation FAQ Chatbot** is a Generative AI-powered application that answers aviation regulatory questions based on the **EASA Air OPS** documentation. Built with Streamlit, Azure OpenAI, and Azure AI Search, this chatbot leverages Retrieval-Augmented Generation (RAG) techniques to provide accurate and relevant responses.

---

## Project Structure

```
azure-aviation-faq-rag/
├── .github/
│   └── workflows/
│       └── azure_webapp_deploy.yaml
├── .streamlit/
│   └── config.toml
├── app/
│   └── streamlit_app.py
├── data/
│   └── easa_air_ops.pdf
├── src/
│   ├── __init__.py
│   ├── azure_rag_chain.py
│   ├── config.py
│   └── ingest_to_azure.py
├── .env
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── runtime.txt
└── setup.py
```

---

## Features

- ✅ **RAG Implementation:**  
  Combines Azure Cognitive Search and Azure OpenAI (GPT-4o) for precise and context-aware answers.
  
- ✅ **Azure Integration:**  
  Seamlessly integrated and deployed on Azure App Service with automatic deployments via GitHub Actions.

- ✅ **User-Friendly Interface:**  
  Built using Streamlit for interactive, clean, and responsive user experience.

---

## Technologies Used

- **Python:** 3.10
- **Streamlit:** Web application framework for interactive frontend.
- **Azure OpenAI (GPT-4o):** Advanced GenAI model used for generating answers.
- **Azure AI Search:** Used for indexing and retrieving relevant document chunks.
- **Docker:** For consistent and portable environments.
- **GitHub Actions:** Continuous Integration/Continuous Deployment (CI/CD).

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/azure-aviation-faq-rag.git
cd azure-aviation-faq-rag
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 3. Configure Environment Variables

Create a `.env` file at the root directory and set your environment variables:

```bash
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_COG_SEARCH_ENDPOINT=your_search_endpoint
AZURE_COG_SEARCH_KEY=your_search_key
AZURE_COG_SEARCH_INDEX=aviation-faq-index
```

### 4. Run the Application Locally

```bash
streamlit run app/streamlit_app.py
```

---

## Deployment

The application is configured for automatic deployment using GitHub Actions.

- Push your code to the `master` branch, and the CI/CD pipeline will automatically deploy to your Azure App Service.

---

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
