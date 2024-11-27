import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnableMap
import os

# Initialize environment variables
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Streamlit App Title
st.title("LangChain LLM Q&A with Multiple Data Sources")

# Initialize the language model and prompt template
llm = ChatOpenAI(model='gpt-3.5-turbo')
str_parser = StrOutputParser()
template = (
    "Please answer the questions based on the following content and your own judgment:\n"
    "{context}\n"
    "Question: {question}"
)
prompt = ChatPromptTemplate.from_template(template)

# Load FAISS indexes
retrievers = {}
try:
    embeddings = OpenAIEmbeddings()

    # Attempt to load FAISS databases for each data source
    try:
        retrievers['youtube'] = FAISS.load_local(
            folder_path="youtube",
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        ).as_retriever()
    except Exception as e:
        st.write("Error loading YouTube index:", e)

    try:
        retrievers['website'] = FAISS.load_local(
            folder_path="website",
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        ).as_retriever()
    except Exception as e:
        st.write("Error loading Website index:", e)

    try:
        retrievers['pdf'] = FAISS.load_local(
            folder_path="PDF",
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        ).as_retriever()
    except Exception as e:
        st.write("Error loading PDF index:", e)

    try:
        retrievers['pptx'] = FAISS.load_local(
            folder_path="pptx",
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        ).as_retriever()
    except Exception as e:
        st.write("Error loading PowerPoint index:", e)

    st.write("Loaded FAISS data sources successfully.")
except Exception as e:
    st.write("Error initializing FAISS indexes:", e)

# User input for the question
question = st.text_input("Ask me anything:")

# Process user input when button is clicked
if st.button("Get Answer"):
    if question and retrievers:
        try:
            with st.spinner("Retrieving information..."):
                # Create a RunnableMap to handle retrieval from all sources
                retriever_map = RunnableMap(retrievers)

                # Retrieve context relevant to the question
                contexts = retriever_map.invoke({"input": question})
                combined_contexts = "\n".join(
                    f"Source: {source}\n{data.page_content[:2000]}"  # Limit context length
                    for source, results in contexts.items()
                    for data in results
                )

                # Check if context is available
                if not combined_contexts.strip():
                    st.write("No relevant context found for your question.")
                    st.stop()

            with st.spinner("Generating answer..."):
                # Format the prompt and get an answer
                inputs = {"context": combined_contexts, "question": question}
                formatted_prompt = prompt.format(**inputs)
                answer = llm(formatted_prompt)

                # Display the answer
                st.write("Answer:", answer.content)
        except Exception as e:
            st.write("Error during retrieval or processing:", e)
    else:
        st.write("Please enter a question and ensure all retrievers are loaded.")
