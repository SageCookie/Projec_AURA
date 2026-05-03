# Project_AURA
Autonomous multi-agent Research Assistant

AURA is an intelligent, self-scheduling research engine designed to autonomously navigate the web, extract high-signal information, and synthesize structured knowledge. Built with a modular, agent-first architecture, AURA transforms messy web data into a searchable, AI-ready memory bank.

🚀 The Vision
Most research tools require manual input. AURA operates on a "Heartbeat" principle—waking up daily to scout for new information, process it through specialized LLM agents, and store it for long-term retrieval. It is designed to be lean enough to run on local consumer hardware (RTX 3050+) while remaining scalable for cloud deployment.

🛠️ Modular Architecture
The system is divided into six independent modules to ensure stability and maintainability:

Module 1: The Collector – High-performance web scraping using Crawl4AI and Playwright to convert URLs into clean, LLM-optimized Markdown.

Module 2: The Brain – Structured information extraction using Gemini/Llama and Pydantic for zero-error JSON parsing.

Module 3: The Memory – A persistent storage layer powered by Supabase (PostgreSQL), designed for future semantic search integration.

Module 4: Agentic Workflow – Multi-agent orchestration via CrewAI, featuring "Scout," "Analyst," and "Archivist" personas.

Module 5: The Storefront – A modern UI built with FastAPI and Streamlit for data visualization and interaction.

Module 6: The Heartbeat – Fully automated execution cycles managed by GitHub Actions.

🧠 Tech Stack
Language: Python 3.11+

Orchestration: CrewAI / LangGraph

Scraping: Crawl4AI, Playwright

Database: Supabase (PostgreSQL)

Models: Google Gemini API / Local Llama 3 (via Ollama)

Automation: GitHub Actions

📈 Roadmap
[ ] Implement robust get_content function with Crawl4AI.

[ ] Design Pydantic schemas for structured research output.

[ ] Set up Supabase table migrations.

[ ] Configure CrewAI agent collaboration logic.

[ ] Build Streamlit dashboard for real-time monitoring.

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
    