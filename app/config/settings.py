from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "devops_ai")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))


TOP_K_CHUNKS = 15
TOP_DOCUMENTS = 2