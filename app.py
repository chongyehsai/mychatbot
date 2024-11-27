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
llm = ChatOpenAI(model='gpt-4o')
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
retrievers = {}
try:
    embeddings = OpenAIEmbeddings()

    # Load FAISS databases for each data source
    retrievers['youtube'] = FAISS.load_local(
        folder_path="youtube",
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    ).as_retriever()
    retrievers['website'] = FAISS.load_local(
        folder_path="website",
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    ).as_retriever()
    retrievers['pdf'] = FAISS.load_local(
        folder_path="PDF",
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    ).as_retriever()
    retrievers['pptx'] = FAISS.load_local(
        folder_path="pptx",
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    ).as_retriever()

    st.write("Loaded FAISS data sources successfully.")
except Exception as e:
    st.write("Error loading FAISS indexes:", e)

# Process user input when button is clicked
if st.button("Get Answer"):
    if question and retrievers:
        try:
            # Create a RunnableMap to handle retrieval from all sources
            retriever_map = RunnableMap(retrievers)
            
            # Retrieve context relevant to the question
            contexts = retriever_map.invoke({"input": question})
            combined_contexts = "\n".join([f"Source: {source}\n{data.page_content}" 
                                           for source, results in contexts.items() 
                                           for data in results])
            
            # Format and retrieve the answer from the LLM
            inputs = {"context": combined_contexts, "question": question}
            answer = llm(prompt.format(**inputs))
            
            # Display the answer
            st.write("Answer:", answer.content)
        except Exception as e:
            st.write("Error during retrieval or processing:", e)
    else:
        st.write("Please enter a question and ensure all retrievers are loaded.")
