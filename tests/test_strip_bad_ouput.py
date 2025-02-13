# File: tests/test_strip_bad_output.py
import pytest
from gptdiff.gptdiff import strip_bad_output

def test_strip_bad_output_removes_wrapping():
    """
    If the original file content does not start with a code fence,
    but the LLM output starts with a code block and extra text,
    then only the content inside the first code block should be returned.
    """
    # Original file content does not start with a code fence.
    original = "def hello():\n    print('Hello')\n"
    # Simulated LLM output with extraneous text and a code block.
    updated = (
        "This is the file you requested:\n"
        "```diff\n"
        "def hello():\n"
        "    print('Goodbye')\n"
        "```\n"
        "Thank you!"
    )
    # We expect the function to extract only the content inside the code block.
    expected = "diff\ndef hello():\n    print('Goodbye')"
    result = strip_bad_output(updated, original)
    assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"

def test_strip_bad_output_no_change_when_original_has_code_block():
    """
    If the original file already starts with a code fence,
    the function should leave the updated output unchanged.
    """
    original = "```diff\ndef hello():\n    print('Hello')\n```"
    updated = "```diff\ndef hello():\n    print('Modified')\n```"
    expected = updated.strip()
    result = strip_bad_output(updated, original)
    assert result == expected, "Expected no changes when original already starts with a code fence"

def test_strip_bad_output_no_wrapping_detected():
    """
    If the updated output does not start with a code fence,
    the function should return the updated output unchanged.
    """
    original = "def hello():\n    print('Hello')\n"
    updated = "def hello():\n    print('Modified')\n"
    expected = updated.strip()
    result = strip_bad_output(updated, original)
    assert result == expected, "Expected output to remain unchanged if no code block is detected"


def test_strip_bad_output_prod_case():
    """
    Test that when the updated output includes extraneous introductory text and
    a language specifier in the code block, the function extracts only the content
    within the code block (without the language tag or extra text).

    For example, given an updated output like:

        Here's the entire file after applying the diff:

        ```typescript
        def foo():
            print('Modified')
        ```
        Some trailing text that should be ignored.

    the expected extracted content is:

        def foo():
            print('Modified')
    """
    # Original file content does not start with a code fence.
    original = "def foo():\n    pass\n"

    # Simulated LLM output with extraneous text, a language specifier ("typescript"),
    # and trailing text.
    updated = (
        "Here's the entire file after applying the diff:\n\n"
        "```typescript\n"
        "def foo():\n"
        "    print('Modified')\n"
        "```\n"
        "Some trailing text that should be ignored."
    )

    # We expect the function to extract only the content inside the first code block,
    # ignoring the language specifier and any text outside the code block.
    expected = "def foo():\n    print('Modified')"

    result = strip_bad_output(updated, original)
    assert result == expected, f"Expected:\n{expected}\nGot:\n{result}"
