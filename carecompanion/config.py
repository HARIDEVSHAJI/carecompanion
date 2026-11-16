"""Settings. Reads the .env file (if present) and environment variables."""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
DATA_DIR = ROOT / "data"
DB_PATH = Path(os.getenv("DB_PATH", str(DATA_DIR / "carecompanion.db")))


def provider() -> str:
    p = os.getenv("LLM_PROVIDER", "").strip().lower()
    if p:
        return p
    if os.getenv("GROQ_API_KEY"):
        return "groq"
    if os.getenv("AZURE_OPENAI_API_KEY"):
        return "azure"
    return "mock"
