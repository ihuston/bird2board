import os

from setuptools import setup
from os import path

version = '0.1.0'

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if "GITHUB_WORKFLOW" in os.environ:
    print(f"Running inside {os.getenv('GITHUB_WORKFLOW')}")
    if os.getenv('GITHUB_WORKFLOW') == "Upload Python Package on Test PyPI":
        version = os.getenv("GITHUB_SHA")


setup(
    name='bird2board',
    version=version,
    packages=['bird2board'],
    url='https://github.com/ihuston/bird2board',
    license='MIT',
    author='Ian Huston',
    author_email='ian@ianhuston.net',
    description='Convert bird based bookmarks to board based ones.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'bird2board = bird2board.app:convert',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities"
    ],
    install_requires=[
        "requests~=2.25.1",
        "click~=8.0.1"
    ],
)
