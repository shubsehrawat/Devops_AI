import torch

from langchain_huggingface import HuggingFaceEmbeddings

from app.config.settings import (
    EMBEDDING_MODEL,
    EMBEDDING_DEVICE
)


class EmbeddingModel:

    def __init__(self):

        # Fall back to CPU if CUDA isn't available
        device = (
            EMBEDDING_DEVICE
            if EMBEDDING_DEVICE == "cpu"
            else "cuda" if torch.cuda.is_available() else "cpu"
        )

        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        print(f"Using device: {device}")

        if device == "cuda":
            print(f"GPU: {torch.cuda.get_device_name(0)}")

        self.embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={
                "device": device
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

    def get_embeddings(self):
        return self.embedding_model