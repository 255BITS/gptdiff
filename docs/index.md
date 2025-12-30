# GPTDiff Documentation

**Transform your codebase with natural language.** Describe what you want to change in plain English, and GPTDiff generates and applies the code modifications automatically.

```bash
pip install gptdiff
export GPTDIFF_LLM_API_KEY='your-key'
gptdiff "Add input validation to all form fields" --apply
```

---

## What is GPTDiff?

GPTDiff is a command-line tool that uses AI to modify your code. Instead of manually editing files, you describe the change you want, and GPTDiff:

1. **Reads your codebase** - Understands your project structure and code
2. **Generates a diff** - Creates a unified diff implementing your request
3. **Applies changes** - Uses smart patching to modify your files

It works with any programming language and integrates seamlessly with Git.

---

## See It Work

**Command:**
```bash
gptdiff "Add error handling to database queries" --apply
```

**Before:**
```python
def get_user(user_id):
    result = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    return result.fetchone()
```

**After:**
```python
def get_user(user_id):
    try:
        result = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        return result.fetchone()
    except DatabaseError as e:
        logger.error(f"Failed to fetch user {user_id}: {e}")
        raise UserNotFoundError(f"Could not retrieve user {user_id}") from e
```

---

## Three Ways to Use GPTDiff

| Command | What It Does | Use Case |
|---------|--------------|----------|
| `gptdiff "prompt"` | Generates prompt.txt only | Preview what will be sent to the AI |
| `gptdiff "prompt" --call` | Generates diff.patch | Review changes before applying |
| `gptdiff "prompt" --apply` | Generates and applies diff | Ready to make changes |

---

## Quick Start

### 1. Install

```bash
pip install gptdiff
```

### 2. Configure

Get an API key from [nano-gpt.com/api](https://nano-gpt.com/api), then:

```bash
# Linux/macOS
export GPTDIFF_LLM_API_KEY='your-api-key'

# Windows
set GPTDIFF_LLM_API_KEY=your-api-key
```

### 3. Use

```bash
cd your-project
gptdiff "Add type hints to all functions" --apply
```

For detailed setup instructions, see the [Installation Guide](installation.md).

---

## Git-Native Workflow

GPTDiff fits naturally into your Git workflow:

```bash
# 1. Make AI-powered changes
gptdiff "Refactor authentication to use JWT" --apply

# 2. Review what changed
git diff

# 3. Stage changes you want to keep
git add -p

# 4. Commit or discard
git commit -m "Refactor auth to JWT"
git checkout .  # Undo unwanted changes
```

---

## Documentation

| Guide | Description |
|-------|-------------|
| [Quickstart](quickstart.md) | Get running in 2 minutes |
| [Installation](installation.md) | Setup and configuration |
| [CLI Reference](cli.md) | All command-line options |
| [Python API](api.md) | Use GPTDiff in your Python code |
| [Core Concepts](concepts.md) | How GPTDiff works under the hood |
| [Troubleshooting](troubleshooting.md) | Common issues and solutions |

**Model Selection:** Different AI models work better for different tasks. See [Choosing a Model](https://github.com/255BITS/gptdiff#choosing-a-model) in the README for guidance.

---

## Agent Loops

Run GPTDiff continuously for iterative improvements:

```bash
while true; do
  gptdiff "Add missing test cases" --apply
  sleep 5
done
```

*Works best with capable models like `gemini-3-pro-preview` or `gpt-4o`.*

---

## Links

- [GitHub Repository](https://github.com/255BITS/gptdiff) - Source code (MIT licensed)
- [PyPI Package](https://pypi.org/project/gptdiff/) - Install with pip
- Built with [AI Agent Toolbox](https://toolbox.255labs.xyz)
