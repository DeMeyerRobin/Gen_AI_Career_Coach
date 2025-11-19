import gradio as gr
import os
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Import your pipeline functions
from Backend.utils.pdf_reader import pdf_to_text
from Backend.utils.bullet_extractor import extract_bullets_with_ollama

# Setup path for RAG but don't import yet (lazy loading)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Rag")))

# Initialize RAG matcher (lazy loading)
_matcher = None

def get_matcher():
    """Lazy load the matcher to avoid startup delays."""
    global _matcher
    if _matcher is None:
        from career_coach_matcher import CareerCoachMatcher
        _matcher = CareerCoachMatcher()
    return _matcher


def process_cv(pdf_file, job_title):
    """
    This function is triggered when the user uploads a PDF in Gradio.
    """
    if pdf_file is None:
        return "❌ Please upload a PDF file first.", None, ""
    
    if not job_title or job_title.strip() == "":
        return "❌ Please enter a job title.", None, ""

    try:
        # Temporary txt path
        txt_path = "cv_output.txt"

        # Step 1 — Read PDF → raw text
        # Gradio returns the file path directly as a string
        pdf_path = pdf_file if isinstance(pdf_file, str) else pdf_file.name
        
        print(f"DEBUG: PDF path = {pdf_path}")
        print(f"DEBUG: Job title = {job_title}")
        
        pdf_to_text(pdf_path, txt_path)

        # Load raw text
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        # Step 2 — Ollama cleanup → bullet points (with job context)
        cleaned_bullets = extract_bullets_with_ollama(raw_text)
        
        # Add job title context to output
        result = f"🎯 Target Job: {job_title}\n\n{'='*60}\n\n{cleaned_bullets}"

        # Save for download
        output_path = "clean_bullets.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Target Job: {job_title}\n\n{cleaned_bullets}")

        # Step 3 — RAG Analysis for improvements
        improvement_analysis = analyze_cv_improvements(cleaned_bullets, job_title)

        return result, output_path, improvement_analysis
        
    except Exception as e:
        error_msg = f"❌ Error processing CV: {str(e)}"
        print(f"ERROR: {error_msg}")
        import traceback
        traceback.print_exc()
        return error_msg, None, ""


def analyze_cv_improvements(cv_text, job_title):
    """
    Analyze CV and provide improvement suggestions using RAG.
    """
    if not cv_text or cv_text.strip() == "":
        return "❌ Please provide CV text to analyze."
    
    if not job_title or job_title.strip() == "":
        job_title = "Software Engineer"  # Default
    
    try:
        from collections import Counter
        
        # Get matcher (this loads RAG on first use)
        matcher = get_matcher()
        
        # Find similar CVs
        similar_cvs = matcher.find_resumes_for_job(
            job_title=job_title,
            job_description=cv_text,
            n_results=5,
            min_score=0.5
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
        
        # Find missing keywords
        common_keywords = [word for word, count in keyword_freq.most_common(30) 
                          if count >= 3 and len(word) > 4 and word not in user_words]
        
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


# Gradio UI
with gr.Blocks(title="AI Career Coach — CV Bullet Cleaner") as app:
    gr.Markdown("## 🧠 AI Career Coach — CV Processor & Improvement Analyzer\nUpload your CV as PDF, specify your target job, and get clean bullet points + improvement suggestions using RAG.")

    with gr.Row():
        with gr.Column():
            pdf_input = gr.File(label="📄 Upload your CV (PDF)", file_types=[".pdf"])
        with gr.Column():
            job_input = gr.Textbox(
                label="🎯 Target Job Title",
                placeholder="e.g., Software Engineer, Marketing Manager, Data Analyst...",
                lines=1
            )

    with gr.Row():
        submit_btn = gr.Button("🚀 Process CV", variant="primary")

    with gr.Row():
        output_text = gr.Textbox(
            label="✨ Cleaned Bullet Points",
            lines=20,
            interactive=False
        )

    with gr.Row():
        download_btn = gr.File(
            label="⬇️ Download Clean Bullet Points",
            interactive=False
        )
    
    with gr.Row():
        improvement_output = gr.Markdown(
            label="💡 CV Improvement Suggestions (RAG)",
            value="*Improvement suggestions will appear here after processing...*"
        )

    # Button logic
    submit_btn.click(
        process_cv,
        inputs=[pdf_input, job_input],
        outputs=[output_text, download_btn, improvement_output]
    )


# Launch Gradio (disable API docs to avoid Gradio bug)
app.launch(show_api=False)
