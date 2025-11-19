import gradio as gr
import os
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Import your pipeline functions
from Backend.utils.pdf_reader import pdf_to_text
from Backend.utils.bullet_extractor import extract_bullets_with_ollama


def process_cv(pdf_file):
    """
    This function is triggered when the user uploads a PDF in Gradio.
    """
    if pdf_file is None:
        return "❌ Please upload a PDF file first.", None

    # Temporary txt path
    txt_path = "cv_output.txt"

    # Step 1 — Read PDF → raw text
    # Gradio returns the file path directly as a string
    pdf_path = pdf_file if isinstance(pdf_file, str) else pdf_file.name
    pdf_to_text(pdf_path, txt_path)

    # Load raw text
    with open(txt_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Step 2 — Ollama cleanup → bullet points
    cleaned_bullets = extract_bullets_with_ollama(raw_text)

    # Save for download
    output_path = "clean_bullets.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_bullets)

    return cleaned_bullets, output_path


# Gradio UI
with gr.Blocks(title="AI CV Cleaner (Powered by Ollama)") as app:
    gr.Markdown("## 🧠 AI Career Coach — CV Bullet Cleaner\nUpload your CV as PDF and get clean, professional bullet points.")

    with gr.Row():
        pdf_input = gr.File(label="📄 Upload your CV (PDF)", file_types=[".pdf"])

    with gr.Row():
        submit_btn = gr.Button("🚀 Process CV")

    with gr.Row():
        output_text = gr.Textbox(
            label="✨ Cleaned Bullet Points",
            lines=25,
            interactive=False
        )

    with gr.Row():
        download_btn = gr.File(
            label="⬇️ Download Clean Bullet Points",
            interactive=False
        )

    # Button logic
    submit_btn.click(
        process_cv,
        inputs=pdf_input,
        outputs=[output_text, download_btn]
    )


# Launch Gradio
app.launch()
