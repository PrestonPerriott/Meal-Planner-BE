import aiohttp
from typing import Optional
from .base import BaseLLMService
from ...core.config import settings

# TODO: Add a logger service to capture prompt and response metrics
class OllamsService(BaseLLMService):
    def __init__(self):
        self.base_url = settings.OLLAMA_HOST
        self.model = settings.OLLAMA_MODEL
        self.timeout = aiohttp.ClientTimeout(total=None)
        self.client_args = dict(
            timeout=self.timeout,
            headers={'Connection': 'keep-alive'}
        )
        
    # TODO: Need to fifure out how to best optimize the response time and resource usage
    async def generate_response(self, prompt: str, max_tokens: Optional[int] = 1024, temperature: Optional[float] = 0.7) -> str:
        """Generate a response using Ollama API"""
        async with aiohttp.ClientSession(**self.client_args) as session:
            try:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "token_count": max_tokens,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "stream": False,
                        "keep_alive": -1 # Hopefully keep model loaded in memory longer
                    }
                ) as response:
                    if response.status != 200:
                        error_message = await response.text()
                        print(f"Error generating response from Ollama API: {error_message}")
                        print(f"Response: {response}")
                        return 'Sorry, I encountered an error generating a meal suggestion. Please try again later.'
                    data = await response.json()
                    # data['eval_duration] - The time in nanoseconds it took to generate the response
                    # data['context'] - Encoding of convo, can be sent to next req for convo mem
                    # data['prompt_eval_count'] - Number of tokens processed in prompt
                    # data['eval_count'] - Number of tokens processed in response
                    print(f"Recipes: {data}")
                    return data['response']
            except Exception as e:
                print(f"Error generating response from Ollama API: {e}")
                return 'Sorry, I encountered an error generating a meal suggestion. Please try again later.'
    
    
    