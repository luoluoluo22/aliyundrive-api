#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aliyundrive-api",
    version="0.1.0",
    author="luoluoluo22",
    author_email="您的邮箱",
    description="阿里云盘API的Python实现",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luoluoluo22/aliyundrive-api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
        "tqdm>=4.61.0",
    ],
    entry_points={
        'console_scripts': [
            'aliyundrive=aliyundrive.cli:main',
        ],
    },
) 

