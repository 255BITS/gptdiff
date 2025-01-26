# Quickstart Guide

## Installation

```bash
pip install gptdiff
```

## Configuration

Set your API key:

```bash
export NANOGPT_API_KEY='your-api-key'
```

## Your First Transformation

1. **Navigate to your project**:
   ```bash
   cd myproject
   ```

2. **Generate a diff**:
   ```bash
   gptdiff "Add type hints to functions" --call > type_hints.patch
   ```

3. **Review changes**:
   ```bash
   git apply --stat type_hints.patch
   ```

4. **Apply safely**:
   ```bash
   gptdiff "Add type hints to functions" --apply
   ```

## Next Steps

- Explore [common recipes](/examples/recipes.md) for typical use cases
- Learn advanced patterns in the [Automation Guide](/examples/automation.md)
- Dive into the [API Reference](/api.md) for programmatic usage

<div class="toolbox-note">💡 Pro Tip: Start with small changes and use <code>--call</code> to preview before applying!</div>
