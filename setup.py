from setuptools import setup, find_packages

setup(
    name='gptdiff',
    version='0.1.0',
    description='A tool to generate and apply git diffs using LLMs',
    author='255labs',
    packages=find_packages(),  # Use find_packages() to automatically discover packages
    package_data={'gptdiff': []},  # Add any package data if needed
    install_requires=[
        'openai>=1.0.0',
        'tiktoken>=0.5.0',
        'ai_agent_toolbox>=0.1.0'
    ],
    extras_require={
        'test': ['pytest', 'pytest-mock'],
        'docs': ['mkdocs', 'mkdocs-material']
    },
    entry_points={
        'console_scripts': ['gptdiff=gptdiff.gptdiff:main'],
    },
    license='MIT',  # Specify the license type (e.g., MIT, Apache 2.0, etc.)
    license_files=('LICENSE.txt',),  # Include the license file(s)
)
