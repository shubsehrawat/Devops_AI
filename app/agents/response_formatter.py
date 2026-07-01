"""
Response Formatter Agent

Generates intent-specific prompts for the LLM.

Instead of formatting the answer after generation,
this agent instructs the LLM how the response should
be structured.
"""

from __future__ import annotations


class ResponseFormatter:
    """
    Generates prompt templates based on intent.
    """

    def get_prompt(
        self,
        intent: str,
        query: str,
        context: str,
    ) -> str:

        formatter = self._get_formatter(intent)

        return f"""
            You are an Enterprise DevOps AI Copilot.

            Answer ONLY using the supplied enterprise documentation.

            If the answer is not present in the context,
            respond with:

            "I couldn't find sufficient information in the enterprise knowledge base."

            Never hallucinate.

            --------------------------------------------
            Intent
            --------------------------------------------

            {intent}

            --------------------------------------------
            Enterprise Context
            --------------------------------------------

            {context}

            --------------------------------------------
            User Question
            --------------------------------------------

            {query}

            --------------------------------------------
            Response Format
            --------------------------------------------

            {formatter}

            Always mention the source documents used.

            Answer:
            """

    def _get_formatter(self, intent: str) -> str:

        templates = {

            "rca": """
            Provide the answer using the following sections:

            ## Issue Summary

            ## Root Cause

            ## Business Impact

            ## Resolution

            ## Preventive Actions

            """,

            "runbook": """
                Provide the answer using the following sections:

                ## Purpose

                ## Prerequisites

                ## Execution Steps

                ## Commands

                ## Verification

                ## Rollback Procedure


                """,

            "incident_summary": """
                Provide the answer using the following sections:

                ## Incident Overview

                ## Timeline

                ## Services Affected

                ## Business Impact

                ## Actions Taken

                ## Current Status

                ## Lessons Learned


                """,

            "troubleshooting": """
                Provide the answer using the following sections:

                ## Problem

                ## Possible Causes

                ## Diagnostic Steps

                ## Resolution Steps

                ## Verification


                """,

            "sop": """
                Provide the answer using the following sections:

                ## Objective

                ## Scope

                ## Preconditions

                ## Procedure

                ## Validation

                ## Rollback

                """,

            "best_practices": """
                Provide the answer using the following sections:

                ## Recommendations

                ## Why It Matters

                ## Implementation Guidelines

                ## Common Mistakes

                ## References
                """,
        }

        return templates.get(
            intent,
            """
                Provide a concise enterprise answer.

                Include Sources.
                """
                        )