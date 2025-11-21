# 🧠 AI Career Coach

An intelligent CV analysis and interview preparation tool powered by RAG (Retrieval-Augmented Generation), Ollama, and ChromaDB.

## ✨ Features

- **📄 CV Cleaning** - Transform messy CVs into professional bullet points using Ollama
- **💡 Smart Improvements** - Get personalized suggestions based on 1000+ successful CVs
- **🎤 Interview Prep** - Generate tailored interview questions for your target role
- **📊 Skills Analysis** - Identify missing keywords and skills gaps
- **🔍 RAG-Powered** - Semantic search through 2000+ job descriptions

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install tf-keras  # For TensorFlow/Keras compatibility
   ```

2. **Run the app:**
   ```bash
   python Frontend/app.py
   ```

3. **Open your browser:** `http://localhost:7860`

## 📁 Project Structure

```
Gen_AI_Career_Coach/
├── config.py          # Centralized configuration
├── services/          # Business logic services
│   ├── cv_analyzer.py       # CV improvement analysis
│   ├── cv_processor.py      # Main CV processing pipeline
│   └── interview_generator.py # Interview question generation
├── Backend/           # Core utilities
│   └── utils/
│       ├── pdf_reader.py    # PDF text extraction
│       └── bullet_extractor.py # Ollama CV cleaning
├── Frontend/          # Gradio web interface
│   └── app.py         # Clean UI (now 100 lines!)
├── Rag/              # RAG system (ChromaDB + embeddings)
│   ├── career_coach_matcher.py # High-level RAG API
│   ├── chroma_ingestion.py    # Embedding generation
│   └── chroma_setup.py        # Database initialization
├── models/           # AI models
├── Data/             # ChromaDB database (resumes & jobs)
├── docs/             # Documentation
├── demos/            # Demo scripts
└── temp/             # Temporary output files
```

## 🏗️ Architecture

**Clean separation of concerns:**
- `config.py` - All configuration in one place
- `services/` - Business logic isolated from UI
- `Backend/utils/` - Reusable utility functions
- `Frontend/app.py` - Pure UI code, no business logic
- `Rag/` - RAG system with lazy loading

## 🛠️ Tech Stack

- **Ollama (Mistral)** - CV cleaning and text generation
- **ChromaDB** - Vector database (1000+ resumes, 2000+ jobs)
- **sentence-transformers** - Text embeddings (all-MiniLM-L6-v2)
- **Gradio 5** - Modern web UI
- **PyPDF2** - PDF text extraction

## 📚 Documentation

See the `docs/` folder for detailed documentation:
- Project overview
- Getting started guide
- File structure

## 🎯 How It Works

1. **Upload CV** → Extract text from PDF
2. **Clean with Ollama** → Generate professional bullet points
3. **RAG Analysis** → Compare with 1000+ CVs in ChromaDB
4. **Generate Insights** → Improvement tips + interview questions

## 🤝 Contributing

This is a school project for Howest 2025-2026 Gen AI course.

## 📝 License

Educational project - Howest University
