import streamlit as st
from streamlit_chat import message
# from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import PromptTemplate
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
# from langchain_core.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.schema.document import Document
from langchain.prompts import ChatPromptTemplate

CHROMA_PATH = "chroma_db"
# Set up message history for Streamlit session
chat_history = StreamlitChatMessageHistory()
# Set up memory
memory = ConversationBufferMemory(
    memory_key="history",
    chat_memory=chat_history,
    return_messages=True
)

# Prompt template
prompt = PromptTemplate(
    input_variables=["history", "input"],
    template="""
    You are a helpful assistant and your name is CampusPal.
    {history}
    User: {input}
    Assistant:"""
)

# Chat-compatible LLaMA model
llm = ChatOllama(model="llama3", 
                      temperature=0.6, 
                      max_tokens=2024, 
                      top_p=0.9, 
                      frequency_penalty=0.5, 
                      presence_penalty=0.5
                      )

# Chain using LangChain's RunnableSequence
chain = prompt | llm

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
do not say Based on the provided context or anything like that.
"""

def get_embedding_function():
    # embeddings = BedrockEmbeddings(
    #     credentials_profile_name="default", region_name="us-east-1"
    # )
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

# 🔧 Function to generate response
def generate_response(user_input: str,context) -> str:
    
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context, question=user_input)
    
    inputs = memory.load_memory_variables({})
    inputs["input"] = prompt
    response = chain.invoke(inputs)
    memory.save_context({"input": prompt}, {"output": response.content})
    return response.content

def chroma_search(query: str) -> list[Document]:
    # Initialize Chroma with the same embedding model as used in the app
    # embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(embedding_function=get_embedding_function(), persist_directory=CHROMA_PATH)
    
    # Perform the search
    print("Querying Chroma...")
    results = db.similarity_search_with_score(query, k=5)
    # print("Chroma query results:", results)
    context = []
    for doc, _score in results:
        file_name = doc.metadata["filename"]
        page_content = doc.page_content
        context.append(f"File: {file_name}\nContent: {page_content}")
    # for cont in context:
    #     print(cont)
    context_text = "\n\n---\n\n".join(context)
    return context_text

def app():

    # Title
    st.title("🧠 ChatGPT-like App with Modern LangChain Memory")

    # Initialize session state
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    
    # Define callback function to process user input
    def submit_input():
        user_input = st.session_state.input
        
        if user_input:
            if user_input.lower() in ["/bye", "/exit"]:
                # Clear LangChain memory
                memory.chat_memory.clear()
                # Clear Streamlit session state
                st.session_state['generated'] = []
                st.session_state['past'] = []
                st.success("Chat history cleared!")
            else:
                # Generate response
                chroma_context = chroma_search(user_input)
                if chroma_context:
                    output = generate_response(user_input, chroma_context)
                else:
                    context = "nothing"
                    output = generate_response(user_input, context)
                
                # Store the output
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)
            
            # Clear input
            st.session_state.input = ""
    
    # Text input with on_change callback
    user_input = st.text_input("You:", key='input', placeholder="Write your query", on_change=submit_input)
        
    # Display message history
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state['past'][i], key=str(i) + '_user', is_user=True)
            message(st.session_state["generated"][i], is_user=False, key=str(i))