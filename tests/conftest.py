"""
Shared pytest fixtures and configuration for testing the EduNavigator chatbot.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
import os


@pytest.fixture
def mock_streamlit():
    """Mock streamlit module to prevent actual UI rendering during tests."""
    with patch('app.st') as mock_st:
        # Mock secrets
        mock_st.secrets = {"OPENAI_API_KEY": "test-api-key-12345"}
        
        # Mock common streamlit functions
        mock_st.set_page_config = Mock()
        mock_st.columns = Mock(return_value=[Mock(), Mock()])
        mock_st.image = Mock()
        mock_st.title = Mock()
        mock_st.markdown = Mock()
        mock_st.text_input = Mock()
        mock_st.form_submit_button = Mock()
        mock_st.spinner = MagicMock()
        mock_st.write = Mock()
        mock_st.stop = Mock()
        mock_st.form = MagicMock()
        
        yield mock_st


@pytest.fixture
def mock_openai():
    """Mock OpenAI-related components."""
    with patch('app.ChatOpenAI') as mock_chat_openai, \
         patch('app.OpenAIEmbeddings') as mock_embeddings:
        
        # Mock ChatOpenAI instance
        mock_llm_instance = Mock()
        mock_response = Mock()
        mock_response.content = "This is a test answer from the LLM."
        mock_llm_instance.return_value = mock_response
        mock_chat_openai.return_value = mock_llm_instance
        
        # Mock OpenAIEmbeddings instance
        mock_embeddings_instance = Mock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        yield {
            'chat_openai': mock_chat_openai,
            'embeddings': mock_embeddings,
            'llm_instance': mock_llm_instance,
            'embeddings_instance': mock_embeddings_instance
        }


@pytest.fixture
def mock_faiss():
    """Mock FAISS vector store."""
    with patch('app.FAISS') as mock_faiss_class:
        # Create mock retriever
        mock_retriever = Mock()
        
        # Create mock document
        mock_doc = Mock()
        mock_doc.page_content = "This is test content from the knowledge base."
        mock_doc.metadata = {"source": "test_source"}
        
        # Mock retriever invoke to return documents
        mock_retriever.invoke = Mock(return_value=[mock_doc])
        
        # Mock FAISS load_local to return a mock vector store
        mock_vector_store = Mock()
        mock_vector_store.as_retriever = Mock(return_value=mock_retriever)
        mock_faiss_class.load_local = Mock(return_value=mock_vector_store)
        
        yield {
            'faiss_class': mock_faiss_class,
            'vector_store': mock_vector_store,
            'retriever': mock_retriever,
            'document': mock_doc
        }


@pytest.fixture
def mock_langchain_components():
    """Mock LangChain components."""
    with patch('app.StrOutputParser') as mock_parser, \
         patch('app.ChatPromptTemplate') as mock_prompt, \
         patch('app.RunnableMap') as mock_runnable_map:
        
        # Mock StrOutputParser
        mock_parser_instance = Mock()
        mock_parser.return_value = mock_parser_instance
        
        # Mock ChatPromptTemplate
        mock_prompt_instance = Mock()
        mock_prompt_instance.format = Mock(return_value="Formatted prompt")
        mock_prompt.from_template = Mock(return_value=mock_prompt_instance)
        
        # Mock RunnableMap
        mock_runnable_instance = Mock()
        mock_contexts = {
            'youtube': [Mock(page_content="YouTube content")],
            'website': [Mock(page_content="Website content")],
            'pdf': [Mock(page_content="PDF content")],
            'pptx': [Mock(page_content="PPTX content")]
        }
        mock_runnable_instance.invoke = Mock(return_value=mock_contexts)
        mock_runnable_map.return_value = mock_runnable_instance
        
        yield {
            'parser': mock_parser,
            'prompt': mock_prompt,
            'runnable_map': mock_runnable_map,
            'parser_instance': mock_parser_instance,
            'prompt_instance': mock_prompt_instance,
            'runnable_instance': mock_runnable_instance
        }


@pytest.fixture
def clean_environment():
    """Ensure clean environment variables for each test."""
    original_env = os.environ.copy()
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)