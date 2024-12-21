#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aliyundrive-api",
    version="0.1.0",
    author="__LittleQ__",
    author_email="",
    description="阿里云盘 API 的 Python 实现",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Litt1eQ/aliyundrive-api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
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