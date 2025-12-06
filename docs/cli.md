# GPTDiff CLI Reference

## Core Command Structure
```bash
gptdiff "<transformation-prompt>" [FILES...] [OPTIONS]
```

## Key Options

### .gitignore and .gptignore

Files matching .gitignore pattern or <b>.gptignore</b> patterns are ignored when no files are specified.

### Transformation Control
`--apply`  
**AI-powered patch application**  
*Example:*  
⚠️ Processes files concurrently for performance
```bash
gptdiff "Add null safety checks" --apply src/
```

`--call`  
**Generate diff without applying**  
*Example:*  
```bash
gptdiff "Modernize string formatting" --call
```

`--prepend <file>`
**Prepend custom instructions from file to system prompt**
*Example:*
```bash
gptdiff "Modernize string formatting" --prepend style-guide.txt
```
`--prepend <file_or_url>`: Prepend custom instructions from the specified file or URL to the system prompt

`--image <path>`
**Attach one or more images**
*Example:*
```bash
gptdiff "Explain the chart in the README and refactor accordingly" --image docs/chart.png --image docs/layout.png
```
Adds each image (base64-encoded) to the request so the LLM can use visual context when generating diffs.

`--temperature <0-2>`  
**Control transformation creativity**  
*Default:* 0.7  
*Example:*  
```bash
gptdiff "Refactor legacy API" --temperature 0.3
```

### Model Selection
`--model`  
**Choose reasoning engine (default: $GPTDIFF_MODEL or 'deepseek-reasoner')**  
*Options:* `deepseek-reasoner` (structural), `gemini-2.0-flash` (text)  
*Example:*  
```bash
gptdiff "Translate docs to French" --model gemini-2.0-flash
```

### Scope Management
`--files`  
**Target specific paths**  
*Example:*  
```bash
gptdiff "Update config system" config/ utils/config_loader.py
```

`--max_tokens <number>`: Set the maximum number of tokens for the API response (default: 30000)
`--applymodel <model_name>`: Specify the model to use for applying the diff (used in smartapply). If not specified, defaults to the model from `--model` or `GPTDIFF_MODEL`.
`--nowarn`: Disable the warning and confirmation prompt for large token usage
`--verbose`: Enable verbose output for detailed information during execution

`--nobeep`  
**Silence completion alerts**  
*Example:*  
```bash
gptdiff "Remove deprecated features" --nobeep
```

### Environment Variables
GPTDiff uses the following environment variables:
- `GPTDIFF_LLM_API_KEY`: API key for the LLM service
- `GPTDIFF_LLM_BASE_URL`: Base URL for the LLM API (default: https://nano-gpt.com/api/v1/)
- `GPTDIFF_MODEL`: Default model for generating diffs (default: deepseek-reasoner)

For the smartapply feature, you can set separate variables:
- `GPTDIFF_SMARTAPPLY_MODEL`: Model for smartapply (recommended: `openai/gpt-4.1-mini`, the fastest model that applies diffs reliably; defaults to `GPTDIFF_MODEL` if not set)
- `GPTDIFF_SMARTAPPLY_API_KEY`: API key for smartapply (defaults to `GPTDIFF_LLM_API_KEY` if not set)
- `GPTDIFF_SMARTAPPLY_BASE_URL`: Base URL for smartapply (defaults to `GPTDIFF_LLM_BASE_URL` if not set)

These allow you to use different models or credentials for generating and applying diffs—perfect for virtual team flexibility!
  
## plangptdiff
  
`plangptdiff` scans your repository with **ripgrep**, selects only the files likely to change (always including anything named *schema*), and writes a ready‑to‑paste prompt to **planprompt.txt**.  

**Usage:**  
```bash  
plangptdiff "<natural language command>" [--apply]  
```  

**Examples:**  
- Generate a prompt only:  
  ```bash  
  plangptdiff "add validation to the signup form"  
  ```  
- Generate a prompt and auto‑apply the diff:  
  ```bash  
  plangptdiff "upgrade to Django 5" --apply  
  ```  

The file list is appended to the generated `gptdiff` command so the LLM sees only the files that matter.