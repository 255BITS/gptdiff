---
title: gptpatch
---

# gptpatch Command-Line Tool

`gptpatch` is a companion tool to [GPTDiff](https://github.com/255BITS/gptdiff) that applies unified diffs directly to your project using GPTDiff’s patch logic.

## Overview

`gptpatch` accepts diffs either directly via a command-line argument or from a file. It first attempts to apply the diff using standard patch logic. If that fails, it falls back to a smart apply mechanism that leverages AI-powered conflict resolution.

## Usage

### Apply Diff from Command Line

```bash
gptpatch --diff "<diff text>"
```

### Apply Diff from a File

```bash
gptpatch path/to/diff.patch
```

## Options

- **--project-dir**: Specify the target directory for applying the diff (default: current directory)
- **--model**: (Optional) Specify the LLM model for advanced conflict resolution
- **--max_tokens**: (Optional) Maximum tokens to use for LLM responses
- **--nobeep**: Disable the completion beep notification

## Workflow

1. The tool first attempts to apply the diff using standard patch logic via the `apply_diff` function.
2. If standard application fails, it automatically falls back to a smart apply mechanism using AI-powered conflict resolution.

For further details about GPTDiff and its companion tools, please refer to the [GPTDiff Documentation](https://gptdiff.255labs.xyz).