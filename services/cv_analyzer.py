"""
CV Analysis Service
Analyzes CVs and provides improvement suggestions using RAG
"""

import sys
import os
from collections import Counter
from typing import Optional
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(parent_dir / "Rag"))

from config import RAG_DEFAULT_RESULTS, RAG_MIN_SIMILARITY


def get_matcher():
    """Lazy load the matcher to avoid startup delays."""
    from career_coach_matcher import CareerCoachMatcher
    return CareerCoachMatcher()


def analyze_cv_improvements(cv_text: str, job_title: str, n_results: int = 5) -> str:
    """
    Analyze CV and provide improvement suggestions using RAG.
    
    Args:
        cv_text: Cleaned CV text content
        job_title: Target job title
        n_results: Number of similar CVs to analyze
    
    Returns:
        Formatted markdown report with improvement suggestions
    """
    if not cv_text or cv_text.strip() == "":
        return "❌ Please provide CV text to analyze."
    
    if not job_title or job_title.strip() == "":
        job_title = "Software Engineer"  # Default
    
    try:
        # Get matcher (lazy loading)
        matcher = get_matcher()
        
        # Find similar CVs
        similar_cvs = matcher.find_resumes_for_job(
            job_title=job_title,
            job_description=cv_text,
            n_results=n_results,
            min_score=RAG_MIN_SIMILARITY
        )
        
        if not similar_cvs:
            return "⚠️ No similar CVs found in database. Try a different job title."
        
        # Build analysis report
        report = f"# 📊 CV IMPROVEMENT ANALYSIS\n\n"
        report += f"**Target Job:** {job_title}\n\n"
        report += f"**Similar CVs Found:** {len(similar_cvs)}\n\n"
        report += "---\n\n"
        
        # Show top similar CVs
        report += "## 🎯 Top Matching CVs\n\n"
        for i, cv in enumerate(similar_cvs[:3], 1):
            category = cv.metadata.get('category', 'Unknown')
            similarity = cv.similarity_score * 100
            report += f"**{i}. {category}** - Match: {similarity:.1f}%\n"
            report += f"   *Preview:* {cv.text[:150]}...\n\n"
        
        # Extract keywords
        all_keywords = []
        for cv in similar_cvs:
            words = cv.text.lower().split()
            all_keywords.extend(words)
        
        keyword_freq = Counter(all_keywords)
        user_words = set(cv_text.lower().split())
        
        # Find missing keywords (filter for meaningful words)
        common_keywords = [
            word for word, count in keyword_freq.most_common(30) 
            if count >= 3 and len(word) > 4 and word not in user_words
        ]
        
        report += "---\n\n"
        report += "## 💡 IMPROVEMENT SUGGESTIONS\n\n"
        
        report += "### 1️⃣ Keywords You Might Be Missing\n"
        report += "*(These appear frequently in similar successful CVs)*\n\n"
        for keyword in common_keywords[:10]:
            report += f"- {keyword}\n"
        
        report += f"\n### 2️⃣ Best Matching Category\n"
        if similar_cvs:
            best_category = similar_cvs[0].metadata.get('category', 'Unknown')
            report += f"Your CV is most similar to: **{best_category}**\n\n"
        
        report += "### 3️⃣ Quick Tips\n"
        report += "- ✅ Add specific project examples with measurable results\n"
        report += "- ✅ Use action verbs (developed, implemented, managed)\n"
        report += "- ✅ Quantify achievements (increased by X%, reduced by Y%)\n"
        report += "- ✅ Include relevant certifications and technical skills\n"
        
        return report
        
    except Exception as e:
        return f"❌ Error analyzing CV: {str(e)}"
