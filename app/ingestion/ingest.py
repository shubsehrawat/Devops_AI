"""
ingest.py

Main ingestion pipeline for the DevOps AI Copilot.

Steps
------
1. Load documents
2. Chunk documents
3. Load embedding model
4. Create Qdrant collection
5. Upload chunks

Author: Shubham Chaudhary
"""

import time

from loguru import logger

from app.ingestion.document_loader import DocumentLoader
from app.ingestion.chunking import DocumentChunker
from app.ingestion.embeddings import EmbeddingModel
from app.ingestion.vector_store import VectorStore


class IngestionPipeline:

    def __init__(self, data_directory: str):

        self.data_directory = data_directory

    def run(self):

        start_time = time.time()

        logger.info("=" * 70)
        logger.info("Starting DevOps AI Knowledge Base Ingestion")
        logger.info("=" * 70)

        ###########################################################
        # Step 1 - Load Documents
        ###########################################################

        logger.info("Step 1 : Loading Documents")

        loader = DocumentLoader(self.data_directory)

        documents = loader.load_documents()

        logger.success(
            f"Loaded {len(documents)} documents."
        )

        ###########################################################
        # Step 2 - Chunk Documents
        ###########################################################

        logger.info("Step 2 : Chunking Documents")

        chunker = DocumentChunker()

        chunks = chunker.split_documents(documents)

        logger.success(
            f"Created {len(chunks)} chunks."
        )

        ###########################################################
        # Step 3 - Load Embedding Model
        ###########################################################

        logger.info("Step 3 : Loading Embedding Model")

        embedding_model = EmbeddingModel().get_embeddings()

        logger.success("Embedding model loaded successfully.")

        ###########################################################
        # Step 4 - Create Qdrant Collection
        ###########################################################

        logger.info("Step 4 : Connecting to Qdrant")

        vector_store = VectorStore(
            embedding_model=embedding_model
        )

        logger.success("Connected to Qdrant.")

        ###########################################################
        # Step 5 - Upload Chunks
        ###########################################################

        logger.info("Step 5 : Uploading Chunks")

        vector_store.add_documents(chunks)

        logger.success("Knowledge Base Created Successfully")

        ###########################################################
        # Summary
        ###########################################################

        elapsed = round(time.time() - start_time, 2)

        logger.info("=" * 70)
        logger.info("Ingestion Summary")
        logger.info("=" * 70)

        logger.info(f"Documents Loaded : {len(documents)}")
        logger.info(f"Chunks Created   : {len(chunks)}")
        logger.info(f"Collection Name  : {vector_store.collection_name}")
        logger.info(f"Execution Time   : {elapsed} seconds")

        logger.success("Pipeline Completed Successfully")


if __name__ == "__main__":

    pipeline = IngestionPipeline(
        data_directory="data"
    )

    pipeline.run()