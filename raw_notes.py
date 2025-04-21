from streamlit_file_browser import st_file_browser,show_file_preview
import streamlit as st

from streamlit_pdf_viewer import pdf_viewer

import os
    
import streamlit as st
from streamlit_file_browser import st_file_browser

def app():
    current_path = "D:/Codes/pdf chatter/Fine-tuning-learning/college_data"

    cols = st.columns(2)

    with cols[0]:
        st.header("Raw Notes")
        st.write("Click on the file to preview it")
        st.write("Search for the file 👇")
        event = st_file_browser(
            path=current_path,
            # key="deep",
            show_download_file=True,
            show_preview=False,
            show_preview_top=False,
            show_choose_file=False,
            show_delete_file=False,
            show_new_folder=False,
            show_upload_file=False,
        )
        # st.write(event)
        
    with cols[1]:
        if event:
            st.header("   ")
            st.header("   ")
            if st.button("Download", key="download"):
                st.download_button(
                    label="",
                    data=event['target']['path'],
                    file_name=event['target']['path'],
                    mime="application/octet-stream",
                    on_click=None,
                    disabled=True,
                )
            root= current_path
            file = os.path.join(root, event['target']['path'])
            pdf_viewer(file, width="90%",height=800,render_text=True)
            # file= event['target']
            # artifacts_site= None
            # overide_preview_handles= None
            # height=2000
            # show_file_preview(root,file,artifacts_site,overide_preview_handles,height=height)
            
                    # st.download_button(pdf_name, pdf_file, file_name=pdf_path.split("/")[-1])
 