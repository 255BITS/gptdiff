#!/usr/bin/env python3

import openai
import tiktoken

import os
import json
import subprocess
from pathlib import Path
import sys
import fnmatch
import argparse
import pkgutil
import re

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

# Load API key from environment variable
NANOGPT_API_KEY = os.getenv('NANOGPT_API_KEY')

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
    ignore_paths = [Path(cwd) / ".gitignore", Path(cwd) / ".gptignore"]
    gitignore_patterns = ["developer.json", ".gitignore", "diff.patch", "prompt.txt", ".gptignore", "*.pdf", "*.docx", ".git"]

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

def load_developer_persona(developer_file):
    try:
        with open(developer_file, 'r') as f:
            developer_persona = json.load(f)
    except FileNotFoundError:
        # Load the default developer.json from the pip package if not found
        developer_json = pkgutil.get_data(__package__, 'developer.json').decode('utf-8')
        developer_persona = json.loads(developer_json)
    return developer_persona

# Function to call GPT-4 API and calculate the cost
def call_gpt4_api(system_prompt, user_prompt, files_content, model):
    openai.api_key = NANOGPT_API_KEY
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt + "\n\n"+files_content},
    ]
    #print(messages)

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=1500,  # Adjust as necessary
        temperature=0.7
    )

    prompt_tokens = response.usage['prompt_tokens']
    completion_tokens = response.usage['completion_tokens']
    total_tokens = response.usage['total_tokens']

    # Now, these rates are updated to per million tokens
    cost_per_million_prompt_tokens = 30
    cost_per_million_completion_tokens = 60
    cost = (prompt_tokens / 1_000_000 * cost_per_million_prompt_tokens) + (completion_tokens / 1_000_000 * cost_per_million_completion_tokens)

    full_response = response.choices[0].message['content'].strip()

    # Find first code block start (```diff or ```)
    lines = full_response.split('\n')
    start_idx = next((i for i, line in enumerate(lines) if line.strip().startswith('```')), -1)
 
    if start_idx == -1:
        diff_response = ''
        return full_response, diff_response, prompt_tokens, completion_tokens, total_tokens, cost
    # Look for closing ``` that's on its own line
    end_idx = next((i for i, line in enumerate(lines[start_idx+1:], start_idx+1)
                   if line.strip() == '```'), -1)

    if end_idx == -1:
        # Try looking for any closing backticks as fallback
        end_idx = next((i for i, line in enumerate(lines[start_idx+1:], start_idx+1) if '```' in line), -1)
        diff_response = ''
    else: 
        diff_response = '\n'.join(lines[start_idx+1:end_idx])
     

    return full_response, diff_response, prompt_tokens, completion_tokens, total_tokens, cost

# Function to apply diff to project files
def apply_diff(project_dir, diff_text):
    diff_file = Path(project_dir) / "diff.patch"
    with open(diff_file, 'w') as f:
        f.write(diff_text)
    
    result = subprocess.run(["git", "apply", str(diff_file)], cwd=project_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"\033[1;31mError running 'git apply diff.patch': {result.stderr}\033[0m")  # Red color for error message
    else:
        print(f"\033[1;32mPatch applied successfully.\033[0m")  # Green color for success message

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate and optionally apply git diffs using GPT-4.')
    parser.add_argument('prompt', type=str, help='Prompt that runs on the codebase.')
    parser.add_argument('--smartapply', action='store_true', help='Apply diff by having AI rewrite each file individually')

    parser.add_argument('--apply', action='store_true', help='Attempt to apply the generated git diff.')
    parser.add_argument('--developer', type=str, default='developer.json', help='Path to developer persona JSON file. It can contain any information about the developer that is writing the diff. Such as name, education, code style, etc. Defaults to included https://github.com/255BITS/gptdiff/blob/main/developer.json')

    # New flag --prompt that does not call the API but instead writes the full prompt to prompt.txt
    parser.add_argument('--call', action='store_true',
                        help='Call the GPT-4 API. Writes the full prompt to prompt.txt if not specified.')
    parser.add_argument('files', nargs='*', default=[], help='Specify additional files or directories to include.')
    parser.add_argument('--model', type=str, default='deepseek-reasoner', help='Model to use for the API call.')


    return parser.parse_args()

def absolute_to_relative(absolute_path):
    cwd = os.getcwd()
    relative_path = os.path.relpath(absolute_path, cwd)
    return relative_path

