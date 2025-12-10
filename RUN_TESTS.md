# Running Tests for EduNavigator

## Quick Start

### 1. Install Test Dependencies

```bash
pip install pytest pytest-mock pytest-cov pytest-xdist
```

Or use the requirements file:

```bash
pip install -r requirements-test.txt
```

### 2. Run All Tests

```bash
pytest tests/ -v
```

### 3. Run with Coverage

```bash
pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
```

## Test Organization

### Test Files Created

- `tests/conftest.py` - Shared fixtures and mocks (129 lines)
- `tests/test_app.py` - Comprehensive test suite (716 lines)
- `tests/__init__.py` - Package initialization
- `pytest.ini` - Pytest configuration
- `requirements-test.txt` - Test dependencies

### Test Statistics

- **12 Test Classes** covering different aspects of the application
- **52 Test Methods** providing comprehensive coverage
- **5 Shared Fixtures** for consistent mocking

### Test Classes

1. `TestEnvironmentSetup` - Environment variable and Streamlit config
2. `TestLanguageModelInitialization` - LLM and prompt setup
3. `TestFAISSRetrieverLoading` - Vector store loading and error handling
4. `TestQueryProcessing` - Query flow and context retrieval
5. `TestErrorHandling` - Exception handling scenarios
6. `TestUIInteraction` - Streamlit UI components
7. `TestEdgeCases` - Boundary conditions and special inputs
8. `TestDataFlowIntegration` - End-to-end flow validation
9. `TestConfigurationValidation` - Configuration correctness
10. `TestSecurityConsiderations` - Security best practices
11. `TestPerformanceConsiderations` - Performance optimizations
12. `TestDiffSpecificChanges` - Validation of specific code changes

## Running Specific Tests

### By Test Class

```bash
pytest tests/test_app.py::TestEnvironmentSetup -v
pytest tests/test_app.py::TestQueryProcessing -v
pytest tests/test_app.py::TestErrorHandling -v
```

### By Test Method

```bash
pytest tests/test_app.py::TestEnvironmentSetup::test_openai_api_key_set_from_secrets -v
pytest tests/test_app.py::TestFAISSRetrieverLoading::test_all_retrievers_loaded_successfully -v
```

### By Pattern

```bash
pytest tests/ -k "test_error" -v
pytest tests/ -k "test_retriever" -v
pytest tests/ -k "test_context" -v
```

## Coverage Reports

### Generate HTML Coverage Report

```bash
pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html in your browser
```

### Terminal Coverage Report

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Coverage Badge

```bash
pytest tests/ --cov=app --cov-report=term | grep "TOTAL"
```

## Parallel Execution

For faster test execution:

```bash
pytest tests/ -n auto
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt -r requirements-test.txt
      - run: pytest tests/ --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## Test Fixtures

### Available Fixtures (from conftest.py)

1. **mock_streamlit** - Mocks all Streamlit UI components
2. **mock_openai** - Mocks ChatOpenAI and OpenAIEmbeddings
3. **mock_faiss** - Mocks FAISS vector store operations
4. **mock_langchain_components** - Mocks LangChain components
5. **clean_environment** - Ensures clean environment variables

## What's Being Tested

### The git diff showed changes to `app.py`:
- Removed errant "123" line after imports
- Removed trailing newline at end of file

### Comprehensive test coverage includes:

✅ **Environment Setup**
- API key configuration from Streamlit secrets
- Page configuration and branding
- Logo and title display

✅ **Component Initialization**
- ChatOpenAI with correct model (gpt-4o) and temperature (0)
- Prompt template structure
- Output parser initialization

✅ **Data Source Loading**
- FAISS index loading for 4 sources (YouTube, website, PDF, PPTX)
- Individual source failure handling
- Complete failure scenarios

✅ **Query Processing**
- Empty question validation
- Context retrieval from multiple sources
- Context length limitation (2000 chars/doc)
- Prompt formatting
- LLM invocation
- Answer display

✅ **Error Handling**
- API errors
- Retrieval failures
- Missing dependencies
- File not found scenarios

✅ **Edge Cases**
- Very long questions
- Special characters (XSS prevention)
- Unicode characters
- Whitespace-only input
- Empty results

✅ **Security**
- API keys not hardcoded
- Dangerous deserialization awareness

✅ **Performance**
- Context truncation for token management
- Proper operation ordering

## Troubleshooting

### Import Errors

If you get import errors, ensure you're running from the repository root:

```bash
cd /path/to/mychatbot
pytest tests/
```

### Mock Issues

If mocks aren't working, check that pytest-mock is installed:

```bash
pip install pytest-mock
```

### Coverage Not Working

Ensure pytest-cov is installed:

```bash
pip install pytest-cov
```

## Best Practices

1. **Run tests before committing**
   ```bash
   pytest tests/ -v
   ```

2. **Check coverage regularly**
   ```bash
   pytest tests/ --cov=app --cov-report=term-missing
   ```

3. **Add tests for new features**
   - Follow existing naming conventions
   - Use appropriate fixtures
   - Test both success and failure paths

4. **Keep tests fast**
   - Use mocks for external dependencies
   - Avoid actual API calls
   - Don't read/write files unnecessarily

5. **Write descriptive test names**
   - Clearly state what is being tested
   - Include expected behavior
   - Make failures easy to understand

## Expected Test Results

All 52 tests should pass when run against the current version of `app.py` (after the diff changes).

Example output: