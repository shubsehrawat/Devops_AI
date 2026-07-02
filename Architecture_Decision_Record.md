# Architecture Decision Record (ADR)

## ADR-001: Hybrid Retrieval-Augmented Generation (RAG)

**Status:** Accepted

### Context

Enterprise DevOps documentation is distributed across multiple document
types, including Runbooks, Root Cause Analyses (RCA), Incident
Summaries, Standard Operating Procedures (SOPs), Troubleshooting Guides,
and Best Practices. Using a standalone Large Language Model (LLM) would
rely solely on its pre-trained knowledge, which could result in
inaccurate or hallucinated responses.

### Decision

Adopt a **Hybrid Retrieval-Augmented Generation (RAG)** architecture
where relevant enterprise documents are retrieved before generating a
response.

### Rationale

-   Grounds responses in enterprise knowledge.
-   Minimizes hallucinations.
-   Ensures answers remain traceable to source documents.
-   Allows the knowledge base to evolve without retraining the LLM.

### Consequences

-   Requires an embedding pipeline and vector database.
-   Introduces a retrieval step before inference.
-   Significantly improves response reliability.

------------------------------------------------------------------------

## ADR-002: Agentic Workflow

**Status:** Accepted

### Decision

Implement an Agentic AI workflow composed of independent services:

-   Intent Classification Agent
-   Retrieval Service
-   Context Builder
-   Response Formatter
-   LLM Service

### Rationale

-   Clear separation of responsibilities
-   Easier maintenance and testing
-   Supports future scalability

------------------------------------------------------------------------

## ADR-003: Metadata-Based Retrieval

**Status:** Accepted

### Decision

Use intent classification to filter documents before semantic search.

``` text
User Query --> Intent Classification --> Metadata Filter --> Semantic Retrieval
```

### Rationale

-   Reduces search space
-   Improves retrieval precision
-   Reduces irrelevant context

------------------------------------------------------------------------

## ADR-004: ChromaDB

**Status:** Accepted

### Decision

Use ChromaDB as the vector database.

### Rationale

-   Open source
-   Local persistence
-   LangChain integration
-   Suitable for assessment-scale enterprise knowledge bases

------------------------------------------------------------------------

## ADR-005: Embedding Model

**Status:** Accepted

### Decision

Use **BAAI/bge-base-en-v1.5**.

### Rationale

-   Strong semantic retrieval
-   High MTEB ranking
-   Open source
-   Normalized embeddings for cosine similarity

------------------------------------------------------------------------

## ADR-006: Chunking Strategy

**Status:** Accepted

### Decision

Use RecursiveCharacterTextSplitter.

-   Chunk Size: 800
-   Chunk Overlap: 100

### Rationale

Preserves document structure while maintaining contextual continuity.

------------------------------------------------------------------------

## ADR-007: Local Intent Classification

**Status:** Accepted

### Decision

Use a lightweight local intent classifier for six predefined document
categories.

### Rationale

-   Low latency
-   No additional LLM cost
-   Deterministic classification

------------------------------------------------------------------------

## ADR-008: Document-Centric Retrieval

**Status:** Accepted

### Decision

Retrieve the highest-ranked document and use its most relevant chunks
rather than mixing unrelated documents.

### Rationale

-   Better grounding
-   Reduced prompt noise
-   Improved answer quality

------------------------------------------------------------------------

## ADR-009: LLM Selection

**Status:** Accepted

### Decision

Use Google Gemini 2.5 Flash Lite.

### Rationale

-   Fast inference
-   Large context window
-   Cost-effective
-   Strong reasoning performance

------------------------------------------------------------------------

## ADR-010: Modular Architecture

**Status:** Accepted

### Decision

Organize the application into modular components:

-   Ingestion
-   Agents
-   Services
-   Evaluation
-   Configuration

### Rationale

Improves maintainability, testability, and extensibility for future
enhancements.
