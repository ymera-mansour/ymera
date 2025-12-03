"""
Task Delegator

Handles delegation of tasks to cloud agents.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from ..agent.cloud_agent import CloudAgent

logger = logging.getLogger(__name__)


class TaskDelegator:
    """Delegates tasks to registered cloud agents."""
    
    def __init__(self):
        """Initialize the task delegator."""
        self.agents: List[CloudAgent] = []
        self._current_agent_index: int = 0
        self._index_lock: asyncio.Lock = asyncio.Lock()
    
    async def register_agent(self, agent: CloudAgent) -> None:
        """
        Register a cloud agent with the delegator.
        
        Args:
            agent: CloudAgent instance to register
        """
        # Check health before acquiring lock to avoid blocking
        if not agent.health_check():
            logger.warning(f"Agent {agent.agent_id} failed health check")
            return
        
        async with self._index_lock:
            self.agents.append(agent)
        logger.info(f"Agent {agent.agent_id} registered successfully")
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister a cloud agent.
        
        Args:
            agent_id: ID of the agent to unregister
            
        Returns:
            True if agent was found and removed, False otherwise
        """
        async with self._index_lock:
            for i, agent in enumerate(self.agents):
                if agent.agent_id == agent_id:
                    self.agents.pop(i)
                    # Reset round-robin index if it's out of bounds or no agents left
                    if not self.agents or self._current_agent_index >= len(self.agents):
                        self._current_agent_index = 0
                    logger.info(f"Agent {agent_id} unregistered")
                    return True
        return False
    
    async def delegate(self, task: Dict[str, Any], agent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Delegate a task to a cloud agent.
        
        Args:
            task: Task specification dictionary
            agent_id: Optional specific agent ID to use
            
        Returns:
            Result dictionary from task execution
            
        Raises:
            ValueError: If no agents are available or specified agent not found
        """
        # Select agent with thread-safe access
        async with self._index_lock:
            if not self.agents:
                raise ValueError("No agents registered")
            
            if agent_id:
                agent = next((a for a in self.agents if a.agent_id == agent_id), None)
                if not agent:
                    raise ValueError(f"Agent {agent_id} not found")
            else:
                # Round-robin selection
                agent = self.agents[self._current_agent_index]
                self._current_agent_index = (self._current_agent_index + 1) % len(self.agents)
        
        # Execute task outside the lock to allow concurrent execution
        logger.info(f"Delegating task to agent {agent.agent_id}")
        result = await agent.execute(task)
        return result
    
    async def list_agents(self) -> List[Dict[str, Any]]:
        """
        List all registered agents and their capabilities.
        
        Returns:
            List of agent capability dictionaries
        """
        async with self._index_lock:
            return [agent.get_capabilities() for agent in self.agents]
