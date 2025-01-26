# GPTDiff CLI Reference

## Core Command Structure
```bash
gptdiff "<transformation-prompt>" [OPTIONS] [FILES...]
```

## Key Options

### Transformation Control
`--apply`  
**AI-powered patch application**  
*Example:*  
```bash
gptdiff "Add null safety checks" --apply src/
```

`--call`  
**Generate diff without applying**  
*Example:*  
```bash
gptdiff "Modernize string formatting" --call
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
**Choose reasoning engine**  
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

## Common Workflows

### Atomic Code Review
```bash
gptdiff "Improve test coverage" tests/ --call > review.patch
git apply --check review.patch
```

### Emergency Hotfix
```bash
gptdiff "Fix login regression" --apply --model deepseek-reasoner
```

### Legacy Modernization
```bash
gptdiff "Convert Python 2 syntax to 3" --apply \
  --temperature 0.1 \
  src/legacy/
```