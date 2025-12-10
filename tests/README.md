# EduNavigator Test Suite

This directory contains comprehensive unit tests for the EduNavigator chatbot application.

## Test Coverage

The test suite covers:

1. **Environment Setup** (`TestEnvironmentSetup`)
   - OpenAI API key configuration
   - Streamlit page configuration
   - Logo and title display
   - Welcome message rendering

2. **Language Model Initialization** (`TestLanguageModelInitialization`)
   - ChatOpenAI initialization with correct parameters
   - Prompt template creation and structure
   - Output parser initialization

3. **FAISS Retriever Loading** (`TestFAISSRetrieverLoading`)
   - Successful loading of all data sources (YouTube, website, PDF, PPTX)
   - Proper embedding integration
   - Individual and complete failure handling
   - Dangerous deserialization flag

4. **Query Processing** (`TestQueryProcessing`)
   - Empty question handling
   - Context retrieval from multiple sources
   - Context length limitation (2000 chars per document)
   - Empty context detection
   - Prompt formatting
   - LLM invocation
   - Answer display

5. **Error Handling** (`TestErrorHandling`)
   - Retrieval errors
   - LLM API errors
   - Embedding initialization failures
   - Missing API keys
   - File not found scenarios

6. **UI Interaction** (`TestUIInteraction`)
   - Form creation and submission
   - Input field configuration
   - Spinner display during processing
   - User feedback messages

7. **Edge Cases** (`TestEdgeCases`)
   - Very long questions
   - Special characters and XSS prevention
   - Unicode character handling
   - Whitespace-only input
   - Single retriever availability
   - Empty retrieval results

8. **Data Flow Integration** (`TestDataFlowIntegration`)
   - Complete query flow from input to output
   - Multiple documents per source
   - Source labeling in context

9. **Configuration Validation** (`TestConfigurationValidation`)
   - Correct model name (gpt-4o)
   - Temperature setting (0 for deterministic output)
   - All data source folders defined
   - Page title and icon configuration

10. **Security Considerations** (`TestSecurityConsiderations`)
    - API key not hardcoded
    - Dangerous deserialization awareness

11. **Performance Considerations** (`TestPerformanceConsiderations`)
    - Context truncation for token management
    - Proper operation ordering

12. **Diff-Specific Changes** (`TestDiffSpecificChanges`)
    - Validation that errant '123' was removed
    - Clean imports section
    - No excessive trailing newlines

## Running the Tests

### Prerequisites

Install test dependencies:

```bash
pip install -r requirements.txt
pip install pytest pytest-mock pytest-cov
```

### Run All Tests

```bash
pytest tests/
```

### Run with Coverage Report

```bash
pytest tests/ --cov=app --cov-report=html --cov-report=term
```

### Run Specific Test Class

```bash
pytest tests/test_app.py::TestEnvironmentSetup -v
```

### Run Specific Test

```bash
pytest tests/test_app.py::TestEnvironmentSetup::test_openai_api_key_set_from_secrets -v
```

### Run with Verbose Output

```bash
pytest tests/ -v
```

### Run Tests in Parallel

```bash
pip install pytest-xdist
pytest tests/ -n auto
```

## Test Structure

- `conftest.py`: Shared fixtures and mock configurations
  - `mock_streamlit`: Mocks Streamlit UI components
  - `mock_openai`: Mocks OpenAI ChatGPT and Embeddings
  - `mock_faiss`: Mocks FAISS vector store operations
  - `mock_langchain_components`: Mocks LangChain components
  - `clean_environment`: Ensures clean environment variables

- `test_app.py`: Comprehensive test suite with 60+ test cases

## Mocking Strategy

The tests use extensive mocking to:
- Avoid actual API calls to OpenAI (cost and rate limits)
- Prevent UI rendering during tests (Streamlit)
- Isolate component behavior (FAISS, LangChain)
- Ensure fast, reliable test execution
- Test error conditions safely

## Best Practices

1. **Isolation**: Each test is independent and doesn't affect others
2. **Mocking**: External dependencies are mocked to prevent side effects
3. **Descriptive Names**: Test names clearly describe what is being tested
4. **Comprehensive Coverage**: Happy paths, edge cases, and error conditions
5. **Fast Execution**: Tests run quickly without external dependencies
6. **Maintainability**: Clear structure and documentation

## Continuous Integration

These tests are designed to run in CI/CD pipelines. They:
- Don't require external services
- Don't need API keys (mocked)
- Don't need data files (mocked)
- Run quickly and reliably
- Provide clear failure messages

## Contributing

When adding new features to `app.py`:

1. Add corresponding tests to appropriate test class
2. Follow existing naming conventions
3. Mock external dependencies
4. Test both success and failure scenarios
5. Run full test suite before committing
6. Ensure coverage remains high (aim for >80%)

## Known Limitations

- Tests mock Streamlit UI, so visual aspects aren't validated
- FAISS vector store behavior is mocked, not tested with real data
- OpenAI API responses are mocked, not validated against actual API
- File system operations (logo loading) are partially mocked

For integration testing with real data and APIs, see the integration test suite (if available).