"""
Retrieval Evaluation Metrics

This module implements standard Information Retrieval metrics
for evaluating the performance of the Hybrid RAG retriever.

Metrics:
---------
1. Precision@K
2. Recall@K

The functions are intentionally framework-agnostic and operate
on plain Python lists.
"""

from __future__ import annotations

from typing import Dict, List


class RetrievalMetrics:
    """
    Computes retrieval evaluation metrics.
    """

    @staticmethod
    def precision_at_k(
        expected_documents: List[str],
        retrieved_documents: List[str],
        k: int,
    ) -> float:
        """
        Compute Precision@K.

        Precision@K =
            Relevant Retrieved Documents
            ----------------------------
            Total Retrieved Documents
        """

        retrieved = retrieved_documents[:k]

        if not retrieved:
            return 0.0

        relevant = sum(
            1
            for doc in retrieved
            if doc in expected_documents
        )

        return relevant / len(retrieved)

    @staticmethod
    def recall_at_k(
        expected_documents: List[str],
        retrieved_documents: List[str],
        k: int,
    ) -> float:
        """
        Compute Recall@K.

        Recall@K =
            Relevant Retrieved Documents
            ----------------------------
            Total Relevant Documents
        """

        if not expected_documents:
            return 0.0

        retrieved = retrieved_documents[:k]

        relevant = sum(
            1
            for doc in retrieved
            if doc in expected_documents
        )

        return relevant / len(expected_documents)

    @staticmethod
    def evaluate(
        expected_documents: List[str],
        retrieved_documents: List[str],
        k: int = 3,
    ) -> Dict:
        """
        Evaluate retrieval for a single query.
        """

        precision = RetrievalMetrics.precision_at_k(
            expected_documents,
            retrieved_documents,
            k,
        )

        recall = RetrievalMetrics.recall_at_k(
            expected_documents,
            retrieved_documents,
            k,
        )

        return {
            "precision_at_k": round(precision, 3),
            "recall_at_k": round(recall, 3),
        }

    @staticmethod
    def evaluate_dataset(
        results: List[Dict],
        k: int = 3,
    ) -> Dict:
        """
        Evaluate an entire dataset.

        Parameters
        ----------
        results

        Example:

        [
            {
                "expected_documents":[...],
                "retrieved_documents":[...]
            }
        ]
        """

        if not results:
            return {
                "precision_at_k": 0.0,
                "recall_at_k": 0.0,
            }

        precision_scores = []
        recall_scores = []

        for item in results:

            metrics = RetrievalMetrics.evaluate(
                expected_documents=item["expected_documents"],
                retrieved_documents=item["retrieved_documents"],
                k=k,
            )

            precision_scores.append(
                metrics["precision_at_k"]
            )

            recall_scores.append(
                metrics["recall_at_k"]
            )

        return {
            "queries_evaluated": len(results),
            "precision_at_k": round(
                sum(precision_scores) / len(precision_scores),
                3,
            ),
            "recall_at_k": round(
                sum(recall_scores) / len(recall_scores),
                3,
            ),
        }