"""
Interview Question Generator Service
Generates role-specific interview questions using RAG
"""

import sys
import os
from typing import Optional
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(parent_dir / "Rag"))

from config import RAG_MIN_SIMILARITY


def get_matcher():
    """Lazy load the matcher to avoid startup delays."""
    from career_coach_matcher import CareerCoachMatcher
    return CareerCoachMatcher()


def generate_interview_questions(cv_text: str, job_title: str, n_jobs: int = 3) -> str:
    """
    Generate interview questions based on job title using RAG.
    
    Args:
        cv_text: CV text content
        job_title: Target job title
        n_jobs: Number of job descriptions to analyze
    
    Returns:
        Formatted markdown report with interview questions and tips
    """
    if not job_title or job_title.strip() == "":
        job_title = "Software Engineer"
    
    try:
        # Get matcher
        matcher = get_matcher()
        
        # Find relevant job descriptions
        relevant_jobs = matcher.find_jobs_for_resume(
            cv_text, 
            n_results=n_jobs, 
            min_score=RAG_MIN_SIMILARITY
        )
        
        if not relevant_jobs:
            return "⚠️ No relevant jobs found to generate questions."
        
        # Build interview questions report
        report = f"# 🎤 INTERVIEW PREPARATION QUESTIONS\n\n"
        report += f"**Target Job:** {job_title}\n\n"
        report += "---\n\n"
        
        # General questions based on job
        report += "## 📋 Common Interview Questions\n\n"
        report += f"### For {job_title} Position:\n\n"
        report += "1. **Tell me about yourself and your background**\n"
        report += f"   - *Focus on: Your experience relevant to {job_title} role*\n\n"
        
        report += "2. **Why are you interested in this position?**\n"
        report += f"   - *Highlight: Your passion for {job_title} work and company alignment*\n\n"
        
        report += "3. **What are your greatest strengths?**\n"
        report += "   - *Use STAR method: Situation, Task, Action, Result*\n\n"
        
        report += "4. **Describe a challenging project you worked on**\n"
        report += "   - *Emphasize: Problem-solving skills and technical expertise*\n\n"
        
        report += "5. **Where do you see yourself in 5 years?**\n"
        report += f"   - *Connect: Your growth with {job_title} career path*\n\n"
        
        # Technical/role-specific questions based on job description
        report += "---\n\n"
        report += "## 🔧 Role-Specific Questions\n\n"
        report += "*Based on similar job descriptions in our database:*\n\n"
        
        for i, job in enumerate(relevant_jobs[:2], 1):
            job_desc = job.text[:300]
            report += f"### Scenario {i}:\n"
            report += f"*Related to: {job.metadata.get('job_title', 'Unknown')}*\n\n"
            
            # Extract key skills/topics from job description
            keywords = ['experience', 'skills', 'requirements', 'responsibilities']
            for keyword in keywords:
                if keyword.lower() in job_desc.lower():
                    report += f"- **Question:** Describe your {keyword} related to this role\n"
                    break
            report += "\n"
        
        report += "---\n\n"
        report += "## 💡 PREPARATION TIPS\n\n"
        report += "### Before the Interview:\n"
        report += "- ✅ Research the company thoroughly\n"
        report += "- ✅ Prepare 3-4 STAR method examples\n"
        report += "- ✅ Review your CV and be ready to explain gaps\n"
        report += "- ✅ Prepare questions to ask the interviewer\n\n"
        
        report += "### During the Interview:\n"
        report += "- ✅ Listen carefully to questions before answering\n"
        report += "- ✅ Use specific examples from your experience\n"
        report += "- ✅ Be honest about what you don't know\n"
        report += "- ✅ Show enthusiasm for the role and company\n\n"
        
        report += "### Questions to Ask Them:\n"
        report += "- What does success look like in this role?\n"
        report += "- What are the team dynamics like?\n"
        report += "- What are the biggest challenges facing the team?\n"
        report += "- What opportunities for growth are available?\n"
        
        return report
        
    except Exception as e:
        return f"❌ Error generating questions: {str(e)}"
