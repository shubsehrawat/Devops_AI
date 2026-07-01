"""
Intent Classification Agent

Local rule-based intent classifier for the Enterprise DevOps AI Copilot.

Supported Intents
-----------------
- runbook
- rca
- incident_summary
- troubleshooting
- sop
- best_practices
"""

from __future__ import annotations

import re
from typing import Dict

from loguru import logger


class IntentClassifier:
    """
    Local Intent Classification Agent.
    """

    INTENT_KEYWORDS = {
        "rca": [
            "root cause",
            "why",
            "failed",
            "failure",
            "outage",
            "downtime",
            "incident cause",
            "reason",
            "database failure",
            "payment api",
            "timeout",
            "error occurred",
        ],

        "incident_summary": [
            "incident",
            "summary",
            "summarize",
            "overview",
            "timeline",
            "status",
            "inc-",
        ],

        "runbook": [
            "runbook",
            "deploy",
            "deployment",
            "execute",
            "installation",
            "install",
            "restart",
            "upgrade",
            "rollback",
            "steps",
            "procedure",
        ],

        "troubleshooting": [
            "troubleshoot",
            "troubleshooting",
            "fix",
            "resolve",
            "debug",
            "diagnose",
            "crashloopbackoff",
            "pod crash",
            "error",
            "issue",
            "unable",
        ],

        "sop": [
            "sop",
            "standard operating procedure",
            "standard procedure",
            "process",
            "policy",
            "workflow",
        ],

        "best_practices": [
            "best practice",
            "best practices",
            "recommendation",
            "recommend",
            "guidelines",
            "security",
            "optimization",
            "optimize",
        ],
    }

    def classify(self, query: str) -> Dict:
        """
        Classify user query.

        Returns
        -------
        {
            "intent": "...",
            "confidence": 0.xx,
            "reason": "..."
        }
        """

        logger.info("Running local intent classifier...")

        query = query.lower()

        scores = {}

        for intent, keywords in self.INTENT_KEYWORDS.items():

            score = 0

            for keyword in keywords:

                if re.search(rf"\b{re.escape(keyword)}\b", query):
                    score += 1

            scores[intent] = score

        best_intent = max(scores, key=scores.get)

        best_score = scores[best_intent]

        if best_score == 0:

            logger.warning(
                "No intent matched. Falling back to troubleshooting."
            )

            return {
                "intent": "troubleshooting",
                "confidence": 0.50,
                "reason": "Default fallback",
            }

        confidence = min(
            0.70 + (best_score * 0.10),
            0.99,
        )

        logger.success(
            f"Intent: {best_intent} | Score: {best_score}"
        )

        return {
            "intent": best_intent,
            "confidence": round(confidence, 2),
            "reason": f"Matched {best_score} keyword(s)",
        }