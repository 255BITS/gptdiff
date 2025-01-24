from setuptools import setup, find_packages

setup(
    name='gptdiff',
    version='0.1.0',
    description='A tool to generate git diffs using GPT-4',
    author='255labs',
    packages=['gptdiff'],
    package_data={'gptdiff': ['developer.json']},
    install_requires=[
        'openai',
    ],
    entry_points={
        'console_scripts': ['gptdiff=gptdiff.gptdiff:main'],
    }
)