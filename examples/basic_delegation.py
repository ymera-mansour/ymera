"""
Basic Cloud Agent Delegation Example

Demonstrates how to use the cloud agent delegation framework.

To run this example:
1. Install the package: pip install -e .
2. Run: python -m examples.basic_delegation

For development, from the repository root:
python -m examples.basic_delegation
"""

import asyncio
import logging
from typing import Any, Dict

from src.agent.cloud_agent import CloudAgent
from src.delegator.task_delegator import TaskDelegator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class SimpleCloudAgent(CloudAgent):
    """A simple implementation of a cloud agent for demonstration."""
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task.
        
        Args:
            task: Task specification with 'action' and optional 'data'
            
        Returns:
            Result dictionary with execution results
        """
        action = task.get('action', 'unknown')
        data = task.get('data', {})
        
        # Simulate some processing
        await asyncio.sleep(0.5)
        
        result = {
            'status': 'success',
            'agent_id': self.agent_id,
            'action': action,
            'result': f"Processed {action} with data: {data}"
        }
        
        return result
    
    def health_check(self) -> bool:
        """Check if agent is healthy."""
        return True


async def main():
    """Main demonstration function."""
    print("=== Cloud Agent Delegation Demo ===\n")
    
    # Create delegator
    delegator = TaskDelegator()
    
    # Create and register agents
    agent1 = SimpleCloudAgent("cloud-agent-1", {"region": "us-east"})
    agent2 = SimpleCloudAgent("cloud-agent-2", {"region": "eu-west"})
    
    await delegator.register_agent(agent1)
    await delegator.register_agent(agent2)
    
    # List registered agents
    print("\nRegistered agents:")
    for agent_info in delegator.list_agents():
        print(f"  - {agent_info['agent_id']}: {agent_info['config']}")
    
    # Delegate tasks
    print("\n=== Delegating Tasks ===\n")
    
    task1 = {
        'action': 'process_data',
        'data': {'input': 'Hello from cloud agent delegation!'}
    }
    
    result1 = await delegator.delegate(task1, agent_id="cloud-agent-1")
    print(f"Task 1 Result: {result1}")
    
    task2 = {
        'action': 'analyze',
        'data': {'input': 'More data to process'}
    }
    
    result2 = await delegator.delegate(task2, agent_id="cloud-agent-2")
    print(f"Task 2 Result: {result2}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
