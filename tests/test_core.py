import pytest
import json
from unittest.mock import MagicMock, patch, call
from gptdiff import generate_diff, smartapply

SAMPLE_ENVIRONMENT = '''\
def greet():
    print("Hello World")
'''

EXPECTED_DIFF = """\
diff --git a/test_file.py b/test_file.py
@@ -1,2 +1,2 @@
 def greet():
-    print("Hello World")
+    print("Hola Mundo")
"""

UPDATED_ENVIRONMENT = {"test_file.py": '''\
def greet():
    print("Hola Mundo")'''}

RM_EXAMPLE="""index 2345678..0000000
--- a/instructions/2.txt
+++ /dev/null
@@ -1,1 +0,0 @@
- hello world
"""

@pytest.fixture
def complex_diff():
    return """\
diff --git a/instructions/4.txt b/instructions/4.txt
new file mode 100644
--- /dev/null
+++ b/instructions/4.txt
@@ -0,0 +1,11 @@
+Create a surreal dreamscape song using non-linear storytelling and paradoxical imagery. Alternate between whispered verses and explosive choruses. Incorporate glitchy electronic elements with organic instrumentation.
+
+Song:
+Uses: [Glitch Beats], [Whale Song Samples], [Polymeter 7/8 vs 4/4], [Theremin]
+Structure: Verse-PreChorus-Chorus-Verse-Bridge-Chorus-Coda
+Note: Should feel like drifting between reality and simulation. Use at least three contrasting vocal styles.
+
+Lyric constraints:
+- Include one mathematical equation
+- Reference a forgotten childhood memory
+- Use color synesthesia descriptions
diff --git a/instructions/5.txt b/instructions/5.txt
new file mode 100644
--- /dev/null
+++ b/instructions/5.txt
@@ -0,0 +1,12 @@
+Compose a song exploring the tension between human intuition and machine logic. Use alternating sections of rigid quantized rhythms and free-form jazz improvisation. Include error messages as lyrical elements.
+
+Song:
+Uses: [Modular Synth Bursts], [Jazz Scat Breakdown], [Bitcrushed Vocals], [Chaotic Time Signature Changes]
+Required elements:
+- A chorus where human vocals and AI-generated vocals argue
+- Bridge using actual code syntax as lyrics
+- Outro that gradually degrades into white noise
+
+Themes to blend:
+1. Neural network training metaphors
+2. Biological vs digital consciousness
+3. The loneliness of infinite scalability"""

@pytest.fixture
def mock_openai():
    with patch('gptdiff.gptdiff.OpenAI') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        
        # Mock for generate_diff
        mock_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=f"""<diff>
{EXPECTED_DIFF}
</diff>"""))])
        
        yield mock_instance

def test_generate_diff(mock_openai):
    diff = generate_diff(SAMPLE_ENVIRONMENT, "Translate to Spanish")
    
    # Check the diff was generated
    assert diff.strip() == EXPECTED_DIFF.strip()
    
    # Verify API call
    mock_openai.chat.completions.create.assert_called_once()
    prompt = mock_openai.chat.completions.create.call_args[1]['messages'][1]['content']
    assert "Translate to Spanish" in prompt
    assert SAMPLE_ENVIRONMENT in prompt

@patch('gptdiff.gptdiff.call_llm_for_apply')
def test_smartapply(mock_call_llm):
    # Mock the LLM call to return patched content
    mock_call_llm.return_value = UPDATED_ENVIRONMENT["test_file.py"]
    
    original_files = {"test_file.py": SAMPLE_ENVIRONMENT}
    updated_environment = smartapply(EXPECTED_DIFF, original_files)

    assert updated_environment == UPDATED_ENVIRONMENT

@patch('gptdiff.gptdiff.call_llm_for_apply')
def test_smartapply_with_new_files(mock_call_llm, complex_diff):
    expected_files = {
        "instructions/4.txt": "\n".join(line[1:] for line in complex_diff.split('\n')[5:16]),
        "instructions/5.txt": "\n".join(line[1:] for line in complex_diff.split('\n')[22:34])
    }
    
    # Mock LLM to return file contents line by line
    def side_effect(file_path, original_content, file_diff, model, **kwargs):
        return expected_files[file_path]
    mock_call_llm.side_effect = side_effect

    original_files = {}
    updated = smartapply(complex_diff, original_files)
    assert len(updated.keys()) == 2

@patch('gptdiff.gptdiff.call_llm_for_apply')
def test_rm_file(mock_call_llm):
    original_files = {"instructions/2.txt": "hello world\n"}
    
    # Shouldn't call LLM for deletions
    mock_call_llm.side_effect = AssertionError("LLM should not be called for file deletion")

    updated = smartapply(RM_EXAMPLE, original_files)
    assert "instructions/2.txt" not in updated.keys()
