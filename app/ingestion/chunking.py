"""
chunking.py

Splits documents into semantically meaningful chunks
while preserving metadata.

Author: Shubham Chaudhary
"""

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


class DocumentChunker:

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
    ):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=self.chunk_size,

            chunk_overlap=self.chunk_overlap,

            separators=[
                "\n## ",
                "\n### ",
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def split_documents(
        self,
        documents: List[Document]
    ) -> List[Document]:

        chunked_documents = []

        for document in documents:

            chunks = self.splitter.split_text(
                document.page_content
            )

            total_chunks = len(chunks)

            for index, chunk in enumerate(chunks):

                metadata = document.metadata.copy()

                metadata["chunk_id"] = (
                    f"{metadata['source']}"
                    f"_page_{metadata.get('page',0)}"
                    f"_chunk_{index+1}"
                )

                metadata["chunk_number"] = index + 1

                metadata["total_chunks"] = total_chunks

                metadata["chunk_size"] = len(chunk)

                chunked_documents.append(

                    Document(

                        page_content=chunk,

                        metadata=metadata

                    )

                )

        print("=" * 60)
        print(f"Original Documents : {len(documents)}")
        print(f"Total Chunks       : {len(chunked_documents)}")
        print("=" * 60)

        return chunked_documents