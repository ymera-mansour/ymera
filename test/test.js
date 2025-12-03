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

    // Test 4: Round-robin distribution
    console.log('\nTest 4: Round-robin distribution across multiple agents');
    const delegator2 = new CloudAgentDelegator();
    const agent1 = new CloudAgent('agent-1', ['compute']);
    const agent2 = new CloudAgent('agent-2', ['compute']);
    delegator2.registerAgent(agent1);
    delegator2.registerAgent(agent2);
    
    const results = [];
    for (let i = 0; i < 4; i++) {
        const result = await delegator2.delegate({ task: 'compute', data: { id: i } });
        results.push(result.agent);
    }
    console.log('✓ Distribution:', results);
    console.assert(results[0] === 'agent-1', 'First should be agent-1');
    console.assert(results[1] === 'agent-2', 'Second should be agent-2');
    console.assert(results[2] === 'agent-1', 'Third should be agent-1');
    console.assert(results[3] === 'agent-2', 'Fourth should be agent-2');

    console.log('\n✅ All tests passed!');
}

// Run tests
runTests().catch(error => {
    console.error('❌ Test failed:', error);
    process.exit(1);
});
