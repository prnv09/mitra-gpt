# RAG Chatbot with ChromaDB Storage

This repository contains a chatbot built with a Retrieval-Augmented Generation (RAG) architecture, designed for efficient querying of PDF documents stored in ChromaDB. It leverages two main scripts: `saveinfo.py` for document processing and embedding storage, and `run.py` for conversational querying.

## Overview

This chatbot allows you to add PDF documents, which are processed into smaller chunks and embedded for efficient storage and retrieval. Using `saveinfo.py`, embeddings are stored in ChromaDB, and `run.py` then enables querying based on these stored embeddings, providing accurate answers from the contents of your PDFs.

## Requirements
- Libraries listed in `requirements.txt`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/prnv09/openai-rag/
   cd openai-rag 

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
3. Configure OpenAI API Key in a .env file.

   
