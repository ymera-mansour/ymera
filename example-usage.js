/**
 * Example usage of Cloud Agent Delegation
 * 
 * This demonstrates how to delegate tasks to cloud agents
 */

const CloudAgentDelegate = require('./src/cloud-agent');

async function main() {
  // Initialize cloud agent delegate
  const cloudAgent = new CloudAgentDelegate();

  console.log('Cloud Agent Capabilities:', cloudAgent.getCapabilities());
  console.log('');

  // Example 1: Delegate a computation task
  console.log('Example 1: Delegating a computation task...');
  const computeTask = {
    type: 'compute',
    payload: {
      operation: 'matrix-multiplication',
      data: {
        matrixA: [[1, 2], [3, 4]],
        matrixB: [[5, 6], [7, 8]]
      }
    },
    options: {
      priority: 'high'
    }
  };

  try {
    const result1 = await cloudAgent.delegateTask(computeTask);
    console.log('Delegation Result:', result1);
    console.log('');

    // Check status
    console.log('Checking task status...');
    const status = await cloudAgent.getTaskStatus(result1.taskId);
    console.log('Status:', status);
    console.log('');
  } catch (error) {
    console.error('Error delegating compute task:', error.message);
  }

  // Example 2: Delegate a data processing task
  console.log('Example 2: Delegating a data processing task...');
  const dataTask = {
    type: 'data-processing',
    payload: {
      operation: 'aggregate',
      dataSource: 'database',
      filters: {
        dateRange: '2023-01-01 to 2023-12-31'
      }
    },
    options: {
      async: true
    }
  };

  try {
    const result2 = await cloudAgent.delegateTask(dataTask);
    console.log('Delegation Result:', result2);
    console.log('');
  } catch (error) {
    console.error('Error delegating data task:', error.message);
  }

  // Example 3: Delegate a long-running task
  console.log('Example 3: Delegating a long-running task...');
  const longTask = {
    type: 'batch-processing',
    payload: {
      operation: 'generate-report',
      items: 1000000,
      outputFormat: 'pdf'
    },
    options: {
      priority: 'normal',
      notify: true
    }
  };

  try {
    const result3 = await cloudAgent.delegateTask(longTask);
    console.log('Delegation Result:', result3);
    console.log('Task will complete by:', result3.estimatedCompletion);
  } catch (error) {
    console.error('Error delegating long task:', error.message);
  }
}

// Run the examples
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { main };
