"""Configuration management for the multi-agent debate system."""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the debate system."""
    
    def __init__(self):
        # API Configuration
        self.zai_api_key = os.getenv("ZAI_API_KEY", "")
        self.glm_model = os.getenv("GLM_MODEL", "glm-4.6")
        self.glm_base_url = os.getenv("GLM_BASE_URL", "https://api.z.ai/api/coding/paas/v4/")
        
        # Experiment Configuration
        self.default_temperature = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
        self.low_temperature = float(os.getenv("LOW_TEMPERATURE", "0.2"))
        self.high_temperature = float(os.getenv("HIGH_TEMPERATURE", "0.9"))
        
        # Debate Configuration
        self.default_rounds = int(os.getenv("DEFAULT_ROUNDS", "2"))
        self.default_agents = int(os.getenv("DEFAULT_AGENTS", "4"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
        
        # Logging Configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "experiments/logs/debate.log")
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        if not self.zai_api_key or self.zai_api_key == "your-api-key-here":
            raise ValueError("ZAI_API_KEY must be set in .env file")
        return True
    
    def get_llm_config(self, temperature: float = None) -> Dict[str, Any]:
        """Get LLM configuration dictionary."""
        temp = temperature or self.default_temperature
        return {
            "model": self.glm_model,
            "openai_api_key": self.zai_api_key,
            "openai_api_base": self.glm_base_url,
            "temperature": temp,
            "max_tokens": self.max_tokens
        }

# Global configuration instance
config = Config()
