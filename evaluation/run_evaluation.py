"""
Run Evaluation

Entry point for evaluating the Enterprise DevOps AI Copilot.

Evaluates:

1. Retrieval Quality
    - Precision@K
    - Recall@K

2. Generation Quality
    - Faithfulness
    - Answer Relevancy
    - Context Precision
    - Context Recall

Usage
-----

python evaluation/run_evaluation.py
"""

from __future__ import annotations

from pathlib import Path

from loguru import logger

from evaluation.evaluator import Evaluator


def print_summary(results: dict) -> None:
    """
    Print evaluation summary.
    """

    retrieval = results["retrieval"]
    generation = results["generation"]

    print("\n")
    print("=" * 70)
    print("Retrieval Evaluation")
    print("=" * 70)

    print(f"Queries Evaluated : {retrieval['queries_evaluated']}")
    print(f"Precision@K       : {retrieval['precision_at_k']:.3f}")
    print(f"Recall@K          : {retrieval['recall_at_k']:.3f}")

    print("\n")
    print("=" * 70)
    print("Generation Evaluation (RAGAS)")
    print("=" * 70)

    print(generation)

    print("\n")


def save_results(results: dict) -> None:
    """
    Save RAGAS evaluation results.
    """

    output_dir = Path("evaluation/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "ragas_results.csv"

    results["generation"].to_csv(
        output_file,
        index=False,
    )

    logger.success(f"Results saved to {output_file}")


def main() -> None:
    """
    Execute evaluation.
    """

    logger.info("=" * 80)
    logger.info("Enterprise DevOps AI Copilot Evaluation")
    logger.info("=" * 80)

    evaluator = Evaluator()

    results = evaluator.run()

    print_summary(results)

    save_results(results)

    logger.success("Evaluation completed successfully.")


if __name__ == "__main__":
    main()