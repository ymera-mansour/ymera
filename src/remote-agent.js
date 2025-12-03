const https = require('https');
const http = require('http');
const { CloudAgent } = require('./agent');

/**
 * RemoteCloudAgent - Cloud agent that delegates to remote HTTP endpoints
 */
class RemoteCloudAgent extends CloudAgent {
    constructor(name, endpoint, capabilities = []) {
        super(name, capabilities);
        this.endpoint = endpoint;
    }

    /**
     * Process task by sending to remote endpoint
     * @private
     */
    async _process(task) {
        const url = new URL(this.endpoint);
        const protocol = url.protocol === 'https:' ? https : http;
        
        const postData = JSON.stringify({
            task: task.task,
            data: task.data
        });

        return new Promise((resolve, reject) => {
            const options = {
                hostname: url.hostname,
                port: url.port || (url.protocol === 'https:' ? 443 : 80),
                path: url.pathname + url.search,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(postData)
                }
            };

            const req = protocol.request(options, (res) => {
                let data = '';

                res.on('data', (chunk) => {
                    data += chunk;
                });

                res.on('end', () => {
                    if (res.statusCode >= 200 && res.statusCode < 300) {
                        try {
                            const result = JSON.parse(data);
                            resolve({
                                status: 'completed',
                                agent: this.name,
                                task: task.task,
                                result: result
                            });
                        } catch (error) {
                            reject(new Error(`Failed to parse response: ${error.message}`));
                        }
                    } else {
                        reject(new Error(`HTTP ${res.statusCode}: ${data}`));
                    }
                });
            });

            req.on('error', (error) => {
                reject(new Error(`Request failed: ${error.message}`));
            });

            req.write(postData);
            req.end();
        });
    }
}

module.exports = { RemoteCloudAgent };
