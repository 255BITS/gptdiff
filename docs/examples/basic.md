# Basic Examples

## Single-File Refactor

```bash
# Before: utils.py
def process_data(input):
    result = []
    for item in input:
        result.append(item*2)
    return result

gptdiff "Convert loop to list comprehension" utils.py --apply
```

```python
# After: utils.py
def process_data(input):
    return [item*2 for item in input]
```

## Multi-File Rename

```bash
gptdiff "Rename UserController to AccountController" \
    app/controllers/user_controller.py \
    test/controllers/test_user_controller.py \
    docs/api.md --apply
```

## Full-Stack Type Safety

```bash
gptdiff "Add Python type hints throughout codebase" \
    --model deepseek-reasoner \
    --temperature 0.3 \
    --apply
```

## Legacy Modernization

```bash
gptdiff "Convert string formatting to f-strings" src/ --apply
```
