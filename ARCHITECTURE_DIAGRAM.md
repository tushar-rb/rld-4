# Revenue Leakage Detection System
## Architecture Diagram (Text Version)

```
┌─────────────────┐    ┌──────────────┐    ┌────────────┐    ┌──────────┐
│   Data Sources  │───▶│   Ingestion  │───▶│Enrichment  │───▶│Detection │
│                 │    │   Layer      │    │   Layer    │    │  Engine  │
│ ┌─────────────┐ │    └──────────────┘    └────────────┘    └──────────┘
│ │ Billing     │ │                                                │
│ ├─────────────┤ │                                                ▼
│ │Provisioning │ │    ┌──────────────┐    ┌────────────┐    ┌──────────┐
│ ├─────────────┤ │───▶│   Stream     │───▶│   Rule-    │───▶│   ML     │
│ │ Usage Logs  │ │    │  Processing  │    │   Based    │    │Anomaly   │
│ ├─────────────┤ │    └──────────────┘    │ Detection  │    │Detection │
│ │ Contracts   │ │                        └────────────┘    └──────────┘
└─────────────────┘                                                │
                                                                   ▼
                                                        ┌──────────────────┐
                                                        │  CrewAI Agents   │
                                                        │                  │
                                                        │ ┌──────────────┐ │
                                                        │ │ Triage Agent │ │
                                                        │ ├──────────────┤ │
                                                        │ │Evidence      │ │
                                                        │ │Collector     │ │
                                                        │ ├──────────────┤ │
                                                        │ │ RCA Agent    │ │
                                                        │ ├──────────────┤ │
                                                        │ │Ticket Creator│ │
                                                        │ └──────────────┘ │
                                                        └──────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌──────────────────┐
                                                        │  Qdrant Vector   │
                                                        │   Database       │
                                                        │                  │
                                                        │ ┌──────────────┐ │
                                                        │ │ Incidents    │ │
                                                        │ ├──────────────┤ │
                                                        │ │ Contracts    │ │
                                                        │ ├──────────────┤ │
                                                        │ │ Usage        │ │
                                                        │ │ Templates    │ │
                                                        │ ├──────────────┤ │
                                                        │ │ Knowledge    │ │
                                                        │ │ Base         │ │
                                                        │ └──────────────┘ │
                                                        └──────────────────┘
                                                                   │
                                                                   ▼
                                                        ┌──────────────────┐
                                                        │ Resolution &     │
                                                        │ Reporting        │
                                                        │                  │
                                                        │ ┌──────────────┐ │
                                                        │ │ Ticketing    │ │
                                                        │ │ Systems      │ │
                                                        │ ├──────────────┤ │
                                                        │ │ Dashboard    │ │
                                                        │ │ (Streamlit)  │ │
                                                        │ └──────────────┘ │
                                                        └──────────────────┘
```

This diagram shows the flow from data sources through detection and AI investigation to resolution and reporting.