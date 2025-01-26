# Advanced Refactoring

## Database Layer Migration

```bash
gptdiff "Replace raw SQL with SQLAlchemy ORM" \
    --files models/ queries/ \
    --apply
```

**Transformations Applied:**
- SQL injection protection
- Session management
- Type-safe query building
- Transaction handling

## API Versioning

```bash
gptdiff "Add v2 API endpoints with backward compatibility" \
    --model deepseek-reasoner \
    --temperature 0.5 \
    --apply
```

**Created Files:**
- `api/v2/schemas.py`
- `api/v2/routers/`
- `tests/v2/`

## Internationalization

```bash
gptdiff "Extract all UI strings to translation files" \
    --files templates/ static/js/ \
    --call > i18n.patch
```
**Preserved:** String context comments for translators