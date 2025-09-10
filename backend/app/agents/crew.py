"""
CrewAI Agent Definitions for Revenue Leakage Detection
"""
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.settings import settings

class RLDAgents:
    """Collection of CrewAI agents for revenue leakage detection"""
    
    def __init__(self):
        """Initialize all agents"""
        # Initialize LLM for CrewAI agents
        if settings.GEMINI_API_KEY:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                google_api_key=settings.GEMINI_API_KEY
            )
        else:
            self.llm = None
            
        self.triage_agent = self._create_triage_agent()
        self.evidence_collector_agent = self._create_evidence_collector_agent()
        self.rca_agent = self._create_rca_agent()
        self.ticket_creator_agent = self._create_ticket_creator_agent()
    
    def _create_triage_agent(self) -> Agent:
        """Create the Triage Agent"""
        return Agent(
            role='Incident Triage Specialist',
            goal='Classify and prioritize revenue leakage incidents based on severity and financial impact',
            backstory="""You are an expert at analyzing revenue leakage incidents. 
            Your role is to quickly assess newly detected incidents, categorize them correctly, 
            and assign appropriate severity levels. You understand the business impact of 
            different types of revenue leakages and can prioritize them effectively.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _create_evidence_collector_agent(self) -> Agent:
        """Create the Evidence Collector Agent"""
        return Agent(
            role='Evidence Gathering Specialist',
            goal='Collect and organize all relevant evidence for revenue leakage incidents',
            backstory="""You are a meticulous investigator who specializes in gathering 
            evidence for revenue leakage cases. You know how to retrieve billing records, 
            provisioning data, usage logs, and contract information. You ensure all 
            relevant data is collected and organized for analysis.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _create_rca_agent(self) -> Agent:
        """Create the Root Cause Analysis Agent"""
        return Agent(
            role='Root Cause Analysis Expert',
            goal='Perform in-depth analysis to determine the underlying causes of revenue leakages',
            backstory="""You are a seasoned analyst with deep expertise in identifying 
            the root causes of revenue leakages. You use both data analysis and your 
            knowledge base to formulate hypotheses about why leakages occur. You're 
            skilled at connecting dots between different data sources to uncover 
            systemic issues.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _create_ticket_creator_agent(self) -> Agent:
        """Create the Ticket Creator Agent"""
        return Agent(
            role='Incident Resolution Coordinator',
            goal='Create and route investigation tickets to appropriate teams for resolution',
            backstory="""You are an experienced coordinator who knows how to create 
            effective incident tickets for different types of revenue leakages. You 
            understand which teams should handle different kinds of issues and how 
            to communicate the necessary information for resolution. You ensure 
            tickets contain all required information for efficient investigation.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

# Global instance
rld_agents = RLDAgents()