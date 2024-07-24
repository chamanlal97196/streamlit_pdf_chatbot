import streamlit as st
import requests
import PyPDF2
import os
from dotenv import load_dotenv


load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
HF_API_URL = os.getenv("HF_API_URL")


headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


st.title("PDF Chatbot")

st.sidebar.header("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("Text extracted from PDF!")

    
    if st.checkbox("Show Extracted Text"):
        st.write(pdf_text)

    
    query = st.text_input("Ask a question about the PDF content:")

    if st.button("Get Answer"):
        if query:
            
            input_data = {
                "context": pdf_text,
                "question": query
            }

            
            try:
                with st.spinner("Querying the model..."):
                    response = requests.post(
                        HF_API_URL,
                        headers=headers,
                        json=input_data
                    )

                    if response.status_code != 200:
                        st.error(f"Error: {response.json()}")
                    else:
                        result = response.json()
                        
                        answer = result.get('answer', 'No answer found.')
                        st.success("Answer:")
                        st.write(answer.strip())

            except Exception as e:
                st.error(f"Request failed: {str(e)}")
        else:
            st.warning("Please enter a question.")
else:
    st.info("Please upload a PDF file to get started.")
