import os
import streamlit as st
from doc_chat_utulity import get_answer

working_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Chat with Doc",
    layout="centered"
)

st.title("UnderWriting AI PDF Reader")

uploaded_file = st.file_uploader(label="Upload your pdf", type=["pdf"])

user_query = st.text_input("Ask your question")

if st.button("Run"):
    bytes_data = uploaded_file.read()
    file_name = uploaded_file.name

    #the purpose is to save the file
    file_path  = os.path.join(working_dir, file_name)
    with open(file_path,"wb") as f:
        f.write(bytes_data)
    answer = get_answer(file_name, user_query)

    st.success(answer)