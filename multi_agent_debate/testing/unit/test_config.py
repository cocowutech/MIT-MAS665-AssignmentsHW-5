"""Unit tests for configuration components."""

import unittest
import os
from unittest.mock import patch
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.utils.config import Config, config

class TestConfig(unittest.TestCase):
    """Test the configuration functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Save original environment
        self.original_env = os.environ.copy()
    
    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_env)
    
    def test_default_config(self):
        """Test default configuration values."""
        with patch.dict(os.environ, {}, clear=True):
            cfg = Config()
            
            self.assertEqual(cfg.glm_model, "glm-4.6")
            self.assertEqual(cfg.glm_base_url, "https://api.z.ai/api/coding/paas/v4/")
            self.assertEqual(cfg.default_temperature, 0.7)
            self.assertEqual(cfg.low_temperature, 0.2)
            self.assertEqual(cfg.high_temperature, 0.9)
            self.assertEqual(cfg.default_rounds, 2)
            self.assertEqual(cfg.default_agents, 4)
            self.assertEqual(cfg.max_tokens, 1000)
            self.assertEqual(cfg.log_level, "INFO")
            self.assertEqual(cfg.log_file, "experiments/logs/debate.log")
    
    def test_config_from_env(self):
        """Test configuration from environment variables."""
        with patch.dict(os.environ, {
            "GLM_MODEL": "custom-model",
            "DEFAULT_TEMPERATURE": "0.5",
            "DEFAULT_ROUNDS": "3",
            "MAX_TOKENS": "2000"
        }, clear=True):
            cfg = Config()
            
            self.assertEqual(cfg.glm_model, "custom-model")
            self.assertEqual(cfg.default_temperature, 0.5)
            self.assertEqual(cfg.default_rounds, 3)
            self.assertEqual(cfg.max_tokens, 2000)
    
    def test_validate_success(self):
        """Test successful validation."""
        with patch.dict(os.environ, {
            "ZAI_API_KEY": "valid-api-key"
        }, clear=True):
            cfg = Config()
            self.assertTrue(cfg.validate())
    
    def test_validate_failure(self):
        """Test validation failure."""
        with patch.dict(os.environ, {
            "ZAI_API_KEY": ""  # Empty API key
        }, clear=True):
            cfg = Config()
            with self.assertRaises(ValueError):
                cfg.validate()
    
    def test_get_llm_config(self):
        """Test getting LLM configuration."""
        with patch.dict(os.environ, {
            "ZAI_API_KEY": "test-api-key"
        }, clear=True):
            cfg = Config()
            
            # Test with default temperature
            llm_config = cfg.get_llm_config()
            self.assertEqual(llm_config["model"], "glm-4.6")
            self.assertEqual(llm_config["openai_api_key"], "test-api-key")
            self.assertEqual(llm_config["openai_api_base"], "https://api.z.ai/api/coding/paas/v4/")
            self.assertEqual(llm_config["temperature"], 0.7)
            self.assertEqual(llm_config["max_tokens"], 1000)
            
            # Test with custom temperature
            llm_config = cfg.get_llm_config(temperature=0.3)
            self.assertEqual(llm_config["temperature"], 0.3)

if __name__ == "__main__":
    unittest.main()
