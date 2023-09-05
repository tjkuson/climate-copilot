"""Entry point for the application."""
from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import pinecone
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone

if TYPE_CHECKING:
    from langchain.schema import Document


def pinecone_environment_variables() -> tuple[str, str]:
    """Ensure the required environment variables are set."""
    PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")

    if PINECONE_API_KEY is None:
        msg = "PINECONE_API_KEY environment variable is not set."
        raise ValueError(msg)

    if PINECONE_ENVIRONMENT is None:
        msg = "PINECONE_ENVIRONMENT environment variable is not set."
        raise ValueError(msg)

    return PINECONE_API_KEY, PINECONE_ENVIRONMENT


def ingest_resources(directory: Path) -> list[Document]:
    """Ingest the resources from the given directory."""
    loader = PyPDFDirectoryLoader(directory)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200, chunk_overlap=50, separators=["\n", "\r\n"],
    )
    return loader.load_and_split(text_splitter)


def load_resources() -> None:
    """Load the resources into Pinecone."""
    PINECONE_API_KEY, PINECONE_ENVIRONMENT = pinecone_environment_variables()

    print("Connecting to Pinecone...")
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    embeddings = OpenAIEmbeddings()

    print("Loading resources...")
    resources_dir = Path(__file__).parent / "resources"
    pages = ingest_resources(resources_dir)
    Pinecone.from_documents(
        documents=pages, embedding=embeddings, index_name="climate-copilot-text-db",
    )

    print("Loaded resources into Pinecone.")


if __name__ == "__main__":
    ...
