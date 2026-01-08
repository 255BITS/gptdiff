# GPTDiff Documentation

**Transform your codebase with natural language.** Describe what you want to change in plain English, and GPTDiff generates and applies the code modifications automatically—one command at a time, or continuously with agent loops.

```bash
pip install gptdiff
export GPTDIFF_LLM_API_KEY='your-key'

# Make changes with a single command
gptdiff "Add input validation to all form fields" --apply

# Or run continuously for autonomous improvement
while true; do gptdiff "Fix code quality issues" --apply; sleep 5; done
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

## Agent Loops: Autonomous Code Improvement

| Without Agent Loops | With Agent Loops |
|---------------------|------------------|
| Manual code reviews | Automated 24/7 scanning |
| Reactive bug fixes | Proactive issue detection |
| Weekend tech debt sprints | Continuous improvement |
| One change per prompt | Hundreds of changes overnight |

Run GPTDiff continuously for hands-off, iterative improvements:

```bash
while true; do
  gptdiff "Add missing test cases for edge conditions" --apply
  sleep 5
done
```

**Real Results:** One overnight run on a Python project:

| Metric | Before | After |
|--------|--------|-------|
| Test cases | 18 | 127 |
| Functions with tests | 12% | 71% |

**More Use Cases:** Security hardening, tech debt reduction, documentation sync—each loop cycle finds the next issue and fixes it automatically.

For detailed patterns and recipes, see the [Automation Guide](examples/automation.md).

---

## Documentation

| Guide | Description |
|-------|-------------|
| [Quickstart](quickstart.md) | Get running in 2 minutes |
| [Agent Loops](examples/automation.md) | Ship improvements overnight—one user went 18→127 tests |
| [Installation](installation.md) | Setup and configuration |
| [CLI Reference](cli.md) | All command-line options |
| [Python API](api.md) | Use GPTDiff in your Python code |
| [Core Concepts](concepts.md) | How GPTDiff works under the hood |
| [Troubleshooting](troubleshooting.md) | Common issues and solutions |

**Model Selection:** Different AI models work better for different tasks. See [Choosing a Model](https://github.com/255BITS/gptdiff#choosing-a-model) in the README for guidance.

---

## Links

- [GitHub Repository](https://github.com/255BITS/gptdiff) - Source code (MIT licensed)
- [PyPI Package](https://pypi.org/project/gptdiff/) - Install with pip
- Built with [AI Agent Toolbox](https://toolbox.255labs.xyz)
