# Ymera - Cloud Agent Delegation Framework

A lightweight framework for delegating tasks to cloud agents.

## Overview

This project demonstrates a simple pattern for delegating computational tasks to cloud-based agents, enabling distributed processing and scalability.

## Quick Start

```javascript
const { CloudAgentDelegator, RemoteCloudAgent } = require('./src');

// Create delegator
const delegator = new CloudAgentDelegator();

// Register a remote cloud agent
const cloudAgent = new RemoteCloudAgent(
    'my-cloud-agent',
    'https://api.example.com/process',
    ['process_data', 'analyze']
);
delegator.registerAgent(cloudAgent);

// Delegate task to cloud
const result = await delegator.delegate({
    task: 'process_data',
    data: { items: [1, 2, 3] }
});
```

## Architecture

The framework consists of:
- **Delegator**: Coordinates task submission to cloud agents with capability-based selection
- **Agent Interface**: Defines the contract for cloud agent implementations with status tracking
- **RemoteCloudAgent**: HTTP-based agent for delegating tasks to remote cloud endpoints
- **CloudAgent**: Base class for local agent implementations

## Use Cases

- Offloading compute-intensive operations to remote cloud services
- Distributed data processing across multiple cloud agents
- Scalable background job processing with HTTP endpoints
- Cloud-native microservices delegation via REST APIs
- Integration with AWS Lambda, Azure Functions, or Google Cloud Functions

## Examples

### Local Agent Delegation
```javascript
const { CloudAgentDelegator, CloudAgent } = require('./src');

const delegator = new CloudAgentDelegator();
const localAgent = new CloudAgent('local-processor', ['analyze']);
delegator.registerAgent(localAgent);

const result = await delegator.delegate({
    task: 'analyze',
    data: { values: [1, 2, 3] }
});
```

### Remote Cloud Agent Delegation
```javascript
const { CloudAgentDelegator, RemoteCloudAgent } = require('./src');

const delegator = new CloudAgentDelegator();
const remoteAgent = new RemoteCloudAgent(
    'cloud-processor',
    'https://api.example.com/process',
    ['analyze', 'transform']
);
delegator.registerAgent(remoteAgent);

const result = await delegator.delegate({
    task: 'analyze',
    data: { dataset: 'sales-2024' }
});
```

Run `node example.js` for local delegation or `node example-cloud.js` for remote cloud delegation examples.

## License

MIT
