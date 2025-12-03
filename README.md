# Ymera - Cloud Agent Delegation Framework

This project demonstrates a cloud agent delegation pattern for distributed task processing.

## Overview

The Ymera framework provides a simple interface for delegating tasks to cloud-based agents, enabling scalable and distributed processing.

## Features

- Cloud agent registration and discovery
- Task delegation with round-robin load balancing
- Thread-safe concurrent task execution
- Asynchronous task processing
- Configuration management
- Comprehensive logging support

## Installation

Install in development mode:

```bash
pip install -e .
```

## Usage

Run the example:

```bash
python -m examples.basic_delegation
```

## Quick Start

```python
import asyncio
from src.agent.cloud_agent import CloudAgent
from src.delegator.task_delegator import TaskDelegator

# Create a custom agent
class MyAgent(CloudAgent):
    async def execute(self, task):
        # Process task
        return {'status': 'success', 'result': 'processed'}
    
    def health_check(self):
        return True

# Use the delegator
async def main():
    delegator = TaskDelegator()
    agent = MyAgent("my-agent-1")
    delegator.register_agent(agent)
    
    result = await delegator.delegate({'action': 'process'})
    print(result)

asyncio.run(main())
```

## Architecture

- `src/agent/` - Cloud agent interface and implementations
- `src/delegator/` - Task delegation logic with load balancing
- `src/config/` - Configuration management
- `examples/` - Usage examples
