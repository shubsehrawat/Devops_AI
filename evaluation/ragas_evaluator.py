"""
RAGAS Evaluator

Evaluates the generation quality of the Hybrid RAG system using
RAGAS metrics.

Metrics:
---------
- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall
"""

from __future__ import annotations

import os
from typing import List

import pandas as pd
from datasets import Dataset

from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.settings import GOOGLE_API_KEY


class RagasEvaluator:
    """
    Runs RAGAS evaluation on generated answers.
    """

    def __init__(self):

        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

        self.evaluator_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0,
        )

    def evaluate(
        self,
        evaluation_rows: List[dict],
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        evaluation_rows

        Example

        [
            {
                "question": "...",
                "answer": "...",
                "contexts": ["..."],
                "ground_truth": "..."
            }
        ]
        """

        dataset = Dataset.from_list(evaluation_rows)

        result = evaluate(
            dataset=dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
            ],
            llm=self.evaluator_llm,
        )

        df = result.to_pandas()

        return df