import pytest

from gptdiff.gptdiff import swallow_reasoning


def test_swallow_reasoning_extraction():
    llm_response = (
        "> Reasoning\n"
        "**Applying the diff**\n"
        "I'm piecing together how to efficiently apply a diff to a file...\n"
        "**Returning the result**\n"
        "I'm finalizing the method to apply the diff updates...\n"
        "Reasoned for 6 seconds\n"
        "\n"
        "```diff\n"
        "--- a/file.py\n"
        "+++ b/file.py\n"
        "@@ -1,2 +1,2 @@\n"
        "-def old():\n"
        "+def new():\n"
        "```"
    )
    final_content, reasoning = swallow_reasoning(llm_response)
    expected_reasoning = (
        "> Reasoning\n"
        "**Applying the diff**\n"
        "I'm piecing together how to efficiently apply a diff to a file...\n"
        "**Returning the result**\n"
        "I'm finalizing the method to apply the diff updates...\n"
        "Reasoned for 6 seconds"
    )
    assert reasoning == expected_reasoning
    # The final content should no longer contain the reasoning block.
    assert expected_reasoning not in final_content
    # And it should contain the diff block.
    assert "```diff" in final_content


def test_swallow_reasoning_no_reasoning():
    llm_response = (
        "```diff\n"
        "--- a/file.py\n"
        "+++ b/file.py\n"
        "@@ -1,2 +1,2 @@\n"
        "-def old():\n"
        "+def new():\n"
        "```"
    )
    final_content, reasoning = swallow_reasoning(llm_response)
    assert reasoning == ""
    assert final_content == llm_response.strip()
