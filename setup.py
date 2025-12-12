#!/usr/bin/env python3
"""
Video Upscaler Pro - Setup Script
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Version
__version__ = "0.1.0"

setup(
    name="video-upscaler-pro",
    version=__version__,
    author="Video Upscaler Pro Contributors",
    author_email="your.email@example.com",
    description="Open source video upscaling application using AI models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/video-upscaler-pro",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/video-upscaler-pro/issues",
        "Source": "https://github.com/yourusername/video-upscaler-pro",
        "Documentation": "https://github.com/yourusername/video-upscaler-pro/wiki",
    },
    packages=find_packages(exclude=["tests", "tests.*", "benchmarks", "docs"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "pytest-cov>=4.1.0",
            "pre-commit>=3.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "video-upscaler=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json"],
    },
    zip_safe=False,
)
