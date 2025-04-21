import numpy as np
import time
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

st.set_page_config(page_title="Chat with Memory")

def get_pdf_text(pdf_docs):
    documents= []
    for pdf in pdf_docs:
        # print(pdf.name,"\n")
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        documents.append({"filename":pdf.name,"content":text})
    print(f"Number of documents: {len(documents)}")
    # print(documents)
    return documents

def chunk_documents(documents, chunk_size=120, chunk_overlap=10):
    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    # return text_splitter.split_documents(documents)
    
    chunks = []
    for doc in documents:
        content = doc["content"]
        filename = doc["filename"]
        
        # Create a temporary Document object for the splitter
        temp_doc = Document(page_content=content, metadata={"filename": filename})
        
        # Split the document using RecursiveCharacterTextSplitter
        split_docs = text_splitter.split_documents([temp_doc])
        
        # Convert back to your preferred format
        for split_doc in split_docs:
            chunks.append({
                "filename": split_doc.metadata["filename"],
                "chunk": split_doc.page_content
            })
    
    return chunks


def add_to_chroma(chunks):
    # Load the existing Chroma database or create a new one
    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=get_embedding_function()
    )
    
    # Convert chunks to Document objects with metadata
    documents = [
        Document(
            page_content=chunk["chunk"], 
            metadata={"filename": chunk["filename"]}
        ) 
        for chunk in chunks
    ]
    
    # Add documents to the database
    db.add_documents(documents)
    
    # Persist the database to disk
    # db.persist()
    print(f"Added {len(documents)} documents to the Chroma database.")



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
            # print(text_chunks,"\n\n")
            print('\n\n')

            # create vector store
            add_to_chroma(text_chunks)
            
            e_time = time.time()
            st.write(f"Processed {len(pdf_docs)} PDFs in {round(e_time-s_time, 2)} seconds")
    
    
if app == "Home":
    home.app()
elif app == "ChatBot":
    chatbot.app()
elif app == "Raw Notes":
    # raw_notes.app()
    pass








# [
#     {'filename': 'Shubh_CV_Updated.pdf', 'chunk': 'Shubh Somani\n♂phone9999204212 — /envel⌢peshubhsomani098@gmail.com — /linkedinlinkedin.com/in/shubh-somani-aa4a49284 — /githubgithub.com/ShubhxYT\nSummary —Aspiring Machine Learning Engineer , Passionate About AI and Innovation , Data Structures & Algorithms\nLearner , Computer Vision Implementation in real life cases .\nSkills\nLanguages Python, Batch, Basics C , Java , IOT\nOSWindows , Debian(Kali) , RedHat(Fedora)Libraries Pytorch, Tensorflow, Scikit-Learn, LangChain,\nUltralytics, MediaPipe, OpenCV\nExperience\nIEEE CS (Computer Society) Oct 2024 – Apr 2025\nJunior Working Team (Technical)\nTeam Project : Virtual Mentor\n– AI-powered learning assistant that leverages the capabilities of LLM’s to provide students with an intelligent academic\ncompanion.'
#         }, 
#     {'filename': 'Shubh_CV_Updated.pdf', 'chunk': 'companion.\n– Integrating multi-modal RAG to process and understand course materials across all eight semesters of study, offering\nprecise, contextual, and interactive responses.\nEvent: Snatch\n– 48 teams are split up into brackets and compete with one another by answering Coding Block problems.\n– Teams that answer questions properly and first receive the most points and move forward.\n– Every squad has four power-ups that they can employ to their benefit.\nEvent: HackerzStreet\n– An intense 24-hour coding marathon.\n– Participants work on diverse technical themes with unique challenges.\nEducation\nGD Goenka Public School\nCBSE 12th (PCM)\nCBSE 10th\nCertifications\n– Stanford - Unsupervised Learning,Recommenders, Reinforcement Learning'
#         },
#     {'filename': 'Shubh_CV_Updated.pdf', 'chunk': '– Stanford - Unsupervised Learning,Recommenders, Reinforcement Learning\n– Stanford - Supervised Machine Learning: Regression and Classification\n– IBM - Python for Data Science, AI & Development (IBM)\nProjects\nVaidya-Health-Care-with-Yoga-Assistant Jan 2025\n– Comprehensive healthcare management system that includes various applications for yoga pose tracking, disease\nprediction, mental health analysis, and more.\n– The system leverages machine learning models, computer vision, and natural language processing to provide real-time\nfeedback and insights.\nManipal ChatBot (CampusPal) Apr 2025\n– A special large language model created using the RAG system and fine-tuning to relay Manipal University-specific\nresponses to the chatbot.'
#         }, 
#     {'filename': 'Shubh_CV_Updated.pdf', 'chunk': 'responses to the chatbot.\n– Upload your own PDF content to ask questions about your substance.\n– All of our university’s notes are located in one place.\nFinger Count Detector Aug 2024\n– Using the Google MediaPipe library to track hand and finger locations, enabling accurate detection of fingertip positions.\n– Developed a function to analyze whether fingers are open or closed, with the added functionality of distinguishing\nbetween the left and right hand.\nUltralytics (YOLO) Detection Aug 2024\n– Leveraged YOLOv8 models pre-trained to create various detection systems.\n– Examples such as a road traffic car counter and a people counter for mall environments\n– Custom training models for detecting rodents and vehicle number plates.'
#         }
# ]

