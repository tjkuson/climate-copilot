"""Entry point for the application."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING

import pinecone
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone

if TYPE_CHECKING:
    from langchain.schema import Document


from climate_copilot.utils import pinecone_environment_variables


def ingest_resources(directory: Path) -> list[Document]:
    """Ingest the resources from the given directory."""
    loader = PyPDFDirectoryLoader(directory)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        separators=["\n", "\r\n"],
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
    docs = ingest_resources(resources_dir)
    Pinecone.from_documents(
        documents=docs,
        embedding=embeddings,
        index_name="climate-copilot-text-db",
    )

    print("Loaded resources into Pinecone.")


def ask(query: str) -> dict[str, str]:
    """Ask a question to the chatbot."""
    PINECONE_API_KEY, PINECONE_ENVIRONMENT = pinecone_environment_variables()
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    embeddings = OpenAIEmbeddings()
    doc_search = Pinecone.from_existing_index(
        index_name="climate-copilot-text-db",
        embedding=embeddings,
    )
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1, verbose=True)
    qa = RetrievalQA.from_chain_type(
        chain_type="stuff",
        llm=chat,
        retriever=doc_search.as_retriever(),
    )
    return qa({"query": query}).get("result")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="climate-copilot",
        description="Chatbot that answers questions about climate change.",
    )
    parser.add_argument(
        "--load-resources",
        action="store_true",
        help="Load the resources into Pinecone.",
    )
    parser.add_argument(
        "--ask",
        type=str,
        help="Ask a single question to the chatbot.",
    )
    args = parser.parse_args()

    if args.load_resources:
        load_resources()

    if args.ask:
        print(ask(args.ask))
    else:
        msg = "Conversation mode not implemented."
        raise NotImplementedError(msg)
