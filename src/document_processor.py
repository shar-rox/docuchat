"""
Document Processor Module

Handles PDF extraction, text cleaning, and intelligent chunking for RAG pipeline.
"""

import os
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


@dataclass
class DocumentChunk:
    """Represents a chunk of text from a document."""
    text: str
    metadata: Dict[str, any]
    chunk_id: str
    
    def __repr__(self):
        return f"DocumentChunk(chunk_id={self.chunk_id}, length={len(self.text)})"


class DocumentProcessor:
    """
    Processes PDF documents into semantically meaningful chunks.
    
    Features:
    - Extracts text from PDFs with metadata preservation
    - Cleans and normalizes text
    - Creates overlapping chunks for better context retrieval
    - Preserves document structure and page numbers
    """
    
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 200,
        max_chunks_per_doc: Optional[int] = 500
    ):
        """
        Initialize the document processor.
        
        Args:
            chunk_size: Target size for each chunk in characters
            chunk_overlap: Number of overlapping characters between chunks
            max_chunks_per_doc: Maximum chunks to extract per document (None for unlimited)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.max_chunks_per_doc = max_chunks_per_doc
        
        logger.info(
            f"Initialized DocumentProcessor (chunk_size={chunk_size}, "
            f"overlap={chunk_overlap})"
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> Dict[int, str]:
        """
        Extract text from a PDF file, preserving page numbers.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary mapping page numbers to extracted text
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF cannot be opened or read
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            doc = fitz.open(pdf_path)
            page_texts = {}
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                page_texts[page_num + 1] = text  # 1-indexed page numbers
            
            doc.close()
            logger.info(f"Extracted text from {len(page_texts)} pages in {pdf_path}")
            return page_texts
            
        except Exception as e:
            raise ValueError(f"Error reading PDF {pdf_path}: {str(e)}")
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text: Raw text from PDF
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers/footers (common patterns)
        text = re.sub(r'Page \d+', '', text, flags=re.IGNORECASE)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-\'"]+', '', text)
        
        # Remove standalone numbers (often artifacts)
        text = re.sub(r'\b\d+\b', '', text)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        return text.strip()
    
    def create_chunks(
        self,
        page_texts: Dict[int, str],
        doc_name: str
    ) -> List[DocumentChunk]:
        """
        Create overlapping chunks from page texts.
        
        Args:
            page_texts: Dictionary of page numbers to text
            doc_name: Name of the source document
            
        Returns:
            List of DocumentChunk objects
        """
        chunks = []
        chunk_counter = 0
        
        # Combine all pages into one text with page markers
        full_text = ""
        page_mapping = {}  # Maps character positions to page numbers
        current_pos = 0
        
        for page_num in sorted(page_texts.keys()):
            page_text = self.clean_text(page_texts[page_num])
            page_start = current_pos
            page_end = current_pos + len(page_text)
            
            page_mapping[(page_start, page_end)] = page_num
            full_text += page_text + " "
            current_pos = len(full_text)
        
        # Create overlapping chunks
        start = 0
        while start < len(full_text):
            # Define chunk boundaries
            end = min(start + self.chunk_size, len(full_text))
            chunk_text = full_text[start:end]
            
            # Find which page(s) this chunk belongs to
            chunk_pages = self._get_pages_for_chunk(
                start, end, page_mapping
            )
            
            # Create chunk with metadata
            chunk = DocumentChunk(
                text=chunk_text.strip(),
                metadata={
                    "source": doc_name,
                    "pages": chunk_pages,
                    "chunk_index": chunk_counter,
                    "start_char": start,
                    "end_char": end
                },
                chunk_id=f"{doc_name}_chunk_{chunk_counter}"
            )
            
            chunks.append(chunk)
            chunk_counter += 1
            
            # Check max chunks limit
            if self.max_chunks_per_doc and chunk_counter >= self.max_chunks_per_doc:
                logger.warning(
                    f"Reached max chunks limit ({self.max_chunks_per_doc}) "
                    f"for document {doc_name}"
                )
                break
            
            # Move to next chunk with overlap
            start += self.chunk_size - self.chunk_overlap
        
        logger.info(f"Created {len(chunks)} chunks from {doc_name}")
        return chunks
    
    def _get_pages_for_chunk(
        self,
        start: int,
        end: int,
        page_mapping: Dict[tuple, int]
    ) -> List[int]:
        """
        Determine which pages a chunk spans.
        
        Args:
            start: Start character position
            end: End character position
            page_mapping: Mapping of character ranges to page numbers
            
        Returns:
            List of page numbers the chunk spans
        """
        pages = set()
        
        for (page_start, page_end), page_num in page_mapping.items():
            # Check if chunk overlaps with this page
            if not (end <= page_start or start >= page_end):
                pages.add(page_num)
        
        return sorted(list(pages))
    
    def process_document(self, pdf_path: str) -> List[DocumentChunk]:
        """
        Complete processing pipeline for a single PDF document.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of DocumentChunk objects ready for embedding
        """
        doc_name = os.path.basename(pdf_path)
        logger.info(f"Processing document: {doc_name}")
        
        # Extract text
        page_texts = self.extract_text_from_pdf(pdf_path)
        
        # Create chunks
        chunks = self.create_chunks(page_texts, doc_name)
        
        logger.info(f"Successfully processed {doc_name}: {len(chunks)} chunks created")
        return chunks
    
    def process_directory(self, dir_path: str) -> Dict[str, List[DocumentChunk]]:
        """
        Process all PDF files in a directory.
        
        Args:
            dir_path: Path to directory containing PDFs
            
        Returns:
            Dictionary mapping filenames to their chunks
        """
        if not os.path.isdir(dir_path):
            raise ValueError(f"Directory not found: {dir_path}")
        
        all_chunks = {}
        pdf_files = [f for f in os.listdir(dir_path) if f.endswith('.pdf')]
        
        logger.info(f"Found {len(pdf_files)} PDF files in {dir_path}")
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(dir_path, pdf_file)
            try:
                chunks = self.process_document(pdf_path)
                all_chunks[pdf_file] = chunks
            except Exception as e:
                logger.error(f"Failed to process {pdf_file}: {str(e)}")
                continue
        
        total_chunks = sum(len(chunks) for chunks in all_chunks.values())
        logger.info(
            f"Processed {len(all_chunks)} documents, "
            f"total {total_chunks} chunks"
        )
        
        return all_chunks


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=100)
    
    # Test with a sample PDF
    # chunks = processor.process_document("data/sample_docs/sample.pdf")
    # for chunk in chunks[:3]:
    #     print(f"\n{chunk}")
    #     print(f"Text: {chunk.text[:100]}...")
    
    print("DocumentProcessor module loaded successfully!")
