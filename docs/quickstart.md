# Quickstart Guide

## Installation

```bash
pip install gptdiff
```

## Configuration

Set your API key:

```bash
export GPTDIFF_LLM_API_KEY='your-api-key'
```

## Your First Transformation

1. **Navigate to your project**:
   ```bash
   cd myproject
   cat "# A collection of useful linux commands: ..."
   ```

2. **Generate and smartapply a diff**:
   ```bash
   gptdiff "Add some useful linux commands" --apply
   ```

3. **Apply**:
   ```bash
   git add -p
   git commit
   ```

## Next Steps

- Explore [common recipes](/examples/recipes.md) for typical use cases
- Learn advanced patterns in the [Automation Guide](/examples/automation.md)
- Dive into the [API Reference](/api.md) for programmatic usage
