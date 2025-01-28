# GPTDiff

🚀 **AI-Powered Code Evolution** - Transform your codebase with natural language instructions

```bash
cd myproject
gptdiff 'add hover effects to the buttons'
```

Generates a prompt.txt file that you can copy and paste into a large context gpt to have a conversation with suggested changes. You can also invoke the API and try to directly apply the patch using a smartapply if the git apply fails.

## Value Proposition

```bash
gptdiff "Update the readme with an api section" --apply
```
<span style="color: #00ff00;">Patch applied successfully.</span>

### Why GPTDiff?

- **Understands Your Code** - Describe changes in plain English
- **Safe Modifications** - Keeps existing code working
- **Auto-Fix** - `--apply` fixes mistakes in generated changes
- **Works Instantly** - No complex setup needed
- **Whole Project View** - Handles multiple files together

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
export GPTDIFF_LLM_BASE_URL='https://nano-gpt.com/api/v1/
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

### Command Line Usage

After installing the package, you can use the `gptdiff` command in your terminal. cd into your codebase and run:

```bash
gptdiff '<user_prompt>'
```

any files that are included in .gitignore are ignored when generating prompt.txt.

#### Specifying Additional Files

You can specify additional files or directories to include in the prompt by adding them as arguments to the `gptdiff` command. If no additional files or directories are specified, the tool will default to using the current working directory.

Example usage:

```bash
gptdiff 'make this change' src test
```

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
<span style="color: #0066cc;">ℹ️ Diff preview generated - review changes before applying</span>

This often generates incorrect diffs that need to be manually merged.

#### Smart Apply

For more reliable patching of complex changes, use `smartapply` which processes each file's diff individually with the LLM:

```bash
gptdiff 'refactor authentication system' --apply
```

### Completion Notification

Use the `--nobeep` option to disable the default completion beep:

```bash
gptdiff '<user_prompt>' --beep
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

# Create environment representation
environment = '''
File: main.py
Content:
def old_name():
    print("Need renaming")
'''

# Generate transformation diff
diff = generate_diff(
    environment=environment,
    goal='Rename function to new_name()',
    model='deepseek-reasoner'
)

# Apply changes safely
updated_environment = smartapply(
    diff_text=diff,
    environment_str=environment
)

print("Transformed codebase:")
print(updated_environment)
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