import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Initialize the language model
llm = ChatOpenAI(model="gpt-4", max_tokens=100)

# Define prompt template
template = (
    "Please answer the questions based on the following content and your own judgment:\n"
    "{context}\n"
    "Question: {question}"
)
prompt = ChatPromptTemplate.from_template(template)

# Streamlit App
st.title("LangChain LLM Q&A")

# User input for the question
question = st.text_input("Ask me anything:")

# Load FAISS index
try:
    # Load pre-indexed FAISS database
    db_pdf = FAISS.load_local("Database/PDF", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    pdf_retriever = db_pdf.as_retriever()
    st.write("Loaded pre-indexed FAISS data successfully.")
except Exception as e:
    pdf_retriever = None
    st.write("Error loading FAISS index:", e)

# Process user input when button is clicked
if st.button("Get Answer"):
    if question and pdf_retriever:
        # Retrieve context relevant to the question
        retrieved_docs = pdf_retriever.get_relevant_documents(question)
        context_texts = "\n".join([doc.page_content for doc in retrieved_docs])

        # Format inputs and retrieve the answer from the LLM
        inputs = {"context": context_texts, "question": question}
        response = llm(prompt.format(**inputs))

        # Extract and display only the 'content' field
        content = response.get("content", "No content found.")
        st.write("Content:", content)
    elif not question:
        st.write("Please enter a question.")
    else:
        st.write("PDF Retriever not available. Check FAISS index loading.")
