"""Utilities for the Climate Copilot application."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class PineconeEnvironment:
    """Environment variables for Pinecone."""

    api_key: str
    index_name: str
    environment: str


def pinecone_environment() -> PineconeEnvironment:
    """Ensure the required environment variables are set and return them."""
    pinecone_api_key = os.environ.get("PINECONE_API_KEY")
    pinecone_index_name = os.environ.get("PINECONE_INDEX_NAME")
    pinecone_index_environment = os.environ.get("PINECONE_INDEX_ENVIRONMENT")

    if pinecone_api_key is None:
        msg = "PINECONE_API_KEY environment variable is not set."
        raise ValueError(msg)

    if pinecone_index_name is None:
        msg = "PINECONE_INDEX_NAME environment variable is not set."
        raise ValueError(msg)

    if pinecone_index_environment is None:
        msg = "PINECONE_INDEX_ENVIRONMENT environment variable is not set."
        raise ValueError(msg)

    return PineconeEnvironment(
        api_key=pinecone_api_key,
        index_name=pinecone_index_name,
        environment=pinecone_index_environment,
    )
