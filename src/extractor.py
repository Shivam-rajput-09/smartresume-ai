"""
SmartResume AI — Resume Text Extraction Engine

Handles extracting raw text from PDF and TXT resume files with robust
error handling, encoding detection, and fallback parsing mechanisms.
"""

import os
from pathlib import Path
from typing import Dict, Any, Union
import PyPDF2
import pdfplumber

from config import Config


class ResumeExtractorError(Exception):
    """Custom exception class for resume extraction failures."""
    pass


class ResumeExtractor:
    """Extracts clean text content and metadata from PDF and TXT documents."""
    
    ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS
    
    @classmethod
    def is_allowed_file(cls, filename: str) -> bool:
        """Validates if the uploaded filename has an allowed extension."""
        if not filename or '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in cls.ALLOWED_EXTENSIONS

    @classmethod
    def extract_from_txt(cls, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Extracts text from a plain text file using UTF-8 with fallback
        to latin-1 and cp1252 encodings.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
            
        encodings = ['utf-8', 'latin-1', 'cp1252']
        text = ""
        
        for enc in encodings:
            try:
                with open(path, 'r', encoding=enc) as f:
                    text = f.read()
                break
            except UnicodeDecodeError:
                continue
                
        cleaned_text = text.strip()
        if not cleaned_text:
            raise ResumeExtractorError("The uploaded TXT resume is empty.")
            
        return {
            "status": "success",
            "file_type": "txt",
            "file_name": path.name,
            "text": cleaned_text,
            "char_count": len(cleaned_text),
            "word_count": len(cleaned_text.split()),
            "num_pages": 1
        }

    @classmethod
    def extract_from_pdf(cls, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Extracts text from a PDF resume using pdfplumber as the primary
        high-fidelity layout engine, with PyPDF2 as an automated fallback.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
            
        extracted_pages = []
        num_pages = 0
        
        # 1. Primary Extraction Method: pdfplumber
        try:
            with pdfplumber.open(path) as pdf:
                num_pages = len(pdf.pages)
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_pages.append(page_text.strip())
        except Exception as primary_error:
            extracted_pages = []  # Reset for fallback

        # 2. Fallback Extraction Method: PyPDF2 (if pdfplumber extracted nothing or failed)
        if not extracted_pages:
            try:
                with open(path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    if reader.is_encrypted:
                        try:
                            reader.decrypt('')
                        except Exception:
                            raise ResumeExtractorError("The PDF is password protected and cannot be read.")
                    num_pages = len(reader.pages)
                    for page in reader.pages:
                        t = page.extract_text()
                        if t:
                            extracted_pages.append(t.strip())
            except Exception as e:
                raise ResumeExtractorError(f"Failed to extract text from PDF: {str(e)}")

        full_text = "\n\n".join(extracted_pages).strip()
        if not full_text:
            raise ResumeExtractorError(
                "Unable to extract readable text from this PDF. "
                "The file may be a scanned image-only PDF or empty."
            )
            
        return {
            "status": "success",
            "file_type": "pdf",
            "file_name": path.name,
            "text": full_text,
            "char_count": len(full_text),
            "word_count": len(full_text.split()),
            "num_pages": num_pages
        }

    @classmethod
    def extract_text(cls, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Master extraction dispatcher. Identifies file format and calls
        the appropriate parser.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")
            
        ext = path.suffix.lower().lstrip('.')
        if ext == 'pdf':
            return cls.extract_from_pdf(path)
        elif ext in ['txt', 'text']:
            return cls.extract_from_txt(path)
        else:
            raise ResumeExtractorError(
                f"Unsupported file format: .{ext}. Allowed formats: {', '.join(cls.ALLOWED_EXTENSIONS)}"
            )


# Convenient module-level function
def extract_resume_text(file_path: Union[str, Path]) -> Dict[str, Any]:
    return ResumeExtractor.extract_text(file_path)
