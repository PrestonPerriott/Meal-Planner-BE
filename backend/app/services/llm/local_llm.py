import aiohttp
from typing import Optional
from .base import BaseLLMService
from ...core.config import settings

class OllamsService(BaseLLMService):
    def __init__(self):
        self.base_url = settings.OLLAMA_HOST
        self.model = settings.OLLAMA_MODEL
        
    async def generate_response(self, prompt: str, max_tokens: Optional[int] = 1024, temperature: Optional[float] = 0.7) -> str:
        """Generate a response using Ollama API"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "token_count": max_tokens,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "stream": False
                    }
                ) as response:
                    if response.status != 200:
                        error_message = await response.text()
                        print(f"Error generating response from Ollama API: {error_message}")
                        return 'Sorry, I encountered an error generating a meal suggestion. Please try again later.'
                    data = await response.json()
                    return data['response']
            except Exception as e:
                print(f"Error generating response from Ollama API: {e}")
                return 'Sorry, I encountered an error generating a meal suggestion. Please try again later.'
    
    
    