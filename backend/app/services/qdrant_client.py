"""
Qdrant client integration for vector storage
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.config.settings import settings
import google.generativeai as genai

class QdrantService:
    def __init__(self):
        """Initialize Qdrant client"""
        # Handle Qdrant Cloud configuration
        if hasattr(settings, 'QDRANT_API_KEY') and settings.QDRANT_API_KEY:
            self.client = QdrantClient(
                url=f"https://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}" if getattr(settings, 'QDRANT_USE_HTTPS', False) else f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}",
                api_key=settings.QDRANT_API_KEY,
            )
        else:
            # Self-hosted Qdrant
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT
            )
        
        # Initialize Gemini for embeddings
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
    
    def create_collections(self):
        """Create required collections in Qdrant"""
        collections = [
            "incidents",
            "contract_clauses",
            "usage_templates",
            "kb_fixes"
        ]
        
        for collection_name in collections:
            try:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
                )
                print(f"Created collection: {collection_name}")
            except Exception as e:
                print(f"Collection {collection_name} may already exist: {e}")
    
    def generate_embedding(self, text: str) -> list:
        """Generate embedding for text using Gemini"""
        if not settings.GEMINI_API_KEY:
            # Return a dummy embedding for testing
            return [0.1] * 768
            
        # For actual implementation, we would use Gemini's embedding API
        # This is a simplified version for demonstration
        try:
            # Generate a mock embedding based on text length
            # In real implementation, use proper embedding API
            embedding = [len(text) / 1000.0] * 768
            return embedding[:768]  # Ensure correct size
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return [0.0] * 768
    
    def upsert_incident(self, incident_id: str, incident_data: dict):
        """Insert or update an incident in Qdrant"""
        # Generate embedding for incident description
        description = incident_data.get("description", "")
        embedding = self.generate_embedding(description)
        
        # Create point for Qdrant
        point = PointStruct(
            id=incident_id,
            vector=embedding,
            payload=incident_data
        )
        
        # Upsert to incidents collection
        self.client.upsert(
            collection_name="incidents",
            points=[point]
        )
        
        return incident_id

# Global instance
qdrant_service = QdrantService()