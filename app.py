import streamlit as st
from agents import agent
import chromadb
import os
import fitz
from io import StringIO
from tools import gemini_client

chromadb_client = chromadb.Client()

if "collection" not in st.session_state:
    st.session_state.collection = chromadb_client.get_or_create_collection(name="my_docs")

if "processed" not in st.session_state:
    st.session_state.processed = False

if "messages" not in st.session_state:
    st.session_state.messages = []


file = st.file_uploader("Upload a document" , max_upload_size=10 , type=("pdf" , "txt"))

def extract_text(file):
            name , extension = os.path.splitext(file.name)

            if extension == ".pdf":
                final_string = ""
                doc = fitz.open(stream=file.read() , filetype="pdf")

                for pages in doc:
                    final_string += pages.get_text()

                return final_string

            elif extension == ".txt":
                stringio = StringIO(file.getvalue().decode("utf-8"))
                text_file_text = stringio.read()
                return text_file_text

def create_chunk(text):
            
            chunks = [text[i : i + 150] for i in range(0 , len(text) , 150 - 30)]
            return chunks

def generate_embeddings(chunks):
            result = gemini_client.models.embed_content(
                model="gemini-embedding-001",
                contents=chunks
            )

            embeddings = []

            for value in result.embeddings:
                embeddings.append(value.values)
            
            return embeddings
        
def adding_embedding_in_collection(chunks , embeddings):
            st.session_state.collection.add(
                embeddings=embeddings,
                documents=chunks,
                ids= [f"chunk{i}" for i in range(len(chunks))]
            )
        

with st.spinner("processing document....."):
    if file and not st.session_state.processed:
        
        text = extract_text(file)

        chunks = create_chunk(text)
        
        embeddings = generate_embeddings(chunks)

        adding_embedding_in_collection(chunks , embeddings)

        st.session_state.processed = True
        st.success("document is ready ")

if st.session_state.processed :

    que = st.chat_input("Ask a Question : ")

    if que:
        with st.spinner("processing...."):
            st.session_state.messages.append({"role" : "user" , "content" : que})
            response = agent(que , st.session_state.collection)

            st.session_state.messages.append({"role" : "assistant" , "content" : response})
            
            if "output.pdf" in response:
                  with open("output.pdf" , "rb") as file:
                        text = file.read()
                
                  st.download_button(
                        label="Download PDF",
                        data=text,
                        file_name="output.pdf"
                  )

    for message in st.session_state.messages:
          with st.chat_message(message["role"]):
                st.write(message["content"])
    




          
                
                





