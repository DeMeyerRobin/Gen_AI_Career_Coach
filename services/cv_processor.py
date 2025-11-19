"""
CV Processing Service
Handles CV upload, extraction, cleaning, and analysis orchestration
"""

import os
import sys
from typing import Tuple, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Backend.utils.pdf_reader import pdf_to_text
from Backend.utils.bullet_extractor import extract_bullets_with_ollama
from services.cv_analyzer import analyze_cv_improvements
from services.interview_generator import generate_interview_questions
from config import TEMP_DIR


def process_cv(pdf_file, job_title: str) -> Tuple[str, Optional[str], str, str]:
    """
    Main CV processing pipeline.
    
    Args:
        pdf_file: Uploaded PDF file (Gradio file object or path string)
        job_title: Target job title
    
    Returns:
        Tuple of (cleaned_text, download_path, improvements, interview_questions)
    """
    if pdf_file is None:
        return "❌ Please upload a PDF file first.", None, "", ""
    
    if not job_title or job_title.strip() == "":
        return "❌ Please enter a job title.", None, "", ""

    try:
        # Ensure temp directory exists
        TEMP_DIR.mkdir(exist_ok=True)
        
        # Temporary txt path
        txt_path = TEMP_DIR / "cv_output.txt"

        # Step 1 — Read PDF → raw text
        pdf_path = pdf_file if isinstance(pdf_file, str) else pdf_file.name
        
        print(f"DEBUG: PDF path = {pdf_path}")
        print(f"DEBUG: Job title = {job_title}")
        
        pdf_to_text(pdf_path, str(txt_path))

        # Load raw text
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        # Step 2 — Ollama cleanup → bullet points
        cleaned_bullets = extract_bullets_with_ollama(raw_text)
        
        # Add job title context to output
        result = f"🎯 Target Job: {job_title}\n\n{'='*60}\n\n{cleaned_bullets}"

        # Save for download
        output_path = TEMP_DIR / "clean_bullets.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Target Job: {job_title}\n\n{cleaned_bullets}")

        # Step 3 — RAG Analysis for improvements
        improvement_analysis = analyze_cv_improvements(cleaned_bullets, job_title)
        
        # Step 4 — Generate interview questions
        interview_questions = generate_interview_questions(cleaned_bullets, job_title)

        return result, str(output_path), improvement_analysis, interview_questions
        
    except Exception as e:
        error_msg = f"❌ Error processing CV: {str(e)}"
        print(f"ERROR: {error_msg}")
        import traceback
        traceback.print_exc()
        return error_msg, None, "", ""
