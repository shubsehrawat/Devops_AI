# Enterprise DevOps AI

A Hybrid RAG + Agentic AI application that enables engineers to query enterprise DevOps knowledge using natural language. The system retrieves relevant operational documents, grounds responses using enterprise documentation, and generates structured answers tailored to the type of request.

---

# Problem Statement

Modern DevOps teams manage a large collection of operational documentation, including runbooks, incident reports, root cause analyses, SOPs, troubleshooting guides, and best practice documents. As organizations grow, locating the right document quickly becomes increasingly difficult.

Engineers often spend valuable time searching through documentation to answer questions such as:

- Why did the Payment API fail yesterday?
- Give me the Kubernetes deployment runbook.
- Summarize Incident INC-003.
- How do I troubleshoot CrashLoopBackOff?
- What is the Production Deployment SOP?
- What are the Kubernetes security best practices?

The objective of this project is to build an intelligent Enterprise DevOps AI Copilot capable of understanding the user's intent, retrieving only the relevant enterprise documentation, and generating accurate, structured, and grounded responses.

The solution combines Hybrid Retrieval-Augmented Generation (RAG) with an Agentic AI workflow to improve retrieval accuracy and response quality.

---

# System Architecture

```
                    User
                      │
                      ▼
              Streamlit Frontend
                      │
                      ▼
                FastAPI Backend
                      │
                      ▼
           Intent Classification Agent
                      │
                      ▼
          Metadata Filter Generation
                      │
                      ▼
             ChromaDB Vector Search
                      │
                      ▼
          Document Ranking & Selection
                      │
                      ▼
              Context Builder Agent
                      │
                      ▼
           Response Formatter Agent
                      │
                      ▼
              Google Gemini Flash
                      │
                      ▼
             Structured Final Answer
```

---

# Project Structure

```
Devops AI/

│

├── app/
│   ├── agents/
│   │      intent_classifier.py
│   │      response_formatter.py
│   │
│   ├── config/
│   │      settings.py
│   │
│   ├── ingestion/
│   │      document_loader.py
│   │      chunking.py
│   │      embeddings.py
│   │      ingest.py
│   │      vector_store.py
│   │
│   ├── services/
│   │      retrieval_service.py
│   │      context_builder.py
│   │      llm_service.py
│   │      chat_service.py
│   │
│   ├── main.py
│
├── data/
├── evaluation
│   ├── evaluator.py
│   ├── ragas_evaluator.py
│   ├── retrieval_metrics.py
│   ├── run_evaluation.py
│   ├── test_queries.py
│
├── chroma_db/
│
├── streamlit_app.py
│
├── requirements.txt
│
└── README.md
```

---

# Tech Stack Used

| Component | Technology |
|------------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | Google Gemini 2.5 Flash Lite |
| Framework | LangChain |
| Embedding Model | BAAI/bge-base-en-v1.5 |
| Vector Database | ChromaDB |
| Language | Python |
| Logging | Loguru |
| Document Formats | PDF, TXT |
| Evaluation | Precision@K, Recall@K, RAGAS |

---

# Architecture Decision Record

## Why Hybrid RAG?

Instead of relying solely on an LLM, the system retrieves relevant enterprise documents before generating a response. This grounds the LLM's answers in enterprise knowledge and significantly reduces hallucinations.

---

## Why an Agentic Workflow?

Rather than building a generic chatbot, the application is composed of specialized agents, each responsible for a single task.

- Intent Classification Agent
- Retrieval Service
- Context Builder
- Response Formatter
- LLM Service

This separation keeps the system modular, easier to maintain, and easier to extend.

---

## Why Metadata-Based Retrieval?

Each document is tagged with metadata such as:

- document_type
- source
- page
- chunk_number

Instead of searching the entire knowledge base, the retriever first filters documents based on the detected intent. This improves retrieval relevance while reducing the search space.

---

# Key Technical Decisions

## LLM Selection

**Model Used**

Google Gemini 2.5 Flash Lite

### Why?

- Excellent reasoning capability
- Fast inference
- Cost-effective compared to larger models
- Strong performance on structured enterprise documentation
- Native JSON generation support

The LLM is used only for answer generation, while retrieval is handled separately to improve grounding.

---

## Vector Database

**Chosen Database**

ChromaDB

### Why?

- Lightweight
- Easy local deployment
- Native LangChain integration
- Persistent storage
- Suitable for medium-sized enterprise document collections