# [Document(metadata={'producer': 'pdfTeX-1.40.25', 'creator': 'LaTeX with hyperref', 'creationdate': '2025-04-16T21:10:19+00:00', 'author': '', 'keywords': '', 'moddate': '2025-04-16T21:10:19+00:00', 'ptex.fullbanner': 'This is pdfTeX, Version 3.141592653-2.6-1.40.25 (TeX Live 2023) kpathsea version 6.3.5', 'subject': '', 'title': '', 'trapped': '/False', 'source': 'D:\\Codes\\pdf chatter\\data\\Shubh_CV_Updated.pdf', 'total_pages': 1, 'page': 0, 'page_label': '1'
#                     }, 
#           page_content='Shubh Somani\n♂phone9999204212 — /envel⌢peshubhsomani098@gmail.com — /linkedinlinkedin.com/in/shubh-somani-aa4a49284 — /githubgithub.com/ShubhxYT\nSummary — Aspiring Machine Learning Engineer , Passionate About AI and Innovation , Data Structures & Algorithms\nLearner , Computer Vision Implementation in real life cases .\nSkills\nLanguages Python, Batch, Basics C , Java , IOT\nOS Windows , Debian(Kali) , RedHat(Fedora)\nLibraries Pytorch, Tensorflow, Scikit-Learn, LangChain,\nUltralytics, MediaPipe, OpenCV\nExperience\nIEEE CS (Computer Society) Oct 2024 – Apr 2025\nJunior Working Team (Technical)\nTeam Project : Virtual Mentor\n– AI-powered learning assistant that leverages the capabilities of LLM’s to provide students with an intelligent academic\ncompanion.\n– Integrating multi-modal RAG to process and understand course materials across all eight semesters of study , offering\nprecise, contextual, and interactive responses.\nEvent: Snatch\n– 48 teams are split up into brackets and compete with one another by answering Coding Block problems.\n– Teams that answer questions properly and first receive the most points and move forward.\n– Every squad has four power-ups that they can employ to their benefit.\nEvent: HackerzStreet\n– An intense 24-hour coding marathon.\n– Participants work on diverse technical themes with unique challenges.\nEducation\nGD Goenka Public School\nCBSE 12th (PCM)\nCBSE 10th\nCertifications\n– Stanford - Unsupervised Learning,Recommenders, Reinforcement Learning\n– Stanford - Supervised Machine Learning: Regression and Classification\n– IBM - Python for Data Science, AI & Development (IBM)\nProjects\nVaidya-Health-Care-with-Yoga-Assistant Jan 2025\n– Comprehensive healthcare management system that includes various applications for yoga pose tracking, disease\nprediction, mental health analysis, and more.\n– The system leverages machine learning models, computer vision, and natural language processing to provide real-time\nfeedback and insights.\nManipal ChatBot (CampusPal) Apr 2025\n– A special large language model created using the RAG system and fine-tuning to relay Manipal University-specific\nresponses to the chatbot.\n– Upload your own PDF content to ask questions about your substance.\n– All of our university’s notes are located in one place.\nFinger Count Detector Aug 2024\n– Using the Google MediaPipe library to track hand and finger locations, enabling accurate detection of fingertip positions.\n– Developed a function to analyze whether fingers are open or closed, with the added functionality of distinguishing\nbetween the left and right hand.\nUltralytics (YOLO) Detection Aug 2024\n– Leveraged YOLOv8 models pre-trained to create various detection systems.\n– Examples such as a road traffic car counter and a people counter for mall environments\n– Custom training models for detecting rodents and vehicle number plates.'
#           )
#  ]


