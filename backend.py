import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

@st.cache_resource
def get_vectorstore():
    data_folder = "./data"
    if not os.path.exists(data_folder) or not os.listdir(data_folder):
        return None
    
    is_streamlit = st.runtime.exists()
    
    docs = []
    
    # progress tracking
    if is_streamlit:
        status = st.status("Reading MIT Catalog PDFs...", expanded=True)
    else:
        print("Reading MIT Catalog PDFs...")

    for file in os.listdir(data_folder):
        if file.endswith(".pdf"):
            if is_streamlit: st.write(f"Processing {file}...")
            else: print(f"Processing {file}...")
            
            loader = PyPDFLoader(os.path.join(data_folder, file))
            docs.extend(loader.load())
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    final_chunks = splitter.split_documents(docs)
    
    if is_streamlit: st.write("Generating Embeddings (Ollama)...")
    else: print("Generating Embeddings (Ollama)...")
    
    embeddings = OllamaEmbeddings(model="llama3:8b")
    vectorstore = FAISS.from_documents(final_chunks, embeddings)
    
    if is_streamlit:
        status.update(label="Knowledge Base Ready!", state="complete", expanded=False)
    else:
        print("Knowledge Base Ready!")
        
    return vectorstore

def generate_assistant_response(vstore, prompt, student_history):
    retriever = vstore.as_retriever(search_kwargs={"k": 5})
    context_docs = retriever.invoke(prompt)
    context_text = "\n\n".join([f"Source: {d.metadata['source']}\nContent: {d.page_content}" for d in context_docs])

    llm = ChatOllama(model="llama3:8b", temperature=0)
    
    # Assessment 
    template = """You are a helpful MIT Course Advisor. 
    Answer strictly based on the context. If not found, say "I don't have that information in the provided catalog."
    
    Context: {context}
    Student History: {history}
    Question: {question}

    Format your response EXACTLY like this:
    Answer / Plan: 
    Why (requirements/prereqs satisfied): 
    Citations: 
    Clarifying questions (if needed): 
    Assumptions / Not in catalog: 
    """
    prompt_template = ChatPromptTemplate.from_template(template)
    chain = prompt_template | llm
    
    response = chain.invoke({
        "context": context_text, 
        "history": student_history, 
        "question": prompt
    })
    return response.content