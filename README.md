# 🤖 DocuChat - Intelligent Document Q&A System

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Ask questions about your documents and get accurate, cited answers using RAG (Retrieval-Augmented Generation) and LLMs

## 🌟 Features

- 📄 **Multi-document support**: Upload and query multiple PDFs simultaneously
- 🔍 **Semantic search**: Find relevant context using state-of-the-art vector embeddings
- 🤖 **AI-powered answers**: Generate accurate responses with citations
- 📌 **Source citations**: Every answer includes document references with page numbers
- ⚡ **Fast retrieval**: Efficient vector search with ChromaDB
- 💬 **Conversation mode**: Ask follow-up questions naturally

## 🏗️ Architecture

```
PDF Documents → Document Processor → Chunks
                                       ↓
User Query → Embeddings ←→ Vector Store (ChromaDB)
                ↓
          Retriever (Top-K chunks)
                ↓
            LLM + RAG → Answer with Citations
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/shar-rox/docuchat.git
cd docuchat

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Usage

```bash
# Process documents
python -m src.cli process --input data/sample_docs/

# Ask questions
python -m src.cli query "What are the main findings in the research paper?"

# Interactive mode
python -m src.cli chat
```

## 📊 How It Works

1. **Document Ingestion**: PDFs are extracted and split into semantic chunks (500-1000 tokens)
2. **Embedding Generation**: Text chunks are converted to dense vector representations
3. **Vector Storage**: Embeddings are stored in ChromaDB for efficient similarity search
4. **Query Processing**: User questions are embedded using the same model
5. **Context Retrieval**: Top-k most relevant chunks are retrieved via cosine similarity
6. **Answer Generation**: LLM generates contextual answers from retrieved chunks
7. **Citation**: Sources are displayed with document names and page numbers

## 🛠️ Tech Stack

- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB
- **LLM**: OpenAI GPT-4 / Anthropic Claude (configurable)
- **Framework**: LangChain
- **PDF Processing**: PyMuPDF
- **CLI**: Rich (beautiful terminal output)

## 📈 Project Status

- [x] Day 1: Project setup & document processing
- [ ] Day 2: Vector embeddings & ChromaDB integration
- [ ] Day 3: Retrieval system implementation
- [ ] Day 4: LLM integration & RAG pipeline
- [ ] Day 5: CLI interface & UX
- [ ] Day 6: Testing & documentation
- [ ] Day 7: Docker & deployment

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 📁 Project Structure

```
docuchat/
├── src/                    # Source code
│   ├── document_processor.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── llm_interface.py
│   ├── rag_pipeline.py
│   └── cli.py
├── tests/                  # Test suite
├── data/                   # Sample documents
├── config/                 # Configuration files
├── docs/                   # Documentation
└── notebooks/              # Jupyter notebooks
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by modern RAG architectures used in production AI systems
- Built with open-source tools and libraries

---

**Note**: This is a portfolio project demonstrating practical AI/ML skills including NLP, vector search, and LLM integration.
