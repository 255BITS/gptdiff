# Troubleshooting

## Common Issues and Solutions

### Issue 1: API Key Not Found
**Description:**
You receive an error message indicating that the NANOGPT_API_KEY environment variable is required.

**Solution:**
- Ensure that you have set the NANOGPT_API_KEY environment variable correctly. For Linux/MacOS, you can set it using:
    ```bash
    export NANOGPT_API_KEY='your-api-key'
    ```
- For Windows, use:
    ```cmd
    set NANOGPT_API_KEY=your-api-key
    ```
- Verify that the API key is correctly set by running `echo $NANOGPT_API_KEY` on Linux/MacOS or `echo %NANOGPT_API_KEY%` on Windows.

### Issue 2: Unable to Apply Generated Diff
**Description:**
The `gptdiff` command generates a diff, but applying the patch using `git apply` fails.

**Solution:**
1. First, make sure that the generated diff is valid by saving it to a file and checking it manually:
    ```bash
    gptdiff "your prompt" --call > diff.patch
    git apply --check diff.patch
    ```
2. If `git apply` fails, try using the `smartapply` feature:
    ```bash
    gptdiff "your prompt" --apply
    ```
    This uses an AI-powered conflict resolution to handle issues with applying the diff.

### Issue 3: GPTDiff Ignores a File
**Description:**
A file that you want to be processed by `gptdiff` is being ignored.

**Solution:**
1. Ensure that the file is not listed in your `.gitignore` or `.gptignore` file. Files listed in these ignore files are excluded from being processed by `gptdiff`.
2. If you need to include an ignored file, manually specify it in the `gptdiff` command:
    ```bash
    gptdiff "your prompt" yourfile.py
    ```

### Issue 4: Large Token Usage Warning
**Description:**
When running `gptdiff`, you get a warning that the request is large and a confirmation prompt appears.

**Solution:**
1. If you are sure that you want to send a large request, type `y` when prompted.
2. To bypass this warning in the future, you can add the `--nowarn` flag to your command:
    ```bash
    gptdiff "your prompt" --apply --nowarn
    ```

### Issue 5: Patch Does Not Produce Expected Changes
**Description:**
The changes made by the generated patch do not match what you expected from your prompt.

**Solution:**
1. Review your prompt for clarity and make sure it unambiguously describes the changes you want.
2. Use the `--call` option first to preview the generated diff without applying it:
    ```bash
    gptdiff "your prompt" --call
    ```
3. If the generated diff is still not as expected, try refining your prompt or using a lower `--temperature` value for a more deterministic output:
    ```bash
    gptdiff "your prompt" --temperature 0.3 --call
    ```

### Issue 6: UnicodeDecodeError When Reading Files
**Description:**
You encounter `UnicodeDecodeError` while reading some files.

**Solution:**
1. `gptdiff` currently supports only text files encoded in UTF-8. Make sure that all files you want to process are UTF-8 encoded.
2. Binary files are skipped automatically. To handle non-UTF-8 text files, you need to convert them to UTF-8 before processing.

### Issue 7: Model Not Responding as Expected
**Description:**
The model seems to be generating incorrect or irrelevant diffs.

**Solution:**
1. Check that you're using the appropriate model for your task. The default model can be changed by setting the `GPTDIFF_MODEL` environment variable.
2. Try adjusting the `--temperature` parameter for more deterministic output:
    ```bash
    gptdiff "your prompt" --temperature 0.3
    ```
3. Ensure your API key has access to the specified model.