```mermaid
graph TD
    User([User Query]) --> Orchestrator{LiteLLM Orchestrator}
    
    subgraph Ingestion_Layer [Ingestion & Extraction]
        Orchestrator --> Crawler[Crawl4AI Engine]
        Crawler --> RawData[(Raw Web Content)]
    end
    
    subgraph Validation_Layer [Data Integrity]
        RawData --> PydanticValidator[Pydantic Schema Validation]
        PydanticValidator --> CleanData[Structured Data]
    end
    
    subgraph Intelligence_Layer [LLM Processing]
        CleanData --> Agent1[Research Agent]
        CleanData --> Agent2[Summarization Agent]
        Agent1 & Agent2 --> LLM[Gemini / Gemma Models]
    end
    
    LLM --> FinalReport[Final Markdown Research Report]
    FinalReport --> User
    
   
  
    ```mermaid
    sequenceDiagram
    participant U as User
    participant O as LiteLLM (Controller)
    participant C as Crawl4AI
    participant P as Pydantic Schema
    participant A as AI Models (Gemini/Gemma)

    U->>O: Submits Research Topic
    O->>C: Trigger Scrape (Search URLs)
    C-->>O: Return Raw HTML/Markdown
    O->>P: Pass Data for Validation
    P-->>O: Return Clean JSON/Structured Data
    O->>A: Send Context for Analysis
    A-->>O: Return Research Insights
    O-->>U: Deliver Final Research Report
    