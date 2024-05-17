# GPTDiff

Send your entire codebase to gpt and get a changeset.

```bash
cd myproject
gptdiff 'add hover effects to the buttons'
```

Generates a prompt.txt file that you can copy and paste into a large context gpt to have a conversation with suggested changes. You can also invoke the API and try to directly apply the patch (this often doesn't work).

## Installation

Requires Python. Clone this repo and run:

```bash
python setup.py install
```

## Configuration

To call openai from the command line, you need to set the `OPENAI_API_KEY` environment variable:

```bash
export OPENAI_API_KEY='your-openai-api-key'
```

OpenAI will not be called unless you specify `--call` or `--apply`

Prevent files being appended to the prompt by adding them to `.gitignore` or `.gptignore`

## Usage

After installing the package, you can use the `gptdiff` command in your terminal. cd into your codebase and run:

```bash
gptdiff '<user_prompt>'
```

any files that are included in .gitignore are ignored when generating prompt.txt.

## Autopatch with --apply

You can also call openai and automatically apply the generated git diff with the `--apply` flag:

```bash
gptdiff '<user_prompt>' --apply
```

This often generates incorrect diffs that need to be manually merged.

## Dependencies

The `gptdiff` package depends on the `argparse` and `openai` packages.

## License

This project is licensed under the terms of the MIT license.

