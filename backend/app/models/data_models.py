"""
Data models for the Revenue Leakage Detection System
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class BillingRecord(BaseModel):
    """Model for billing records"""
    id: str
    customer_id: str
    invoice_id: str
    service_id: str
    amount: float
    currency: str
    billing_date: datetime
    due_date: datetime
    status: str  # paid, unpaid, overdue
    billing_period_start: datetime
    billing_period_end: datetime

class ProvisioningRecord(BaseModel):
    """Model for service provisioning records"""
    id: str
    customer_id: str
    service_id: str
    provision_date: datetime
    status: str  # active, inactive, suspended
    plan_id: str
    start_date: datetime
    end_date: Optional[datetime] = None

class UsageRecord(BaseModel):
    """Model for usage logs"""
    id: str
    customer_id: str
    service_id: str
    usage_date: datetime
    usage_type: str
    quantity: float
    unit: str
    cost: float

class ContractClause(BaseModel):
    """Model for contract clauses"""
    id: str
    contract_id: str
    clause_type: str  # rate, service_level, penalty, etc.
    content: str
    effective_date: datetime
    expiry_date: Optional[datetime] = None

class Contract(BaseModel):
    """Model for contracts"""
    id: str
    customer_id: str
    contract_date: datetime
    effective_date: datetime
    expiry_date: Optional[datetime] = None
    status: str  # active, expired, terminated
    clauses: List[ContractClause] = []

class Incident(BaseModel):
    """Model for detected incidents"""
    id: str
    type: str  # missing_charge, incorrect_rate, usage_mismatch, duplicate
    severity: str  # low, medium, high, critical
    status: str  # detected, investigating, resolved, closed
    description: str
    financial_impact: float
    currency: str
    detection_date: datetime
    related_entities: Dict[str, str]  # References to related records
    evidence: List[str] = []  # References to evidence
    root_cause: Optional[str] = None
    resolution: Optional[str] = None
    created_at: datetime
    updated_at: datetime