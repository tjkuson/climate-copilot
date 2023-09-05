"""Entry point for the application."""
from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

import pinecone
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

from climate_copilot.load import load_resources
from climate_copilot.utils import pinecone_environment

if TYPE_CHECKING:
    from climate_copilot.utils import PineconeEnvironment


def ask(query: str, pinecone_env: PineconeEnvironment) -> str | None:
    """Ask a question to the chatbot."""
    pinecone.init(api_key=pinecone_env.api_key, environment=pinecone_env.environment)
    embeddings = OpenAIEmbeddings()  # type: ignore[call-arg]
    doc_search = Pinecone.from_existing_index(
        index_name=pinecone_env.index_name,
        embedding=embeddings,
    )
    chat = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=1,
        verbose=True,
    )  # type: ignore[call-arg]
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

    pinecone_env = pinecone_environment()
    if args.load_resources:
        load_resources(pinecone_env)
    elif args.ask:
        res = ask(args.ask, pinecone_env)
        print(res)
    else:
        msg = "Conversation mode not implemented."
        raise NotImplementedError(msg)
