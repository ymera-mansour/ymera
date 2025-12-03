"""
Agent Configuration

Configuration management for cloud agents.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class AgentConfig:
    """Manages configuration for cloud agents."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        if config_path:
            self.load()
    
    def load(self) -> None:
        """Load configuration from file."""
        if not self.config_path:
            return
        
        path = Path(self.config_path)
        if path.exists():
            with open(path, 'r') as f:
                self.config = json.load(f)
    
    def save(self) -> None:
        """Save configuration to file."""
        if not self.config_path:
            raise ValueError("No config path specified")
        
        path = Path(self.config_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
    
    def get_agent_config(self, agent_id: str) -> Dict[str, Any]:
        """
        Get configuration for a specific agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Agent-specific configuration dictionary
        """
        agents = self.config.get('agents', {})
        return agents.get(agent_id, {})
