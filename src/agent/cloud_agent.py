"""
Cloud Agent Interface

Defines the interface for cloud-based agents that can execute tasks.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class CloudAgent(ABC):
    """Abstract base class for cloud agents."""
    
    def __init__(self, agent_id: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a cloud agent.
        
        Args:
            agent_id: Unique identifier for the agent
            config: Optional configuration dictionary
        """
        self.agent_id = agent_id
        self.config = config or {}
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task on the cloud agent.
        
        Args:
            task: Task specification dictionary
            
        Returns:
            Result dictionary with execution results
        """
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """
        Check if the agent is healthy and ready to receive tasks.
        
        Returns:
            True if agent is healthy, False otherwise
        """
        pass
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get the capabilities of this agent.
        
        Returns:
            Dictionary describing agent capabilities
        """
        return {
            "agent_id": self.agent_id,
            "config": self.config
        }
