# GPTDiff

## AI-Powered Code Transformations

```bash
cd myproject
gptdiff 'add hover effects to the buttons'
```

Generates a prompt.txt file that you can copy and paste into a large context gpt to have a conversation with suggested changes. You can also invoke the API and try to directly apply the patch (this often doesn't work).
  
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
export NANOGPT_API_KEY='your-api-key'
# Optional: For switching API providers
export NANOGPT_BASE_URL='https://nano-gpt.com/api/v1/'
```

#### Windows
```cmd
set NANOGPT_API_KEY=your-api-key
rem Optional: For switching API providers
set NANOGPT_BASE_URL=https://nano-gpt.com/api/v1/
```

The default base URL points to nano-gpt.com's API. Supported models can be specified with:

```bash
gptdiff 'your prompt' --model deepseek-reasoner
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

This often generates incorrect diffs that need to be manually merged.


#### Smart Apply

For more reliable patching of complex changes, use `--smartapply` which processes each file's diff individually with the LLM:

```bash
gptdiff 'refactor authentication system' --smartapply
```

## Python API

Integrate GPTDiff directly into your Python workflows:

```python
from gptdiff import generate_diff, smartapply
import os

os.environ['NANOGPT_API_KEY'] = 'your-api-key'

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

### Core Functions

- `generate_diff(environment: str, goal: str, model: str) -> str`  
  Generates a git diff implementing the requested changes
  
- `smartapply(diff_text: str, environment_str: str, model: str) -> str`  
  Applies complex diffs while preserving file context

### Environment Format

```text
File: [path]
Content:
[file contents]
```
Repeat for each file in your codebase snapshot

## Testing

To run the test suite:

```bash
pip install -e .[test]
pytest tests/
```

This will execute all unit tests verifying core diff generation and application logic.