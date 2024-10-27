
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
load_dotenv()

openai_api_key = os.getenv('OPENAI_KEY')
llm = ChatOpenAI(model="gpt-4o")

def generate_response(user_query):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    vector_store = Chroma(
    collection_name="default",
    embedding_function=embeddings,
       persist_directory = "./chroma_db"   )
    retriever = vector_store.as_retriever()

    system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    results = rag_chain.invoke({"input": user_query})
    st.write(results.get("answer"))
    
    

st.header("Chat with multiple PDFs :books:")
user_question = st.text_input("Ask a question about your documents:")
if user_question:
    generate_response(user_question)