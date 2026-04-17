"""
Base Agent Class
Provides common functionality for all agents in the ConViCure fundraising system
"""

import os
import yaml
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from anthropic import Anthropic


class BaseAgent:
    """Base class for all fundraising system agents"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize base agent with configuration
        
        Args:
            config_path: Path to system configuration file
        """
        self.config = self._load_config(config_path)
        self.knowledge = self._load_knowledge()
        self.logger = self._setup_logging()
        
        # Initialize Anthropic client
        api_key = os.getenv("ANTHROPIC_API_KEY") or self.config.get("anthropic", {}).get("api_key")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment or config")
        
        self.client = Anthropic(api_key=api_key)
        self.model = self.config.get("anthropic", {}).get("model", "claude-sonnet-4-20250514")
        
    def _load_config(self, path: str) -> Dict:
        """Load system configuration from YAML"""
        try:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            self.logger.warning(f"Config file not found at {path}, using defaults")
            return {}
            
    def _load_knowledge(self) -> Dict:
        """Load ConViCure knowledge base"""
        kb_path = self.config.get("paths", {}).get("knowledge_base", "config/convicure_knowledge.yaml")
        try:
            with open(kb_path, 'r') as f:
                knowledge = yaml.safe_load(f)
            return knowledge
        except FileNotFoundError:
            self.logger.warning(f"Knowledge base not found at {kb_path}")
            return {}
            
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for this agent"""
        log_level = self.config.get("logging", {}).get("level", "INFO")
        log_file = self.config.get("logging", {}).get("file", "data/analytics/system.log")
        
        # Create logger
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(getattr(logging, log_level))
        
        # Create handlers
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
        
    def call_claude(self, prompt: str, system_prompt: Optional[str] = None, 
                   max_tokens: int = 4000) -> str:
        """
        Call Claude API with given prompt
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens in response
            
        Returns:
            Claude's response text
        """
        try:
            messages = [{"role": "user", "content": prompt}]
            
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": messages
            }
            
            if system_prompt:
                kwargs["system"] = system_prompt
                
            response = self.client.messages.create(**kwargs)
            
            # Extract text from response
            return response.content[0].text
            
        except Exception as e:
            self.logger.error(f"Claude API error: {e}")
            raise
            
    def save_json(self, data: Any, filepath: str):
        """Save data to JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
            
    def load_json(self, filepath: str) -> Any:
        """Load data from JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
            
    def get_timestamp(self) -> str:
        """Get current timestamp string"""
        return datetime.now().isoformat()
        
    def log_activity(self, activity_type: str, details: Dict):
        """Log agent activity to analytics"""
        activity = {
            "timestamp": self.get_timestamp(),
            "agent": self.__class__.__name__,
            "type": activity_type,
            "details": details
        }
        
        # Append to activity log
        log_path = self.config.get("paths", {}).get("analytics_dir", "data/analytics/") + "activity.jsonl"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        with open(log_path, 'a') as f:
            f.write(json.dumps(activity, default=str) + '\n')
