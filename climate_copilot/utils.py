import os


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
