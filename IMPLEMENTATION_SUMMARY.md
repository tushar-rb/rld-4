# Revenue Leakage Detection System - Implementation Summary

## Overview

This is a Revenue Leakage Detection System built with:
- Python backend using FastAPI and CrewAI for orchestration
- Qdrant vector database for knowledge storage
- **Google's Gemini 1.5 Pro** as the LLM for analysis and embedding
- Streamlit for dashboard with Plotly visualizations

## Backend Components

### 1. Data Models (`app/models/data_models.py`)
- BillingRecord: Billing information
- ProvisioningRecord: Service provisioning data
- UsageRecord: Usage logs
- Contract/ContractClause: Contract information
- Incident: Detected revenue leakage incidents

### 2. Detection Rules (`app/models/detection_rules.py`)
- MissingChargeRule: Detect services provisioned but not billed
- IncorrectRateRule: Detect billing records with wrong rates
- UsageMismatchRule: Detect discrepancies between usage and billing
- DuplicateEntryRule: Detect duplicate billing entries

### 3. Qdrant Integration (`app/services/qdrant_client.py`, `app/services/qdrant_schema.py`)
- Collections for incidents, contract clauses, usage templates, and KB fixes
- Incident upsert with Gemini embeddings
- Similar incident search functionality

### 4. CrewAI Agents (`app/agents/crew.py`, `app/agents/tasks.py`)
- TriageAgent: Classify and prioritize incidents (using Gemini 1.5 Pro)
- EvidenceCollector: Gather relevant data (using Gemini 1.5 Pro)
- RCAAgent: Perform root cause analysis (using Gemini 1.5 Pro)
- TicketCreator: Create investigation tickets (using Gemini 1.5 Pro)

### 5. Gemini Integration (`app/services/gemini_client.py`)
- Text generation using Gemini
- JSON response generation for analysis

### 6. FastAPI Application (`app/api.py`)
- RESTful API endpoints for detection and incident management
- Health checks and monitoring endpoints
- Integration with all system components

### 7. Data Generator (`app/utils/data_generator.py`)
- Generate sample PDF billing statements
- Generate sample CSV provisioning records
- Generate sample JSON contract data
- Read PDF, CSV, and JSON files

### 8. OCR Reader (`app/utils/ocr_reader.py`)
- Extract text from PDF files using OCR
- Preprocess images for better OCR results
- Support for various document formats

## Streamlit Dashboard Components

### 1. Dashboard Page
- Financial impact metrics
- Incident trends visualization
- Root cause distribution charts

### 2. Incidents Page
- Filterable table of incidents
- Severity and status indicators
- Detailed incident view

### 3. Detection Page
- Run detection jobs
- Configure detection rules
- View detection results

### 4. Data Generator Page
- Generate sample PDF, CSV, and JSON files
- Upload your own data files
- Process uploaded files with OCR

### 5. Settings Page
- System configuration
- Qdrant and Gemini settings
- Alerting configuration

## Deployment Options

### 1. Docker Deployment (Recommended)
- `docker-compose.yml` for multi-container orchestration
- Individual Dockerfiles for backend and Streamlit
- Pre-configured Qdrant service

### 2. Manual Installation
- Virtual environment setup script
- Dependency management with pip
- Clear installation instructions

## Example Usage

The system includes examples demonstrating:
1. Rule-based detection of missing charges
2. Qdrant integration for incident storage
3. Similar incident search using embeddings
4. API endpoints for detection and incident management
5. Data generation for testing and development
6. OCR capabilities for processing PDF documents

## Architecture

```
Ingest → Kafka/stream → Enrichment → Detection → CrewAI Investigation → Qdrant KB → Ticketing + Dashboard
```

## Key Features

- Real-time rule-based + ML anomaly detection
- Vector storage of enriched incidents and knowledge
- CrewAI agents for triage, evidence collection, RCA, and ticketing (powered by Gemini 1.5 Pro)
- Auto-creation and routing of investigation tickets
- Dashboard for monitoring and reporting
- Financial impact tracking and trends
- RESTful API for integration with other systems
- Docker-based deployment for easy scaling
- Data generator for testing and development
- OCR capabilities for processing PDF documents