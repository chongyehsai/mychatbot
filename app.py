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

# Add a logo to the app
st.set_page_config(page_title="EduNavigator Q&A", page_icon="EduNavigator Logo.PNG")
col1, col2 = st.columns([1, 6])  # Adjust proportions to position the logo
with col1:
    st.image("EduNavigator Logo.PNG", use_column_width=True)  # Display the logo
with col2:
    st.title("LangChain LLM Q&A with Multiple Data Sources")  # Title beside the logo

# Initialize the language model and prompt template
llm = ChatOpenAI(model='gpt-4o')
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
    for source_name, folder_path in [
        ("youtube", "youtube"),
        ("website", "website"),
        ("pdf", "PDF"),
        ("pptx", "pptx"),
    ]:
        try:
            retrievers[source_name] = FAISS.load_local(
                folder_path=folder_path,
                embeddings=embeddings,
                allow_dangerous_deserialization=True
            ).as_retriever()
            st.write(f"Loaded {source_name} index successfully.")
        except Exception as e:
            st.write(f"Error loading {source_name} index:", e)
except Exception as e:
    st.write("Error initializing FAISS retrievers:", e)

# Form to handle "Enter to run"
with st.form("qa_form"):
    question = st.text_input("Ask me anything:")
    submitted = st.form_submit_button("Submit")  # Allows pressing "Enter" to trigger

if submitted:
    if question and retrievers:
        try:
            with st.spinner("Retrieving information..."):
                # Create a RunnableMap to handle retrieval from all sources
                retriever_map = RunnableMap(retrievers)

                # Retrieve context relevant to the question
                contexts = retriever_map.invoke(question)  # Pass `question` as a plain string
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