def parse_diff_per_file(diff_text):
    diffs = []
    current_diff = []
    file_path = None

    for line in diff_text.split('\n'):
        if line.startswith('diff --git'):
            if current_diff and file_path:
                diffs.append((file_path, '\n'.join(current_diff)))
            current_diff = [line]
            file_path = None
        elif line.startswith('+++ '):
            # Extract target file path from +++ line
            file_path = line[4:].strip()
            if file_path.startswith('b/'):
                file_path = file_path[2:]
            current_diff.append(line)
        elif file_path:
            current_diff.append(line)

    if current_diff and file_path:
        diffs.append((file_path, '\n'.join(current_diff)))

    return diffs

def call_llm_for_apply(file_path, original_content, file_diff, model):
    openai.api_key = NANOGPT_API_KEY

    system_prompt = """Please apply the diff to this file. Return the result in a block. Write the entire file.

1. Carefully apply all changes from the diff
2. Preserve surrounding context that isn't changed
3. Only return the final file content in a code block"""

    user_prompt = f"""File: {file_path}
File contents:
```filecontents
{original_content}
```

Diff to apply:
```isolateddiff
{file_diff}
```"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.0,
        max_tokens=4000
    )

    content = response.choices[0].message['content'].strip()

    # Extract code block contents
    match = re.search(r'```[^\n]*\n(.*?)```', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return content

def main():
    # Adding color support for Windows CMD
    if os.name == 'nt':
        os.system('color')

    args = parse_arguments()

    openai.api_key = NANOGPT_API_KEY
    openai.api_base = "https://nano-gpt.com/api/v1/"
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
 
    developer_persona = load_developer_persona(args.developer)
    print("Including developer.json",len(enc.encode(json.dumps(developer_persona))), "tokens")

    # Prepare system prompt
    system_prompt = f"You are this agent: <json>{json.dumps(developer_persona)}</json>\n\nFollow the user request. Output a git diff into a ``` block. State who you are and what you are trying to do. Do not worry about getting it wrong, just try."

    files_content = ""
    for file, content in project_files:
        print(f"Including {len(enc.encode(content)):5d} tokens", absolute_to_relative(file))

        # Prepare the prompt for GPT-4
        files_content += f"File: {absolute_to_relative(file)}\nContent:\n{content}\n"

    if not args.call and not args.apply:
        full_prompt = system_prompt + '\n\n' + user_prompt + '\n\n' + files_content
        with open('prompt.txt', 'w') as f:
            f.write(full_prompt)
        print(f"Total tokens: {len(enc.encode(full_prompt)):5d}")
        print(f"\033[1;32mNot calling GPT-4.\033[0m")  # Green color for success message
        print('Instead, wrote full prompt to prompt.txt. Use `xclip -selection clipboard < prompt.txt` then paste into chatgpt')
        print(f"Total cost: ${0.0:.4f}")
        exit(0)
    else:
        full_text, diff_text, prompt_tokens, completion_tokens, total_tokens, cost = call_gpt4_api(system_prompt, user_prompt, files_content, args.model)


    if args.apply:
        print("Attempting changes:")
        print("```")
        print(diff_text)
        print("```")
        # Apply the diff
        apply_diff(project_dir, diff_text)
    else:
        print(f"\033[1;32mFull response.\033[0m")  # Green color for success message
        print(full_text)

    # Output result
    if args.smartapply:
        print("\nAttempting smart apply:")
        parsed_diffs = parse_diff_per_file(diff_text)
        
        total_files = len(parsed_diffs)
        for i, (file_path, file_diff) in enumerate(parsed_diffs):
            full_path = Path(project_dir) / file_path
            print(f"Processing file {i+1}/{total_files}: {file_path}")
            
            original_content = ''
            if full_path.exists():
                try:
                    original_content = full_path.read_text()
                except UnicodeDecodeError:
                    print(f"Skipping binary file {file_path}")
                    continue

            try:
                updated_content = call_llm_for_apply(file_path, original_content, file_diff, args.model)
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(updated_content)
                print(f"Successfully updated {file_path}")
            except Exception as e:
                print(f"Failed to process {file_path}: {str(e)}")
                if original_content:
                    full_path.write_text(original_content)  # Restore original content
        
        print("Smart apply completed")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Completion tokens: {completion_tokens}")
    print(f"Total tokens: {total_tokens}")
    print(f"Total cost: ${cost:.4f}")

if __name__ == "__main__":
    main()

