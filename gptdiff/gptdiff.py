#!/usr/bin/env python3

import openai
import os
import json
import subprocess
from pathlib import Path
import sys
import fnmatch
import argparse
import pkgutil

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
            if fnmatch.fnmatch(str(filepath), pattern) or fnmatch.fnmatch(str(filepath.relative_to(Path.cwd())), pattern):
                ignored = True
            if pattern.endswith('/') and (str(filepath).startswith(str(Path(pattern[:-1]).resolve()))) or str(filepath.relative_to(Path.cwd())).startswith(pattern[:-1]):
                ignored = True

    # Ensure .gitignore itself is not ignored unless explicitly mentioned
    if filepath.name == ".gitignore" and not any(pattern == ".gitignore" for pattern in gitignore_patterns):
        ignored = False

    return ignored

# Load API key from environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Function to load project files considering .gitignore
def load_project_files(project_dir, cwd):
    ignore_paths = [Path(cwd) / ".gitignore", Path(cwd) / ".gptignore"]
    gitignore_patterns = ["developer.json", ".gitignore", "diff.patch", "prompt.txt", ".gitignore", ".gptignore"]

    for p in ignore_paths:
        if p.exists():
            with open(p, 'r') as f:
                gitignore_patterns.extend([line.strip() for line in f if line.strip() and not line.startswith('#')])

    project_files = []
    for root, _, files in os.walk(project_dir):
        for file in files:
            filepath = os.path.relpath(os.path.join(root, file), project_dir)
            if not is_ignored(filepath, gitignore_patterns):
                print("Including", filepath)
                with open(os.path.join(root, file), 'r') as f:
                    project_files.append((filepath, f.read()))
    
    print("")
    return project_files

def load_developer_persona(developer_file):
    try:
        with open(developer_file, 'r') as f:
            developer_persona = json.load(f)
    except FileNotFoundError:
        # Load the default developer.json from the pip package if not found
        developer_persona = json.loads(pkgutil.get_data(__package__, 'developer.json').decode('utf-8'))
    return developer_persona

# Function to call GPT-4 API and calculate the cost
def call_gpt4_api(system_prompt, user_prompt, files_content):
    openai.api_key = OPENAI_API_KEY
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt + "\n\n"+files_content},
    ]
    #print(messages)

    response = openai.ChatCompletion.create(
        model="gpt-4",
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
    git_diff_start = full_response.find('```')

    if git_diff_start == -1:
        diff_response = ''
    git_diff_end = full_response.rfind('```')
    if git_diff_end == -1 or git_diff_end <= git_diff_start:
        diff_response = ''
    diff_response = full_response[git_diff_start+6:git_diff_end]
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

    parser.add_argument('--apply', action='store_true', help='Attempt to apply the generated git diff.')
    parser.add_argument('--developer', type=str, default='developer.json', help='Path to developer persona JSON file. It can contain any information about the developer that is writing the diff. Such as name, education, code style, etc. Defaults to included https://github.com/255BITS/gptdiff/blob/main/developer.json')

    # New flag --prompt that does not call the API but instead writes the full prompt to prompt.txt
    parser.add_argument('--call', action='store_true',
                        help='Call the GPT-4 API. Writes the full prompt to prompt.txt if not specified.')
    parser.add_argument('files', nargs='*', default=[], help='Specify additional files or directories to include.')



    return parser.parse_args()

def main():
    # Adding color support for Windows CMD
    if os.name == 'nt':
        os.system('color')

    args = parse_arguments()
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script.py '<user_prompt>' [--apply]")
        sys.exit(1)

    user_prompt = sys.argv[1]
    project_dir = os.getcwd()

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

    # Prepare system prompt
    system_prompt = f"You are this agent: <json>{json.dumps(developer_persona)}</json>\n\nFollow the user request. Output a git diff into a ``` block. State who you are and what you are trying to do. Do not worry about getting it wrong, just try."

    # Prepare the prompt for GPT-4
    files_content = "\n".join([f"File: {file}\nContent:\n{content}" for file, content in project_files])

    if not args.call and not args.apply:
        with open('prompt.txt', 'w') as f:
            f.write(system_prompt + '\n\n' + user_prompt + '\n\n' + files_content)
        print(f"\033[1;32mNot calling GPT-4.\033[0m")  # Green color for success message
        print('Instead, wrote full prompt to prompt.txt. Use `xclip -selection clipboard < prompt.txt` then paste into chatgpt')
        print(f"Total cost: ${0.0:.4f}")
        exit(0)
    else:
        full_text, diff_text, prompt_tokens, completion_tokens, total_tokens, cost = call_gpt4_api(system_prompt, user_prompt, files_content)


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
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Completion tokens: {completion_tokens}")
    print(f"Total tokens: {total_tokens}")
    print(f"Total cost: ${cost:.4f}")

if __name__ == "__main__":
    main()

