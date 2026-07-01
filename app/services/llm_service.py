"""
LLM Service

Responsible for interacting with Google Gemini.

Responsibilities:
- Initialize Gemini client
- Build prompts
- Generate grounded responses using retrieved context
"""

from __future__ import annotations
import time
from google import genai
from google.genai import types
from loguru import logger

from app.config.settings import GOOGLE_API_KEY


class LLMService:
    """
    Service responsible for interacting with Gemini.
    """

    def __init__(self) -> None:

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

        self.model = "gemini-3.1-flash-lite"

        logger.info(f"Initialized Gemini Model: {self.model}")

    def generate_response(self, prompt: str) -> str:

        logger.info(f"Prompt Length : {len(prompt)} characters")

        start = time.perf_counter()

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=700,
            ),
        )

        logger.info(
            f"Gemini Response Time : {time.perf_counter() - start:.2f} sec"
        )

        logger.info("=" * 80)
        logger.info("PROMPT SENT TO GEMINI")
        logger.info("=" * 80)
        logger.info(prompt)
        logger.info("=" * 80)


        logger.info("=" * 80)
        logger.info("RAW GEMINI RESPONSE")
        logger.info("=" * 80)
        logger.info(response)
        logger.info("=" * 80)

        print(response)
        return response.text