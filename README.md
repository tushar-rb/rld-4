# Revenue Leakage Detection System

A complete implementation of a Revenue Leakage Detection System using CrewAI + Qdrant with Gemini as LLM.

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── data_models.py
│   │   │   └── detection_rules.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── crew.py
│   │   │   └── tasks.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── qdrant_client.py
│   │   │   ├── qdrant_schema.py
│   │   │   ├── gemini_client.py
│   │   │   └── detection_engine.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── data_generator.py
│   │   │   ├── ocr_reader.py
│   │   │   └── test_data_generator.py
│   │   └── config/
│   │       ├── __init__.py
│   │       └── settings.py
│   ├── streamlit_app/
│   │   └── dashboard.py
│   ├── sample_data/
│   ├── requirements.txt
│   └── README.md
└── README.md
```

## Key Components

### Backend

1. **Data Models** - Pydantic models for all data entities
2. **Detection Rules** - Rule-based anomaly detection for:
   - Missing charges
   - Incorrect rates
   - Usage mismatches
   - Duplicate entries
3. **CrewAI Agents** - Orchestration of investigation workflow using **Gemini 1.5 Pro** as the LLM
4. **Qdrant Integration** - Vector storage for incidents and knowledge
5. **Gemini Integration** - LLM for analysis and embedding
6. **FastAPI Application** - RESTful API endpoints for detection and incident management
7. **Data Generator** - Generate sample PDF, CSV, and JSON files with realistic data
8. **OCR Reader** - Extract text from PDF files using optical character recognition

### Streamlit Dashboard Components

1. **Dashboard Page** - Financial impact metrics and trends visualization
2. **Incident Management** - Filterable table of detected incidents with details
3. **Detection Interface** - Run detection jobs and configure rules
4. **Data Generator** - Generate sample data files and upload your own data
5. **Settings** - System configuration management

## Getting Started

### Option 1: Using Docker (Recommended)

1. Build and run all services:
   ```bash
   docker-compose up --build
   ```

2. Access the services:
   - Streamlit Dashboard: http://localhost:8501
   - Backend API: http://localhost:8000
   - Qdrant Dashboard: http://localhost:6333/dashboard

### Option 2: Manual Installation

1. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration
   ```

3. Start Qdrant database:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

4. Run the backend:
   ```bash
   cd backend
   python3 -m app.main
   ```

5. Run the Streamlit dashboard:
   ```bash
   cd backend
   streamlit run streamlit_app/dashboard.py
   ```

## Data Generator Features

The Data Generator allows you to:
1. **Generate Sample Files**:
   - PDF billing statements with realistic data
   - CSV provisioning records
   - JSON contract information
   
2. **Upload Your Own Data**:
   - Upload PDF, CSV, or JSON files
   - Process uploaded files for analysis
   - Extract text from PDFs using OCR (in full implementation)

3. **File Processing**:
   - Read PDF content using OCR
   - Parse CSV data into structured format
   - Load JSON data for processing

## AI Agents

The system uses CrewAI agents powered by **Google's Gemini 1.5 Pro** LLM:
- **Triage Agent**: Classifies and prioritizes incidents
- **Evidence Collector**: Gathers relevant data
- **RCA Agent**: Performs root cause analysis
- **Ticket Creator**: Creates investigation tickets

## Architecture

```
Ingest → Kafka/stream → Enrichment → Detection → CrewAI Investigation → Qdrant KB → Ticketing + Dashboard
```

## Key Features

- Real-time rule-based + ML anomaly detection
- Vector storage of enriched incidents and knowledge
- CrewAI agents for triage, evidence collection, RCA, and ticketing (powered by Gemini)
- Auto-creation and routing of investigation tickets
- Dashboard for monitoring and reporting
- Financial impact tracking and trends
- RESTful API for integration with other systems
- Docker-based deployment for easy scaling
- Data generator for testing and development
- OCR capabilities for processing PDF documents