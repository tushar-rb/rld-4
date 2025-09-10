# Revenue Leakage Detection System

This system detects revenue leakage using CrewAI + Qdrant with Gemini as LLM.

## Components

- Python backend with CrewAI orchestration
- Qdrant vector database for knowledge storage
- React dashboard for visualization

## Setup

1. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration
   ```

## Running the System

### Option 1: Using Docker (Recommended)
```bash
docker-compose up backend
```

### Option 2: Manual Installation

1. Start Qdrant database (using Docker):
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

2. Run the backend:
   ```bash
   cd backend
   python -m app.main
   ```

3. Run the frontend:
   ```bash
   cd frontend
   npm start
   ```

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
│   │   └── config/
│   │       ├── __init__.py
│   │       └── settings.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```