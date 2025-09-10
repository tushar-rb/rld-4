# Revenue Leakage Detection System

A system to detect revenue leakage using CrewAI + Qdrant with Gemini as LLM.

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
│   ├── streamlit_app/
│   │   └── dashboard.py
│   ├── requirements.txt
│   └── README.md
└── README.md
```