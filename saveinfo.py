import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from uuid import uuid4
import os

openai_api_key = os.getenv('OPENAI_KEY')
def get_pdf_text(pdf_docs):
    text = ""
    
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf) 
        for page in pdf_reader.pages:
            text += page.extract_text() # extracting text from each page
    return text

def get_text_chunks(raw_text):
    documents = []
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 250,
        chunk_overlap = 50, 
        length_function = len
    )
    chunks = text_splitter.split_text(raw_text)
    print(f"chunking done {type(chunks)}")
    for chunk in chunks:
        doc = Document(page_content=chunk)
        documents.append(doc)
    #print(f"documents created : {documents}")
    return documents

def create_vector(text_doc):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = Chroma(
    collection_name="default",
    embedding_function=embeddings,
    persist_directory = "./chroma_db" 
)
    uuids = [str(uuid4()) for _ in range(len(text_doc))]
    vector_store.add_documents(documents=text_doc, ids=uuids)
    


pdf_docs = st.file_uploader(
    "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)

if st.button("Process"):
    with st.spinner("Processing"):
        # get pdf text
        raw_text = get_pdf_text(pdf_docs)
        # get the text chunks
        text_chunks = get_text_chunks(raw_text)
        # create vector store
        db = create_vector(text_chunks)