#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from pathlib import Path

# Build the long description using README & HISTORY
readme = (Path(__file__).parent / "README.md").read_text()
history = (Path(__file__).parent / "HISTORY.md").read_text()
long_description = readme + history

requirements = [
    "watchdog>=3.0.0",
    "requests>=2.31.0",
    "tabulate>=0.9.0",
    "click>=8.1.3",
    "img_processor>=0.20.0",
]

setup_requirements = []

test_requirements = []

setup(
    author="Justin Keller",
    author_email="kellerjustin@protonmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="REST API Uploader",
    entry_points={"console_scripts": ["rest_uploader=rest_uploader.cli:main"]},
    install_requires=requirements,
    license="MIT license",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=["rest_uploader", "joplin", "rest-uploader"],
    name="rest_uploader",
    packages=find_packages(include=["rest_uploader"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/kellerjustin/rest-uploader",
    version="1.20.0",
    zip_safe=False,
)