For the scope of this project, ChromaDB provides an excellent balance between simplicity and retrieval performance.

---

## Embedding Model

**Model**

BAAI/bge-base-en-v1.5

### Why?

- High MTEB ranking
- Strong semantic retrieval quality
- 768-dimensional embeddings
- Better retrieval performance than MiniLM
- Completely open source

Embeddings are normalized before indexing to improve cosine similarity search.

---

## Chunking Strategy

Documents are chunked using:

**RecursiveCharacterTextSplitter**

Configuration:

```
Chunk Size      : 800
Chunk Overlap   : 100
```

### Why?

Recursive chunking preserves the logical structure of technical documentation while preventing chunks from breaking in the middle of important sections.

The overlap ensures continuity between adjacent chunks.

---

## Framework Choice

**LangChain**

### Why?

LangChain provides:

- Standard document abstraction
- Embedding integration
- ChromaDB integration
- Prompt management
- Extensibility for future agent workflows

Given the project timeline, LangChain significantly reduced implementation effort while maintaining clean architecture.

---

## Agentic Design

The system is composed of independent agents.

### Intent Classification Agent

Classifies the incoming query into one of six document categories.

- Runbook
- RCA
- Incident Summary
- Troubleshooting
- SOP
- Best Practices

A lightweight local classifier is used instead of an LLM because the intent space is fixed and well-defined, resulting in significantly lower latency and zero inference cost.

---

### Retrieval Service

Responsible for:

- Metadata filtering
- Semantic search
- Document ranking
- Returning complete documents rather than isolated chunks

---

### Context Builder

Combines retrieved chunks into a structured context before sending them to the LLM.

---

### Response Formatter Agent

Generates intent-specific response templates so that answers follow consistent enterprise documentation standards.

---

### LLM Service

Responsible only for interacting with Gemini and generating grounded responses.

---

# Retrieval Workflow

```
User Query

↓

Intent Classification

↓

Metadata Filtering

↓

Vector Search

↓

Document Ranking

↓

Context Building

↓

Gemini

↓

Structured Response
```

---

# Trade-offs Considered

## Accuracy vs Cost vs Latency

Several trade-offs were considered during implementation.

### Accuracy

Priority was given to retrieval accuracy by:

- Metadata filtering
- Semantic embeddings
- Document-level retrieval
- Grounded generation

---

### Cost

To reduce cost:

- Open-source embedding model
- Local ChromaDB deployment
- Lightweight intent classifier
- Gemini used only for response generation

No unnecessary LLM calls are made during retrieval.

---

### Latency

Latency was reduced by:

- Local vector search
- Local intent classification
- Persistent Chroma database
- Metadata filtering before retrieval

---

# What I Would Improve With More Time

Given additional development time, the following improvements would be implemented:

- Hybrid Search (BM25 + Dense Retrieval)
- Cross-Encoder reranking
- Multi-agent orchestration using LangGraph
- Conversation memory
- Feedback-driven retrieval optimization
- Query rewriting agent
- Streaming responses
- Authentication and role-based access control
- Docker and Kubernetes deployment
- CI/CD pipeline
- Monitoring with Prometheus and Grafana

---

# Production Considerations

Several production aspects were considered while designing the application.

### Scalability

- Replace ChromaDB with Qdrant or Azure AI Search
- Horizontal FastAPI deployment
- Distributed embedding generation

### Observability

- Structured logging
- Request tracing
- Retrieval metrics
- LLM latency monitoring

---

### Evaluation

The retrieval pipeline can be evaluated using:

- Precision@K
- Recall@K

The generation quality can be evaluated using:

- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall

using the RAGAS evaluation framework.

---

# Future Enhancements

- Hybrid Search (BM25 + Vector Search)
- Cross-Encoder Reranking
- LangGraph Multi-Agent Workflow
- Human Feedback Loop
- Automatic Knowledge Base Updates
- Real-time Document Ingestion
- Enterprise Authentication
- Containerized Deployment

---

# Conclusion

This project demonstrates a production-inspired Hybrid RAG + Agentic AI architecture for enterprise knowledge retrieval. Rather than functioning as a generic chatbot, the application uses specialized agents for intent classification, retrieval, context construction, response formatting, and grounded answer generation.

The modular architecture allows individual components to evolve independently, making the solution maintainable, scalable, and suitable for enterprise environments while remaining lightweight enough for rapid development.