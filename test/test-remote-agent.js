const http = require('http');
const { CloudAgentDelegator } = require('../src/delegator');
const { RemoteCloudAgent } = require('../src/remote-agent');

/**
 * Test suite for remote cloud agent delegation
 */
async function runRemoteAgentTests() {
    console.log('Running Remote Cloud Agent Tests...\n');

    // Create a mock cloud server
    const server = http.createServer((req, res) => {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            try {
                const task = JSON.parse(body);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    processed: true,
                    taskType: task.task,
                    data: task.data,
                    timestamp: new Date().toISOString()
                }));
            } catch (error) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: error.message }));
            }
        });
    });

    // Start server
    await new Promise((resolve) => {
        server.listen(8888, () => {
            console.log('Mock cloud server started on port 8888\n');
            resolve();
        });
    });

    try {
        // Test 1: Create remote agent and delegate task
        console.log('Test 1: Delegate to remote cloud agent');
        const delegator = new CloudAgentDelegator();
        const remoteAgent = new RemoteCloudAgent(
            'cloud-processor',
            'http://localhost:8888/process',
            ['analyze', 'transform']
        );
        delegator.registerAgent(remoteAgent);

        const result1 = await delegator.delegate({
            task: 'analyze',
            data: { values: [10, 20, 30] }
        });
        console.log('✓ Result:', result1);
        console.assert(result1.status === 'completed', 'Task should complete');
        console.assert(result1.agent === 'cloud-processor', 'Should use cloud-processor agent');
        console.assert(result1.result.processed === true, 'Should be processed by remote server');

        // Test 2: Agent status tracking
        console.log('\nTest 2: Agent status tracking');
        console.log('✓ Agent status:', remoteAgent.status);
        console.assert(remoteAgent.status === 'idle', 'Agent should be idle after completion');

        // Test 3: Multiple remote delegations
        console.log('\nTest 3: Multiple remote delegations');
        const results = [];
        for (let i = 0; i < 3; i++) {
            const result = await delegator.delegate({
                task: 'transform',
                data: { id: i, value: i * 10 }
            });
            results.push(result.result.processed);
        }
        console.log('✓ All processed:', results);
        console.assert(results.every(r => r === true), 'All tasks should be processed');

        console.log('\n✅ All remote agent tests passed!');
    } finally {
        // Close server
        server.close();
        console.log('\nMock cloud server stopped');
    }
}

// Run tests
runRemoteAgentTests().catch(error => {
    console.error('❌ Test failed:', error);
    process.exit(1);
});
