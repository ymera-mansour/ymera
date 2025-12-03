const http = require('http');
const { CloudAgentDelegator } = require('./src/delegator');
const { RemoteCloudAgent } = require('./src/remote-agent');

/**
 * Example demonstrating remote cloud agent delegation
 */
async function main() {
    console.log('=== Remote Cloud Agent Delegation Example ===\n');

    // Start a mock cloud service
    const server = http.createServer((req, res) => {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            const task = JSON.parse(body);
            console.log(`   [Cloud] Processing ${task.task} with data:`, task.data);
            
            // Simulate cloud processing
            const result = {
                processed: true,
                taskType: task.task,
                cloudRegion: 'us-east-1',
                processingTime: Math.random() * 100,
                result: task.data
            };
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(result));
        });
    });

    await new Promise(resolve => server.listen(9000, resolve));
    console.log('Mock cloud service running on http://localhost:9000\n');

    try {
        // Create delegator with remote cloud agent
        const delegator = new CloudAgentDelegator({
            maxRetries: 3,
            timeout: 5000
        });

        // Register a remote cloud agent
        const cloudAgent = new RemoteCloudAgent(
            'aws-lambda-processor',
            'http://localhost:9000/api/process',
            ['analyze', 'transform', 'compute']
        );
        delegator.registerAgent(cloudAgent);

        // Example 1: Analyze data in the cloud
        console.log('1. Delegating data analysis to cloud:');
        const result1 = await delegator.delegate({
            task: 'analyze',
            data: { dataset: 'sales-2024', metrics: ['revenue', 'growth'] }
        });
        console.log('   Result:', result1);

        // Example 2: Transform data in the cloud
        console.log('\n2. Delegating data transformation to cloud:');
        const result2 = await delegator.delegate({
            task: 'transform',
            data: { format: 'csv-to-json', rows: 5000 }
        });
        console.log('   Result:', result2);

        // Example 3: Compute intensive operation
        console.log('\n3. Delegating compute task to cloud:');
        const result3 = await delegator.delegate({
            task: 'compute',
            data: { operation: 'matrix-multiply', size: 1000 }
        });
        console.log('   Result:', result3);

        console.log('\n=== Cloud Delegation Complete ===');
        console.log(`Agent status: ${cloudAgent.status}`);
        console.log(`Agent endpoint: ${cloudAgent.endpoint}`);
    } finally {
        await new Promise(resolve => server.close(resolve));
        console.log('\nMock cloud service stopped');
    }
}

// Run example
main().catch(console.error);
