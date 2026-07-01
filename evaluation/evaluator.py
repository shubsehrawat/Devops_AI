"""
Enterprise DevOps AI Copilot

Evaluation Orchestrator

Coordinates the complete evaluation pipeline.

Pipeline
--------

Ground Truth Queries
        │
        ▼
Chat Service
        │
        ▼
Retrieval Evaluation
        │
        ▼
RAGAS Evaluation
        │
        ▼
Final Evaluation Report
"""

from __future__ import annotations

from typing import Dict, List

from loguru import logger

from app.services.chat_service import ChatService

from evaluation.test_queries import TEST_QUERIES
from evaluation.retrieval_metrics import RetrievalMetrics
from evaluation.ragas_evaluator import RagasEvaluator


class Evaluator:
    """
    Complete evaluation pipeline.
    """

    def __init__(self) -> None:

        logger.info("Initializing Evaluation Pipeline...")

        self.chat_service = ChatService()
        self.ragas = RagasEvaluator()

    def run(self) -> Dict:
        """
        Execute retrieval and generation evaluation.

        Returns
        -------
        Dictionary containing evaluation metrics.
        """

        retrieval_results: List[Dict] = []

        ragas_rows: List[Dict] = []

        logger.info("=" * 80)
        logger.info("Starting Evaluation")
        logger.info("=" * 80)

        for sample in TEST_QUERIES:

            logger.info(f"Evaluating Query: {sample['query']}")

            response = self.chat_service.chat(
                sample["query"]
            )

            retrieved_documents = response["sources"]

            retrieval_results.append(
                {
                    "expected_documents": sample["expected_documents"],
                    "retrieved_documents": retrieved_documents,
                }
            )

            ragas_rows.append(
                {
                    "question": sample["query"],
                    "answer": response["answer"],
                    "contexts": [response["context"]],
                    "ground_truth": sample["ground_truth"],
                }
            )

        logger.success("Retrieval completed.")

        retrieval_metrics = RetrievalMetrics.evaluate_dataset(
            retrieval_results,
            k=3,
        )

        logger.success("Retrieval metrics calculated.")

        ragas_df = self.ragas.evaluate(
            ragas_rows
        )

        logger.success("RAGAS evaluation completed.")

        return {
            "retrieval": retrieval_metrics,
            "generation": ragas_df,
        }