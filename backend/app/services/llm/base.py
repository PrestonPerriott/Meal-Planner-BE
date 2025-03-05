from abc import ABC, abstractmethod
from typing import Optional

# Abstract base class for LLM services
class BaseLLMService(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, max_tokens: Optional[int] = None, temperature: Optional[float] = None) -> str:
        """Generate a response from the LLM"""
        pass    
    