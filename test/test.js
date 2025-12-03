const { CloudAgentDelegator } = require('../src/delegator');
const { CloudAgent } = require('../src/agent');

/**
 * Simple test suite for cloud agent delegation
 */
async function runTests() {
    console.log('Running Cloud Agent Delegation Tests...\n');

    // Test 1: Basic delegation without registered agents
    console.log('Test 1: Simulated delegation');
    const delegator = new CloudAgentDelegator();
    const result1 = await delegator.delegate({
        task: 'process_data',
        data: { value: 42 }
    });
    console.log('✓ Result:', result1);
    console.assert(result1.status === 'completed', 'Task should complete');

    // Test 2: Delegation with registered agent
    console.log('\nTest 2: Delegation with registered agent');
    const agent = new CloudAgent('test-agent', ['process_data']);
    delegator.registerAgent(agent);
    const result2 = await delegator.delegate({
        task: 'process_data',
        data: { items: [1, 2, 3] }
    });
    console.log('✓ Result:', result2);
    console.assert(result2.status === 'completed', 'Task should complete');
    console.assert(result2.agent === 'test-agent', 'Should use registered agent');

    // Test 3: Agent capability check
    console.log('\nTest 3: Agent capability check');
    const canHandle = agent.canHandle({ task: 'process_data' });
    console.log('✓ Can handle:', canHandle);
    console.assert(canHandle === true, 'Agent should handle process_data');

    console.log('\n✅ All tests passed!');
}

// Run tests
runTests().catch(error => {
    console.error('❌ Test failed:', error);
    process.exit(1);
});
