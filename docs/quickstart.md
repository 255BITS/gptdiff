# Quickstart Guide

Get GPTDiff running in under 2 minutes.

## Step 1: Install

```bash
pip install gptdiff
```

## Step 2: Configure

Get your API key from [nano-gpt.com/api](https://nano-gpt.com/api), then set it:

```bash
# Linux/macOS
export GPTDIFF_LLM_API_KEY='your-api-key'

# Windows
set GPTDIFF_LLM_API_KEY=your-api-key
```

## Step 3: Your First Transformation

Navigate to any project and describe the change you want:

```bash
cd your-project
gptdiff "Add type hints to all functions" --apply
```

**What happens:**
1. GPTDiff scans your project files (respecting `.gitignore`)
2. Sends the code + your instruction to an AI model
3. Receives a unified diff with the requested changes
4. Applies the diff to your files

**Expected output:**
```
Reading project files...
Generating diff with deepseek-reasoner...
Applying changes...
✅ Successfully applied patch to 3 files
```

**Tip:** The default model (`deepseek-reasoner`) is best for complex changes. For simple tasks, use a faster model:
```bash
gptdiff "Fix typos in comments" --model gemini-2.0-flash --apply
```

## Step 4: Review and Commit

GPTDiff modifies your files directly. Use Git to review and manage changes:

```bash
# See what changed
git diff

# Stage changes interactively (review each change)
git add -p

# Commit the changes you want
git commit -m "Add type hints"

# Or discard all changes if needed
git checkout .
```

## Three Usage Modes

| Command | Behavior | When to Use |
|---------|----------|-------------|
| `gptdiff "prompt"` | Creates `prompt.txt` only | Preview what will be sent to AI |
| `gptdiff "prompt" --call` | Creates `diff.patch` | Review diff before applying |
| `gptdiff "prompt" --apply` | Applies changes directly | Ready to modify files |

**Example: Preview before applying**
```bash
# First, generate and review the diff
gptdiff "Refactor to async/await" --call
cat diff.patch  # Review the changes

# If it looks good, apply it
gptpatch diff.patch
```

---

## Tips for Success

- **Start small**: Test with a focused change before attempting large refactors
- **Review first**: Use `--call` to preview changes before applying
- **Target specific files**: For large codebases, specify directories to reduce context:
  ```bash
  gptdiff "Add logging" src/api/ src/utils/
  ```
- **Expect timing variance**: Complex changes with `deepseek-reasoner` may take 30-60 seconds
- **Always review**: AI-generated code should be checked, especially for error handling and edge cases

---

## Next Steps

- See [basic examples](examples/basic.md) for common use cases
- Learn about [automation patterns](examples/automation.md)
- Read the full [CLI Reference](cli.md) for all options
- Use GPTDiff in Python with the [API Reference](api.md)
- Having issues? Check the [Troubleshooting Guide](troubleshooting.md)
