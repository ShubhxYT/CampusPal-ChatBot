import numpy as np
import time
import atexit
import shutil
import os
import streamlit as st

from streamlit_chat import message
from streamlit_option_menu import option_menu
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
# from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_chroma import Chroma

import chatbot,home,raw_notes
from chatbot import get_embedding_function,CHROMA_PATH

def get_pdf_text(pdf_docs):
    pdf_documents= []
    for pdf in pdf_docs:
        # print(pdf.name,"\n")
        # print(pdf)
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        pdf_documents.append({"filename":pdf.name,"id":pdf.file_id,"content":text})
    print(f"Number of pdf documents: {len(pdf_documents)}")
    # print(pdf_documents)
    return pdf_documents

def chunk_documents(documents, chunk_size=120, chunk_overlap=10):
    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    
    chunks = []
    for doc in documents:
        # print(doc)
        content = doc["content"]
        filename = doc["filename"]
        id = doc["id"]
        
        print(f"id: {id}\nfilename: {filename}\n")
        
        # Create a temporary Document object for the splitter
        temp_doc = Document(page_content=content, metadata={"filename": filename,"id":id})
        
        # Split the document using RecursiveCharacterTextSplitter
        split_docs = text_splitter.split_documents([temp_doc])
        
        # Convert back to your preferred format
        for split_doc in split_docs:
            chunks.append({
                "filename": split_doc.metadata["filename"],
                "id": split_doc.metadata["id"],
                "chunk": split_doc.page_content
            })
    
    return chunks

def add_to_chroma(chunks):
    # Load the existing Chroma database or create a new one
    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=get_embedding_function()
    )
    
    # Add or Update the documents.
    existing_items = db.get()  # IDs are always included by default
    # print(existing_items)
    existing_names = [i["filename"] for i in existing_items["metadatas"]]
    # print(existing_names)
        
    print(f"Number of existing documents in DB: {len(existing_names)}")

    
    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks:
        if chunk["filename"] not in existing_names:
            new_chunks.append(chunk)
    
    # Convert chunks to Document objects with metadata
    if new_chunks:
        print(f"\n👉 Adding new documents: {len(new_chunks)}")
        documents = [
            Document(
                page_content=chunk["chunk"], 
                metadata={"filename": chunk["filename"], "id": chunk["id"]}
            ) 
            for chunk in new_chunks
        ]
        db.add_documents(documents)
        print(f"Added {len(documents)} documents to the Chroma database.")
    else:
        print("✅ No new documents to add")
    

st.set_page_config(page_title="Chat with Memory",layout="wide")

with st.sidebar:
    app = option_menu(
        menu_title='Navigation', 
        options=['Home',"ChatBot", "Raw Notes"],
        icons=["house", "chat", "book"],
        default_index=0,
        styles={
            
            "container": {"padding": "5!important", "background-color": "0f1117"},
            "icon": {"font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "e95b48"},
        }
    )
    st.subheader("Your documents")
    # pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    pdf_docs = st.file_uploader("Upload your pdfs here", type=["pdf"], accept_multiple_files=True)
    chunk_size = st.slider("Select chunk size", min_value=10, max_value=500, value=200)
    
    if st.button("Process"):
        with st.spinner("Processing"):
            s_time = time.time()
            
            # get pdf text
            raw_text = get_pdf_text(pdf_docs)
            # get the text chunks
            text_chunks = chunk_documents(raw_text, chunk_size=chunk_size, chunk_overlap=10)
            # create vector store
            add_to_chroma(text_chunks)
            
            e_time = time.time()
            st.write(f"Processed {len(pdf_docs)} PDFs in {round(e_time-s_time, 2)} seconds")
    
    
if app == "Home":
    home.app()
elif app == "ChatBot":
    chatbot.app()
elif app == "Raw Notes":
    raw_notes.app()


