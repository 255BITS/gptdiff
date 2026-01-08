# GPTDiff

**Transform your codebase with natural language.** GPTDiff lets you describe code changes in plain English and automatically generates and applies the diffs for you—one command at a time, or continuously with agent loops.

```bash
# Install and configure
pip install gptdiff
export GPTDIFF_LLM_API_KEY='your-api-key'  # Get one at https://nano-gpt.com/api

# Make changes with a single command
gptdiff "Add input validation to all form fields" --apply

# Or run continuously for autonomous improvement
while true; do gptdiff "Fix code quality issues" --apply; sleep 5; done
```

That's it. GPTDiff reads your entire project, understands the context, generates a unified diff, and applies it. Run it once for quick changes, or loop it for hands-off continuous improvement.

📚 Full documentation at [gptdiff.255labs.xyz](https://gptdiff.255labs.xyz)

---

## Quick Start

### Step 1: Install

```bash
pip install gptdiff
```

### Step 2: Set Your API Key

```bash
# Linux/macOS
export GPTDIFF_LLM_API_KEY='your-api-key'

# Windows
set GPTDIFF_LLM_API_KEY=your-api-key
```

Get your API key at [nano-gpt.com/api](https://nano-gpt.com/api).

### Step 3: Run Your First Command

Navigate to any project directory and describe what you want to change:

```bash
cd your-project
gptdiff "Add type hints to all functions" --apply
```

**What happens:**
1. GPTDiff scans your codebase (respecting `.gitignore`)
2. Sends context + your instruction to an AI model
3. Receives a unified diff
4. Applies the changes to your files

### Three Ways to Use GPTDiff

| Command | What It Does | When to Use |
|---------|--------------|-------------|
| `gptdiff "prompt"` | Generates `prompt.txt` only | Preview what will be sent to the LLM |
| `gptdiff "prompt" --call` | Generates diff, saves to `diff.patch` | Review changes before applying |
| `gptdiff "prompt" --apply` | Generates and applies diff automatically | When you're ready to make changes |

**Examples:**

```bash
# Just generate the prompt (no API call)
gptdiff "Improve error messages"
# → Creates prompt.txt - useful for manual LLM experimentation

# Generate diff but don't apply it
gptdiff "Add API documentation" --call
# → Creates diff.patch - review before applying

# Generate and apply in one step
gptdiff "Add button animations on press" --apply
# → Changes applied directly to your files
```

---

## See It In Action

GPTDiff doesn't just run commands—it transforms your code. Here are real before/after examples:

### Example 1: Add Type Hints

**Command:**
```bash
gptdiff "Add type hints to all functions" --apply
```

**Before:**
```python
def calculate_total(items, tax_rate):
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    return subtotal * (1 + tax_rate)

def format_currency(amount):
    return f"${amount:.2f}"
```

**After:**
```python
def calculate_total(items: list[dict], tax_rate: float) -> float:
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    return subtotal * (1 + tax_rate)

def format_currency(amount: float) -> str:
    return f"${amount:.2f}"
```

### Example 2: Add Error Handling

**Command:**
```bash
gptdiff "Add try/except blocks with proper error messages to all file operations" --apply
```

**Before:**
```python
def read_config(path):
    with open(path) as f:
        return json.load(f)
```

**After:**
```python
def read_config(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise ConfigError(f"Configuration file not found: {path}")
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in config file {path}: {e}")
```

### Example 3: Refactor Across Multiple Files

**Command:**
```bash
gptdiff "Rename the User class to Account and update all imports and references" --apply
```

**Before (models/user.py):**
```python
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
```

**Before (services/auth.py):**
```python
from models.user import User

def get_current_user() -> User:
    return User("John", "john@example.com")
```

**After (models/account.py):** *(file renamed)*
```python
class Account:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
```

**After (services/auth.py):**
```python
from models.account import Account

def get_current_user() -> Account:
    return Account("John", "john@example.com")
```

GPTDiff understands your entire codebase—it updates class definitions, imports, type hints, and references across all files in one operation.

---

## Why Choose GPTDiff?

| Feature | Benefit |
|---------|---------|
| **Agent loops** | Ship improvements while you sleep—one loop took tests from 18 to 127 overnight |
| **Plain English instructions** | No need to learn complex refactoring tools |
| **Full project context** | AI sees all your files, understands relationships |
| **Smart conflict resolution** | Handles merge conflicts automatically |
| **Git-native workflow** | Review changes with `git diff`, undo with `git checkout` |
| **You control everything** | Preview with `--call`, apply only when ready |

## Agent Loops: Continuous Code Improvement

Run GPTDiff in a loop for autonomous, iterative improvements to your codebase:

```bash
# Copy-paste this and run tonight:
while true; do
  gptdiff "Add missing test cases for edge conditions" --apply
  git add -A && git commit -m "Auto-improvement $(date +%H:%M)" 2>/dev/null
  sleep 30
done
```

Each improvement auto-commits with a timestamp, giving you a clean history to review in the morning.

**Real Results:** One test coverage loop running overnight:

| Metric | Before | After |
|--------|--------|-------|
| Test files | 3 | 14 |
| Test cases | 18 | 127 |
| Functions with tests | 12% | 71% |

**What else Agent Loops can do:**

| Use Case | Example Prompt |
|----------|----------------|
| **Security Hardening** | "Find and fix OWASP Top 10 vulnerabilities" |
| **Tech Debt Reduction** | "Refactor functions with high complexity scores" |
| **Documentation Sync** | "Update documentation to match current implementation" |

Each cycle analyzes your code, generates targeted improvements, and applies them—building better software automatically.

For detailed automation recipes, see the [Automation Guide](https://gptdiff.255labs.xyz/examples/automation).

---

## Choosing a Model

Different AI models have different strengths. **Reasoning models** produce more accurate results for complex refactoring but take longer. **Fast models** are better for simple, straightforward changes.

| Model | Best For | Speed | Notes |
|-------|----------|-------|-------|
| `gemini-3-pro-preview` | General code changes, refactoring | Fast | **Recommended default** - great balance |
| `gpt-4o` | Complex multi-file changes | Medium | Reliable for most tasks |
| `claude-sonnet-4-20250514` | Nuanced code understanding | Medium | Great for context-sensitive changes |
| `gemini-2.0-flash` | Simple text changes, translations | Very fast | Most cost-effective option |
| `gpt5-mini` | Applying diffs (smartapply) | Very fast | Best for `GPTDIFF_SMARTAPPLY_MODEL` |

**Quick rule:** Use `gemini-3-pro-preview` as your default. For applying diffs, set `gpt5-mini` as your smartapply model.

```bash
# Recommended setup
export GPTDIFF_MODEL='gemini-3-pro-preview'
export GPTDIFF_SMARTAPPLY_MODEL='gpt5-mini'

# Use a specific model for one command
gptdiff "Convert callbacks to async/await" --model gpt-4o
```

---

## Advanced Configuration

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `GPTDIFF_LLM_API_KEY` | Your API key (required) | - |
| `GPTDIFF_MODEL` | Model for diff generation | `gemini-3-pro-preview` |
| `GPTDIFF_SMARTAPPLY_MODEL` | Model for applying diffs | `gpt5-mini` |
| `GPTDIFF_LLM_BASE_URL` | API endpoint | `https://nano-gpt.com/api/v1/` |

### Excluding Files

Prevent files from being sent to the LLM by adding them to `.gitignore` or `.gptignore`:

```bash
# .gptignore example
*.env
secrets/
node_modules/
```

---

## gptpatch: Apply Diffs Directly

`gptpatch` is a companion command-line tool to [GPTDiff](https://github.com/255BITS/gptdiff) that applies unified diffs directly to your project.

### Usage

Apply a diff provided directly:

```bash
gptpatch --diff "<diff text>"
```

Or apply a diff from a file:

```bash
gptpatch path/to/diff.patch
```

### Options

- **--project-dir**: Specify the target project directory (default: current directory)
- **--model**: (Optional) Specify the LLM model for advanced conflict resolution
- **--max_tokens**: (Optional) Define the maximum token count for LLM responses during patch application
- **--nobeep**: Disable the completion beep notification

### Workflow

`gptpatch` first attempts to apply the diff using standard patch logic. If that fails, it automatically falls back to a smart apply mechanism that leverages AI-powered conflict resolution.

For more details, see the [gptpatch documentation](https://gptdiff.255labs.xyz) on our docs site.

---

## CLI Options Reference

| Option | Description |
|--------|-------------|
| `--apply` | Generate diff and apply it automatically |
| `--call` | Generate diff and save to `diff.patch` (for review) |
| `--model <name>` | Specify which LLM to use |
| `--temperature <0-2>` | Control creativity (default: 0.7) |
| `--nobeep` | Disable completion notification sound |
| `--prepend <file>` | Prepend custom instructions to the prompt |
| `--image <path>` | Include images for visual context |

**Target specific files:**
```bash
gptdiff "Add logging" src/api/ src/utils/helpers.py
```

For the complete CLI reference, see [cli.md](https://gptdiff.255labs.xyz/cli).

---

## Documentation

Preview API docs locally using MkDocs:

```bash
pip install .[docs]
mkdocs serve
```
Open http://localhost:8000 to view the documentation

## Python API

Integrate GPTDiff directly into your Python workflows:

```python
from gptdiff import generate_diff, smartapply
import os

os.environ['GPTDIFF_LLM_API_KEY'] = 'your-api-key'

# Create files dictionary
files = {"main.py": "def old_name():\n    print('Need renaming')"}

# Generate transformation diff using an environment string built from the files dictionary
environment = ""
for path, content in files.items():
    environment += f"File: {path}\nContent:\n{content}\n"

diff = generate_diff(
    environment=environment,
    goal='Rename function to new_name()',
    model='deepseek-reasoner'
)

# Apply changes safely using the files dict
updated_files = smartapply(diff, files)

print("Transformed codebase:")
print(updated_files["main.py"])
```

**Batch Processing Example:**
```python
from gptdiff import generate_diff, smartapply

files = load_your_codebase()  # Dict of {path: content}

transformations = [
    "Add python type annotations",
    "Convert string formatting to f-strings",
    "Update deprecated API calls"
]

for task in transformations:
    files = smartapply(generate_diff(build_environment(files), task), files)
```

**Integration Note:** GPTDiff leverages the [AI Agent Toolbox](https://github.com/255BITS/ai-agent-toolbox) for seamless tool usage across AI models and frameworks, making it ideal for both single responses and complex agent workflows.

### Core Functions

- `generate_diff(environment: str, goal: str, model: str) -> str`  
  Generates a git diff implementing the requested changes
  
  *`model` parameter defaults to `GPTDIFF_MODEL` environment variable*
- `smartapply(diff_text: str, environment_str: str, model: str) -> str`  
  Applies complex diffs while preserving file context

## Testing

To run the test suite:

```bash
pip install -e .[test]
pytest tests/
```

This will execute all unit tests verifying core diff generation and application logic.

### plangptdiff: Generate *plan* prompts that call GPTDiff

`plangptdiff` scans your repo with **ripgrep**, selects only the files likely to
change (always including anything named *schema*), and writes a ready‑to‑paste
prompt to **planprompt.txt**:

```bash
# Prompt only
plangptdiff "add validation to the signup form"

# Prompt that will auto‑apply the diff
plangptdiff "upgrade to Django 5" --apply
```

The file list is appended to the generated `gptdiff` command so the LLM sees
only the files that matter, keeping prompts lean and costs down.