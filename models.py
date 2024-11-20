from dataclasses import dataclass
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.chat_models.base import BaseChatModel


@dataclass
class ModelConfig:
    provider: str
    model_name: str
    api_key: str
    api_base: Optional[str] = None
    
    def create_chat_model(self) -> BaseChatModel:
        """Create a chat model instance based on the provider configuration."""
        if self.provider == "openai":
            return ChatOpenAI(
                model_name=self.model_name,
                openai_api_key=self.api_key
            )
        elif self.provider == "openrouter":
            return ChatOpenAI(
                model_name=self.model_name,
                openai_api_key=self.api_key,
                openai_api_base=self.api_base,
                default_headers={
                    "HTTP-Referer": "https://github.com/cascade", # Required for OpenRouter
                    "X-Title": "Paper Analyzer"  # Optional, helps OpenRouter track usage
                }
            )
        elif self.provider == "gemini":
            return ChatOpenAI(
                model_name=self.model_name,
                openai_api_key=self.api_key,
                openai_api_base=self.api_base
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")


def create_model_config(provider: str, model_name: str, api_key: str, api_base: Optional[str] = None) -> ModelConfig:
    """Factory function to create a ModelConfig instance."""
    return ModelConfig(
        provider=provider,
        model_name=model_name,
        api_key=api_key,
        api_base=api_base
    )
