"""
Context Builder Service

Builds a structured LLM context from retrieved documents.
"""

from __future__ import annotations

from typing import List, Tuple

from langchain_core.documents import Document
from loguru import logger


class ContextBuilder:
    """
    Builds structured context from retrieved documents.
    """

    def build(
        self,
        documents: List[Document],
    ) -> Tuple[str, List[str]]:

        logger.info("Building LLM context...")

        context_blocks = []

        unique_sources = set()

        seen_chunks = set()

        for index, doc in enumerate(documents, start=1):

            metadata = doc.metadata

            chunk_id = metadata.get("chunk_id")

            if chunk_id in seen_chunks:
                continue

            seen_chunks.add(chunk_id)

            source = metadata.get("source", "Unknown")
            document_type = metadata.get("document_type", "Unknown")

            unique_sources.add(source)

            block = f"""
                    ====================================================
                    Document {index}

                    Source          : {source}
                    Document Type   : {document_type}

                    Content:
                    {doc.page_content.strip()}
                    ====================================================
                    """

            context_blocks.append(block)

        context = "\n\n".join(context_blocks)

        logger.success(
            f"Context built with {len(context_blocks)} unique chunks."
        )

        return context, sorted(unique_sources)