import streamlit as st
import chatbot, raw_notes

# from app import app

def app():
    """
    Main Streamlit application homepage for CampusPal.
    """
    # Page config to avoid duplicate buttons being triggered
    # st.set_page_config(page_title="CampusPal - Home", layout="wide")
    
    # Create session state for navigation if it doesn't exist
    # if 'page' not in st.session_state:
    #     st.session_state.page = 'home'
    
    # # If we're not on the home page, show the appropriate page
    # if st.session_state.page == 'chatbot':
    #     chatbot.app()
    #     return
    # elif st.session_state.page == 'raw_notes':
    #     raw_notes.app()
    #     return
    
    # Home page content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Main title and logo
        st.title("🎓 CAMPUSPAL")
        st.subheader("Your AI Learning Companion for Manipal University")
        
        
    
    with col2:
        st.image("image.png", use_container_width=True)
        
        # # Quick access buttons with navigation functionality
        # st.markdown("### Quick Access")
        # if st.button("📝 Start Chatting", use_container_width=True):
        #     # chatbot.app()
        #     app = "ChatBot"
        #     # st.session_state.page = 'chatbot'
        #     st.rerun()
        
        # if st.button("📚 Browse Notes", use_container_width=True):
        #     # st.session_state.page = 'raw_notes'
        #     app = "Raw Notes"
        #     st.rerun()
    
    
        # Description
    st.markdown("""
    **CampusPal** provides personalized, easily accessible, and interactive learning resources 
    specifically designed for Manipal University students.
    """)
    
    # Technical information
    st.markdown("""
    ### 🤖 Key Features
    - **Smart Chatbot**: Get instant answers to your academic questions
    - **Document Analysis**: Upload and analyze course materials
    - **Personalized Learning**: Tailored responses based on your curriculum
    - **All Semesters Covered**: Access information across all eight semesters
    
    ### 📚 How to Use
    1. **ChatBot**: Ask questions related to your courses
    2. **Raw Notes**: Browse and search through available study materials
    3. **Upload Documents**: Add your own study materials to enhance responses
    """)
    st.markdown("---")
    st.markdown("""
    ### 🛠️ Technology
    CampusPal is built using RAG (Retrieval-Augmented Generation) technology with fine-tuning 
    to provide Manipal University-specific knowledge. The system leverages LLama3 to process 
    and understand course materials across multiple disciplines.
    
    ### 🧠 Available Subject Areas
    BFE • CM • EC • EES • EMM • EP • MATLAB • PSUC and more
    """)
    
    # Footer
    st.markdown("---")
    st.caption("© 2023-2024 CampusPal • Made with ❤️ for Manipal University Students")

if __name__ == "__main__":
    app()