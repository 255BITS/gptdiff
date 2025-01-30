#!/usr/bin/env python3

import openai
from openai import OpenAI

import tiktoken
import time

import os
import json
import subprocess
from pathlib import Path
import sys
import fnmatch
import argparse
import pkgutil
import re
import contextvars
from ai_agent_toolbox import FlatXMLParser, FlatXMLPromptFormatter, Toolbox
import threading
from pkgutil import get_data

diff_context = contextvars.ContextVar('diffcontent', default="")
def create_diff_toolbox():
    toolbox = Toolbox()
    
    def diff(content: str):
        diff_context.set(content)
        return content

    toolbox.add_tool(
        name="diff",
        fn=diff,
        args={
            "content": {
                "type": "string",
                "description": "Complete diff."
            }
        },
        description="""Save the calculated diff as used in 'git apply'. Should include the file and line number. For example:
a/file.py b/file.py
--- a/file.py
+++ b/file.py
@@ -1,2 +1,2 @@
-def old():
+def new():
"""
    )
    return toolbox

def create_think_toolbox():
    toolbox = Toolbox()
    
    def think(content: str):
        print("Swallowed thoughts", content)

    toolbox.add_tool(
        name="think",
        fn=think,
        args={
            "content": {
                "type": "string",
                "description": "Thoughts"
            }
        },
        description=""
    )
    return toolbox


def load_gitignore_patterns(gitignore_path):
    with open(gitignore_path, 'r') as f:
        patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return patterns

def is_ignored(filepath, gitignore_patterns):
    filepath = Path(filepath).resolve()
    ignored = False

    for pattern in gitignore_patterns:
        if pattern.startswith('!'):
            negated_pattern = pattern[1:]
            if fnmatch.fnmatch(str(filepath), negated_pattern) or fnmatch.fnmatch(str(filepath.relative_to(Path.cwd())), negated_pattern):
                ignored = False
        else:
            relative_path = str(filepath.relative_to(Path.cwd()))
            if fnmatch.fnmatch(str(filepath), pattern) or fnmatch.fnmatch(relative_path, pattern):
                ignored = True
                break
            if pattern in relative_path:
                ignored = True
                break

    # Ensure .gitignore itself is not ignored unless explicitly mentioned
    if filepath.name == ".gitignore" and not any(pattern == ".gitignore" for pattern in gitignore_patterns):
        ignored = False

    return ignored

def list_files_and_dirs(path, ignore_list=None):
    if ignore_list is None:
        ignore_list = []

    result = []

    # List all items in the current directory
    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if is_ignored(item_path, ignore_list):
            continue

        # Add the item to the result list
        result.append(item_path)

        # If it's a directory, recurse into it
        if os.path.isdir(item_path):
            result.extend(list_files_and_dirs(item_path, ignore_list))

    return result

# Function to load project files considering .gitignore
def load_project_files(project_dir, cwd): 
    """Load project files while respecting .gitignore and .gptignore rules.
    
    Recursively scans directories, skipping:
    - Files/directories matching patterns in .gitignore/.gptignore
    - Binary files that can't be decoded as UTF-8 text
    
    Args:
        project_dir: Root directory to scan for files
        cwd: Base directory for resolving ignore files
    
    Returns:
        List of (absolute_path, file_content) tuples
    
    Note:
        Prints skipped files to stdout for visibility
    """
    ignore_paths = [Path(cwd) / ".gitignore", Path(cwd) / ".gptignore"]
    gitignore_patterns = [".gitignore", "diff.patch", "prompt.txt", ".gptignore", "*.pdf", "*.docx", ".git", "*.orig", "*.rej"]

    for p in ignore_paths:
        if p.exists():
            with open(p, 'r') as f:
                gitignore_patterns.extend([line.strip() for line in f if line.strip() and not line.startswith('#')])

    project_files = []
    for file in list_files_and_dirs(project_dir, gitignore_patterns):
        if os.path.isfile(file):
                try:
                    with open(file, 'r') as f:
                        content = f.read()
                    print(file)
                    project_files.append((file, content))
                except UnicodeDecodeError:
                    print(f"Skipping file {file} due to UnicodeDecodeError")
                    continue

    print("")
    return project_files

def load_prepend_file(file):
    with open(file, 'r') as f:
        return f.read()

