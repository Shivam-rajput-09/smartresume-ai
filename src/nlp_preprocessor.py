"""
SmartResume AI — NLP Preprocessing & Information Extraction Engine

Implements an explainable NLP pipeline:
Cleaning -> Tokenization -> Lemmatization -> Regex Extraction -> N-Gram Skill Matching
"""

import re
import string
from typing import Dict, List, Set, Optional, Any, Tuple
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from src.dataset_loader import dataset_loader


class NLPPreprocessor:
    """Natural Language Processing engine for resume analysis and entity extraction."""
    
    def __init__(self):
        # Initialize NLTK components
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords', quiet=True)
            self.stop_words = set(stopwords.words('english'))
            
        self.lemmatizer = WordNetLemmatizer()
        
        # Load taxonomy from dataset loader
        self.known_skills = dataset_loader.get_all_known_skills()
        self.skill_categories = dataset_loader.get_skill_categories()
        
        # Regex Patterns for contact information and sections
        self.EMAIL_REGEX = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        )
        self.PHONE_REGEX = re.compile(
            r'(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{2,5}\)?[\s-]?)?\d{3,5}[\s-]?\d{4,5}'
        )
        self.LINKEDIN_REGEX = re.compile(
            r'(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+',
            re.IGNORECASE
        )
        self.GITHUB_REGEX = re.compile(
            r'(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+',
            re.IGNORECASE
        )
        
        # Standard education degrees
        self.EDUCATION_DEGREES = [
            'bca', 'bca-ai', 'mca', 'b.tech', 'btech', 'm.tech', 'mtech',
            'b.e.', 'be', 'b.sc', 'bsc', 'm.sc', 'msc', 'b.com', 'bcom',
            'bba', 'mba', 'ph.d', 'phd', 'diploma', 'bachelor of computer applications',
            'bachelor of technology', 'master of computer applications',
            'bachelor of science', 'master of science', 'bachelor', 'master'
        ]
        
        # Standard resume section headers
        self.SECTION_HEADERS = [
            'summary', 'professional summary', 'objective', 'education',
            'experience', 'work experience', 'projects', 'skills', 'technical skills',
            'certifications', 'achievements', 'awards', 'publications'
        ]

    def clean_text(self, text: str) -> str:
        """
        Cleans raw text by normalizing whitespaces, removing URLs,
        and standardizing line breaks.
        """
        if not text:
            return ""
        # Replace non-breaking spaces and tabs
        cleaned = text.replace('\xa0', ' ').replace('\t', ' ')
        # Remove multiple consecutive blank lines/spaces
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)
        cleaned = re.sub(r'\n\s*\n+', '\n\n', cleaned)
        return cleaned.strip()

    def tokenize_and_lemmatize(self, text: str) -> List[str]:
        """
        Tokenizes text into words, removes punctuation/stopwords,
        and converts words to their base lemma.
        """
        if not text:
            return []
            
        # Lowercase and clean
        cleaned = text.lower()
        
        try:
            tokens = word_tokenize(cleaned)
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)
            tokens = word_tokenize(cleaned)
            
        processed_tokens = []
        for token in tokens:
            # Filter punctuation and pure digits
            if token not in string.punctuation and token not in self.stop_words:
                try:
                    lemma = self.lemmatizer.lemmatize(token)
                except LookupError:
                    nltk.download('wordnet', quiet=True)
                    lemma = self.lemmatizer.lemmatize(token)
                if len(lemma) > 1:
                    processed_tokens.append(lemma)
                    
        return processed_tokens

    def extract_contact_info(self, text: str) -> Dict[str, Optional[str]]:
        """Extracts candidate Name, Email, Phone, LinkedIn, and GitHub profile."""
        emails = self.EMAIL_REGEX.findall(text)
        phones = self.PHONE_REGEX.findall(text)
        linkedin = self.LINKEDIN_REGEX.findall(text)
        github = self.GITHUB_REGEX.findall(text)
        
        # Candidate name heuristic: First non-empty line of text
        name = "Not Detected"
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if lines:
            first_line = lines[0]
            # Ignore if the first line is an email or section header
            if not self.EMAIL_REGEX.search(first_line) and len(first_line.split()) <= 4:
                # Clean any non-alpha prefix/suffix
                name = re.sub(r'[^A-Za-z\s]', '', first_line).strip().title()
                
        # Clean phone numbers
        cleaned_phone = None
        for raw_p in phones:
            digits = re.sub(r'\D', '', raw_p)
            if 10 <= len(digits) <= 13:
                cleaned_phone = raw_p.strip()
                break
                
        return {
            "name": name if name else "Candidate",
            "email": emails[0] if emails else None,
            "phone": cleaned_phone,
            "linkedin": linkedin[0] if linkedin else None,
            "github": github[0] if github else None
        }

    def extract_education(self, text: str) -> List[str]:
        """Detects mentioned educational qualifications."""
        lower_text = f" {text.lower()} "
        found_education = []
        
        for degree in self.EDUCATION_DEGREES:
            # Use word boundary matching
            pattern = r'\b' + re.escape(degree) + r'\b'
            if re.search(pattern, lower_text):
                found_education.append(degree.upper() if len(degree) <= 4 else degree.title())
                
        return list(dict.fromkeys(found_education))

    def extract_experience_years(self, text: str) -> float:
        """
        Estimates total work experience in years using regex heuristics
        (e.g., '2.5 years of experience', '3+ yrs exp', 'Intern (6 months)').
        """
        lower_text = text.lower()
        
        # Pattern 1: Explicit years (e.g., "2.5 years", "3 yrs", "1+ year")
        years_pattern = re.compile(
            r'(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)?',
            re.IGNORECASE
        )
        matches = years_pattern.findall(lower_text)
        if matches:
            try:
                # Return maximum stated experience
                vals = [float(m) for m in matches if float(m) <= 40]
                if vals:
                    return max(vals)
            except ValueError:
                pass
                
        # Pattern 2: Months (e.g., "6 months intern")
        months_pattern = re.compile(r'(\d+)\s*months?', re.IGNORECASE)
        m_matches = months_pattern.findall(lower_text)
        if m_matches:
            try:
                m_vals = [float(m) / 12.0 for m in m_matches if float(m) <= 60]
                if m_vals:
                    return round(max(m_vals), 1)
            except ValueError:
                pass
                
        return 0.0

    def extract_sections(self, text: str) -> List[str]:
        """Identifies standard resume sections present in the document."""
        lower_text = text.lower()
        detected_sections = []
        
        for header in self.SECTION_HEADERS:
            pattern = r'(?:^|\n)\s*' + re.escape(header) + r'\s*(?::|\n)'
            if re.search(pattern, lower_text, re.MULTILINE):
                detected_sections.append(header.title())
                
        return detected_sections

    def extract_skills(self, text: str) -> Tuple[List[str], Dict[str, List[str]]]:
        """
        Extracts single-word and multi-word technical skills using
        n-gram and boundary-checked taxonomy matching.
        """
        lower_text = text.lower()
        extracted_skills_set = set()
        
        # 1. Direct Regex Phrase Matching for All Known Skills
        for skill in self.known_skills:
            # Word boundary matching (handles symbols like c++, c#, .net, node.js)
            if '+' in skill or '#' in skill or '.' in skill:
                # Literal matching for special tech names
                pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill) + r'(?![a-zA-Z0-9])'
            else:
                pattern = r'\b' + re.escape(skill) + r'\b'
                
            if re.search(pattern, lower_text):
                canonical_skill = dataset_loader.normalize_skill(skill)
                extracted_skills_set.add(canonical_skill)

        # 2. Categorize Extracted Skills
        skills_by_category: Dict[str, List[str]] = {}
        for category, cat_skills in self.skill_categories.items():
            matched_in_cat = []
            for s in cat_skills:
                norm_s = dataset_loader.normalize_skill(s)
                if norm_s in extracted_skills_set:
                    matched_in_cat.append(norm_s)
            if matched_in_cat:
                skills_by_category[category] = sorted(list(set(matched_in_cat)))
                
        sorted_all_skills = sorted(list(extracted_skills_set))
        return sorted_all_skills, skills_by_category

    def parse_resume(self, raw_text: str) -> Dict[str, Any]:
        """
        Master NLP Pipeline execution.
        Transforms raw extracted text into structured resume intelligence.
        """
        cleaned = self.clean_text(raw_text)
        tokens = self.tokenize_and_lemmatize(cleaned)
        contact = self.extract_contact_info(cleaned)
        education = self.extract_education(cleaned)
        experience_years = self.extract_experience_years(cleaned)
        sections = self.extract_sections(cleaned)
        skills, skills_by_category = self.extract_skills(cleaned)
        
        return {
            "contact_info": contact,
            "education": education,
            "experience_years": experience_years,
            "sections_detected": sections,
            "skills": skills,
            "skills_count": len(skills),
            "skills_by_category": skills_by_category,
            "token_count": len(tokens),
            "tokens_sample": tokens[:25],
            "raw_text_length": len(raw_text)
        }


# Singleton preprocessor instance for fast reuse
nlp_preprocessor = NLPPreprocessor()


def parse_resume_nlp(raw_text: str) -> Dict[str, Any]:
    return nlp_preprocessor.parse_resume(raw_text)
