"""
Example of rule-based detection and Qdrant integration
"""
from app.models.detection_rules import run_all_rules, MISSING_CHARGE_RULE
from app.models.data_models import BillingRecord, ProvisioningRecord, UsageRecord, Contract, ContractClause
from app.services.qdrant_schema import upsert_incident_example, search_similar_incidents
from datetime import datetime

def example_rule_detection():
    """Example showing how to use detection rules"""
    
    # Sample data representing a scenario with missing charges
    sample_data = {
        "provisioning": [
            ProvisioningRecord(
                id="PROV-001",
                customer_id="CUST-123",
                service_id="SERVICE-001",
                provision_date=datetime(2023, 6, 1),
                status="active",
                plan_id="PLAN-BASIC",
                start_date=datetime(2023, 6, 1)
            )
        ],
        "billing": [
            BillingRecord(
                id="BILL-001",
                customer_id="CUST-123",
                invoice_id="INV-001",
                service_id="SERVICE-002",  # Different service - this will cause a missing charge detection
                amount=99.99,
                currency="USD",
                billing_date=datetime(2023, 6, 1),
                due_date=datetime(2023, 6, 15),
                status="paid",
                billing_period_start=datetime(2023, 6, 1),
                billing_period_end=datetime(2023, 6, 30)
            )
        ]
    }
    
    print("=== Rule-Based Detection Example ===")
    print("Checking for missing charges...")
    
    # Run just the missing charge rule
    incidents = MISSING_CHARGE_RULE.check(sample_data)
    
    print(f"Found {len(incidents)} missing charge incidents")
    
    for incident in incidents:
        print(f"\nIncident ID: {incident.id}")
        print(f"Type: {incident.type}")
        print(f"Severity: {incident.severity}")
        print(f"Description: {incident.description}")
        print(f"Financial Impact: ${incident.financial_impact} {incident.currency}")
        print(f"Related Entities: {incident.related_entities}")
    
    return incidents

def example_qdrant_upsert():
    """Example showing how to upsert incidents to Qdrant"""
    print("\n=== Qdrant Integration Example ===")
    
    # Upsert a sample incident
    incident_id = upsert_incident_example()
    
    if incident_id:
        print(f"Successfully upserted incident {incident_id} to Qdrant")
        
        # Search for similar incidents
        print("Searching for similar incidents...")
        similar_incidents = search_similar_incidents(
            "Service provisioned but not billed"
        )
        
        print(f"Found {len(similar_incidents)} similar incidents")
        
        for incident in similar_incidents:
            print(f" - Similar incident: {incident.id} (score: {incident.score})")
    
    return incident_id

if __name__ == "__main__":
    # Run examples
    incidents = example_rule_detection()
    incident_id = example_qdrant_upsert()
    
    print("\n=== Examples Complete ===")