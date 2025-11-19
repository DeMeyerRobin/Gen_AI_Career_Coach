"""
AI Career Coach - Gradio Frontend
Clean UI for CV analysis and interview preparation
"""

import gradio as gr
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import service functions
from services.cv_processor import process_cv


# Gradio UI with custom CSS
custom_css = """
.gradio-container {
    max-width: 1200px !important;
}
.output-markdown {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
}
"""

with gr.Blocks(title="AI Career Coach", css=custom_css, theme=gr.themes.Soft()) as app:
    # Header
    gr.Markdown("""
    # 🧠 AI Career Coach
    ### Transform your CV and ace your interview with AI-powered insights
    Upload your CV, specify your target job, and get personalized feedback powered by RAG (Retrieval-Augmented Generation)
    """)
    
    gr.Markdown("---")
    
    # Input Section
    with gr.Row():
        with gr.Column(scale=1):
            pdf_input = gr.File(
                label="📄 Upload Your CV", 
                file_types=[".pdf"],
                file_count="single"
            )
            job_input = gr.Textbox(
                label="🎯 Target Job Title",
                placeholder="e.g., Software Engineer, Data Scientist, Product Manager...",
                lines=1
            )
            submit_btn = gr.Button("🚀 Analyze My CV", variant="primary", size="lg")
        
        with gr.Column(scale=1):
            gr.Markdown("""
            ### 📝 What You'll Get:
            - ✨ **Cleaned CV bullets** - Professional, concise format
            - 💡 **Improvement tips** - Based on 1000+ successful CVs
            - 🎤 **Interview questions** - Tailored to your target role
            - 📊 **Skills analysis** - What you're missing vs. top candidates
            """)
    
    gr.Markdown("---")
    
    # Output Section - Cleaned CV
    with gr.Column():
        gr.Markdown("## ✨ Your Cleaned CV")
        output_text = gr.Textbox(
            label="Cleaned Bullet Points",
            lines=15,
            interactive=False,
            show_label=False
        )
        download_btn = gr.File(
            label="⬇️ Download",
            interactive=False
        )
    
    gr.Markdown("---")
    
    # Output Section - Improvements and Questions in Tabs
    with gr.Tabs():
        with gr.Tab("💡 CV Improvements"):
            improvement_output = gr.Markdown(
                value="*Upload your CV and click 'Analyze My CV' to see personalized improvement suggestions...*",
                elem_classes="output-markdown"
            )
        
        with gr.Tab("🎤 Interview Prep"):
            interview_output = gr.Markdown(
                value="*Upload your CV and click 'Analyze My CV' to get interview questions and preparation tips...*",
                elem_classes="output-markdown"
            )
    
    # Footer
    gr.Markdown("""
    ---
    <center>
    <small>Powered by RAG, Ollama, and ChromaDB | Analyzing 1000+ CVs and 2000+ job descriptions</small>
    </center>
    """)

    # Button logic
    submit_btn.click(
        process_cv,
        inputs=[pdf_input, job_input],
        outputs=[output_text, download_btn, improvement_output, interview_output]
    )


# Launch Gradio (disable API docs to avoid Gradio bug)
app.launch(show_api=False)
