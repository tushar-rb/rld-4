"""
Gemini client for LLM operations
"""
import google.generativeai as genai
from app.config.settings import settings

class GeminiClient:
    def __init__(self):
        """Initialize Gemini client"""
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def generate_text(self, prompt: str) -> str:
        """Generate text using Gemini"""
        if not self.model:
            return "Gemini API key not configured. This is a placeholder response."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating text with Gemini: {e}")
            return "Error generating response"
    
    def generate_json(self, prompt: str) -> dict:
        """Generate JSON response using Gemini"""
        if not self.model:
            return {"status": "error", "message": "Gemini API key not configured"}
        
        try:
            response = self.model.generate_content(prompt)
            # In a real implementation, you would parse the response as JSON
            # For now, returning a mock structure
            return {
                "status": "success",
                "content": response.text,
                "raw_response": response
            }
        except Exception as e:
            print(f"Error generating JSON with Gemini: {e}")
            return {"status": "error", "message": str(e)}

# Global instance
gemini_client = GeminiClient()