"""
document_loader.py

Loads all supported documents from the knowledge base
and enriches them with metadata.

Supported Formats:
- PDF
- TXT

Author: Shubham Chaudhary
"""

from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

SUPPORTED_EXTENSIONS = [".pdf", ".txt"]


class DocumentLoader:

    def __init__(self, data_directory: str):
        self.data_directory = Path(data_directory)

    def load_documents(self) -> List[Document]:
        """
        Load every supported document recursively.

        Returns
        -------
        List[Document]
        """

        documents = []

        for file in self.data_directory.rglob("*"):

            if not file.is_file():
                continue

            if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            print(f"Loading : {file.name}")

            loaded_docs = self._load_file(file)

            documents.extend(loaded_docs)

        print(f"\nTotal Documents Loaded : {len(documents)}")

        return documents

    def _load_file(self, file_path: Path) -> List[Document]:
        """
        Load an individual file using the appropriate loader.
        """

        if file_path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file_path))

        elif file_path.suffix.lower() == ".txt":
            loader = TextLoader(
                str(file_path),
                encoding="utf-8"
            )

        else:
            return []

        docs = loader.load()

        document_type = self._get_document_type(file_path)

        for doc in docs:

            doc.metadata.update({

                "document_type": document_type,

                "intent": document_type,

                "source": file_path.name,

                "file_name": file_path.name,

                "file_path": str(file_path),

                "extension": file_path.suffix.lower()

            })

        return docs

    @staticmethod
    def _get_document_type(file_path: Path) -> str:
        """
        Infer document type from parent folder.
        """

        folder = file_path.parent.name.lower()

        mapping = {

            "runbooks": "runbook",

            "rca": "rca",

            "incident_summaries": "incident_summary",

            "troubleshooting": "troubleshooting",

            "sop": "sop",

            "best_practices": "best_practices"

        }

        return mapping.get(folder, "unknown")


if __name__ == "__main__":

    loader = DocumentLoader("data")

    docs = loader.load_documents()

    print("\nExample Metadata\n")

    print(docs[0].metadata)

    print("\n")

    print(docs[0].page_content[:500])