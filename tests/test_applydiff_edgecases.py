import re
import subprocess
from pathlib import Path

import pytest

from gptdiff.gptdiff import apply_diff


@pytest.fixture
def tmp_project_dir(tmp_path):
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    # Create a baseline file for tests.
    file = project_dir / "example.txt"
    file.write_text("line1\nline2\nline3\n")
    return project_dir


def test_empty_diff(tmp_project_dir):
    """
    Test that an empty diff returns False.
    """
    diff_text = ""
    result = apply_diff(str(tmp_project_dir), diff_text)
    assert result is False, "Empty diff should return False"


def test_diff_no_changes(tmp_project_dir):
    """
    Test a diff that makes no changes. Even though a hunk is present, 
    if the content remains the same, the function should return False.
    """
    diff_text = (
        "diff --git a/example.txt b/example.txt\n"
        "--- a/example.txt\n"
        "+++ a/example.txt\n"
        "@@ -1,3 +1,3 @@\n"
        " line1\n"
        "-line2\n"
        "+line2\n"
        " line3\n"
    )
    result = apply_diff(str(tmp_project_dir), diff_text)
    assert result is False, "Diff that makes no changes should return False"
    content = (tmp_project_dir / "example.txt").read_text()
    assert "line2" in content, "Original content should remain unchanged"


def test_new_file_creation(tmp_project_dir):
    """
    Test that a diff creating a new file is applied correctly.
    """
    diff_text = (
        "diff --git a/newfile.txt b/newfile.txt\n"
        "new file mode 100644\n"
        "index 0000000..e69de29\n"
        "--- /dev/null\n"
        "+++ b/newfile.txt\n"
        "@@ -0,0 +1,3 @@\n"
        "+new line1\n"
        "+new line2\n"
        "+new line3\n"
    )
    result = apply_diff(str(tmp_project_dir), diff_text)
    assert result is True, "Diff for new file creation should return True"
    new_file = tmp_project_dir / "newfile.txt"
    assert new_file.exists(), "New file should be created"
    content = new_file.read_text()
    assert "new line1" in content, "New file content should be present"


def test_multiple_hunks(tmp_project_dir):
    """
    Test that a diff with multiple hunks in one file applies correctly.
    """
    file = tmp_project_dir / "example.txt"
    # Overwrite with a known baseline.
    file.write_text("a\nb\nc\nd\ne\n")
    diff_text = (
        "diff --git a/example.txt b/example.txt\n"
        "--- a/example.txt\n"
        "+++ b/example.txt\n"
        "@@ -1,3 +1,3 @@\n"
        "-a\n"
        "+alpha\n"
        " b\n"
        " c\n"
        "@@ -4,2 +4,2 @@\n"
        "-d\n"
        "-e\n"
        "+delta\n"
        "+epsilon\n"
    )
    result = apply_diff(str(tmp_project_dir), diff_text)
    assert result is True, "Diff with multiple hunks should return True"
    content = (tmp_project_dir / "example.txt").read_text()
    assert "alpha" in content
    assert "delta" in content and "epsilon" in content


def test_diff_with_incorrect_context(tmp_project_dir):
    """
    Test that a diff with incorrect context (non-matching original content) fails.
    """
    file = tmp_project_dir / "example.txt"
    file.write_text("different content\n")
    diff_text = (
        "diff --git a/example.txt b/example.txt\n"
        "--- a/example.txt\n"
        "+++ a/example.txt\n"
        "@@ -1,1 +1,1 @@\n"
        "-line that does not exist\n"
        "+modified content\n"
    )
    result = apply_diff(str(tmp_project_dir), diff_text)
    assert result is False, "Diff with incorrect context should return False"
    content = file.read_text()
    assert "different content" in content, "Original content should remain unchanged"


def test_diff_with_whitespace_changes(tmp_project_dir):
    """
    Test that a diff with only whitespace changes is applied.
    """
    file = tmp_project_dir / "example.txt"
    file.write_text("line1\nline2\nline3\n")
    diff_text = (
        "diff --git a/example.txt b/example.txt\n"
        "--- a/example.txt\n"
        "+++ a/example.txt\n"
        "@@ -1,3 +1,3 @@\n"
        " line1\n"
        "-line2\n"
        "+line2  \n"
        " line3\n"
    )
    result = apply_diff(str(tmp_project_dir), diff_text)
    assert result is True, "Diff with whitespace changes should return True if applied"
    content = file.read_text()
    assert "line2  " in content, "Whitespace change should be reflected in the file"


def test_diff_file_deletion_edge(tmp_project_dir):
    """
    Test deletion diff for a file with minimal content.
    """
    file = tmp_project_dir / "small.txt"
    file.write_text("only line\n")
    diff_text = (
        "diff --git a/small.txt b/small.txt\n"
        "deleted file mode 100644\n"
        "index e69de29..0000000\n"
        "--- a/small.txt\n"
        "+++ /dev/null\n"
        "@@ -1,1 +0,0 @@\n"
        "-only line\n"
    )
    result = apply_diff(str(tmp_project_dir), diff_text)
    assert result is True, "Deletion diff on a minimal file should return True"
    assert not (tmp_project_dir / "small.txt").exists(), "File should be deleted"
