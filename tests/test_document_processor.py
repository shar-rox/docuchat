"""
Unit tests for DocumentProcessor module.
"""

import pytest
import os
from src.document_processor import DocumentProcessor, DocumentChunk


class TestDocumentProcessor:
    """Test suite for DocumentProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = DocumentProcessor(
            chunk_size=500,
            chunk_overlap=100
        )
    
    def test_initialization(self):
        """Test processor initialization with custom parameters."""
        assert self.processor.chunk_size == 500
        assert self.processor.chunk_overlap == 100
        assert self.processor.max_chunks_per_doc == 500
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        dirty_text = "This  is   a    test.   Page 42  "
        clean = self.processor.clean_text(dirty_text)
        
        assert "This is a test." in clean
        assert "  " not in clean  # No double spaces
        assert "Page" not in clean  # Page numbers removed
    
    def test_clean_text_special_chars(self):
        """Test special character handling in text cleaning."""
        text_with_special = "Hello © World™ - this is a test!"
        clean = self.processor.clean_text(text_with_special)
        
        assert "Hello" in clean
        assert "World" in clean
        assert "-" in clean  # Hyphens preserved
        assert "!" in clean  # Punctuation preserved
    
    def test_document_chunk_creation(self):
        """Test DocumentChunk dataclass."""
        chunk = DocumentChunk(
            text="Sample text",
            metadata={"source": "test.pdf", "pages": [1]},
            chunk_id="test_chunk_0"
        )
        
        assert chunk.text == "Sample text"
        assert chunk.metadata["source"] == "test.pdf"
        assert chunk.chunk_id == "test_chunk_0"
    
    def test_create_chunks_basic(self):
        """Test basic chunk creation from page texts."""
        page_texts = {
            1: "This is the first page with some content.",
            2: "This is the second page with more content."
        }
        
        chunks = self.processor.create_chunks(page_texts, "test.pdf")
        
        assert len(chunks) > 0
        assert all(isinstance(c, DocumentChunk) for c in chunks)
        assert all("test.pdf" in c.metadata["source"] for c in chunks)
    
    def test_create_chunks_with_overlap(self):
        """Test that chunks have proper overlap."""
        # Create a long text that will require multiple chunks
        long_text = "word " * 200  # 1000 characters
        page_texts = {1: long_text}
        
        chunks = self.processor.create_chunks(page_texts, "test.pdf")
        
        # Should create multiple chunks due to length
        assert len(chunks) > 1
        
        # Check overlap exists between consecutive chunks
        if len(chunks) >= 2:
            # Some content from chunk 0 should appear in chunk 1
            chunk0_end = chunks[0].text[-50:]
            chunk1_start = chunks[1].text[:100]
            # At least some words should overlap
            overlap_words = set(chunk0_end.split()) & set(chunk1_start.split())
            assert len(overlap_words) > 0
    
    def test_max_chunks_limit(self):
        """Test that max_chunks_per_doc limit is respected."""
        processor = DocumentProcessor(
            chunk_size=100,
            chunk_overlap=20,
            max_chunks_per_doc=5
        )
        
        # Create very long text
        long_text = "word " * 1000
        page_texts = {1: long_text}
        
        chunks = processor.create_chunks(page_texts, "test.pdf")
        
        # Should respect the limit
        assert len(chunks) <= 5
    
    def test_page_mapping(self):
        """Test that page numbers are correctly mapped to chunks."""
        page_texts = {
            1: "Content on page one. " * 10,
            2: "Content on page two. " * 10
        }
        
        chunks = self.processor.create_chunks(page_texts, "test.pdf")
        
        # Each chunk should have page metadata
        for chunk in chunks:
            assert "pages" in chunk.metadata
            assert isinstance(chunk.metadata["pages"], list)
            assert len(chunk.metadata["pages"]) > 0
    
    # Note: Tests for PDF extraction would require sample PDF files
    # These should be added in integration tests
    
    def test_extract_text_file_not_found(self):
        """Test error handling for missing PDF file."""
        with pytest.raises(FileNotFoundError):
            self.processor.extract_text_from_pdf("nonexistent.pdf")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
