from setuptools import setup, find_packages

setup(
    name='gptdiff',
    version='0.1.8',
    description='A tool to generate and apply git diffs using LLMs',
    author='255labs',
    packages=find_packages(),  # Use find_packages() to automatically discover packages
    package_data={'gptdiff': []},  # Add any package data if needed
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'openai>=1.0.0',
        'tiktoken>=0.5.0',
        'ai_agent_toolbox>=0.1.11'
    ],
    extras_require={
        'test': ['pytest', 'pytest-mock'],
        'docs': ['mkdocs', 'mkdocs-material']
    },
    entry_points={
        'console_scripts': ['gptdiff=gptdiff.gptdiff:main'],
    },
    license=None, # Remove license argument
    # license_file='LICENSE.txt', # Remove license_file argument
    classifiers=[  # Add license classifiers
        'License :: OSI Approved :: MIT License', # Standard MIT license classifier
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
