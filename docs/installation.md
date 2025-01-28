# Installation

## Prerequisites
- Python 3.8 or higher

## Install via pip

To install `gptdiff` from PyPI, run the following command:

```bash
pip install gptdiff
pip install tiktoken  # For token counting
```

## Development Installation (if no pip package is available yet)

If the `gptdiff` package is not yet available on PyPI, you can install it from the source code:

```bash
git clone https://github.com/255BITS/gptdiff.git
cd gptdiff
python setup.py install
```

## Configuration

### API Key and Base URL

To use `gptdiff`, you need an API key from [nano-gpt.com/api](https://nano-gpt.com/api). Once you get your API key, you need to set up the following environment variables.

#### Linux/MacOS
```bash
export GPTDIFF_LLM_API_KEY='your-api-key'
# Optional: For switching API providers
export GPTDIFF_MODEL='deepseek-reasoner'  # Default model
export GPTDIFF_LLM_BASE_URL='https://nano-gpt.com/api/v1/'
```

#### Windows
```cmd
set GPTDIFF_LLM_API_KEY=your-api-key
rem Optional: For switching API providers
set GPTDIFF_LLM_BASE_URL=https://nano-gpt.com/api/v1/
```

The default base URL points to `nano-gpt.com`'s API. Supported models can be specified with:

```bash
gptdiff 'your prompt' --model $GPTDIFF_MODEL
```