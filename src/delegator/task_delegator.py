"""
Task Delegator

Handles delegation of tasks to cloud agents.
"""

import asyncio
from typing import Any, Dict, List, Optional
from ..agent.cloud_agent import CloudAgent


class TaskDelegator:
    """Delegates tasks to registered cloud agents."""
    
    def __init__(self):
        """Initialize the task delegator."""
        self.agents: List[CloudAgent] = []
        self.task_queue: asyncio.Queue = asyncio.Queue()
    
    def register_agent(self, agent: CloudAgent) -> None:
        """
        Register a cloud agent with the delegator.
        
        Args:
            agent: CloudAgent instance to register
        """
        if agent.health_check():
            self.agents.append(agent)
            print(f"Agent {agent.agent_id} registered successfully")
        else:
            print(f"Agent {agent.agent_id} failed health check")
    
    def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister a cloud agent.
        
        Args:
            agent_id: ID of the agent to unregister
            
        Returns:
            True if agent was found and removed, False otherwise
        """
        for i, agent in enumerate(self.agents):
            if agent.agent_id == agent_id:
                self.agents.pop(i)
                print(f"Agent {agent_id} unregistered")
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
        if not self.agents:
            raise ValueError("No agents registered")
        
        # Select agent
        if agent_id:
            agent = next((a for a in self.agents if a.agent_id == agent_id), None)
            if not agent:
                raise ValueError(f"Agent {agent_id} not found")
        else:
            # Simple round-robin selection
            agent = self.agents[0]
        
        # Execute task
        print(f"Delegating task to agent {agent.agent_id}")
        result = await agent.execute(task)
        return result
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """
        List all registered agents and their capabilities.
        
        Returns:
            List of agent capability dictionaries
        """
        return [agent.get_capabilities() for agent in self.agents]