# Function to call GPT-4 API and calculate the cost
def call_llm_for_diff(system_prompt, user_prompt, files_content, model, temperature=0.7, max_tokens=30000, api_key=None, base_url=None):
    enc = tiktoken.get_encoding("o200k_base")
    start_time = time.time()

    parser = FlatXMLParser("diff")
    formatter = FlatXMLPromptFormatter(tag="diff")
    toolbox = create_diff_toolbox()
    tool_prompt = formatter.usage_prompt(toolbox)
    system_prompt += "\n"+tool_prompt

    if model == "gemini-2.0-flash-thinking-exp-01-21":
        user_prompt = system_prompt+"\n"+user_prompt

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt + "\n"+files_content},
    ]
    print("Using", model)
    print("SYSTEM PROMPT")
    print(system_prompt)
    print("USER PROMPT")
    print(user_prompt, "+", len(enc.encode(files_content)), "tokens of file content")

    if api_key is None:
        api_key = os.getenv('GPTDIFF_LLM_API_KEY')
    if base_url is None:
        base_url = os.getenv('GPTDIFF_LLM_BASE_URL', "https://nano-gpt.com/api/v1/")
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature)

    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    elapsed = time.time() - start_time
    minutes, seconds = divmod(int(elapsed), 60)
    time_str = f"{minutes}m {seconds}s" if minutes else f"{seconds}s"
    print(f"Diff creation time: {time_str}")
    print("-" * 40)

    # Now, these rates are updated to per million tokens
    cost_per_million_prompt_tokens = 30
    cost_per_million_completion_tokens = 60
    cost = (prompt_tokens / 1_000_000 * cost_per_million_prompt_tokens) + (completion_tokens / 1_000_000 * cost_per_million_completion_tokens)

    full_response = response.choices[0].message.content.strip()

    events = parser.parse(full_response)
    for event in events:
        toolbox.use(event)
    diff_response = diff_context.get()

    return full_response, diff_response, prompt_tokens, completion_tokens, total_tokens, cost

# New API functions
def build_environment(files_dict):
    """Rebuild environment string from file dictionary"""
    env = []
    for path, content in files_dict.items():
        env.append(f"File: {path}")
        env.append("Content:")
        env.append(content)
    return '\n'.join(env)

