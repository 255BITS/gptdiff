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

`--nobeep`  
**Silence completion alerts**  
*Example:*  
```bash
gptdiff "Remove deprecated features" --nobeep
```

