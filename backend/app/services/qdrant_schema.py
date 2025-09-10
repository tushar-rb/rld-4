"""
Qdrant schema implementation and examples
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, CollectionStatus
from app.config.settings import settings
from app.models.data_models import Incident
from typing import List, Dict, Any
import json
import uuid

class QdrantSchema:
    """Qdrant schema definition and management"""
    
    def __init__(self):
        """Initialize Qdrant client"""
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
    
    def create_collections(self):
        """Create all required collections in Qdrant"""
        collections_config = {
            "incidents": {
                "size": 768,
                "distance": Distance.COSINE
            },
            "contract_clauses": {
                "size": 768,
                "distance": Distance.COSINE
            },
            "usage_templates": {
                "size": 768,
                "distance": Distance.COSINE
            },
            "kb_fixes": {
                "size": 768,
                "distance": Distance.COSINE
            }
        }
        
        for collection_name, config in collections_config.items():
            try:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=config["size"],
                        distance=config["distance"]
                    )
                )
                print(f"Created collection: {collection_name}")
            except Exception as e:
                print(f"Collection {collection_name} may already exist: {e}")
    
    def get_collection_info(self, collection_name: str):
        """Get information about a collection"""
        try:
            info = self.client.get_collection(collection_name=collection_name)
            return info
        except Exception as e:
            print(f"Error getting collection info for {collection_name}: {e}")
            return None

def generate_mock_embedding(text: str, size: int = 768) -> List[float]:
    """
    Generate a mock embedding based on text for demonstration purposes.
    In a real implementation, this would use Gemini's embedding API.
    """
    # Simple hash-based approach for deterministic mock embeddings
    hash_value = hash(text) % 1000000
    # Normalize to [0, 1] range
    normalized = hash_value / 1000000.0
    # Create embedding with consistent values
    return [normalized] * size

def upsert_incident_example():
    """
    Example of how to upsert an incident into Qdrant
    """
    # Initialize Qdrant client
    client = QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT
    )
    
    # Create a sample incident
    sample_incident = Incident(
        id=str(uuid.uuid4()),
        type="missing_charge",
        severity="high",
        status="detected",
        description="Service PROD-001 provisioned for customer CUST-123 but not billed for period 2023-06-01 to 2023-06-30",
        financial_impact=299.99,
        currency="USD",
        detection_date="2023-07-01T10:00:00",
        related_entities={
            "provisioning_id": "PROV-789",
            "customer_id": "CUST-123",
            "service_id": "PROD-001"
        },
        evidence=["PROV-789", "BILL-456-NOT-FOUND"],
        created_at="2023-07-01T10:00:00",
        updated_at="2023-07-01T10:00:00"
    )
    
    # Generate embedding for the incident description
    embedding = generate_mock_embedding(sample_incident.description)
    
    # Create point for Qdrant
    point = PointStruct(
        id=sample_incident.id,
        vector=embedding,
        payload=sample_incident.dict()  # Convert Pydantic model to dict
    )
    
    # Upsert to incidents collection
    try:
        client.upsert(
            collection_name="incidents",
            points=[point]
        )
        print(f"Successfully upserted incident {sample_incident.id} to Qdrant")
        return sample_incident.id
    except Exception as e:
        print(f"Error upserting incident: {e}")
        return None

def search_similar_incidents(incident_description: str, limit: int = 5):
    """
    Search for similar incidents using semantic similarity
    """
    client = QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT
    )
    
    # Generate embedding for the query
    query_vector = generate_mock_embedding(incident_description)
    
    # Search for similar incidents
    try:
        search_result = client.search(
            collection_name="incidents",
            query_vector=query_vector,
            limit=limit
        )
        return search_result
    except Exception as e:
        print(f"Error searching for similar incidents: {e}")
        return []

# Example usage
if __name__ == "__main__":
    # Initialize schema
    schema = QdrantSchema()
    
    # Create collections
    schema.create_collections()
    
    # Show collection info
    info = schema.get_collection_info("incidents")
    if info:
        print(f"Collection 'incidents' status: {info.status}")
    
    # Upsert a sample incident
    incident_id = upsert_incident_example()
    
    # Search for similar incidents
    if incident_id:
        similar = search_similar_incidents("Missing charge for provisioned service")
        print(f"Found {len(similar)} similar incidents")