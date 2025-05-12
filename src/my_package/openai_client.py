#!/usr/bin/env python3
"""
File: src/my_package/openai_client.py
Description: Example module updated to use the OpenAI Responses API (v1.x SDK).
Author: You <you@example.com>
Version: 0.2.0
"""

import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# ── Load environment ──────────────────────────────────────────────────────────
load_dotenv()  # pulls in .env → OPENAI_API_KEY
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable")

# ── Logging configuration ────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ── Instantiate the Responses client ─────────────────────────────────────────
client = OpenAI()


def get_chat_response(
    message: list[dict[str, str]],
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
) -> str:
    """
    Send a single multi-turn request via the Responses API.

    messages: list of {"role": "system"|"developer"|"user", "content": "..."}
    """
    response = client.responses.create(
        model=model,
        instructions="You are a helpful assistant.",
        input="What's the capital of Missouri?",
        temperature=temperature,
    )
    logger.info("Response: %s", response)
    # Log full object and key metadata
    logger.info("Full Responses API response: %s", response)
    logger.info("Request ID: %s", response.id)
    logger.info("Model used: %s", response.model)
    logger.info("Total tokens used: %d", response.usage.total_tokens)
    # Return the rendered output text
    return response.output_text


def main():

    # Example conversation
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the capital of Missouri?"},
    ]
    answer = get_chat_response(messages)
    print("Chat response:", answer)


if __name__ == "__main__":
    main()