# ['Shubh Somani\n♂phone9999204212 — /envel⌢peshubhsomani098@gmail.com — /linkedinlinkedin.com/in/shubh-somani-aa4a49284 — /githubgithub.com/ShubhxYT\nSummary —Aspiring Machine Learning Engineer , Passionate About AI and Innovation , Data Structures & Algorithms\nLearner , Computer Vision Implementation in real life cases .\nSkills\nLanguages Python, Batch, Basics C , Java , IOT\nOSWindows , Debian(Kali) , RedHat(Fedora)Libraries Pytorch, Tensorflow, Scikit-Learn, LangChain,\nUltralytics, MediaPipe, OpenCV\nExperience\nIEEE CS (Computer Society) Oct 2024 – Apr 2025\nJunior Working Team (Technical)\nTeam Project : Virtual Mentor\n– AI-powered learning assistant that leverages the capabilities of LLM’s to provide students with an intelligent academic\ncompanion.\n– Integrating multi-modal RAG to process and understand course materials across all eight semesters of study, offering\nprecise, contextual, and interactive responses.\nEvent: Snatch', 'companion.\n– Integrating multi-modal RAG to process and understand course materials across all eight semesters of study, offering\nprecise, contextual, and interactive responses.\nEvent: Snatch\n– 48 teams are split up into brackets and compete with one another by answering Coding Block problems.\n– Teams that answer questions properly and first receive the most points and move forward.\n– Every squad has four power-ups that they can employ to their benefit.\nEvent: HackerzStreet\n– An intense 24-hour coding marathon.\n– Participants work on diverse technical themes with unique challenges.\nEducation\nGD Goenka Public School\nCBSE 12th (PCM)\nCBSE 10th\nCertifications\n– Stanford - Unsupervised Learning,Recommenders, Reinforcement Learning\n– Stanford - Supervised Machine Learning: Regression and Classification\n– IBM - Python for Data Science, AI & Development (IBM)\nProjects\nVaidya-Health-Care-with-Yoga-Assistant Jan 2025', '– Stanford - Supervised Machine Learning: Regression and Classification\n– IBM - Python for Data Science, AI & Development (IBM)\nProjects\nVaidya-Health-Care-with-Yoga-Assistant Jan 2025\n– Comprehensive healthcare management system that includes various applications for yoga pose tracking, disease\nprediction, mental health analysis, and more.\n– The system leverages machine learning models, computer vision, and natural language processing to provide real-time\nfeedback and insights.\nManipal ChatBot (CampusPal) Apr 2025\n– A special large language model created using the RAG system and fine-tuning to relay Manipal University-specific\nresponses to the chatbot.\n– Upload your own PDF content to ask questions about your substance.\n– All of our university’s notes are located in one place.\nFinger Count Detector Aug 2024\n– Using the Google MediaPipe library to track hand and finger locations, enabling accurate detection of fingertip positions.', 'Finger Count Detector Aug 2024\n– Using the Google MediaPipe library to track hand and finger locations, enabling accurate detection of fingertip positions.\n –  Developed a function to analyze whether fingers are open or closed, with the added functionality of distinguishing\nbetween the left and right hand.\nUltralytics (YOLO) Detection Aug 2024\n– Leveraged YOLOv8 models pre-trained to create various detection systems.\n– Examples such as a road traffic car counter and a people counter for mall environments\n– Custom training models for detecting rodents and vehicle number plates.']

