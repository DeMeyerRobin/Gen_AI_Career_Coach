"""
Configuration file for AI Career Coach
Centralized configuration for models, paths, and settings
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "Backend"
FRONTEND_DIR = PROJECT_ROOT / "Frontend"
RAG_DIR = PROJECT_ROOT / "Rag"
DATA_DIR = PROJECT_ROOT / "Data"
TEMP_DIR = PROJECT_ROOT / "temp"

# Ensure temp directory exists
TEMP_DIR.mkdir(exist_ok=True)

# Model configurations
OLLAMA_MODEL = "mistral"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# ChromaDB configurations
CHROMADB_PATH = DATA_DIR / "chromadb"
COLLECTION_RESUMES = "resumes"
COLLECTION_JOBS = "jobs"

# Processing configurations
BATCH_SIZE = 32
RAG_DEFAULT_RESULTS = 10
RAG_MIN_SIMILARITY = 0.5

# File configurations
ALLOWED_PDF_EXTENSIONS = [".pdf"]
MAX_FILE_SIZE_MB = 10
