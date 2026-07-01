"""
vector_store.py

Creates and manages the Chroma Vector Store.

Author: Shubham Chaudhary
"""

from loguru import logger

from langchain_chroma import Chroma

from app.config.settings import (
    CHROMA_PERSIST_DIR,
    COLLECTION_NAME
)


class VectorStore:

    def __init__(
        self,
        embedding_model
    ):

        self.embedding_model = embedding_model

        self.collection_name = COLLECTION_NAME

        self.persist_directory = CHROMA_PERSIST_DIR

        logger.info(
            f"Initializing Chroma collection '{self.collection_name}' "
            f"at '{self.persist_directory}'"
        )

        self.vector_store = Chroma(

            collection_name=self.collection_name,

            embedding_function=self.embedding_model,

            persist_directory=self.persist_directory

        )

        logger.success("Chroma vector store ready.")

    def add_documents(
        self,
        documents
    ):

        logger.info(
            f"Uploading {len(documents)} chunks..."
        )

        self.vector_store.add_documents(documents)

        logger.success(
            "Documents uploaded successfully."
        )

    def get_retriever(
        self,
        k: int = 5
    ):

        return self.vector_store.as_retriever(

            search_kwargs={

                "k": k

            }

        )

    def get_vector_store(self):

        return self.vector_store

    def delete_collection(self):

        logger.warning(
            f"Deleting collection {self.collection_name}"
        )

        self.vector_store.delete_collection()

        logger.success(
            "Collection deleted."
        )