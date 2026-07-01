"""
main.py

FastAPI Entry Point

Author: Shubham Chaudhary
"""

import traceback

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models.retrieve_request import RetrieveRequest
from app.services.retrieval_service import RetrievalService
from app.ingestion.ingest import IngestionPipeline
from app.services.chat_service import ChatService

app = FastAPI(
    title="DevOps AI Copilot",
    version="1.0.0",
    description="Hybrid RAG + Agentic AI"
)

retriever = RetrievalService()
chat_service = ChatService()

@app.get("/")
def health():

    return {
        "status": "running",
        "application": "DevOps AI Copilot"
    }


@app.post("/ingest")
def ingest_documents():

    try:

        pipeline = IngestionPipeline(
            data_directory="data"
        )

        pipeline.run()

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Knowledge Base Created Successfully."
            }
        )

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )




@app.post("/retrieve")
def retrieve(request: RetrieveRequest):

    docs = retriever.retrieve(
        query=request.query,
        intent=request.intent,
        top_k=request.top_k,
    )

    results = []

    for doc in docs:

        results.append(
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
        )

    return {
        "query": request.query,
        "results": results,
    }

class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
def chat(request: ChatRequest):

    return chat_service.chat(request.query)

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }