# GPTDiff

GPTDiff uses GPT-4 to generate git diffs. The codebase in the current working directory is included in a generated prompt.txt file that you can copy and paste into chatgpt. You can also invoke the API and try to directly apply the patch (this often doesn't work).

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

OpenAI will not be called unless you specify --call

## Usage

After installing the package, you can use the `gptdiff` command in your terminal. You need to provide a prompt that runs on the codebase:

```bash
gptdiff '<user_prompt>'
```

You can also apply the generated git diff with the `--apply` flag:

```bash
gptdiff '<user_prompt>' --apply
```

## Dependencies

The `gptdiff` package depends on the `argparse` and `openai` packages.

## License

This project is licensed under the terms of the MIT license.

