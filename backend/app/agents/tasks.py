"""
CrewAI Task Definitions for Revenue Leakage Detection
"""
from crewai import Task
from app.agents.crew import rld_agents
from datetime import datetime

class RLDTasks:
    """Collection of CrewAI tasks for revenue leakage detection"""
    
    def __init__(self):
        """Initialize all tasks"""
        pass
    
    def triage_incident_task(self, incident_data: dict) -> Task:
        """Create a task for triaging an incident"""
        return Task(
            description=f"""Analyze the following revenue leakage incident and classify it:
            
            Incident Details:
            Type: {incident_data.get('type', 'Unknown')}
            Severity: {incident_data.get('severity', 'Unknown')}
            Description: {incident_data.get('description', 'No description provided')}
            Financial Impact: {incident_data.get('financial_impact', 0)} {incident_data.get('currency', 'USD')}
            
            Please:
            1. Confirm the incident classification
            2. Verify the severity level
            3. Suggest initial investigation priorities
            4. Identify which evidence sources would be most relevant
            
            Provide your analysis in a structured format.""",
            agent=rld_agents.triage_agent,
            expected_output="Incident classification, verified severity, investigation priorities, and relevant evidence sources"
        )
    
    def collect_evidence_task(self, incident_data: dict, evidence_sources: list) -> Task:
        """Create a task for collecting evidence"""
        sources_str = ", ".join(evidence_sources) if evidence_sources else "Not specified"
        
        return Task(
            description=f"""Collect evidence for the following revenue leakage incident:
            
            Incident Details:
            ID: {incident_data.get('id', 'Unknown')}
            Type: {incident_data.get('type', 'Unknown')}
            Description: {incident_data.get('description', 'No description provided')}
            
            Relevant Evidence Sources:
            {sources_str}
            
            Please:
            1. Retrieve the specified evidence types
            2. Organize the evidence in a structured format
            3. Highlight any anomalies or inconsistencies found
            4. Prepare the evidence for root cause analysis
            
            Include all relevant data points that would help with analysis.""",
            agent=rld_agents.evidence_collector_agent,
            expected_output="Structured collection of relevant evidence with anomalies highlighted"
        )
    
    def root_cause_analysis_task(self, incident_data: dict, evidence: dict) -> Task:
        """Create a task for root cause analysis"""
        return Task(
            description=f"""Perform root cause analysis for the following revenue leakage incident:
            
            Incident Details:
            ID: {incident_data.get('id', 'Unknown')}
            Type: {incident_data.get('type', 'Unknown')}
            Description: {incident_data.get('description', 'No description provided')}
            
            Collected Evidence:
            {str(evidence)[:1000]}...  # Truncate for readability
            
            Please:
            1. Analyze the evidence to identify the root cause
            2. Formulate 2-3 hypotheses about why this leakage occurred
            3. For each hypothesis, explain the supporting evidence
            4. Identify any systemic issues that might cause similar problems
            5. Suggest preventive measures to avoid recurrence
            
            Return your analysis in JSON format with clear hypotheses and recommendations.""",
            agent=rld_agents.rca_agent,
            expected_output="JSON-formatted root cause analysis with hypotheses and preventive measures"
        )
    
    def create_ticket_task(self, incident_data: dict, rca_results: dict) -> Task:
        """Create a task for creating investigation tickets"""
        return Task(
            description=f"""Create an investigation ticket for the following revenue leakage incident:
            
            Incident Details:
            ID: {incident_data.get('id', 'Unknown')}
            Type: {incident_data.get('type', 'Unknown')}
            Severity: {incident_data.get('severity', 'Unknown')}
            Description: {incident_data.get('description', 'No description provided')}
            Financial Impact: {incident_data.get('financial_impact', 0)} {incident_data.get('currency', 'USD')}
            
            Root Cause Analysis Results:
            {str(rca_results)[:1000]}...  # Truncate for readability
            
            Please:
            1. Create a detailed ticket for investigation
            2. Specify the assigned team or individual
            3. Include all relevant information for resolution
            4. Set appropriate priority based on severity and impact
            5. Suggest next steps for resolution
            6. Include links to related records and evidence
            
            Return the ticket details in a structured format.""",
            agent=rld_agents.ticket_creator_agent,
            expected_output="Detailed investigation ticket with assignment and resolution steps"
        )

# Global instance
rld_tasks = RLDTasks()