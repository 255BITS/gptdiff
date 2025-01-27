# Testing Philosophy & Practices

## Core Testing Principles

### **Attributes of a good test**
- Zero cross-test contamination
- Pure functions with no side effects
- Deterministic results across runs

## Key Test Categories

### File Operations
```python
# tests/test_smartapply.py
def test_smartapply_file_deletion():
    """Verify clean removal without residual artifacts"""
    # Tests deletion idempotency and missing file safety

def test_smartapply_new_file_creation():
    """Validate file initialization from diffs"""
    # Ensures proper handling of /dev/null sources
```

### Complex Modifications
```python
def test_smartapply_complex_single_hunk(mocker):
    """Test multi-line changes with context preservation"""
    # Validates LLM mock integration and structural understanding

**Example Mock Setup:**
```python
# Mock LLM response for predictable testing
mocker.patch('gptdiff.gptdiff.call_llm_for_apply',
    return_value="def new():\n    print('Updated')")

# Verify transformation
updated = smartapply(diff, original_files)
assert "Updated" in updated["file.py"]
```


## Running the Test Suite

```bash
# Install development dependencies
pip install -e .[test]

# Run all tests with coverage
pytest tests/ --cov=gptdiff --cov-report=term-missing

# Target specific test cases
pytest tests/test_smartapply.py -k "test_smartapply_file_modification"
```

## Writing New Tests

1. **Isolate Scenarios**: One logical case per test
2. **Mock LLM Responses**: Use `@patch` for deterministic outcomes
3. **Check Boundaries**: Empty files, invalid paths, encoding issues
