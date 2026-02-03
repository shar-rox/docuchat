"""
Setup script for DocuChat package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docuchat",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Intelligent Document Q&A System using RAG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/docuchat",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "sentence-transformers>=2.2.2",
        "chromadb>=0.4.22",
        "langchain>=0.1.0",
        "openai>=1.10.0",
        "anthropic>=0.18.1",
        "pymupdf>=1.23.21",
        "rich>=13.7.0",
        "click>=8.1.7",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-cov>=4.1.0",
            "black>=24.1.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "docuchat=src.cli:main",
        ],
    },
)
