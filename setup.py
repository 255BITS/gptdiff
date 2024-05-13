from setuptools import setup, find_packages

setup(
    name='gptdiff',
    version='0.1.0',
    description='A tool to generate git diffs using GPT-4',
    author='255labs',
    packages=['gptdiff'],
    install_requires=[
        'argparse',
        'openai',
    ],
    entry_points={
        'console_scripts': ['gptdiff=gptdiff.gptdiff:main'],
    }
)
