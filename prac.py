import streamlit as st
import fitz
import os

file = st.file_uploader("Upload a file" , type="pdf")

if file:
    name , extension = os.path.splitext(file.name)
    

    final_string = ""
    doc = fitz.open(stream=file.read() , filetype="pdf")
    
    for pages in doc:
        final_string += pages.get_text()

    st.write(final_string)    