"""
Chat Service

Orchestrates the complete Hybrid RAG workflow.

Flow:

User Query
    │
    ▼
Intent Classification Agent
    │
    ▼
Metadata-based Retrieval
    │
    ▼
Context Builder
    │
    ▼
Response Formatter
    │
    ▼
LLM Service
    │
    ▼
Final Response
"""

from typing import Any, Dict

from loguru import logger

from app.agents.intent_classifier import IntentClassifier
from app.agents.response_formatter import ResponseFormatter
from app.config.settings import (
    TOP_DOCUMENTS,
    TOP_K_CHUNKS,
)
from app.services.context_builder import ContextBuilder
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService


class ChatService:
    """
    Orchestrates the complete Hybrid RAG workflow.
    """

    def __init__(self) -> None:
        """
        Initialize all services once when the application starts.
        """

        logger.info("Initializing Chat Service...")

        self.intent_classifier = IntentClassifier()
        self.retriever = RetrievalService()
        self.context_builder = ContextBuilder()
        self.response_formatter = ResponseFormatter()
        self.llm_service = LLMService()

        logger.success("Chat Service initialized successfully.")

    def chat(self, query: str) -> Dict[str, Any]:
        """
        Execute the complete RAG workflow.

        Args:
            query: User question.

        Returns:
            Response dictionary.
        """

        logger.info("=" * 100)
        logger.info(f"Processing Query : {query}")

        # -------------------------------------------------------
        # Step 1 : Intent Classification
        # -------------------------------------------------------

        intent_result = self.intent_classifier.classify(query)

        intent = intent_result["intent"]

        logger.info(f"Detected Intent : {intent}")

        # -------------------------------------------------------
        # Step 2 : Retrieve Documents
        # -------------------------------------------------------

        documents = self.retriever.retrieve(
            query=query,
            intent=intent,
            top_k_chunks=TOP_K_CHUNKS,
            top_documents=TOP_DOCUMENTS,
        )

        logger.info(f"Retrieved {len(documents)} chunks")

        # -------------------------------------------------------
        # Step 3 : Build Context
        # -------------------------------------------------------

        context, sources = self.context_builder.build(documents)

        logger.info("Context successfully built.")

        # -------------------------------------------------------
        # Step 4 : Build Prompt
        # -------------------------------------------------------

        prompt = self.response_formatter.get_prompt(
            intent=intent,
            query=query,
            context=context,
        )

        logger.info(f"Prompt Length : {len(prompt)} characters")

        # -------------------------------------------------------
        # Step 5 : Generate Answer
        # -------------------------------------------------------

        answer = self.llm_service.generate_response(prompt)

        logger.success("LLM response generated.")

        # -------------------------------------------------------
        # Final Response
        # -------------------------------------------------------

        return {
            "query": query,
            "intent": intent,
            "confidence": intent_result.get("confidence"),
            "retrieved_documents": len(documents),
            "answer": answer,
            "sources": sources,
        }