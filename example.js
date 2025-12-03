const { CloudAgentDelegator } = require('./src/delegator');
const { CloudAgent } = require('./src/agent');

/**
 * Example demonstrating cloud agent delegation
 */
async function main() {
    console.log('=== Cloud Agent Delegation Example ===\n');

    // Create delegator
    const delegator = new CloudAgentDelegator({
        maxRetries: 3,
        timeout: 5000
    });

    // Example 1: Delegate without agents (simulated)
    console.log('1. Simulated cloud execution:');
    const result1 = await delegator.delegate({
        task: 'analyze_data',
        data: { dataset: 'sample.csv', rows: 1000 }
    });
    console.log('   Result:', result1);

    // Example 2: Register and use a custom agent
    console.log('\n2. Using registered cloud agent:');
    const customAgent = new CloudAgent('data-processor', ['analyze_data', 'transform_data']);
    delegator.registerAgent(customAgent);
    
    const result2 = await delegator.delegate({
        task: 'analyze_data',
        data: { metrics: ['avg', 'sum', 'count'] }
    });
    console.log('   Result:', result2);
    console.log('   Agent status:', customAgent.status);

    console.log('\n=== Delegation Complete ===');
}

// Run example
main().catch(console.error);
