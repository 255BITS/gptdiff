# GPTDiff
<!--
GPTDiff: Create and apply diffs using AI.
This tool leverages natural language instructions to modify project codebases.
-->

## Table of Contents

- [Quick Start](#quick-start)
- [Example Usage](#example-usage-of-gptdiff)
- [Basic Usage](#basic-usage)
- [Simple Command Line Agent Loops](#simple-command-line-agent-loops)
- [Why Choose GPTDiff?](#why-choose-gptdiff)
- [Core Capabilities](#core-capabilities)
  - [CLI Excellence](#-cli-excellence)
  - [Magic Diff Generation](#-magic-diff-generation)
  - [Smart Apply System](#-smart-apply-system)
- [Get Started](#get-started)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Command Line Usage](#command-line-usage)

🚀 **Create and apply diffs with AI**  
Modify your project using plain English.

More documentation at [gptdiff.255labs.xyz](https://gptdiff.255labs.xyz)

## Quick Start

1. **Install GPTDiff**
   
   
### Example Usage of `gptdiff`

#### Apply a Patch Directly
```bash
gptdiff "Add button animations on press" --apply
```
✅ Successfully applied patch

#### Generate a Patch File
```bash
gptdiff "Add API documentation" --call
```
🔧 Patch written to `diff.patch`

#### Generate a Prompt File Without Calling LLM
```bash
gptdiff "Improve error messages"
```
📄 LLM not called, written to `prompt.txt`

---

### Basic Usage

```bash
cd myproject
gptdiff 'add hover effects to the buttons'
```

Generates a prompt.txt file containing the full request.
Copy and paste its content into your preferred LLM (e.g., ChatGPT) for further experimentation.

### Simple command line agent loops

```bash
while
do
  gptdiff "Add missing test cases" --apply
done
```

*Requires reasoning model*

## Why Choose GPTDiff?

- **Describe changes in plain English**  
- **AI gets your whole project**  
- **Auto-fixes conflicts**  
- **Keeps code functional**  
- **Fast setup, no fuss**  
- **You approve every change**  
- **Costs are upfront**

## Core Capabilities

### ⚡ CLI Excellence
- **Target Specific Files** - Change just what you need
- **Live Updates** - See changes as they're made
- **Try Before Applying** - Test changes safely first
- **Clear Pricing** - Know costs upfront
- **Preview Changes** - See what will change with `--call`
- **Fix Mistakes** - Automatic error correction

### ✨ Magic Diff Generation
```bash
gptdiff "Convert class components to React hooks" --model deepseek-reasoner
```
- Full project context awareness
- Cross-file refactoring support
- Automatic conflict prevention

### 🧠 Smart Apply System

**Git-native Workflow:**
```bash
# 1. Apply AI-generated changes
gptdiff "Improve error handling" --apply

# 2. Review each change interactively
git add -p

# 3. Commit or discard
git commit -m "Enhanced error handling"
git reset --hard  # To undo all changes
```

```bash
gptdiff "Refactor authentication to use OAuth 2.0" --apply
```
<span style="color: #00ff00;">✅ Successfully applied complex changes across 5 files</span>

## Get Started

### Installation

Requires Python 3.8+. Install from PyPI:

```bash
pip install gptdiff
pip install tiktoken  # For token counting
```

Development install (no pip package yet)
```bash
python setup.py install
```

### Configuration

First sign up for an API key at https://nano-gpt.com/api and generate your key. Then configure your environment: 

#### Linux/MacOS
```bash
export GPTDIFF_LLM_API_KEY='your-api-key'
# Optional: For switching API providers
export GPTDIFF_MODEL='deepseek-reasoner'  # Set default model for all commands
export GPTDIFF_LLM_BASE_URL='https://nano-gpt.com/api/v1/'
```

#### Windows
```cmd
set GPTDIFF_LLM_API_KEY=your-api-key
rem Optional: For switching API providers 
set GPTDIFF_MODEL=deepseek-reasoner
set GPTDIFF_LLM_BASE_URL=https://nano-gpt.com/api/v1/
```

The default base URL points to nano-gpt.com's API. Supported models can be specified with:

```bash
gptdiff 'your prompt' --model deepseek-reasoner
# Default model can be set via GPTDIFF_MODEL environment variable
```

OpenAI will not be called unless you specify `--call` or `--apply`

Prevent files being appended to the prompt by adding them to `.gitignore` or `.gptignore`

## Command Line Usage

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

After installing the package, use the `gptdiff` command in your terminal. Change directory into your codebase and run:

```bash
gptdiff '<user_prompt>'
```

any files that are included in .gitignore are ignored when generating prompt.txt.

#### Specifying Additional Files

You may supply extra files or directories as arguments to the `gptdiff` command. If omitted, the tool defaults to the current working directory, excluding those matching ignore rules.

#### Autopatch Changes

You can also call openai and automatically apply the generated git diff with the `--apply` flag:

```bash
gptdiff '<user_prompt>' --apply
```

### Dry-Run Validation
Preview changes without applying them by omitting the `--apply` flag when using `--call`:
```bash
gptdiff "Modernize database queries" --call
```
<span style="color: #0066cc;">i️ Diff preview generated - review changes before applying</span>

This often generates incorrect diffs that need to be manually merged.

#### Smart Apply

For robust handling of complex changes, use `smartapply`. It processes each file’s diff individually via the LLM, ensuring nuanced conflict resolution.

## Completion Notification

Use the `--nobeep` option to disable the default completion beep:

```bash
gptdiff '<user_prompt>' --nobeep
```

## Local API Documentation

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