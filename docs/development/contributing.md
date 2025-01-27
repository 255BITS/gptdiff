# Contributing to GPTDiff

## Development Philosophy

**Core Principles:**
1. Changes should be utility driven
2. Command line and API usage resist change
3. Test where possible

## Development Setup

1. **Clone Repository**:
   ```bash
   git clone https://github.com/255BITS/gptdiff.git
   cd gptdiff
   ```

2. **Install Dependencies**:
   ```bash
   pip install -e .[test]
   ```

3. **Run Test Suite**:
   ```bash
   pytest tests/ --cov=gptdiff --cov-report=term-missing
   ```

## Contribution Workflow

1. **Create Feature Branch**:
   ```bash
   git checkout -b feat/new-feature
   ```
2. **Add Tests**:
3. **Update Documentation**:
   - Keep API reference current
   - Add examples for new features
4. **Submit Pull Request**:
   - Reference related issues
   - Include test coverage report
   - Document breaking changes

## Code Standards
- Try to get the LLMs to bootstrap the change.
- Don't hyperfocus on what the LLMs will soon be able to do.
