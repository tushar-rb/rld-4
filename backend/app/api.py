"""
FastAPI application for the Revenue Leakage Detection System
"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

from app.models.data_models import Incident, BillingRecord, ProvisioningRecord, UsageRecord, Contract
from app.models.detection_rules import run_all_rules
from app.services.qdrant_client import qdrant_service
from app.agents.crew import rld_agents
from app.agents.tasks import rld_tasks

app = FastAPI(
    title="Revenue Leakage Detection System API",
    description="API for detecting and managing revenue leakage incidents",
    version="0.1.0"
)

# Initialize Qdrant collections on startup
@app.on_event("startup")
async def startup_event():
    """Initialize Qdrant collections on startup"""
    qdrant_service.create_collections()

# Pydantic models for API requests
class DetectionRequest(BaseModel):
    """Request model for running detection"""
    billing_records: List[BillingRecord]
    provisioning_records: List[ProvisioningRecord]
    usage_records: List[UsageRecord]
    contracts: List[Contract]

class DetectionResponse(BaseModel):
    """Response model for detection results"""
    incidents: List[Incident]
    count: int

class IncidentResponse(BaseModel):
    """Response model for incident operations"""
    incident_id: str
    status: str
    message: str

# API endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Revenue Leakage Detection System API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/detect", response_model=DetectionResponse)
async def run_detection(request: DetectionRequest):
    """Run revenue leakage detection on provided data"""
    # Prepare data for detection rules
    detection_data = {
        "billing": request.billing_records,
        "provisioning": request.provisioning_records,
        "usage": request.usage_records,
        "contracts": request.contracts
    }
    
    # Run all detection rules
    incidents = run_all_rules(detection_data)
    
    # Store incidents in Qdrant
    for incident in incidents:
        qdrant_service.upsert_incident(incident.id, incident.dict())
    
    return DetectionResponse(
        incidents=incidents,
        count=len(incidents)
    )

@app.get("/incidents", response_model=List[Incident])
async def list_incidents():
    """List all detected incidents"""
    # In a real implementation, this would query Qdrant
    # For now, returning an empty list
    return []

@app.get("/incidents/{incident_id}", response_model=Incident)
async def get_incident(incident_id: str):
    """Get details of a specific incident"""
    # In a real implementation, this would query Qdrant
    # For now, returning a placeholder
    return Incident(
        id=incident_id,
        type="missing_charge",
        severity="high",
        status="detected",
        description=f"Sample incident {incident_id}",
        financial_impact=0.0,
        currency="USD",
        detection_date=datetime.now(),
        related_entities={},
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)