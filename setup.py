from setuptools import setup

setup(
    name='bird2board',
    version='0.1.0',
    packages=['bird2board'],
    url='https://github.com/ihuston/bird2board',
    license='MIT',
    author='Ian Huston',
    author_email='ian@ianhuston.net',
    description='Convert Twitter Bookmarks to Pinboard bookmarks',
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
