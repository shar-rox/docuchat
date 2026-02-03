"""
DocuChat - Intelligent Document Q&A System

A RAG-based question-answering system that allows users to query 
PDF documents using natural language and receive accurate, cited answers.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .document_processor import DocumentProcessor
from .embeddings import EmbeddingGenerator
from .vector_store import VectorStore
from .retriever import Retriever
from .rag_pipeline import RAGPipeline

__all__ = [
    "DocumentProcessor",
    "EmbeddingGenerator", 
    "VectorStore",
    "Retriever",
    "RAGPipeline",
]
