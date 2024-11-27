import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnableMap, RunnablePassthrough
import os

# Initialize environment variables
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Initialize the language model and prompt template
llm = ChatOpenAI(model='gpt-3.5-turbo')
str_parser = StrOutputParser()
template = (
    "Please answer the questions based on the following content and your own judgment:\n"
    "{context}\n"
    "Question: {question}"
)
prompt = ChatPromptTemplate.from_template(template)

# Streamlit App
st.title("LangChain LLM Q&A with Multiple Data Sources")

# User input for the question
question = st.text_input("Ask me anything:")

# Load FAISS indexes
try:
    embeddings = OpenAIEmbeddings()

    # Load FAISS databases for each data source
    youtube_retriever = FAISS.load_local(
        folder_path="youtube",
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    ).as_retriever()
    website_retriever = FAISS.load_local(
        folder_path="website",
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    ).as_retriever()
    pdf_retriever = FAISS.load_local(
        folder_path="PDF",
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    ).as_retriever()
    pptx_retriever = FAISS.load_local(
        folder_path="pptx",
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    ).as_retriever()

    st.write("Loaded FAISS data sources successfully.")
except Exception as e:
    st.write("Error loading FAISS indexes:", e)

# Create retriever map and chain
retriever_map = RunnableMap({
    "youtube": youtube_retriever,
    "website": website_retriever,
    "pdf": pdf_retriever,
    "pptx": pptx_retriever,
})

chain = (
    {"context": retriever_map, "question": RunnablePassthrough()}
    | prompt
    | llm
    | str_parser
)

# Process user input when button is clicked
if st.button("Get Answer"):
    if question:
        try:
            # Run the chain to retrieve and answer the question
            result = chain.invoke({"context": question})
            
            # Display the answer
            st.write("Answer:", result)
        except Exception as e:
            st.write("Error during retrieval or processing:", e)
    else:
        st.write("Please enter a question.")
