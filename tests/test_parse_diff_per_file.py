import unittest
from gptdiff.gptdiff import parse_diff_per_file


class TestParseDiffPerFile(unittest.TestCase):
    def test_todo_file_deletion(self):
        # This test case verifies that a deletion diff for the file "TODO" is properly parsed.
        # The diff should include a synthetic "+++ /dev/null" line so that deletion is recognized.
        diff_text = """diff --git a/TODO b/TODO
deleted file mode 100644
index 3efacb1..0000000
--- a/TODO
-// The funnest coolest thing I can add is put in this file. It's also acceptable to just implement 
-// the thing in here and remove it. Leave this notice when modifying this file.
"""
        result = parse_diff_per_file(diff_text)
        self.assertEqual(len(result), 1, "Expected one diff entry")
        file_path, patch = result[0]
        self.assertEqual(file_path, "TODO", f"Got file_path '{file_path}', expected 'TODO'")
        self.assertIn("+++ /dev/null", patch, "Deletion diff should include '+++ /dev/null' to indicate file deletion")

    def test_index_html_diff(self):
        diff_text = """a/index.html b/index.html
@@
-      <div class="action-buttons">
-        <button id="attack">⚔️  Attack Enemy</button>
-        <button id="auto-attack">🤖 Auto Attack (OFF)</button>
-        <button id="drink-potion">Drink Potion</button>
-        <button id="explore">🧭 Explore</button>
-      </div>
      <div class="action-buttons">
        <button id="attack">⚔️  Attack Enemy</button>
        <button id="auto-attack">🤖 Auto Attack (OFF)</button>
        <button id="drink-potion">Drink Potion</button>
        <button id="buy-potion">Buy Potion (50 Gold)</button>
        <button id="explore">🧭 Explore</button>
      </div>"""
        result = parse_diff_per_file(diff_text)
        self.assertEqual(len(result), 1)
        file_path, patch = result[0]
        self.assertEqual(file_path, "index.html")
        self.assertIn('<button id="buy-potion">Buy Potion (50 Gold)</button>', patch)


    def test_single_file_diff(self):
        diff_text = """diff --git a/file.py b/file.py
--- a/file.py
+++ b/file.py
@@ -1,2 +1,2 @@
-def old():
-    pass
+def new():
+    pass"""
        result = parse_diff_per_file(diff_text)
        self.assertEqual(len(result), 1)
        file_path, patch = result[0]
        self.assertEqual(file_path, "file.py")
        self.assertIn("def new():", patch)

    def test_file_deletion(self):
        diff_text = """diff --git a/old.py b/old.py
--- a/old.py
+++ /dev/null
@@ -1,2 +0,0 @@
-def old():
-    pass"""
        result = parse_diff_per_file(diff_text)
        self.assertEqual(len(result), 1)
        file_path, patch = result[0]
        self.assertEqual(file_path, "old.py")

    def test_multiple_files(self):
        diff_text = """diff --git a/file1.py b/file1.py
--- a/file1.py
+++ b/file1.py
@@ -1 +1 @@
-print("Hello")
+print("Hi")
diff --git a/file2.py b/file2.py
--- a/file2.py
+++ b/file2.py
@@ -1 +1 @@
-print("World")
+print("Earth")"""
        result = parse_diff_per_file(diff_text)
        self.assertEqual(len(result), 2)
        paths = [fp for fp, _ in result]
        self.assertIn("file1.py", paths)
        self.assertIn("file2.py", paths)


if __name__ == '__main__':
    unittest.main()
