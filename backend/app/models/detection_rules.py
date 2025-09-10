"""
Rule-based detection functions for revenue leakage
"""
from typing import List, Dict, Any
from app.models.data_models import BillingRecord, ProvisioningRecord, UsageRecord, Incident
from datetime import datetime
import uuid

class DetectionRule:
    """Base class for detection rules"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def check(self, data: Dict[str, Any]) -> List[Incident]:
        """Check for incidents based on this rule"""
        raise NotImplementedError("Subclasses must implement check method")

class MissingChargeRule(DetectionRule):
    """Detect missing charges - services provisioned but not billed"""
    
    def __init__(self):
        super().__init__(
            "Missing Charge Detection",
            "Detect services that have been provisioned but not billed"
        )
    
    def check(self, data: Dict[str, Any]) -> List[Incident]:
        """
        Check for missing charges by comparing provisioning and billing records
        
        Args:
            data: Dictionary containing 'provisioning' and 'billing' lists
            
        Returns:
            List of Incident objects representing detected missing charges
        """
        incidents = []
        provisioning_records = data.get('provisioning', [])
        billing_records = data.get('billing', [])
        
        # Create a set of billed service IDs for quick lookup
        billed_services = {
            (record.customer_id, record.service_id, record.billing_period_start.date(), record.billing_period_end.date())
            for record in billing_records
        }
        
        # Check each provisioning record
        for provision in provisioning_records:
            # Check if this provisioned service was billed
            billed = any(
                bill.customer_id == provision.customer_id and
                bill.service_id == provision.service_id and
                bill.billing_period_start.date() <= provision.start_date.date() <= bill.billing_period_end.date()
                for bill in billing_records
            )
            
            if not billed:
                # Create incident for missing charge
                incident = Incident(
                    id=str(uuid.uuid4()),
                    type="missing_charge",
                    severity="high",
                    status="detected",
                    description=f"Service {provision.service_id} provisioned for customer {provision.customer_id} but not billed",
                    financial_impact=0.0,  # Would be calculated based on contract rates
                    currency="USD",
                    detection_date=datetime.now(),
                    related_entities={
                        "provisioning_id": provision.id,
                        "customer_id": provision.customer_id,
                        "service_id": provision.service_id
                    },
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                incidents.append(incident)
        
        return incidents

class IncorrectRateRule(DetectionRule):
    """Detect incorrect billing rates"""
    
    def __init__(self):
        super().__init__(
            "Incorrect Rate Detection",
            "Detect billing records with rates that don't match contract terms"
        )
    
    def check(self, data: Dict[str, Any]) -> List[Incident]:
        """
        Check for incorrect rates by comparing billing records with contract terms
        
        Args:
            data: Dictionary containing 'billing', 'contracts', and 'clauses' lists
            
        Returns:
            List of Incident objects representing detected incorrect rates
        """
        incidents = []
        billing_records = data.get('billing', [])
        contracts = data.get('contracts', [])
        clauses = data.get('clauses', [])
        
        # Create mapping of contracts and clauses for quick lookup
        contract_map = {contract.id: contract for contract in contracts}
        clause_map = {clause.contract_id: clause for clause in clauses if clause.clause_type == "rate"}
        
        # Check each billing record
        for bill in billing_records:
            # Find related contract and rate clause
            customer_contracts = [
                contract for contract in contracts 
                if contract.customer_id == bill.customer_id
            ]
            
            # Find active contract for billing period
            active_contract = None
            for contract in customer_contracts:
                if (contract.effective_date <= bill.billing_date and 
                    (contract.expiry_date is None or contract.expiry_date >= bill.billing_date)):
                    active_contract = contract
                    break
            
            if active_contract:
                # Find rate clause for this contract
                rate_clause = clause_map.get(active_contract.id)
                if rate_clause:
                    # In a real implementation, we would parse the rate from the clause
                    # and compare it with the billing record amount
                    # For this example, we'll just create a placeholder check
                    expected_rate = 100.0  # This would come from contract parsing
                    if abs(bill.amount - expected_rate) > 1.0:  # Allow for small rounding differences
                        incident = Incident(
                            id=str(uuid.uuid4()),
                            type="incorrect_rate",
                            severity="medium",
                            status="detected",
                            description=f"Incorrect rate for service {bill.service_id}, customer {bill.customer_id}",
                            financial_impact=abs(bill.amount - expected_rate),
                            currency=bill.currency,
                            detection_date=datetime.now(),
                            related_entities={
                                "billing_id": bill.id,
                                "contract_id": active_contract.id,
                                "clause_id": rate_clause.id
                            },
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )
                        incidents.append(incident)
        
        return incidents

class UsageMismatchRule(DetectionRule):
    """Detect usage mismatches - billed usage not matching actual usage"""
    
    def __init__(self):
        super().__init__(
            "Usage Mismatch Detection",
            "Detect discrepancies between billed usage and actual usage logs"
        )
    
    def check(self, data: Dict[str, Any]) -> List[Incident]:
        """
        Check for usage mismatches by comparing billing and usage records
        
        Args:
            data: Dictionary containing 'billing' and 'usage' lists
            
        Returns:
            List of Incident objects representing detected usage mismatches
        """
        incidents = []
        billing_records = data.get('billing', [])
        usage_records = data.get('usage', [])
        
        # Group usage records by customer, service, and date for aggregation
        usage_by_service = {}
        for usage in usage_records:
            key = (usage.customer_id, usage.service_id, usage.usage_date.date())
            if key not in usage_by_service:
                usage_by_service[key] = 0
            usage_by_service[key] += usage.quantity
        
        # Check each billing record
        for bill in billing_records:
            # Find corresponding usage records
            usage_key = (bill.customer_id, bill.service_id, bill.billing_date.date())
            actual_usage = usage_by_service.get(usage_key, 0)
            
            # In a real implementation, we would convert usage units and calculate expected billing
            # For this example, we'll assume 1 unit = $1
            expected_billing = actual_usage
            if abs(bill.amount - expected_billing) > 1.0:  # Allow for small rounding differences
                incident = Incident(
                    id=str(uuid.uuid4()),
                    type="usage_mismatch",
                    severity="medium",
                    status="detected",
                    description=f"Usage mismatch for service {bill.service_id}, customer {bill.customer_id}",
                    financial_impact=abs(bill.amount - expected_billing),
                    currency=bill.currency,
                    detection_date=datetime.now(),
                    related_entities={
                        "billing_id": bill.id,
                        "usage_date": str(bill.billing_date.date())
                    },
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                incidents.append(incident)
        
        return incidents

class DuplicateEntryRule(DetectionRule):
    """Detect duplicate billing entries"""
    
    def __init__(self):
        super().__init__(
            "Duplicate Entry Detection",
            "Detect duplicate billing records"
        )
    
    def check(self, data: Dict[str, Any]) -> List[Incident]:
        """
        Check for duplicate billing entries
        
        Args:
            data: Dictionary containing 'billing' list
            
        Returns:
            List of Incident objects representing detected duplicate entries
        """
        incidents = []
        billing_records = data.get('billing', [])
        
        # Group billing records by key attributes to find duplicates
        billing_groups = {}
        for bill in billing_records:
            # Create a key that identifies duplicate records
            key = (bill.customer_id, bill.service_id, bill.billing_period_start, bill.billing_period_end, bill.amount)
            if key not in billing_groups:
                billing_groups[key] = []
            billing_groups[key].append(bill)
        
        # Check for groups with more than one record (duplicates)
        for key, records in billing_groups.items():
            if len(records) > 1:
                # Create incident for each duplicate (except the first one)
                for i, duplicate in enumerate(records[1:]):
                    incident = Incident(
                        id=str(uuid.uuid4()),
                        type="duplicate_entry",
                        severity="high",
                        status="detected",
                        description=f"Duplicate billing entry for service {duplicate.service_id}, customer {duplicate.customer_id}",
                        financial_impact=duplicate.amount,
                        currency=duplicate.currency,
                        detection_date=datetime.now(),
                        related_entities={
                            "billing_id": duplicate.id,
                            "duplicate_of": records[0].id
                        },
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    incidents.append(incident)
        
        return incidents

# Initialize detection rules
MISSING_CHARGE_RULE = MissingChargeRule()
INCORRECT_RATE_RULE = IncorrectRateRule()
USAGE_MISMATCH_RULE = UsageMismatchRule()
DUPLICATE_ENTRY_RULE = DuplicateEntryRule()

# List of all rules for easy execution
ALL_RULES = [
    MISSING_CHARGE_RULE,
    INCORRECT_RATE_RULE,
    USAGE_MISMATCH_RULE,
    DUPLICATE_ENTRY_RULE
]

def run_all_rules(data: Dict[str, Any]) -> List[Incident]:
    """
    Run all detection rules on the provided data
    
    Args:
        data: Dictionary containing all relevant data (billing, provisioning, etc.)
        
    Returns:
        List of all detected incidents
    """
    all_incidents = []
    for rule in ALL_RULES:
        incidents = rule.check(data)
        all_incidents.extend(incidents)
    
    return all_incidents