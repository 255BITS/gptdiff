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
- **--dumb**: Attempt to apply the diff using standard patch logic (like git apply) before falling back to smart apply

## Workflow

By default, gptpatch uses an AI-powered smart apply mechanism to apply the diff directly. If the `--dumb` flag is specified, it first attempts to apply the diff using standard patch logic (similar to git apply). If that fails, it falls back to the smart apply mechanism with AI-powered conflict resolution.

For further details about GPTDiff and its companion tools, please refer to the [GPTDiff Documentation](https://gptdiff.255labs.xyz).