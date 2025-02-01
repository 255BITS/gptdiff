import os
from pathlib import Path

import pytest

from gptdiff.gptdiff import apply_diff


@pytest.fixture
def tmp_project_dir(tmp_path):
    """
    Create a temporary project directory with a dummy file to patch.
    """
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    file = project_dir / "example.txt"
    file.write_text("original content\n")
    return project_dir


def test_apply_diff_success(tmp_project_dir):
    """
    Test that apply_diff successfully applies a valid diff.
    The diff changes 'original content' to 'modified content'.
    """
    diff_text = (
        "diff --git a/example.txt b/example.txt\n"
        "--- a/example.txt\n"
        "+++ b/example.txt\n"
        "@@ -1 +1 @@\n"
        "-original content\n"
        "+modified content\n"
    )
    result = apply_diff(str(tmp_project_dir), diff_text)
    assert result is True, "apply_diff should return True for a successful patch"

    file_path = tmp_project_dir / "example.txt"
    content = file_path.read_text()
    assert "modified content" in content, "File content should be updated to 'modified content'"


def test_apply_diff_failure(tmp_project_dir):
    """
    Test that apply_diff fails when provided with an incorrect hunk header.
    The diff references a non-existent line, so the patch should not apply.
    """
    diff_text = (
        "diff --git a/example.txt b/example.txt\n"
        "--- a/example.txt\n"
        "+++ a/example.txt\n"
        "@@ -2,1 +2,1 @@\n"
        "-original content\n"
        "+modified content\n"
    )
    result = apply_diff(str(tmp_project_dir), diff_text)
    assert result is False, "apply_diff should return False when the diff fails to apply"

    file_path = tmp_project_dir / "example.txt"
    content = file_path.read_text()
    assert "original content" in content, "File content should remain unchanged on failure"


def test_apply_diff_file_deletion(tmp_project_dir):
    """
    Test that apply_diff can successfully delete a file.
    The diff marks 'example.txt' for deletion.
    """
    diff_text = (
        "diff --git a/example.txt b/example.txt\n"
        "deleted file mode 100644\n"
        "--- a/example.txt\n"
        "+++ /dev/null\n"
        "@@ -1,1 +0,0 @@\n"
        "-original content\n"
    )
    result = apply_diff(str(tmp_project_dir), diff_text)
    assert result is True, "apply_diff should return True for a successful file deletion"

    file_path = tmp_project_dir / "example.txt"
    assert not file_path.exists(), "File should be deleted after applying the diff"
