#!/bin/bash

# Setup test environment
echo "Setting up test environment..."
mkdir -p test_project
echo "def main(): print('Hello')" > test_project/main.py
echo "def util(): return 42" > test_project/utils.py
echo "# Test Project" > test_project/README.md
cd test_project

# Test 1: Generate and apply diff
echo "Test 1: Generate and apply diff"
gptdiff "Add a new utility function" --apply
echo "Please inspect changes in test_project/ files (e.g., utils.py)"
read -p "Press enter to continue..."

# Test 2: Generate diff without applying
echo "Test 2: Generate diff without applying"
gptdiff "Update readme with usage info" --call
echo "Please check diff.patch for the generated diff"
cat diff.patch 2>/dev/null || echo "diff.patch not created"
read -p "Press enter to continue..."

# Test 3: Write prompt only
echo "Test 3: Write prompt only"
gptdiff "Improve error handling"
echo "Please check prompt.txt for the generated prompt"
cat prompt.txt 2>/dev/null || echo "prompt.txt not created"
read -p "Press enter to continue..."

# Test 4: Target specific file with apply
echo "Test 4: Target specific file with apply"
gptdiff "Add logging to main.py" main.py --apply
echo "Please inspect changes in main.py"
cat main.py 2>/dev/null || echo "main.py not modified"
read -p "Press enter to continue..."

# Cleanup
echo "Cleaning up..."
cd ..
rm -rf test_project
echo "Test environment removed."