def generate_diff(environment, goal, model=None, temperature=0.7, max_tokens=32000, api_key=None, base_url=None, prepend=None):
    """API: Generate diff from environment and goal"""
    if model is None:
        model = os.getenv('GPTDIFF_MODEL', 'deepseek-reasoner')
    if prepend:
        prepend = load_prepend_file(args.prepend)
        print("Including prepend",len(enc.encode(json.dumps(prepend))), "tokens")
    else:
        prepend = ""
    
    system_prompt = prepend+f"Output a git diff into a <diff> block."
    _, diff_text, _, _, _, _ = call_llm_for_diff(
        system_prompt, 
        goal, 
        environment, 
        model=model,
        api_key=api_key,
        base_url=base_url,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return diff_text

def smartapply(diff_text, files, model=None, api_key=None, base_url=None):
    """Applies unified diffs to file contents with AI-powered conflict resolution.
    
    Key features:
    - Handles file creations, modifications, and deletions
    - Maintains idempotency - reapplying same diff produces same result
    - Uses LLM to resolve ambiguous changes while preserving context
    - Returns new files dictionary without modifying input

    Args:
        diff_text: Unified diff string compatible with git apply
        files: Dictionary of {file_path: content} to modify
        model: LLM to use for conflict resolution (default: deepseek-reasoner)
        api_key: Optional API key override
        base_url: Optional API base URL override

    Returns:
        New dictionary with updated file contents. Deleted files are omitted.

    Raises:
        APIError: If LLM API calls fail

    Example:
        >>> original = {"file.py": "def old():\n    pass"}
        >>> diff = '''diff --git a/file.py b/file.py
        ... --- a/file.py
        ... +++ b/file.py
        ... @@ -1,2 +1,2 @@
        ... -def old():
        ... +def new():'''
        >>> updated = smartapply(diff, original)
        >>> print(updated["file.py"])
        def new():
            pass
    """
    if model is None:
        model = os.getenv('GPTDIFF_MODEL', 'deepseek-reasoner')
    parsed_diffs = parse_diff_per_file(diff_text)    
    print("-" * 40)
    print("SMARTAPPLY")
    print(diff_text)
    print("-" * 40)

    def process_file(path, patch):
        original = files.get(path, '')
        # Handle file deletions
        if '+++ /dev/null' in patch:
            if path in files:
                del files[path]
        else:
            updated = call_llm_for_apply_with_think_tool_available(path, original, patch, model, api_key=api_key, base_url=base_url)
            files[path] = updated.strip()

    for path, patch in parsed_diffs:
        process_file(path, patch)

    return files

# Function to apply diff to project files
def apply_diff(project_dir, diff_text):
    diff_file = Path(project_dir) / "diff.patch"
    with open(diff_file, 'w') as f:
        f.write(diff_text)

    result = subprocess.run(["patch", "-p1", "-f", "--remove-empty-files", "--input", str(diff_file)], cwd=project_dir, capture_output=True, text=True)
    if result.returncode != 0:
        return False
    else:
        return True

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate and optionally apply git diffs using GPT-4.')
    parser.add_argument('prompt', type=str, help='Prompt that runs on the codebase.')
    parser.add_argument('--apply', action='store_true', help='Attempt to apply the generated git diff. Uses smartapply if applying the patch fails.')
    parser.add_argument('--prepend', type=str, default=None, help='Path to content prepended to system prompt')

    parser.add_argument('--nobeep', action='store_false', dest='beep', default=True, help='Disable completion notification beep')
    # New flag --prompt that does not call the API but instead writes the full prompt to prompt.txt
    parser.add_argument('--call', action='store_true',
                        help='Call the GPT-4 API. Writes the full prompt to prompt.txt if not specified.')
    parser.add_argument('files', nargs='*', default=[], help='Specify additional files or directories to include.')
    parser.add_argument('--temperature', type=float, default=0.7, help='Temperature parameter for model creativity (0.0 to 2.0)')
    parser.add_argument('--max_tokens', type=int, default=30000, help='Temperature parameter for model creativity (0.0 to 2.0)')
    parser.add_argument('--model', type=str, default=None, help='Model to use for the API call.')

    parser.add_argument('--nowarn', action='store_true', help='Disable large token warning')

    return parser.parse_args()

def absolute_to_relative(absolute_path):
    cwd = os.getcwd()
    relative_path = os.path.relpath(absolute_path, cwd)
    return relative_path

def parse_diff_per_file(diff_text):
    """Parse unified diff text into individual file patches.

    Splits a multi-file diff into per-file entries for processing. Handles:
    - File creations (+++ /dev/null)
    - File deletions (--- /dev/null)
    - Standard modifications

    Args:
        diff_text: Unified diff string as generated by `git diff`

    Returns:
        List of tuples (file_path, patch) where:
        - file_path: Relative path to modified file
        - patch: Full diff fragment for this file

    Note:
        Uses 'b/' prefix detection from git diffs to determine target paths
    """
    diffs = []
    file_path = None
    current_diff = []
    from_path = None

    for line in diff_text.split('\n'):
        if line.startswith('diff --git'):
            if current_diff and file_path is not None:
                diffs.append((file_path, '\n'.join(current_diff)))
            current_diff = [line]
            file_path = None
            from_path = None
            parts = line.split()
            if len(parts) >= 4:
                b_path = parts[3]
                file_path = b_path[2:] if b_path.startswith('b/') else b_path
        else:
            current_diff.append(line)
            if line.startswith('--- '):
                from_path = line[4:].strip()
            elif line.startswith('+++ '):
                to_path = line[4:].strip()
                if to_path == '/dev/null':
                    if from_path:
                        # For deletions, use from_path after stripping 'a/' prefix
                        file_path = from_path[2:] if from_path.startswith('a/') else from_path
                else:
                    # For normal cases, use to_path after stripping 'b/' prefix
                    file_path = to_path[2:] if to_path.startswith('b/') else to_path

    # Handle remaining diff content after loop
    if current_diff and file_path is not None:
        diffs.append((file_path, '\n'.join(current_diff)))

    return diffs

def call_llm_for_apply_with_think_tool_available(file_path, original_content, file_diff, model, api_key=None, base_url=None):
    parser = FlatXMLParser("think")
    formatter = FlatXMLPromptFormatter(tag="think")
    toolbox = create_think_toolbox()
    full_response = call_llm_for_apply(file_path, original_content, file_diff, model, api_key=None, base_url=None)
    notool_response = ""
    events = parser.parse(full_response)
    is_in_tool = False
    appended_content = ""
    for event in events:
        if event.mode == 'append':
            appended_content += event.content
        if event.mode == 'close' and appended_content and event.tool is None:
            notool_response += appended_content
        if event.mode == 'close':
            appended_content = ""
        toolbox.use(event)

    return notool_response

def call_llm_for_apply(file_path, original_content, file_diff, model, api_key=None, base_url=None):
    """AI-powered diff application with conflict resolution.
    
    Internal workhorse for smartapply that handles individual file patches.
    Uses LLM to reconcile diffs while preserving code structure and context.

    Args:
        file_path: Target file path (used for context/error messages)
        original_content: Current file content as string
        file_diff: Unified diff snippet to apply
        model: LLM identifier for processing
        api_key: Optional override for LLM API credentials
        base_url: Optional override for LLM API endpoint

    Returns:
        Updated file content as string with diff applied

    Raises:
        APIError: If LLM processing fails

    Example:
        >>> updated = call_llm_for_apply(
        ...     file_path='utils.py',
        ...     original_content='def old(): pass',
        ...     file_diff='''@@ -1 +1 @@
        ...                  -def old()
        ...                  +def new()''',
        ...     model='deepseek-reasoner'
        ... )
        >>> print(updated)
        def new(): pass"""

    system_prompt = """Please apply the diff to this file. Return the result in a block. Write the entire file.

1. Carefully apply all changes from the diff
2. Preserve surrounding context that isn't changed
3. Only return the final file content, do not add any additional markup and do not add a code block
4. You must return the entire file. It overwrites the existing file."""

    user_prompt = f"""File: {file_path}
File contents:
<filecontents>
{original_content}
</filecontents>

Diff to apply:
<diff>
{file_diff}
</diff>"""

    if model == "gemini-2.0-flash-thinking-exp-01-21":
        user_prompt = system_prompt+"\n"+user_prompt
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    if api_key is None:
        api_key = os.getenv('GPTDIFF_LLM_API_KEY')
    if base_url is None:
        base_url = os.getenv('GPTDIFF_LLM_BASE_URL', "https://nano-gpt.com/api/v1/")
    client = OpenAI(api_key=api_key, base_url=base_url)
    start_time = time.time()
    response = client.chat.completions.create(model=model,
        messages=messages,
        temperature=0.0,
        max_tokens=30000)
    full_response = response.choices[0].message.content

    elapsed = time.time() - start_time
    minutes, seconds = divmod(int(elapsed), 60)
    time_str = f"{minutes}m {seconds}s" if minutes else f"{seconds}s"
    print(f"Smartapply time: {time_str}")
    print("-" * 40)
    return full_response

def build_environment_from_filelist(file_list, cwd):
    """Build environment string from list of file paths"""
    files_dict = {}
    for file_path in file_list:
        relative_path = os.path.relpath(file_path, cwd)
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            files_dict[relative_path] = content
        except UnicodeDecodeError:
            print(f"Skipping file {file_path} due to UnicodeDecodeError")
            continue
        except IOError as e:
            print(f"Error reading {file_path}: {e}")
            continue
    return build_environment(files_dict)

def main():
    # Adding color support for Windows CMD
    if os.name == 'nt':
        os.system('color')

    args = parse_arguments()

    # TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url="https://nano-gpt.com/api/v1/")'
    # openai.api_base = "https://nano-gpt.com/api/v1/"
    if len(sys.argv) < 2:
        print("Usage: python script.py '<user_prompt>' [--apply]")
        sys.exit(1)

    user_prompt = sys.argv[1]
    project_dir = os.getcwd()
    enc = tiktoken.get_encoding("o200k_base")


    # Load project files, defaulting to current working directory if no additional paths are specified
    if not args.files:
        project_files = load_project_files(project_dir, project_dir)
    else:
        project_files = []
        for additional_path in args.files:
            if os.path.isfile(additional_path):
                with open(additional_path, 'r') as f:
                    project_files.append((additional_path, f.read()))
            elif os.path.isdir(additional_path):
                project_files.extend(load_project_files(additional_path, project_dir))

    if args.prepend:
        prepend = load_prepend_file(args.prepend)
        print("Including prepend",len(enc.encode(json.dumps(prepend))), "tokens")
    else:
        prepend = ""

    # Prepare system prompt
    system_prompt = prepend + f"Output a git diff into a <diff> block."

    files_content = ""
    for file, content in project_files:
        print(f"Including {len(enc.encode(content)):5d} tokens", absolute_to_relative(file))

        # Prepare the prompt for GPT-4
        files_content += f"File: {absolute_to_relative(file)}\nContent:\n{content}\n"

    full_prompt = f"{system_prompt}\n\n{user_prompt}\n\n{files_content}"
    token_count = len(enc.encode(full_prompt))
    if args.model is None:
        args.model = os.getenv('GPTDIFF_MODEL', 'deepseek-reasoner')

    if not args.call and not args.apply:
        with open('prompt.txt', 'w') as f:
            f.write(full_prompt)
        print(f"Total tokens: {token_count:5d}")
        print(f"\033[1;32mNot calling GPT-4.\033[0m")  # Green color for success message
        print('Instead, wrote full prompt to prompt.txt. Use `xclip -selection clipboard < prompt.txt` then paste into chatgpt')
        print(f"Total cost: ${0.0:.4f}")
        exit(0)
    else:
        # Validate API key presence before any API operations
        if not os.getenv('GPTDIFF_LLM_API_KEY'):
            print("\033[1;31mError: GPTDIFF_LLM_API_KEY environment variable required\033[0m")
            print("Set it with: export GPTDIFF_LLM_API_KEY='your-key'")
            sys.exit(1)

        # Confirm large requests without specified files
        if (not args.nowarn) and (not args.files) and token_count > 10000 and (args.call or args.apply):
            print(f"\033[1;33mThis is a larger request ({token_count} tokens). Disable this warning with --nowarn. Are you sure you want to send it? [y/N]\033[0m")
            confirmation = input().strip().lower()
            if confirmation != 'y':
                print("Request canceled")
                sys.exit(0)
        full_text, diff_text, prompt_tokens, completion_tokens, total_tokens, cost = call_llm_for_diff(system_prompt, user_prompt, files_content, args.model, 
                                                                                                    temperature=args.temperature,
                                                                                                    api_key=os.getenv('GPTDIFF_LLM_API_KEY'),
                                                                                                    base_url=os.getenv('GPTDIFF_LLM_BASE_URL', "https://nano-gpt.com/api/v1/"),
                                                                                                    max_tokens=args.max_tokens
                                                                                                    ) 

    if(diff_text.strip() == ""):
        print(f"\033[1;33mThere was no data in this diff. The LLM may have returned something invalid.\033[0m")
        print("Unable to parse diff text. Full response:", full_text)
        if args.beep:
            print("\a")  # Terminal bell for completion notification
        return

    # Output result
    elif args.apply:
        print("\nAttempting apply with the following diff:")
        print("\n<diff>")
        print(diff_text)
        print("\n</diff>")
        print("Saved to patch.diff")
        if apply_diff(project_dir, diff_text):
            print(f"\033[1;32mPatch applied successfully with 'git apply'.\033[0m")  # Green color for success message
        else:
            print("Apply failed, attempting smart apply.")
            parsed_diffs = parse_diff_per_file(diff_text)
            print("Found", len(parsed_diffs), " files in diff, calling smartdiff for each file concurrently:")

            if(len(parsed_diffs) == 0):
                print(f"\033[1;33mThere were no entries in this diff. The LLM may have returned something invalid.\033[0m")
                if args.beep:
                    print("\a")  # Terminal bell for completion notification
                return

            threads = []

            def process_file(file_path, file_diff):
                full_path = Path(project_dir) / file_path
                print(f"Processing file: {file_path}")
                
                # Handle file deletions from diff
                if '+++ /dev/null' in file_diff:
                    if full_path.exists():
                        full_path.unlink()
                        print(f"\033[1;32mDeleted file {file_path}.\033[0m")
                    else:
                        print(f"\033[1;33mFile {file_path} not found - skipping deletion\033[0m")
                    return

                original_content = ''
                if full_path.exists():
                    try:
                        original_content = full_path.read_text()
                    except UnicodeDecodeError:
                        print(f"Skipping binary file {file_path}")
                        return

                print("-" * 40)
                print("SMARTAPPLY")
                print(file_diff)
                print("-" * 40)
                try:
                    updated_content = call_llm_for_apply_with_think_tool_available(file_path, original_content, file_diff, args.model)

                    if updated_content.strip() == "":
                        print("Cowardly refusing to write empty file to", file_path, "merge failed")
                        return

                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(updated_content)
                    print(f"\033[1;32mSuccessful 'smartapply' update {file_path}.\033[0m")
                except Exception as e:
                    print(f"\033[1;31mFailed to process {file_path}: {str(e)}\033[0m")

            threads = []
            for file_path, file_diff in parsed_diffs:
                thread = threading.Thread(
                    target=process_file,
                    args=(file_path, file_diff)
                )
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()

    
    if args.beep:
        print("\a")  # Terminal bell for completion notification

    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Completion tokens: {completion_tokens}")
    print(f"Total tokens: {total_tokens}")
    #print(f"Total cost: ${cost:.4f}")
