"""
Retrieval Service

Responsible for retrieving relevant enterprise documents from ChromaDB.

Workflow

Query
    │
    ▼
Similarity Search
    │
    ▼
Group by Document
    │
    ▼
Rank Documents
    │
    ▼
Return Complete Documents
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional, Tuple

import torch
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger

from app.config.settings import (
    EMBEDDING_DEVICE,
    EMBEDDING_MODEL,
    CHROMA_PERSIST_DIR,
    COLLECTION_NAME,
)


class RetrievalService:

    def __init__(self):

        device = (
            "cuda"
            if torch.cuda.is_available()
            and EMBEDDING_DEVICE == "cuda"
            else "cpu"
        )

        logger.info(f"Embedding Device : {device}")

        self.embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={
                "device": device
            },
            encode_kwargs={
                "normalize_embeddings": True
            },
        )

        self.vector_store = Chroma(
            persist_directory=CHROMA_PERSIST_DIR,
            collection_name=COLLECTION_NAME,
            embedding_function=self.embedding_model,
        )

    def retrieve(
        self,
        query: str,
        intent: Optional[str] = None,
        top_k_chunks: int = 15,
        top_documents: int = 2,
    ) -> List[Document]:
        """
        Retrieve complete documents rather than isolated chunks.
        """

        logger.info(f"Searching for : {query}")

        filter_dict = (
            {"document_type": intent}
            if intent
            else None
        )

        results = self.vector_store.similarity_search_with_score(
            query=query,
            k=top_k_chunks,
            filter=filter_dict,
        )

        logger.info(f"Retrieved {len(results)} candidate chunks")

        grouped_docs = self._group_documents(results)

        ranked_docs = self._rank_documents(grouped_docs)

        selected_docs = ranked_docs[:top_documents]

        final_chunks: List[Document] = []

        for source, score, chunks in selected_docs:

            logger.info(
                f"Selected Document : {source} | Score : {score:.4f}"
            )

            chunks = sorted(
                chunks,
                key=lambda x: x.metadata.get(
                    "chunk_number",
                    0,
                ),
            )

            final_chunks.extend(chunks)

        logger.success(
            f"Returning {len(final_chunks)} chunks from "
            f"{len(selected_docs)} documents."
        )

        return final_chunks

    def _group_documents(
        self,
        results: List[Tuple[Document, float]],
    ) -> Dict[str, List[Tuple[Document, float]]]:

        grouped = defaultdict(list)

        for doc, score in results:

            source = doc.metadata.get("source")

            grouped[source].append((doc, score))

        return grouped

    def _rank_documents(
        self,
        grouped_docs: Dict[str, List[Tuple[Document, float]]],
    ):

        ranked = []

        for source, items in grouped_docs.items():

            chunks = [doc for doc, _ in items]

            scores = [score for _, score in items]

            # Lower distance is better
            document_score = min(scores)

            ranked.append(
                (
                    source,
                    document_score,
                    chunks,
                )
            )

        ranked.sort(key=lambda x: x[1])

        return ranked